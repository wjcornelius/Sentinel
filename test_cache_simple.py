"""Simple cache test"""
import yfinance as yf
import pandas as pd
from Departments.Research import ResearchDepartment

print("Testing Research Department caching...")

# Initialize
research = ResearchDepartment(db_path="sentinel.db")

# Fetch AAPL data
print("\nFetching AAPL data...")
data = research._get_cached_price_data('AAPL')

if data is not None:
    print(f"✓ Got data: {len(data)} rows")
    print(f"  Latest close: ${data['Close'].iloc[-1]:.2f}")
else:
    print("✗ Failed to get data")

# Check cache
import sqlite3
conn = sqlite3.connect('sentinel.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM market_data_cache WHERE ticker='AAPL'")
count = cursor.fetchone()[0]
print(f"\nCache entries for AAPL: {count}")
conn.close()

print("\nDone!")
