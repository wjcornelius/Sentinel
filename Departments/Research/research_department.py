"""
Research Department - Market Intelligence and Stock Analysis
Built fresh from DEPARTMENTAL_SPECIFICATIONS v1.0

Responsibilities:
- Monitor market conditions (VIX, SPY, sector rotation)
- Analyze sentiment via Perplexity API (with caching)
- Calculate technical indicators (RSI, MACD, Bollinger Bands)
- Evaluate fundamentals (P/E, revenue growth, margins)
- Generate DailyBriefing messages with stock candidates

Pattern: Message-based architecture (same as Trading Department)
Zero code reuse from v6.2 (100% fresh implementation)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging
import json
import yaml
import uuid
import sqlite3
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ResearchDepartment')


@dataclass
class MarketConditions:
    """Market condition snapshot"""
    date: date
    spy_price: float
    spy_change_pct: float
    qqq_price: float
    qqq_change_pct: float
    vix_level: float
    vix_status: str  # NORMAL, ELEVATED, CAUTION, PANIC
    market_sentiment: str  # BULLISH, NEUTRAL, BEARISH
    top_sectors: List[Dict]  # [{"sector": "Technology", "change_pct": 1.2}, ...]
    bottom_sectors: List[Dict]


@dataclass
class StockAnalysis:
    """Comprehensive stock analysis results"""
    ticker: str
    company_name: str
    sector: str
    current_price: float

    # Technical scores
    rsi: float
    macd: float
    macd_signal: float
    bollinger_position: float
    volume_ratio: float
    technical_score: float  # 1-10

    # Fundamental scores
    market_cap: float
    pe_ratio: Optional[float]
    revenue_growth_yoy: Optional[float]
    profit_margin: Optional[float]
    debt_to_equity: Optional[float]
    fundamental_score: float  # 1-10

    # Sentiment scores
    sentiment_score: float  # 1-10
    sentiment_summary: str
    news_count: int

    # Overall assessment
    overall_score: float  # 1-10
    catalyst: str  # Why this stock is interesting


class MessageHandler:
    """
    Handles reading and writing messages for Research Department

    Pattern learned from Trading Department (Week 1)
    Implements YAML frontmatter + Markdown + JSON payload format
    """

    def __init__(self):
        self.inbox_path = Path("Messages_Between_Departments/Inbox/RESEARCH")
        self.outbox_path = Path("Messages_Between_Departments/Outbox/RESEARCH")
        self.archive_path = Path("Messages_Between_Departments/Archive")

        # Create directories if they don't exist
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        self.outbox_path.mkdir(parents=True, exist_ok=True)

        logger.info("MessageHandler initialized for Research Department")

    def read_message(self, message_path: Path) -> Tuple[Dict, str]:
        """
        Read message from file and parse YAML frontmatter + markdown body

        Returns:
            (metadata_dict, body_string)
        """
        with open(message_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split YAML frontmatter from body
        parts = content.split('---\n')
        if len(parts) < 3:
            raise ValueError(f"Invalid message format in {message_path}")

        metadata = yaml.safe_load(parts[1])
        body = '---\n'.join(parts[2:]).strip()

        logger.info(f"Read message: {metadata.get('message_id')}")
        return metadata, body

    def write_message(self, to_dept: str, message_type: str, subject: str,
                     body: str, data_payload: Optional[Dict] = None,
                     priority: str = 'routine') -> str:
        """
        Write message to outbox with YAML frontmatter + markdown + JSON payload

        Returns:
            message_id (for database tracking)
        """
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        msg_id = f"MSG_RESEARCH_{timestamp}_{uuid.uuid4().hex[:8]}"

        # Build YAML frontmatter
        metadata = {
            'message_id': msg_id,
            'from': 'RESEARCH',
            'to': to_dept,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'message_type': message_type,
            'priority': priority,
            'requires_response': False
        }

        # Build message content
        content = "---\n"
        content += yaml.dump(metadata, default_flow_style=False)
        content += "---\n\n"
        content += f"# {subject}\n\n"
        content += body

        # Add JSON payload if provided
        if data_payload:
            content += "\n\n```json\n"
            content += json.dumps(data_payload, indent=2)
            content += "\n```\n"

        # Write to outbox
        filename = f"{msg_id}.md"
        filepath = self.outbox_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Wrote message {msg_id} to {to_dept}")
        return msg_id

    def archive_message(self, message_path: Path):
        """Move processed message to archive"""
        today = datetime.now().strftime('%Y-%m-%d')
        archive_dir = self.archive_path / today / "RESEARCH"
        archive_dir.mkdir(parents=True, exist_ok=True)

        archived_path = archive_dir / message_path.name

        # If file already exists in archive, remove inbox file
        if archived_path.exists():
            message_path.unlink()
        else:
            message_path.rename(archived_path)

        logger.info(f"Archived message: {message_path.name}")


class MarketDataCollector:
    """
    Collects market data from yfinance and Alpaca APIs

    Responsibilities:
    - Fetch VIX level
    - Fetch SPY/QQQ/DIA prices and changes
    - Calculate sector performance (using sector ETFs)
    - Determine market sentiment (BULLISH/NEUTRAL/BEARISH)
    """

    def __init__(self, config: Dict):
        self.config = config
        self.vix_thresholds = config['market_conditions']['vix_thresholds']
        self.sector_etfs = config['market_conditions']['sector_etfs']

        logger.info("MarketDataCollector initialized")

    def get_market_conditions(self) -> MarketConditions:
        """
        Fetch current market conditions

        Returns:
            MarketConditions dataclass with all market metrics
        """
        logger.info("Fetching market conditions...")

        try:
            # Fetch major indices
            spy = yf.Ticker("SPY")
            qqq = yf.Ticker("QQQ")
            vix = yf.Ticker("^VIX")

            # Get current prices
            spy_data = spy.history(period="2d")
            qqq_data = qqq.history(period="2d")
            vix_data = vix.history(period="1d")

            if len(spy_data) < 2 or len(qqq_data) < 2:
                raise ValueError("Insufficient historical data")

            # Calculate changes
            spy_price = float(spy_data['Close'].iloc[-1])
            spy_prev = float(spy_data['Close'].iloc[-2])
            spy_change_pct = ((spy_price - spy_prev) / spy_prev) * 100

            qqq_price = float(qqq_data['Close'].iloc[-1])
            qqq_prev = float(qqq_data['Close'].iloc[-2])
            qqq_change_pct = ((qqq_price - qqq_prev) / qqq_prev) * 100

            vix_level = float(vix_data['Close'].iloc[-1])

            # Determine VIX status
            if vix_level < self.vix_thresholds['normal']:
                vix_status = 'NORMAL'
            elif vix_level < self.vix_thresholds['elevated']:
                vix_status = 'ELEVATED'
            elif vix_level < self.vix_thresholds['panic']:
                vix_status = 'CAUTION'
            else:
                vix_status = 'PANIC'

            # Determine overall market sentiment
            avg_change = (spy_change_pct + qqq_change_pct) / 2
            if avg_change > 0.5:
                market_sentiment = 'BULLISH'
            elif avg_change < -0.5:
                market_sentiment = 'BEARISH'
            else:
                market_sentiment = 'NEUTRAL'

            # Fetch sector performance
            top_sectors, bottom_sectors = self._get_sector_performance()

            logger.info(f"Market conditions: SPY {spy_change_pct:+.2f}%, VIX {vix_level:.1f} ({vix_status})")

            return MarketConditions(
                date=date.today(),
                spy_price=spy_price,
                spy_change_pct=spy_change_pct,
                qqq_price=qqq_price,
                qqq_change_pct=qqq_change_pct,
                vix_level=vix_level,
                vix_status=vix_status,
                market_sentiment=market_sentiment,
                top_sectors=top_sectors[:3],
                bottom_sectors=bottom_sectors[:3]
            )

        except Exception as e:
            logger.error(f"Failed to fetch market conditions: {e}", exc_info=True)
            raise

    def _get_sector_performance(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Calculate sector performance using sector ETFs

        Returns:
            (top_performers, bottom_performers)
        """
        sector_performance = []

        for sector_name, etf_ticker in self.sector_etfs.items():
            try:
                etf = yf.Ticker(etf_ticker)
                data = etf.history(period="2d")

                if len(data) >= 2:
                    current = float(data['Close'].iloc[-1])
                    prev = float(data['Close'].iloc[-2])
                    change_pct = ((current - prev) / prev) * 100

                    sector_performance.append({
                        'sector': sector_name,
                        'etf': etf_ticker,
                        'change_pct': change_pct
                    })
            except Exception as e:
                logger.warning(f"Failed to fetch {sector_name} ({etf_ticker}): {e}")

        # Sort by performance
        sorted_sectors = sorted(sector_performance, key=lambda x: x['change_pct'], reverse=True)

        top_performers = sorted_sectors[:3]
        bottom_performers = sorted_sectors[-3:]

        return top_performers, bottom_performers


class SentimentAnalyzer:
    """
    Analyzes news sentiment using Perplexity API with intelligent caching

    Features:
    - 24-hour sentiment cache (reduces API costs)
    - Keyword-based scoring
    - Exponential backoff retry (pattern from Trading Department)
    """

    def __init__(self, config: Dict, api_key: str):
        self.config = config
        self.api_key = api_key
        self.cache_ttl_hours = config['sentiment']['cache_ttl_hours']
        self.model = config['sentiment']['perplexity_model']
        self.bullish_keywords = config['sentiment']['bullish_keywords']
        self.bearish_keywords = config['sentiment']['bearish_keywords']

        self.db_path = Path("sentinel.db")

        logger.info(f"SentimentAnalyzer initialized (model: {self.model}, cache TTL: {self.cache_ttl_hours}h)")

    def get_sentiment_score(self, ticker: str) -> Tuple[float, str, int]:
        """
        Get sentiment score for ticker (1-10 scale)

        Checks cache first, falls back to Perplexity API on cache miss

        Returns:
            (sentiment_score, sentiment_summary, news_count)
        """
        # Check cache first
        cached_sentiment = self._check_cache(ticker)
        if cached_sentiment:
            logger.info(f"Sentiment cache HIT for {ticker}")
            return cached_sentiment

        logger.info(f"Sentiment cache MISS for {ticker} - calling Perplexity API")

        # Fetch from Perplexity API
        sentiment_score, sentiment_summary, news_count = self._fetch_from_perplexity(ticker)

        # Store in cache
        self._store_in_cache(ticker, sentiment_score, sentiment_summary, news_count)

        return sentiment_score, sentiment_summary, news_count

    def _check_cache(self, ticker: str) -> Optional[Tuple[float, str, int]]:
        """Check if sentiment is cached and still valid"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.utcnow()

        cursor.execute("""
            SELECT sentiment_score, sentiment_summary, news_articles_count
            FROM research_sentiment_cache
            WHERE ticker = ?
              AND query_date = ?
              AND expires_at > ?
        """, (ticker, date.today(), now))

        result = cursor.fetchone()
        conn.close()

        if result:
            return (float(result[0]), result[1], int(result[2]))
        return None

    def _fetch_from_perplexity(self, ticker: str) -> Tuple[float, str, int]:
        """
        Fetch sentiment from Perplexity API with retry logic

        Pattern learned from Trading Department's exponential backoff
        """
        retry_delays = self.config['api']['perplexity']['retry_delays']
        max_retries = self.config['api']['perplexity']['max_retries']
        timeout = self.config['api']['perplexity']['timeout_seconds']

        prompt = f"""Analyze recent news sentiment for {ticker} stock.
        Provide a brief summary (2-3 sentences) of the overall sentiment and key themes.
        Focus on: earnings, analyst ratings, product news, management changes, market position."""

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    'https://api.perplexity.ai/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': self.model,
                        'messages': [{'role': 'user', 'content': prompt}],
                        'temperature': 0.2,
                        'max_tokens': 200
                    },
                    timeout=timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    summary = data['choices'][0]['message']['content']

                    # Calculate sentiment score from keywords
                    sentiment_score = self._calculate_sentiment_from_text(summary)

                    # Estimate news count (Perplexity doesn't provide this directly)
                    news_count = 10  # Placeholder - Perplexity analyzes multiple sources

                    self._log_api_call('PERPLEXITY', 'SUCCESS', response.elapsed.total_seconds() * 1000)

                    logger.info(f"Perplexity sentiment for {ticker}: {sentiment_score}/10")
                    return sentiment_score, summary, news_count

                elif response.status_code == 429:  # Rate limited
                    logger.warning(f"Perplexity rate limit hit (attempt {attempt+1}/{max_retries})")
                    self._log_api_call('PERPLEXITY', 'RATE_LIMITED', 0, error=str(response.status_code))

                    if attempt < max_retries - 1:
                        import time
                        time.sleep(retry_delays[attempt])
                else:
                    raise Exception(f"Perplexity API error: {response.status_code} - {response.text}")

            except Exception as e:
                logger.error(f"Perplexity API call failed (attempt {attempt+1}/{max_retries}): {e}")
                self._log_api_call('PERPLEXITY', 'ERROR', 0, error=str(e))

                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delays[attempt])
                else:
                    # Fallback: return neutral score with error message
                    return 5.0, f"Unable to fetch sentiment (API error: {str(e)})", 0

        return 5.0, "Unable to fetch sentiment (max retries exceeded)", 0

    def _calculate_sentiment_from_text(self, text: str) -> float:
        """
        Calculate sentiment score (1-10) based on keyword analysis

        Simple keyword counting approach for Phase 1
        """
        text_lower = text.lower()

        bullish_count = sum(1 for keyword in self.bullish_keywords if keyword in text_lower)
        bearish_count = sum(1 for keyword in self.bearish_keywords if keyword in text_lower)

        # Baseline neutral score
        score = 5.0

        # Adjust based on keyword balance
        net_sentiment = bullish_count - bearish_count

        # Scale: each keyword difference = 0.5 points
        score += net_sentiment * 0.5

        # Clamp to 1-10 range
        score = max(1.0, min(10.0, score))

        return round(score, 1)

    def _store_in_cache(self, ticker: str, sentiment_score: float,
                       sentiment_summary: str, news_count: int):
        """Store sentiment in cache with TTL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        expires_at = datetime.utcnow() + timedelta(hours=self.cache_ttl_hours)

        cursor.execute("""
            INSERT OR REPLACE INTO research_sentiment_cache
            (ticker, query_date, sentiment_score, sentiment_summary,
             news_articles_count, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticker, date.today(), sentiment_score, sentiment_summary,
              news_count, expires_at))

        conn.commit()
        conn.close()

        logger.info(f"Cached sentiment for {ticker} (expires: {expires_at})")

    def _log_api_call(self, api_name: str, status: str, response_time_ms: float,
                     error: Optional[str] = None):
        """Log API call to database for rate limit tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO research_api_calls
            (api_name, endpoint, response_status, response_time_ms, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (api_name, '/chat/completions', status, int(response_time_ms), error))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Quick test of MarketDataCollector
    logger.info("Research Department - Testing MarketDataCollector")

    # Load config
    config_path = Path("Config/research_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Test market data collection
    collector = MarketDataCollector(config)
    try:
        market_conditions = collector.get_market_conditions()
        logger.info(f"Market test successful: SPY ${market_conditions.spy_price:.2f} ({market_conditions.spy_change_pct:+.2f}%)")
        logger.info(f"VIX: {market_conditions.vix_level:.1f} ({market_conditions.vix_status})")
        logger.info(f"Sentiment: {market_conditions.market_sentiment}")
    except Exception as e:
        logger.error(f"Market test failed: {e}")
