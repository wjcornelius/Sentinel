-- Migration 002: Create portfolio_snapshots table
-- Stores daily portfolio state for historical analysis and charting

CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date DATE NOT NULL UNIQUE,
    timestamp DATETIME NOT NULL,
    equity REAL NOT NULL,
    cash REAL,
    positions_count INTEGER,
    daily_pnl REAL,
    daily_pnl_percent REAL,
    ytd_pnl REAL,
    ytd_pnl_percent REAL,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_snapshot_date ON portfolio_snapshots(snapshot_date);
