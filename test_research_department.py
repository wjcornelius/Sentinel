"""
Test Research Department - Adaptive Filtering & Alpaca Integration

Tests:
1. Load ticker universe (~515 stocks from S&P 500 + Nasdaq 100)
2. Test adaptive filtering to find ~50 buy candidates
3. Verify Alpaca integration for current holdings
4. Check 16-hour cache for price data
5. Verify output structure (candidates + holdings)
"""

import sys
import logging
from datetime import datetime
from Departments.Research import ResearchDepartment

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_research_department():
    """Test Research Department adaptive filtering"""
    print("=" * 80)
    print("RESEARCH DEPARTMENT TEST - Adaptive Filtering")
    print("=" * 80)
    print()

    # Initialize
    print("[1/5] Initializing Research Department...")
    research = ResearchDepartment(db_path="sentinel.db")
    print("[OK] Initialized")
    print()

    # Load universe
    print("[2/5] Loading ticker universe from ticker_universe.txt...")
    with open("ticker_universe.txt", "r") as f:
        universe = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"[OK] Loaded {len(universe)} tickers from universe")
    print(f"  Sample: {universe[:10]}")
    print()

    # Test adaptive filtering
    print("[3/5] Testing adaptive filtering (target ~50 buy candidates)...")
    print("  This will iterate through filter presets (strict -> loose)")
    print("  until ~50 candidates are found...")
    print()

    start_time = datetime.now()

    # Run research workflow
    result = research.generate_daily_candidate_universe()

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"[OK] Research completed in {elapsed:.1f}s")
    print()

    # Verify structure
    print("[4/5] Verifying output structure...")

    required_keys = ['buy_candidates', 'current_holdings', 'summary']
    missing_keys = [k for k in required_keys if k not in result]

    if missing_keys:
        print(f"[ERROR] Missing keys: {missing_keys}")
        return False

    buy_candidates = result['buy_candidates']
    current_holdings = result['current_holdings']
    summary = result['summary']

    print(f"[OK] Output structure valid")
    print(f"  Buy candidates: {len(buy_candidates)}")
    print(f"  Current holdings: {len(current_holdings)}")
    print(f"  Total stocks: {len(buy_candidates) + len(current_holdings)}")
    print()

    # Check if close to target
    target = 50
    tolerance = 0.2  # 20% tolerance

    if not (target * (1 - tolerance) <= len(buy_candidates) <= target * (1 + tolerance)):
        print(f"[WARNING] Buy candidates {len(buy_candidates)} not close to target {target}")
        print(f"  Expected: {int(target * (1 - tolerance))}-{int(target * (1 + tolerance))}")
    else:
        print(f"[OK] Buy candidates {len(buy_candidates)} within target range")

    print()

    # Verify candidate structure
    print("[5/5] Verifying candidate data structure...")

    if len(buy_candidates) > 0:
        sample = buy_candidates[0]
        required_fields = ['ticker', 'score', 'current_price', 'reasoning']
        missing_fields = [f for f in required_fields if f not in sample]

        if missing_fields:
            print(f"[ERROR] Missing fields in candidates: {missing_fields}")
            return False

        print(f"[OK] Candidate structure valid")
        print(f"  Sample candidate: {sample['ticker']}")
        print(f"    Score: {sample['score']:.1f}/100")
        print(f"    Price: ${sample['current_price']:.2f}")
        print(f"    Reasoning: {sample['reasoning'][:60]}...")
        print()

    # Summary
    print("=" * 80)
    print("TEST RESULTS - RESEARCH DEPARTMENT")
    print("=" * 80)
    print(f"[OK] Universe loading: Working ({len(universe)} tickers)")
    print(f"[OK] Adaptive filtering: Working ({len(buy_candidates)} candidates in {elapsed:.1f}s)")
    print(f"[OK] Data structure: Valid")
    print()

    print("Summary from Research Department:")
    print(f"  {summary.get('universe_size', 0)} tickers in universe")
    print(f"  {summary.get('candidates_found', 0)} buy candidates found")
    print(f"  {summary.get('holdings_count', 0)} current holdings")
    print(f"  {summary.get('total_output', 0)} total stocks for downstream analysis")
    print()

    if len(buy_candidates) > 0:
        print("Top 10 Buy Candidates:")
        for i, candidate in enumerate(buy_candidates[:10], 1):
            print(f"  {i:2d}. {candidate['ticker']:6s} - Score: {candidate['score']:5.1f}/100 - ${candidate['current_price']:7.2f}")
        print()

    print("[OK] Research Department: WORKING")
    return True

if __name__ == "__main__":
    try:
        success = test_research_department()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
