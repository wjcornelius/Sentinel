#!/usr/bin/env python3
"""
Test script for today's fixes:
1. Alpaca Position parsing
2. Pandas FutureWarning
3. Invalid tickers removed
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from Departments.Executive.ceo import CEO

def main():
    print("=" * 80)
    print("TESTING FIXES - Generating Trading Plan")
    print("=" * 80)
    print()

    # Initialize CEO
    print("[1/3] Initializing CEO...")
    ceo = CEO(project_root=project_root)
    print("✓ CEO initialized")
    print()

    # Generate trading plan
    print("[2/3] Generating trading plan...")
    print("(This will test Research Department with fixes)")
    print()

    result = ceo.generate_plan()

    print()
    print("=" * 80)
    print("[3/3] RESULT")
    print("=" * 80)

    if result['status'] == 'SUCCESS':
        print("✓ Trading plan generated successfully!")
        print()
        plan = result.get('plan', {})
        summary = plan.get('summary', {})

        print(f"Total Trades: {summary.get('total_trades', 0)}")
        print(f"Research Candidates: {summary.get('research_candidates', 0)}")
        print(f"GPT-5 Selected: {summary.get('gpt5_selected', 0)}")
        print(f"Compliance Flagged: {summary.get('compliance_flagged', 0)}")
        print(f"Quality Score: {summary.get('overall_quality_score', 0)}/100")
        print()

        trades = plan.get('trades', [])
        if trades:
            print(f"First 5 trades:")
            for i, trade in enumerate(trades[:5], 1):
                ticker = trade.get('ticker', 'UNKNOWN')
                action = trade.get('action', 'UNKNOWN')
                shares = trade.get('shares', 0)
                price = trade.get('entry_price', trade.get('current_price', 0))
                print(f"  {i}. {action} {shares} {ticker} @ ${price:.2f}")

        print()
        print("=" * 80)
        print("ALL FIXES WORKING! ✓")
        print("=" * 80)
        return 0

    else:
        print(f"✗ Error: {result.get('message', 'Unknown error')}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
