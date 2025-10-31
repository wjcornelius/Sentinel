"""
Quick test to verify Perplexity API works with corrected model name
Tests sentiment analysis for AAPL with the new model name
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
import sqlite3
import time
from pathlib import Path
from research_department import SentimentAnalyzer

# Load config
config_path = Path("Config/research_config.yaml")
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Load API key
from config import PERPLEXITY_API_KEY

db_path = Path("sentinel.db")

print("=" * 80)
print("PERPLEXITY MODEL FIX VERIFICATION TEST")
print("=" * 80)
print()

# Verify config has correct model name
print("CONFIG VERIFICATION:")
print(f"  Model Name: {config['sentiment']['perplexity_model']}")
print()

# Clear cache for AAPL to force fresh API call
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM research_sentiment_cache WHERE ticker = 'AAPL'")
cursor.execute("DELETE FROM research_api_calls WHERE api_name = 'PERPLEXITY'")
conn.commit()
conn.close()

print("SENTIMENT ANALYSIS TEST (AAPL):")
print("-" * 80)

analyzer = SentimentAnalyzer(config, PERPLEXITY_API_KEY)

start_time = time.time()
score, summary, news_count = analyzer.get_sentiment_score("AAPL")
elapsed = time.time() - start_time

print(f"  Sentiment Score: {score}/10")
print(f"  Summary: {summary[:150]}...")
print(f"  News Count: {news_count}")
print(f"  Time: {elapsed:.2f}s")
print()

# Check if API call was logged
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT api_name, endpoint, success, response_time_ms, error_message
    FROM research_api_calls
    WHERE api_name = 'PERPLEXITY'
    ORDER BY timestamp DESC
    LIMIT 1
""")
result = cursor.fetchone()
conn.close()

if result:
    api_name, endpoint, success, response_time, error = result
    print("API CALL RESULT:")
    print(f"  API: {api_name}")
    print(f"  Endpoint: {endpoint}")
    print(f"  Success: {'YES' if success == 1 else 'NO'}")
    print(f"  Response Time: {response_time}ms")
    if error:
        print(f"  Error: {error}")
    print()

if score != 5.0 or news_count > 0:
    print("[SUCCESS] Perplexity API call succeeded with corrected model name!")
else:
    print("[WARNING] API may have failed - returned neutral fallback score")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
