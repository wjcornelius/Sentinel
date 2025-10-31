-- Portfolio Department Database Schema
-- Week 4: Portfolio Management, Position Tracking, Trade Order Generation
-- Built fresh from C(P) Week 4 specifications

-- Table 1: Portfolio Positions (What Portfolio WANTS to have open)
CREATE TABLE IF NOT EXISTS portfolio_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Position Identifier
    position_id TEXT UNIQUE NOT NULL,  -- POS_{YYYYMMDD}_{TICKER}_{UUID8}
    ticker TEXT NOT NULL,
    status TEXT CHECK(status IN ('PENDING', 'OPEN', 'CLOSED', 'REJECTED')) NOT NULL,

    -- Intended Trade (what Portfolio decided)
    intended_entry_price REAL NOT NULL,
    intended_shares INTEGER NOT NULL,
    intended_stop_loss REAL NOT NULL,
    intended_target REAL NOT NULL,

    -- Actual Execution (what Trading filled)
    actual_entry_price REAL,
    actual_entry_date DATE,
    actual_shares INTEGER,

    -- Exit Details
    exit_reason TEXT,  -- STOP_LOSS, TARGET, TIME, DOWNGRADE, MANUAL
    exit_price REAL,
    exit_date DATE,

    -- Risk Tracking
    risk_per_share REAL NOT NULL,
    total_risk REAL NOT NULL,

    -- Sector
    sector TEXT,

    -- Message Chain (audit trail)
    entry_order_message_id TEXT,  -- BuyOrder message sent to Trading
    exit_order_message_id TEXT,   -- SellOrder message sent to Trading
    risk_assessment_message_id TEXT,  -- Parent RiskAssessment message

    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE INDEX idx_portfolio_positions_ticker ON portfolio_positions(ticker);
CREATE INDEX idx_portfolio_positions_status ON portfolio_positions(status);
CREATE INDEX idx_portfolio_positions_position_id ON portfolio_positions(position_id);


-- Table 2: Portfolio Decisions (Audit trail of Portfolio's decisions)
CREATE TABLE IF NOT EXISTS portfolio_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Message IDs
    message_id TEXT UNIQUE NOT NULL,  -- Portfolio's message ID
    parent_message_id TEXT NOT NULL,  -- Risk's message ID

    -- Decision Metadata
    decision_type TEXT CHECK(decision_type IN ('BUY', 'SELL', 'HOLD', 'REJECT')) NOT NULL,
    decision_date DATE NOT NULL,
    decision_timestamp DATETIME NOT NULL,

    -- Portfolio State (snapshot at decision time)
    positions_before INTEGER NOT NULL,
    positions_after INTEGER NOT NULL,
    capital_deployed_before REAL NOT NULL,
    capital_deployed_after REAL NOT NULL,
    deployment_pct_before REAL NOT NULL,
    deployment_pct_after REAL NOT NULL,

    -- Decision Outcomes
    buy_orders_count INTEGER DEFAULT 0,
    sell_orders_count INTEGER DEFAULT 0,
    rejected_count INTEGER DEFAULT 0,

    -- Config Snapshot (what limits were active)
    max_positions INTEGER NOT NULL,
    max_capital_deployed_pct REAL NOT NULL,
    min_composite_score REAL NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_portfolio_decisions_date ON portfolio_decisions(decision_date DESC);
CREATE INDEX idx_portfolio_decisions_message ON portfolio_decisions(message_id);


-- Table 3: Portfolio Rejections (Candidates rejected by Portfolio)
CREATE TABLE IF NOT EXISTS portfolio_rejections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Links
    decision_message_id TEXT NOT NULL,  -- FK to portfolio_decisions.message_id
    ticker TEXT NOT NULL,
    decision_date DATE NOT NULL,

    -- Rejection Details
    rejection_reason TEXT NOT NULL,  -- MAX_POSITIONS_REACHED, INSUFFICIENT_CAPITAL, LOW_SCORE, etc.
    rejection_category TEXT CHECK(rejection_category IN ('CAPACITY', 'CAPITAL', 'SCORE', 'OTHER')) NOT NULL,
    rejection_details TEXT NOT NULL,

    -- What Would Have Been (for analysis)
    would_be_shares INTEGER,
    would_be_position_value REAL,
    would_be_risk REAL,
    research_composite_score REAL,

    decision_timestamp DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (decision_message_id) REFERENCES portfolio_decisions(message_id)
);

CREATE INDEX idx_portfolio_rejections_date ON portfolio_rejections(decision_date DESC);
CREATE INDEX idx_portfolio_rejections_ticker ON portfolio_rejections(ticker);
CREATE INDEX idx_portfolio_rejections_reason ON portfolio_rejections(rejection_category);


-- Notes:
-- - portfolio_positions: Tracks INTENDED state (what Portfolio wants)
-- - Trading Department will have separate table for ACTUAL executions
-- - Status flow: PENDING (order sent) → OPEN (filled) → CLOSED (exited)
-- - Status can also be: REJECTED (Trading couldn't fill)
-- - Complete audit trail via message_id linking
