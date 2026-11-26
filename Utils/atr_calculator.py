"""
ATR-Based Trailing Stop Calculator

Calculates optimal trailing stop percentages based on Average True Range (ATR).
This provides volatility-adjusted stop levels that respect each stock's natural
price movement patterns.

Key Features:
- 3x ATR as trailing stop (widened 2026-07-22 — 2x was killing swing thesis
  on noise. Hold-period bucketing showed <=7 day holds = 19% win rate.)
- Floor: 5% (widened from 3% — same reason)
- Ceiling: 15% (never wider than this - limits max loss)
- Uses 14-day ATR (industry standard)
- Companion rule (see trading_department.py): first 5 trading days after entry
  the stop sits at the 15% ceiling to let the swing thesis develop; on day 6
  it gets replaced with the tighter 3x ATR trailing stop.

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


# ---------------------------------------------------------------------------
# Stop parameters, 2026-08-10.
#
# These three numbers set every stop Sentinel places, and until now they lived
# only as function defaults here. risk_config.yaml had a `stop_loss:` block with
# an atr_multiplier in it that NOTHING READ — the Risk department that would
# have used it hardcodes its own 2.0 and is not in the live path at all. So the
# file said 2.0, the bot used 3.0, and a tuner pointed at the file would have
# adjusted a dead knob.
#
# They are now loaded from Config/risk_config.yaml -> trailing_stop, with the
# previous hardcoded values as fallback so behaviour is unchanged if the file
# is missing. auto_tune.py writes that block, which is what makes stop width
# genuinely tunable rather than decoratively so.
# ---------------------------------------------------------------------------
_STOP_DEFAULTS = {"atr_multiplier": 3.0, "min_stop_pct": 5.0, "max_stop_pct": 15.0}


def _load_stop_params() -> Dict:
    try:
        import yaml
        from pathlib import Path as _P
        cfg = _P(__file__).resolve().parent.parent / "Config" / "risk_config.yaml"
        block = (yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}).get("trailing_stop")
        if isinstance(block, dict):
            out = dict(_STOP_DEFAULTS)
            for k in out:
                v = block.get(k)
                if isinstance(v, (int, float)):
                    out[k] = float(v)
            return out
    except Exception:
        pass
    return dict(_STOP_DEFAULTS)


STOP_PARAMS = _load_stop_params()


def calculate_trailing_stop_percent(
    ticker: str,
    current_price: Optional[float] = None,
    atr_multiplier: Optional[float] = None,
    min_stop_pct: Optional[float] = None,
    max_stop_pct: Optional[float] = None
) -> Dict:
    """
    Calculate the optimal trailing stop percentage for a ticker based on ATR.

    Args:
        ticker: Stock symbol
        current_price: Current price (fetched if not provided)
        atr_multiplier: Multiplier for ATR. None -> Config/risk_config.yaml
            trailing_stop.atr_multiplier (3.0 if unset). Tuned by auto_tune.py.
        min_stop_pct: Floor on the stop %. None -> config (5.0 if unset).
        max_stop_pct: Ceiling on the stop %. None -> config (15.0 if unset).

    Returns:
        Dictionary with:
        - trail_percent: The calculated trailing stop percentage
        - atr_value: The ATR in dollars
        - atr_percent: The ATR as % of current price
        - current_price: The current price used
        - method: How the value was determined
    """
    # Resolve from config at call time, not import time, so a tuning change
    # takes effect on the next run without restarting anything.
    _p = _load_stop_params()
    if atr_multiplier is None:
        atr_multiplier = _p["atr_multiplier"]
    if min_stop_pct is None:
        min_stop_pct = _p["min_stop_pct"]
    if max_stop_pct is None:
        max_stop_pct = _p["max_stop_pct"]

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

    # Calculate trailing stop percentage (3x ATR — widened 2026-07-22)
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
