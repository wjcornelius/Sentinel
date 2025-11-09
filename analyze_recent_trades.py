"""Analyze most recent trading plan to identify improvement areas"""
import json
from pathlib import Path

# Load most recent trading plan
trade_file = Path(__file__).parent / "proposed_trades_2025-11-07.json"
with open(trade_file, 'r') as f:
    data = json.load(f)

print("=" * 80)
print("MOST RECENT TRADING PLAN ANALYSIS (November 7, 2025)")
print("=" * 80)

# BUY analysis
buys = data.get("approved_buys", [])
sells = data.get("approved_sells", [])

print(f"\nTotal approved BUY orders: {len(buys)}")
print(f"Total approved SELL orders: {len(sells)}")

# Capital deployment
total_allocated = sum([b.get("allocated_capital", 0) for b in buys])
print(f"\nTotal capital allocated: ${total_allocated:,.0f}")
if buys:
    avg_allocation = total_allocated / len(buys)
    print(f"Average position size: ${avg_allocation:,.0f}")

# Top allocations
print("\nTop 5 BUY allocations:")
sorted_buys = sorted(buys, key=lambda x: -x.get("allocated_capital", 0))
for i, b in enumerate(sorted_buys[:5], 1):
    print(f"  {i}. {b['ticker']:6s}: ${b['allocated_capital']:>8,.0f} ({b.get('allocation_pct', 0):4.1f}%)")

# Smallest allocations
print("\nSmallest 5 BUY allocations:")
for i, b in enumerate(sorted_buys[-5:], 1):
    print(f"  {i}. {b['ticker']:6s}: ${b['allocated_capital']:>8,.0f} ({b.get('allocation_pct', 0):4.1f}%)")

# SELL analysis
if sells:
    print(f"\nSELL orders ({len(sells)} total):")
    for s in sells:
        ticker = s.get("ticker", "?")
        pct = s.get("sell_pct", 100)
        reason = s.get("reasoning", "No reason provided")[:60]
        print(f"  {ticker:6s}: {pct:3.0f}% - {reason}...")
else:
    print("\nNo SELL orders (no positions closed)")

# Score distribution
print("\nScore distribution of BUY candidates:")
scores = [b.get("composite_score", 0) for b in buys if "composite_score" in b]
if scores:
    print(f"  Average score: {sum(scores)/len(scores):.1f}")
    print(f"  Highest score: {max(scores):.1f}")
    print(f"  Lowest score:  {min(scores):.1f}")

# Check for quality issues
print("\n" + "=" * 80)
print("POTENTIAL ISSUES")
print("=" * 80)

# Issue 1: Position count
if len(buys) < 15:
    print(f"\n⚠ Only {len(buys)} positions - target is 15-20 for diversification")

# Issue 2: Capital deployment
deployment_pct = (total_allocated / 100000) * 100  # Assuming $100K capital
if deployment_pct < 90:
    print(f"\n⚠ Only {deployment_pct:.1f}% capital deployed - target is 90-100%")

# Issue 3: Oversized positions
oversized = [b for b in buys if b.get("allocation_pct", 0) > 10]
if oversized:
    print(f"\n⚠ {len(oversized)} positions exceed 10% limit:")
    for b in oversized:
        print(f"  {b['ticker']}: {b['allocation_pct']:.1f}%")

# Issue 4: Undersized positions
undersized = [b for b in buys if b.get("allocated_capital", 0) < 3000]
if undersized:
    print(f"\n⚠ {len(undersized)} positions under $3K (may not be worth the trade costs):")
    for b in undersized:
        print(f"  {b['ticker']}: ${b['allocated_capital']:,.0f}")

print("\n" + "=" * 80)
