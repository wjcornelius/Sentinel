-- Compliance Department Database Schema
-- Week 5: Pre-Trade Validation, Post-Trade Auditing, Regulatory Reporting
-- Guards the system with configurable rules and comprehensive oversight

-- ============================================================================
-- Table 1: Trade Validations (Pre-Trade Checks)
-- ============================================================================
CREATE TABLE IF NOT EXISTS compliance_trade_validations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Message Tracking
    trade_proposal_message_id TEXT UNIQUE NOT NULL,  -- Portfolio's TradeProposal
    response_message_id TEXT NOT NULL,  -- Compliance's TradeApproval/Rejection

    -- Trade Details
    ticker TEXT NOT NULL,
    trade_type TEXT CHECK(trade_type IN ('BUY', 'SELL')) NOT NULL,
    shares INTEGER NOT NULL,
    price REAL NOT NULL,
    position_value REAL NOT NULL,

    -- Validation Result
    validation_status TEXT CHECK(validation_status IN ('APPROVED', 'REJECTED')) NOT NULL,
    validation_timestamp DATETIME NOT NULL,

    -- Rule Checks (each rule gets a pass/fail flag)
    position_size_check TEXT CHECK(position_size_check IN ('PASS', 'FAIL', 'SKIP')) DEFAULT 'SKIP',
    sector_concentration_check TEXT CHECK(sector_concentration_check IN ('PASS', 'FAIL', 'SKIP')) DEFAULT 'SKIP',
    risk_limit_check TEXT CHECK(risk_limit_check IN ('PASS', 'FAIL', 'SKIP')) DEFAULT 'SKIP',
    duplicate_order_check TEXT CHECK(duplicate_order_check IN ('PASS', 'FAIL', 'SKIP')) DEFAULT 'SKIP',
    restricted_ticker_check TEXT CHECK(restricted_ticker_check IN ('PASS', 'FAIL', 'SKIP')) DEFAULT 'SKIP',

    -- Rejection Details (populated if validation_status = 'REJECTED')
    rejection_reason TEXT,
    rejection_category TEXT CHECK(rejection_category IN ('POSITION_SIZE', 'SECTOR_LIMIT', 'RISK_LIMIT', 'DUPLICATE', 'RESTRICTED', 'OTHER')),
    rejection_details TEXT,

    -- Portfolio Context at Validation Time
    portfolio_positions_count INTEGER,
    portfolio_deployed_capital REAL,
    portfolio_total_risk REAL,
    sector TEXT,
    sector_allocation_pct REAL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_compliance_validations_ticker ON compliance_trade_validations(ticker);
CREATE INDEX idx_compliance_validations_status ON compliance_trade_validations(validation_status);
CREATE INDEX idx_compliance_validations_timestamp ON compliance_trade_validations(validation_timestamp DESC);


-- ============================================================================
-- Table 2: Trade Audits (Post-Trade Reviews)
-- ============================================================================
CREATE TABLE IF NOT EXISTS compliance_trade_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Position Tracking
    position_id TEXT NOT NULL,  -- Links to portfolio_positions.position_id
    ticker TEXT NOT NULL,

    -- Trade Execution Details
    intended_entry_price REAL NOT NULL,
    actual_entry_price REAL NOT NULL,
    intended_shares INTEGER NOT NULL,
    actual_shares INTEGER NOT NULL,

    -- Intended Risk Parameters
    intended_stop_loss REAL NOT NULL,
    intended_target REAL NOT NULL,

    -- Audit Results
    audit_status TEXT CHECK(audit_status IN ('PASS', 'WARN', 'FAIL')) NOT NULL,
    audit_timestamp DATETIME NOT NULL,

    -- Individual Audit Checks
    slippage_check TEXT CHECK(slippage_check IN ('PASS', 'WARN', 'FAIL')) DEFAULT 'PASS',
    slippage_pct REAL,
    slippage_amount REAL,

    partial_fill_check TEXT CHECK(partial_fill_check IN ('PASS', 'WARN', 'FAIL')) DEFAULT 'PASS',
    fill_rate REAL,

    stop_loss_accuracy_check TEXT CHECK(stop_loss_accuracy_check IN ('PASS', 'WARN', 'FAIL')) DEFAULT 'PASS',
    stop_loss_deviation_pct REAL,

    target_accuracy_check TEXT CHECK(target_accuracy_check IN ('PASS', 'WARN', 'FAIL')) DEFAULT 'PASS',
    target_deviation_pct REAL,

    -- Audit Findings
    findings TEXT,  -- Human-readable description of issues found
    severity TEXT CHECK(severity IN ('INFO', 'WARN', 'CRITICAL')),

    -- Execution Metadata
    fill_message_id TEXT,  -- Trading's FillConfirmation message
    trade_date DATE NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_compliance_audits_position ON compliance_trade_audits(position_id);
CREATE INDEX idx_compliance_audits_status ON compliance_trade_audits(audit_status);
CREATE INDEX idx_compliance_audits_date ON compliance_trade_audits(trade_date DESC);


-- ============================================================================
-- Table 3: Rule Violations (Limit Breaches)
-- ============================================================================
CREATE TABLE IF NOT EXISTS compliance_violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Violation Metadata
    violation_type TEXT CHECK(violation_type IN ('POSITION_SIZE', 'SECTOR_CONCENTRATION', 'RISK_LIMIT', 'DUPLICATE_ORDER', 'RESTRICTED_TICKER', 'SLIPPAGE', 'PARTIAL_FILL', 'OTHER')) NOT NULL,
    severity TEXT CHECK(severity IN ('INFO', 'WARN', 'CRITICAL')) NOT NULL,

    -- What Violated
    ticker TEXT,
    position_id TEXT,
    trade_proposal_message_id TEXT,

    -- Violation Details
    rule_name TEXT NOT NULL,
    rule_limit REAL,  -- The limit that was breached (e.g., 0.10 for 10%)
    actual_value REAL,  -- The actual value that breached (e.g., 0.15 for 15%)
    breach_amount REAL,  -- How much over the limit (e.g., 0.05 for 5% over)

    -- Description
    violation_description TEXT NOT NULL,

    -- Resolution
    resolution_status TEXT CHECK(resolution_status IN ('UNRESOLVED', 'ACKNOWLEDGED', 'RESOLVED')) DEFAULT 'UNRESOLVED',
    resolution_notes TEXT,
    resolved_at DATETIME,

    -- Timestamps
    violation_timestamp DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_compliance_violations_type ON compliance_violations(violation_type);
CREATE INDEX idx_compliance_violations_severity ON compliance_violations(severity);
CREATE INDEX idx_compliance_violations_status ON compliance_violations(resolution_status);
CREATE INDEX idx_compliance_violations_timestamp ON compliance_violations(violation_timestamp DESC);


-- ============================================================================
-- Table 4: Daily Compliance Reports (Regulatory Reporting)
-- ============================================================================
CREATE TABLE IF NOT EXISTS compliance_daily_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Report Metadata
    report_date DATE UNIQUE NOT NULL,
    report_generated_at DATETIME NOT NULL,

    -- Trade Statistics
    total_trades INTEGER DEFAULT 0,
    buy_trades INTEGER DEFAULT 0,
    sell_trades INTEGER DEFAULT 0,
    approved_trades INTEGER DEFAULT 0,
    rejected_trades INTEGER DEFAULT 0,

    -- Validation Statistics
    total_validations INTEGER DEFAULT 0,
    position_size_failures INTEGER DEFAULT 0,
    sector_limit_failures INTEGER DEFAULT 0,
    risk_limit_failures INTEGER DEFAULT 0,
    duplicate_order_failures INTEGER DEFAULT 0,
    restricted_ticker_failures INTEGER DEFAULT 0,

    -- Audit Statistics
    total_audits INTEGER DEFAULT 0,
    audit_pass INTEGER DEFAULT 0,
    audit_warn INTEGER DEFAULT 0,
    audit_fail INTEGER DEFAULT 0,
    slippage_warnings INTEGER DEFAULT 0,
    partial_fill_warnings INTEGER DEFAULT 0,

    -- Violation Statistics
    total_violations INTEGER DEFAULT 0,
    critical_violations INTEGER DEFAULT 0,
    warn_violations INTEGER DEFAULT 0,
    unresolved_violations INTEGER DEFAULT 0,

    -- Portfolio Metrics (snapshot at end of day)
    positions_count INTEGER,
    deployed_capital REAL,
    total_portfolio_risk REAL,
    largest_position_pct REAL,
    largest_sector_pct REAL,

    -- Report File Path
    report_file_path TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_compliance_reports_date ON compliance_daily_reports(report_date DESC);


-- ============================================================================
-- Notes:
-- ============================================================================
-- 1. Pre-Trade Validation Flow:
--    Portfolio → TradeProposal → Compliance validates → TradeApproval/Rejection → Portfolio
--
-- 2. Post-Trade Audit Flow:
--    Trading → FillConfirmation → Portfolio updates position → Compliance audits fill
--
-- 3. Daily Report Flow:
--    Compliance aggregates all validations, audits, violations → Generates report
--
-- 4. Violation Tracking:
--    Any rule breach logged to compliance_violations for human review
--
-- 5. Complete Audit Trail:
--    Every trade validated (compliance_trade_validations)
--    Every fill audited (compliance_trade_audits)
--    Every violation tracked (compliance_violations)
--    Daily summaries generated (compliance_daily_reports)
