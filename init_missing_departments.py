"""
Initialize missing Research and Trading Department database tables
This will create the tables needed for 100% end-to-end test pass rate
"""

import sys
from pathlib import Path
import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import configuration
from config import PERPLEXITY_API_KEY

# Import departments
from Departments.Research.research_department import ResearchDepartment
from Departments.Trading.trading_department import TradingDepartment

def init_research_department():
    """Initialize Research Department and create research_market_briefings table"""
    print("=" * 70)
    print("INITIALIZING RESEARCH DEPARTMENT")
    print("=" * 70)

    # Load research config
    config_path = Path("Config/research_config.yaml")
    if not config_path.exists():
        print(f"[ERROR] Config file not found: {config_path}")
        return False

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize Research Department
    try:
        research = ResearchDepartment(
            config=config,
            perplexity_api_key=PERPLEXITY_API_KEY,
            db_path=Path("sentinel.db")
        )
        print("[OK] Research Department initialized successfully")
        print(f"[OK] Database tables should now exist in sentinel.db")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize Research Department: {e}")
        import traceback
        traceback.print_exc()
        return False

def init_trading_department():
    """Initialize Trading Department and create trading_orders table"""
    print()
    print("=" * 70)
    print("INITIALIZING TRADING DEPARTMENT")
    print("=" * 70)

    # Initialize Trading Department
    try:
        trading = TradingDepartment(db_path="sentinel.db")
        print("[OK] Trading Department initialized successfully")
        print(f"[OK] Database tables should now exist in sentinel.db")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize Trading Department: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_tables():
    """Verify that the tables were created"""
    import sqlite3

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
        print(f"  - {table}: {count} rows")

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
    print("DEPARTMENT TABLE INITIALIZATION")
    print("=" * 70)
    print("This script will initialize Research and Trading departments")
    print("to create missing database tables needed for 100% test pass rate.")
    print()

    # Initialize departments
    research_ok = init_research_department()
    trading_ok = init_trading_department()

    # Verify tables were created
    tables_ok = verify_tables()

    # Final summary
    print()
    print("=" * 70)
    print("INITIALIZATION SUMMARY")
    print("=" * 70)
    print(f"Research Department: {'[OK]' if research_ok else '[FAIL]'}")
    print(f"Trading Department:  {'[OK]' if trading_ok else '[FAIL]'}")
    print(f"Tables Verified:     {'[OK]' if tables_ok else '[FAIL]'}")
    print("=" * 70)

    if research_ok and trading_ok and tables_ok:
        print("\n[SUCCESS] All departments initialized! Ready for 100% test pass rate.")
        print("\nNext step: Run 'python test_end_to_end.py' to verify.")
    else:
        print("\n[WARNING] Some initialization steps failed. Check errors above.")

    print()
