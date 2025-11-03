"""
Test CEO Trading Plan Generation
Quick test to see if existing CEO system works
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("TESTING CEO TRADING PLAN GENERATION")
print("=" * 80)
print()

# Import CEO
from Departments.Executive import CEO

# Initialize CEO
print("Initializing CEO...")
ceo = CEO()
print()

# Request trading plan
print("Requesting trading plan from CEO...")
print("-" * 80)
result = ceo.request_trading_plan()
print("-" * 80)
print()

# Display result
print("RESULT:")
print(f"Success: {result.get('success', False)}")
print(f"Status: {result.get('status', 'UNKNOWN')}")
print(f"Message: {result.get('message', 'No message')}")
print()

if result.get('plan'):
    plan = result['plan']
    print("PLAN SUMMARY:")
    if 'summary' in plan:
        for key, value in plan['summary'].items():
            print(f"  {key}: {value}")
    print()

    if 'trades' in plan and len(plan['trades']) > 0:
        print(f"TRADES: {len(plan['trades'])} total")
        for i, trade in enumerate(plan['trades'][:5], 1):
            print(f"  {i}. {trade.get('ticker', '?')} - {trade.get('shares', 0)} shares @ ${trade.get('price', 0):.2f}")
        if len(plan['trades']) > 5:
            print(f"  ... and {len(plan['trades']) - 5} more")
    else:
        print("  No trades in plan")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
