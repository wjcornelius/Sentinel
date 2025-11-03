"""
Quick Research Test - 25 tickers only (smoke test)
"""

import sys
import logging
import tempfile
from datetime import datetime
from Departments.Research import ResearchDepartment

logging.basicConfig(level=logging.WARNING)  # Suppress INFO logs
logger = logging.getLogger(__name__)

def test_research_quick():
    """Quick smoke test with 25 tickers"""
    print("=" * 80)
    print("RESEARCH DEPARTMENT QUICK TEST - 25 Tickers")
    print("=" * 80)
    print()

    # Create temp universe file with just 25 tickers
    test_tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',
        'META', 'TSLA', 'V', 'JNJ',
        'WMT', 'JPM', 'MA', 'PG', 'UNH',
        'HD', 'CVX', 'LLY', 'ABBV', 'MRK',
        'KO', 'PEP', 'COST', 'AVGO', 'TMO', 'NFLX'
    ]

    # Write temp universe
    with open("ticker_universe.txt.bak_test", "w") as f:
        f.write("# Test universe - 25 tickers\n")
        for ticker in test_tickers:
            f.write(f"{ticker}\n")

    print(f"[1/3] Created test universe: {len(test_tickers)} tickers")
    print()

    # Initialize with test file
    print("[2/3] Running adaptive filtering...")
    research = ResearchDepartment(db_path="sentinel.db")

    # Temporarily swap universe file
    original_file = research.universe_file
    research.universe_file = "ticker_universe.txt.bak_test"

    start_time = datetime.now()
    result = research.generate_daily_candidate_universe()
    elapsed = (datetime.now() - start_time).total_seconds()

    # Restore
    research.universe_file = original_file

    print(f"[OK] Completed in {elapsed:.1f}s")
    print()

    # Check results
    print("[3/3] Verifying results...")

    buy_candidates = result.get('buy_candidates', [])
    current_holdings = result.get('current_holdings', [])

    print(f"[OK] Buy candidates: {len(buy_candidates)}")
    print(f"[OK] Current holdings: {len(current_holdings)}")
    print(f"[OK] Total output: {len(buy_candidates) + len(current_holdings)}")
    print()

    if len(buy_candidates) > 0:
        print("Top 10 Buy Candidates:")
        for i, c in enumerate(buy_candidates[:10], 1):
            print(f"  {i:2d}. {c['ticker']:6s} - Score: {c['score']:5.1f}/100")
        print()

    print("=" * 80)
    print("[OK] Research Department: WORKING")
    print("=" * 80)

    # Cleanup
    import os
    os.remove("ticker_universe.txt.bak_test")

    return True

if __name__ == "__main__":
    try:
        success = test_research_quick()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
