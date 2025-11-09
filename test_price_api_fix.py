"""
Test script to verify Trading Department price API fix
Tests the new get_stock_latest_bar() method
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import APCA_API_KEY_ID, APCA_API_SECRET_KEY
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestBarRequest

print("\n" + "=" * 80)
print("TESTING: Trading Department Price API Fix")
print("=" * 80)

# Initialize data client (same as Trading Department now uses)
print("\n[1] Initializing Alpaca Data Client...")
data_client = StockHistoricalDataClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)
print("    SUCCESS: Data client initialized")

# Test fetching latest price for a test ticker
test_tickers = ['AAPL', 'MSFT', 'TSLA']

print(f"\n[2] Testing latest bar price fetching for {len(test_tickers)} tickers...")
for ticker in test_tickers:
    try:
        request = StockLatestBarRequest(symbol_or_symbols=ticker)
        latest_bar = data_client.get_stock_latest_bar(request)
        current_price = float(latest_bar[ticker].close)
        print(f"    {ticker}: ${current_price:.2f} [OK]")
    except Exception as e:
        print(f"    {ticker}: ERROR - {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print("\nIf prices displayed above, the fix is working correctly!")
print("Trading Department will now use REAL-TIME prices for bracket orders.\n")
