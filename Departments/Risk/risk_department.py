"""
Risk Department - Position Sizing, Stop-Loss Calculation, Portfolio Risk Management
Built fresh from C(P) Week 3 guidance + DEPARTMENTAL_SPECIFICATIONS v1.0

Responsibilities:
- Calculate position sizes (Fixed Fractional, Kelly Criterion future)
- Calculate stop-loss levels (ATR-based, Percentage fallback)
- Validate risk per trade (max 1% of capital)
- Monitor portfolio heat (max 5% total risk)
- Check sector concentration (max 40% per sector)
- Generate RiskAssessment messages for Portfolio Department

Pattern: Message-based architecture (same as Research/Trading Departments)
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
from datetime import datetime, timedelta, date, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('RiskDepartment')


class PositionSizer:
    """
    Calculates position sizes based on configured method
    Phase 1: Fixed Fractional (10% of capital per position)
    Future: Kelly Criterion, Volatility-Adjusted
    """

    def __init__(self, config: Dict):
        """
        Initialize Position Sizer

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.method = config['position_sizing']['method']
        self.position_size_pct = config['position_sizing']['position_size_pct']

        logger.info(f"PositionSizer initialized (method: {self.method}, size: {self.position_size_pct*100:.0f}%)")

    def calculate_position_size(self, capital: float, current_price: float, ticker: str) -> Dict:
        """
        Calculate position size for a stock

        Args:
            capital: Total capital available
            current_price: Current stock price
            ticker: Stock symbol

        Returns:
            Dictionary with position size details
        """
        try:
            if self.method == "FIXED_FRACTIONAL":
                return self._fixed_fractional(capital, current_price, ticker)
            else:
                logger.error(f"Unknown position sizing method: {self.method}")
                return None

        except Exception as e:
            logger.error(f"Position sizing failed for {ticker}: {e}", exc_info=True)
            return None

    def _fixed_fractional(self, capital: float, current_price: float, ticker: str) -> Dict:
        """
        Fixed Fractional position sizing: Use fixed % of capital per position

        Args:
            capital: Total capital available
            current_price: Current stock price
            ticker: Stock symbol

        Returns:
            Position size details
        """
        # Calculate position value (e.g., $100K × 10% = $10K)
        position_value = capital * self.position_size_pct

        # Calculate number of shares (round down to avoid exceeding position size)
        shares = int(position_value / current_price)

        # Actual position value (may be slightly less due to rounding)
        actual_position_value = shares * current_price

        # Actual position percentage
        actual_position_pct = actual_position_value / capital if capital > 0 else 0

        result = {
            'method': 'FIXED_FRACTIONAL',
            'ticker': ticker,
            'capital': capital,
            'current_price': current_price,
            'target_position_pct': self.position_size_pct,
            'target_position_value': position_value,
            'shares': shares,
            'actual_position_value': actual_position_value,
            'actual_position_pct': actual_position_pct
        }

        logger.info(f"Position size for {ticker}: {shares} shares @ ${current_price:.2f} = ${actual_position_value:,.0f} ({actual_position_pct*100:.1f}% of capital)")

        return result


class StopLossCalculator:
    """
    Calculates stop-loss levels based on configured method
    Phase 1: ATR-based (2× 14-day ATR), Percentage fallback
    Future: Support-based, Volatility-adjusted
    """

    def __init__(self, config: Dict):
        """
        Initialize Stop-Loss Calculator

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.method = config['stop_loss']['method']
        self.atr_period = config['stop_loss']['atr_period']
        self.atr_multiplier = config['stop_loss']['atr_multiplier']
        self.percentage_stop = config['stop_loss']['percentage_stop']
        self.min_stop_pct = config['stop_loss']['min_stop_distance_pct']
        self.max_stop_pct = config['stop_loss']['max_stop_distance_pct']

        logger.info(f"StopLossCalculator initialized (method: {self.method}, ATR: {self.atr_period}d × {self.atr_multiplier})")

    def calculate_stop_loss(self, ticker: str, entry_price: float) -> Dict:
        """
        Calculate stop-loss level for a stock

        Args:
            ticker: Stock symbol
            entry_price: Entry price for position

        Returns:
            Dictionary with stop-loss details
        """
        try:
            if self.method == "ATR_BASED":
                return self._atr_based_stop(ticker, entry_price)
            elif self.method == "PERCENTAGE":
                return self._percentage_stop(ticker, entry_price)
            else:
                logger.error(f"Unknown stop-loss method: {self.method}")
                return None

        except Exception as e:
            logger.error(f"Stop-loss calculation failed for {ticker}: {e}", exc_info=True)
            # Fallback to percentage stop
            return self._percentage_stop(ticker, entry_price)

    def _calculate_atr(self, ticker: str) -> Optional[float]:
        """
        Calculate Average True Range (ATR) for a stock

        Args:
            ticker: Stock symbol

        Returns:
            ATR value or None if calculation fails
        """
        try:
            # Fetch historical data (need ATR period + buffer)
            stock = yf.Ticker(ticker)
            hist = stock.history(period=f"{self.atr_period + 10}d")

            if len(hist) < self.config['data_quality']['min_atr_data_points']:
                logger.warning(f"{ticker}: Insufficient data for ATR ({len(hist)} days, need {self.config['data_quality']['min_atr_data_points']})")
                return None

            # Calculate True Range components
            high = hist['High']
            low = hist['Low']
            close = hist['Close'].shift(1)

            # True Range = max(High-Low, abs(High-PrevClose), abs(Low-PrevClose))
            tr1 = high - low
            tr2 = abs(high - close)
            tr3 = abs(low - close)

            true_range = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)

            # ATR = Moving average of True Range
            atr = true_range.rolling(window=self.atr_period).mean().iloc[-1]

            logger.debug(f"{ticker} ATR({self.atr_period}): ${atr:.2f}")
            return float(atr)

        except Exception as e:
            logger.error(f"ATR calculation failed for {ticker}: {e}")
            return None

    def _atr_based_stop(self, ticker: str, entry_price: float) -> Dict:
        """
        ATR-based stop-loss: Stop = Entry - (ATR × multiplier)

        Args:
            ticker: Stock symbol
            entry_price: Entry price for position

        Returns:
            Stop-loss details
        """
        # Calculate ATR
        atr = self._calculate_atr(ticker)

        if atr is None:
            logger.warning(f"{ticker}: ATR unavailable, falling back to percentage stop")
            return self._percentage_stop(ticker, entry_price)

        # Calculate stop-loss
        stop_loss = entry_price - (atr * self.atr_multiplier)

        # Calculate stop distance as percentage
        stop_distance_pct = (entry_price - stop_loss) / entry_price

        # Validate stop distance
        if stop_distance_pct < self.min_stop_pct:
            logger.warning(f"{ticker}: ATR stop too tight ({stop_distance_pct*100:.1f}%), widening to {self.min_stop_pct*100:.0f}%")
            stop_loss = entry_price * (1 - self.min_stop_pct)
            stop_distance_pct = self.min_stop_pct

        elif stop_distance_pct > self.max_stop_pct:
            logger.warning(f"{ticker}: ATR stop too wide ({stop_distance_pct*100:.1f}%), narrowing to {self.max_stop_pct*100:.0f}%")
            stop_loss = entry_price * (1 - self.max_stop_pct)
            stop_distance_pct = self.max_stop_pct

        result = {
            'method': 'ATR_BASED',
            'ticker': ticker,
            'entry_price': entry_price,
            'atr_value': atr,
            'atr_multiplier': self.atr_multiplier,
            'stop_loss': round(stop_loss, 2),
            'stop_distance_pct': stop_distance_pct,
            'risk_per_share': round(entry_price - stop_loss, 2)
        }

        logger.info(f"Stop-loss for {ticker}: ${stop_loss:.2f} (ATR: ${atr:.2f}, Risk: ${result['risk_per_share']:.2f}/share, {stop_distance_pct*100:.1f}%)")

        return result

    def _percentage_stop(self, ticker: str, entry_price: float) -> Dict:
        """
        Percentage-based stop-loss: Stop = Entry × (1 - percentage)

        Args:
            ticker: Stock symbol
            entry_price: Entry price for position

        Returns:
            Stop-loss details
        """
        stop_loss = entry_price * (1 - self.percentage_stop)
        risk_per_share = entry_price - stop_loss

        result = {
            'method': 'PERCENTAGE',
            'ticker': ticker,
            'entry_price': entry_price,
            'atr_value': None,
            'atr_multiplier': None,
            'stop_loss': round(stop_loss, 2),
            'stop_distance_pct': self.percentage_stop,
            'risk_per_share': round(risk_per_share, 2)
        }

        logger.info(f"Stop-loss for {ticker}: ${stop_loss:.2f} (Percentage: {self.percentage_stop*100:.0f}%, Risk: ${risk_per_share:.2f}/share)")

        return result


if __name__ == "__main__":
    # Test Position Sizer and Stop-Loss Calculator
    logger.info("Risk Department - Testing Position Sizer & Stop-Loss Calculator")

    # Load config
    config_path = Path("Config/risk_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize classes
    position_sizer = PositionSizer(config)
    stop_loss_calc = StopLossCalculator(config)

    # Test with sample data
    capital = config['testing']['initial_capital']  # $100,000
    test_ticker = "AAPL"
    test_price = 175.50

    print("\n" + "=" * 80)
    print(f"TESTING: {test_ticker} @ ${test_price:.2f}")
    print("=" * 80)

    # Test position sizing
    print("\n[1/2] POSITION SIZING:")
    print("-" * 80)
    position = position_sizer.calculate_position_size(capital, test_price, test_ticker)
    if position:
        print(f"  Capital: ${capital:,.0f}")
        print(f"  Target Position: {position['target_position_pct']*100:.0f}% = ${position['target_position_value']:,.0f}")
        print(f"  Shares: {position['shares']}")
        print(f"  Actual Position: ${position['actual_position_value']:,.0f} ({position['actual_position_pct']*100:.1f}%)")

    # Test stop-loss
    print("\n[2/2] STOP-LOSS CALCULATION:")
    print("-" * 80)
    stop = stop_loss_calc.calculate_stop_loss(test_ticker, test_price)
    if stop:
        print(f"  Entry Price: ${stop['entry_price']:.2f}")
        if stop['atr_value']:
            print(f"  ATR({stop_loss_calc.atr_period}): ${stop['atr_value']:.2f}")
        print(f"  Method: {stop['method']}")
        print(f"  Stop-Loss: ${stop['stop_loss']:.2f}")
        print(f"  Risk Per Share: ${stop['risk_per_share']:.2f} ({stop['stop_distance_pct']*100:.1f}%)")

        # Calculate total risk
        if position:
            total_risk = position['shares'] * stop['risk_per_share']
            risk_pct = total_risk / capital
            print(f"\n  Total Risk: {position['shares']} shares × ${stop['risk_per_share']:.2f} = ${total_risk:,.0f} ({risk_pct*100:.2f}% of capital)")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
