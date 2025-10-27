# -*- coding: utf-8 -*-
# tests/test_database_operations.py
# Unit Tests for Database Operations - Week 1
# Stop-Loss Only Architecture

"""
Unit tests for database operations without requiring Alpaca API.
Tests database schema, queries, and data integrity.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# DATABASE SETUP FOR TESTS
# ============================================================================

def get_test_db_connection():
    """Create in-memory database for testing."""
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_test_schema(conn):
    """Create test database schema."""
    cursor = conn.cursor()

    # entry_orders table
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
            time_in_force TEXT DEFAULT 'day',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'filled', 'partial', 'cancelled', 'expired', 'rejected')),
            filled_at TIMESTAMP,
            filled_price REAL,
            filled_qty INTEGER
        )
    """)

    # stop_loss_orders table
    cursor.execute("""
        CREATE TABLE stop_loss_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_order_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            order_id TEXT UNIQUE NOT NULL,
            client_order_id TEXT UNIQUE NOT NULL,
            qty INTEGER NOT NULL CHECK(qty > 0),
            stop_price REAL NOT NULL CHECK(stop_price > 0),
            stop_type TEXT DEFAULT 'initial',
            time_in_force TEXT DEFAULT 'gtc',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'triggered', 'cancelled', 'replaced')),
            triggered_at TIMESTAMP,
            triggered_price REAL,
            cancelled_at TIMESTAMP,
            cancel_reason TEXT,
            replaced_by_stop_id INTEGER,
            FOREIGN KEY (entry_order_id) REFERENCES entry_orders(id)
        )
    """)

    # entry_stop_pairs table
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
            resolution TEXT,
            notes TEXT,
            FOREIGN KEY (entry_order_id) REFERENCES entry_orders(id),
            FOREIGN KEY (stop_order_id) REFERENCES stop_loss_orders(id),
            UNIQUE(entry_order_id, stop_order_id)
        )
    """)

    conn.commit()
    return conn


# ============================================================================
# TEST: Schema Creation
# ============================================================================

def test_schema_creation():
    """Test that database schema creates correctly."""
    print("\n[TEST] Schema Creation")

    conn = get_test_db_connection()
    conn = create_test_schema(conn)

    cursor = conn.cursor()

    # Verify tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    assert 'entry_orders' in tables, "entry_orders table not created"
    assert 'stop_loss_orders' in tables, "stop_loss_orders table not created"
    assert 'entry_stop_pairs' in tables, "entry_stop_pairs table not created"

    print("  [OK] All tables created successfully")

    conn.close()
    return True


# ============================================================================
# TEST: Entry Order CRUD
# ============================================================================

def test_entry_order_crud():
    """Test entry order create, read, update operations."""
    print("\n[TEST] Entry Order CRUD")

    conn = get_test_db_connection()
    conn = create_test_schema(conn)
    cursor = conn.cursor()

    # CREATE
    cursor.execute("""
        INSERT INTO entry_orders (
            symbol, order_id, client_order_id, side, qty, order_type, limit_price, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ('AAPL', 'order_123', 'client_123', 'buy', 10, 'limit', 150.00, 'pending'))

    entry_id = cursor.lastrowid
    assert entry_id == 1, "Entry order ID should be 1"

    # READ
    cursor.execute("SELECT * FROM entry_orders WHERE id = ?", (entry_id,))
    row = cursor.fetchone()

    assert row['symbol'] == 'AAPL', "Symbol mismatch"
    assert row['qty'] == 10, "Quantity mismatch"
    assert row['status'] == 'pending', "Status mismatch"

    print("  [OK] Entry order created and read successfully")

    # UPDATE (mark as filled)
    cursor.execute("""
        UPDATE entry_orders
        SET status = 'filled', filled_at = ?, filled_price = ?, filled_qty = ?
        WHERE id = ?
    """, (datetime.now(timezone.utc), 150.10, 10, entry_id))

    cursor.execute("SELECT status, filled_price FROM entry_orders WHERE id = ?", (entry_id,))
    row = cursor.fetchone()

    assert row['status'] == 'filled', "Status not updated"
    assert abs(row['filled_price'] - 150.10) < 0.01, "Fill price mismatch"

    print("  [OK] Entry order updated successfully")

    conn.close()
    return True


# ============================================================================
# TEST: Stop Loss Order CRUD
# ============================================================================

def test_stop_order_crud():
    """Test stop loss order create, read, update operations."""
    print("\n[TEST] Stop Loss Order CRUD")

    conn = get_test_db_connection()
    conn = create_test_schema(conn)
    cursor = conn.cursor()

    # First create entry order (foreign key requirement)
    cursor.execute("""
        INSERT INTO entry_orders (
            symbol, order_id, client_order_id, side, qty, order_type, limit_price
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('AAPL', 'entry_123', 'client_123', 'buy', 10, 'limit', 150.00))

    entry_id = cursor.lastrowid

    # CREATE stop
    cursor.execute("""
        INSERT INTO stop_loss_orders (
            entry_order_id, symbol, order_id, client_order_id, qty, stop_price, stop_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (entry_id, 'AAPL', 'stop_123', 'client_stop_123', 10, 138.00, 'initial'))

    stop_id = cursor.lastrowid
    assert stop_id == 1, "Stop order ID should be 1"

    # READ
    cursor.execute("SELECT * FROM stop_loss_orders WHERE id = ?", (stop_id,))
    row = cursor.fetchone()

    assert row['stop_price'] == 138.00, "Stop price mismatch"
    assert row['status'] == 'active', "Status should be active"

    print("  [OK] Stop order created and read successfully")

    # UPDATE (cancel stop)
    cursor.execute("""
        UPDATE stop_loss_orders
        SET status = 'cancelled', cancelled_at = ?, cancel_reason = ?
        WHERE id = ?
    """, (datetime.now(timezone.utc), 'entry_unfilled', stop_id))

    cursor.execute("SELECT status, cancel_reason FROM stop_loss_orders WHERE id = ?", (stop_id,))
    row = cursor.fetchone()

    assert row['status'] == 'cancelled', "Status not updated"
    assert row['cancel_reason'] == 'entry_unfilled', "Cancel reason mismatch"

    print("  [OK] Stop order updated successfully")

    conn.close()
    return True


# ============================================================================
# TEST: Entry-Stop Pair Relationship
# ============================================================================

def test_entry_stop_pair():
    """Test entry-stop pair relationship and constraints."""
    print("\n[TEST] Entry-Stop Pair Relationship")

    conn = get_test_db_connection()
    conn = create_test_schema(conn)
    cursor = conn.cursor()

    # Create entry
    cursor.execute("""
        INSERT INTO entry_orders (
            symbol, order_id, client_order_id, side, qty, order_type, limit_price
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('AAPL', 'entry_123', 'client_123', 'buy', 10, 'limit', 150.00))
    entry_id = cursor.lastrowid

    # Create stop
    cursor.execute("""
        INSERT INTO stop_loss_orders (
            entry_order_id, symbol, order_id, client_order_id, qty, stop_price
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (entry_id, 'AAPL', 'stop_123', 'client_stop_123', 10, 138.00))
    stop_id = cursor.lastrowid

    # Create pair
    cursor.execute("""
        INSERT INTO entry_stop_pairs (
            entry_order_id, stop_order_id, symbol, entry_price, stop_price
        ) VALUES (?, ?, ?, ?, ?)
    """, (entry_id, stop_id, 'AAPL', 150.00, 138.00))
    pair_id = cursor.lastrowid

    # Verify pair
    cursor.execute("SELECT * FROM entry_stop_pairs WHERE id = ?", (pair_id,))
    row = cursor.fetchone()

    assert row['entry_order_id'] == entry_id, "Entry ID mismatch"
    assert row['stop_order_id'] == stop_id, "Stop ID mismatch"
    assert row['symbol'] == 'AAPL', "Symbol mismatch"

    print("  [OK] Entry-stop pair created successfully")

    # Test unique constraint (should fail if we try to create duplicate)
    try:
        cursor.execute("""
            INSERT INTO entry_stop_pairs (
                entry_order_id, stop_order_id, symbol, entry_price, stop_price
            ) VALUES (?, ?, ?, ?, ?)
        """, (entry_id, stop_id, 'AAPL', 150.00, 138.00))
        assert False, "Duplicate pair should have failed unique constraint"
    except sqlite3.IntegrityError:
        print("  [OK] Unique constraint prevents duplicate pairs")

    conn.close()
    return True


# ============================================================================
# TEST: Foreign Key Constraints
# ============================================================================

def test_foreign_key_constraints():
    """Test that foreign key constraints are enforced."""
    print("\n[TEST] Foreign Key Constraints")

    conn = get_test_db_connection()
    conn = create_test_schema(conn)
    cursor = conn.cursor()

    # Try to create stop without corresponding entry (should fail)
    try:
        cursor.execute("""
            INSERT INTO stop_loss_orders (
                entry_order_id, symbol, order_id, client_order_id, qty, stop_price
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (999, 'AAPL', 'stop_123', 'client_123', 10, 138.00))
        assert False, "Foreign key constraint should have failed"
    except sqlite3.IntegrityError:
        print("  [OK] Foreign key constraint prevents orphaned stops")

    conn.close()
    return True


# ============================================================================
# TEST: Query Active Positions
# ============================================================================

def test_query_active_positions():
    """Test querying active positions with joins."""
    print("\n[TEST] Query Active Positions")

    conn = get_test_db_connection()
    conn = create_test_schema(conn)
    cursor = conn.cursor()

    # Create sample data
    # Position 1: AAPL (filled, active stop)
    cursor.execute("""
        INSERT INTO entry_orders (
            symbol, order_id, client_order_id, side, qty, order_type, limit_price, status, filled_price, filled_qty
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('AAPL', 'entry_1', 'client_1', 'buy', 10, 'limit', 150.00, 'filled', 150.10, 10))
    entry1_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO stop_loss_orders (
            entry_order_id, symbol, order_id, client_order_id, qty, stop_price, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (entry1_id, 'AAPL', 'stop_1', 'client_stop_1', 10, 138.00, 'active'))
    stop1_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO entry_stop_pairs (
            entry_order_id, stop_order_id, symbol, entry_price, stop_price
        ) VALUES (?, ?, ?, ?, ?)
    """, (entry1_id, stop1_id, 'AAPL', 150.00, 138.00))

    # Position 2: MSFT (filled, active stop)
    cursor.execute("""
        INSERT INTO entry_orders (
            symbol, order_id, client_order_id, side, qty, order_type, limit_price, status, filled_price, filled_qty
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('MSFT', 'entry_2', 'client_2', 'buy', 5, 'limit', 300.00, 'filled', 300.50, 5))
    entry2_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO stop_loss_orders (
            entry_order_id, symbol, order_id, client_order_id, qty, stop_price, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (entry2_id, 'MSFT', 'stop_2', 'client_stop_2', 5, 276.00, 'active'))
    stop2_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO entry_stop_pairs (
            entry_order_id, stop_order_id, symbol, entry_price, stop_price
        ) VALUES (?, ?, ?, ?, ?)
    """, (entry2_id, stop2_id, 'MSFT', 300.00, 276.00))

    # Query active positions
    cursor.execute("""
        SELECT
            ep.symbol,
            e.filled_price AS entry_price,
            e.filled_qty AS qty,
            s.stop_price,
            s.stop_type
        FROM entry_stop_pairs ep
        JOIN entry_orders e ON ep.entry_order_id = e.id
        JOIN stop_loss_orders s ON ep.stop_order_id = s.id
        WHERE e.status = 'filled'
          AND s.status = 'active'
          AND ep.resolution IS NULL
    """)

    positions = cursor.fetchall()

    assert len(positions) == 2, f"Expected 2 active positions, got {len(positions)}"

    # Verify AAPL
    aapl = [p for p in positions if p['symbol'] == 'AAPL'][0]
    assert aapl['qty'] == 10, f"AAPL quantity mismatch: expected 10, got {aapl['qty']}"
    assert abs(aapl['entry_price'] - 150.10) < 0.01, f"AAPL entry price mismatch: expected 150.10, got {aapl['entry_price']}"
    assert aapl['stop_price'] == 138.00, f"AAPL stop price mismatch: expected 138.00, got {aapl['stop_price']}"

    print("  [OK] Active positions queried successfully")

    conn.close()
    return True


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all database tests."""
    print("\n" + "=" * 70)
    print("DATABASE UNIT TESTS - STOP-LOSS ARCHITECTURE")
    print("=" * 70)

    tests = [
        ("Schema Creation", test_schema_creation),
        ("Entry Order CRUD", test_entry_order_crud),
        ("Stop Order CRUD", test_stop_order_crud),
        ("Entry-Stop Pair", test_entry_stop_pair),
        ("Foreign Key Constraints", test_foreign_key_constraints),
        ("Query Active Positions", test_query_active_positions),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"  [FAIL] {test_name}: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
