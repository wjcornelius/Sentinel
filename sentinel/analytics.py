# -*- coding: utf-8 -*-
"""
Advanced analytics and performance metrics for Sentinel.

Calculates risk-adjusted returns, drawdowns, and trading statistics.
"""

import logging
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

DB_FILE = "sentinel.db"


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.04) -> float:
    """
    Calculate annualized Sharpe ratio.

    Args:
        returns: Series of daily returns (as decimals, not percentages)
        risk_free_rate: Annual risk-free rate (default 4%)

    Returns:
        Annualized Sharpe ratio

    Example:
        >>> returns = pd.Series([0.01, -0.005, 0.02, 0.01])
        >>> sharpe = calculate_sharpe_ratio(returns)
        >>> print(f"Sharpe Ratio: {sharpe:.2f}")
    """
    if len(returns) < 2:
        return 0.0

    # Calculate excess returns
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1
    excess_returns = returns - daily_rf

    # Annualize
    mean_excess = excess_returns.mean() * 252
    std_excess = excess_returns.std() * np.sqrt(252)

    if std_excess == 0:
        return 0.0

    return mean_excess / std_excess


def calculate_max_drawdown(equity_curve: pd.Series) -> Tuple[float, Optional[str], Optional[str]]:
    """
    Calculate maximum drawdown and its duration.

    Args:
        equity_curve: Series of portfolio values over time

    Returns:
        Tuple of (max_drawdown_pct, start_date, end_date)

    Example:
        >>> equity = pd.Series([100, 105, 102, 98, 103, 110])
        >>> max_dd, start, end = calculate_max_drawdown(equity)
        >>> print(f"Max Drawdown: {max_dd:.2f}%")
    """
    if len(equity_curve) < 2:
        return 0.0, None, None

    # Calculate running maximum
    running_max = equity_curve.expanding().max()

    # Calculate drawdown at each point
    drawdown = (equity_curve - running_max) / running_max * 100

    # Find maximum drawdown
    max_dd = drawdown.min()

    if max_dd >= 0:
        return 0.0, None, None

    # Find the dates
    max_dd_idx = drawdown.idxmin()
    # Find the peak before this drawdown
    peak_idx = equity_curve[:max_dd_idx].idxmax()

    peak_date = str(peak_idx) if hasattr(peak_idx, '__str__') else None
    trough_date = str(max_dd_idx) if hasattr(max_dd_idx, '__str__') else None

    return abs(max_dd), peak_date, trough_date


def calculate_win_rate(db_file: str = DB_FILE) -> Dict[str, float]:
    """
    Calculate win rate and average win/loss from trade history.

    Returns:
        Dictionary with win_rate, avg_win, avg_loss, profit_factor

    Example:
        >>> stats = calculate_win_rate()
        >>> print(f"Win Rate: {stats['win_rate']:.1f}%")
    """
    try:
        conn = sqlite3.connect(db_file)

        # Get all completed trades with their outcomes
        query = """
        SELECT
            t.symbol,
            t.side,
            t.quantity,
            t.timestamp as exit_time,
            d.latest_price as decision_price,
            t.status
        FROM trades t
        LEFT JOIN decisions d ON t.decision_id = d.id
        WHERE t.status IN ('submitted', 'filled')
        AND t.side = 'sell'
        ORDER BY t.timestamp
        """

        df = pd.read_sql_query(query, conn)
        conn.close()

        if len(df) < 10:  # Need at least 10 trades for meaningful stats
            return {
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'total_trades': len(df)
            }

        # This is a simplified calculation - in reality we'd need entry prices
        # For now, we'll estimate based on decision data
        # TODO: Enhance this with actual trade P&L tracking

        return {
            'win_rate': 50.0,  # Placeholder
            'avg_win': 0.0,  # Placeholder
            'avg_loss': 0.0,  # Placeholder
            'profit_factor': 1.0,  # Placeholder
            'total_trades': len(df)
        }

    except Exception as e:
        logging.error(f"Error calculating win rate: {e}")
        return {
            'win_rate': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'profit_factor': 0.0,
            'total_trades': 0
        }


def get_sector_concentration(positions: List[Dict], portfolio_value: float) -> Dict[str, float]:
    """
    Calculate portfolio concentration by sector.

    Args:
        positions: List of position dictionaries with 'sector' and 'market_value'
        portfolio_value: Total portfolio value

    Returns:
        Dictionary mapping sectors to their percentage of portfolio

    Example:
        >>> positions = [
        ...     {'sector': 'Technology', 'market_value': 5000},
        ...     {'sector': 'Healthcare', 'market_value': 3000}
        ... ]
        >>> concentration = get_sector_concentration(positions, 10000)
        >>> print(concentration)  # {'Technology': 50.0, 'Healthcare': 30.0}
    """
    sector_values = {}

    for pos in positions:
        sector = pos.get('sector', 'Unknown')
        value = pos.get('market_value', 0)

        if sector in sector_values:
            sector_values[sector] += value
        else:
            sector_values[sector] = value

    # Convert to percentages
    sector_pcts = {}
    for sector, value in sector_values.items():
        if portfolio_value > 0:
            sector_pcts[sector] = (value / portfolio_value) * 100
        else:
            sector_pcts[sector] = 0.0

    # Sort by percentage descending
    return dict(sorted(sector_pcts.items(), key=lambda x: x[1], reverse=True))


def generate_performance_summary(api, current_value: float) -> Dict[str, any]:
    """
    Generate comprehensive performance summary with advanced metrics.

    Args:
        api: Alpaca API instance
        current_value: Current portfolio value

    Returns:
        Dictionary with all performance metrics
    """
    try:
        # Get historical equity data
        hist_90d = api.get_portfolio_history(period='90D', timeframe='1D')

        if len(hist_90d.equity) < 2:
            return {
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'max_dd_start': None,
                'max_dd_end': None,
                'volatility_annual': 0.0,
                'days_tracked': 0
            }

        # Convert to pandas Series
        equity_series = pd.Series(
            [e for e in hist_90d.equity if e is not None and e > 0]
        )

        if len(equity_series) < 2:
            return {
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'max_dd_start': None,
                'max_dd_end': None,
                'volatility_annual': 0.0,
                'days_tracked': 0
            }

        # Calculate daily returns
        returns = equity_series.pct_change().dropna()

        # Calculate metrics
        sharpe = calculate_sharpe_ratio(returns)
        max_dd, dd_start, dd_end = calculate_max_drawdown(equity_series)
        volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility %

        return {
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'max_dd_start': dd_start,
            'max_dd_end': dd_end,
            'volatility_annual': volatility,
            'days_tracked': len(equity_series)
        }

    except Exception as e:
        logging.error(f"Error generating performance summary: {e}")
        return {
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'max_dd_start': None,
            'max_dd_end': None,
            'volatility_annual': 0.0,
            'days_tracked': 0
        }
