-- Risk Department Database Schema
-- Built fresh from C(P) Week 3 guidance + DEPARTMENTAL_SPECIFICATIONS v1.0
-- Date: 2025-10-31
-- Purpose: Track risk assessments, position sizing, stop-loss calculations, portfolio heat

-- Table 1: Risk Assessments (Daily risk evaluation of Research candidates)
CREATE TABLE IF NOT EXISTS risk_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Message Tracking (Revolutionary - links to Research Department)
    message_id TEXT UNIQUE NOT NULL,  -- e.g., MSG_RISK_20251031T090000Z_abc123
    parent_message_id TEXT NOT NULL,  -- Links to research_market_briefings.message_id

    -- Assessment Info
    assessment_date DATE NOT NULL,
    timestamp DATETIME NOT NULL,

    -- Portfolio Status at Time of Assessment
    current_capital REAL NOT NULL,  -- Total capital available (e.g., $100,000)
    current_heat REAL NOT NULL,  -- Current total risk across all open positions (e.g., $2,500)
    available_heat REAL NOT NULL,  -- Remaining risk capacity (e.g., $2,500)
    open_positions_count INTEGER NOT NULL,  -- Number of currently open positions

    -- Assessment Summary
    candidates_reviewed INTEGER NOT NULL,  -- How many candidates from Research
    candidates_approved INTEGER NOT NULL,  -- How many passed risk checks
    candidates_rejected INTEGER NOT NULL,  -- How many failed risk checks

    -- Risk Limits Applied (snapshot of config at assessment time)
    max_risk_per_trade_pct REAL NOT NULL,  -- e.g., 0.01 (1%)
    max_portfolio_heat_pct REAL NOT NULL,  -- e.g., 0.05 (5%)
    max_sector_concentration_pct REAL NOT NULL,  -- e.g., 0.40 (40%)
    position_size_pct REAL NOT NULL,  -- e.g., 0.10 (10% of capital)

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_risk_assessments_date ON risk_assessments(assessment_date DESC);
CREATE INDEX idx_risk_assessments_parent ON risk_assessments(parent_message_id);

CREATE TRIGGER IF NOT EXISTS update_risk_assessments_timestamp
AFTER UPDATE ON risk_assessments
FOR EACH ROW
BEGIN
    UPDATE risk_assessments
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;


-- Table 2: Approved Candidates (Candidates that passed all risk checks)
CREATE TABLE IF NOT EXISTS risk_approved_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Links
    message_id TEXT NOT NULL,  -- FK to risk_assessments.message_id
    ticker TEXT NOT NULL,
    assessment_date DATE NOT NULL,

    -- Research Scores (from parent Research briefing)
    research_composite_score REAL NOT NULL,  -- e.g., 6.0/10
    research_technical_score REAL,
    research_fundamental_score REAL,
    research_sentiment_score REAL,

    -- Position Sizing
    position_sizing_method TEXT NOT NULL,  -- e.g., "FIXED_FRACTIONAL"
    position_size_pct REAL NOT NULL,  -- Percentage of capital (e.g., 0.10 = 10%)
    position_size_shares INTEGER NOT NULL,  -- Number of shares to buy
    position_size_value REAL NOT NULL,  -- Dollar value of position (shares × entry_price)

    -- Entry & Exit
    entry_price REAL NOT NULL,  -- Current market price at assessment time
    stop_loss REAL NOT NULL,  -- Stop-loss price
    stop_loss_method TEXT NOT NULL,  -- e.g., "ATR_2X"
    atr_value REAL,  -- ATR value used for calculation (if applicable)
    target_price REAL,  -- Optional price target

    -- Risk Metrics
    risk_per_share REAL NOT NULL,  -- entry_price - stop_loss
    total_risk REAL NOT NULL,  -- position_size_shares × risk_per_share
    risk_percentage REAL NOT NULL,  -- total_risk / current_capital
    risk_reward_ratio REAL,  -- (target_price - entry_price) / (entry_price - stop_loss)

    -- Portfolio Impact
    portfolio_heat_before REAL NOT NULL,  -- Heat before this trade
    portfolio_heat_after REAL NOT NULL,  -- Heat after adding this trade
    sector TEXT,  -- Stock sector (for concentration tracking)
    sector_exposure_pct REAL,  -- Percentage of capital in this sector after trade

    -- Timestamps
    decision_timestamp DATETIME NOT NULL,  -- When this candidate was approved
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (message_id) REFERENCES risk_assessments(message_id)
);

CREATE INDEX idx_risk_approved_date ON risk_approved_candidates(assessment_date DESC);
CREATE INDEX idx_risk_approved_ticker ON risk_approved_candidates(ticker);
CREATE INDEX idx_risk_approved_message ON risk_approved_candidates(message_id);


-- Table 3: Rejected Candidates (Candidates that failed risk checks)
CREATE TABLE IF NOT EXISTS risk_rejected_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Links
    message_id TEXT NOT NULL,  -- FK to risk_assessments.message_id
    ticker TEXT NOT NULL,
    assessment_date DATE NOT NULL,

    -- Research Scores (from parent Research briefing)
    research_composite_score REAL NOT NULL,

    -- Rejection Details
    rejection_reason TEXT NOT NULL,  -- e.g., "PORTFOLIO_HEAT_EXCEEDED", "SECTOR_LIMIT", "RISK_TOO_HIGH"
    rejection_category TEXT CHECK(rejection_category IN ('PORTFOLIO_HEAT', 'SECTOR_CONCENTRATION', 'RISK_PER_TRADE', 'DATA_UNAVAILABLE', 'OTHER')),
    rejection_details TEXT,  -- Additional context (e.g., "Would push heat to 6.2%, limit is 5%")

    -- What Would Have Been (for analysis)
    would_be_position_size_shares INTEGER,
    would_be_total_risk REAL,
    would_be_portfolio_heat REAL,

    -- Timestamps
    decision_timestamp DATETIME NOT NULL,  -- When this candidate was rejected
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (message_id) REFERENCES risk_assessments(message_id)
);

CREATE INDEX idx_risk_rejected_date ON risk_rejected_candidates(assessment_date DESC);
CREATE INDEX idx_risk_rejected_ticker ON risk_rejected_candidates(ticker);
CREATE INDEX idx_risk_rejected_reason ON risk_rejected_candidates(rejection_category);


-- Notes for CC:
-- - All tables link via message_id for complete audit trail
-- - Portfolio status snapshot preserved (can see capital/heat at time of assessment)
-- - Risk limits snapshot preserved (can see what thresholds were active)
-- - Approved candidates have full position sizing calculations
-- - Rejected candidates preserve "what would have been" for backtesting
-- - Indexes on date fields for fast historical queries
-- - Timestamps track when decisions were made
