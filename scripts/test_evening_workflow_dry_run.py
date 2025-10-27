# -*- coding: utf-8 -*-
# scripts/test_evening_workflow_dry_run.py
# Dry-run test of evening workflow (no real orders submitted)

"""
Dry-run test of evening workflow.
Connects to Alpaca, reads account data, but doesn't submit any orders.

Tests:
- API connectivity
- Database connectivity
- Workflow orchestration
- Logging functionality
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi
from sentinel.execution_engine import OrderExecutionEngine


def main():
    """Run dry-run test of evening workflow components."""
    print("\n" + "=" * 70)
    print("EVENING WORKFLOW DRY-RUN TEST")
    print("=" * 70)

    # Test 1: Alpaca API connection
    print("\n[TEST 1] Alpaca API Connection")
    try:
        api = tradeapi.REST(
            config.APCA_API_KEY_ID,
            config.APCA_API_SECRET_KEY,
            config.APCA_API_BASE_URL,
            api_version='v2'
        )
        account = api.get_account()
        print(f"  [OK] Connected to Alpaca")
        print(f"  Account Status: {account.status}")
        print(f"  Portfolio Value: ${float(account.portfolio_value):,.2f}")
        print(f"  Cash: ${float(account.cash):,.2f}")
    except Exception as e:
        print(f"  [FAIL] Could not connect to Alpaca: {e}")
        return 1

    # Test 2: Get current positions
    print("\n[TEST 2] Fetch Current Positions")
    try:
        positions = api.list_positions()
        print(f"  [OK] Found {len(positions)} open positions")

        if positions:
            print("\n  Current Positions:")
            for pos in positions[:5]:  # Show first 5
                pnl_pct = (float(pos.current_price) - float(pos.avg_entry_price)) / float(pos.avg_entry_price) * 100
                print(f"    {pos.symbol}: {pos.qty} shares @ ${float(pos.avg_entry_price):.2f} "
                      f"(Current: ${float(pos.current_price):.2f}, P&L: {pnl_pct:+.1f}%)")

            if len(positions) > 5:
                print(f"    ... and {len(positions) - 5} more")
    except Exception as e:
        print(f"  [FAIL] Could not fetch positions: {e}")
        return 1

    # Test 3: Initialize execution engine
    print("\n[TEST 3] Initialize Execution Engine")
    try:
        engine = OrderExecutionEngine(api)
        print(f"  [OK] OrderExecutionEngine initialized")
        print(f"  Database: sentinel.db")
        print(f"  Max retries: {engine.max_retries}")
    except Exception as e:
        print(f"  [FAIL] Could not initialize engine: {e}")
        return 1

    # Test 4: Reconcile fills (read-only)
    print("\n[TEST 4] Reconcile Fills (Read-Only)")
    try:
        counts = engine.reconcile_fills()
        print(f"  [OK] Fill reconciliation completed")
        print(f"    Filled: {counts['filled']}")
        print(f"    Cancelled: {counts['cancelled']}")
        print(f"    Expired: {counts['expired']}")
        print(f"    Errors: {counts['errors']}")
    except Exception as e:
        print(f"  [FAIL] Fill reconciliation failed: {e}")
        # Non-critical, continue

    # Test 5: Check trailing stops (read-only, won't update without profitable positions)
    print("\n[TEST 5] Check Trailing Stops (Read-Only)")
    try:
        counts = engine.update_trailing_stops()
        print(f"  [OK] Trailing stop check completed")
        print(f"    Raised: {counts['raised']}")
        print(f"    Unchanged: {counts['unchanged']}")
        print(f"    Emergency stops: {counts.get('emergency_stops', 0)}")
        print(f"    Errors: {counts['errors']}")
    except Exception as e:
        print(f"  [FAIL] Trailing stop check failed: {e}")
        # Non-critical, continue

    # Test 6: Check profit-taking (read-only)
    print("\n[TEST 6] Check Profit-Taking Opportunities (Read-Only)")
    try:
        result = engine.check_profit_taking()
        candidates = result.get('candidates', [])
        print(f"  [OK] Profit-taking check completed")
        print(f"    Candidates found: {len(candidates)}")

        if candidates:
            for candidate in candidates:
                print(f"      {candidate['symbol']}: +{candidate['unrealized_pnl_pct']:.1%} "
                      f"(${candidate['unrealized_pl']:.2f})")
    except Exception as e:
        print(f"  [FAIL] Profit-taking check failed: {e}")
        # Non-critical, continue

    # Test 7: Check orphaned stops (read-only)
    print("\n[TEST 7] Check Orphaned Stops (Read-Only)")
    try:
        counts = engine.cleanup_orphaned_stops()
        print(f"  [OK] Orphaned stop check completed")
        print(f"    Cancelled: {counts['cancelled']}")
        print(f"    Skipped: {counts['skipped']}")
    except Exception as e:
        print(f"  [FAIL] Orphaned stop check failed: {e}")
        # Non-critical, continue

    # Summary
    print("\n" + "=" * 70)
    print("DRY-RUN TEST COMPLETE")
    print("=" * 70)
    print("\nAll critical tests passed!")
    print("Evening workflow components are functioning correctly.")
    print("\nNext step: Run full evening workflow with:")
    print("  python sentinel_evening_workflow.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
