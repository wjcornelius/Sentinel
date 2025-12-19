"""
ATR-Based Trailing Stop Calculator

Calculates optimal trailing stop percentages based on Average True Range (ATR).
This provides volatility-adjusted stop levels that respect each stock's natural
price movement patterns.

Key Features:
- 2x ATR as trailing stop (standard risk management practice)
- Floor: 3% (never tighter than this - avoids whipsaws)
- Ceiling: 15% (never wider than this - limits max loss)
- Uses 14-day ATR (industry standard)

Why ATR-Based Stops:
- Volatile stocks (miners, crypto) need wider stops
- Stable stocks (utilities, consumer staples) can use tighter stops
- Fixed percentage stops ignore volatility = either stopped out by noise OR too loose

Example:
- HRL (Hormel - consumer staples): 1.5% daily vol -> ~3% trailing stop
- CLSK (Bitcoin miner): 7% daily vol -> ~14% trailing stop
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def calculate_atr(ticker: str, period: int = 14, days: int = 30) -> Optional[float]:
    """
    Calculate the Average True Range for a ticker.

    Args:
        ticker: Stock symbol
        period: ATR period (default 14 days)
        days: Days of historical data to fetch (default 30)

    Returns:
        ATR value in dollars, or None if calculation fails
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )

        if data.empty or len(data) < period:
            logger.warning(f"{ticker}: Insufficient data for ATR calculation")
            return None

        # Handle multi-level columns from yfinance
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Calculate True Range components
        high_low = data['High'] - data['Low']
        high_close = abs(data['High'] - data['Close'].shift(1))
        low_close = abs(data['Low'] - data['Close'].shift(1))

        # True Range is max of the three
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

        # ATR is rolling mean of True Range
        atr = tr.rolling(window=period).mean()

        # Return most recent ATR value
        atr_value = float(atr.iloc[-1])

        if pd.isna(atr_value):
            logger.warning(f"{ticker}: ATR calculation resulted in NaN")
            return None

        return atr_value

    except Exception as e:
        logger.error(f"{ticker}: ATR calculation failed - {e}")
        return None


def calculate_trailing_stop_percent(
    ticker: str,
    current_price: Optional[float] = None,
    atr_multiplier: float = 2.0,
    min_stop_pct: float = 3.0,
    max_stop_pct: float = 15.0
) -> Dict:
    """
    Calculate the optimal trailing stop percentage for a ticker based on ATR.

    Args:
        ticker: Stock symbol
        current_price: Current price (fetched if not provided)
        atr_multiplier: Multiplier for ATR (default 2.0)
        min_stop_pct: Minimum trailing stop % (floor, default 3%)
        max_stop_pct: Maximum trailing stop % (ceiling, default 15%)

    Returns:
        Dictionary with:
        - trail_percent: The calculated trailing stop percentage
        - atr_value: The ATR in dollars
        - atr_percent: The ATR as % of current price
        - current_price: The current price used
        - method: How the value was determined
    """
    result = {
        'ticker': ticker,
        'trail_percent': None,
        'atr_value': None,
        'atr_percent': None,
        'current_price': None,
        'method': None,
        'success': False
    }

    # Get current price if not provided
    if current_price is None:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1d')
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
            else:
                logger.warning(f"{ticker}: Could not fetch current price")
                result['method'] = 'fallback_default'
                result['trail_percent'] = 8.0  # Fallback to original fixed 8%
                return result
        except Exception as e:
            logger.error(f"{ticker}: Price fetch failed - {e}")
            result['method'] = 'fallback_default'
            result['trail_percent'] = 8.0
            return result

    result['current_price'] = current_price

    # Calculate ATR
    atr_value = calculate_atr(ticker)

    if atr_value is None:
        # Fallback to fixed percentage if ATR calculation fails
        result['method'] = 'fallback_default'
        result['trail_percent'] = 8.0
        logger.info(f"{ticker}: Using fallback 8% trailing stop (ATR unavailable)")
        return result

    result['atr_value'] = atr_value

    # Calculate ATR as percentage of current price
    atr_percent = (atr_value / current_price) * 100
    result['atr_percent'] = atr_percent

    # Calculate trailing stop percentage (2x ATR)
    raw_trail_pct = atr_percent * atr_multiplier

    # Apply floor and ceiling
    trail_percent = max(min_stop_pct, min(max_stop_pct, raw_trail_pct))

    result['trail_percent'] = round(trail_percent, 2)
    result['method'] = 'atr_calculated'
    result['success'] = True

    # Log the calculation
    if trail_percent == min_stop_pct:
        logger.info(f"{ticker}: Trail stop = {trail_percent}% (floor applied, raw: {raw_trail_pct:.1f}%)")
    elif trail_percent == max_stop_pct:
        logger.info(f"{ticker}: Trail stop = {trail_percent}% (ceiling applied, raw: {raw_trail_pct:.1f}%)")
    else:
        logger.info(f"{ticker}: Trail stop = {trail_percent}% (ATR: ${atr_value:.2f}, {atr_percent:.1f}% of price)")

    return result


def get_volatility_tier(ticker: str) -> Tuple[str, float]:
    """
    Classify a stock into volatility tiers for quick decision-making.

    Returns:
        Tuple of (tier_name, suggested_trail_percent)

    Tiers:
    - 'low': Stable stocks (utilities, staples) -> 5%
    - 'medium': Typical growth stocks -> 8%
    - 'high': Volatile stocks (miners, tech) -> 12%
    """
    result = calculate_trailing_stop_percent(ticker)

    if not result['success']:
        return ('medium', 8.0)  # Default to medium

    trail_pct = result['trail_percent']

    if trail_pct <= 5.0:
        return ('low', trail_pct)
    elif trail_pct <= 10.0:
        return ('medium', trail_pct)
    else:
        return ('high', trail_pct)


def analyze_current_positions(positions: list) -> Dict:
    """
    Analyze current positions and calculate optimal trailing stops for each.

    Args:
        positions: List of position dictionaries with 'ticker' and 'current_price'

    Returns:
        Dictionary mapping ticker to trailing stop analysis
    """
    analysis = {}

    for pos in positions:
        ticker = pos.get('ticker')
        current_price = pos.get('current_price')

        if ticker:
            analysis[ticker] = calculate_trailing_stop_percent(ticker, current_price)

    return analysis


if __name__ == "__main__":
    # Test with sample tickers representing different volatility levels
    logging.basicConfig(level=logging.INFO)

    test_tickers = [
        'HRL',   # Hormel - consumer staples (low vol)
        'JPM',   # JP Morgan - large cap bank (medium vol)
        'CLSK',  # CleanSpark - Bitcoin miner (high vol)
        'HL',    # Hecla Mining - silver miner (high vol)
        'CWAN',  # Clearwater Analytics (medium-high vol)
    ]

    print("\n" + "="*70)
    print("ATR-Based Trailing Stop Calculator - Test Results")
    print("="*70)
    print(f"{'Ticker':<8} {'Price':>10} {'ATR':>10} {'ATR%':>8} {'Trail%':>8} {'Tier':<8}")
    print("-"*70)

    for ticker in test_tickers:
        result = calculate_trailing_stop_percent(ticker)
        tier, _ = get_volatility_tier(ticker)

        price = f"${result['current_price']:.2f}" if result['current_price'] else "N/A"
        atr = f"${result['atr_value']:.2f}" if result['atr_value'] else "N/A"
        atr_pct = f"{result['atr_percent']:.1f}%" if result['atr_percent'] else "N/A"
        trail = f"{result['trail_percent']:.1f}%" if result['trail_percent'] else "N/A"

        print(f"{ticker:<8} {price:>10} {atr:>10} {atr_pct:>8} {trail:>8} {tier:<8}")

    print("="*70)
