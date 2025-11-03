"""Debug cache test"""
import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

from Departments.Research import ResearchDepartment

print("Testing Research Department caching with DEBUG logging...")

# Initialize
research = ResearchDepartment(db_path="sentinel.db")

# Fetch AAPL data
print("\nFetching AAPL data...")
try:
    data = research._get_cached_price_data('AAPL')

    if data is not None:
        print(f"SUCCESS: Got data: {len(data)} rows")
        print(f"  Latest close: ${data['Close'].iloc[-1]:.2f}")
    else:
        print("FAILED: data is None")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check cache
import sqlite3
conn = sqlite3.connect('sentinel.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM market_data_cache WHERE ticker='AAPL'")
count = cursor.fetchone()[0]
print(f"\nCache entries for AAPL: {count}")
conn.close()

print("\nDone!")
