# -*- coding: utf-8 -*-
"""
Helper functions and utilities for Sentinel.

Includes mathematical helpers, data processing utilities, and decorators.
"""

import logging
import math
import time
from functools import wraps
from typing import Optional, Callable, Tuple

# Constants
MAX_API_RETRIES = 3
API_RETRY_DELAY = 2  # seconds
CONVICTION_WEIGHT_EXP = 1.6  # Exponential weight for conviction scoring
MIN_WEIGHT_FLOOR = 0.05  # Minimum allocation weight


def retry_on_failure(
    max_retries: int = MAX_API_RETRIES,
    delay: float = API_RETRY_DELAY,
    exceptions: Tuple = (Exception,)
) -> Callable:
    """
    Decorator to retry a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Base delay in seconds between retries (doubles with each retry)
        exceptions: Tuple of exception types to catch and retry on

    Returns:
        Decorated function that retries on failure

    Example:
        @retry_on_failure(max_retries=3, delay=2)
        def fetch_data():
            return api.get_data()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logging.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= 2  # Exponential backoff
                    else:
                        logging.error(
                            f"{func.__name__} failed after {max_retries} attempts: {e}",
                            exc_info=True
                        )

            # If we get here, all retries failed
            raise last_exception

        return wrapper
    return decorator


def sanitize_conviction(raw_value) -> int:
    """
    Ensure conviction score is an integer between 1 and 10.

    Args:
        raw_value: Raw conviction value (can be int, float, or string)

    Returns:
        Sanitized conviction score between 1 and 10

    Example:
        >>> sanitize_conviction(7.8)
        8
        >>> sanitize_conviction(15)
        10
        >>> sanitize_conviction("invalid")
        5
    """
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return 5  # Default to neutral conviction if invalid
    value = max(1, min(10, value))
    return int(round(value))


def conviction_to_weight(conviction: int) -> float:
    """
    Convert conviction score (1-10) to allocation weight using exponential scaling.

    Higher conviction scores receive disproportionately higher weights to
    concentrate capital in the best opportunities.

    Args:
        conviction: Integer conviction score between 1 and 10

    Returns:
        Weight value (minimum MIN_WEIGHT_FLOOR, maximum 1.0)

    Example:
        >>> conviction_to_weight(10)  # Max conviction
        1.0
        >>> conviction_to_weight(5)   # Mid conviction
        ~0.32
        >>> conviction_to_weight(1)   # Min conviction
        0.05 (floor)
    """
    normalized = max(1, min(10, conviction)) / 10.0
    weight = normalized ** CONVICTION_WEIGHT_EXP
    return max(MIN_WEIGHT_FLOOR, weight)


def floor_to_precision(value: float, decimals: int = 6) -> float:
    """
    Floor a value to specified decimal precision with epsilon adjustment.

    Used to ensure order quantities don't exceed available shares due to
    floating-point precision issues.

    Args:
        value: Value to floor
        decimals: Number of decimal places

    Returns:
        Floored value with epsilon adjustment

    Example:
        >>> floor_to_precision(1.9999999, 6)
        1.999999  # Slightly below to avoid rounding up
    """
    if value <= 0:
        return 0.0
    factor = 10 ** decimals
    floored = math.floor(value * factor) / factor
    epsilon = 1 / factor
    if floored > 0:
        floored = max(0.0, floored - epsilon)
    return max(0.0, floored)


def calculate_rsi(series, period: int = 14) -> Optional[float]:
    """
    Calculate Relative Strength Index (RSI) for a price series.

    RSI is a momentum oscillator that measures the speed and magnitude of
    price changes, ranging from 0 to 100.

    Args:
        series: Pandas Series of prices
        period: Lookback period (typically 14)

    Returns:
        RSI value (0-100), or None if insufficient data

    Example:
        >>> rsi = calculate_rsi(price_series, period=14)
        >>> if rsi > 70:
        ...     print("Overbought")
    """
    if series is None or len(series) < period + 1:
        return None

    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    if avg_loss.iloc[-1] == 0:
        return 100.0  # All gains, no losses

    rs = avg_gain.iloc[-1] / avg_loss.iloc[-1]
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)


def compute_pct_change(series, periods: int) -> Optional[float]:
    """
    Calculate percentage change over specified number of periods.

    Args:
        series: Pandas Series of values
        periods: Number of periods to look back

    Returns:
        Percentage change as float, or None if insufficient data

    Example:
        >>> change_20d = compute_pct_change(close_prices, 20)
        >>> print(f"20-day return: {change_20d:.2f}%")
    """
    if len(series) <= periods:
        return None

    start = series.iloc[-periods - 1]
    end = series.iloc[-1]

    if start == 0:
        return None

    return float((end - start) / start * 100)
