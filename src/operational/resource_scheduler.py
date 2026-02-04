"""
Resource Scheduler
Allocates and manages resources (AI agents, compute) across workflows
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()


class Resource(BaseModel):
    """A computational resource (agent, service, etc.)"""
    resource_id: str
    resource_type: str  # agent, service, compute
    name: str
    capacity: int = 1
    current_load: int = 0
    available: bool = True
    metadata: Dict[str, Any] = {}


class ResourceScheduler:
    """Manages resource allocation for workflow tasks"""
    
    def __init__(self):
        self.logger = logger.bind(component="resource_scheduler")
        self.resources: Dict[str, Resource] = {}
    
    async def register_resource(self, resource: Resource) -> None:
        """Register a new resource"""
        self.resources[resource.resource_id] = resource
        self.logger.info("resource_registered", resource_id=resource.resource_id)
    
    async def allocate_resource(
        self, task_type: str, requirements: Dict[str, Any]
    ) -> Optional[str]:
        """Allocate a resource for a task"""
        # Find available resource matching requirements
        for resource in self.resources.values():
            if (resource.available and 
                resource.current_load < resource.capacity):
                resource.current_load += 1
                self.logger.info("resource_allocated", resource_id=resource.resource_id)
                return resource.resource_id
        return None
    
    async def release_resource(self, resource_id: str) -> None:
        """Release an allocated resource"""
        if resource_id in self.resources:
            self.resources[resource_id].current_load -= 1
            self.logger.info("resource_released", resource_id=resource_id)
