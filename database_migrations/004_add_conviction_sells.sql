-- Migration 004: Add conviction_sells table
-- Purpose: Track SELL orders submitted based on Tier 3 conviction analysis
-- Author: Sentinel Week 3 Implementation
-- Date: 2025-10-27

CREATE TABLE IF NOT EXISTS conviction_sells (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    order_id TEXT UNIQUE NOT NULL,
    client_order_id TEXT UNIQUE NOT NULL,
    qty INTEGER NOT NULL CHECK(qty > 0),
    conviction_score INTEGER NOT NULL CHECK(conviction_score >= 1 AND conviction_score <= 100),
    reasoning TEXT,
    tier3_decision TEXT CHECK(tier3_decision IN ('SELL', 'sell')),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'filled', 'partial', 'cancelled', 'rejected')),
    filled_at TIMESTAMP,
    filled_price REAL,
    filled_qty INTEGER,
    realized_pl REAL,
    realized_pl_pct REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Index for quick lookups by symbol
CREATE INDEX IF NOT EXISTS idx_conviction_sells_symbol ON conviction_sells(symbol);

-- Index for status filtering
CREATE INDEX IF NOT EXISTS idx_conviction_sells_status ON conviction_sells(status);

-- Index for date-based queries
CREATE INDEX IF NOT EXISTS idx_conviction_sells_submitted ON conviction_sells(submitted_at);
