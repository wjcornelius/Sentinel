"""Test cache with fix"""
from Departments.Research import ResearchDepartment
import sqlite3

research = ResearchDepartment()
data = research._get_cached_price_data('AAPL')

if data is not None:
    print(f"SUCCESS: Got {len(data)} rows")
else:
    print("FAILED: data is None")

conn = sqlite3.connect('sentinel.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM market_data_cache WHERE ticker='AAPL'")
count = cursor.fetchone()[0]
print(f"Cache entries: {count}")
conn.close()
