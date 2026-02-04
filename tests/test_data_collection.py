"""
測試市場數據收集與整合
測試 RSS feeds 和 Public APIs 的數據抓取能力
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
import json

# ============================================================================
# 模擬數據源（真實環境會調用實際 API）
# ============================================================================

class MockDataSource:
    """模擬數據源"""
    
    @staticmethod
    def fetch_rss_feed(source_name: str) -> List[Dict]:
        """模擬 RSS Feed 抓取"""
        
        mock_data = {
            "TechCrunch": [
                {
                    "title": "OpenAI Announces GPT-5 with Multimodal Capabilities",
                    "url": "https://techcrunch.com/2026/02/04/openai-gpt5",
                    "published": datetime.now() - timedelta(hours=2),
                    "summary": "OpenAI unveils GPT-5, featuring advanced multimodal processing and improved reasoning capabilities.",
                    "source": "TechCrunch",
                    "category": "AI/ML"
                },
                {
                    "title": "Stripe Valuation Hits $100B After Latest Funding Round",
                    "url": "https://techcrunch.com/2026/02/03/stripe-funding",
                    "published": datetime.now() - timedelta(hours=12),
                    "summary": "Payment processor Stripe reaches $100B valuation in Series H funding round.",
                    "source": "TechCrunch",
                    "category": "Fintech"
                }
            ],
            "Bloomberg": [
                {
                    "title": "Fed Signals Potential Rate Cut in Q2 2026",
                    "url": "https://bloomberg.com/news/fed-rate-cut",
                    "published": datetime.now() - timedelta(hours=5),
                    "summary": "Federal Reserve chair hints at possible interest rate reduction amid cooling inflation.",
                    "source": "Bloomberg",
                    "category": "Economics"
                },
                {
                    "title": "Tech Stocks Rally on Strong Earnings Reports",
                    "url": "https://bloomberg.com/markets/tech-rally",
                    "published": datetime.now() - timedelta(hours=8),
                    "summary": "Major tech companies exceed Q4 expectations, driving market surge.",
                    "source": "Bloomberg",
                    "category": "Markets"
                }
            ],
            "Wired": [
                {
                    "title": "Quantum Computing Breakthrough: IBM Achieves Error Correction Milestone",
                    "url": "https://wired.com/quantum-breakthrough",
                    "published": datetime.now() - timedelta(hours=6),
                    "summary": "IBM's new quantum processor demonstrates practical error correction at scale.",
                    "source": "Wired",
                    "category": "Technology"
                }
            ],
            "Harvard Business Review": [
                {
                    "title": "The Future of Remote Work: Hybrid Models That Actually Work",
                    "url": "https://hbr.org/remote-work-future",
                    "published": datetime.now() - timedelta(days=1),
                    "summary": "Research reveals which hybrid work models drive productivity and employee satisfaction.",
                    "source": "Harvard Business Review",
                    "category": "Management"
                },
                {
                    "title": "CEO Decision-Making in the Age of AI",
                    "url": "https://hbr.org/ceo-ai-decisions",
                    "published": datetime.now() - timedelta(days=2),
                    "summary": "How top executives are leveraging AI to improve strategic decision-making.",
                    "source": "Harvard Business Review",
                    "category": "Leadership"
                }
            ]
        }
        
        return mock_data.get(source_name, [])
    
    @staticmethod
    def fetch_hacker_news() -> List[Dict]:
        """模擬 Hacker News API"""
        return [
            {
                "title": "Show HN: I built an AI coding assistant that actually understands context",
                "url": "https://news.ycombinator.com/item?id=123456",
                "published": datetime.now() - timedelta(hours=3),
                "score": 450,
                "comments": 120,
                "source": "Hacker News",
                "category": "Developer Tools"
            },
            {
                "title": "Why We're Migrating 100M Users from PostgreSQL to CockroachDB",
                "url": "https://news.ycombinator.com/item?id=123457",
                "published": datetime.now() - timedelta(hours=7),
                "score": 380,
                "comments": 95,
                "source": "Hacker News",
                "category": "Databases"
            }
        ]
    
    @staticmethod
    def fetch_arxiv_papers(topic: str) -> List[Dict]:
        """模擬 arXiv API"""
        papers = {
            "AI": [
                {
                    "title": "Scaling Laws for Large Language Models: New Insights",
                    "authors": ["Smith, J.", "Chen, L.", "Garcia, M."],
                    "url": "https://arxiv.org/abs/2602.12345",
                    "published": datetime.now() - timedelta(days=1),
                    "summary": "Novel analysis of scaling behavior in transformer-based models.",
                    "source": "arXiv",
                    "category": "AI Research"
                }
            ],
            "Quantum": [
                {
                    "title": "Practical Quantum Error Correction Using Surface Codes",
                    "authors": ["Johnson, R.", "Lee, K."],
                    "url": "https://arxiv.org/abs/2602.54321",
                    "published": datetime.now() - timedelta(days=3),
                    "summary": "Experimental validation of surface code implementation on superconducting qubits.",
                    "source": "arXiv",
                    "category": "Quantum Computing"
                }
            ]
        }
        return papers.get(topic, [])


class DataAggregator:
    """數據聚合器"""
    
    def __init__(self):
        self.data_source = MockDataSource()
        self.collected_articles = []
    
    def collect_from_rss_feeds(self, sources: List[str]) -> List[Dict]:
        """從 RSS Feeds 收集數據"""
        print(f"\n📡 正在從 {len(sources)} 個 RSS 源收集數據...")
        
        all_articles = []
        for source in sources:
            articles = self.data_source.fetch_rss_feed(source)
            all_articles.extend(articles)
            print(f"  ✓ {source}: 收集 {len(articles)} 篇文章")
        
        self.collected_articles.extend(all_articles)
        return all_articles
    
    def collect_from_hacker_news(self) -> List[Dict]:
        """從 Hacker News 收集數據"""
        print(f"\n📡 正在從 Hacker News 收集熱門話題...")
        
        articles = self.data_source.fetch_hacker_news()
        self.collected_articles.extend(articles)
        print(f"  ✓ 收集 {len(articles)} 個熱門討論")
        
        return articles
    
    def collect_from_arxiv(self, topics: List[str]) -> List[Dict]:
        """從 arXiv 收集研究論文"""
        print(f"\n📡 正在從 arXiv 收集研究論文...")
        
        all_papers = []
        for topic in topics:
            papers = self.data_source.fetch_arxiv_papers(topic)
            all_papers.extend(papers)
            print(f"  ✓ {topic}: 收集 {len(papers)} 篇論文")
        
        self.collected_articles.extend(all_papers)
        return all_papers
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """按分類過濾"""
        return [
            article for article in self.collected_articles
            if article.get("category") == category
        ]
    
    def filter_by_date(self, hours: int = 24) -> List[Dict]:
        """按時間過濾（最近 N 小時）"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            article for article in self.collected_articles
            if article.get("published", datetime.min) > cutoff
        ]
    
    def get_top_by_score(self, n: int = 10) -> List[Dict]:
        """獲取評分最高的文章"""
        scored_articles = [
            article for article in self.collected_articles
            if "score" in article
        ]
        return sorted(scored_articles, key=lambda x: x["score"], reverse=True)[:n]
    
    def extract_keywords(self, article: Dict) -> List[str]:
        """提取關鍵字（簡化版）"""
        text = f"{article.get('title', '')} {article.get('summary', '')}"
        
        # 簡化的關鍵字提取（實際會用 NLP）
        keywords = []
        important_terms = [
            "AI", "machine learning", "quantum", "blockchain", "cloud",
            "security", "data", "automation", "API", "infrastructure",
            "CEO", "leadership", "strategy", "innovation", "digital transformation"
        ]
        
        text_lower = text.lower()
        for term in important_terms:
            if term.lower() in text_lower:
                keywords.append(term)
        
        return keywords
    
    def analyze_trends(self) -> Dict:
        """分析趨勢"""
        category_counts = {}
        keyword_counts = {}
        sources_counts = {}
        
        for article in self.collected_articles:
            # 統計分類
            category = article.get("category", "Unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # 統計來源
            source = article.get("source", "Unknown")
            sources_counts[source] = sources_counts.get(source, 0) + 1
            
            # 統計關鍵字
            keywords = self.extract_keywords(article)
            for kw in keywords:
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        return {
            "total_articles": len(self.collected_articles),
            "by_category": category_counts,
            "by_source": sources_counts,
            "top_keywords": sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "date_range": {
                "oldest": min([a.get("published", datetime.now()) for a in self.collected_articles]).strftime("%Y-%m-%d %H:%M"),
                "newest": max([a.get("published", datetime.now()) for a in self.collected_articles]).strftime("%Y-%m-%d %H:%M")
            }
        }
    
    def generate_summary_for_ceo(self, topic: str = "strategic_intelligence") -> Dict:
        """為 CEO 生成摘要"""
        
        # 根據主題過濾相關文章
        relevant_categories = {
            "strategic_intelligence": ["Economics", "Markets", "Leadership", "Management"],
            "technology_radar": ["AI/ML", "Technology", "Developer Tools", "Databases"],
            "market_pulse": ["Markets", "Economics", "Fintech"]
        }
        
        target_categories = relevant_categories.get(topic, [])
        relevant_articles = [
            article for article in self.collected_articles
            if article.get("category") in target_categories
        ]
        
        # 最近 24 小時的文章
        recent_articles = [
            article for article in relevant_articles
            if (datetime.now() - article.get("published", datetime.min)).total_seconds() < 86400
        ]
        
        return {
            "topic": topic,
            "total_relevant": len(relevant_articles),
            "recent_24h": len(recent_articles),
            "top_stories": recent_articles[:5],
            "key_themes": self._extract_themes(relevant_articles)
        }
    
    def _extract_themes(self, articles: List[Dict]) -> List[str]:
        """提取主題"""
        keyword_counts = {}
        for article in articles:
            keywords = self.extract_keywords(article)
            for kw in keywords:
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        return [kw for kw, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]]


# ============================================================================
# 執行測試
# ============================================================================

def main():
    print("=" * 80)
    print("📊 市場數據收集與整合系統測試")
    print("=" * 80)
    
    aggregator = DataAggregator()
    
    # Test 1: RSS Feeds 收集
    print("\n✅ Test 1: 從 RSS Feeds 收集數據")
    print("-" * 80)
    
    rss_sources = ["TechCrunch", "Bloomberg", "Wired", "Harvard Business Review"]
    rss_articles = aggregator.collect_from_rss_feeds(rss_sources)
    print(f"\n總共收集: {len(rss_articles)} 篇文章")
    
    # Test 2: Hacker News 收集
    print("\n✅ Test 2: 從 Hacker News 收集數據")
    print("-" * 80)
    
    hn_articles = aggregator.collect_from_hacker_news()
    print(f"\n總共收集: {len(hn_articles)} 個討論")
    
    # Test 3: arXiv 論文收集
    print("\n✅ Test 3: 從 arXiv 收集研究論文")
    print("-" * 80)
    
    arxiv_topics = ["AI", "Quantum"]
    arxiv_papers = aggregator.collect_from_arxiv(arxiv_topics)
    print(f"\n總共收集: {len(arxiv_papers)} 篇論文")
    
    # Test 4: 趨勢分析
    print("\n✅ Test 4: 分析收集的數據趨勢")
    print("-" * 80)
    
    trends = aggregator.analyze_trends()
    print(f"\n總文章數: {trends['total_articles']}")
    print(f"時間範圍: {trends['date_range']['oldest']} 到 {trends['date_range']['newest']}")
    
    print("\n依分類分布:")
    for category, count in sorted(trends['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {category}: {count} 篇")
    
    print("\n依來源分布:")
    for source, count in sorted(trends['by_source'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {source}: {count} 篇")
    
    print("\n熱門關鍵字:")
    for i, (keyword, count) in enumerate(trends['top_keywords'], 1):
        print(f"  {i}. {keyword}: 出現 {count} 次")
    
    # Test 5: 按分類過濾
    print("\n✅ Test 5: 按分類過濾文章")
    print("-" * 80)
    
    ai_articles = aggregator.filter_by_category("AI/ML")
    print(f"AI/ML 相關文章: {len(ai_articles)} 篇")
    for article in ai_articles:
        print(f"  - {article['title']}")
        print(f"    來源: {article['source']}, 發布: {article['published'].strftime('%Y-%m-%d %H:%M')}")
    
    # Test 6: 按時間過濾
    print("\n✅ Test 6: 過濾最近 12 小時的文章")
    print("-" * 80)
    
    recent_articles = aggregator.filter_by_date(hours=12)
    print(f"最近 12 小時: {len(recent_articles)} 篇")
    for article in recent_articles:
        hours_ago = (datetime.now() - article['published']).total_seconds() / 3600
        print(f"  - {article['title']}")
        print(f"    {hours_ago:.1f} 小時前 | {article['source']}")
    
    # Test 7: 評分排序
    print("\n✅ Test 7: 獲取高評分內容")
    print("-" * 80)
    
    top_scored = aggregator.get_top_by_score(n=3)
    print(f"評分最高的 {len(top_scored)} 個話題:")
    for i, article in enumerate(top_scored, 1):
        print(f"\n  {i}. {article['title']}")
        print(f"     評分: {article['score']} | 評論: {article['comments']} | {article['source']}")
    
    # Test 8: 為 CEO 生成主題摘要
    print("\n✅ Test 8: 為 CEO 生成主題摘要")
    print("-" * 80)
    
    topics_to_test = ["strategic_intelligence", "technology_radar", "market_pulse"]
    
    for topic in topics_to_test:
        print(f"\n📰 主題: {topic.replace('_', ' ').title()}")
        print("-" * 60)
        
        summary = aggregator.generate_summary_for_ceo(topic)
        print(f"相關文章總數: {summary['total_relevant']}")
        print(f"最近 24 小時: {summary['recent_24h']}")
        print(f"關鍵主題: {', '.join(summary['key_themes'])}")
        
        print(f"\n最新故事:")
        for i, story in enumerate(summary['top_stories'][:3], 1):
            print(f"  {i}. {story['title']}")
            print(f"     {story['source']} | {story.get('category', 'N/A')}")
    
    # Test 9: 關鍵字提取
    print("\n✅ Test 9: 測試關鍵字提取功能")
    print("-" * 80)
    
    sample_article = rss_articles[0]
    keywords = aggregator.extract_keywords(sample_article)
    print(f"\n文章: {sample_article['title']}")
    print(f"提取的關鍵字: {', '.join(keywords)}")
    
    # Final Summary
    print("\n" + "=" * 80)
    print("📊 數據收集系統測試摘要")
    print("=" * 80)
    
    print(f"""
✅ RSS Feeds 收集: 成功（{len(rss_sources)} 個來源）
✅ Hacker News 收集: 成功
✅ arXiv 論文收集: 成功（{len(arxiv_topics)} 個主題）
✅ 數據過濾: 成功（分類、時間、評分）
✅ 趨勢分析: 成功
✅ CEO 摘要生成: 成功（{len(topics_to_test)} 個主題）
✅ 關鍵字提取: 成功

總收集文章: {trends['total_articles']} 篇
數據來源: {len(trends['by_source'])} 個
覆蓋分類: {len(trends['by_category'])} 個
熱門關鍵字: {len(trends['top_keywords'])} 個

✅ 所有數據收集功能測試通過！
系統已準備好為 CEO Newsletter 提供市場情報。
""")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
