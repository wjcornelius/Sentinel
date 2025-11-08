"""
Create portfolio_snapshots table in sentinel.db
This will track portfolio value over time for performance analysis

NOTE: This table was migrated from sentinel_corporation.db during
database consolidation on 2025-11-08. Now all tables are in sentinel.db.
"""

import sqlite3
from pathlib import Path

# Database path (consolidated database)
db_path = Path(__file__).parent / "sentinel.db"

print(f"Creating portfolio tracking table in: {db_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create portfolio_snapshots table
cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    total_value REAL,
    cash_balance REAL,
    equity_value REAL,
    buying_power REAL,
    margin_used REAL,
    positions_count INTEGER,
    daily_pl REAL,
    daily_pl_pct REAL,
    spy_close REAL,
    spy_change_pct REAL,
    source TEXT,
    notes TEXT
)
""")

print("[OK] Created portfolio_snapshots table")

# Create index on timestamp for fast queries
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_portfolio_snapshots_timestamp
ON portfolio_snapshots(timestamp DESC)
""")

print("[OK] Created timestamp index")

# Commit and close
conn.commit()
conn.close()

print("\n[OK] Portfolio tracking database ready!")
print("\nTable structure:")
print("  - snapshot_id: Unique ID for each snapshot")
print("  - timestamp: When the snapshot was taken")
print("  - total_value: Total account value (equity + cash)")
print("  - cash_balance: Cash available")
print("  - equity_value: Total value of positions")
print("  - buying_power: Available buying power (includes margin)")
print("  - margin_used: Amount of margin currently used")
print("  - positions_count: Number of open positions")
print("  - daily_pl: Daily profit/loss in dollars")
print("  - daily_pl_pct: Daily profit/loss percentage")
print("  - spy_close: S&P 500 close price for comparison")
print("  - spy_change_pct: S&P 500 daily change for comparison")
print("  - source: Where snapshot came from (alpaca_api, trade_execution, etc)")
print("  - notes: Optional notes about this snapshot")
