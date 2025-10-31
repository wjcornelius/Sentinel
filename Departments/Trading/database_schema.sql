-- TRADING DEPARTMENT DATABASE SCHEMA
-- Built fresh for Sentinel Corporation Phase 1
-- Based on DEPARTMENTAL_SPECIFICATIONS v1.0
-- Date: 2025-10-31

-- Orders table: All orders submitted to Alpaca
CREATE TABLE IF NOT EXISTS trading_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE NOT NULL,           -- Our internal order ID
    alpaca_order_id TEXT UNIQUE,             -- Alpaca's order ID (after submission)
    ticker TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    order_type TEXT NOT NULL CHECK(order_type IN ('MARKET', 'LIMIT')),
    limit_price REAL,                        -- NULL for market orders

    -- Message chain tracking (REVOLUTIONARY - links to message protocol)
    executive_approval_msg_id TEXT NOT NULL, -- Link to Executive's approval message
    portfolio_request_msg_id TEXT,           -- Link to Portfolio's original request

    -- Status tracking
    status TEXT NOT NULL CHECK(status IN ('PENDING', 'SUBMITTED', 'FILLED', 'PARTIAL', 'REJECTED', 'CANCELLED')),
    submitted_timestamp DATETIME,            -- When we submitted to Alpaca

    -- Hard constraint validation
    hard_constraints_passed BOOLEAN NOT NULL DEFAULT 0,
    constraint_violations TEXT,              -- JSON array of any violations found

    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Fills table: All order fill events from Alpaca
CREATE TABLE IF NOT EXISTS trading_fills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,               -- FK to trading_orders

    -- Fill details
    fill_price REAL NOT NULL,
    quantity_filled INTEGER NOT NULL,
    commission REAL DEFAULT 0.00,
    fill_timestamp DATETIME NOT NULL,

    -- Slippage tracking
    expected_price REAL,                     -- What we expected to pay
    slippage_pct REAL,                       -- Actual slippage percentage
    slippage_flag BOOLEAN DEFAULT 0,         -- TRUE if slippage >2%

    -- Alpaca details
    alpaca_fill_id TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES trading_orders(id)
);

-- Rejections table: All order rejection events
CREATE TABLE IF NOT EXISTS trading_rejections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,               -- FK to trading_orders

    -- Rejection details
    rejection_reason TEXT NOT NULL,
    rejection_code TEXT,                     -- Alpaca's error code
    rejection_timestamp DATETIME NOT NULL,

    -- Was this a hard constraint violation or Alpaca rejection?
    rejection_source TEXT NOT NULL CHECK(rejection_source IN ('HARD_CONSTRAINT', 'ALPACA', 'DUPLICATE')),

    -- Escalation tracking
    escalated_to_executive BOOLEAN DEFAULT 0,
    escalation_msg_id TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES trading_orders(id)
);

-- Execution reports: Daily summary logs for Compliance
CREATE TABLE IF NOT EXISTS trading_daily_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date DATE NOT NULL UNIQUE,

    -- Summary stats
    total_orders INTEGER DEFAULT 0,
    total_fills INTEGER DEFAULT 0,
    total_rejections INTEGER DEFAULT 0,
    total_volume_traded REAL DEFAULT 0.00,   -- Dollar volume
    total_commissions REAL DEFAULT 0.00,

    -- Slippage stats
    avg_slippage_pct REAL DEFAULT 0.00,
    max_slippage_pct REAL DEFAULT 0.00,
    slippage_events INTEGER DEFAULT 0,       -- Count of >2% slippage

    -- Message tracking
    compliance_report_msg_id TEXT,           -- Link to Compliance log message

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Duplicate detection cache: Prevents accidental duplicate orders
CREATE TABLE IF NOT EXISTS trading_duplicate_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    action TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    submitted_timestamp DATETIME NOT NULL,
    order_id INTEGER NOT NULL,               -- FK to trading_orders

    -- Auto-cleanup old entries (keep last 5 minutes only)
    expires_at DATETIME NOT NULL,

    FOREIGN KEY (order_id) REFERENCES trading_orders(id)
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_trading_orders_status ON trading_orders(status);
CREATE INDEX IF NOT EXISTS idx_trading_orders_ticker ON trading_orders(ticker);
CREATE INDEX IF NOT EXISTS idx_trading_orders_alpaca_id ON trading_orders(alpaca_order_id);
CREATE INDEX IF NOT EXISTS idx_trading_fills_order_id ON trading_fills(order_id);
CREATE INDEX IF NOT EXISTS idx_trading_fills_timestamp ON trading_fills(fill_timestamp);
CREATE INDEX IF NOT EXISTS idx_trading_rejections_order_id ON trading_rejections(order_id);
CREATE INDEX IF NOT EXISTS idx_trading_duplicate_cache_expires ON trading_duplicate_cache(expires_at);

-- Trigger to auto-update updated_at timestamps
CREATE TRIGGER IF NOT EXISTS update_trading_orders_timestamp
AFTER UPDATE ON trading_orders
BEGIN
    UPDATE trading_orders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_trading_daily_logs_timestamp
AFTER UPDATE ON trading_daily_logs
BEGIN
    UPDATE trading_daily_logs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
