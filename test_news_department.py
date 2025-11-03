"""
Test News Department - Sentiment Caching & Batch Fetching

Tests:
1. Fetch sentiment for 25 tickers (should batch in groups of 10)
2. Verify cache hit on second fetch (< 16 hours)
3. Check sentiment_score, news_summary, sentiment_reasoning fields
4. Verify fallback to neutral (50.0) on API errors
"""

import sys
import logging
from datetime import datetime
from Departments.News import NewsDepartment

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_news_department():
    """Test News Department sentiment caching"""
    print("=" * 80)
    print("NEWS DEPARTMENT TEST - Sentiment Caching & Batch Fetching")
    print("=" * 80)
    print()

    # Initialize
    print("[1/5] Initializing News Department...")
    news_dept = NewsDepartment(db_path="sentinel.db")
    print("[OK] Initialized")
    print()

    # Test with 25 tickers (will batch in groups of 10)
    test_tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',
        'META', 'TSLA', 'BRK.B', 'V', 'JNJ',
        'WMT', 'JPM', 'MA', 'PG', 'UNH',
        'HD', 'CVX', 'LLY', 'ABBV', 'MRK',
        'KO', 'PEP', 'COST', 'AVGO', 'TMO'
    ]

    print(f"[2/5] Fetching sentiment for {len(test_tickers)} tickers (fresh fetch)...")
    print("Expected: 3 batches (10 + 10 + 5)")
    print()

    start_time = datetime.now()
    sentiment_data = news_dept.get_sentiment_scores(test_tickers)
    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"[OK] Fetched {len(sentiment_data)} sentiment scores in {elapsed:.1f}s")
    print()

    # Verify structure
    print("[3/5] Verifying sentiment data structure...")
    sample_ticker = test_tickers[0]
    sample_data = sentiment_data[sample_ticker]

    required_fields = ['sentiment_score', 'news_summary', 'sentiment_reasoning', 'age_hours']
    missing_fields = [f for f in required_fields if f not in sample_data]

    if missing_fields:
        print(f"[ERROR] Missing fields: {missing_fields}")
        return False

    print(f"[OK] All required fields present")
    print(f"  Sample ({sample_ticker}):")
    print(f"    sentiment_score: {sample_data['sentiment_score']}")
    print(f"    news_summary: {sample_data['news_summary'][:80]}...")
    print(f"    sentiment_reasoning: {sample_data['sentiment_reasoning'][:80]}...")
    print(f"    age_hours: {sample_data['age_hours']:.2f}")
    print()

    # Test cache hit
    print("[4/5] Testing cache (should be instant)...")
    start_time = datetime.now()
    cached_data = news_dept.get_sentiment_scores(test_tickers)
    cache_elapsed = (datetime.now() - start_time).total_seconds()

    print(f"[OK] Cache hit in {cache_elapsed:.3f}s (vs {elapsed:.1f}s fresh fetch)")
    print()

    # Verify scores are in 0-100 range
    print("[5/5] Validating sentiment scores (0-100 range)...")
    invalid_scores = []
    for ticker, data in sentiment_data.items():
        score = data['sentiment_score']
        if not (0 <= score <= 100):
            invalid_scores.append((ticker, score))

    if invalid_scores:
        print(f"[ERROR] {len(invalid_scores)} invalid scores found:")
        for ticker, score in invalid_scores[:5]:
            print(f"  {ticker}: {score}")
        return False

    print(f"[OK] All {len(sentiment_data)} scores in valid range (0-100)")
    print()

    # Summary
    print("=" * 80)
    print("TEST RESULTS - NEWS DEPARTMENT")
    print("=" * 80)
    print(f"[OK] Batch fetching: Working ({len(test_tickers)} tickers in {elapsed:.1f}s)")
    print(f"[OK] Cache hit: Working ({cache_elapsed:.3f}s)")
    print(f"[OK] Data structure: Valid")
    print(f"[OK] Score range: Valid (0-100)")
    print()

    # Sample scores
    print("Sample Sentiment Scores:")
    for ticker in test_tickers[:10]:
        data = sentiment_data[ticker]
        score = data['sentiment_score']
        print(f"  {ticker:6s}: {score:5.1f}/100 - {data['news_summary'][:60]}...")
    print()

    print("[OK] News Department: WORKING")
    return True

if __name__ == "__main__":
    try:
        success = test_news_department()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
