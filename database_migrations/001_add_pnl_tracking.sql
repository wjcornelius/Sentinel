-- Migration 001: Add P&L tracking columns to trades table
-- Enables accurate win rate and performance analysis

-- Add entry/exit price tracking
ALTER TABLE trades ADD COLUMN entry_price REAL DEFAULT NULL;
ALTER TABLE trades ADD COLUMN exit_price REAL DEFAULT NULL;

-- Add realized P&L tracking
ALTER TABLE trades ADD COLUMN realized_pnl REAL DEFAULT NULL;
ALTER TABLE trades ADD COLUMN pnl_percent REAL DEFAULT NULL;

-- Add trade metadata
ALTER TABLE trades ADD COLUMN trade_type TEXT DEFAULT NULL; -- 'ENTRY', 'EXIT', 'TRIM', 'ADD'
ALTER TABLE trades ADD COLUMN filled_at DATETIME DEFAULT NULL;
