# -*- coding: utf-8 -*-
# scripts/test_full_conviction_pipeline.py
# Test the complete three-tier conviction analysis pipeline

"""
Test Full Conviction Pipeline

Tests the complete flow:
Tier 1 (Technical) → Tier 2 (AI Screening) → Context Builder → Tier 3 (Deep Analysis)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi
from sentinel.tier1_technical_filter import run_tier1_filter
from sentinel.tier2_ai_screening import run_tier2_screening
from sentinel.context_builder import build_context
from sentinel.tier3_conviction_analysis import run_tier3_analysis


def main():
    """Test full conviction analysis pipeline."""

    print("\n" + "=" * 70)
    print("FULL CONVICTION ANALYSIS PIPELINE TEST")
    print("=" * 70)

    # Connect to Alpaca
    api = tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

    # Get test universe
    print("\nFetching test universe...")
    positions = api.list_positions()
    portfolio_symbols = [p.symbol for p in positions]

    test_symbols = list(set(portfolio_symbols + [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AMD',
        'NFLX', 'ADBE', 'CRM', 'ORCL', 'AVGO', 'CSCO', 'INTC', 'QCOM',
        'TXN', 'AMAT', 'MU', 'KLAC', 'LRCX', 'SHOP', 'SQ',
        'PYPL', 'V', 'MA', 'JPM', 'BAC', 'WFC', 'GS', 'MS',
        'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'LLY'
    ]))

    print(f"Test universe: {len(test_symbols)} symbols")

    # ========================================================================
    # TIER 1: Technical Filter
    # ========================================================================
    print("\n" + "=" * 70)
    print("TIER 1: Technical Filter (2500 -> 250)")
    print("=" * 70)

    tier1_candidates = run_tier1_filter(
        api=api,
        universe_symbols=test_symbols,
        target_count=15  # Smaller for testing
    )

    print(f"[OK] Tier 1 complete: {len(tier1_candidates)} candidates")
    if tier1_candidates:
        top_3 = [(c['symbol'], c['score']) for c in tier1_candidates[:3]]
        print(f"  Top 3: {top_3}")

    # ========================================================================
    # TIER 2: AI Screening
    # ========================================================================
    print("\n" + "=" * 70)
    print("TIER 2: AI Screening (250 -> 70)")
    print("=" * 70)
    print("(This will take ~20 seconds)")

    tier2_finalists = run_tier2_screening(
        api=api,
        tier1_candidates=tier1_candidates,
        market_context="Market showing mixed signals with tech leadership.",
        target_count=8  # Smaller for testing
    )

    print(f"[OK] Tier 2 complete: {len(tier2_finalists)} finalists")
    if tier2_finalists:
        top_3 = [(f['symbol'], f['tier2_score']) for f in tier2_finalists[:3]]
        print(f"  Top 3: {top_3}")

    # ========================================================================
    # CONTEXT BUILDER: Hierarchical Context
    # ========================================================================
    print("\n" + "=" * 70)
    print("CONTEXT BUILDER: Hierarchical Context")
    print("=" * 70)

    hierarchical_context = build_context(
        tier2_finalists=tier2_finalists,
        market_news="Tech stocks leading market gains amid interest rate uncertainty."
    )

    print(f"[OK] Context built:")
    print(f"  - Market context: {len(hierarchical_context['market_context'])} chars")
    print(f"  - Sector contexts: {len(hierarchical_context['sector_contexts'])} sectors")
    for sector in hierarchical_context['sector_contexts'].keys():
        print(f"    - {sector}")

    # ========================================================================
    # TIER 3: Deep Conviction Analysis
    # ========================================================================
    print("\n" + "=" * 70)
    print("TIER 3: Deep Conviction Analysis (70 stocks)")
    print("=" * 70)
    print("(This will take ~2-3 minutes)")

    # Get current positions for context
    current_positions = {p.symbol: p for p in api.list_positions()}

    conviction_results = run_tier3_analysis(
        api=api,
        tier2_finalists=tier2_finalists,
        hierarchical_context=hierarchical_context,
        current_positions=current_positions
    )

    print(f"[OK] Tier 3 complete: {len(conviction_results)} analyzed")

    # ========================================================================
    # FINAL RESULTS
    # ========================================================================
    print("\n" + "=" * 70)
    print("FINAL CONVICTION ANALYSIS RESULTS")
    print("=" * 70)

    if conviction_results:
        # Separate by decision
        buys = [r for r in conviction_results if r['decision'] == 'BUY']
        sells = [r for r in conviction_results if r['decision'] == 'SELL']
        holds = [r for r in conviction_results if r['decision'] == 'HOLD']

        print(f"\nDecision Breakdown:")
        print(f"  BUY:  {len(buys)}")
        print(f"  SELL: {len(sells)}")
        print(f"  HOLD: {len(holds)}")

        # Show BUY recommendations
        if buys:
            buys.sort(key=lambda x: x['conviction_score'], reverse=True)
            print(f"\nTop BUY Recommendations:")
            print(f"{'Symbol':<8} {'Conv':<6} {'Price':<10} {'Rationale':<50}")
            print("-" * 70)

            for buy in buys[:5]:
                rationale_short = buy['rationale'][:47] + "..." if len(buy['rationale']) > 50 else buy['rationale']
                print(
                    f"{buy['symbol']:<8} "
                    f"{buy['conviction_score']:<6} "
                    f"${buy['latest_price']:<9.2f} "
                    f"{rationale_short:<50}"
                )

        # Score distribution
        scores = [r['conviction_score'] for r in conviction_results]
        print(f"\nConviction Score Distribution:")
        print(f"  High (8-10): {sum(1 for s in scores if s >= 8)}")
        print(f"  Mid (5-7):   {sum(1 for s in scores if 5 <= s < 8)}")
        print(f"  Low (1-4):   {sum(1 for s in scores if s < 5)}")
        print(f"  Average:     {sum(scores)/len(scores):.1f}")

    else:
        print("\nWARNING: No conviction results!")

    print("\n" + "=" * 70)
    print("PIPELINE TEST COMPLETE")
    print("=" * 70)

    # Summary
    print("\nPipeline Summary:")
    print(f"  Input:  {len(test_symbols)} symbols")
    print(f"  Tier 1: {len(tier1_candidates)} candidates (technical filter)")
    print(f"  Tier 2: {len(tier2_finalists)} finalists (AI screening)")
    print(f"  Tier 3: {len(conviction_results)} analyzed (deep conviction)")
    if conviction_results:
        buys = sum(1 for r in conviction_results if r['decision'] == 'BUY')
        print(f"  Output: {buys} BUY signals")

    return 0


if __name__ == "__main__":
    sys.exit(main())
