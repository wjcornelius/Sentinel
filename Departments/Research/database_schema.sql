-- Research Department Database Schema
-- Built fresh from DEPARTMENTAL_SPECIFICATIONS v1.0
-- Date: 2025-10-31
-- Purpose: Track market briefings, ticker analyses, news events, sentiment scores

-- Table 1: Market Briefings (Daily market condition summaries)
CREATE TABLE IF NOT EXISTS research_market_briefings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    briefing_date DATE NOT NULL UNIQUE,

    -- Market Indices
    spy_price REAL,
    spy_change_pct REAL,
    qqq_price REAL,
    qqq_change_pct REAL,
    dia_price REAL,
    dia_change_pct REAL,

    -- Volatility & Risk
    vix_level REAL,
    vix_status TEXT CHECK(vix_status IN ('NORMAL', 'ELEVATED', 'CAUTION', 'PANIC')),

    -- Sector Performance (Top 3 / Bottom 3)
    top_sector_1 TEXT,
    top_sector_1_change REAL,
    top_sector_2 TEXT,
    top_sector_2_change REAL,
    top_sector_3 TEXT,
    top_sector_3_change REAL,
    bottom_sector_1 TEXT,
    bottom_sector_1_change REAL,
    bottom_sector_2 TEXT,
    bottom_sector_2_change REAL,
    bottom_sector_3 TEXT,
    bottom_sector_3_change REAL,

    -- Market Summary
    market_sentiment TEXT CHECK(market_sentiment IN ('BULLISH', 'NEUTRAL', 'BEARISH')),
    major_news_summary TEXT,

    -- Message Tracking (Revolutionary - doesn't exist in v6.2)
    message_id TEXT UNIQUE NOT NULL,  -- Links to message sent to Risk/Portfolio

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER IF NOT EXISTS update_research_market_briefings_timestamp
AFTER UPDATE ON research_market_briefings
FOR EACH ROW
BEGIN
    UPDATE research_market_briefings
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;

-- Table 2: Ticker Analyses (Individual stock research)
CREATE TABLE IF NOT EXISTS research_ticker_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id TEXT UNIQUE NOT NULL,  -- e.g., "ANALYSIS_AAPL_20251031_1430"

    -- Ticker Info
    ticker TEXT NOT NULL,
    company_name TEXT,
    sector TEXT,
    industry TEXT,

    -- Price Data
    current_price REAL,
    price_change_1d_pct REAL,
    price_change_5d_pct REAL,
    price_change_20d_pct REAL,

    -- Volume & Liquidity
    avg_volume_30d INTEGER,
    current_volume INTEGER,
    volume_ratio REAL,  -- current / average

    -- Fundamental Metrics
    market_cap_millions REAL,
    pe_ratio REAL,
    forward_pe REAL,
    peg_ratio REAL,
    revenue_growth_yoy_pct REAL,
    profit_margin_pct REAL,
    debt_to_equity REAL,

    -- Technical Indicators
    rsi_14 REAL,
    macd REAL,
    macd_signal REAL,
    bollinger_upper REAL,
    bollinger_lower REAL,
    bollinger_position REAL,  -- (price - lower) / (upper - lower)

    -- Sentiment Analysis
    sentiment_score REAL CHECK(sentiment_score BETWEEN 1 AND 10),  -- 1=Very Bearish, 10=Very Bullish
    sentiment_summary TEXT,
    news_count INTEGER DEFAULT 0,

    -- Overall Assessment
    technical_score REAL CHECK(technical_score BETWEEN 1 AND 10),
    fundamental_score REAL CHECK(fundamental_score BETWEEN 1 AND 10),
    overall_score REAL CHECK(overall_score BETWEEN 1 AND 10),  -- Composite score

    -- Analysis Metadata
    analysis_type TEXT CHECK(analysis_type IN ('DAILY_SCREENING', 'AD_HOC_REQUEST', 'DEEP_DIVE')),
    requested_by_dept TEXT,  -- Which department requested this analysis

    -- Message Tracking (Revolutionary)
    request_message_id TEXT,  -- Link to request message
    response_message_id TEXT UNIQUE NOT NULL,  -- Link to response message

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_research_ticker_analyses_ticker ON research_ticker_analyses(ticker);
CREATE INDEX idx_research_ticker_analyses_date ON research_ticker_analyses(created_at);
CREATE INDEX idx_research_ticker_analyses_score ON research_ticker_analyses(overall_score DESC);

-- Table 3: News Events (Major market-moving events)
CREATE TABLE IF NOT EXISTS research_news_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,

    -- Event Details
    event_date DATETIME NOT NULL,
    event_type TEXT CHECK(event_type IN ('EARNINGS', 'ECONOMIC_DATA', 'FED_ANNOUNCEMENT',
                                          'GEOPOLITICAL', 'CORPORATE_ACTION', 'MARKET_MOVE', 'OTHER')),
    event_title TEXT NOT NULL,
    event_summary TEXT,

    -- Impact Assessment
    impact_level TEXT CHECK(impact_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    affected_tickers TEXT,  -- Comma-separated list
    affected_sectors TEXT,  -- Comma-separated list

    -- Market Reaction
    market_reaction TEXT,  -- Brief description of how market reacted
    spy_move_pct REAL,  -- SPY change on event day

    -- Message Tracking (if alert was generated)
    alert_generated BOOLEAN DEFAULT 0,
    alert_message_id TEXT,  -- Link to alert message sent to Executive

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_research_news_events_date ON research_news_events(event_date DESC);
CREATE INDEX idx_research_news_events_impact ON research_news_events(impact_level);

-- Table 4: Candidate Tickers (Daily screening results)
CREATE TABLE IF NOT EXISTS research_candidate_tickers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Screening Date
    screening_date DATE NOT NULL,

    -- Ticker Info
    ticker TEXT NOT NULL,
    rank INTEGER,  -- 1 = top candidate

    -- Why This Ticker?
    catalyst TEXT,  -- What makes this ticker interesting today
    catalyst_type TEXT CHECK(catalyst_type IN ('MOMENTUM', 'VALUE', 'NEWS', 'TECHNICAL', 'FUNDAMENTAL', 'SENTIMENT')),

    -- Quick Metrics
    quick_score REAL CHECK(quick_score BETWEEN 1 AND 10),
    sentiment_score REAL CHECK(sentiment_score BETWEEN 1 AND 10),
    technical_score REAL CHECK(technical_score BETWEEN 1 AND 10),

    -- Analysis Reference
    full_analysis_id TEXT,  -- FK to research_ticker_analyses.analysis_id (if deep dive done)

    -- Message Tracking
    candidate_list_message_id TEXT,  -- Link to daily candidate list message

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(screening_date, ticker)  -- One entry per ticker per day
);

CREATE INDEX idx_research_candidate_tickers_date ON research_candidate_tickers(screening_date DESC);
CREATE INDEX idx_research_candidate_tickers_rank ON research_candidate_tickers(screening_date, rank);

-- Table 5: Sentiment Cache (Cache Perplexity results to avoid duplicate API calls)
CREATE TABLE IF NOT EXISTS research_sentiment_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Cache Key
    ticker TEXT NOT NULL,
    query_date DATE NOT NULL,

    -- Sentiment Results
    sentiment_score REAL CHECK(sentiment_score BETWEEN 1 AND 10),
    sentiment_summary TEXT,
    news_articles_count INTEGER,
    perplexity_response TEXT,  -- Full JSON response for debugging

    -- Cache Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,  -- Cache expires after 24 hours

    UNIQUE(ticker, query_date)
);

CREATE INDEX idx_research_sentiment_cache_expiry ON research_sentiment_cache(expires_at);

-- Table 6: API Call Log (Track API usage for rate limit management)
CREATE TABLE IF NOT EXISTS research_api_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- API Info
    api_name TEXT NOT NULL CHECK(api_name IN ('PERPLEXITY', 'YFINANCE', 'ALPACA', 'ALPHA_VANTAGE', 'FRED')),
    endpoint TEXT,

    -- Call Details
    request_params TEXT,  -- JSON string
    response_status TEXT CHECK(response_status IN ('SUCCESS', 'ERROR', 'TIMEOUT', 'RATE_LIMITED')),
    response_time_ms INTEGER,
    error_message TEXT,

    -- Rate Limiting
    rate_limit_remaining INTEGER,
    rate_limit_reset DATETIME,

    call_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_research_api_calls_timestamp ON research_api_calls(call_timestamp DESC);
CREATE INDEX idx_research_api_calls_api ON research_api_calls(api_name, call_timestamp);

-- Notes for CC:
-- 1. Message tracking fields (message_id, request_message_id, response_message_id) are REVOLUTIONARY
--    v6.2 had no concept of message chains - this enables complete audit trail
-- 2. All tables designed FOR Research Department's specific needs (not adapted from v6.2)
-- 3. Sentiment cache reduces Perplexity API costs (24-hour cache window)
-- 4. API call log enables proactive rate limit management
-- 5. Candidate tickers table supports daily screening workflow
