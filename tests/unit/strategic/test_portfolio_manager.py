"""Tests for Portfolio Manager"""

import pytest
from src.strategic.portfolio_manager import (
    PortfolioManager,
    TopicFrequency,
    TopicStatus,
)


@pytest.mark.asyncio
async def test_create_topic():
    """Test creating a new newsletter topic"""
    manager = PortfolioManager()
    
    topic = await manager.create_topic(
        name="CEO Insights",
        description="Weekly strategic insights for executives",
        target_audience=["CEOs", "Executives"],
        frequency=TopicFrequency.WEEKLY,
        priority=8,
    )
    
    assert topic.name == "CEO Insights"
    assert topic.status == TopicStatus.PLANNING
    assert topic.priority == 8
    assert topic.subscriber_count == 0


@pytest.mark.asyncio
async def test_activate_topic():
    """Test activating a topic"""
    manager = PortfolioManager()
    
    topic = await manager.create_topic(
        name="Test Topic",
        description="Test",
        target_audience=["Test"],
        frequency=TopicFrequency.WEEKLY,
    )
    
    activated = await manager.activate_topic(topic.topic_id)
    
    assert activated.status == TopicStatus.ACTIVE
    assert activated.activated_at is not None


@pytest.mark.asyncio
async def test_portfolio_metrics():
    """Test portfolio metrics calculation"""
    manager = PortfolioManager()
    
    # Create and activate topics
    topic1 = await manager.create_topic(
        name="Topic 1",
        description="Test",
        target_audience=["Test"],
        frequency=TopicFrequency.WEEKLY,
    )
    await manager.activate_topic(topic1.topic_id)
    await manager.update_topic_metrics(
        topic1.topic_id,
        subscriber_count=100,
        avg_open_rate=0.25,
    )
    
    metrics = await manager.get_portfolio_metrics()
    
    assert metrics.total_topics == 1
    assert metrics.active_topics == 1
    assert metrics.total_subscribers == 100
    assert metrics.avg_open_rate == 0.25
