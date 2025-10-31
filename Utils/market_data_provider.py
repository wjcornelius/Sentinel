"""
Market Data Provider - Week 7 Day 1
Provides real-time and historical market data via yfinance API

Features:
- Current price fetching with retry logic
- Historical price data for technical analysis
- Stock fundamentals (sector, market cap, PE ratio)
- Benchmark data (SPY, QQQ) for performance comparison
- Circuit breaker pattern for API failure handling
- Caching to reduce API calls

Author: Claude Code (CC)
Week: 7 Day 1
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import wraps
from pathlib import Path
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def retry_on_failure(max_retries: int = 3, delay: float = 2.0):
    """
    Decorator for retrying failed API calls

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay in seconds between retries
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        # Last attempt failed, re-raise
                        raise
                    logging.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern to prevent cascading failures

    States:
    - CLOSED: Normal operation
    - OPEN: Too many failures, stop calling
    - HALF_OPEN: Testing if service recovered
    """

    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
        self.logger = logging.getLogger(self.__class__.__name__)

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""

        # If circuit is open, check if timeout expired
        if self.state == 'OPEN':
            if self.last_failure_time and datetime.now() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
                self.logger.info("Circuit breaker entering HALF_OPEN state (testing recovery)")
            else:
                raise Exception(f"Circuit breaker is OPEN - service unavailable (failures: {self.failure_count})")

        try:
            result = func(*args, **kwargs)
            # Success - reset circuit
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
                self.logger.info("Circuit breaker returning to CLOSED state (service recovered)")
            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
                self.logger.error(f"Circuit breaker entering OPEN state after {self.failure_count} failures")

            raise e


class MarketDataProvider:
    """
    Fetches real-time and historical market data from Yahoo Finance

    Features:
    - Current prices with retry logic
    - Historical OHLCV data
    - Stock fundamentals (sector, market cap, etc.)
    - Benchmark performance (SPY, QQQ)
    - Local caching to reduce API calls
    - Circuit breaker for API failures
    """

    def __init__(self, cache_dir: Path = None, enable_cache: bool = True):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.enable_cache = enable_cache

        # Setup cache directory
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "Cache" / "MarketData"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Circuit breakers for different API endpoints
        self.price_breaker = CircuitBreaker(failure_threshold=5, timeout_seconds=60)
        self.history_breaker = CircuitBreaker(failure_threshold=5, timeout_seconds=60)

        self.logger.info(f"MarketDataProvider initialized: cache={enable_cache}, cache_dir={cache_dir}")

    @retry_on_failure(max_retries=3, delay=2.0)
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get current stock price

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            Current price or None if unavailable
        """
        try:
            # Check cache first (5-minute expiry for current prices)
            cached_price = self._get_cached_price(ticker, expiry_minutes=5)
            if cached_price is not None:
                return cached_price

            # Fetch from yfinance with circuit breaker
            price = self.price_breaker.call(self._fetch_current_price, ticker)

            # Cache the result
            if price is not None:
                self._cache_price(ticker, price)

            return price

        except Exception as e:
            self.logger.error(f"Failed to get current price for {ticker}: {e}")
            return None

    def _fetch_current_price(self, ticker: str) -> Optional[float]:
        """Internal method to fetch price from yfinance"""
        stock = yf.Ticker(ticker)

        # Try fast_info first (faster but may be unavailable)
        try:
            if hasattr(stock, 'fast_info') and hasattr(stock.fast_info, 'last_price'):
                price = stock.fast_info.last_price
                if price and not np.isnan(price):
                    self.logger.debug(f"Got price for {ticker}: ${price:.2f} (fast_info)")
                    return float(price)
        except:
            pass

        # Fallback to history (1 day)
        hist = stock.history(period="1d")
        if not hist.empty and 'Close' in hist.columns:
            price = hist['Close'].iloc[-1]
            self.logger.debug(f"Got price for {ticker}: ${price:.2f} (history)")
            return float(price)

        self.logger.warning(f"Could not fetch price for {ticker}")
        return None

    @retry_on_failure(max_retries=3, delay=2.0)
    def get_historical_prices(self, ticker: str, start_date: datetime = None,
                             end_date: datetime = None, period: str = "1mo") -> pd.DataFrame:
        """
        Get historical OHLCV data

        Args:
            ticker: Stock ticker symbol
            start_date: Start date for historical data
            end_date: End date for historical data (defaults to today)
            period: Period string if start_date not provided ("1mo", "3mo", "1y", etc.)

        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume
        """
        try:
            # Check cache (1-hour expiry for historical data)
            cache_key = f"{ticker}_{period}" if start_date is None else f"{ticker}_{start_date}_{end_date}"
            cached_data = self._get_cached_history(cache_key, expiry_minutes=60)
            if cached_data is not None:
                return cached_data

            # Fetch from yfinance with circuit breaker
            data = self.history_breaker.call(self._fetch_historical_prices, ticker, start_date, end_date, period)

            # Cache the result
            if data is not None and not data.empty:
                self._cache_history(cache_key, data)

            return data

        except Exception as e:
            self.logger.error(f"Failed to get historical data for {ticker}: {e}")
            return pd.DataFrame()

    def _fetch_historical_prices(self, ticker: str, start_date: datetime = None,
                                 end_date: datetime = None, period: str = "1mo") -> pd.DataFrame:
        """Internal method to fetch history from yfinance"""
        stock = yf.Ticker(ticker)

        if start_date is not None:
            if end_date is None:
                end_date = datetime.now()
            hist = stock.history(start=start_date, end=end_date)
        else:
            hist = stock.history(period=period)

        if not hist.empty:
            self.logger.debug(f"Got {len(hist)} days of history for {ticker}")

        return hist

    def get_stock_info(self, ticker: str) -> Dict:
        """
        Get stock fundamentals and info

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with sector, industry, market_cap, pe_ratio, etc.
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'ticker': ticker,
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', None),
                'forward_pe': info.get('forwardPE', None),
                'dividend_yield': info.get('dividendYield', None),
                'beta': info.get('beta', None),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', None),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', None),
                'avg_volume': info.get('averageVolume', None)
            }

        except Exception as e:
            self.logger.error(f"Failed to get info for {ticker}: {e}")
            return {'ticker': ticker, 'sector': 'Unknown', 'industry': 'Unknown'}

    def get_benchmark_return(self, benchmark: str = 'SPY', start_date: datetime = None,
                            end_date: datetime = None, period_days: int = 30) -> Tuple[float, Dict]:
        """
        Get benchmark return for comparison

        Args:
            benchmark: Benchmark ticker (SPY or QQQ)
            start_date: Start date for return calculation
            end_date: End date (defaults to today)
            period_days: Number of days if start_date not provided

        Returns:
            Tuple of (return_pct, details_dict)
        """
        try:
            if end_date is None:
                end_date = datetime.now()

            if start_date is None:
                start_date = end_date - timedelta(days=period_days)

            # Get historical data
            hist = self.get_historical_prices(benchmark, start_date=start_date, end_date=end_date)

            if hist.empty or len(hist) < 2:
                self.logger.warning(f"Insufficient data for {benchmark} benchmark calculation")
                return 0.0, {'error': 'Insufficient data'}

            # Calculate return
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            return_pct = ((end_price - start_price) / start_price) * 100

            self.logger.info(f"Benchmark {benchmark}: {return_pct:.2f}% over {len(hist)} days")

            return return_pct, {
                'benchmark': benchmark,
                'start_date': str(hist.index[0].date()),
                'end_date': str(hist.index[-1].date()),
                'start_price': float(start_price),
                'end_price': float(end_price),
                'return_pct': float(return_pct),
                'days': len(hist)
            }

        except Exception as e:
            self.logger.error(f"Failed to get benchmark return for {benchmark}: {e}")
            return 0.0, {'error': str(e)}

    # ========================================================================
    # CACHING METHODS
    # ========================================================================

    def _get_cached_price(self, ticker: str, expiry_minutes: int = 5) -> Optional[float]:
        """Get cached current price if not expired"""
        if not self.enable_cache:
            return None

        cache_file = self.cache_dir / f"price_{ticker}.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)

            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time < timedelta(minutes=expiry_minutes):
                self.logger.debug(f"Using cached price for {ticker}: ${data['price']:.2f}")
                return data['price']
        except:
            pass

        return None

    def _cache_price(self, ticker: str, price: float):
        """Cache current price"""
        if not self.enable_cache:
            return

        cache_file = self.cache_dir / f"price_{ticker}.json"
        data = {
            'ticker': ticker,
            'price': price,
            'timestamp': datetime.now().isoformat()
        }

        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            self.logger.warning(f"Failed to cache price for {ticker}: {e}")

    def _get_cached_history(self, cache_key: str, expiry_minutes: int = 60) -> Optional[pd.DataFrame]:
        """Get cached historical data if not expired"""
        if not self.enable_cache:
            return None

        cache_file = self.cache_dir / f"history_{cache_key}.parquet"
        if not cache_file.exists():
            return None

        try:
            # Check file modification time
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - file_time < timedelta(minutes=expiry_minutes):
                data = pd.read_parquet(cache_file)
                self.logger.debug(f"Using cached history for {cache_key}: {len(data)} rows")
                return data
        except:
            pass

        return None

    def _cache_history(self, cache_key: str, data: pd.DataFrame):
        """Cache historical data"""
        if not self.enable_cache:
            return

        cache_file = self.cache_dir / f"history_{cache_key}.parquet"

        try:
            data.to_parquet(cache_file)
        except Exception as e:
            # Fallback to CSV if parquet fails
            try:
                csv_file = self.cache_dir / f"history_{cache_key}.csv"
                data.to_csv(csv_file)
            except:
                self.logger.warning(f"Failed to cache history for {cache_key}: {e}")


# Quick test
if __name__ == "__main__":
    print("Testing MarketDataProvider...")

    provider = MarketDataProvider(enable_cache=True)

    # Test 1: Get current price
    print("\n[TEST 1] Get Current Price")
    print("-" * 80)
    for ticker in ['AAPL', 'MSFT', 'GOOGL']:
        price = provider.get_current_price(ticker)
        print(f"  {ticker}: ${price:.2f}" if price else f"  {ticker}: N/A")

    # Test 2: Get historical data
    print("\n[TEST 2] Get Historical Data")
    print("-" * 80)
    hist = provider.get_historical_prices('AAPL', period='1mo')
    print(f"  AAPL: {len(hist)} days of data")
    if not hist.empty:
        print(f"  Latest close: ${hist['Close'].iloc[-1]:.2f}")
        print(f"  30-day return: {((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100):.2f}%")

    # Test 3: Get stock info
    print("\n[TEST 3] Get Stock Info")
    print("-" * 80)
    info = provider.get_stock_info('AAPL')
    print(f"  Sector: {info['sector']}")
    print(f"  Market Cap: ${info['market_cap']:,}" if info['market_cap'] else "  Market Cap: N/A")
    print(f"  P/E Ratio: {info['pe_ratio']:.2f}" if info['pe_ratio'] else "  P/E Ratio: N/A")

    # Test 4: Get benchmark return
    print("\n[TEST 4] Get Benchmark Return")
    print("-" * 80)
    spy_return, spy_details = provider.get_benchmark_return('SPY', period_days=30)
    print(f"  SPY 30-day return: {spy_return:.2f}%")
    print(f"  Days: {spy_details.get('days', 'N/A')}")

    print("\n" + "=" * 80)
    print("MarketDataProvider tests complete!")
    print("=" * 80)
