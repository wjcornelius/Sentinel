# -*- coding: utf-8 -*-
# migrations/migrate_v7_to_v8_stop_only.py
# Database migration: v7 (dashboard) -> v8 (stop-loss only architecture)

"""
Migration Strategy:
1. Preserve all v7 data in archived tables (decisions, trades)
2. Create new v8 tables (entry_orders, stop_loss_orders, entry_stop_pairs)
3. Create indices for performance
4. Validate migration success
5. Generate migration report

SAFE TO RUN MULTIPLE TIMES: Checks for existing tables before creating.
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

DB_FILE = "sentinel.db"


def get_db_connection():
    """Get database connection with proper settings."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def check_table_exists(conn, table_name):
    """Check if table already exists."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table_name,))
    return cursor.fetchone() is not None


def archive_v7_data(conn):
    """
    Archive existing v7 data to separate tables.
    Preserves data for historical analysis and backtesting.
    """
    print("\n=== Step 1: Archiving v7 Data ===")

    cursor = conn.cursor()

    # Count existing records
    cursor.execute("SELECT COUNT(*) FROM decisions")
    decisions_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM trades")
    trades_count = cursor.fetchone()[0]

    print(f"  Found {decisions_count} decisions and {trades_count} trades to archive")

    # Archive decisions table
    if not check_table_exists(conn, 'archived_decisions_v7'):
        cursor.execute("""
            CREATE TABLE archived_decisions_v7 AS
            SELECT * FROM decisions
        """)
        print(f"  [OK] Created archived_decisions_v7 ({decisions_count} rows)")
    else:
        print(f"  [O] archived_decisions_v7 already exists, skipping")

    # Archive trades table
    if not check_table_exists(conn, 'archived_trades_v7'):
        cursor.execute("""
            CREATE TABLE archived_trades_v7 AS
            SELECT * FROM trades
        """)
        print(f"  [OK] Created archived_trades_v7 ({trades_count} rows)")
    else:
        print(f"  [O] archived_trades_v7 already exists, skipping")

    conn.commit()
    return decisions_count, trades_count


def create_v8_schema(conn):
    """
    Create new v8 schema for stop-loss only architecture.

    New tables:
    - entry_orders: Tracks limit buy/sell orders submitted for next trading day
    - stop_loss_orders: Tracks protective stop orders
    - entry_stop_pairs: Maintains relationships for cleanup operations
    """
    print("\n=== Step 2: Creating v8 Schema ===")

    cursor = conn.cursor()

    # ========================================================================
    # TABLE: entry_orders
    # ========================================================================
    if not check_table_exists(conn, 'entry_orders'):
        cursor.execute("""
            CREATE TABLE entry_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                strategy_signal_id INTEGER,
                order_id TEXT UNIQUE NOT NULL,
                client_order_id TEXT UNIQUE NOT NULL,
                side TEXT NOT NULL CHECK(side IN ('buy', 'sell')),
                qty INTEGER NOT NULL CHECK(qty > 0),
                order_type TEXT NOT NULL CHECK(order_type IN ('limit', 'market')),
                limit_price REAL,
                time_in_force TEXT DEFAULT 'day' CHECK(time_in_force IN ('day', 'gtc', 'ioc')),
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'filled', 'partial', 'cancelled', 'expired', 'rejected')),
                filled_at TIMESTAMP,
                filled_price REAL,
                filled_qty INTEGER,
                FOREIGN KEY (strategy_signal_id) REFERENCES decisions(id)
            )
        """)
        print("  [OK] Created entry_orders table")
    else:
        print("  [O] entry_orders table already exists")

    # ========================================================================
    # TABLE: stop_loss_orders
    # ========================================================================
    if not check_table_exists(conn, 'stop_loss_orders'):
        cursor.execute("""
            CREATE TABLE stop_loss_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_order_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                order_id TEXT UNIQUE NOT NULL,
                client_order_id TEXT UNIQUE NOT NULL,
                qty INTEGER NOT NULL CHECK(qty > 0),
                stop_price REAL NOT NULL CHECK(stop_price > 0),
                stop_type TEXT DEFAULT 'initial' CHECK(stop_type IN ('initial', 'trailing_conservative', 'trailing_moderate', 'trailing_aggressive', 'breakeven')),
                time_in_force TEXT DEFAULT 'gtc',
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active' CHECK(status IN ('active', 'triggered', 'cancelled', 'replaced')),
                triggered_at TIMESTAMP,
                triggered_price REAL,
                cancelled_at TIMESTAMP,
                cancel_reason TEXT,
                replaced_by_stop_id INTEGER,
                FOREIGN KEY (entry_order_id) REFERENCES entry_orders(id),
                FOREIGN KEY (replaced_by_stop_id) REFERENCES stop_loss_orders(id)
            )
        """)
        print("  [OK] Created stop_loss_orders table")
    else:
        print("  [O] stop_loss_orders table already exists")

    # ========================================================================
    # TABLE: entry_stop_pairs
    # ========================================================================
    if not check_table_exists(conn, 'entry_stop_pairs'):
        cursor.execute("""
            CREATE TABLE entry_stop_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_order_id INTEGER NOT NULL,
                stop_order_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                entry_price REAL,
                stop_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                resolution TEXT CHECK(resolution IN (
                    'entry_unfilled',
                    'stop_triggered',
                    'manual_exit',
                    'still_active',
                    NULL
                )),
                notes TEXT,
                FOREIGN KEY (entry_order_id) REFERENCES entry_orders(id),
                FOREIGN KEY (stop_order_id) REFERENCES stop_loss_orders(id),
                UNIQUE(entry_order_id, stop_order_id)
            )
        """)
        print("  [OK] Created entry_stop_pairs table")
    else:
        print("  [O] entry_stop_pairs table already exists")

    conn.commit()


def create_indices(conn):
    """Create indices for query performance."""
    print("\n=== Step 3: Creating Indices ===")

    cursor = conn.cursor()

    indices = [
        # entry_orders indices
        ("idx_entry_orders_symbol", "CREATE INDEX IF NOT EXISTS idx_entry_orders_symbol ON entry_orders(symbol)"),
        ("idx_entry_orders_status", "CREATE INDEX IF NOT EXISTS idx_entry_orders_status ON entry_orders(status)"),
        ("idx_entry_orders_submitted", "CREATE INDEX IF NOT EXISTS idx_entry_orders_submitted ON entry_orders(submitted_at)"),

        # stop_loss_orders indices
        ("idx_stop_loss_symbol", "CREATE INDEX IF NOT EXISTS idx_stop_loss_symbol ON stop_loss_orders(symbol)"),
        ("idx_stop_loss_status", "CREATE INDEX IF NOT EXISTS idx_stop_loss_status ON stop_loss_orders(status)"),
        ("idx_stop_loss_entry_id", "CREATE INDEX IF NOT EXISTS idx_stop_loss_entry_id ON stop_loss_orders(entry_order_id)"),

        # entry_stop_pairs indices
        ("idx_pairs_symbol", "CREATE INDEX IF NOT EXISTS idx_pairs_symbol ON entry_stop_pairs(symbol)"),
        ("idx_pairs_resolved", "CREATE INDEX IF NOT EXISTS idx_pairs_resolved ON entry_stop_pairs(resolved_at)"),
        ("idx_pairs_resolution", "CREATE INDEX IF NOT EXISTS idx_pairs_resolution ON entry_stop_pairs(resolution)"),
    ]

    for idx_name, idx_sql in indices:
        cursor.execute(idx_sql)
        print(f"  [OK] Created {idx_name}")

    conn.commit()


def create_views(conn):
    """Create helpful views for queries."""
    print("\n=== Step 4: Creating Views ===")

    cursor = conn.cursor()

    # View: Active positions with their protective stops
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_active_positions AS
        SELECT
            ep.symbol,
            ep.entry_price,
            e.filled_price AS actual_entry_price,
            e.filled_qty AS qty,
            s.stop_price AS current_stop_price,
            s.stop_type,
            s.status AS stop_status,
            e.filled_at AS entry_filled_at,
            ep.created_at AS pair_created_at
        FROM entry_stop_pairs ep
        JOIN entry_orders e ON ep.entry_order_id = e.id
        JOIN stop_loss_orders s ON ep.stop_order_id = s.id
        WHERE e.status = 'filled'
          AND s.status = 'active'
          AND ep.resolution IS NULL
    """)
    print("  [OK] Created view: v_active_positions")

    # View: Pending entry orders with their queued stops
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_pending_entries AS
        SELECT
            ep.symbol,
            e.order_id AS entry_order_id,
            e.limit_price,
            e.qty,
            e.submitted_at,
            s.order_id AS stop_order_id,
            s.stop_price
        FROM entry_stop_pairs ep
        JOIN entry_orders e ON ep.entry_order_id = e.id
        JOIN stop_loss_orders s ON ep.stop_order_id = s.id
        WHERE e.status = 'pending'
          AND ep.resolution IS NULL
    """)
    print("  [OK] Created view: v_pending_entries")

    # View: Orphaned stops (stop exists but no position)
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_orphaned_stops AS
        SELECT
            s.id,
            s.symbol,
            s.order_id,
            s.stop_price,
            s.submitted_at,
            e.status AS entry_status,
            ep.resolution
        FROM stop_loss_orders s
        JOIN entry_stop_pairs ep ON s.id = ep.stop_order_id
        JOIN entry_orders e ON ep.entry_order_id = e.id
        WHERE s.status = 'active'
          AND e.status IN ('cancelled', 'expired', 'rejected')
          AND ep.resolution IS NULL
    """)
    print("  [OK] Created view: v_orphaned_stops")

    conn.commit()


def validate_migration(conn):
    """Validate migration was successful."""
    print("\n=== Step 5: Validating Migration ===")

    cursor = conn.cursor()

    # Check all required tables exist
    required_tables = [
        'entry_orders',
        'stop_loss_orders',
        'entry_stop_pairs',
        'archived_decisions_v7',
        'archived_trades_v7'
    ]

    all_exist = True
    for table in required_tables:
        exists = check_table_exists(conn, table)
        status = "[OK]" if exists else "[X]"
        print(f"  {status} {table}: {'EXISTS' if exists else 'MISSING'}")
        if not exists:
            all_exist = False

    # Check row counts
    cursor.execute("SELECT COUNT(*) FROM entry_orders")
    entry_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM stop_loss_orders")
    stop_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM entry_stop_pairs")
    pair_count = cursor.fetchone()[0]

    print(f"\n  Current v8 data:")
    print(f"    Entry orders: {entry_count}")
    print(f"    Stop orders: {stop_count}")
    print(f"    Entry-stop pairs: {pair_count}")

    return all_exist


def generate_migration_report(conn, decisions_count, trades_count):
    """Generate comprehensive migration report."""
    print("\n" + "=" * 70)
    print("MIGRATION REPORT")
    print("=" * 70)

    cursor = conn.cursor()

    # Database file size
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    db_size = cursor.fetchone()[0]

    print(f"\nDatabase: {DB_FILE}")
    print(f"Size: {db_size:,} bytes ({db_size / 1024 / 1024:.2f} MB)")
    print(f"Migration date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\nArchived v7 Data:")
    print(f"  Decisions: {decisions_count}")
    print(f"  Trades: {trades_count}")

    print(f"\nNew v8 Tables:")
    for table in ['entry_orders', 'stop_loss_orders', 'entry_stop_pairs']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")

    print(f"\nViews Created:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name LIKE 'v_%'")
    views = cursor.fetchall()
    for view in views:
        print(f"  {view[0]}")

    print(f"\nIndices Created:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
    indices = cursor.fetchall()
    for idx in indices:
        print(f"  {idx[0]}")

    print("\n" + "=" * 70)
    print("[OK] Migration completed successfully")
    print("=" * 70)


def main():
    """Execute complete migration."""
    print("=" * 70)
    print("Sentinel v7 -> v8 Migration: Stop-Loss Only Architecture")
    print("=" * 70)

    try:
        conn = get_db_connection()

        # Step 1: Archive v7 data
        decisions_count, trades_count = archive_v7_data(conn)

        # Step 2: Create v8 schema
        create_v8_schema(conn)

        # Step 3: Create indices
        create_indices(conn)

        # Step 4: Create views
        create_views(conn)

        # Step 5: Validate
        success = validate_migration(conn)

        if not success:
            print("\n[X] Migration validation FAILED - some tables missing")
            return 1

        # Step 6: Report
        generate_migration_report(conn, decisions_count, trades_count)

        conn.close()
        return 0

    except Exception as e:
        print(f"\n[X] Migration FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
