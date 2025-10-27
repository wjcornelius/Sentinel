# -*- coding: utf-8 -*-
# scripts/test_tier2_screening.py
# Test script for Tier 2 AI screening

"""
Test Tier 2 AI Screening

Tests the AI screening system with output from Tier 1 filter.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi
from sentinel.tier1_technical_filter import run_tier1_filter
from sentinel.tier2_ai_screening import run_tier2_screening


def main():
    """Test Tier 2 AI screening with Tier 1 output."""

    print("\n" + "=" * 70)
    print("TIER 2 AI SCREENING TEST")
    print("=" * 70)

    # Connect to Alpaca
    api = tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

    # Get test universe
    print("\nFetching current positions...")
    positions = api.list_positions()
    portfolio_symbols = [p.symbol for p in positions]

    # Add well-known stocks for testing
    test_symbols = list(set(portfolio_symbols + [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AMD',
        'NFLX', 'ADBE', 'CRM', 'ORCL', 'AVGO', 'CSCO', 'INTC', 'QCOM',
        'TXN', 'AMAT', 'MU', 'KLAC', 'LRCX', 'ASML', 'SHOP', 'SQ',
        'PYPL', 'V', 'MA', 'JPM', 'BAC', 'WFC', 'GS', 'MS',
        'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'LLY'
    ]))

    print(f"Test universe: {len(test_symbols)} symbols")

    # Run Tier 1 filter
    print("\n" + "-" * 70)
    print("STEP 1: Tier 1 Technical Filter")
    print("-" * 70)

    tier1_candidates = run_tier1_filter(
        api=api,
        universe_symbols=test_symbols,
        target_count=25  # Smaller for testing
    )

    print(f"Tier 1 output: {len(tier1_candidates)} candidates")

    if not tier1_candidates:
        print("ERROR: No candidates from Tier 1!")
        return 1

    # Run Tier 2 screening
    print("\n" + "-" * 70)
    print("STEP 2: Tier 2 AI Screening (GPT-4o-mini)")
    print("-" * 70)
    print(f"Screening {len(tier1_candidates)} candidates...")
    print("(This will take ~30 seconds)")

    market_context = "Market showing mixed signals with tech sector leading gains."

    tier2_finalists = run_tier2_screening(
        api=api,
        tier1_candidates=tier1_candidates,
        market_context=market_context,
        target_count=10  # Top 10 for testing
    )

    # Display results
    print("\n" + "=" * 70)
    print(f"SCREENING RESULTS: {len(tier2_finalists)} finalists selected")
    print("=" * 70)

    if tier2_finalists:
        print("\nTop 10 Finalists:")
        print(f"{'Rank':<6} {'Symbol':<8} {'T1':<6} {'T2':<6} {'Sector':<20} {'Reason':<30}")
        print("-" * 70)

        for i, finalist in enumerate(tier2_finalists[:10], 1):
            symbol = finalist['symbol']
            t1_score = finalist['tier1_score']
            t2_score = finalist['tier2_score']
            sector = finalist['sector'][:18]
            reason = finalist['tier2_reason'][:28]

            print(
                f"{i:<6} "
                f"{symbol:<8} "
                f"{t1_score:>4.0f}  "
                f"{t2_score:>4.0f}  "
                f"{sector:<20} "
                f"{reason:<30}"
            )

        # Show statistics
        print("\n" + "-" * 70)
        print("Screening Statistics:")

        t2_scores = [f['tier2_score'] for f in tier2_finalists]
        print(f"  Tier 2 score range: {min(t2_scores)} - {max(t2_scores)}")

        # Score distribution
        high_scores = sum(1 for s in t2_scores if s >= 7)
        mid_scores = sum(1 for s in t2_scores if 4 <= s < 7)
        low_scores = sum(1 for s in t2_scores if s < 4)

        print(f"  Score distribution:")
        print(f"    High (7-10): {high_scores}")
        print(f"    Mid (4-6): {mid_scores}")
        print(f"    Low (1-3): {low_scores}")

        # Sector breakdown
        sectors = {}
        for f in tier2_finalists:
            sector = f['sector']
            sectors[sector] = sectors.get(sector, 0) + 1

        print(f"\n  Sector breakdown:")
        for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
            print(f"    {sector}: {count}")

    else:
        print("\nWARNING: No finalists from Tier 2!")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
