# 🚀 AI-Powered Newsletter Platform
## Enterprise-Grade Multi-Agent Newsletter Automation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Production Ready](https://img.shields.io/badge/status-production%20ready-success.svg)]()

**一個完全自動化的 AI 電子報平台，從市場研究、內容生成、訂閱管理到收費營運，只需串接第三方金流與 LLM API 即可立即使用。**

---

## 📋 目錄

- [🎯 快速開始（5分鐘部署）](#-快速開始5分鐘部署)
- [✨ 核心特色](#-核心特色)
- [🏗️ 系統架構](#️-系統架構)
- [📦 安裝方式](#-安裝方式)
- [🔧 配置指南](#-配置指南)
- [🚀 部署方案](#-部署方案)
- [💰 收費功能整合](#-收費功能整合)
- [📊 監控與維護](#-監控與維護)
- [🤝 貢獻指南](#-貢獻指南)

---

## 🎯 快速開始（5分鐘部署）

### 前置需求

- Docker & Docker Compose
- Git
- 可選：LLM API Key（OpenAI/Anthropic/Google）

### 一鍵部署（本地環境）

```bash
# 1. Clone 專案
git clone https://github.com/glen200392/ai-newsletter-platform.git
cd ai-newsletter-platform

# 2. 設置環境變數
cp .env.example .env
# 編輯 .env 文件，填入必要配置

# 3. 啟動所有服務
docker-compose up -d

# 4. 驗證部署
curl http://localhost:8000/health
```

**🎉 完成！** 服務現在運行在：
- 📧 Newsletter API: `http://localhost:8000`
- 📊 Admin Dashboard: `http://localhost:3000`
- 💾 PostgreSQL: `localhost:5432`
- 📨 Redis: `localhost:6379`

### 創建第一份 Newsletter

```bash
# 使用 CLI 工具
python scripts/create_newsletter.py \
  --topic "Strategic Intelligence" \
  --audience "CEO" \
  --language "zh-TW"

# 或通過 API
curl -X POST http://localhost:8000/api/v1/newsletters/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "strategic_intelligence",
    "target_audience": "CEO",
    "language": "zh-TW"
  }'
```

---

## ✨ 核心特色

### 🤖 AI Agent 團隊協作

- **Market Research Agent**: 自動掃描市場趨勢、新聞來源、技術文章
- **Content Generation Agent**: 基於 CEO/CTO/CFO 等角色生成專業內容
- **Quality Control Agent**: 確保內容符合品質標準（BLUF、可讀性、引用）
- **Personalization Agent**: 根據訂閱者偏好客製化內容
- **Distribution Agent**: 智能排程與發送管理

### 📊 完整的訂閱管理系統

✅ **訂閱者生命週期管理**
- 註冊 → Email 驗證 → 偏好設置 → 訂閱管理
- 暫停/恢復訂閱
- 取消訂閱流程
- 重新訂閱處理

✅ **個性化偏好設置**
- 5 個主題選擇（Strategic Intelligence, Technology Radar, Market Pulse, Leadership, Talent）
- 3 種頻率（Daily, Weekly, Bi-weekly）
- 4 種語調（Professional, Analytical, Conversational, Bold）
- 時區與最佳發送時間

✅ **分析與追蹤**
- 開信率（Open Rate）
- 點擊率（Click Rate）
- 閱讀時間
- 用戶參與度評分
- A/B 測試支持

### 🎯 專為高階主管設計

**5 個 Newsletter 主題**，每個都有獨特視角：

| 主題 | 目標讀者 | 核心價值 | 更新頻率 |
|------|---------|---------|---------|
| **Strategic Intelligence** | CEO, 董事會 | 先於市場看到變化 | 每週 |
| **Technology Radar** | 非技術高管 | 技術→商業意義翻譯 | 雙週 |
| **Market Pulse** | CFO, CEO | 數據驅動決策洞察 | 每週 |
| **Leadership Insights** | 所有高管 | 可複製的領導框架 | 每週 |
| **Talent & Culture** | CHRO, CEO | 組織設計模式 | 雙週 |

### 💰 可商業化設計

- ✅ **訂閱計費整合**：Stripe/PayPal/綠界科技
- ✅ **分層定價**：Free, Pro, Enterprise
- ✅ **Trial 期管理**：7/14/30 天試用
- ✅ **發票與收據**：自動生成
- ✅ **退款處理**：自動化流程

### ☁️ 多雲部署支持

- **AWS**: ECS Fargate + RDS + S3
- **GCP**: Cloud Run + Cloud SQL + Cloud Storage
- **Azure**: Container Instances + Azure Database + Blob Storage
- **地端部署**: Docker Compose + PostgreSQL

### 📈 企業級可靠性

- 99.9% 可用性保證
- 自動擴展（Auto-scaling）
- 災難恢復（Disaster Recovery）
- 完整監控與告警
- 日誌聚合與分析

---

## 🏗️ 系統架構

### 三層編排架構

```
┌─────────────────────────────────────────────────────┐
│         Strategic Orchestrator (L1)                 │
│  Market Intelligence | Portfolio Manager | Planner  │
└────────────────┬────────────────────────────────────┘
                 │ Events: ContentStrategyUpdated
                 │         TopicCreated, TopicArchived
┌────────────────▼────────────────────────────────────┐
│       Operational Orchestrator (L2)                 │
│  Workflow Engine | Resource Scheduler | Monitor     │
└────────────────┬────────────────────────────────────┘
                 │ Events: WorkflowStarted
                 │         TaskAssigned, TaskCompleted
┌────────────────▼────────────────────────────────────┐
│      Execution Layer (L3) - Agent Teams             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Research │  │ Content  │  │ Quality  │          │
│  │  Agents  │  │  Agents  │  │  Agents  │          │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
```

### 核心組件

```
ai-newsletter-platform/
├── src/
│   ├── agents/              # AI Agent 實現
│   │   ├── market_research_agent.py
│   │   ├── content_generation_agent.py
│   │   ├── quality_control_agent.py
│   │   ├── personalization_agent.py
│   │   └── distribution_agent.py
│   ├── orchestrator/        # 編排層
│   │   ├── strategic_orchestrator.py
│   │   ├── operational_orchestrator.py
│   │   └── event_bus.py
│   ├── api/                 # REST API
│   │   ├── routes/
│   │   ├── models/
│   │   └── middleware/
│   ├── subscriber/          # 訂閱者管理
│   │   ├── subscriber_manager.py
│   │   ├── preference_engine.py
│   │   └── analytics.py
│   ├── payment/             # 支付整合
│   │   ├── stripe_integration.py
│   │   ├── paypal_integration.py
│   │   └── invoice_generator.py
│   └── infrastructure/      # 基礎設施
│       ├── database/
│       ├── cache/
│       └── messaging/
├── tests/                   # 完整測試套件
├── docs/                    # 詳細文檔
├── deployments/             # 部署配置
│   ├── aws/
│   ├── gcp/
│   ├── azure/
│   └── on-premise/
└── scripts/                 # 工具腳本
```

---

## 📦 安裝方式

### 方式 1: Docker Compose（推薦）

最簡單的方式，適合本地開發與測試：

```bash
# Clone 專案
git clone https://github.com/glen200392/ai-newsletter-platform.git
cd ai-newsletter-platform

# 設置環境變數
cp .env.example .env
nano .env  # 編輯配置

# 啟動服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

### 方式 2: Python 虛擬環境

適合開發與調試：

```bash
# 創建虛擬環境
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
alembic upgrade head

# 啟動開發服務器
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 方式 3: Kubernetes

適合生產環境：

```bash
# 應用 Kubernetes 配置
kubectl apply -f deployments/kubernetes/

# 檢查部署狀態
kubectl get pods -n newsletter-platform

# 查看服務
kubectl get svc -n newsletter-platform
```

---

## 🔧 配置指南

### 環境變數設置

完整的 `.env` 配置範例：

```bash
# ============================================================================
# 應用基礎配置
# ============================================================================
APP_NAME=AI Newsletter Platform
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# API 配置
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# ============================================================================
# 資料庫配置
# ============================================================================
DATABASE_URL=postgresql://user:password@localhost:5432/newsletter_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# ============================================================================
# Redis 配置（快取 & 任務隊列）
# ============================================================================
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# ============================================================================
# LLM API 配置（選擇一個或多個）
# ============================================================================
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=4000

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus-20240229

# Google Gemini
GOOGLE_API_KEY=AIza...
GOOGLE_MODEL=gemini-pro

# ============================================================================
# Email 發送配置（選擇一個）
# ============================================================================
# SendGrid
SENDGRID_API_KEY=SG...
SENDGRID_FROM_EMAIL=newsletter@yourcompany.com
SENDGRID_FROM_NAME=Your Company Newsletter

# AWS SES
AWS_SES_REGION=us-east-1
AWS_SES_ACCESS_KEY=AKIA...
AWS_SES_SECRET_KEY=...

# SMTP (通用)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

# ============================================================================
# 支付整合配置
# ============================================================================
# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PayPal
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_MODE=live  # sandbox 或 live

# 綠界科技 (台灣)
ECPAY_MERCHANT_ID=...
ECPAY_HASH_KEY=...
ECPAY_HASH_IV=...

# ============================================================================
# 外部數據源（可選）
# ============================================================================
# Hacker News API - 免費，無需 Key
HACKERNEWS_API_URL=https://hacker-news.firebaseio.com/v0

# arXiv API - 免費，無需 Key
ARXIV_API_URL=http://export.arxiv.org/api/query

# RSS Feeds（自定義）
RSS_FEEDS=https://techcrunch.com/feed/,https://www.bloomberg.com/feed/

# ============================================================================
# 監控與追蹤
# ============================================================================
# Sentry
SENTRY_DSN=https://...@sentry.io/...

# Google Analytics
GA_TRACKING_ID=UA-...

# Mixpanel
MIXPANEL_TOKEN=...

# ============================================================================
# 安全配置
# ============================================================================
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=another-secret-key-for-jwt
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

ALLOWED_ORIGINS=https://yourcompany.com,https://app.yourcompany.com
RATE_LIMIT=100/minute

# ============================================================================
# 功能開關
# ============================================================================
ENABLE_ANALYTICS=true
ENABLE_AB_TESTING=true
ENABLE_PAYMENT=true
ENABLE_EMAIL_VERIFICATION=true
```

### LLM 選擇指南

根據需求選擇合適的 LLM：

| 提供商 | 模型 | 適用場景 | 價格 | 速度 |
|--------|------|---------|------|------|
| **OpenAI** | GPT-4 Turbo | 高品質內容生成 | $$$ | 中 |
| **OpenAI** | GPT-3.5 Turbo | 快速生成，測試 | $ | 快 |
| **Anthropic** | Claude 3 Opus | 長文本分析 | $$$ | 中 |
| **Anthropic** | Claude 3 Sonnet | 平衡性能價格 | $$ | 快 |
| **Google** | Gemini Pro | 多模態支持 | $$ | 快 |
| **開源** | Llama 3 | 自主部署 | 硬體成本 | 可控 |

**建議配置**：
- **開發環境**: GPT-3.5 Turbo（便宜快速）
- **生產環境**: GPT-4 Turbo 或 Claude 3 Opus（品質優先）
- **成本敏感**: 混合使用（初稿用 3.5，潤稿用 4）

---

## 🚀 部署方案

### 本地開發部署

使用 Docker Compose 一鍵部署：

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/newsletter
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  worker:
    build: .
    command: celery -A src.worker worker -l info
    depends_on:
      - redis
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: newsletter
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  admin:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

volumes:
  postgres_data:
```

### AWS 雲端部署

完整的 AWS 架構：

```
┌─────────────────────────────────────────────────────┐
│                    CloudFront                        │
│              (CDN + SSL Termination)                 │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│            Application Load Balancer                 │
└─────────────┬───────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐         ┌───▼────┐
│  ECS   │         │  ECS   │
│ Task 1 │         │ Task 2 │
└───┬────┘         └───┬────┘
    │                   │
    └─────────┬─────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│              RDS PostgreSQL                          │
│         (Multi-AZ, Auto Backup)                      │
└──────────────────────────────────────────────────────┘
```

**部署步驟**：

```bash
# 1. 設置 AWS CLI
aws configure

# 2. 創建 ECR Repository
aws ecr create-repository --repository-name newsletter-platform

# 3. 構建並推送 Docker Image
docker build -t newsletter-platform .
docker tag newsletter-platform:latest $ECR_URL/newsletter-platform:latest
docker push $ECR_URL/newsletter-platform:latest

# 4. 部署 CloudFormation Stack
aws cloudformation create-stack \
  --stack-name newsletter-platform \
  --template-body file://deployments/aws/cloudformation.yaml \
  --parameters file://deployments/aws/parameters.json \
  --capabilities CAPABILITY_IAM

# 5. 檢查部署狀態
aws cloudformation describe-stacks --stack-name newsletter-platform
```

詳細文檔：[deployments/aws/README.md](deployments/aws/README.md)

### GCP 雲端部署

使用 Cloud Run 的無服務器架構：

```bash
# 1. 設置 GCP CLI
gcloud init
gcloud auth configure-docker

# 2. 構建並推送到 GCR
gcloud builds submit --tag gcr.io/$PROJECT_ID/newsletter-platform

# 3. 部署到 Cloud Run
gcloud run deploy newsletter-platform \
  --image gcr.io/$PROJECT_ID/newsletter-platform \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=$DB_URL,REDIS_URL=$REDIS_URL

# 4. 設置 Cloud SQL
gcloud sql instances create newsletter-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

詳細文檔：[deployments/gcp/README.md](deployments/gcp/README.md)

### Azure 雲端部署

使用 Container Instances 與 Azure Database：

```bash
# 1. 登入 Azure
az login

# 2. 創建資源群組
az group create --name newsletter-platform-rg --location eastus

# 3. 部署 Container Instance
az container create \
  --resource-group newsletter-platform-rg \
  --name newsletter-api \
  --image glen200392/newsletter-platform:latest \
  --dns-name-label newsletter-api \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL=$DB_URL \
    REDIS_URL=$REDIS_URL

# 4. 設置 Azure Database for PostgreSQL
az postgres server create \
  --resource-group newsletter-platform-rg \
  --name newsletter-db-server \
  --location eastus \
  --admin-user adminuser \
  --admin-password SecurePassword123! \
  --sku-name B_Gen5_1
```

詳細文檔：[deployments/azure/README.md](deployments/azure/README.md)

### 地端部署

適合有安全或合規要求的企業：

**硬體需求**：
- CPU: 4 cores (8 推薦)
- RAM: 8GB (16GB 推薦)
- Storage: 100GB SSD
- Network: 100Mbps+

**軟體需求**：
- Docker 20.10+
- Docker Compose 2.0+
- PostgreSQL 15+（或使用 Docker）
- Redis 7+（或使用 Docker）

```bash
# 1. Clone 專案到伺服器
git clone https://github.com/glen200392/ai-newsletter-platform.git
cd ai-newsletter-platform

# 2. 設置環境變數
cp .env.example .env
nano .env  # 編輯配置

# 3. 啟動服務
docker-compose -f docker-compose.prod.yml up -d

# 4. 初始化資料庫
docker-compose exec api alembic upgrade head

# 5. 創建管理員帳號
docker-compose exec api python scripts/create_admin.py

# 6. 設置 Nginx 反向代理（可選）
sudo cp deployments/on-premise/nginx.conf /etc/nginx/sites-available/newsletter
sudo ln -s /etc/nginx/sites-available/newsletter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 7. 設置 SSL（使用 Let's Encrypt）
sudo certbot --nginx -d newsletter.yourcompany.com
```

詳細文檔：[deployments/on-premise/README.md](deployments/on-premise/README.md)

---

## 💰 收費功能整合

### Stripe 整合（國際市場）

**1. 安裝 Stripe CLI**：
```bash
brew install stripe/stripe-cli/stripe
stripe login
```

**2. 設置 Webhook**：
```bash
stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe
```

**3. 創建定價方案**：
```python
import stripe
stripe.api_key = "sk_test_..."

# 創建 Free Plan
free_plan = stripe.Product.create(
    name="Free Newsletter",
    description="Basic newsletter access"
)

# 創建 Pro Plan
pro_plan = stripe.Product.create(
    name="Pro Newsletter",
    description="Premium content + Analytics"
)
pro_price = stripe.Price.create(
    product=pro_plan.id,
    unit_amount=999,  # $9.99
    currency="usd",
    recurring={"interval": "month"}
)

# 創建 Enterprise Plan
enterprise_plan = stripe.Product.create(
    name="Enterprise Newsletter",
    description="Custom content + API access + White label"
)
enterprise_price = stripe.Price.create(
    product=enterprise_plan.id,
    unit_amount=9999,  # $99.99
    currency="usd",
    recurring={"interval": "month"}
)
```

**4. 整合到應用**：
```python
from src.payment.stripe_integration import StripePaymentProcessor

processor = StripePaymentProcessor()

# 創建訂閱
subscription = processor.create_subscription(
    customer_email="user@example.com",
    price_id="price_xxx",
    trial_days=14
)

# 處理 Webhook
@app.post("/api/v1/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    event = processor.verify_webhook(payload, sig_header)
    
    if event['type'] == 'customer.subscription.created':
        # 處理訂閱創建
        pass
    elif event['type'] == 'customer.subscription.deleted':
        # 處理訂閱取消
        pass
```

### PayPal 整合

```python
from src.payment.paypal_integration import PayPalPaymentProcessor

processor = PayPalPaymentProcessor()

# 創建訂閱
subscription = processor.create_subscription(
    plan_id="P-xxx",
    subscriber_email="user@example.com"
)
```

### 綠界科技整合（台灣市場）

```python
from src.payment.ecpay_integration import ECPayPaymentProcessor

processor = ECPayPaymentProcessor()

# 創建付款
payment = processor.create_payment(
    amount=990,  # NT$ 990
    item_name="Pro Newsletter - 月訂閱",
    return_url="https://yoursite.com/payment/return",
    notify_url="https://yoursite.com/api/v1/webhooks/ecpay"
)
```

### 定價方案範例

| 方案 | 價格 | 功能 | 試用期 |
|------|------|------|--------|
| **Free** | $0/月 | • 1 個主題<br>• 月更新<br>• 基礎分析 | - |
| **Pro** | $9.99/月 | • 5 個主題<br>• 週更新<br>• 進階分析<br>• Email 支持 | 14 天 |
| **Enterprise** | $99/月 | • 無限主題<br>• 日更新<br>• 完整分析<br>• API 存取<br>• White label<br>• 專屬支持 | 30 天 |

完整文檔：[docs/PAYMENT_INTEGRATION.md](docs/PAYMENT_INTEGRATION.md)

---

## 📊 監控與維護

### 健康檢查 Endpoints

```bash
# 應用健康狀態
curl http://localhost:8000/health

# 詳細系統狀態
curl http://localhost:8000/health/detailed
```

**回應範例**：
```json
{
  "status": "healthy",
  "timestamp": "2026-02-04T14:30:00Z",
  "version": "1.0.0",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "llm_api": "ok",
    "email_service": "ok"
  },
  "metrics": {
    "active_subscribers": 1250,
    "newsletters_sent_today": 450,
    "api_response_time_ms": 125
  }
}
```

### Prometheus Metrics

系統暴露 Prometheus 格式的 metrics：

```bash
curl http://localhost:8000/metrics
```

**關鍵指標**：
- `newsletter_generation_duration_seconds`: Newsletter 生成時間
- `email_send_success_total`: Email 發送成功數
- `email_send_failure_total`: Email 發送失敗數
- `api_request_duration_seconds`: API 請求延遲
- `active_subscribers_total`: 活躍訂閱者數
- `llm_api_tokens_used_total`: LLM API Token 使用量

### 日誌系統

使用結構化日誌（JSON 格式）：

```json
{
  "timestamp": "2026-02-04T14:30:00Z",
  "level": "INFO",
  "logger": "src.agents.content_generation_agent",
  "message": "Newsletter generated successfully",
  "extra": {
    "newsletter_id": "nl_12345",
    "topic": "strategic_intelligence",
    "generation_time_ms": 3500,
    "word_count": 1250
  }
}
```

**日誌聚合**：
- 本地開發：Docker logs
- 生產環境：ELK Stack / CloudWatch / Stackdriver

### 告警規則

建議設置以下告警：

```yaml
# Prometheus Alert Rules
groups:
  - name: newsletter_platform
    rules:
      # Email 發送失敗率過高
      - alert: HighEmailFailureRate
        expr: |
          rate(email_send_failure_total[5m]) /
          rate(email_send_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Email failure rate > 10%"
      
      # API 回應時間過長
      - alert: SlowAPIResponse
        expr: |
          histogram_quantile(0.95,
            rate(api_request_duration_seconds_bucket[5m])
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "95th percentile API response time > 2s"
      
      # 資料庫連線失敗
      - alert: DatabaseConnectionFailed
        expr: up{job="postgresql"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database connection failed"
```

### 備份策略

**資料庫備份**：
```bash
# 每日自動備份
0 2 * * * docker exec newsletter_db pg_dump -U postgres newsletter > /backups/newsletter_$(date +\%Y\%m\%d).sql

# 備份到 S3
0 3 * * * aws s3 cp /backups/newsletter_$(date +\%Y\%m\%d).sql s3://newsletter-backups/
```

**還原**：
```bash
# 從備份還原
docker exec -i newsletter_db psql -U postgres newsletter < backup_20260204.sql
```

完整文檔：[docs/MONITORING.md](docs/MONITORING.md)

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 開發流程

1. **Fork 專案**
2. **創建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交變更** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **開啟 Pull Request**

### 程式碼規範

```bash
# 安裝開發依賴
pip install -r requirements-dev.txt

# 執行 Linter
black src/ tests/
flake8 src/ tests/
mypy src/

# 執行測試
pytest tests/ -v --cov=src

# 生成測試覆蓋率報告
pytest --cov=src --cov-report=html
```

### 提交 Commit 規範

遵循 [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: 新功能
fix: 修復 Bug
docs: 文檔更新
style: 程式碼格式調整
refactor: 重構
test: 測試相關
chore: 建置工具或輔助工具變動
```

**範例**：
```bash
git commit -m "feat: add Stripe payment integration"
git commit -m "fix: resolve email sending timeout issue"
git commit -m "docs: update deployment guide for AWS"
```

---

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件

---

## 🙏 致謝

- [OpenAI](https://openai.com/) - GPT-4 API
- [Anthropic](https://www.anthropic.com/) - Claude API
- [Stripe](https://stripe.com/) - Payment processing
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Docker](https://www.docker.com/) - Containerization

---

## 📞 聯絡方式

- **專案維護者**: Glen
- **Email**: glen200392@gmail.com
- **GitHub**: [@glen200392](https://github.com/glen200392)
- **專案連結**: [https://github.com/glen200392/ai-newsletter-platform](https://github.com/glen200392/ai-newsletter-platform)

---

## 🗺️ Roadmap

### Q1 2026
- ✅ 核心 Newsletter 生成引擎
- ✅ 訂閱者管理系統
- ✅ 多雲部署支持
- 🔄 Stripe/PayPal 整合

### Q2 2026
- ⏳ AI Agent 視覺化編排介面
- ⏳ A/B Testing 框架
- ⏳ 多語言支持（English, 日本語, 한국어）
- ⏳ Mobile App (iOS/Android)

### Q3 2026
- ⏳ 白標解決方案
- ⏳ API Marketplace
- ⏳ 社群功能（評論、分享）
- ⏳ 進階分析（情感分析、閱讀模式）

### Q4 2026
- ⏳ 語音版 Newsletter（Podcast 生成）
- ⏳ 影片摘要整合
- ⏳ 企業 SSO 整合
- ⏳ GDPR 合規工具

---

<div align="center">

**⭐ 如果這個專案對你有幫助，請給我們一顆星星！ ⭐**

Made with ❤️ by the AI Newsletter Platform Team

</div>
