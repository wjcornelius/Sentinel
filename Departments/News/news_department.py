"""
News Department - Sentiment Analysis & Caching

Maintains fresh sentiment scores for stocks using Perplexity AI.
Cache TTL: 16 hours
Batch processing: 10 concurrent requests
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import os

logger = logging.getLogger(__name__)


class NewsDepartment:
    """
    News Department - Manages news and sentiment analysis

    Responsibilities:
    - Fetch news for stocks
    - Generate sentiment scores via Perplexity
    - Cache results with 16-hour TTL
    - Provide sentiment data to other departments
    """

    def __init__(self, db_path: str = "sentinel.db", perplexity_api_key: Optional[str] = None):
        """
        Initialize News Department

        Args:
            db_path: Path to SQLite database
            perplexity_api_key: Perplexity API key (defaults to env var)
        """
        self.db_path = db_path
        self.perplexity_api_key = perplexity_api_key or os.getenv('PERPLEXITY_API_KEY')
        self.cache_ttl_hours = 16
        self.batch_size = 5  # Reduced from 10 to avoid rate limits

        self._initialize_database()
        logger.info("News Department initialized (cache TTL: 16 hours, batch size: 5)")

    def _initialize_database(self):
        """Create news_sentiment_cache table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_sentiment_cache (
                ticker TEXT PRIMARY KEY,
                sentiment_score REAL NOT NULL,
                news_summary TEXT,
                sentiment_reasoning TEXT,
                fetched_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()
        logger.info("News sentiment cache table ready")

    def get_sentiment_scores(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Get sentiment scores for list of tickers
        Fetches from cache if fresh (< 16 hours), otherwise fetches from Perplexity

        Args:
            tickers: List of stock tickers

        Returns:
            Dict mapping ticker to sentiment data:
            {
                'AAPL': {
                    'sentiment_score': 75.0,
                    'news_summary': '...',
                    'sentiment_reasoning': '...',
                    'age_hours': 2.5
                }
            }
        """
        logger.info(f"Fetching sentiment scores for {len(tickers)} tickers")

        # Check cache
        cached, needs_fetch = self._check_cache(tickers)
        logger.info(f"Cache: {len(cached)} hits, {len(needs_fetch)} misses")

        # Batch fetch missing tickers
        if needs_fetch:
            logger.info(f"Fetching {len(needs_fetch)} tickers from Perplexity (batches of {self.batch_size})")
            fresh_data = self._batch_fetch_sentiment(needs_fetch)

            # Update cache
            self._update_cache(fresh_data)

            # Merge with cached
            cached.update(fresh_data)

        return cached

    def _check_cache(self, tickers: List[str]) -> tuple[Dict, List[str]]:
        """
        Check cache for tickers

        Returns:
            (cached_data, tickers_needing_fetch)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cached = {}
        needs_fetch = []
        now = datetime.now()

        for ticker in tickers:
            cursor.execute("""
                SELECT sentiment_score, news_summary, sentiment_reasoning, fetched_at
                FROM news_sentiment_cache
                WHERE ticker = ? AND expires_at > ?
            """, (ticker, now.isoformat()))

            row = cursor.fetchone()

            if row:
                # Cache hit
                fetched_at = datetime.fromisoformat(row[3])
                age_hours = (now - fetched_at).total_seconds() / 3600

                cached[ticker] = {
                    'sentiment_score': row[0],
                    'news_summary': row[1],
                    'sentiment_reasoning': row[2],
                    'age_hours': age_hours
                }
            else:
                # Cache miss
                needs_fetch.append(ticker)

        conn.close()
        return cached, needs_fetch

    def _batch_fetch_sentiment(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Fetch sentiment for tickers in batches (10 concurrent)
        Now with rate limiting protection

        Args:
            tickers: List of tickers to fetch

        Returns:
            Dict mapping ticker to sentiment data
        """
        import time
        results = {}

        # Process in batches with delays to avoid rate limits
        for i in range(0, len(tickers), self.batch_size):
            batch = tickers[i:i + self.batch_size]
            logger.info(f"Processing batch {i//self.batch_size + 1}: {batch}")

            # Fetch batch concurrently
            batch_results = asyncio.run(self._fetch_batch_async(batch))
            results.update(batch_results)

            # Add delay between batches to avoid rate limits (except last batch)
            if i + self.batch_size < len(tickers):
                delay = 5.0  # 5 second delay between batches (increased from 2s)
                logger.info(f"  Waiting {delay}s before next batch (rate limit protection)...")
                time.sleep(delay)

        return results

    async def _fetch_batch_async(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Fetch sentiment for batch of tickers concurrently

        Args:
            tickers: Batch of tickers (max 10)

        Returns:
            Dict mapping ticker to sentiment data
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_sentiment_async(session, ticker) for ticker in tickers]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Build result dict
            batch_results = {}
            for ticker, result in zip(tickers, results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to fetch sentiment for {ticker}: {result}")
                    # Fallback to neutral
                    batch_results[ticker] = {
                        'sentiment_score': 50.0,
                        'news_summary': 'No recent news',
                        'sentiment_reasoning': f'Error fetching sentiment: {result}',
                        'age_hours': 0.0
                    }
                else:
                    batch_results[ticker] = result

            return batch_results

    async def _fetch_sentiment_async(self, session: aiohttp.ClientSession, ticker: str, max_retries: int = 3) -> Dict:
        """
        Fetch sentiment for single ticker from Perplexity
        With retry logic for rate limits and transient errors

        Args:
            session: aiohttp session
            ticker: Stock ticker
            max_retries: Maximum retry attempts

        Returns:
            Sentiment data dict
        """
        import json
        import asyncio

        prompt = f"""Analyze recent news sentiment for {ticker} stock.

Return a JSON object with:
1. sentiment_score: 0-100 (0=very bearish, 50=neutral, 100=very bullish)
2. news_summary: Brief summary of recent news (2-3 sentences)
3. sentiment_reasoning: Why this sentiment score (1-2 sentences)

Base your analysis on news from the last 24 hours."""

        for attempt in range(max_retries):
            try:
                async with session.post(
                    'https://api.perplexity.ai/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.perplexity_api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': 'sonar',
                        'messages': [{'role': 'user', 'content': prompt}]
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    # Handle rate limiting with exponential backoff
                    if response.status == 429:
                        retry_after = int(response.headers.get('Retry-After', 10)) + (attempt * 5)  # Exponential backoff
                        if attempt < max_retries - 1:
                            logger.warning(f"{ticker}: Rate limited (429), retrying in {retry_after}s...")
                            await asyncio.sleep(retry_after)
                            continue
                        else:
                            raise Exception(f"429, message='Too Many Requests', url='{response.url}'")

                    # Handle bad gateway
                    if response.status == 502:
                        if attempt < max_retries - 1:
                            logger.warning(f"{ticker}: Bad Gateway (502), retrying in 2s...")
                            await asyncio.sleep(2)
                            continue
                        else:
                            raise Exception(f"502, message='Bad Gateway', url='{response.url}'")

                    response.raise_for_status()
                    data = await response.json()

                    # Parse response
                    content = data['choices'][0]['message']['content']

                    # Extract JSON - handle various formats
                    try:
                        # Try to find JSON in markdown code block
                        if '```json' in content:
                            json_start = content.find('```json') + 7
                            json_end = content.find('```', json_start)
                            json_str = content[json_start:json_end].strip()
                            parsed = json.loads(json_str)
                        elif '```' in content:
                            # Try generic code block
                            json_start = content.find('```') + 3
                            json_end = content.find('```', json_start)
                            json_str = content[json_start:json_end].strip()
                            parsed = json.loads(json_str)
                        else:
                            # Try parsing entire content as JSON
                            parsed = json.loads(content)
                    except json.JSONDecodeError as je:
                        logger.warning(f"{ticker}: JSON parse error, using neutral sentiment")
                        parsed = {'sentiment_score': 50.0, 'news_summary': content[:200], 'sentiment_reasoning': 'Unable to parse sentiment'}

                    return {
                        'sentiment_score': float(parsed.get('sentiment_score', 50.0)),
                        'news_summary': parsed.get('news_summary', 'No summary available'),
                        'sentiment_reasoning': parsed.get('sentiment_reasoning', 'No reasoning provided'),
                        'age_hours': 0.0
                    }

            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    logger.warning(f"{ticker}: Timeout, retrying...")
                    await asyncio.sleep(1)
                    continue
                else:
                    logger.error(f"{ticker}: Timeout after {max_retries} attempts")
                    raise

            except Exception as e:
                if attempt < max_retries - 1 and ('429' in str(e) or '502' in str(e) or 'Expecting value' in str(e)):
                    logger.warning(f"{ticker}: Error '{e}', retrying...")
                    await asyncio.sleep(2)
                    continue
                else:
                    logger.error(f"Perplexity API error for {ticker}: {e}")
                    raise

    def _update_cache(self, sentiment_data: Dict[str, Dict]):
        """
        Update cache with fresh sentiment data

        Args:
            sentiment_data: Dict mapping ticker to sentiment data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now()
        expires_at = now + timedelta(hours=self.cache_ttl_hours)

        for ticker, data in sentiment_data.items():
            cursor.execute("""
                INSERT OR REPLACE INTO news_sentiment_cache
                (ticker, sentiment_score, news_summary, sentiment_reasoning, fetched_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ticker,
                data['sentiment_score'],
                data.get('news_summary', ''),
                data.get('sentiment_reasoning', ''),
                now.isoformat(),
                expires_at.isoformat()
            ))

        conn.commit()
        conn.close()
        logger.info(f"Updated cache for {len(sentiment_data)} tickers")

    def clear_expired_cache(self):
        """Remove expired entries from cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now()
        cursor.execute("DELETE FROM news_sentiment_cache WHERE expires_at < ?", (now.isoformat(),))

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted > 0:
            logger.info(f"Cleared {deleted} expired cache entries")
