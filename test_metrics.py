"""Quick test to check performance metrics"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from Departments.Executive.executive_department import ExecutiveDepartment

project_root = Path(__file__).parent
executive = ExecutiveDepartment(
    db_path=project_root / 'sentinel.db',
    messages_dir=project_root / 'Messages',
    reports_dir=project_root / 'Reports'
)

print("Fetching dashboard data...")
data = executive.get_realtime_dashboard_data()
perf = data['performance']

print("\n" + "=" * 60)
print("PERFORMANCE METRICS")
print("=" * 60)
print(f"Daily P&L:     ${perf['daily_pnl']:,.2f}")
print(f"Daily P&L %:   {perf['daily_pnl_pct']:+.2f}%")
print(f"Realized:      ${perf['realized_pnl']:,.2f}")
print(f"Unrealized:    ${perf['unrealized_pnl']:,.2f}")
print(f"Sharpe Ratio:  {perf['sharpe_ratio_30d']:.3f}")
print(f"Win Rate:      {perf['win_rate_30d']:.1f}%")
print(f"Alpha vs SPY:  {perf['alpha_vs_spy']:+.2f}%")
print(f"Max Drawdown:  {perf['max_drawdown']:.2f}%")
print("=" * 60)

print("\nOPEN POSITIONS:")
for pos in data['open_positions'][:3]:
    print(f"  {pos['ticker']}: {pos['shares']} shares @ ${pos['entry_price']:.2f}")
