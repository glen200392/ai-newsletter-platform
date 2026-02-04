"""
Strategic Planner
Develops and optimizes content strategy based on market intelligence and portfolio performance
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import structlog
from pydantic import BaseModel, Field

from .market_intelligence import MarketIntelligenceEngine, TopicOpportunity
from .portfolio_manager import PortfolioManager, NewsletterTopic, TopicFrequency

logger = structlog.get_logger()


class StrategyType(str, Enum):
    """Strategic initiative types"""
    EXPAND = "expand"  # Launch new topics
    OPTIMIZE = "optimize"  # Improve existing topics
    CONSOLIDATE = "consolidate"  # Merge or reduce topics
    PIVOT = "pivot"  # Major direction change


class StrategicInitiative(BaseModel):
    """A strategic initiative with action plan"""
    initiative_id: str
    strategy_type: StrategyType
    title: str
    description: str
    rationale: str
    expected_impact: Dict[str, Any]
    action_items: List[Dict[str, Any]]
    timeline_weeks: int
    confidence_level: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ContentStrategy(BaseModel):
    """Overall content strategy"""
    strategy_id: str
    period_start: datetime
    period_end: datetime
    objectives: List[str]
    key_initiatives: List[StrategicInitiative]
    resource_allocation: Dict[str, float]
    success_metrics: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StrategicPlanner:
    """
    Develops high-level strategy by:
    - Analyzing market intelligence
    - Evaluating portfolio performance
    - Identifying strategic opportunities
    - Creating action plans
    """

    def __init__(
        self,
        market_intelligence: MarketIntelligenceEngine,
        portfolio_manager: PortfolioManager,
    ):
        self.market_intelligence = market_intelligence
        self.portfolio_manager = portfolio_manager
        self.logger = logger.bind(component="strategic_planner")

    async def develop_strategy(
        self, planning_horizon_weeks: int = 12
    ) -> ContentStrategy:
        """
        Develop comprehensive content strategy
        
        Args:
            planning_horizon_weeks: Planning period in weeks
            
        Returns:
            ContentStrategy with initiatives and action plans
        """
        self.logger.info(
            "developing_strategy",
            horizon_weeks=planning_horizon_weeks,
        )
        
        # Gather inputs
        market_signals = await self.market_intelligence.scan_market()
        portfolio_metrics = await self.portfolio_manager.get_portfolio_metrics()
        existing_topics = await self.portfolio_manager.list_topics()
        
        # Identify opportunities
        opportunities = await self.market_intelligence.identify_opportunities(
            market_signals,
            [t.name for t in existing_topics],
        )
        
        # Analyze portfolio health
        optimization_results = await self.portfolio_manager.optimize_portfolio()
        
        # Generate strategic initiatives
        initiatives = []
        
        # Initiative 1: Topic expansion based on opportunities
        expansion_initiatives = self._plan_topic_expansion(
            opportunities, portfolio_metrics
        )
        initiatives.extend(expansion_initiatives)
        
        # Initiative 2: Portfolio optimization
        optimization_initiatives = self._plan_portfolio_optimization(
            optimization_results
        )
        initiatives.extend(optimization_initiatives)
        
        # Initiative 3: Content quality improvements
        quality_initiatives = self._plan_quality_improvements(existing_topics)
        initiatives.extend(quality_initiatives)
        
        # Define objectives
        objectives = self._define_strategic_objectives(
            portfolio_metrics, opportunities
        )
        
        # Allocate resources
        resource_allocation = self._allocate_resources(initiatives)
        
        # Define success metrics
        success_metrics = self._define_success_metrics(initiatives)
        
        strategy = ContentStrategy(
            strategy_id=f"strategy_{datetime.utcnow().strftime('%Y%m%d')}",
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow() + timedelta(weeks=planning_horizon_weeks),
            objectives=objectives,
            key_initiatives=initiatives,
            resource_allocation=resource_allocation,
            success_metrics=success_metrics,
        )
        
        self.logger.info(
            "strategy_developed",
            initiatives_count=len(initiatives),
            objectives_count=len(objectives),
        )
        
        return strategy

    def _plan_topic_expansion(
        self,
        opportunities: List[TopicOpportunity],
        portfolio_metrics: Any,
    ) -> List[StrategicInitiative]:
        """Plan new topic launches based on opportunities"""
        initiatives = []
        
        # Filter high-confidence opportunities
        top_opportunities = [
            opp for opp in opportunities
            if opp.recommended_action == "create" and opp.confidence_score >= 0.7
        ]
        
        # Limit based on current portfolio size
        max_new_topics = max(2, int(portfolio_metrics.active_topics * 0.2))
        top_opportunities = top_opportunities[:max_new_topics]
        
        for opp in top_opportunities:
            initiative = StrategicInitiative(
                initiative_id=f"expand_{opp.topic_name.lower().replace(' ', '_')}",
                strategy_type=StrategyType.EXPAND,
                title=f"Launch {opp.topic_name} Newsletter",
                description=f"Create new newsletter topic targeting {', '.join(opp.target_audience)}",
                rationale=opp.reasoning,
                expected_impact={
                    "estimated_subscribers": opp.market_size_estimate,
                    "growth_potential": opp.growth_trend,
                    "confidence": opp.confidence_score,
                },
                action_items=[
                    {
                        "action": "Define content structure",
                        "owner": "content_team",
                        "timeline_days": 7,
                    },
                    {
                        "action": "Configure AI agent",
                        "owner": "tech_team",
                        "timeline_days": 3,
                    },
                    {
                        "action": "Create initial content batch",
                        "owner": "content_team",
                        "timeline_days": 14,
                    },
                    {
                        "action": "Set up email campaigns",
                        "owner": "marketing_team",
                        "timeline_days": 5,
                    },
                    {
                        "action": "Launch to pilot group",
                        "owner": "product_team",
                        "timeline_days": 2,
                    },
                ],
                timeline_weeks=6,
                confidence_level=opp.confidence_score,
            )
            initiatives.append(initiative)
        
        return initiatives

    def _plan_portfolio_optimization(
        self, optimization_results: Dict[str, Any]
    ) -> List[StrategicInitiative]:
        """Plan optimization initiatives based on portfolio analysis"""
        initiatives = []
        
        recommendations = optimization_results.get("recommendations", [])
        
        # Group recommendations by action type
        actions_by_type: Dict[str, List[Dict]] = {}
        for rec in recommendations:
            action = rec["action"]
            if action not in actions_by_type:
                actions_by_type[action] = []
            actions_by_type[action].append(rec)
        
        # Create initiatives for each action type
        if "content_refresh" in actions_by_type:
            topics = actions_by_type["content_refresh"]
            initiative = StrategicInitiative(
                initiative_id="optimize_content_refresh",
                strategy_type=StrategyType.OPTIMIZE,
                title="Content Refresh for Underperforming Topics",
                description=f"Refresh content strategy for {len(topics)} topics",
                rationale="Multiple topics showing declining engagement",
                expected_impact={
                    "affected_topics": len(topics),
                    "expected_engagement_lift": "15-25%",
                },
                action_items=[
                    {
                        "action": "Conduct subscriber surveys",
                        "timeline_days": 7,
                    },
                    {
                        "action": "Analyze competitor content",
                        "timeline_days": 5,
                    },
                    {
                        "action": "Redesign content format",
                        "timeline_days": 10,
                    },
                    {
                        "action": "A/B test new approach",
                        "timeline_days": 14,
                    },
                ],
                timeline_weeks=6,
                confidence_level=0.7,
            )
            initiatives.append(initiative)
        
        if "consider_archiving" in actions_by_type:
            topics = actions_by_type["consider_archiving"]
            if len(topics) > 0:
                initiative = StrategicInitiative(
                    initiative_id="consolidate_underperformers",
                    strategy_type=StrategyType.CONSOLIDATE,
                    title="Consolidate or Archive Low-Performing Topics",
                    description=f"Evaluate {len(topics)} topics for archival",
                    rationale="Low health scores indicate poor product-market fit",
                    expected_impact={
                        "resource_savings": "20-30%",
                        "focus_improvement": "high",
                    },
                    action_items=[
                        {
                            "action": "Final performance review",
                            "timeline_days": 7,
                        },
                        {
                            "action": "Subscriber migration plan",
                            "timeline_days": 10,
                        },
                        {
                            "action": "Archive topics",
                            "timeline_days": 3,
                        },
                    ],
                    timeline_weeks=3,
                    confidence_level=0.8,
                )
                initiatives.append(initiative)
        
        if "scale_up" in actions_by_type:
            topics = actions_by_type["scale_up"]
            initiative = StrategicInitiative(
                initiative_id="scale_top_performers",
                strategy_type=StrategyType.EXPAND,
                title="Scale High-Performing Topics",
                description=f"Increase investment in {len(topics)} top topics",
                rationale="High engagement indicates strong product-market fit",
                expected_impact={
                    "subscriber_growth": "50-100%",
                    "revenue_impact": "high",
                },
                action_items=[
                    {
                        "action": "Increase content frequency",
                        "timeline_days": 7,
                    },
                    {
                        "action": "Launch paid promotion",
                        "timeline_days": 14,
                    },
                    {
                        "action": "Create spin-off content",
                        "timeline_days": 21,
                    },
                ],
                timeline_weeks=8,
                confidence_level=0.85,
            )
            initiatives.append(initiative)
        
        return initiatives

    def _plan_quality_improvements(
        self, existing_topics: List[NewsletterTopic]
    ) -> List[StrategicInitiative]:
        """Plan quality improvement initiatives"""
        initiatives = []
        
        # Calculate average quality metrics
        if not existing_topics:
            return initiatives
        
        avg_open_rate = sum(t.avg_open_rate for t in existing_topics) / len(
            existing_topics
        )
        
        # If overall quality is below threshold, create improvement initiative
        if avg_open_rate < 0.2:
            initiative = StrategicInitiative(
                initiative_id="improve_content_quality",
                strategy_type=StrategyType.OPTIMIZE,
                title="Portfolio-Wide Quality Enhancement",
                description="Systematic improvements to content quality across all topics",
                rationale=f"Average open rate ({avg_open_rate:.1%}) below target (20%)",
                expected_impact={
                    "target_open_rate": "25%",
                    "timeline": "12 weeks",
                },
                action_items=[
                    {
                        "action": "Implement content quality scoring",
                        "timeline_days": 7,
                    },
                    {
                        "action": "Update AI prompts for better output",
                        "timeline_days": 10,
                    },
                    {
                        "action": "Add human editorial review",
                        "timeline_days": 5,
                    },
                    {
                        "action": "Train editors on best practices",
                        "timeline_days": 3,
                    },
                ],
                timeline_weeks=4,
                confidence_level=0.75,
            )
            initiatives.append(initiative)
        
        return initiatives

    def _define_strategic_objectives(
        self, portfolio_metrics: Any, opportunities: List[TopicOpportunity]
    ) -> List[str]:
        """Define strategic objectives for the planning period"""
        objectives = []
        
        # Growth objectives
        if portfolio_metrics.active_topics < 10:
            objectives.append(
                f"Expand portfolio from {portfolio_metrics.active_topics} to "
                f"{portfolio_metrics.active_topics + 3} active topics"
            )
        
        objectives.append(
            f"Grow total subscriber base from {portfolio_metrics.total_subscribers:,} "
            f"to {int(portfolio_metrics.total_subscribers * 1.5):,}"
        )
        
        # Quality objectives
        target_open_rate = max(0.25, portfolio_metrics.avg_open_rate * 1.2)
        objectives.append(
            f"Improve average open rate from {portfolio_metrics.avg_open_rate:.1%} "
            f"to {target_open_rate:.1%}"
        )
        
        # Efficiency objectives
        objectives.append(
            "Reduce content generation cost per newsletter by 15% through optimization"
        )
        
        # Innovation objectives
        if len(opportunities) > 0:
            objectives.append(
                "Launch experimental topics in emerging high-opportunity areas"
            )
        
        return objectives

    def _allocate_resources(
        self, initiatives: List[StrategicInitiative]
    ) -> Dict[str, float]:
        """Allocate resources across initiatives"""
        total_confidence = sum(i.confidence_level for i in initiatives)
        
        allocation = {}
        for initiative in initiatives:
            weight = initiative.confidence_level / total_confidence if total_confidence > 0 else 0
            allocation[initiative.initiative_id] = weight
        
        return allocation

    def _define_success_metrics(
        self, initiatives: List[StrategicInitiative]
    ) -> Dict[str, Any]:
        """Define metrics to track strategy success"""
        return {
            "portfolio_growth": {
                "metric": "active_topics_count",
                "target": "+2-3 topics",
                "measurement": "monthly",
            },
            "subscriber_growth": {
                "metric": "total_subscribers",
                "target": "+50%",
                "measurement": "monthly",
            },
            "engagement": {
                "metric": "avg_open_rate",
                "target": ">25%",
                "measurement": "weekly",
            },
            "efficiency": {
                "metric": "cost_per_newsletter",
                "target": "-15%",
                "measurement": "monthly",
            },
            "initiative_completion": {
                "metric": "initiatives_on_track",
                "target": "80%",
                "measurement": "weekly",
            },
        }

    async def evaluate_strategy_execution(
        self, strategy: ContentStrategy
    ) -> Dict[str, Any]:
        """Evaluate how well the strategy is being executed"""
        self.logger.info("evaluating_strategy_execution", strategy_id=strategy.strategy_id)
        
        # Get current portfolio state
        portfolio_metrics = await self.portfolio_manager.get_portfolio_metrics()
        
        # Evaluate each initiative
        initiative_status = []
        for initiative in strategy.key_initiatives:
            completed_actions = sum(
                1 for item in initiative.action_items
                if item.get("status") == "completed"
            )
            total_actions = len(initiative.action_items)
            
            progress = (
                (completed_actions / total_actions * 100) if total_actions > 0 else 0
            )
            
            initiative_status.append({
                "initiative_id": initiative.initiative_id,
                "title": initiative.title,
                "progress_pct": progress,
                "status": "on_track" if progress >= 50 else "behind",
            })
        
        # Calculate overall execution score
        avg_progress = sum(i["progress_pct"] for i in initiative_status) / len(
            initiative_status
        ) if initiative_status else 0
        
        return {
            "strategy_id": strategy.strategy_id,
            "execution_score": avg_progress / 100,
            "initiatives_status": initiative_status,
            "portfolio_metrics": portfolio_metrics,
            "recommendations": self._generate_execution_recommendations(
                avg_progress, initiative_status
            ),
        }

    def _generate_execution_recommendations(
        self, avg_progress: float, initiative_status: List[Dict]
    ) -> List[str]:
        """Generate recommendations for strategy execution"""
        recommendations = []
        
        if avg_progress < 30:
            recommendations.append("Strategy execution significantly behind schedule - review resource allocation")
        elif avg_progress < 50:
            recommendations.append("Consider reprioritizing initiatives to focus on highest-impact items")
        
        behind_initiatives = [
            i for i in initiative_status if i["status"] == "behind"
        ]
        if len(behind_initiatives) > len(initiative_status) / 2:
            recommendations.append(
                f"{len(behind_initiatives)} initiatives are behind - conduct retrospective"
            )
        
        if avg_progress > 80:
            recommendations.append("Excellent execution - consider advancing timeline for next strategy cycle")
        
        return recommendations
