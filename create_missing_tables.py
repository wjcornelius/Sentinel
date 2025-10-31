"""
Directly create missing database tables from SQL schema files
Simple approach: just run the SQL
"""

import sqlite3
from pathlib import Path

def create_trading_tables():
    """Create Trading Department tables from SQL schema"""
    print("=" * 70)
    print("CREATING TRADING DEPARTMENT TABLES")
    print("=" * 70)

    schema_path = Path("Departments/Trading/database_schema.sql")
    if not schema_path.exists():
        print(f"[ERROR] Schema file not found: {schema_path}")
        return False

    # Read SQL schema
    with open(schema_path, 'r') as f:
        sql_schema = f.read()

    # Execute SQL
    try:
        conn = sqlite3.connect("sentinel.db")
        cursor = conn.cursor()

        # Split and execute each statement
        for statement in sql_schema.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        conn.commit()
        conn.close()

        print("[OK] Trading tables created successfully")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to create trading tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_research_table():
    """Create Research Department table manually (no schema file exists)"""
    print()
    print("=" * 70)
    print("CREATING RESEARCH DEPARTMENT TABLE")
    print("=" * 70)

    # Based on research_department.py usage patterns, create a simple table
    sql = """
    CREATE TABLE IF NOT EXISTS research_market_briefings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        briefing_date DATE NOT NULL UNIQUE,
        market_vix REAL,
        market_spy_change_pct REAL,
        market_status TEXT,
        top_candidates TEXT,  -- JSON list of tickers
        briefing_summary TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        conn = sqlite3.connect("sentinel.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

        print("[OK] Research table created successfully")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to create research table: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_tables():
    """Verify that the tables were created"""
    print()
    print("=" * 70)
    print("VERIFYING DATABASE TABLES")
    print("=" * 70)

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\nTotal tables found: {len(tables)}")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        status = "[NEW]" if table in ['research_market_briefings', 'trading_orders', 'trading_fills',
                                       'trading_rejections', 'trading_daily_logs', 'trading_duplicate_cache'] else ""
        print(f"  {status:6} {table}: {count} rows")

    conn.close()

    # Check for critical tables
    required_tables = ['research_market_briefings', 'trading_orders']
    missing = [t for t in required_tables if t not in tables]

    if missing:
        print(f"\n[WARNING] Still missing tables: {missing}")
        return False
    else:
        print(f"\n[OK] All required tables found!")
        return True

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DATABASE TABLE CREATION")
    print("=" * 70)
    print("Creating missing tables for 100% end-to-end test pass rate")
    print()

    # Create tables
    trading_ok = create_trading_tables()
    research_ok = create_research_table()

    # Verify tables were created
    tables_ok = verify_tables()

    # Final summary
    print()
    print("=" * 70)
    print("CREATION SUMMARY")
    print("=" * 70)
    print(f"Trading Tables:  {'[OK]' if trading_ok else '[FAIL]'}")
    print(f"Research Table:  {'[OK]' if research_ok else '[FAIL]'}")
    print(f"Tables Verified: {'[OK]' if tables_ok else '[FAIL]'}")
    print("=" * 70)

    if trading_ok and research_ok and tables_ok:
        print("\n[SUCCESS] All tables created! Ready for 100% test pass rate.")
        print("\nNext step: Run 'python test_end_to_end.py' to verify.")
    else:
        print("\n[WARNING] Some table creation failed. Check errors above.")

    print()
