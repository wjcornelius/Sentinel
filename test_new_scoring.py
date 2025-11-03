"""
Test New 0-100 Scoring System
==============================
Verify that the new continuous 0-100 scoring system produces better
differentiation than the old 1-10 discrete system.

Tests a sample of stocks to ensure:
1. Scores are properly scaled to 0-100
2. Technical scores use continuous ranges
3. Fundamental scores use continuous ranges
4. Sentiment scores are scaled correctly
5. Composite scores show good distribution
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from Departments.Research.research_department import ResearchDepartment
import yaml
from datetime import datetime
import config as app_config

def test_scoring():
    """Test scoring on sample stocks"""

    print("=" * 80)
    print("TESTING NEW 0-100 SCORING SYSTEM")
    print("=" * 80)

    # Load config
    config_path = Path(__file__).parent / "Config" / "research_config.yaml"
    with open(config_path, 'r') as f:
        research_config = yaml.safe_load(f)

    # Get Perplexity API key from app config
    perplexity_api_key = app_config.PERPLEXITY_API_KEY

    # Database path
    db_path = Path(__file__).parent / "sentinel.db"

    # Initialize Research Department
    print("\nInitializing Research Department...")
    research = ResearchDepartment(research_config, perplexity_api_key, db_path)

    # Test stocks: Mix of quality levels
    test_stocks = [
        "AAPL",  # Blue chip tech
        "MSFT",  # Blue chip tech
        "GOOGL", # Blue chip tech
        "NVDA",  # High growth
        "JPM",   # Blue chip financial
        "BAC",   # Mid-tier financial
        "TSLA",  # Volatile growth
        "F",     # Value/turnaround
        "DIS",   # Entertainment
        "WMT",   # Retail staple
    ]

    print(f"\nTesting {len(test_stocks)} stocks: {', '.join(test_stocks)}")
    print("=" * 80)

    results = []

    for ticker in test_stocks:
        print(f"\n[{ticker}]")

        try:
            # Analyze stock
            analysis = research.analyze_ticker(ticker)

            if analysis:
                tech_score = analysis['technical']['score']
                fund_score = analysis['fundamental']['score']
                sent_score = analysis['sentiment']['score']
                comp_score = analysis['composite_score']

                results.append({
                    'ticker': ticker,
                    'technical': tech_score,
                    'fundamental': fund_score,
                    'sentiment': sent_score,
                    'composite': comp_score
                })

                print(f"  Technical:   {tech_score:.1f}/100")
                print(f"  Fundamental: {fund_score:.1f}/100")
                print(f"  Sentiment:   {sent_score:.1f}/100")
                print(f"  COMPOSITE:   {comp_score:.1f}/100 {'✓ PASS' if comp_score >= 55 else '✗ FAIL'}")

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if results:
        # Sort by composite score
        results.sort(key=lambda x: x['composite'], reverse=True)

        print(f"\nTested: {len(results)} stocks")
        print(f"Threshold: 55/100")

        passing = [r for r in results if r['composite'] >= 55]
        print(f"Passing: {len(passing)} stocks ({len(passing)/len(results)*100:.1f}%)")

        print("\n" + "-" * 80)
        print(f"{'Rank':<6} {'Ticker':<8} {'Composite':<12} {'Tech':<10} {'Fund':<10} {'Sent':<10}")
        print("-" * 80)

        for i, r in enumerate(results, 1):
            status = "✓" if r['composite'] >= 55 else "✗"
            print(f"{i:<6} {r['ticker']:<8} {r['composite']:>6.1f}/100 {status:<3} "
                  f"{r['technical']:>6.1f}/100  {r['fundamental']:>6.1f}/100  {r['sentiment']:>6.1f}/100")

        print("-" * 80)

        # Statistics
        comp_scores = [r['composite'] for r in results]
        tech_scores = [r['technical'] for r in results]
        fund_scores = [r['fundamental'] for r in results]
        sent_scores = [r['sentiment'] for r in results]

        print("\nScore Distribution:")
        print(f"  Composite: min={min(comp_scores):.1f}, max={max(comp_scores):.1f}, avg={sum(comp_scores)/len(comp_scores):.1f}")
        print(f"  Technical: min={min(tech_scores):.1f}, max={max(tech_scores):.1f}, avg={sum(tech_scores)/len(tech_scores):.1f}")
        print(f"  Fundamental: min={min(fund_scores):.1f}, max={max(fund_scores):.1f}, avg={sum(fund_scores)/len(fund_scores):.1f}")
        print(f"  Sentiment: min={min(sent_scores):.1f}, max={max(sent_scores):.1f}, avg={sum(sent_scores)/len(sent_scores):.1f}")

        # Check if we have good differentiation
        comp_range = max(comp_scores) - min(comp_scores)
        print(f"\nComposite Score Range: {comp_range:.1f} points")

        if comp_range < 10:
            print("⚠ WARNING: Scores still too clustered (range < 10 points)")
        elif comp_range < 20:
            print("⚠ CAUTION: Limited differentiation (range < 20 points)")
        else:
            print("✓ GOOD: Scores show good differentiation (range >= 20 points)")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
    else:
        print("\nNO RESULTS - All stocks failed to analyze")

if __name__ == "__main__":
    test_scoring()
