"""
Quick performance analysis of Sentinel's current state
Identifies areas for profitability improvements
"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "sentinel.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=" * 80)
print("SENTINEL PERFORMANCE ANALYSIS")
print("=" * 80)

# Current positions
cur.execute("SELECT COUNT(*) FROM positions WHERE qty > 0")
open_positions = cur.fetchone()[0]
print(f"\nOpen Positions: {open_positions}")

# Position performance
cur.execute("""
    SELECT
        AVG(unrealized_plpc) as avg_return,
        MIN(unrealized_plpc) as worst,
        MAX(unrealized_plpc) as best,
        SUM(CASE WHEN unrealized_plpc > 0 THEN 1 ELSE 0 END) as winners,
        SUM(CASE WHEN unrealized_plpc < 0 THEN 1 ELSE 0 END) as losers
    FROM positions
    WHERE qty > 0
""")
avg, worst, best, winners, losers = cur.fetchone()
if avg is not None:
    print(f"\nPosition Performance:")
    print(f"  Average Return: {avg:.2f}%")
    print(f"  Best Position:  {best:.2f}%")
    print(f"  Worst Position: {worst:.2f}%")
    print(f"  Win Rate: {winners}/{open_positions} ({winners/open_positions*100:.1f}%)")

# Top 5 winners
print("\nTop 5 Winners:")
cur.execute("""
    SELECT symbol, unrealized_plpc, market_value
    FROM positions
    WHERE qty > 0
    ORDER BY unrealized_plpc DESC
    LIMIT 5
""")
for symbol, ret, value in cur.fetchall():
    print(f"  {symbol:6s}: +{ret:6.2f}% (${value:,.0f})")

# Top 5 losers
print("\nTop 5 Losers:")
cur.execute("""
    SELECT symbol, unrealized_plpc, market_value
    FROM positions
    WHERE qty > 0
    ORDER BY unrealized_plpc ASC
    LIMIT 5
""")
for symbol, ret, value in cur.fetchall():
    print(f"  {symbol:6s}: {ret:6.2f}% (${value:,.0f})")

# Market regime history
print("\n" + "=" * 80)
print("MARKET REGIME HISTORY (Last 5 assessments)")
print("=" * 80)
cur.execute("""
    SELECT assessed_at, regime, spy_trend, vix_level
    FROM market_regime_assessments
    ORDER BY assessed_at DESC
    LIMIT 5
""")
for assessed, regime, spy, vix in cur.fetchall():
    print(f"  {assessed}: {regime:8s} (SPY: {spy:8s}, VIX: {vix})")

# Portfolio snapshots
print("\n" + "=" * 80)
print("PORTFOLIO VALUE HISTORY (Last 7 days)")
print("=" * 80)
cur.execute("""
    SELECT snapshot_date, portfolio_value, cash, equity, position_count
    FROM portfolio_snapshots
    ORDER BY snapshot_date DESC
    LIMIT 7
""")
for date, pv, cash, equity, positions in cur.fetchall():
    print(f"  {date}: ${equity:>10,.2f} equity | {positions} positions | ${cash:>10,.2f} cash")

conn.close()

print("\n" + "=" * 80)
print("Analysis complete")
print("=" * 80)
