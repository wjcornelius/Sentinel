#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify holdings data flows correctly through the pipeline.
This tests the fix for LIQUIDATE orders showing $0.
"""

import sys
import json
from pathlib import Path

# Set encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from Departments.Research.research_department import ResearchDepartment
from Departments.Executive.gpt5_portfolio_optimizer import GPT5PortfolioOptimizer

def main():
    print("=" * 80)
    print("TESTING HOLDINGS DATA FIX")
    print("=" * 80)
    print()

    # Initialize Research Department
    print("[1/4] Initializing Research Department...")
    db_path = project_root / "sentinel.db"
    research = ResearchDepartment(db_path=str(db_path))
    print("✓ Research Department initialized")
    print()

    # Get current holdings from Alpaca
    print("[2/4] Fetching holdings from Alpaca...")
    holdings = research._get_current_holdings()
    print(f"✓ Found {len(holdings)} positions")

    if holdings:
        print("\nRaw holdings from Alpaca:")
        for h in holdings[:3]:  # Show first 3
            print(f"  {h['ticker']}: {h['quantity']} shares @ ${h['current_price']:.2f} = ${h['market_value']:.2f}")
    print()

    # Score the holdings
    print("[3/4] Scoring holdings (this applies the fix)...")
    scored_holdings = research._score_stocks(holdings, context='holdings')
    print(f"✓ Scored {len(scored_holdings)} holdings")

    if scored_holdings:
        print("\nScored holdings (should preserve quantity/market_value):")
        for h in scored_holdings[:3]:  # Show first 3
            ticker = h.get('ticker')
            quantity = h.get('quantity', 'MISSING')
            market_value = h.get('market_value', 'MISSING')
            current_price = h.get('current_price', 0)
            composite = h.get('research_composite_score', 0)

            print(f"  {ticker}:")
            print(f"    Quantity: {quantity}")
            print(f"    Market Value: ${market_value:.2f}" if isinstance(market_value, (int, float)) else f"    Market Value: {market_value}")
            print(f"    Current Price: ${current_price:.2f}")
            print(f"    Composite Score: {composite:.1f}/100")
    print()

    # Test sell order creation
    print("[4/4] Testing sell order creation...")
    if scored_holdings:
        # Simulate what Operations Manager does
        holding = scored_holdings[0]
        ticker = holding.get('ticker')
        quantity = holding.get('quantity', 0)
        market_value = holding.get('market_value', 0)
        current_price = holding.get('current_price', 0)

        sell_order = {
            'ticker': ticker,
            'action': 'SELL',
            'shares': quantity,
            'sell_pct': 100,
            'current_price': current_price,
            'current_value': market_value
        }

        print(f"Sample SELL order for {ticker}:")
        print(f"  Shares: {sell_order['shares']:.0f}")
        print(f"  Price: ${sell_order['current_price']:.2f}")
        print(f"  Total Value: ${sell_order['current_value']:.2f}")

        if sell_order['shares'] > 0 and sell_order['current_value'] > 0:
            print("\n✓ SELL order has valid data!")
        else:
            print("\n✗ SELL order still has $0 - fix did not work")
    else:
        print("✗ No holdings found to test")

    print()
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
