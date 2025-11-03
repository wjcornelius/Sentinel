"""
Research Department v2.0 - Programmatic Technical Analysis Only

Phase 1 Redesign:
- NO AI involvement (pure programmatic analysis)
- Adaptive technical filtering to find ~50 buy candidates
- Fetch current holdings from Alpaca (ground truth)
- 16-hour cache for all price/volume data
- Output: ~110 stocks (50 candidates + 60 holdings)
- Sentiment scores = 50 (placeholder for News Department)

Key Changes from v1:
- Removed Perplexity API calls
- Added adaptive filter iteration
- Added Alpaca integration
- Simplified scoring (technical + fundamental only)
"""

import logging
import sqlite3
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class ResearchDepartment:
    """
    Research Department - Programmatic Stock Analysis

    Responsibilities:
    1. Load universe from ticker_universe.txt (user-editable)
    2. Get current holdings from Alpaca (ground truth)
    3. Apply adaptive technical filters → ~50 buy candidates
    4. Score all ~110 stocks (technical + fundamental, NO sentiment)
    5. Output Daily Candidate Universe for downstream departments
    """

    def __init__(self, db_path: str = "sentinel.db", alpaca_client=None):
        """
        Initialize Research Department

        Args:
            db_path: Path to SQLite database (for caching)
            alpaca_client: Alpaca API client (for current holdings)
        """
        self.db_path = db_path
        self.alpaca = alpaca_client
        self.cache_ttl_hours = 16
        self.universe_file = "ticker_universe.txt"

        self._initialize_cache()
        logger.info("Research Department v2.0 initialized (programmatic only, no AI)")

    def _initialize_cache(self):
        """Create cache table for price/volume data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data_cache (
                ticker TEXT,
                data_type TEXT,
                data_json TEXT,
                fetched_at TEXT,
                expires_at TEXT,
                PRIMARY KEY (ticker, data_type)
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Market data cache ready (16-hour TTL)")

    def generate_daily_candidate_universe(self) -> Dict:
        """
        Generate Daily Candidate Universe

        Returns:
            {
                'current_holdings': [...],  # From Alpaca
                'buy_candidates': [...],     # From filtering
                'total_count': int,
                'market_conditions': {...}
            }
        """
        logger.info("=" * 80)
        logger.info("GENERATING DAILY CANDIDATE UNIVERSE")
        logger.info("=" * 80)

        # Step 1: Load universe
        universe_tickers = self._load_universe()
        logger.info(f"Universe loaded: {len(universe_tickers)} tickers")

        # Step 2: Get current holdings from Alpaca
        current_holdings = self._get_current_holdings()
        logger.info(f"Current portfolio: {len(current_holdings)} positions")

        # Step 3: Filter to ~50 buy candidates
        buy_candidates = self._adaptive_filter(
            universe_tickers,
            target_count=50,
            exclude=[h['ticker'] for h in current_holdings]
        )
        logger.info(f"Buy candidates found: {len(buy_candidates)} tickers")

        # Step 4: Score all stocks (programmatic only)
        scored_holdings = self._score_stocks(current_holdings, context='holdings')
        scored_candidates = self._score_stocks(buy_candidates, context='new_buys')

        # Step 5: Get market conditions
        market_conditions = self._get_market_conditions()

        universe = {
            'current_holdings': scored_holdings,
            'buy_candidates': scored_candidates,
            'total_count': len(scored_holdings) + len(scored_candidates),
            'market_conditions': market_conditions,
            'generated_at': datetime.now().isoformat()
        }

        logger.info(f"Daily Candidate Universe complete: {universe['total_count']} stocks")
        logger.info(f"  - Holdings: {len(scored_holdings)}")
        logger.info(f"  - Candidates: {len(scored_candidates)}")

        return universe

    def _load_universe(self) -> List[str]:
        """Load ticker universe from file"""
        universe_path = Path(self.universe_file)

        if not universe_path.exists():
            logger.warning(f"{self.universe_file} not found - using default S&P500+Nasdaq100")
            # Fallback to hardcoded universe (you can edit later)
            return self._get_default_universe()

        with open(universe_path, 'r') as f:
            tickers = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        return tickers

    def _get_default_universe(self) -> List[str]:
        """Default universe if file doesn't exist"""
        # Read from existing ticker_universe.txt
        try:
            with open('ticker_universe.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    def _get_current_holdings(self) -> List[Dict]:
        """
        Get current portfolio positions from Alpaca (GROUND TRUTH)

        Returns:
            List of holdings: [{'ticker': 'AAPL', 'qty': 10, 'value': 2000}, ...]
        """
        if not self.alpaca:
            logger.warning("No Alpaca client - returning empty holdings")
            return []

        try:
            positions = self.alpaca.get_all_positions()

            holdings = []
            for pos in positions:
                holdings.append({
                    'ticker': pos.symbol,
                    'qty': float(pos.qty),
                    'value': float(pos.market_value),
                    'current_price': float(pos.current_price),
                    'cost_basis': float(pos.cost_basis),
                    'unrealized_pl': float(pos.unrealized_pl)
                })

            logger.info(f"Fetched {len(holdings)} positions from Alpaca")
            return holdings

        except Exception as e:
            logger.error(f"Failed to fetch Alpaca positions: {e}")
            return []

    def _adaptive_filter(self, universe: List[str], target_count: int = 50,
                        exclude: List[str] = None) -> List[str]:
        """
        Adaptively filter universe to ~target_count candidates
        Iterates through filter presets (strict → loose) until target reached

        Args:
            universe: List of all tickers
            target_count: Target number of candidates
            exclude: Tickers to exclude (current holdings)

        Returns:
            List of ~target_count tickers
        """
        exclude = exclude or []

        # Filter presets (strict → loose)
        presets = [
            {'name': 'VERY_STRICT', 'rsi': (30, 45), 'volume_min': 2000000, 'price_min': 20},
            {'name': 'STRICT', 'rsi': (25, 50), 'volume_min': 1000000, 'price_min': 10},
            {'name': 'MODERATE', 'rsi': (20, 60), 'volume_min': 500000, 'price_min': 5},
            {'name': 'RELAXED', 'rsi': (15, 70), 'volume_min': 250000, 'price_min': 2},
            {'name': 'VERY_RELAXED', 'rsi': (10, 80), 'volume_min': 100000, 'price_min': 1},
        ]

        for preset in presets:
            logger.info(f"Trying filter preset: {preset['name']}")

            candidates = []
            for ticker in universe:
                if ticker in exclude:
                    continue

                # Get cached data
                data = self._get_cached_price_data(ticker)
                if data is None or len(data) < 20:
                    continue

                # Apply filters
                if self._passes_filters(data, preset):
                    candidates.append(ticker)

            logger.info(f"  → Found {len(candidates)} candidates")

            # Check if close to target
            target_min = int(target_count * 0.8)  # 40 if target=50
            target_max = int(target_count * 1.2)  # 60 if target=50

            if target_min <= len(candidates) <= target_max:
                logger.info(f"✓ Target reached with {preset['name']} preset")
                return candidates[:target_count]  # Cap at exact target

            if len(candidates) < target_min and preset['name'] == 'VERY_RELAXED':
                logger.warning(f"Even loosest filters only found {len(candidates)} - using what we have")
                return candidates

        return candidates[:target_count]

    def _passes_filters(self, data: pd.DataFrame, preset: Dict) -> bool:
        """
        Apply technical filters to stock data

        Args:
            data: Price/volume DataFrame
            preset: Filter parameters

        Returns:
            True if passes all filters
        """
        try:
            # Price filter
            current_price = data['Close'].iloc[-1]
            if current_price < preset['price_min']:
                return False

            # Volume filter
            avg_volume = data['Volume'].mean()
            if avg_volume < preset['volume_min']:
                return False

            # RSI filter
            rsi = self._calculate_rsi(data)
            if not (preset['rsi'][0] <= rsi <= preset['rsi'][1]):
                return False

            return True

        except Exception as e:
            logger.debug(f"Filter check failed: {e}")
            return False

    def _get_cached_price_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Get price/volume data from cache or fetch if stale

        Args:
            ticker: Stock ticker

        Returns:
            DataFrame with OHLCV data or None if failed
        """
        # Check cache
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now()
        cursor.execute("""
            SELECT data_json, fetched_at
            FROM market_data_cache
            WHERE ticker = ? AND data_type = 'price_data' AND expires_at > ?
        """, (ticker, now.isoformat()))

        row = cursor.fetchone()
        conn.close()

        if row:
            # Cache hit
            import json
            data_dict = json.loads(row[0])
            df = pd.DataFrame(data_dict)
            logger.debug(f"{ticker}: Cache hit")
            return df

        # Cache miss - fetch from yfinance
        try:
            logger.debug(f"{ticker}: Fetching from yfinance")
            data = yf.download(ticker, period='60d', progress=False)

            if data.empty:
                return None

            # Cache for 16 hours
            self._cache_price_data(ticker, data)

            return data

        except Exception as e:
            logger.debug(f"{ticker}: Failed to fetch - {e}")
            return None

    def _cache_price_data(self, ticker: str, data: pd.DataFrame):
        """Cache price data with 16-hour TTL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now()
        expires_at = now + timedelta(hours=self.cache_ttl_hours)

        # Convert DataFrame to JSON
        import json
        data_json = json.dumps(data.reset_index().to_dict(orient='records'))

        cursor.execute("""
            INSERT OR REPLACE INTO market_data_cache
            (ticker, data_type, data_json, fetched_at, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (ticker, 'price_data', data_json, now.isoformat(), expires_at.isoformat()))

        conn.commit()
        conn.close()

    def _score_stocks(self, tickers: List, context: str) -> List[Dict]:
        """
        Score stocks using programmatic analysis only

        Args:
            tickers: List of tickers (or dicts with ticker key)
            context: 'holdings' or 'new_buys'

        Returns:
            List of scored candidates
        """
        scored = []

        for item in tickers:
            # Handle both string tickers and dict objects
            ticker = item if isinstance(item, str) else item.get('ticker')

            data = self._get_cached_price_data(ticker)
            if data is None:
                continue

            # Technical score
            tech_score = self._calculate_technical_score(data)

            # Fundamental score (simplified)
            fund_score = 50.0  # Placeholder - implement if needed

            # Sentiment = 50 (placeholder for News Dept)
            sent_score = 50.0

            # Composite
            composite = (tech_score * 0.4) + (fund_score * 0.4) + (sent_score * 0.2)

            scored.append({
                'ticker': ticker,
                'technical_score': tech_score,
                'fundamental_score': fund_score,
                'sentiment_score': sent_score,
                'research_composite_score': composite,
                'context': context,
                'current_price': float(data['Close'].iloc[-1]),
                'sector': 'Unknown'  # Fetch if needed
            })

        return scored

    def _calculate_technical_score(self, data: pd.DataFrame) -> float:
        """Calculate technical score (0-100) from price data"""
        score = 0.0

        try:
            # RSI component (0-30 points)
            rsi = self._calculate_rsi(data)
            if 30 <= rsi <= 70:
                score += 30
            elif 20 <= rsi < 30 or 70 < rsi <= 80:
                score += 20
            else:
                score += 10

            # MACD component (0-30 points)
            macd_signal = self._calculate_macd(data)
            if macd_signal == 'BULLISH':
                score += 30
            elif macd_signal == 'NEUTRAL':
                score += 15

            # Trend component (0-40 points)
            sma_20 = data['Close'].rolling(20).mean().iloc[-1]
            sma_50 = data['Close'].rolling(50).mean().iloc[-1] if len(data) >= 50 else sma_20
            current = data['Close'].iloc[-1]

            if current > sma_20 > sma_50:
                score += 40  # Strong uptrend
            elif current > sma_20:
                score += 25  # Moderate uptrend
            elif current > sma_50:
                score += 15

        except Exception as e:
            logger.debug(f"Technical score calculation failed: {e}")
            score = 50.0  # Default neutral

        return min(100.0, max(0.0, score))

    def _calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate RSI indicator"""
        try:
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return float(rsi.iloc[-1])
        except:
            return 50.0

    def _calculate_macd(self, data: pd.DataFrame) -> str:
        """Calculate MACD signal"""
        try:
            ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()

            if macd_line.iloc[-1] > signal_line.iloc[-1]:
                return 'BULLISH'
            elif macd_line.iloc[-1] < signal_line.iloc[-1]:
                return 'BEARISH'
            else:
                return 'NEUTRAL'
        except:
            return 'NEUTRAL'

    def _get_market_conditions(self) -> Dict:
        """Get current market conditions (SPY, VIX, etc.)"""
        try:
            spy_data = yf.download('SPY', period='5d', progress=False)
            spy_change = ((spy_data['Close'].iloc[-1] / spy_data['Close'].iloc[-2]) - 1) * 100

            vix_data = yf.download('^VIX', period='5d', progress=False)
            vix_level = float(vix_data['Close'].iloc[-1])

            if vix_level < 15:
                vix_status = 'LOW'
            elif vix_level < 20:
                vix_status = 'NORMAL'
            elif vix_level < 30:
                vix_status = 'ELEVATED'
            else:
                vix_status = 'HIGH'

            return {
                'spy_change_pct': float(spy_change),
                'vix': vix_level,
                'vix_status': vix_status,
                'date': datetime.now().date().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to fetch market conditions: {e}")
            return {
                'spy_change_pct': 0.0,
                'vix': 20.0,
                'vix_status': 'UNKNOWN',
                'date': datetime.now().date().isoformat()
            }
