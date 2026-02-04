-- ============================================================================
-- AI Newsletter Platform - Database Schema
-- PostgreSQL 15+
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- Subscribers Table
-- ============================================================================
CREATE TABLE subscribers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',  -- pending, active, paused, cancelled
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    
    -- Indexing
    INDEX idx_subscribers_email (email),
    INDEX idx_subscribers_status (status),
    INDEX idx_subscribers_created_at (created_at)
);

-- ============================================================================
-- Subscriber Preferences
-- ============================================================================
CREATE TABLE subscriber_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subscriber_id UUID NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    
    -- Topic preferences (JSONB array)
    preferred_topics JSONB DEFAULT '[]'::jsonb,
    
    -- Frequency: daily, weekly, biweekly, monthly
    frequency VARCHAR(50) DEFAULT 'weekly',
    
    -- Tone: professional, analytical, conversational, bold
    tone VARCHAR(50) DEFAULT 'professional',
    
    -- Timing
    timezone VARCHAR(100) DEFAULT 'Asia/Taipei',
    preferred_send_time TIME DEFAULT '09:00:00',
    
    -- Language
    language VARCHAR(10) DEFAULT 'zh-TW',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(subscriber_id)
);

-- ============================================================================
-- Newsletters
-- ============================================================================
CREATE TABLE newsletters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic VARCHAR(100) NOT NULL,  -- strategic_intelligence, technology_radar, etc.
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    content_html TEXT,
    
    -- Metadata
    word_count INTEGER,
    reading_time_seconds INTEGER,
    generation_time_ms INTEGER,
    
    -- Status
    status VARCHAR(50) DEFAULT 'draft',  -- draft, approved, sent
    
    -- Source tracking
    data_sources JSONB DEFAULT '[]'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP WITH TIME ZONE,
    sent_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_newsletters_topic (topic),
    INDEX idx_newsletters_status (status),
    INDEX idx_newsletters_created_at (created_at)
);

-- ============================================================================
-- Newsletter Deliveries
-- ============================================================================
CREATE TABLE newsletter_deliveries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    newsletter_id UUID NOT NULL REFERENCES newsletters(id) ON DELETE CASCADE,
    subscriber_id UUID NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    
    -- Delivery status
    status VARCHAR(50) DEFAULT 'pending',  -- pending, sent, failed, bounced
    
    -- Engagement tracking
    opened BOOLEAN DEFAULT FALSE,
    opened_at TIMESTAMP WITH TIME ZONE,
    clicked BOOLEAN DEFAULT FALSE,
    clicked_at TIMESTAMP WITH TIME ZONE,
    
    -- Reading behavior
    reading_time_seconds INTEGER,
    
    -- Error tracking
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(newsletter_id, subscriber_id),
    INDEX idx_deliveries_newsletter (newsletter_id),
    INDEX idx_deliveries_subscriber (subscriber_id),
    INDEX idx_deliveries_status (status),
    INDEX idx_deliveries_opened (opened),
    INDEX idx_deliveries_clicked (clicked)
);

-- ============================================================================
-- Subscription Plans
-- ============================================================================
CREATE TABLE subscription_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,  -- free, pro, enterprise
    description TEXT,
    
    -- Pricing
    price_cents INTEGER DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    billing_interval VARCHAR(50) DEFAULT 'month',  -- month, year
    
    -- Features (JSONB)
    features JSONB DEFAULT '[]'::jsonb,
    
    -- Limits
    max_topics INTEGER,
    max_newsletters_per_month INTEGER,
    
    -- Status
    active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Subscriptions (Payment)
-- ============================================================================
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subscriber_id UUID NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES subscription_plans(id),
    
    -- External payment provider IDs
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    paypal_subscription_id VARCHAR(255),
    
    -- Status
    status VARCHAR(50) DEFAULT 'active',  -- trial, active, past_due, cancelled, expired
    
    -- Billing
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    
    -- Trial
    trial_start TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_subscriptions_subscriber (subscriber_id),
    INDEX idx_subscriptions_status (status),
    INDEX idx_subscriptions_stripe_sub (stripe_subscription_id),
    INDEX idx_subscriptions_stripe_customer (stripe_customer_id)
);

-- ============================================================================
-- Payment Transactions
-- ============================================================================
CREATE TABLE payment_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subscription_id UUID NOT NULL REFERENCES subscriptions(id),
    
    -- Amount
    amount_cents INTEGER NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- External IDs
    stripe_payment_intent_id VARCHAR(255),
    stripe_charge_id VARCHAR(255),
    paypal_order_id VARCHAR(255),
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',  -- pending, succeeded, failed, refunded
    
    -- Details
    description TEXT,
    receipt_url TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP WITH TIME ZONE,
    refunded_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_transactions_subscription (subscription_id),
    INDEX idx_transactions_status (status),
    INDEX idx_transactions_created_at (created_at)
);

-- ============================================================================
-- Data Sources (for content generation)
-- ============================================================================
CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_type VARCHAR(50) NOT NULL,  -- rss, api, hackernews, arxiv
    source_name VARCHAR(255) NOT NULL,
    source_url TEXT NOT NULL,
    
    -- Configuration
    config JSONB DEFAULT '{}'::jsonb,
    
    -- Status
    active BOOLEAN DEFAULT TRUE,
    last_fetched_at TIMESTAMP WITH TIME ZONE,
    
    -- Stats
    total_articles_collected INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Collected Articles
-- ============================================================================
CREATE TABLE collected_articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    data_source_id UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    
    -- Content
    title VARCHAR(1000) NOT NULL,
    url TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    
    -- Metadata
    author VARCHAR(255),
    published_at TIMESTAMP WITH TIME ZONE,
    
    -- Analysis
    keywords JSONB DEFAULT '[]'::jsonb,
    sentiment JSONB DEFAULT '{}'::jsonb,
    relevance_score DECIMAL(5,2),
    
    -- Processing
    processed BOOLEAN DEFAULT FALSE,
    used_in_newsletter_id UUID REFERENCES newsletters(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_articles_source (data_source_id),
    INDEX idx_articles_published (published_at),
    INDEX idx_articles_processed (processed),
    INDEX idx_articles_relevance (relevance_score)
);

-- ============================================================================
-- Audit Log
-- ============================================================================
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL,  -- subscriber, newsletter, payment, etc.
    entity_id UUID NOT NULL,
    action VARCHAR(100) NOT NULL,  -- created, updated, deleted, sent, etc.
    
    -- User context
    user_id UUID,
    user_email VARCHAR(255),
    
    -- Changes
    old_values JSONB,
    new_values JSONB,
    
    -- Request context
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_audit_entity (entity_type, entity_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_created_at (created_at)
);

-- ============================================================================
-- System Configuration
-- ============================================================================
CREATE TABLE system_config (
    key VARCHAR(255) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Triggers for updated_at
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_subscribers_updated_at BEFORE UPDATE ON subscribers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriber_preferences_updated_at BEFORE UPDATE ON subscriber_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscription_plans_updated_at BEFORE UPDATE ON subscription_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_data_sources_updated_at BEFORE UPDATE ON data_sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Initial Data
-- ============================================================================

-- Insert default subscription plans
INSERT INTO subscription_plans (name, slug, description, price_cents, features, max_topics, max_newsletters_per_month) VALUES
('Free', 'free', '基礎 Newsletter 訂閱', 0, '["1 個主題", "月更新", "基礎分析"]'::jsonb, 1, 4),
('Pro', 'pro', '專業 Newsletter 訂閱', 999, '["5 個主題", "週更新", "進階分析", "Email 支持"]'::jsonb, 5, 20),
('Enterprise', 'enterprise', '企業級 Newsletter 訂閱', 9999, '["無限主題", "日更新", "完整分析", "API 存取", "White label", "專屬支持"]'::jsonb, -1, -1);

-- Insert default data sources
INSERT INTO data_sources (source_type, source_name, source_url, active) VALUES
('rss', 'TechCrunch', 'https://techcrunch.com/feed/', true),
('rss', 'Bloomberg Technology', 'https://www.bloomberg.com/feed/podcast/hello-world', true),
('rss', 'Wired', 'https://www.wired.com/feed/rss', true),
('api', 'Hacker News', 'https://hacker-news.firebaseio.com/v0', true),
('api', 'arXiv', 'http://export.arxiv.org/api/query', true);

-- ============================================================================
-- Views for Analytics
-- ============================================================================

-- Subscriber engagement view
CREATE VIEW subscriber_engagement AS
SELECT 
    s.id,
    s.email,
    s.status,
    COUNT(DISTINCT nd.id) as total_deliveries,
    SUM(CASE WHEN nd.opened THEN 1 ELSE 0 END) as opens,
    SUM(CASE WHEN nd.clicked THEN 1 ELSE 0 END) as clicks,
    CASE 
        WHEN COUNT(DISTINCT nd.id) > 0 
        THEN ROUND(100.0 * SUM(CASE WHEN nd.opened THEN 1 ELSE 0 END) / COUNT(DISTINCT nd.id), 2)
        ELSE 0 
    END as open_rate,
    AVG(nd.reading_time_seconds) as avg_reading_time
FROM subscribers s
LEFT JOIN newsletter_deliveries nd ON s.id = nd.subscriber_id
GROUP BY s.id, s.email, s.status;

-- Newsletter performance view
CREATE VIEW newsletter_performance AS
SELECT 
    n.id,
    n.title,
    n.topic,
    n.created_at,
    COUNT(DISTINCT nd.id) as total_sent,
    SUM(CASE WHEN nd.opened THEN 1 ELSE 0 END) as opens,
    SUM(CASE WHEN nd.clicked THEN 1 ELSE 0 END) as clicks,
    CASE 
        WHEN COUNT(DISTINCT nd.id) > 0 
        THEN ROUND(100.0 * SUM(CASE WHEN nd.opened THEN 1 ELSE 0 END) / COUNT(DISTINCT nd.id), 2)
        ELSE 0 
    END as open_rate,
    CASE 
        WHEN COUNT(DISTINCT nd.id) > 0 
        THEN ROUND(100.0 * SUM(CASE WHEN nd.clicked THEN 1 ELSE 0 END) / COUNT(DISTINCT nd.id), 2)
        ELSE 0 
    END as click_rate
FROM newsletters n
LEFT JOIN newsletter_deliveries nd ON n.id = nd.newsletter_id
GROUP BY n.id, n.title, n.topic, n.created_at;

-- ============================================================================
-- Indexes for Performance
-- ============================================================================

-- Composite indexes for common queries
CREATE INDEX idx_deliveries_opened_clicked ON newsletter_deliveries(opened, clicked);
CREATE INDEX idx_subscriptions_active_period ON subscriptions(status, current_period_end);
CREATE INDEX idx_articles_processed_relevance ON collected_articles(processed, relevance_score DESC);

-- Full-text search indexes
CREATE INDEX idx_newsletters_title_search ON newsletters USING gin(to_tsvector('english', title));
CREATE INDEX idx_newsletters_content_search ON newsletters USING gin(to_tsvector('english', content));
CREATE INDEX idx_articles_title_search ON collected_articles USING gin(to_tsvector('english', title));

-- ============================================================================
-- Comments
-- ============================================================================
COMMENT ON TABLE subscribers IS 'Newsletter subscribers with email and verification status';
COMMENT ON TABLE subscriber_preferences IS 'Subscriber preferences for content, frequency, and timing';
COMMENT ON TABLE newsletters IS 'Generated newsletter content';
COMMENT ON TABLE newsletter_deliveries IS 'Delivery tracking and engagement metrics';
COMMENT ON TABLE subscription_plans IS 'Available subscription tiers and pricing';
COMMENT ON TABLE subscriptions IS 'Active subscriber payment subscriptions';
COMMENT ON TABLE payment_transactions IS 'Payment transaction history';
COMMENT ON TABLE data_sources IS 'External data sources for content collection';
COMMENT ON TABLE collected_articles IS 'Articles collected from data sources';
COMMENT ON TABLE audit_log IS 'System-wide audit trail';
