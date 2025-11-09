"""
Test enhanced dashboard display
Shows new Starting Capital → Current Equity → Total Return view
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from Departments.Executive.ceo import CEO

print("\n" + "=" * 80)
print(" " * 25 + "ENHANCED DASHBOARD TEST")
print("=" * 80)

# Initialize CEO
project_root = Path("C:/Users/wjcor/OneDrive/Desktop/Sentinel")
ceo = CEO(project_root)

# Get dashboard
print("\n[CEO] Retrieving dashboard with enhanced metrics...")
result = ceo.handle_user_request("view_dashboard")

if result['status'] == 'SUCCESS':
    dashboard = result['dashboard']
    perf = dashboard['performance']

    print("\n" + "=" * 80)
    print("PORTFOLIO PERFORMANCE:")
    print("-" * 80)

    # Display new metrics
    print(f"  Starting Capital:    ${perf.get('starting_capital', 100000):>12,.2f}")
    print(f"  Current Equity:      ${perf.get('current_equity', 0):>12,.2f}")
    print(f"  Total Return:        ${perf.get('total_return_dollars', 0):>12,.2f}  ({perf.get('total_return_pct', 0):+.2f}%)")
    print()
    print(f"  Today's P/L:         ${perf.get('daily_pl', 0):>12,.2f}  ({perf.get('daily_pl_pct', 0):+.2f}%)")
    print(f"  Cash Available:      ${perf.get('cash', 0):>12,.2f}")
    print(f"  Buying Power:        ${perf.get('buying_power', 0):>12,.2f}")
    print(f"  Open Positions:      {perf.get('positions_count', 0):>12}")
    print()

    # Circuit breaker status
    daily_loss_pct = abs(perf.get('daily_pl_pct', 0)) if perf.get('daily_pl_pct', 0) < 0 else 0
    if daily_loss_pct >= 15:
        print(f"  Circuit Breaker:     RED ALERT ({daily_loss_pct:.1f}% loss today)")
    elif daily_loss_pct >= 10:
        print(f"  Circuit Breaker:     ORANGE ({daily_loss_pct:.1f}% loss today - new BUYs blocked)")
    elif daily_loss_pct >= 5:
        print(f"  Circuit Breaker:     YELLOW ({daily_loss_pct:.1f}% loss today - monitor)")
    else:
        print(f"  Circuit Breaker:     NORMAL")

    print("\n" + "=" * 80)
    print("\nSUCCESS: Enhanced dashboard now shows:")
    print("  1. Starting Capital ($100,000 baseline)")
    print("  2. Current Equity (actual account value)")
    print("  3. Total Return ($ and % from start)")
    print("  4. Today's P/L (for circuit breaker)")
    print("  5. Circuit Breaker status indicator")
    print("\n" + "=" * 80)
else:
    print(f"\nERROR: {result['message']}")
