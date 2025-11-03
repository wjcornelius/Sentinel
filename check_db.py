import sqlite3

conn = sqlite3.connect('sentinel.db')
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='market_data_cache'")
result = cursor.fetchone()
print(f"Table exists: {result is not None}")

if result:
    cursor.execute("PRAGMA table_info(market_data_cache)")
    print("\nSchema:")
    for row in cursor.fetchall():
        print(f"  {row}")

    cursor.execute("SELECT COUNT(*) FROM market_data_cache")
    count = cursor.fetchone()[0]
    print(f"\nTotal entries: {count}")

    cursor.execute("SELECT ticker, data_type, fetched_at FROM market_data_cache LIMIT 10")
    print("\nFirst 10 entries:")
    for row in cursor.fetchall():
        print(f"  {row}")

conn.close()
