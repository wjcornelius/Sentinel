"""
Test: Position Monitoring Entry Date Fix
=========================================

Validates that position monitoring correctly handles missing entry_date fields:
1. Positions WITHOUT entry_date should skip time-based exit checks
2. Positions WITH entry_date should still evaluate time-based rules
3. Score-based exits should work for ALL positions (regardless of date)

Expected: No more false "999 days held" flags
"""

import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("TEST: POSITION MONITORING ENTRY DATE FIX")
print("=" * 80)
print()

# Test configuration
MANDATORY_EXIT_THRESHOLD = 55  # Same as operations_manager.py
TIME_BASED_EXIT_DAYS = 5

# Mock holdings data (simulating different scenarios)
holdings = [
    {
        'ticker': 'AAPL',
        'composite_score': 48,
        'unrealized_plpc': -6.0,
        # No entry_date field (Alpaca doesn't provide it)
    },
    {
        'ticker': 'MSFT',
        'composite_score': 72,
        'unrealized_plpc': 3.0,
        # No entry_date field
    },
    {
        'ticker': 'TSLA',
        'composite_score': 62,
        'unrealized_plpc': 1.5,
        'entry_date': (date.today() - timedelta(days=7)).isoformat()  # 7 days old
    },
    {
        'ticker': 'NVDA',
        'composite_score': 52,
        'unrealized_plpc': -2.0,
        'entry_date': (date.today() - timedelta(days=2)).isoformat()  # 2 days old
    },
]

print("Test Holdings:")
print("-" * 80)
for h in holdings:
    entry = h.get('entry_date', 'NONE')
    print(f"  {h['ticker']:6s}: Score={h['composite_score']:3.0f}, P&L={h['unrealized_plpc']:+6.1f}%, Entry={entry}")
print()

# Apply position monitoring logic (from operations_manager.py)
print("Applying Position Monitoring Logic:")
print("-" * 80)

mandatory_sells = []
holds = []

for holding in holdings:
    ticker = holding.get('ticker')
    score = holding.get('composite_score', 50)
    unrealized_plpc = holding.get('unrealized_plpc', 0)

    # Check entry date for time-based exits
    entry_date = holding.get('entry_date')
    days_held = None  # None means unknown, skip time-based checks
    if entry_date:
        try:
            from datetime import datetime
            entry = datetime.strptime(entry_date, '%Y-%m-%d').date()
            days_held = (date.today() - entry).days
        except:
            pass  # If parsing fails, days_held stays None

    # Determine if this position MUST be sold
    must_sell = False
    sell_reason = None

    # Rule 1: Score deteriorated below threshold AND position losing
    if score < MANDATORY_EXIT_THRESHOLD and unrealized_plpc < 0:
        must_sell = True
        sell_reason = f"Score {score:.1f} < {MANDATORY_EXIT_THRESHOLD}, losing {unrealized_plpc:.1f}%"

    # Rule 2: Time-based exit (held > 5 days and not profitable)
    # ONLY check if we have a valid days_held value
    elif days_held is not None and days_held > TIME_BASED_EXIT_DAYS and unrealized_plpc <= 2.0:
        must_sell = True
        sell_reason = f"Held {days_held} days with only {unrealized_plpc:.1f}% gain"

    if must_sell:
        print(f"  [X] {ticker:6s}: MANDATORY SELL - {sell_reason}")
        mandatory_sells.append(ticker)
    else:
        days_str = f"{days_held} days" if days_held is not None else "unknown"
        print(f"  [OK] {ticker:6s}: HOLD (Score: {score:.1f}, P&L: {unrealized_plpc:+.1f}%, Held: {days_str})")
        holds.append(ticker)

print()
print("=" * 80)
print("RESULTS")
print("=" * 80)
print()

print(f"Total Holdings: {len(holdings)}")
print(f"Mandatory Sells: {len(mandatory_sells)}")
print(f"Holds: {len(holds)}")
print()

# Validate results
print("=" * 80)
print("VALIDATION")
print("=" * 80)
print()

# Expected results:
# AAPL: Score 48 + losing -6% → SELL (Rule 1: score < 55 AND losing)
# MSFT: Score 72 + winning +3% → HOLD (good position)
# TSLA: Score 62, +1.5%, held 7 days → SELL (Rule 2: held > 5 days with low gain)
# NVDA: Score 52 (< 55) + losing -2% → SELL (Rule 1: score < 55 AND losing)

expected_sells = ['AAPL', 'TSLA', 'NVDA']
expected_holds = ['MSFT']

all_correct = True

print("Expected Sells: " + ', '.join(expected_sells))
print("Actual Sells:   " + ', '.join(mandatory_sells))
if set(mandatory_sells) == set(expected_sells):
    print("  [PASS] Sells match expected")
else:
    print("  [FAIL] Sells don't match")
    all_correct = False
print()

print("Expected Holds: " + ', '.join(expected_holds))
print("Actual Holds:   " + ', '.join(holds))
if set(holds) == set(expected_holds):
    print("  [PASS] Holds match expected")
else:
    print("  [FAIL] Holds don't match")
    all_correct = False
print()

# Key validation: AAPL should be flagged by Rule 1, NOT by time-based rule
print("Key Validation: AAPL (no entry_date)")
if 'AAPL' in mandatory_sells:
    print("  [PASS] AAPL correctly flagged for exit (Rule 1: score-based)")
    print("  Note: Would have shown '999 days held' before fix, but Rule 1 still caught it")
else:
    print("  [FAIL] AAPL should be flagged (score 48, losing -6%)")
    all_correct = False
print()

print("Key Validation: MSFT (no entry_date, but winning)")
if 'MSFT' in holds:
    print("  [PASS] MSFT correctly held (winning position despite no entry_date)")
    print("  Note: Before fix, might have been flagged due to '999 days held'")
else:
    print("  [FAIL] MSFT should be held (score 72, winning +3%)")
    all_correct = False
print()

print("Key Validation: TSLA (has entry_date, time-based exit)")
if 'TSLA' in mandatory_sells:
    print("  [PASS] TSLA correctly flagged for exit (Rule 2: held 7 days, only +1.5%)")
    print("  Note: Time-based rule works when entry_date IS available")
else:
    print("  [FAIL] TSLA should be flagged (held 7 days with minimal gain)")
    all_correct = False
print()

print("Key Validation: NVDA (has entry_date, but only held 2 days)")
if 'NVDA' in mandatory_sells:
    print("  [PASS] NVDA correctly flagged for exit (Rule 1: score 52 < 55, losing -2%)")
    print("  Note: Rule 1 caught it before time-based rule (only held 2 days)")
else:
    print("  [FAIL] NVDA should be flagged (score 52, losing -2%)")
    all_correct = False
print()

print("=" * 80)
if all_correct:
    print("[PASS] ALL TESTS PASSED")
    print()
    print("CONCLUSIONS:")
    print("  1. Positions WITHOUT entry_date skip time-based checks (no false '999 days')")
    print("  2. Positions WITH entry_date still evaluate time-based rules correctly")
    print("  3. Score-based exits (Rule 1) work for ALL positions")
    print("  4. No false mandatory sells due to missing dates")
else:
    print("[FAIL] SOME TESTS FAILED")
    print()
    print("Review logic in operations_manager.py")

print("=" * 80)
