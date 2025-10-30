# -*- coding: utf-8 -*-
# scripts/test_tier1_filter.py
# Test script for Tier 1 technical filtering

"""
Test Tier 1 Technical Filter

Tests the technical filtering system with a sample universe of stocks.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi
from sentinel.tier1_technical_filter import run_tier1_filter


def main():
    """Test Tier 1 filter with sample universe."""

    print("\n" + "=" * 70)
    print("TIER 1 TECHNICAL FILTER TEST")
    print("=" * 70)

    # Connect to Alpaca
    api = tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

    # Test with current portfolio positions + some well-known stocks
    print("\nFetching current positions...")
    positions = api.list_positions()
    portfolio_symbols = [p.symbol for p in positions]

    # Add some well-known tech stocks for testing
    test_symbols = list(set(portfolio_symbols + [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AMD',
        'NFLX', 'ADBE', 'CRM', 'ORCL', 'AVGO', 'CSCO', 'INTC', 'QCOM',
        'TXN', 'AMAT', 'MU', 'KLAC', 'LRCX', 'ASML', 'SHOP', 'SQ',
        'PYPL', 'V', 'MA', 'JPM', 'BAC', 'WFC', 'GS', 'MS',
        'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'LLY'
    ]))

    print(f"Test universe: {len(test_symbols)} symbols")
    print(f"  - {len(portfolio_symbols)} from current portfolio")
    print(f"  - {len(test_symbols) - len(portfolio_symbols)} additional test symbols")

    # Run Tier 1 filter
    print("\nRunning Tier 1 technical filter...")
    print("  Target: Top 25 candidates (scaled for small test universe)")

    candidates = run_tier1_filter(
        api=api,
        universe_symbols=test_symbols,
        target_count=25
    )

    # Display results
    print("\n" + "=" * 70)
    print(f"FILTER RESULTS: {len(candidates)} candidates selected")
    print("=" * 70)

    if candidates:
        print("\nTop 10 Candidates:")
        print(f"{'Rank':<6} {'Symbol':<8} {'Score':<8} {'Price':<10} {'Volume':<12} {'20d%':<8} {'RSI':<6}")
        print("-" * 70)

        for i, candidate in enumerate(candidates[:10], 1):
            symbol = candidate['symbol']
            score = candidate['score']
            metrics = candidate['metrics']

            print(
                f"{i:<6} "
                f"{symbol:<8} "
                f"{score:>6.1f}  "
                f"${metrics['price']:>7.2f}  "
                f"${metrics['avg_dollar_volume']/1e6:>6.1f}M   "
                f"{metrics['change_20d']:>+6.1f}%  "
                f"{metrics['rsi']:>5.1f}"
            )

        # Show some statistics
        print("\n" + "-" * 70)
        print("Filter Statistics:")
        scores = [c['score'] for c in candidates]
        prices = [c['metrics']['price'] for c in candidates]
        volumes = [c['metrics']['avg_dollar_volume'] for c in candidates]

        print(f"  Score range: {min(scores):.1f} - {max(scores):.1f}")
        print(f"  Price range: ${min(prices):.2f} - ${max(prices):.2f}")
        print(f"  Avg volume range: ${min(volumes)/1e6:.1f}M - ${max(volumes)/1e6:.1f}M")

        # Show portfolio symbols that made it through
        portfolio_candidates = [c for c in candidates if c['symbol'] in portfolio_symbols]
        print(f"\n  Portfolio symbols passing filter: {len(portfolio_candidates)}/{len(portfolio_symbols)}")
        if portfolio_candidates:
            portfolio_syms = [c['symbol'] for c in portfolio_candidates]
            print(f"    {', '.join(portfolio_syms)}")

    else:
        print("\nWARNING: No candidates passed the filter!")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
