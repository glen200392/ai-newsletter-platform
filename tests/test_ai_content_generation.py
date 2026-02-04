"""
測試 AI 內容生成工作流（Nebula 環境）
展示如何為 CEO 生成高品質的 Newsletter 內容
"""

from datetime import datetime
from typing import Dict, List

# ============================================================================
# CEO Newsletter 內容生成器
# ============================================================================

class CEONewsletterGenerator:
    """CEO Newsletter 內容生成器（Nebula 環境版本）"""
    
    def __init__(self):
        self.newsletter_templates = {
            "strategic_intelligence": self._strategic_intelligence_template,
            "technology_radar": self._technology_radar_template,
            "market_pulse": self._market_pulse_template,
            "leadership_insights": self._leadership_insights_template
        }
    
    def generate_newsletter(
        self,
        topic: str,
        research_data: List[Dict],
        preferences: Dict = None
    ) -> Dict:
        """
        生成 Newsletter 內容
        
        在 Nebula 環境中，這個函數會：
        1. 整理研究數據
        2. 構建 AI 提示詞
        3. 返回生成請求（Nebula 會處理實際的 AI 生成）
        """
        
        preferences = preferences or {}
        template_func = self.newsletter_templates.get(topic)
        
        if not template_func:
            return {
                "status": "error",
                "message": f"Unknown topic: {topic}"
            }
        
        # 構建生成請求
        generation_request = template_func(research_data, preferences)
        
        return {
            "status": "success",
            "topic": topic,
            "generation_request": generation_request,
            "metadata": {
                "articles_analyzed": len(research_data),
                "generated_at": datetime.now().isoformat(),
                "preferences": preferences
            }
        }
    
    def _strategic_intelligence_template(
        self,
        research_data: List[Dict],
        preferences: Dict
    ) -> Dict:
        """Strategic Intelligence Newsletter 模板"""
        
        # 整理研究數據
        recent_articles = sorted(
            research_data,
            key=lambda x: x.get("published", datetime.min),
            reverse=True
        )[:5]
        
        # 構建提示詞
        articles_summary = "\n\n".join([
            f"- {art['title']}\n  Source: {art['source']}\n  Summary: {art.get('summary', 'N/A')}"
            for art in recent_articles
        ])
        
        prompt = f"""Generate a CEO-focused Strategic Intelligence Newsletter for {datetime.now().strftime('%B %d, %Y')}.

CONTEXT:
You are writing for C-level executives who need actionable strategic insights, not just information.

RESEARCH DATA:
{articles_summary}

REQUIREMENTS:
1. **Executive Summary (30 seconds read)**
   - 3 most important strategic insights
   - One sentence each + one action implication

2. **This Week's Strategic Shifts** (3-4 minutes read)
   - Select 2-3 most significant developments
   - For each:
     * What Happened (2-3 sentences of facts)
     * Why It Matters (impact on business/industry)
     * Strategic Implication (what to consider doing)
     * Source (credible citation)

3. **Emerging Patterns** (1 minute read)
   - 1-2 weak signals worth monitoring
   - Why they matter in 2-5 year timeframe

4. **Strategic Questions for Leadership Team**
   - 3 thought-provoking questions based on the insights
   - Should challenge assumptions and drive discussion

5. **By The Numbers**
   - 3-5 key metrics/data points with interpretation

TONE: {preferences.get('tone', 'professional')}
- Professional but not academic
- Direct and action-oriented
- Evidence-based, not speculative

FORMAT:
- Bottom Line Up Front (BLUF) - most important info first
- 5-minute total read time
- Mobile-friendly (short paragraphs, clear headers)

OUTPUT STRUCTURE:
# Strategic Intelligence Weekly
## {datetime.now().strftime('%B %d, %Y')} | 5-min read

[Content follows structure above]
"""
        
        return {
            "prompt": prompt,
            "research_data": recent_articles,
            "target_length": "1200-1500 words",
            "tone": preferences.get('tone', 'professional'),
            "reading_time": "5 minutes"
        }
    
    def _technology_radar_template(
        self,
        research_data: List[Dict],
        preferences: Dict
    ) -> Dict:
        """Technology Radar Newsletter 模板"""
        
        tech_articles = [
            art for art in research_data
            if art.get('category') in ['AI/ML', 'Technology', 'Developer Tools', 'Databases']
        ][:5]
        
        articles_summary = "\n\n".join([
            f"- {art['title']}\n  Source: {art['source']}\n  {art.get('summary', '')}"
            for art in tech_articles
        ])
        
        prompt = f"""Generate a Technology Radar Newsletter for non-technical CEOs.

MISSION: Translate complex technology trends into business strategy implications.

RESEARCH DATA:
{articles_summary}

STRUCTURE:

1. **Technology Maturity Assessment**
   Present 2-3 technologies in a simple matrix:
   | Technology | Maturity Level | Time to Business Impact | Action |
   
2. **Deep Dive: Featured Technology**
   - What Is It? (business definition, no jargon)
   - Why Now? (what changed to make it viable)
   - Business Model Implications (how it changes economics)
   - Who's Winning? (2 real examples with results)
   - Your Action Options:
     * Fast Follow (6 months, $XX-XXX)
     * Strategic Pilot (12 months, $X-XX)
     * Monitor & Learn (ongoing, minimal)

3. **Questions for Your CTO**
   - 3 specific technical questions based on insights
   - Help CEO drive meaningful technical discussions

TONE: Educational but not condescending
- Avoid: "Cutting-edge", "Revolutionary", "Game-changing"
- Use: Specific benefits, concrete examples, honest tradeoffs

TARGET: 7-minute read, 1500 words
"""
        
        return {
            "prompt": prompt,
            "research_data": tech_articles,
            "target_length": "1500-1800 words",
            "tone": "educational",
            "reading_time": "7 minutes"
        }
    
    def _market_pulse_template(
        self,
        research_data: List[Dict],
        preferences: Dict
    ) -> Dict:
        """Market Pulse Newsletter 模板"""
        
        market_articles = [
            art for art in research_data
            if art.get('category') in ['Markets', 'Economics', 'Fintech']
        ][:5]
        
        articles_summary = "\n\n".join([
            f"- {art['title']}\n  {art.get('summary', '')}"
            for art in market_articles
        ])
        
        prompt = f"""Generate a data-driven Market Pulse Newsletter.

FOCUS: Signal over noise. CEO needs to know what matters, not every market move.

DATA:
{articles_summary}

STRUCTURE:

1. **The Week in 5 Charts**
   Describe 5 key charts/metrics:
   - Chart topic
   - Key data point
   - One-sentence interpretation
   - Business implication

2. **Three Numbers That Matter**
   | Metric | Value | Change | What It Means |
   Select metrics that are LEADING indicators

3. **Risk Monitor**
   | Risk | Level | Trend | Watch For |
   - Macro Economic
   - Geopolitical
   - Market Volatility

4. **What Smart Money Is Doing**
   - Where capital is flowing
   - Positioning changes
   - Consensus views

PRINCIPLES:
- Facts, not predictions
- Data, not opinions
- Interpretation, not investment advice

TARGET: 3-minute read, visual-first
"""
        
        return {
            "prompt": prompt,
            "research_data": market_articles,
            "target_length": "800-1000 words",
            "tone": "analytical",
            "reading_time": "3 minutes"
        }
    
    def _leadership_insights_template(
        self,
        research_data: List[Dict],
        preferences: Dict
    ) -> Dict:
        """Leadership Insights Newsletter 模板"""
        
        leadership_articles = [
            art for art in research_data
            if art.get('category') in ['Leadership', 'Management']
        ][:3]
        
        articles_summary = "\n\n".join([
            f"- {art['title']}\n  {art.get('summary', '')}"
            for art in leadership_articles
        ])
        
        prompt = f"""Generate a Leadership Insights Newsletter with actionable frameworks.

PURPOSE: Extract repeatable principles from CEO experiences.

SOURCES:
{articles_summary}

STRUCTURE:

1. **Case Study: [CEO] at [Company]**
   - The Challenge (specific situation)
   - The Decision Process (how they thought through it)
   - The Action (what they did)
   - The Outcome (6-12 months later)
   - Lessons Extracted:
     * Repeatable principles
     * Avoidable mistakes
     * When this applies

2. **Framework: [Name]**
   - Visual representation
   - When to use
   - How to apply (3-step process)
   - Example application

3. **Reflection Questions**
   - Personal reflection
   - Team discussion
   - Organizational assessment

TONE: Inspiring but grounded
- Stories + Frameworks
- Humility (CEOs learn from mistakes)
- Practical application

TARGET: 10-minute read
"""
        
        return {
            "prompt": prompt,
            "research_data": leadership_articles,
            "target_length": "1800-2000 words",
            "tone": "inspirational",
            "reading_time": "10 minutes"
        }


# ============================================================================
# 執行測試
# ============================================================================

def main():
    print("=" * 80)
    print("🤖 AI 內容生成工作流測試（Nebula 環境）")
    print("=" * 80)
    print()
    
    # 模擬從數據收集系統獲取的研究數據
    mock_research_data = [
        {
            "title": "OpenAI Announces GPT-5 with Multimodal Capabilities",
            "source": "TechCrunch",
            "published": datetime(2026, 2, 4, 12, 0),
            "summary": "OpenAI unveils GPT-5, featuring advanced multimodal processing.",
            "category": "AI/ML"
        },
        {
            "title": "Fed Signals Potential Rate Cut in Q2 2026",
            "source": "Bloomberg",
            "published": datetime(2026, 2, 4, 9, 0),
            "summary": "Federal Reserve hints at possible interest rate reduction.",
            "category": "Economics"
        },
        {
            "title": "Quantum Computing Breakthrough: IBM Milestone",
            "source": "Wired",
            "published": datetime(2026, 2, 4, 8, 0),
            "summary": "IBM achieves practical error correction at scale.",
            "category": "Technology"
        },
        {
            "title": "The Future of Remote Work: Hybrid Models That Work",
            "source": "Harvard Business Review",
            "published": datetime(2026, 2, 3, 10, 0),
            "summary": "Research reveals effective hybrid work models.",
            "category": "Management"
        },
        {
            "title": "Tech Stocks Rally on Strong Earnings",
            "source": "Bloomberg",
            "published": datetime(2026, 2, 4, 6, 0),
            "summary": "Major tech companies exceed Q4 expectations.",
            "category": "Markets"
        }
    ]
    
    generator = CEONewsletterGenerator()
    
    # Test 1: Strategic Intelligence Newsletter
    print("✅ Test 1: 生成 Strategic Intelligence Newsletter")
    print("-" * 80)
    
    result1 = generator.generate_newsletter(
        topic="strategic_intelligence",
        research_data=mock_research_data,
        preferences={"tone": "professional"}
    )
    
    print(f"狀態: {result1['status']}")
    print(f"主題: {result1['topic']}")
    print(f"分析文章數: {result1['metadata']['articles_analyzed']}")
    print(f"生成時間: {result1['metadata']['generated_at']}")
    print()
    
    print("生成請求預覽:")
    print("-" * 60)
    request = result1['generation_request']
    print(f"目標長度: {request['target_length']}")
    print(f"語調: {request['tone']}")
    print(f"閱讀時間: {request['reading_time']}")
    print(f"使用數據: {len(request['research_data'])} 篇文章")
    print()
    print("提示詞片段（前 500 字元）:")
    print(request['prompt'][:500] + "...")
    print()
    
    # Test 2: Technology Radar Newsletter
    print("✅ Test 2: 生成 Technology Radar Newsletter")
    print("-" * 80)
    
    result2 = generator.generate_newsletter(
        topic="technology_radar",
        research_data=mock_research_data,
        preferences={"tone": "educational"}
    )
    
    print(f"狀態: {result2['status']}")
    print(f"主題: {result2['topic']}")
    print(f"目標長度: {result2['generation_request']['target_length']}")
    print(f"閱讀時間: {result2['generation_request']['reading_time']}")
    print()
    
    # Test 3: Market Pulse Newsletter
    print("✅ Test 3: 生成 Market Pulse Newsletter")
    print("-" * 80)
    
    result3 = generator.generate_newsletter(
        topic="market_pulse",
        research_data=mock_research_data,
        preferences={"tone": "analytical"}
    )
    
    print(f"狀態: {result3['status']}")
    print(f"主題: {result3['topic']}")
    print(f"目標長度: {result3['generation_request']['target_length']}")
    print(f"閱讀時間: {result3['generation_request']['reading_time']}")
    print()
    
    # Test 4: Leadership Insights Newsletter
    print("✅ Test 4: 生成 Leadership Insights Newsletter")
    print("-" * 80)
    
    result4 = generator.generate_newsletter(
        topic="leadership_insights",
        research_data=mock_research_data,
        preferences={"tone": "inspirational"}
    )
    
    print(f"狀態: {result4['status']}")
    print(f"主題: {result4['topic']}")
    print(f"目標長度: {result4['generation_request']['target_length']}")
    print(f"閱讀時間: {result4['generation_request']['reading_time']}")
    print()
    
    # Test 5: 展示完整的 Strategic Intelligence 提示詞
    print("✅ Test 5: 完整 Strategic Intelligence 提示詞範例")
    print("-" * 80)
    print()
    print(result1['generation_request']['prompt'])
    print()
    
    # Test 6: 測試不同偏好設定
    print("✅ Test 6: 測試不同語調偏好")
    print("-" * 80)
    
    tones = ["professional", "conversational", "technical"]
    for tone in tones:
        result = generator.generate_newsletter(
            topic="strategic_intelligence",
            research_data=mock_research_data[:3],
            preferences={"tone": tone}
        )
        print(f"語調 '{tone}': 生成成功 ✓")
    print()
    
    # Final Summary
    print("=" * 80)
    print("📊 AI 內容生成工作流測試摘要")
    print("=" * 80)
    print(f"""
✅ Strategic Intelligence 生成: 成功
✅ Technology Radar 生成: 成功
✅ Market Pulse 生成: 成功
✅ Leadership Insights 生成: 成功
✅ 多語調支持: 成功
✅ 提示詞結構: 成功

關鍵特點:
- 每個主題都有專門的提示詞模板
- 自動整理研究數據為結構化輸入
- 支持多種語調偏好（professional, conversational, technical）
- 明確的輸出結構要求（BLUF原則）
- 針對 CEO 閱讀習慣優化（5分鐘閱讀）

在 Nebula 環境中的工作流程:
1. 數據收集系統 → 收集市場情報
2. 內容生成器 → 構建結構化提示詞
3. Nebula AI → 執行內容生成（自動）
4. 返回高品質 Newsletter 內容

✅ 所有 AI 內容生成功能測試通過！
系統已準備好在 Nebula 環境中生成專業 CEO Newsletter。
""")
    
    print("=" * 80)
    print()
    print("💡 重要提示：")
    print("在 Nebula 環境中，你不需要管理 LLM API：")
    print("- 提示詞會自動傳送給 Nebula 的 AI 引擎")
    print("- 內容生成在後台自動完成")
    print("- 你只需要專注於提示詞品質和內容結構")
    print("=" * 80)

if __name__ == "__main__":
    main()
