"""
Database Consolidation Migration Script
Migrates tables from sentinel_corporation.db to sentinel.db

Tables to migrate:
1. market_regime_assessments (Research Department)
2. portfolio_snapshots (CEO/Executive)
"""

import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

print("\n" + "=" * 80)
print("DATABASE CONSOLIDATION MIGRATION")
print("=" * 80)

# Paths
source_db = Path("sentinel_corporation.db")
target_db = Path("sentinel.db")
backup_dir = Path("Backups/Database")
backup_dir.mkdir(parents=True, exist_ok=True)

# Step 1: Backup both databases
print("\n[1] Creating backups...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if target_db.exists():
    backup_target = backup_dir / f"sentinel_BEFORE_MERGE_{timestamp}.db"
    shutil.copy2(target_db, backup_target)
    print(f"    Backed up sentinel.db -> {backup_target.name}")

if source_db.exists():
    backup_source = backup_dir / f"sentinel_corporation_FINAL_{timestamp}.db"
    shutil.copy2(source_db, backup_source)
    print(f"    Backed up sentinel_corporation.db -> {backup_source.name}")
else:
    print("    ERROR: sentinel_corporation.db not found!")
    exit(1)

# Step 2: Get table schemas
print("\n[2] Reading table schemas from sentinel_corporation.db...")
source_conn = sqlite3.connect(source_db)
source_cursor = source_conn.cursor()

# Get CREATE TABLE statements
tables_to_migrate = ['market_regime_assessments', 'portfolio_snapshots']
schemas = {}

for table in tables_to_migrate:
    source_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'")
    result = source_cursor.fetchone()
    if result:
        schemas[table] = result[0]
        print(f"    Found schema for {table}")
    else:
        print(f"    WARNING: Table {table} not found in source database")

# Step 3: Migrate tables to target database
print("\n[3] Migrating tables to sentinel.db...")
target_conn = sqlite3.connect(target_db, timeout=30)
target_cursor = target_conn.cursor()

for table, schema in schemas.items():
    print(f"\n    Migrating {table}...")

    # Check if table already exists
    target_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
    if target_cursor.fetchone():
        print(f"      Table already exists in target - dropping and recreating")
        target_cursor.execute(f"DROP TABLE {table}")

    # Create table
    print(f"      Creating table...")
    target_cursor.execute(schema)

    # Copy data
    source_cursor.execute(f"SELECT * FROM {table}")
    rows = source_cursor.fetchall()

    if rows:
        # Get column count
        source_cursor.execute(f"PRAGMA table_info({table})")
        col_count = len(source_cursor.fetchall())

        placeholders = ','.join(['?' for _ in range(col_count)])
        target_cursor.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)

        print(f"      Copied {len(rows)} rows")
    else:
        print(f"      No data to copy (empty table)")

# Commit changes
target_conn.commit()
print("\n[4] Committing changes...")

# Verify migration
print("\n[5] Verifying migration...")
for table in tables_to_migrate:
    target_cursor.execute(f"SELECT COUNT(*) FROM {table}")
    target_count = target_cursor.fetchone()[0]

    source_cursor.execute(f"SELECT COUNT(*) FROM {table}")
    source_count = source_cursor.fetchone()[0]

    if target_count == source_count:
        print(f"    {table}: {target_count} rows [OK]")
    else:
        print(f"    {table}: {target_count} vs {source_count} rows [MISMATCH!]")

# Close connections
source_conn.close()
target_conn.close()

print("\n" + "=" * 80)
print("MIGRATION COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("  1. Update market_regime.py to use sentinel.db")
print("  2. Update ceo.py to use sentinel.db only")
print("  3. Update create_portfolio_tracking.py")
print("  4. Test all departments")
print("  5. Archive sentinel_corporation.db (do NOT delete - keep for safety)")
print("\n" + "=" * 80 + "\n")
