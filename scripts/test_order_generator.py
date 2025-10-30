# -*- coding: utf-8 -*-
# scripts/test_order_generator.py
# Test order generation from conviction analysis results

"""
Test Order Generator

Tests the order generation module with sample conviction results.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi
from sentinel.order_generator import generate_entry_orders


def main():
    """Test order generator with sample conviction results."""

    print("\n" + "=" * 70)
    print("ORDER GENERATOR TEST")
    print("=" * 70)

    # Connect to Alpaca
    api = tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

    # Get current portfolio value
    account = api.get_account()
    portfolio_value = float(account.portfolio_value)
    print(f"\nPortfolio Value: ${portfolio_value:,.2f}")

    # Sample conviction results (simulating Tier 3 output)
    conviction_results = [
        {
            'symbol': 'AMD',
            'decision': 'BUY',
            'conviction_score': 9,
            'latest_price': 258.15,
            'rationale': 'Strong price momentum with significant gains',
            'sector': 'Technology'
        },
        {
            'symbol': 'DHR',
            'decision': 'BUY',
            'conviction_score': 8,
            'latest_price': 221.14,
            'rationale': 'Strong recent performance with 18.9% gain',
            'sector': 'Healthcare'
        },
        {
            'symbol': 'NVDA',
            'decision': 'BUY',
            'conviction_score': 7,
            'latest_price': 190.49,
            'rationale': 'Positive momentum and strong fundamentals',
            'sector': 'Technology'
        },
        {
            'symbol': 'AAPL',
            'decision': 'BUY',
            'conviction_score': 6,
            'latest_price': 267.22,
            'rationale': 'Solid performance with moderate momentum',
            'sector': 'Technology'
        },
        {
            'symbol': 'MU',
            'decision': 'HOLD',
            'conviction_score': 5,
            'latest_price': 219.00,
            'rationale': 'Mixed signals, maintaining position',
            'sector': 'Technology'
        }
    ]

    print(f"\nConviction Results: {len(conviction_results)} total")
    buys = [r for r in conviction_results if r['decision'] == 'BUY']
    print(f"  BUY signals: {len(buys)}")
    print(f"  HOLD signals: {len(conviction_results) - len(buys)}")

    # Get current positions
    positions = api.list_positions()
    current_positions = {p.symbol: p for p in positions}

    # Generate orders
    print("\n" + "=" * 70)
    print("GENERATING ORDERS")
    print("=" * 70)

    result = generate_entry_orders(
        api=api,
        conviction_results=conviction_results,
        portfolio_value=portfolio_value,
        current_positions=current_positions
    )

    orders = result['orders']
    allocation_summary = result['allocation_summary']
    notes = result['notes']

    # Display allocation summary
    print("\nAllocation Summary:")
    print(f"  Total Capital:      ${allocation_summary['total_capital']:,.2f}")
    print(f"  Investable (90%):   ${allocation_summary['investable_capital']:,.2f}")
    print(f"  Allocated:          ${allocation_summary['allocated']:,.2f}")
    print(f"  Cash Remaining:     ${allocation_summary['cash_remaining']:,.2f}")
    print(f"  Allocation %:       {allocation_summary['allocation_pct']:.1f}%")

    # Display generated orders
    print("\n" + "=" * 70)
    print(f"GENERATED ORDERS: {len(orders)} entry+stop pairs")
    print("=" * 70)

    if orders:
        print(f"\n{'Symbol':<8} {'Conv':<6} {'Qty':<8} {'Entry':<10} {'Stop':<10} {'Value':<12} {'Risk %':<8}")
        print("-" * 70)

        for order in orders:
            symbol = order['symbol']
            conv = order['conviction_score']
            qty = order['qty']
            entry = order['entry_price']
            stop = order['stop_price']
            value = order['allocation']
            risk_pct = ((entry - stop) / entry * 100)

            print(
                f"{symbol:<8} "
                f"{conv:<6} "
                f"{qty:<8} "
                f"${entry:<9.2f} "
                f"${stop:<9.2f} "
                f"${value:<11.2f} "
                f"{risk_pct:<7.1f}%"
            )

        print("\nRationales:")
        for order in orders:
            print(f"\n  {order['symbol']}: {order['rationale']}")

    else:
        print("\nNo orders generated")

    # Display notes
    if notes:
        print("\n" + "=" * 70)
        print("ALLOCATION NOTES")
        print("=" * 70)
        for note in notes:
            print(f"  - {note}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
