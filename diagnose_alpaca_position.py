"""
Diagnostic Script: Alpaca Position Object Attributes
=====================================================

Purpose: Inspect what attributes are actually available on Alpaca Position objects
         to determine which field contains the entry date/time.

This will help us fix the "999 days held" issue.
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

import config
from alpaca.trading.client import TradingClient

print("=" * 80)
print("ALPACA POSITION OBJECT DIAGNOSTIC")
print("=" * 80)
print()

try:
    # Initialize Alpaca client
    print("Connecting to Alpaca...")
    trading_client = TradingClient(
        api_key=config.APCA_API_KEY_ID,
        secret_key=config.APCA_API_SECRET_KEY,
        paper=True
    )

    # Get positions
    print("Fetching current positions...")
    positions = trading_client.get_all_positions()

    if not positions:
        print("  No positions found in account")
        print()
        print("SUGGESTION: Open a position first, then run this script again")
        sys.exit(0)

    print(f"  Found {len(positions)} position(s)")
    print()

    # Inspect first position
    pos = positions[0]

    print("=" * 80)
    print(f"POSITION: {pos.symbol}")
    print("=" * 80)
    print()

    print("All Attributes:")
    print("-" * 80)
    all_attrs = dir(pos)
    for attr in sorted(all_attrs):
        if not attr.startswith('_'):  # Skip private attributes
            try:
                value = getattr(pos, attr)
                # Skip methods
                if callable(value):
                    continue
                print(f"  {attr:25s} = {value}")
            except:
                print(f"  {attr:25s} = <error accessing>")

    print()
    print("=" * 80)
    print("DATE-RELATED ATTRIBUTES:")
    print("=" * 80)
    print()

    # Check for date-related attributes
    date_attrs = ['created_at', 'entry_time', 'opened_at', 'purchase_date',
                  'filled_at', 'timestamp', 'date', 'entry_date', 'open_date']

    found_dates = []
    for attr in date_attrs:
        if hasattr(pos, attr):
            value = getattr(pos, attr)
            if value:
                print(f"  ✓ {attr:25s} = {value}")
                found_dates.append(attr)
            else:
                print(f"  ✗ {attr:25s} = None")
        else:
            print(f"  ✗ {attr:25s} = <not found>")

    print()

    if found_dates:
        print(f"RESULT: Found {len(found_dates)} date attribute(s): {', '.join(found_dates)}")
        print()
        print("RECOMMENDATION: Update research_department.py to use this attribute")
    else:
        print("RESULT: No date attributes found")
        print()
        print("EXPLANATION: Alpaca Position objects may not store entry date directly")
        print("WORKAROUND: Query order history for each position to get fill date")

    print()
    print("=" * 80)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
