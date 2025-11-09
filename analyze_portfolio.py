import re
import glob
import os
from datetime import datetime

# Find all research messages from this week
research_path = r'C:\Users\wjcor\OneDrive\Desktop\Sentinel\Messages_Between_Departments\Outbox\RESEARCH'
files = glob.glob(os.path.join(research_path, 'MSG_RESEARCH_202511*.md'))

portfolio_data = []

for file in sorted(files):
    filename = os.path.basename(file)
    # Extract timestamp from filename
    match = re.search(r'MSG_RESEARCH_(\d{8})T(\d{6})Z', filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        time = datetime.strptime(time_str, '%H%M%S').strftime('%H:%M:%S')

        with open(file, 'r') as f:
            content = f.read()

            # Find all market_value entries (these are holdings)
            market_values = re.findall(r'"market_value": ([\d.]+)', content)

            # Find SPY change
            spy_match = re.search(r'"spy_change_pct": ([-\d.]+)', content)
            spy_change = float(spy_match.group(1)) if spy_match else None

            if market_values:
                total = sum(float(v) for v in market_values)
                portfolio_data.append({
                    'date': date,
                    'time': time,
                    'portfolio_value': total,
                    'holdings_count': len(market_values),
                    'spy_change_pct': spy_change,
                    'file': filename
                })

# Print results
print("SENTINEL PORTFOLIO PERFORMANCE - WEEK OF NOV 4-5, 2025")
print("=" * 80)
print()

for i, data in enumerate(portfolio_data):
    print(f"{data['date']} {data['time']} - Holdings: {data['holdings_count']}")
    print(f"  Portfolio Value: ${data['portfolio_value']:,.2f}")
    if data['spy_change_pct'] is not None:
        print(f"  SPY Daily Change: {data['spy_change_pct']:.2f}%")
    print()

# Calculate performance if we have multiple data points
if len(portfolio_data) >= 2:
    print("\nPERFORMANCE COMPARISON:")
    print("-" * 80)

    # Use first and last values
    first = portfolio_data[0]
    last = portfolio_data[-1]

    portfolio_change = ((last['portfolio_value'] - first['portfolio_value']) / first['portfolio_value']) * 100

    print(f"\nSentinel Portfolio:")
    print(f"  Start: ${first['portfolio_value']:,.2f} ({first['date']})")
    print(f"  End:   ${last['portfolio_value']:,.2f} ({last['date']})")
    print(f"  Change: {portfolio_change:+.2f}%")

    print(f"\nMarket Indices (from screenshots):")
    print(f"  S&P 500: -0.94% (past 5 days)")
    print(f"  Nasdaq 100: -1.29% (past 5 days)")

    print(f"\nRelative Performance:")
    if portfolio_change > -0.94:
        print(f"  [BETTER] Outperformed S&P 500 by {portfolio_change - (-0.94):.2f} percentage points")
    else:
        print(f"  [WORSE] Underperformed S&P 500 by {(-0.94) - portfolio_change:.2f} percentage points")

    if portfolio_change > -1.29:
        print(f"  [BETTER] Outperformed Nasdaq 100 by {portfolio_change - (-1.29):.2f} percentage points")
    else:
        print(f"  [WORSE] Underperformed Nasdaq 100 by {(-1.29) - portfolio_change:.2f} percentage points")
