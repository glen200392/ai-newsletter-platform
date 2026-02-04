"""
Workflow Engine
Orchestrates multi-step content generation and distribution workflows
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import asyncio
import structlog
from pydantic import BaseModel, Field
import uuid

logger = structlog.get_logger()


class WorkflowStatus(str, Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    """Individual task status"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowTask(BaseModel):
    """A single task within a workflow"""
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str
    task_type: str  # scan_market, generate_content, qa_review, send_email
    dependencies: List[str] = Field(default_factory=list)
    assigned_to: Optional[str] = None  # Agent or service ID
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3


class Workflow(BaseModel):
    """A complete workflow definition"""
    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:12]}")
    workflow_type: str  # content_generation, market_scan, portfolio_optimization
    topic_id: Optional[str] = None
    status: WorkflowStatus = WorkflowStatus.PENDING
    tasks: List[WorkflowTask] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowEngine:
    """
    Orchestrates complex multi-step workflows:
    - Content generation pipeline
    - Market scanning workflows
    - Portfolio optimization processes
    """

    def __init__(self):
        self.logger = logger.bind(component="workflow_engine")
        self.workflows: Dict[str, Workflow] = {}
        self.running_workflows: set = set()

    async def create_workflow(
        self, workflow_type: str, topic_id: Optional[str] = None, **kwargs
    ) -> Workflow:
        """
        Create a new workflow based on type
        
        Args:
            workflow_type: Type of workflow to create
            topic_id: Associated topic ID (for content workflows)
            **kwargs: Additional workflow parameters
            
        Returns:
            Created Workflow instance
        """
        workflow = Workflow(
            workflow_type=workflow_type,
            topic_id=topic_id,
            metadata=kwargs,
        )
        
        # Build task list based on workflow type
        if workflow_type == "content_generation":
            workflow.tasks = self._build_content_generation_tasks(topic_id, kwargs)
        elif workflow_type == "market_scan":
            workflow.tasks = self._build_market_scan_tasks(kwargs)
        elif workflow_type == "portfolio_optimization":
            workflow.tasks = self._build_portfolio_optimization_tasks(kwargs)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        self.workflows[workflow.workflow_id] = workflow
        
        self.logger.info(
            "workflow_created",
            workflow_id=workflow.workflow_id,
            workflow_type=workflow_type,
            task_count=len(workflow.tasks),
        )
        
        return workflow

    def _build_content_generation_tasks(
        self, topic_id: str, config: Dict[str, Any]
    ) -> List[WorkflowTask]:
        """Build tasks for content generation workflow"""
        tasks = [
            WorkflowTask(
                name="Research Topics",
                task_type="research",
                input_data={"topic_id": topic_id},
                assigned_to="research_agent",
            ),
            WorkflowTask(
                name="Generate Content",
                task_type="generate_content",
                dependencies=["task_research"],
                input_data={"topic_id": topic_id},
                assigned_to="content_agent",
            ),
            WorkflowTask(
                name="Quality Assurance",
                task_type="qa_review",
                dependencies=["task_generate_content"],
                assigned_to="qa_agent",
            ),
            WorkflowTask(
                name="Format Email",
                task_type="format_email",
                dependencies=["task_qa_review"],
                assigned_to="formatter_service",
            ),
            WorkflowTask(
                name="Send Newsletter",
                task_type="send_email",
                dependencies=["task_format_email"],
                assigned_to="email_service",
            ),
            WorkflowTask(
                name="Track Delivery",
                task_type="track_delivery",
                dependencies=["task_send_newsletter"],
                assigned_to="analytics_service",
            ),
        ]
        
        # Set proper dependencies using actual task IDs
        for i, task in enumerate(tasks):
            if i > 0:
                task.dependencies = [tasks[i - 1].task_id]
        
        return tasks

    def _build_market_scan_tasks(self, config: Dict[str, Any]) -> List[WorkflowTask]:
        """Build tasks for market scanning workflow"""
        sources = config.get("sources", ["news_api", "reddit", "hackernews"])
        
        # Create parallel scan tasks for each source
        scan_tasks = [
            WorkflowTask(
                name=f"Scan {source}",
                task_type="scan_source",
                input_data={"source": source},
                assigned_to=f"scanner_{source}",
            )
            for source in sources
        ]
        
        # Aggregation task depends on all scan tasks
        aggregate_task = WorkflowTask(
            name="Aggregate Signals",
            task_type="aggregate_signals",
            dependencies=[t.task_id for t in scan_tasks],
            assigned_to="aggregator_service",
        )
        
        # Analysis task
        analyze_task = WorkflowTask(
            name="Analyze Opportunities",
            task_type="analyze_opportunities",
            dependencies=[aggregate_task.task_id],
            assigned_to="analysis_agent",
        )
        
        return scan_tasks + [aggregate_task, analyze_task]

    def _build_portfolio_optimization_tasks(
        self, config: Dict[str, Any]
    ) -> List[WorkflowTask]:
        """Build tasks for portfolio optimization workflow"""
        return [
            WorkflowTask(
                name="Gather Metrics",
                task_type="gather_metrics",
                assigned_to="metrics_collector",
            ),
            WorkflowTask(
                name="Analyze Performance",
                task_type="analyze_performance",
                dependencies=["task_gather_metrics"],
                assigned_to="analyzer_agent",
            ),
            WorkflowTask(
                name="Generate Recommendations",
                task_type="generate_recommendations",
                dependencies=["task_analyze_performance"],
                assigned_to="recommendation_engine",
            ),
            WorkflowTask(
                name="Create Action Plan",
                task_type="create_action_plan",
                dependencies=["task_generate_recommendations"],
                assigned_to="planning_service",
            ),
        ]

    async def start_workflow(self, workflow_id: str) -> Workflow:
        """Start executing a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if workflow.status != WorkflowStatus.PENDING:
            raise ValueError(f"Workflow {workflow_id} already started or completed")
        
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.utcnow()
        self.running_workflows.add(workflow_id)
        
        self.logger.info("workflow_started", workflow_id=workflow_id)
        
        # Start workflow execution in background
        asyncio.create_task(self._execute_workflow(workflow))
        
        return workflow

    async def _execute_workflow(self, workflow: Workflow) -> None:
        """Execute workflow tasks respecting dependencies"""
        try:
            completed_tasks = set()
            failed_tasks = set()
            
            while len(completed_tasks) < len(workflow.tasks):
                # Find tasks ready to run
                ready_tasks = [
                    task
                    for task in workflow.tasks
                    if task.status == TaskStatus.PENDING
                    and all(dep in completed_tasks for dep in task.dependencies)
                ]
                
                if not ready_tasks:
                    if failed_tasks:
                        # Some tasks failed and blocked downstream tasks
                        break
                    # All tasks are either running or waiting
                    await asyncio.sleep(1)
                    continue
                
                # Execute ready tasks in parallel
                execution_tasks = [
                    self._execute_task(workflow, task) for task in ready_tasks
                ]
                results = await asyncio.gather(*execution_tasks, return_exceptions=True)
                
                # Process results
                for task, result in zip(ready_tasks, results):
                    if isinstance(result, Exception):
                        task.status = TaskStatus.FAILED
                        task.error_message = str(result)
                        failed_tasks.add(task.task_id)
                        self.logger.error(
                            "task_failed",
                            workflow_id=workflow.workflow_id,
                            task_id=task.task_id,
                            error=str(result),
                        )
                    else:
                        task.status = TaskStatus.COMPLETED
                        task.output_data = result
                        completed_tasks.add(task.task_id)
                        self.logger.info(
                            "task_completed",
                            workflow_id=workflow.workflow_id,
                            task_id=task.task_id,
                        )
            
            # Update workflow status
            if failed_tasks:
                workflow.status = WorkflowStatus.FAILED
            else:
                workflow.status = WorkflowStatus.COMPLETED
            
            workflow.completed_at = datetime.utcnow()
            
            self.logger.info(
                "workflow_completed",
                workflow_id=workflow.workflow_id,
                status=workflow.status.value,
                duration_seconds=(
                    workflow.completed_at - workflow.started_at
                ).total_seconds()
                if workflow.started_at
                else 0,
            )
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            self.logger.error(
                "workflow_execution_failed",
                workflow_id=workflow.workflow_id,
                error=str(e),
            )
        finally:
            self.running_workflows.discard(workflow.workflow_id)

    async def _execute_task(self, workflow: Workflow, task: WorkflowTask) -> Dict[str, Any]:
        """Execute a single task"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        self.logger.info(
            "task_started",
            workflow_id=workflow.workflow_id,
            task_id=task.task_id,
            task_type=task.task_type,
        )
        
        try:
            # Simulate task execution (replace with actual implementation)
            await asyncio.sleep(1)  # Simulate work
            
            # In production, this would dispatch to actual services/agents
            result = {
                "status": "success",
                "task_type": task.task_type,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.completed_at = datetime.utcnow()
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                self.logger.warning(
                    "task_retry",
                    workflow_id=workflow.workflow_id,
                    task_id=task.task_id,
                    retry_count=task.retry_count,
                )
                return await self._execute_task(workflow, task)
            
            raise

    async def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID"""
        return self.workflows.get(workflow_id)

    async def list_workflows(
        self,
        workflow_type: Optional[str] = None,
        status: Optional[WorkflowStatus] = None,
    ) -> List[Workflow]:
        """List workflows with optional filters"""
        workflows = list(self.workflows.values())
        
        if workflow_type:
            workflows = [w for w in workflows if w.workflow_type == workflow_type]
        
        if status:
            workflows = [w for w in workflows if w.status == status]
        
        # Sort by created_at descending
        workflows.sort(key=lambda w: w.created_at, reverse=True)
        
        return workflows

    async def cancel_workflow(self, workflow_id: str) -> Workflow:
        """Cancel a running workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if workflow.status != WorkflowStatus.RUNNING:
            raise ValueError(f"Workflow {workflow_id} is not running")
        
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.utcnow()
        self.running_workflows.discard(workflow_id)
        
        self.logger.info("workflow_cancelled", workflow_id=workflow_id)
        
        return workflow

    async def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get overall workflow execution metrics"""
        total = len(self.workflows)
        running = len(self.running_workflows)
        completed = len([w for w in self.workflows.values() if w.status == WorkflowStatus.COMPLETED])
        failed = len([w for w in self.workflows.values() if w.status == WorkflowStatus.FAILED])
        
        return {
            "total_workflows": total,
            "running": running,
            "completed": completed,
            "failed": failed,
            "success_rate": (completed / total * 100) if total > 0 else 0,
        }
