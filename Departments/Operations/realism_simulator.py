"""
Realism Simulator - Makes Paper Trading Reflect Real-Money Constraints
======================================================================

Purpose:
--------
Ensures paper trading results accurately predict real-money performance by:
1. Enforcing PDT rules (always assume < $25K account for maximum safety)
2. Modeling slippage (2-10 bps based on order size and liquidity)
3. Tracking margin interest (~12% APR)
4. Simulating partial fills
5. Tracking entry dates for time-based exits

Auto-Detection:
--------------
- Automatically detects paper vs live mode from config.py
- Enables simulation ONLY for paper trading
- Disables automatically when connected to live account
- Logs mode detection for transparency

Philosophy:
-----------
"It would be a mistake to optimize SC so that it only works well in the
fantasy world of paper trading, and breaks rules and loses money the moment
it is trading real money."

Created: November 10, 2025
"""

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sqlite3
import config


class RealismSimulator:
    """
    Simulates realistic trading constraints for paper trading accounts
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = logging.getLogger(self.__class__.__name__)

        # Detect paper vs live mode from config
        self.is_paper = getattr(config, 'APCA_API_BASE_URL', '').endswith('paper-api.alpaca.markets')

        # Configuration
        self.ALWAYS_ENFORCE_PDT = True  # Always assume < $25K rules
        self.SIMULATED_ACCOUNT_VALUE = 24999  # For PDT calculations
        self.MARGIN_INTEREST_RATE = 0.12  # 12% APR
        self.BASE_SLIPPAGE_BPS = 2  # 2 basis points minimum
        self.MAX_SLIPPAGE_BPS = 10  # 10 basis points maximum

        # Database for entry date tracking
        self.db_path = project_root / "sentinel.db"
        self._initialize_entry_dates_table()

        # PDT tracking
        self.day_trades = []  # List of day trades in last 5 business days

        # Log mode detection
        mode = "PAPER TRADING" if self.is_paper else "LIVE TRADING"
        simulation_status = "ENABLED" if self.is_paper else "DISABLED"
        self.logger.info(f"[RealismSimulator] Mode: {mode}")
        self.logger.info(f"[RealismSimulator] Simulation: {simulation_status}")

        if not self.is_paper:
            self.logger.warning("[RealismSimulator] LIVE MODE DETECTED - Simulation disabled")

    def _initialize_entry_dates_table(self):
        """Create entry_dates table if it doesn't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entry_dates (
                    ticker TEXT PRIMARY KEY,
                    entry_date TEXT NOT NULL,
                    shares REAL NOT NULL,
                    entry_price REAL NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            conn.commit()
            conn.close()

            self.logger.info("[RealismSimulator] Entry dates table initialized")

        except Exception as e:
            self.logger.error(f"[RealismSimulator] Failed to initialize entry_dates table: {e}")

    def is_simulation_enabled(self) -> bool:
        """Check if simulation is enabled (only for paper trading)"""
        return self.is_paper

    def get_effective_account_value(self, actual_value: float) -> float:
        """
        Returns the account value to use for PDT calculations

        For paper trading: Always return $24,999 to enforce strictest rules
        For live trading: Return actual value
        """
        if not self.is_paper:
            return actual_value

        if self.ALWAYS_ENFORCE_PDT:
            return self.SIMULATED_ACCOUNT_VALUE

        return actual_value

    def record_entry_date(self, ticker: str, shares: float, entry_price: float, entry_date: Optional[datetime] = None):
        """
        Record entry date for a position (called when BUY order fills)

        Args:
            ticker: Stock ticker symbol
            shares: Number of shares purchased
            entry_price: Price per share at entry
            entry_date: Date/time of entry (defaults to now)
        """
        if not self.is_paper:
            # Still track entry dates in live mode (useful for Rule 2)
            pass

        if entry_date is None:
            entry_date = datetime.now(timezone.utc)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO entry_dates
                (ticker, entry_date, shares, entry_price, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                ticker,
                entry_date.isoformat(),
                shares,
                entry_price,
                datetime.now(timezone.utc).isoformat()
            ))

            conn.commit()
            conn.close()

            self.logger.info(f"[RealismSimulator] Recorded entry date for {ticker}: {entry_date.date()}")

        except Exception as e:
            self.logger.error(f"[RealismSimulator] Failed to record entry date for {ticker}: {e}")

    def get_entry_date(self, ticker: str) -> Optional[datetime]:
        """
        Get entry date for a position

        Returns:
            datetime object if entry date found, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT entry_date FROM entry_dates WHERE ticker = ?
            """, (ticker,))

            row = cursor.fetchone()
            conn.close()

            if row:
                entry_date_str = row[0]
                entry_date = datetime.fromisoformat(entry_date_str)
                return entry_date

            return None

        except Exception as e:
            self.logger.error(f"[RealismSimulator] Failed to get entry date for {ticker}: {e}")
            return None

    def remove_entry_date(self, ticker: str):
        """Remove entry date for a position (called when SELL order fills)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM entry_dates WHERE ticker = ?
            """, (ticker,))

            conn.commit()
            conn.close()

            self.logger.info(f"[RealismSimulator] Removed entry date for {ticker}")

        except Exception as e:
            self.logger.error(f"[RealismSimulator] Failed to remove entry date for {ticker}: {e}")

    def calculate_days_held(self, ticker: str) -> Optional[int]:
        """
        Calculate number of days a position has been held

        Returns:
            Number of days held, or None if entry date not found
        """
        entry_date = self.get_entry_date(ticker)

        if entry_date is None:
            return None

        now = datetime.now(timezone.utc)
        delta = now - entry_date
        days_held = delta.days

        return days_held

    def record_trade(self, ticker: str, action: str, trade_date: Optional[datetime] = None):
        """
        Record a trade for PDT tracking

        Args:
            ticker: Stock ticker symbol
            action: 'BUY' or 'SELL'
            trade_date: Date/time of trade (defaults to now)
        """
        if not self.is_simulation_enabled():
            return

        if trade_date is None:
            trade_date = datetime.now(timezone.utc)

        # Add to trade history
        self.day_trades.append({
            'ticker': ticker,
            'action': action,
            'date': trade_date
        })

        # Clean up trades older than 5 business days
        self._cleanup_old_trades()

    def _cleanup_old_trades(self):
        """Remove trades older than 5 business days"""
        if not self.day_trades:
            return

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=7)  # Use 7 calendar days as safe buffer

        self.day_trades = [
            t for t in self.day_trades
            if t['date'] > cutoff
        ]

    def count_day_trades_in_period(self, days: int = 5) -> int:
        """
        Count day trades in the last N business days

        A day trade is defined as:
        - BUY followed by SELL of same ticker on same day
        - OR SELL followed by BUY of same ticker on same day (short)
        """
        if not self.is_simulation_enabled():
            return 0

        self._cleanup_old_trades()

        # Group trades by ticker and date
        trades_by_ticker_date = {}

        for trade in self.day_trades:
            ticker = trade['ticker']
            date = trade['date'].date()
            key = (ticker, date)

            if key not in trades_by_ticker_date:
                trades_by_ticker_date[key] = []

            trades_by_ticker_date[key].append(trade['action'])

        # Count day trades (ticker traded on both sides on same day)
        day_trade_count = 0

        for (ticker, date), actions in trades_by_ticker_date.items():
            has_buy = 'BUY' in actions
            has_sell = 'SELL' in actions

            if has_buy and has_sell:
                day_trade_count += 1
                self.logger.warning(
                    f"[RealismSimulator] Day trade detected: {ticker} on {date}"
                )

        return day_trade_count

    def check_pdt_violation(self) -> Tuple[bool, str]:
        """
        Check if proposed trade would violate PDT rules

        Returns:
            (is_violation, message)
        """
        if not self.is_simulation_enabled():
            return (False, "PDT check disabled in live mode")

        day_trade_count = self.count_day_trades_in_period(days=5)

        if day_trade_count >= 4:
            return (
                True,
                f"PDT VIOLATION: {day_trade_count} day trades in last 5 days (max: 3)"
            )

        if day_trade_count == 3:
            return (
                False,
                f"PDT WARNING: {day_trade_count} day trades in last 5 days (limit: 3)"
            )

        return (False, f"PDT OK: {day_trade_count} day trades in last 5 days")

    def calculate_slippage(self, ticker: str, shares: float, price: float,
                          daily_volume: float, action: str) -> float:
        """
        Calculate realistic slippage based on order size and liquidity

        Slippage model:
        - Base: 2 bps (0.02%)
        - Increases with order size relative to daily volume
        - Max: 10 bps (0.10%)

        Args:
            ticker: Stock ticker
            shares: Number of shares
            price: Price per share
            daily_volume: Average daily volume
            action: 'BUY' or 'SELL'

        Returns:
            Slippage amount in dollars (always positive)
        """
        if not self.is_simulation_enabled():
            return 0.0

        # Calculate order size as % of daily volume
        order_value = shares * price
        volume_pct = shares / daily_volume if daily_volume > 0 else 0

        # Scale slippage based on volume impact
        # 0% of volume = 2 bps
        # 10% of volume = 10 bps
        slippage_bps = self.BASE_SLIPPAGE_BPS + (volume_pct * 0.10) * (self.MAX_SLIPPAGE_BPS - self.BASE_SLIPPAGE_BPS)
        slippage_bps = min(slippage_bps, self.MAX_SLIPPAGE_BPS)

        # Convert to dollars
        slippage_dollars = order_value * (slippage_bps / 10000)

        self.logger.info(
            f"[RealismSimulator] Slippage for {action} {ticker}: "
            f"{slippage_bps:.1f} bps (${slippage_dollars:.2f})"
        )

        return slippage_dollars

    def calculate_margin_interest(self, margin_used: float, days_held: int) -> float:
        """
        Calculate margin interest cost

        Args:
            margin_used: Amount of margin borrowed
            days_held: Number of days position held

        Returns:
            Interest cost in dollars
        """
        if not self.is_simulation_enabled():
            return 0.0

        if margin_used <= 0:
            return 0.0

        # Daily interest rate
        daily_rate = self.MARGIN_INTEREST_RATE / 365

        # Calculate interest
        interest = margin_used * daily_rate * days_held

        if interest > 0:
            self.logger.info(
                f"[RealismSimulator] Margin interest: ${interest:.2f} "
                f"(${margin_used:,.0f} @ {self.MARGIN_INTEREST_RATE*100}% for {days_held} days)"
            )

        return interest

    def get_simulation_summary(self, positions: List[Dict]) -> Dict:
        """
        Generate summary of simulation adjustments

        Args:
            positions: List of current positions

        Returns:
            Dictionary with simulation metrics
        """
        if not self.is_simulation_enabled():
            return {
                'enabled': False,
                'mode': 'LIVE',
                'message': 'Simulation disabled in live mode'
            }

        # Calculate total adjustments
        total_slippage = 0.0
        total_margin_interest = 0.0

        for position in positions:
            ticker = position.get('ticker', position.get('symbol', ''))
            days_held = self.calculate_days_held(ticker)

            if days_held:
                # Estimate margin used (simplified)
                position_value = position.get('market_value', 0)
                margin_used = max(0, position_value * 0.5)  # Assume 50% margin

                interest = self.calculate_margin_interest(margin_used, days_held)
                total_margin_interest += interest

        # PDT status
        day_trade_count = self.count_day_trades_in_period()
        pdt_warning = day_trade_count >= 3

        return {
            'enabled': True,
            'mode': 'PAPER',
            'enforced_account_value': self.SIMULATED_ACCOUNT_VALUE,
            'day_trades_in_period': day_trade_count,
            'pdt_warning': pdt_warning,
            'total_margin_interest': total_margin_interest,
            'margin_interest_rate': self.MARGIN_INTEREST_RATE,
            'message': f"Simulating < $25K account (PDT: {day_trade_count}/3 day trades)"
        }
