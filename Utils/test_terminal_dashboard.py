"""
Test script for Terminal Dashboard - Week 7 Day 2
Verifies dashboard functionality and generates a static snapshot
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Utils.terminal_dashboard import TerminalDashboard
from rich.console import Console

def test_dashboard_components():
    """Test all dashboard components individually"""
    print("=" * 80)
    print("TERMINAL DASHBOARD COMPONENT TESTS")
    print("=" * 80)

    # Initialize dashboard
    print("\n[TEST 1] Initializing Dashboard...")
    dashboard = TerminalDashboard(refresh_interval=5)
    print(f"[OK] Dashboard initialized: refresh={dashboard.refresh_interval}s")

    # Test header
    print("\n[TEST 2] Creating Header Panel...")
    header = dashboard.create_header()
    print("[OK] Header panel created")

    # Test fetching data
    print("\n[TEST 3] Fetching Real-Time Data...")
    try:
        data = dashboard.executive.get_realtime_dashboard_data()
        print(f"[OK] Data fetched successfully")
        print(f"   - Open positions: {len(data.get('open_positions', []))}")
        print(f"   - Daily P&L: ${data['performance']['daily_pnl']:,.2f}")
        print(f"   - Sharpe Ratio: {data['performance']['sharpe_ratio_30d']:.3f}")
        print(f"   - Win Rate: {data['performance']['win_rate_30d']:.1f}%")
    except Exception as e:
        print(f"[FAIL] Failed to fetch data: {e}")
        return False

    # Test performance panel
    print("\n[TEST 4] Creating Performance Panel...")
    perf_panel = dashboard.create_performance_panel(data)
    print("[OK] Performance panel created")

    # Test positions table
    print("\n[TEST 5] Creating Positions Table...")
    positions_panel = dashboard.create_positions_table(data.get('open_positions', []))
    print(f"[OK] Positions table created with {len(data.get('open_positions', []))} positions")

    # Test system health panel
    print("\n[TEST 6] Creating System Health Panel...")
    health_panel = dashboard.create_system_health_panel(data.get('system_health', {}))
    print("[OK] System health panel created")

    # Test footer
    print("\n[TEST 7] Creating Footer Panel...")
    footer = dashboard.create_footer()
    print("[OK] Footer panel created")

    # Test full layout generation
    print("\n[TEST 8] Generating Complete Layout...")
    try:
        layout = dashboard.generate_layout()
        print("[OK] Complete layout generated")
    except Exception as e:
        print(f"[FAIL] Failed to generate layout: {e}")
        return False

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED [OK]")
    print("=" * 80)

    return True


def generate_static_snapshot():
    """Generate a static snapshot of the dashboard"""
    print("\n\nGenerating static dashboard snapshot...")
    print("-" * 80)

    dashboard = TerminalDashboard(refresh_interval=5)
    console = Console()

    # Generate and print the layout
    layout = dashboard.generate_layout()
    console.print(layout)

    print("-" * 80)
    print("Snapshot complete!")


if __name__ == "__main__":
    # Run component tests
    success = test_dashboard_components()

    if success:
        # Generate static snapshot
        generate_static_snapshot()

        print("\n" + "=" * 80)
        print("DASHBOARD READY FOR USE!")
        print("=" * 80)
        print("\nTo run the live dashboard:")
        print("  python Utils/terminal_dashboard.py")
        print("\nOptions:")
        print("  --db <path>        Path to database (default: sentinel.db)")
        print("  --refresh <secs>   Refresh interval in seconds (default: 5)")
        print("\nExample:")
        print("  python Utils/terminal_dashboard.py --refresh 3")
        print("=" * 80)
    else:
        print("\n[FAIL] Dashboard tests failed!")
        sys.exit(1)
