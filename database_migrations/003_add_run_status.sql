-- Migration 003: Create run_status table
-- Tracks each Sentinel run for monitoring and safe abort handling

CREATE TABLE IF NOT EXISTS run_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date DATE NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    status TEXT NOT NULL, -- 'running', 'completed', 'aborted', 'failed'
    current_stage TEXT,   -- 'stage0', 'stage1', etc.
    abort_reason TEXT,
    error_message TEXT,
    trades_executed INTEGER DEFAULT 0,
    UNIQUE(run_date)
);

CREATE INDEX IF NOT EXISTS idx_run_date ON run_status(run_date);
CREATE INDEX IF NOT EXISTS idx_run_status ON run_status(status);
