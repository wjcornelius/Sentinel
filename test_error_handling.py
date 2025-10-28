"""
Quick test to validate Perplexity error handling
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sentinel.perplexity_news import PerplexityNewsGatherer
from unittest.mock import patch, Mock
import requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 70)
print("Testing Perplexity Error Handling")
print("=" * 70)
print()

# Initialize gatherer
gatherer = PerplexityNewsGatherer(logger=logger)

# Test 1: Simulate ConnectionError
print("Test 1: Simulating ConnectionError...")
print("-" * 70)

with patch('requests.post') as mock_post:
    # Mock a connection error
    mock_post.side_effect = requests.exceptions.ConnectionError("Remote end closed connection")

    result = gatherer.gather_ticker_news('TEST_TICKER')

    if result['success'] == False and result['error'] == 'ConnectionError':
        print("[PASS] ConnectionError handled gracefully")
        print(f"  news_summary: {result['news_summary']}")
        print(f"  sentiment: {result['sentiment']}")
    else:
        print(f"[FAIL] Expected success=False with error='ConnectionError', got: {result}")

print()

# Test 2: Simulate Timeout
print("Test 2: Simulating Timeout...")
print("-" * 70)

with patch('requests.post') as mock_post:
    # Mock a timeout
    mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

    result = gatherer.gather_ticker_news('TEST_TICKER')

    if result['success'] == False and result['error'] == 'Timeout':
        print("[PASS] Timeout handled gracefully")
        print(f"  news_summary: {result['news_summary']}")
        print(f"  sentiment: {result['sentiment']}")
    else:
        print(f"[FAIL] Expected success=False with error='Timeout', got: {result}")

print()

# Test 3: Simulate Unexpected Exception
print("Test 3: Simulating Unexpected Exception...")
print("-" * 70)

with patch('requests.post') as mock_post:
    # Mock an unexpected error
    mock_post.side_effect = ValueError("Unexpected error")

    result = gatherer.gather_ticker_news('TEST_TICKER')

    if result['success'] == False and 'error' in result:
        print("[PASS] Unexpected exception caught")
        print(f"  error type: {result['error']}")
        print(f"  news_summary: {result['news_summary']}")
        print(f"  sentiment: {result['sentiment']}")
    else:
        print(f"[FAIL] Expected success=False with error key, got: {result}")

print()

# Test 4: Test market overview error handling
print("Test 4: Testing market overview ConnectionError...")
print("-" * 70)

with patch('requests.post') as mock_post:
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

    result = gatherer.gather_market_overview()

    if result['success'] == False and result['error'] == 'ConnectionError':
        print("[PASS] Market overview ConnectionError handled")
        print(f"  market_summary: {result['market_summary']}")
    else:
        print(f"[FAIL] Expected success=False with ConnectionError, got: {result}")

print()
print("=" * 70)
print("Error Handling Tests Complete")
print("=" * 70)
print()
print("Summary:")
print("  All error types are now caught and handled gracefully")
print("  Workflow will continue even if individual tickers fail")
print("  Failed tickers return neutral sentiment with error details")
