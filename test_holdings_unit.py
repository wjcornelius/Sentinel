#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit test to verify holdings data preservation in _score_stocks
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from Departments.Research.research_department import ResearchDepartment

def test_holdings_data_preservation():
    """Test that _score_stocks preserves Alpaca position data"""

    print("=" * 80)
    print("UNIT TEST: Holdings Data Preservation")
    print("=" * 80)
    print()

    # Create mock holdings with Alpaca position data
    mock_holdings = [
        {
            'ticker': 'AAPL',
            'quantity': 100.0,
            'market_value': 17500.00,
            'current_price': 175.00,
            'cost_basis': 15000.00,
            'unrealized_pl': 2500.00,
            'unrealized_plpc': 16.67
        },
        {
            'ticker': 'MSFT',
            'quantity': 50.0,
            'market_value': 18000.00,
            'current_price': 360.00,
            'cost_basis': 16000.00,
            'unrealized_pl': 2000.00,
            'unrealized_plpc': 12.50
        }
    ]

    print("BEFORE _score_stocks:")
    for h in mock_holdings:
        print(f"  {h['ticker']}: quantity={h['quantity']}, market_value=${h['market_value']:.2f}")
    print()

    # Initialize Research Department (no Alpaca needed for this test)
    research = ResearchDepartment(db_path="sentinel.db")

    # Call _score_stocks which should preserve the position data
    print("Calling _score_stocks with context='holdings'...")
    scored_holdings = research._score_stocks(mock_holdings, context='holdings')
    print()

    print("AFTER _score_stocks:")
    all_passed = True
    for i, h in enumerate(scored_holdings):
        original = mock_holdings[i]
        ticker = h.get('ticker')
        quantity = h.get('quantity')
        market_value = h.get('market_value')

        print(f"  {ticker}:")
        print(f"    quantity: {quantity} (expected {original['quantity']})")
        print(f"    market_value: ${market_value:.2f}" if market_value else f"    market_value: MISSING")
        print(f"    research_composite_score: {h.get('research_composite_score', 0):.1f}/100")

        # Check if data preserved
        if quantity == original['quantity'] and market_value == original['market_value']:
            print(f"    [OK] Data preserved correctly")
        else:
            print(f"    [FAIL] Data LOST!")
            all_passed = False
        print()

    print("=" * 80)
    if all_passed:
        print("TEST PASSED: Holdings data preserved correctly!")
        return 0
    else:
        print("TEST FAILED: Holdings data was not preserved")
        return 1
    print("=" * 80)

if __name__ == '__main__':
    sys.exit(test_holdings_data_preservation())
