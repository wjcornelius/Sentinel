"""
Analyze both databases to understand schema differences
"""

import sqlite3
from pathlib import Path

def get_database_info(db_path):
    """Get tables and their schemas from a database"""
    if not Path(db_path).exists():
        return None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    info = {}
    for table in tables:
        # Get schema
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        info[table] = {
            'columns': [(col[1], col[2]) for col in columns],  # (name, type)
            'row_count': count
        }

    conn.close()
    return tables, info

print("\n" + "=" * 80)
print("DATABASE ANALYSIS")
print("=" * 80)

# Analyze sentinel.db
print("\n[1] Analyzing sentinel.db...")
if Path("sentinel.db").exists():
    tables1, info1 = get_database_info("sentinel.db")
    print(f"    Tables found: {len(tables1)}")
    for table in tables1:
        print(f"      - {table}: {info1[table]['row_count']} rows, {len(info1[table]['columns'])} columns")
else:
    print("    FILE NOT FOUND")
    tables1, info1 = [], {}

# Analyze sentinel_corporation.db
print("\n[2] Analyzing sentinel_corporation.db...")
if Path("sentinel_corporation.db").exists():
    tables2, info2 = get_database_info("sentinel_corporation.db")
    print(f"    Tables found: {len(tables2)}")
    for table in tables2:
        print(f"      - {table}: {info2[table]['row_count']} rows, {len(info2[table]['columns'])} columns")
else:
    print("    FILE NOT FOUND")
    tables2, info2 = [], {}

# Find differences
print("\n[3] Schema Comparison:")
print("-" * 80)

only_in_1 = set(tables1) - set(tables2)
only_in_2 = set(tables2) - set(tables1)
in_both = set(tables1) & set(tables2)

if only_in_1:
    print(f"\n  Tables ONLY in sentinel.db ({len(only_in_1)}):")
    for table in sorted(only_in_1):
        print(f"    - {table}: {info1[table]['row_count']} rows")

if only_in_2:
    print(f"\n  Tables ONLY in sentinel_corporation.db ({len(only_in_2)}):")
    for table in sorted(only_in_2):
        print(f"    - {table}: {info2[table]['row_count']} rows")

if in_both:
    print(f"\n  Tables in BOTH databases ({len(in_both)}):")
    for table in sorted(in_both):
        rows1 = info1[table]['row_count']
        rows2 = info2[table]['row_count']
        if rows1 != rows2:
            print(f"    - {table}: {rows1} rows vs {rows2} rows [DIFFERENT]")
        else:
            print(f"    - {table}: {rows1} rows [SAME]")

print("\n" + "=" * 80)
print("\nRECOMMENDATION:")
if not tables2:
    print("  sentinel_corporation.db is empty or doesn't exist")
    print("  Safe to consolidate into sentinel.db")
elif only_in_2:
    print(f"  Need to migrate {len(only_in_2)} tables from sentinel_corporation.db")
    print("  to sentinel.db before consolidation")
else:
    print("  All tables are in sentinel.db")
    print("  Can safely deprecate sentinel_corporation.db")
print("=" * 80 + "\n")
