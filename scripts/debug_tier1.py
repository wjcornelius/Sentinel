# Debug script for Tier 1 filter

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi
from sentinel.tier1_technical_filter import Tier1TechnicalFilter

api = tradeapi.REST(
    config.APCA_API_KEY_ID,
    config.APCA_API_SECRET_KEY,
    config.APCA_API_BASE_URL,
    api_version='v2'
)

# Test with a single known stock
test_symbol = 'AAPL'

print(f"\nTesting Tier 1 filter with {test_symbol}...")

filter_engine = Tier1TechnicalFilter(api)

# Calculate metrics
print("\nCalculating technical metrics...")
try:
    metrics = filter_engine._calculate_technical_metrics(test_symbol)
except Exception as e:
    print(f"ERROR in metric calculation: {e}")
    import traceback
    traceback.print_exc()
    metrics = None

if metrics:
    print("\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    # Check hard filters
    print("\nChecking hard filters...")
    passes = filter_engine._passes_hard_filters(
        metrics,
        min_dollar_volume=1_000_000,
        min_price=5.0,
        max_price=500.0,
        min_rsi=20.0,
        max_rsi=80.0
    )
    print(f"  Passes hard filters: {passes}")

    if not passes:
        print("\n  Filter failures:")
        if metrics['avg_dollar_volume'] < 1_000_000:
            print(f"    - Volume too low: ${metrics['avg_dollar_volume']/1e6:.1f}M < $1M")
        if metrics['price'] < 5.0:
            print(f"    - Price too low: ${metrics['price']} < $5")
        if metrics['price'] > 500.0:
            print(f"    - Price too high: ${metrics['price']} > $500")
        if metrics['rsi'] is None:
            print(f"    - RSI is None")
        elif metrics['rsi'] < 20.0:
            print(f"    - RSI too low: {metrics['rsi']} < 20")
        elif metrics['rsi'] > 80.0:
            print(f"    - RSI too high: {metrics['rsi']} > 80")
        if metrics['atr_percent'] is None or metrics['atr_percent'] < 1.0:
            print(f"    - ATR too low: {metrics['atr_percent']}% < 1%")

    # Calculate score
    score = filter_engine._calculate_composite_score(metrics)
    print(f"\n  Composite score: {score:.1f}")

else:
    print("ERROR: Could not calculate metrics")
