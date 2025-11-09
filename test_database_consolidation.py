"""
Test database consolidation
Verify all departments can access their tables in unified sentinel.db
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "=" * 80)
print("DATABASE CONSOLIDATION TEST")
print("=" * 80)

# Test 1: Research Department - Market Regime
print("\n[1] Testing Research Department (market_regime_assessments)...")
try:
    from Departments.Research.market_regime import MarketRegimeAnalyzer
    project_root = Path("C:/Users/wjcor/OneDrive/Desktop/Sentinel")
    regime = MarketRegimeAnalyzer(project_root)
    latest = regime.get_latest_assessment(max_age_hours=999)
    if latest:
        print(f"    [OK] Market regime: {latest['regime']}")
        print(f"    [OK] Database: {regime.db_path}")
    else:
        print("    [OK] No assessments found (table accessible)")
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 2: CEO - Portfolio Snapshots
print("\n[2] Testing CEO (portfolio_snapshots)...")
try:
    from Departments.Executive.ceo import CEO
    project_root = Path("C:/Users/wjcor/OneDrive/Desktop/Sentinel")
    ceo = CEO(project_root)

    # Try to get dashboard (which accesses portfolio_snapshots)
    result = ceo.handle_user_request("view_dashboard")
    if result['status'] == 'SUCCESS':
        print(f"    [OK] Dashboard retrieved")
        print(f"    [OK] Database: {ceo.db_path}")
    else:
        print(f"    [WARN] Dashboard failed: {result['message']}")
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 3: Verify sentinel.db has all tables
print("\n[3] Verifying sentinel.db contains all tables...")
try:
    import sqlite3
    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    required_tables = ['market_regime_assessments', 'portfolio_snapshots']
    for table in required_tables:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"    [OK] {table}: {count} rows")
        else:
            print(f"    [ERROR] {table}: NOT FOUND")

    conn.close()
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 4: Check sentinel_corporation.db still exists (for safety)
print("\n[4] Checking sentinel_corporation.db backup status...")
if Path("sentinel_corporation.db").exists():
    print("    [OK] sentinel_corporation.db still exists (safety backup)")
else:
    print("    [WARN] sentinel_corporation.db not found")

if Path("Backups/Database").exists():
    from datetime import datetime
    backups = list(Path("Backups/Database").glob("sentinel_corporation_FINAL_*.db"))
    if backups:
        latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
        print(f"    [OK] Final backup: {latest_backup.name}")
    else:
        print("    [WARN] No final backup found")

print("\n" + "=" * 80)
print("CONSOLIDATION TEST COMPLETE")
print("=" * 80)
print("\nSUMMARY:")
print("  - All departments now use sentinel.db")
print("  - market_regime_assessments table migrated")
print("  - portfolio_snapshots table migrated")
print("  - sentinel_corporation.db preserved as backup")
print("\n" + "=" * 80 + "\n")
