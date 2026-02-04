"""
Portfolio Manager
Manages the lifecycle of all newsletter topics (create, monitor, optimize, archive)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import structlog
from pydantic import BaseModel, Field
import uuid

logger = structlog.get_logger()


class TopicStatus(str, Enum):
    """Newsletter topic status"""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class TopicFrequency(str, Enum):
    """Newsletter frequency"""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class NewsletterTopic(BaseModel):
    """Newsletter topic configuration"""
    topic_id: str = Field(default_factory=lambda: f"topic_{uuid.uuid4().hex[:12]}")
    name: str
    description: str
    target_audience: List[str]
    frequency: TopicFrequency
    status: TopicStatus = TopicStatus.PLANNING
    
    # Agent configuration
    agent_config: Dict[str, Any] = Field(default_factory=dict)
    
    # Content configuration
    content_sections: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Metrics
    subscriber_count: int = 0
    avg_open_rate: float = 0.0
    avg_click_rate: float = 0.0
    unsubscribe_rate: float = 0.0
    
    # Lifecycle
    created_at: datetime = Field(default_factory=datetime.utcnow)
    activated_at: Optional[datetime] = None
    last_sent_at: Optional[datetime] = None
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PortfolioMetrics(BaseModel):
    """Overall portfolio health metrics"""
    total_topics: int
    active_topics: int
    total_subscribers: int
    avg_open_rate: float
    avg_click_rate: float
    revenue_per_subscriber: float = 0.0
    calculated_at: datetime = Field(default_factory=datetime.utcnow)


class PortfolioManager:
    """
    Manages the entire portfolio of newsletter topics:
    - Create new topics based on opportunities
    - Monitor topic performance
    - Optimize resource allocation
    - Archive underperforming topics
    """

    def __init__(self):
        self.logger = logger.bind(component="portfolio_manager")
        self.topics: Dict[str, NewsletterTopic] = {}

    async def create_topic(
        self,
        name: str,
        description: str,
        target_audience: List[str],
        frequency: TopicFrequency,
        agent_config: Optional[Dict[str, Any]] = None,
        content_sections: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[List[str]] = None,
        priority: int = 5,
    ) -> NewsletterTopic:
        """
        Create a new newsletter topic
        
        Args:
            name: Topic name
            description: Topic description
            target_audience: Target audience segments
            frequency: Publication frequency
            agent_config: AI agent configuration
            content_sections: Content structure definition
            tags: Topic tags for categorization
            priority: Priority level (1-10)
            
        Returns:
            Created NewsletterTopic instance
        """
        topic = NewsletterTopic(
            name=name,
            description=description,
            target_audience=target_audience,
            frequency=frequency,
            agent_config=agent_config or {},
            content_sections=content_sections or [],
            tags=tags or [],
            priority=priority,
        )
        
        self.topics[topic.topic_id] = topic
        
        self.logger.info(
            "topic_created",
            topic_id=topic.topic_id,
            name=name,
            frequency=frequency.value,
            audience=target_audience,
        )
        
        return topic

    async def activate_topic(self, topic_id: str) -> NewsletterTopic:
        """Activate a topic to start content generation"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")
        
        if topic.status != TopicStatus.PLANNING:
            raise ValueError(f"Topic {topic_id} is not in planning status")
        
        topic.status = TopicStatus.ACTIVE
        topic.activated_at = datetime.utcnow()
        
        self.logger.info("topic_activated", topic_id=topic_id, name=topic.name)
        
        return topic

    async def pause_topic(self, topic_id: str, reason: str = "") -> NewsletterTopic:
        """Temporarily pause a topic"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")
        
        topic.status = TopicStatus.PAUSED
        topic.metadata["pause_reason"] = reason
        topic.metadata["paused_at"] = datetime.utcnow().isoformat()
        
        self.logger.info(
            "topic_paused",
            topic_id=topic_id,
            name=topic.name,
            reason=reason,
        )
        
        return topic

    async def archive_topic(self, topic_id: str, reason: str = "") -> NewsletterTopic:
        """Archive a topic (soft delete)"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")
        
        topic.status = TopicStatus.ARCHIVED
        topic.metadata["archive_reason"] = reason
        topic.metadata["archived_at"] = datetime.utcnow().isoformat()
        
        self.logger.info(
            "topic_archived",
            topic_id=topic_id,
            name=topic.name,
            reason=reason,
        )
        
        return topic

    async def update_topic_metrics(
        self,
        topic_id: str,
        subscriber_count: Optional[int] = None,
        avg_open_rate: Optional[float] = None,
        avg_click_rate: Optional[float] = None,
        unsubscribe_rate: Optional[float] = None,
    ) -> NewsletterTopic:
        """Update topic performance metrics"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")
        
        if subscriber_count is not None:
            topic.subscriber_count = subscriber_count
        if avg_open_rate is not None:
            topic.avg_open_rate = avg_open_rate
        if avg_click_rate is not None:
            topic.avg_click_rate = avg_click_rate
        if unsubscribe_rate is not None:
            topic.unsubscribe_rate = unsubscribe_rate
        
        self.logger.debug(
            "topic_metrics_updated",
            topic_id=topic_id,
            subscribers=topic.subscriber_count,
            open_rate=topic.avg_open_rate,
        )
        
        return topic

    async def get_portfolio_metrics(self) -> PortfolioMetrics:
        """Calculate overall portfolio metrics"""
        active_topics = [
            t for t in self.topics.values() if t.status == TopicStatus.ACTIVE
        ]
        
        if not active_topics:
            return PortfolioMetrics(
                total_topics=len(self.topics),
                active_topics=0,
                total_subscribers=0,
                avg_open_rate=0.0,
                avg_click_rate=0.0,
            )
        
        total_subscribers = sum(t.subscriber_count for t in active_topics)
        avg_open_rate = sum(t.avg_open_rate for t in active_topics) / len(active_topics)
        avg_click_rate = sum(t.avg_click_rate for t in active_topics) / len(active_topics)
        
        return PortfolioMetrics(
            total_topics=len(self.topics),
            active_topics=len(active_topics),
            total_subscribers=total_subscribers,
            avg_open_rate=avg_open_rate,
            avg_click_rate=avg_click_rate,
        )

    async def optimize_portfolio(self) -> Dict[str, Any]:
        """
        Analyze portfolio and provide optimization recommendations
        
        Returns:
            Optimization recommendations and actions
        """
        self.logger.info("starting_portfolio_optimization")
        
        active_topics = [
            t for t in self.topics.values() if t.status == TopicStatus.ACTIVE
        ]
        
        recommendations = []
        actions_taken = []
        
        # Identify underperforming topics
        for topic in active_topics:
            health_score = self._calculate_topic_health(topic)
            
            if health_score < 0.3:
                recommendations.append({
                    "topic_id": topic.topic_id,
                    "topic_name": topic.name,
                    "action": "consider_archiving",
                    "reason": f"Low health score: {health_score:.2f}",
                    "health_score": health_score,
                })
            elif health_score < 0.5:
                recommendations.append({
                    "topic_id": topic.topic_id,
                    "topic_name": topic.name,
                    "action": "content_refresh",
                    "reason": f"Moderate health score: {health_score:.2f}",
                    "health_score": health_score,
                })
        
        # Identify high-performers for scaling
        top_performers = sorted(
            active_topics,
            key=lambda t: self._calculate_topic_health(t),
            reverse=True,
        )[:3]
        
        for topic in top_performers:
            health_score = self._calculate_topic_health(topic)
            if health_score > 0.7:
                recommendations.append({
                    "topic_id": topic.topic_id,
                    "topic_name": topic.name,
                    "action": "scale_up",
                    "reason": f"High performance: {health_score:.2f}",
                    "health_score": health_score,
                })
        
        # Resource allocation optimization
        total_priority = sum(t.priority for t in active_topics)
        if total_priority > 0:
            for topic in active_topics:
                allocated_percentage = (topic.priority / total_priority) * 100
                topic.metadata["resource_allocation_pct"] = allocated_percentage
        
        self.logger.info(
            "portfolio_optimization_completed",
            recommendations_count=len(recommendations),
            active_topics=len(active_topics),
        )
        
        return {
            "recommendations": recommendations,
            "actions_taken": actions_taken,
            "portfolio_health": await self.get_portfolio_metrics(),
        }

    def _calculate_topic_health(self, topic: NewsletterTopic) -> float:
        """Calculate topic health score (0-1)"""
        if topic.subscriber_count == 0:
            return 0.5  # New topic, neutral score
        
        # Weighted health calculation
        open_rate_score = min(topic.avg_open_rate / 0.3, 1.0)  # 30% is excellent
        click_rate_score = min(topic.avg_click_rate / 0.1, 1.0)  # 10% is excellent
        churn_score = max(0, 1 - (topic.unsubscribe_rate / 0.05))  # <5% is good
        
        health = (
            (open_rate_score * 0.4) +
            (click_rate_score * 0.3) +
            (churn_score * 0.3)
        )
        
        return health

    async def get_topic(self, topic_id: str) -> Optional[NewsletterTopic]:
        """Get topic by ID"""
        return self.topics.get(topic_id)

    async def list_topics(
        self,
        status: Optional[TopicStatus] = None,
        tags: Optional[List[str]] = None,
    ) -> List[NewsletterTopic]:
        """List topics with optional filters"""
        topics = list(self.topics.values())
        
        if status:
            topics = [t for t in topics if t.status == status]
        
        if tags:
            topics = [t for t in topics if any(tag in t.tags for tag in tags)]
        
        # Sort by priority and created_at
        topics.sort(key=lambda t: (t.priority, t.created_at), reverse=True)
        
        return topics

    async def get_topic_insights(self, topic_id: str) -> Dict[str, Any]:
        """Get detailed insights for a specific topic"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")
        
        health_score = self._calculate_topic_health(topic)
        
        # Calculate trends (would use historical data in production)
        subscriber_trend = "stable"  # TODO: Calculate from historical data
        engagement_trend = "stable"  # TODO: Calculate from historical data
        
        return {
            "topic": topic,
            "health_score": health_score,
            "subscriber_trend": subscriber_trend,
            "engagement_trend": engagement_trend,
            "recommendations": self._generate_topic_recommendations(topic, health_score),
        }

    def _generate_topic_recommendations(
        self, topic: NewsletterTopic, health_score: float
    ) -> List[str]:
        """Generate actionable recommendations for a topic"""
        recommendations = []
        
        if health_score < 0.3:
            recommendations.append("Consider major content overhaul or archiving")
            recommendations.append("Survey subscribers for detailed feedback")
        elif health_score < 0.5:
            recommendations.append("Test new content formats with A/B testing")
            recommendations.append("Review and refresh content sources")
        elif health_score < 0.7:
            recommendations.append("Maintain current strategy with minor optimizations")
            recommendations.append("Monitor competitor newsletters for insights")
        else:
            recommendations.append("Scale up promotion efforts")
            recommendations.append("Consider creating related spin-off topics")
            recommendations.append("Document success factors for replication")
        
        if topic.avg_open_rate < 0.15:
            recommendations.append("Improve email subject lines and preview text")
        
        if topic.avg_click_rate < 0.03:
            recommendations.append("Add more actionable content and clear CTAs")
        
        if topic.unsubscribe_rate > 0.05:
            recommendations.append("Review content relevance and frequency")
        
        return recommendations
