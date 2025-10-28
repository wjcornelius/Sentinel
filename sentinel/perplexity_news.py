# -*- coding: utf-8 -*-
# sentinel/perplexity_news.py
# Perplexity AI Integration for Real-Time News Gathering
# Week 3 Implementation

"""
Perplexity News Gatherer

Uses Perplexity AI to fetch real-time news, events, and sentiment for tickers.
This fills a critical gap in Tier 3 analysis - providing current market context
that GPT-4-Turbo alone cannot access.

Cost: ~$0.005 per query (pay-per-use) or $20/month unlimited
Purpose: News aggregation for conviction analysis
"""

import logging
import requests
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timezone

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class PerplexityNewsGatherer:
    """
    Fetches real-time news and market events using Perplexity AI.

    Perplexity specializes in web search with citations - perfect for
    gathering recent news that affects trading decisions.
    """

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        """
        Initialize Perplexity news gatherer.

        Args:
            api_key: Perplexity API key (defaults to config.PERPLEXITY_API_KEY)
            logger: Optional logger instance
        """
        self.api_key = api_key or config.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.logger = logger or logging.getLogger(__name__)

        if not self.api_key:
            raise ValueError("Perplexity API key not found in config")

    def gather_ticker_news(
        self,
        symbol: str,
        days_back: int = 7,
        max_words: int = 200
    ) -> Dict[str, any]:
        """
        Gather recent news for a specific ticker.

        Args:
            symbol: Stock ticker (e.g., 'NVDA')
            days_back: How many days of news to fetch (default: 7)
            max_words: Maximum words in summary (default: 200)

        Returns:
            Dict with:
                - symbol: Stock ticker
                - news_summary: Text summary of recent news
                - key_events: List of important events
                - sentiment: Overall sentiment (positive/negative/neutral)
                - sources: List of source URLs
                - timestamp: When news was gathered
                - success: Whether the query succeeded
        """
        self.logger.debug(f"Gathering news for {symbol} (last {days_back} days)")

        prompt = f"""Search for the most recent news and developments about {symbol} stock.
Focus on the last {days_back} days.

Include:
- Major announcements (earnings, products, partnerships)
- Executive changes or leadership news
- Analyst upgrades/downgrades and price target changes
- Sector news affecting this company
- Any legal, regulatory, or compliance issues
- Market sentiment and institutional activity

Summarize in {max_words} words or less.
Format: Brief paragraphs focusing on market-moving events.
Be factual and objective."""

        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",  # Online model for real-time search
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.2,  # Low temperature for factual output
                    "max_tokens": 500
                },
                timeout=30
            )

            if response.status_code != 200:
                self.logger.error(f"Perplexity API error: {response.status_code}")
                self.logger.error(f"Response: {response.text}")

            response.raise_for_status()
            data = response.json()

            # Extract response
            news_summary = data['choices'][0]['message']['content']
            citations = data.get('citations', []) if 'citations' in data else []

            # Basic sentiment analysis based on keywords
            sentiment = self._analyze_sentiment(news_summary)

            # Extract key events (simple version - looks for bullet points or key phrases)
            key_events = self._extract_key_events(news_summary)

            self.logger.info(f"News gathered for {symbol}: {len(news_summary)} chars, {len(citations)} sources")

            return {
                'symbol': symbol,
                'news_summary': news_summary,
                'key_events': key_events,
                'sentiment': sentiment,
                'sources': citations,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': True,
                'days_back': days_back
            }

        except requests.exceptions.HTTPError as e:
            error_detail = e.response.text if hasattr(e, 'response') and e.response else str(e)
            self.logger.error(f"HTTP error fetching news for {symbol}: {e}")
            self.logger.error(f"Response body: {error_detail}")
            return {
                'symbol': symbol,
                'news_summary': f"Error: Unable to fetch news ({e})",
                'key_events': [],
                'sentiment': 'unknown',
                'sources': [],
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': False,
                'error': str(e),
                'error_detail': error_detail
            }

        except Exception as e:
            self.logger.error(f"Error fetching news for {symbol}: {e}")
            return {
                'symbol': symbol,
                'news_summary': f"Error: {str(e)}",
                'key_events': [],
                'sentiment': 'unknown',
                'sources': [],
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': False,
                'error': str(e)
            }

    def gather_market_overview(
        self,
        max_words: int = 300
    ) -> Dict[str, any]:
        """
        Gather overall market conditions and sentiment.

        Args:
            max_words: Maximum words in summary

        Returns:
            Dict with market overview information
        """
        self.logger.debug("Gathering market overview")

        prompt = f"""What are the major market-moving events today and this week?

Focus on:
- Overall market sentiment (bullish/bearish/mixed)
- Key economic data releases and Fed commentary
- Sector rotation and leadership
- Geopolitical events affecting markets
- Major index performance (S&P 500, Nasdaq, Dow)
- VIX and volatility trends

Summarize in {max_words} words or less.
Be concise and focus on actionable market context."""

        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.2,
                    "max_tokens": 600
                },
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            market_summary = data['choices'][0]['message']['content']
            citations = data.get('citations', [])

            self.logger.info(f"Market overview gathered: {len(market_summary)} chars")

            return {
                'market_summary': market_summary,
                'sources': citations,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': True
            }

        except Exception as e:
            self.logger.error(f"Error fetching market overview: {e}")
            return {
                'market_summary': f"Error: {str(e)}",
                'sources': [],
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': False,
                'error': str(e)
            }

    def gather_batch_news(
        self,
        symbols: List[str],
        days_back: int = 7
    ) -> Dict[str, Dict]:
        """
        Gather news for multiple tickers efficiently.

        Args:
            symbols: List of stock tickers
            days_back: How many days of news to fetch

        Returns:
            Dict mapping symbol -> news dict
        """
        self.logger.info(f"Gathering news for {len(symbols)} tickers")

        results = {}
        for symbol in symbols:
            results[symbol] = self.gather_ticker_news(symbol, days_back=days_back)

        successful = sum(1 for r in results.values() if r['success'])
        self.logger.info(f"Batch news gathering complete: {successful}/{len(symbols)} successful")

        return results

    def _analyze_sentiment(self, text: str) -> str:
        """
        Simple keyword-based sentiment analysis.

        Args:
            text: News summary text

        Returns:
            'positive', 'negative', or 'neutral'
        """
        text_lower = text.lower()

        positive_keywords = [
            'beat', 'upgrade', 'raised', 'strong', 'growth', 'partnership',
            'acquisition', 'launched', 'record', 'bullish', 'outperform',
            'exceeded', 'positive', 'momentum'
        ]

        negative_keywords = [
            'miss', 'downgrade', 'lowered', 'weak', 'decline', 'lawsuit',
            'regulatory', 'bearish', 'underperform', 'warning', 'negative',
            'concern', 'investigation', 'departed'
        ]

        positive_count = sum(1 for kw in positive_keywords if kw in text_lower)
        negative_count = sum(1 for kw in negative_keywords if kw in text_lower)

        if positive_count > negative_count * 1.5:
            return 'positive'
        elif negative_count > positive_count * 1.5:
            return 'negative'
        else:
            return 'neutral'

    def _extract_key_events(self, text: str) -> List[str]:
        """
        Extract key events from news summary (simple version).

        Args:
            text: News summary text

        Returns:
            List of key event strings
        """
        # Simple extraction - split by sentences and look for important markers
        events = []

        # Look for sentences with key event markers
        event_markers = [
            'announced', 'reported', 'upgraded', 'downgraded', 'beat',
            'missed', 'launched', 'partnership', 'acquisition', 'earnings'
        ]

        sentences = text.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(marker in sentence_lower for marker in event_markers):
                events.append(sentence.strip())

        # Limit to top 5 events
        return events[:5]


def test_perplexity_integration():
    """Test function to validate Perplexity integration."""
    print("Testing Perplexity News Integration...")
    print("=" * 70)

    gatherer = PerplexityNewsGatherer()

    # Test single ticker
    print("\n1. Testing single ticker news (NVDA):")
    print("-" * 70)
    nvda_news = gatherer.gather_ticker_news('NVDA', days_back=7)

    if nvda_news['success']:
        print(f"Symbol: {nvda_news['symbol']}")
        print(f"Sentiment: {nvda_news['sentiment']}")
        print(f"Summary:\n{nvda_news['news_summary']}")
        print(f"\nKey Events:")
        for event in nvda_news['key_events']:
            print(f"  - {event}")
        print(f"\nSources ({len(nvda_news['sources'])}):")
        for source in nvda_news['sources'][:3]:  # Show first 3
            print(f"  - {source}")
    else:
        print(f"ERROR: {nvda_news.get('error', 'Unknown error')}")

    # Test market overview
    print("\n\n2. Testing market overview:")
    print("-" * 70)
    market = gatherer.gather_market_overview()

    if market['success']:
        print(f"Market Summary:\n{market['market_summary']}")
        print(f"\nSources: {len(market['sources'])} citations")
    else:
        print(f"ERROR: {market.get('error', 'Unknown error')}")

    print("\n" + "=" * 70)
    print("Test complete!")


if __name__ == "__main__":
    # Run test when module is executed directly
    logging.basicConfig(level=logging.INFO)
    test_perplexity_integration()
