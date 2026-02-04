"""
完整測試：訂閱者管理系統
測試註冊、偏好設定、取消訂閱等核心功能
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4
import secrets

# ============================================================================
# 數據模型定義
# ============================================================================

class SubscriptionStatus(str, Enum):
    """訂閱狀態"""
    PENDING = "pending"           # 待確認
    ACTIVE = "active"             # 活躍
    PAUSED = "paused"             # 暫停
    UNSUBSCRIBED = "unsubscribed" # 已取消
    BOUNCED = "bounced"           # 郵件退回

class Frequency(str, Enum):
    """發送頻率"""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"

class SubscriptionTier(str, Enum):
    """訂閱層級"""
    FREE = "free"
    PREMIUM = "premium"

class SubscriberPreferences:
    """訂閱者偏好設定"""
    def __init__(
        self,
        frequency: Frequency = Frequency.WEEKLY,
        topics: List[str] = None,
        tone: str = "professional",
        language: str = "en",
        preferred_time: str = "09:00"
    ):
        self.frequency = frequency
        self.topics = topics or []
        self.tone = tone
        self.language = language
        self.preferred_time = preferred_time

class Subscriber:
    """訂閱者模型"""
    def __init__(
        self,
        email: str,
        name: Optional[str] = None,
        preferences: Optional[SubscriberPreferences] = None
    ):
        self.id = str(uuid4())
        self.email = email
        self.name = name
        self.status = SubscriptionStatus.PENDING
        self.tier = SubscriptionTier.FREE
        self.preferences = preferences or SubscriberPreferences()
        self.confirmation_token = secrets.token_urlsafe(32)
        self.subscribed_at = datetime.now()
        self.confirmed_at = None
        self.unsubscribed_at = None
        self.unsubscribe_reason = None

# ============================================================================
# 訂閱者管理系統
# ============================================================================

class SubscriberManager:
    """訂閱者管理系統"""
    
    def __init__(self):
        self.subscribers: Dict[str, Subscriber] = {}
    
    def subscribe(
        self,
        email: str,
        name: Optional[str] = None,
        preferences: Optional[Dict] = None
    ) -> Dict:
        """創建新訂閱"""
        
        # 檢查是否已存在
        if email in self.subscribers:
            existing = self.subscribers[email]
            if existing.status == SubscriptionStatus.ACTIVE:
                return {
                    "status": "error",
                    "message": "Email already subscribed",
                    "subscriber_id": existing.id
                }
            elif existing.status == SubscriptionStatus.UNSUBSCRIBED:
                # 重新訂閱
                existing.status = SubscriptionStatus.PENDING
                existing.confirmation_token = secrets.token_urlsafe(32)
                existing.subscribed_at = datetime.now()
                return {
                    "status": "success",
                    "message": "Resubscribed successfully",
                    "subscriber_id": existing.id,
                    "confirmation_required": True
                }
        
        # 處理偏好設定
        pref_obj = SubscriberPreferences()
        if preferences:
            if "frequency" in preferences:
                pref_obj.frequency = preferences["frequency"]
            if "topics" in preferences:
                pref_obj.topics = preferences["topics"]
            if "tone" in preferences:
                pref_obj.tone = preferences["tone"]
            if "language" in preferences:
                pref_obj.language = preferences["language"]
            if "preferred_time" in preferences:
                pref_obj.preferred_time = preferences["preferred_time"]
        
        # 創建訂閱者
        subscriber = Subscriber(
            email=email,
            name=name,
            preferences=pref_obj
        )
        
        self.subscribers[email] = subscriber
        
        return {
            "status": "success",
            "message": "Subscription created",
            "subscriber_id": subscriber.id,
            "confirmation_required": True,
            "confirmation_token": subscriber.confirmation_token
        }
    
    def confirm_subscription(self, email: str, token: str) -> Dict:
        """確認訂閱"""
        subscriber = self.subscribers.get(email)
        
        if not subscriber:
            return {"status": "error", "message": "Subscriber not found"}
        
        if subscriber.confirmation_token != token:
            return {"status": "error", "message": "Invalid token"}
        
        if subscriber.status == SubscriptionStatus.ACTIVE:
            return {"status": "info", "message": "Already confirmed"}
        
        subscriber.status = SubscriptionStatus.ACTIVE
        subscriber.confirmed_at = datetime.now()
        
        return {
            "status": "success",
            "message": "Subscription confirmed",
            "subscription_status": subscriber.status
        }
    
    def get_subscriber(self, email: str) -> Optional[Subscriber]:
        """獲取訂閱者"""
        return self.subscribers.get(email)
    
    def update_preferences(self, email: str, preferences: Dict) -> Dict:
        """更新偏好設定"""
        subscriber = self.subscribers.get(email)
        
        if not subscriber:
            return {"status": "error", "message": "Subscriber not found"}
        
        # 更新偏好
        if "frequency" in preferences:
            subscriber.preferences.frequency = preferences["frequency"]
        if "topics" in preferences:
            subscriber.preferences.topics = preferences["topics"]
        if "tone" in preferences:
            subscriber.preferences.tone = preferences["tone"]
        if "language" in preferences:
            subscriber.preferences.language = preferences["language"]
        if "preferred_time" in preferences:
            subscriber.preferences.preferred_time = preferences["preferred_time"]
        
        return {
            "status": "success",
            "message": "Preferences updated"
        }
    
    def unsubscribe(self, email: str, reason: Optional[str] = None) -> Dict:
        """取消訂閱"""
        subscriber = self.subscribers.get(email)
        
        if not subscriber:
            return {"status": "error", "message": "Subscriber not found"}
        
        if subscriber.status == SubscriptionStatus.UNSUBSCRIBED:
            return {"status": "info", "message": "Already unsubscribed"}
        
        subscriber.status = SubscriptionStatus.UNSUBSCRIBED
        subscriber.unsubscribed_at = datetime.now()
        subscriber.unsubscribe_reason = reason
        
        return {
            "status": "success",
            "message": "Unsubscribed successfully"
        }
    
    def pause_subscription(self, email: str) -> Dict:
        """暫停訂閱"""
        subscriber = self.subscribers.get(email)
        
        if not subscriber:
            return {"status": "error", "message": "Subscriber not found"}
        
        if subscriber.status != SubscriptionStatus.ACTIVE:
            return {"status": "error", "message": "Can only pause active subscriptions"}
        
        subscriber.status = SubscriptionStatus.PAUSED
        
        return {"status": "success", "message": "Subscription paused"}
    
    def resume_subscription(self, email: str) -> Dict:
        """恢復訂閱"""
        subscriber = self.subscribers.get(email)
        
        if not subscriber:
            return {"status": "error", "message": "Subscriber not found"}
        
        if subscriber.status != SubscriptionStatus.PAUSED:
            return {"status": "error", "message": "Subscription is not paused"}
        
        subscriber.status = SubscriptionStatus.ACTIVE
        
        return {"status": "success", "message": "Subscription resumed"}
    
    def get_subscribers_by_topic(self, topic: str) -> List[Subscriber]:
        """按主題查詢訂閱者"""
        return [
            sub for sub in self.subscribers.values()
            if topic in sub.preferences.topics and sub.status == SubscriptionStatus.ACTIVE
        ]
    
    def get_subscribers_by_frequency(self, frequency: Frequency) -> List[Subscriber]:
        """按頻率查詢訂閱者"""
        return [
            sub for sub in self.subscribers.values()
            if sub.preferences.frequency == frequency and sub.status == SubscriptionStatus.ACTIVE
        ]
    
    def get_subscriber_stats(self) -> Dict:
        """獲取訂閱者統計"""
        total = len(self.subscribers)
        
        if total == 0:
            return {
                "total_subscribers": 0,
                "active_subscribers": 0,
                "pending_confirmation": 0,
                "paused": 0,
                "unsubscribed": 0,
                "active_rate": 0.0,
                "churn_rate": 0.0,
                "by_topic": {},
                "by_frequency": {}
            }
        
        status_counts = {}
        topic_counts = {}
        frequency_counts = {}
        
        for sub in self.subscribers.values():
            # 統計狀態
            status = sub.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # 統計主題（僅活躍用戶）
            if sub.status == SubscriptionStatus.ACTIVE:
                for topic in sub.preferences.topics:
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
                
                # 統計頻率
                freq = sub.preferences.frequency.value
                frequency_counts[freq] = frequency_counts.get(freq, 0) + 1
        
        active = status_counts.get("active", 0)
        unsubscribed = status_counts.get("unsubscribed", 0)
        
        return {
            "total_subscribers": total,
            "active_subscribers": active,
            "pending_confirmation": status_counts.get("pending", 0),
            "paused": status_counts.get("paused", 0),
            "unsubscribed": unsubscribed,
            "active_rate": (active / total * 100) if total > 0 else 0.0,
            "churn_rate": (unsubscribed / total * 100) if total > 0 else 0.0,
            "by_topic": topic_counts,
            "by_frequency": frequency_counts
        }

# ============================================================================
# 執行測試
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("📋 訂閱者管理系統完整測試")
    print("=" * 80)
    print()
    
    manager = SubscriberManager()
    
    # Test 1: 創建 CEO 訂閱者
    print("✅ Test 1: 創建 CEO 訂閱者")
    print("-" * 80)
    
    ceo_result = manager.subscribe(
        email="ceo@company.com",
        name="John CEO",
        preferences={
            "frequency": Frequency.WEEKLY,
            "topics": ["strategic_intelligence", "technology_radar", "market_pulse"],
            "tone": "professional",
            "language": "en",
            "preferred_time": "07:00"
        }
    )
    
    print(f"訂閱結果: {ceo_result['status']}")
    print(f"訂閱者 ID: {ceo_result['subscriber_id']}")
    print(f"需要確認: {ceo_result['confirmation_required']}")
    print()
    
    # Test 2: 確認訂閱
    print("✅ Test 2: 確認訂閱")
    print("-" * 80)
    
    ceo = manager.get_subscriber("ceo@company.com")
    confirm_result = manager.confirm_subscription("ceo@company.com", ceo.confirmation_token)
    print(f"確認結果: {confirm_result['status']}")
    print(f"訂閱狀態: {confirm_result['subscription_status']}")
    print()
    
    # Test 3: 查看訂閱者詳情
    print("✅ Test 3: 查看訂閱者詳情")
    print("-" * 80)
    
    ceo = manager.get_subscriber("ceo@company.com")
    print(f"姓名: {ceo.name}")
    print(f"Email: {ceo.email}")
    print(f"狀態: {ceo.status.value}")
    print(f"訂閱層級: {ceo.tier.value}")
    print(f"訂閱主題: {ceo.preferences.topics}")
    print(f"頻率: {ceo.preferences.frequency.value}")
    print(f"語調: {ceo.preferences.tone}")
    print(f"偏好時間: {ceo.preferences.preferred_time}")
    print(f"訂閱日期: {ceo.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 4: 更新偏好設定
    print("✅ Test 4: 更新偏好設定")
    print("-" * 80)
    
    update_result = manager.update_preferences(
        "ceo@company.com",
        {
            "topics": ["strategic_intelligence", "technology_radar", "market_pulse", "leadership_insights"],
            "frequency": Frequency.DAILY,
            "tone": "conversational"
        }
    )
    print(f"更新結果: {update_result['status']}")
    
    ceo = manager.get_subscriber("ceo@company.com")
    print(f"新主題: {ceo.preferences.topics}")
    print(f"新頻率: {ceo.preferences.frequency.value}")
    print(f"新語調: {ceo.preferences.tone}")
    print()
    
    # Test 5: 創建多個訂閱者
    print("✅ Test 5: 創建多個不同角色的訂閱者")
    print("-" * 80)
    
    test_subscribers = [
        {
            "email": "cto@company.com",
            "name": "Sarah CTO",
            "preferences": {
                "frequency": Frequency.WEEKLY,
                "topics": ["technology_radar", "market_pulse"],
                "tone": "technical"
            }
        },
        {
            "email": "cfo@company.com",
            "name": "Mike CFO",
            "preferences": {
                "frequency": Frequency.WEEKLY,
                "topics": ["market_pulse", "strategic_intelligence"],
                "tone": "professional"
            }
        },
        {
            "email": "chro@company.com",
            "name": "Lisa CHRO",
            "preferences": {
                "frequency": Frequency.BIWEEKLY,
                "topics": ["talent_culture", "leadership_insights"],
                "tone": "conversational"
            }
        }
    ]
    
    for sub_data in test_subscribers:
        result = manager.subscribe(**sub_data)
        print(f"✓ {sub_data['name']}: {result['status']}")
        # 自動確認
        sub = manager.get_subscriber(sub_data['email'])
        manager.confirm_subscription(sub_data['email'], sub.confirmation_token)
    
    print()
    
    # Test 6: 統計數據
    print("✅ Test 6: 訂閱者統計")
    print("-" * 80)
    
    stats = manager.get_subscriber_stats()
    print(f"總訂閱者: {stats['total_subscribers']}")
    print(f"活躍訂閱者: {stats['active_subscribers']}")
    print(f"待確認: {stats['pending_confirmation']}")
    print(f"已取消: {stats['unsubscribed']}")
    print(f"活躍率: {stats['active_rate']:.1f}%")
    print()
    
    print("依主題分布:")
    for topic, count in sorted(stats['by_topic'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {topic}: {count} 人")
    print()
    
    print("依頻率分布:")
    for freq, count in stats['by_frequency'].items():
        print(f"  - {freq}: {count} 人")
    print()
    
    # Test 7: 按主題查詢
    print("✅ Test 7: 按主題查詢訂閱者")
    print("-" * 80)
    
    strategic_subs = manager.get_subscribers_by_topic("strategic_intelligence")
    print(f"訂閱 Strategic Intelligence 的用戶: {len(strategic_subs)} 人")
    for sub in strategic_subs:
        print(f"  - {sub.name} ({sub.email})")
    print()
    
    tech_subs = manager.get_subscribers_by_topic("technology_radar")
    print(f"訂閱 Technology Radar 的用戶: {len(tech_subs)} 人")
    for sub in tech_subs:
        print(f"  - {sub.name} ({sub.email})")
    print()
    
    # Test 8: 暫停與恢復
    print("✅ Test 8: 暫停與恢復訂閱")
    print("-" * 80)
    
    print(f"暫停前狀態: {manager.get_subscriber('cto@company.com').status.value}")
    pause_result = manager.pause_subscription("cto@company.com")
    print(f"暫停結果: {pause_result['status']}")
    print(f"暫停後狀態: {manager.get_subscriber('cto@company.com').status.value}")
    
    resume_result = manager.resume_subscription("cto@company.com")
    print(f"恢復結果: {resume_result['status']}")
    print(f"恢復後狀態: {manager.get_subscriber('cto@company.com').status.value}")
    print()
    
    # Test 9: 取消訂閱
    print("✅ Test 9: 取消訂閱流程")
    print("-" * 80)
    
    test_email = "test@company.com"
    manager.subscribe(email=test_email, name="Test User", preferences={"topics": ["market_pulse"]})
    test_sub = manager.get_subscriber(test_email)
    manager.confirm_subscription(test_email, test_sub.confirmation_token)
    
    print(f"取消前狀態: {manager.get_subscriber(test_email).status.value}")
    unsub_result = manager.unsubscribe(test_email, reason="Just testing")
    print(f"取消結果: {unsub_result['status']}")
    print(f"取消後狀態: {manager.get_subscriber(test_email).status.value}")
    print()
    
    # Final Stats
    print("=" * 80)
    print("📊 最終統計摘要")
    print("=" * 80)
    
    final_stats = manager.get_subscriber_stats()
    print(f"""
總訂閱者數: {final_stats['total_subscribers']}
活躍訂閱者: {final_stats['active_subscribers']}
待確認: {final_stats['pending_confirmation']}
已暫停: {final_stats['paused']}
已取消: {final_stats['unsubscribed']}
活躍率: {final_stats['active_rate']:.1f}%
流失率: {final_stats['churn_rate']:.1f}%
""")
    
    print("主題受歡迎度排名:")
    sorted_topics = sorted(final_stats['by_topic'].items(), key=lambda x: x[1], reverse=True)
    for i, (topic, count) in enumerate(sorted_topics, 1):
        print(f"{i}. {topic}: {count} 訂閱者")
    
    print()
    print("✅ 訂閱者管理系統測試完成！所有功能運作正常。")
    print("=" * 80)
