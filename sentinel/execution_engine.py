# -*- coding: utf-8 -*-
# sentinel/execution_engine.py
# Order Execution Engine - Stop-Loss Only Architecture
# Week 1 Implementation

"""
OrderExecutionEngine handles all order lifecycle operations:
1. Entry order + stop loss submission (atomic)
2. Fill reconciliation (evening workflow)
3. Trailing stop updates (protect profits)
4. Profit-taking detection (manual approval)
5. Orphaned stop cleanup (housekeeping)

CRITICAL: This engine implements stop-loss-only architecture.
No profit target orders or OCO pairs during paper trading phase.
"""

import logging
import time
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

# Import risk configuration
from sentinel.risk_config import (
    INITIAL_STOP_LOSS_PCT,
    TRAILING_STOP_TRIGGER_PCT,
    TRAILING_STOP_LOCK_IN_PCT,
    TRAILING_STOP_LEVELS,
    PROFIT_TARGET_PCT,
    REQUIRE_MANUAL_APPROVAL_FOR_PROFIT_TAKING,
    MAX_API_RETRIES,
    API_RETRY_DELAYS,
    API_CALL_TIMEOUT,
    ORPHANED_STOP_GRACE_PERIOD,
    calculate_stop_price,
    calculate_trailing_stop_price,
    get_stop_type_label,
    should_take_profit
)


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class EntryOrder:
    """Represents an entry order in the database."""
    id: int
    symbol: str
    order_id: str
    client_order_id: str
    side: str
    qty: int
    order_type: str
    limit_price: Optional[float]
    status: str
    submitted_at: datetime
    filled_at: Optional[datetime] = None
    filled_price: Optional[float] = None
    filled_qty: Optional[int] = None


@dataclass
class StopLossOrder:
    """Represents a stop loss order in the database."""
    id: int
    entry_order_id: int
    symbol: str
    order_id: str
    client_order_id: str
    qty: int
    stop_price: float
    stop_type: str
    status: str
    submitted_at: datetime
    triggered_at: Optional[datetime] = None
    triggered_price: Optional[float] = None
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None


@dataclass
class EntryStopPair:
    """Represents an entry-stop pair relationship."""
    id: int
    entry_order_id: int
    stop_order_id: int
    symbol: str
    entry_price: Optional[float]
    stop_price: Optional[float]
    created_at: datetime
    resolved_at: Optional[datetime]
    resolution: Optional[str]
    notes: Optional[str]


# ============================================================================
# EXCEPTIONS
# ============================================================================

class OrderSubmissionError(Exception):
    """Raised when order submission fails after retries."""
    pass


class DatabaseError(Exception):
    """Raised when database operations fail."""
    pass


class APIError(Exception):
    """Raised when Alpaca API calls fail."""
    pass


# ============================================================================
# ORDER EXECUTION ENGINE
# ============================================================================

class OrderExecutionEngine:
    """
    Manages all order lifecycle operations for stop-loss-only architecture.

    Responsibilities:
    - Atomic entry + stop submission
    - Fill reconciliation
    - Trailing stop management
    - Profit-taking detection
    - Orphaned stop cleanup

    NOT responsible for:
    - Strategy signal generation (handled by conviction analysis)
    - Position sizing (handled by portfolio construction)
    - Trade approval (handled by approval workflow)
    """

    def __init__(self, api_client, db_path="sentinel.db", max_retries=MAX_API_RETRIES):
        """
        Initialize order execution engine.

        Args:
            api_client: Alpaca API client
            db_path: Path to SQLite database
            max_retries: Maximum API call retries
        """
        self.api = api_client
        self.db_path = db_path
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

    # ========================================================================
    # DATABASE HELPERS
    # ========================================================================

    def _get_db_connection(self):
        """Get database connection with proper settings."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _store_entry_order(self, conn, symbol, order_id, client_order_id, side, qty, order_type, limit_price):
        """Store entry order in database."""
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entry_orders (
                symbol, order_id, client_order_id, side, qty,
                order_type, limit_price, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (symbol, order_id, client_order_id, side, qty, order_type, limit_price))
        return cursor.lastrowid

    def _store_stop_order(self, conn, entry_order_id, symbol, order_id, client_order_id, qty, stop_price, stop_type='initial'):
        """Store stop loss order in database."""
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stop_loss_orders (
                entry_order_id, symbol, order_id, client_order_id,
                qty, stop_price, stop_type, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
        """, (entry_order_id, symbol, order_id, client_order_id, qty, stop_price, stop_type))
        return cursor.lastrowid

    def _store_entry_stop_pair(self, conn, entry_order_id, stop_order_id, symbol, entry_price, stop_price):
        """Store entry-stop pair relationship."""
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entry_stop_pairs (
                entry_order_id, stop_order_id, symbol, entry_price, stop_price
            ) VALUES (?, ?, ?, ?, ?)
        """, (entry_order_id, stop_order_id, symbol, entry_price, stop_price))
        return cursor.lastrowid

    # ========================================================================
    # API HELPERS WITH RETRY LOGIC
    # ========================================================================

    def _submit_with_retry(self, submit_func, description="API call"):
        """
        Execute API call with exponential backoff retry logic.

        Args:
            submit_func: Function that performs the API call
            description: Human-readable description for logging

        Returns:
            API response or None if all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                result = submit_func()
                self.logger.debug(f"{description} succeeded on attempt {attempt + 1}")
                return result

            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait_time = API_RETRY_DELAYS[attempt]
                    self.logger.warning(
                        f"{description} failed on attempt {attempt + 1}/{self.max_retries}: {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"{description} failed after {self.max_retries} attempts: {e}")
                    return None

        return None

    # ========================================================================
    # CORE: ENTRY + STOP SUBMISSION
    # ========================================================================

    def submit_entry_with_stop(
        self,
        symbol: str,
        entry_price: float,
        qty: int,
        stop_loss_pct: float = INITIAL_STOP_LOSS_PCT,
        side: str = 'buy'
    ) -> Tuple[Optional[object], Optional[object]]:
        """
        Submit entry order + protective stop loss as atomic operation.

        This is the ONLY way to create new positions in the system.
        Ensures every entry has immediate stop loss protection.

        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            entry_price: Desired entry price
            qty: Share quantity
            stop_loss_pct: Stop loss as decimal (0.92 = -8%)
            side: 'buy' or 'sell'

        Returns:
            Tuple of (entry_order, stop_order) or (None, None) on failure

        Raises:
            OrderSubmissionError: If submission fails critically
        """
        # ====================================================================
        # VALIDATION
        # ====================================================================
        if qty <= 0:
            raise ValueError(f"Invalid quantity: {qty}")
        if entry_price <= 0:
            raise ValueError(f"Invalid entry price: {entry_price}")
        if not (0.80 <= stop_loss_pct <= 0.98):
            raise ValueError(f"Stop loss % out of range: {stop_loss_pct}")
        if side not in ['buy', 'sell']:
            raise ValueError(f"Invalid side: {side}")

        # ====================================================================
        # CALCULATE PRICES
        # ====================================================================
        # Entry limit: slight edge above market to ensure fill
        entry_limit = round(entry_price * 1.001, 2)

        # Stop price: percentage below entry
        stop_price = round(entry_price * stop_loss_pct, 2)

        self.logger.info(
            f"Preparing entry+stop for {symbol}: "
            f"Entry ${entry_limit} x{qty}, Stop ${stop_price} ({(1-stop_loss_pct)*100:.1f}% below)"
        )

        # ====================================================================
        # GENERATE CLIENT ORDER IDS (for idempotency)
        # ====================================================================
        timestamp = datetime.now(timezone.utc).isoformat()
        entry_coid = f"{symbol}_entry_{timestamp}"
        stop_coid = f"{symbol}_stop_{timestamp}"

        # ====================================================================
        # SUBMIT ENTRY ORDER
        # ====================================================================
        self.logger.debug(f"Submitting entry order: {symbol} {side} {qty} @ ${entry_limit}")

        entry_order = self._submit_with_retry(
            lambda: self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type='limit',
                limit_price=entry_limit,
                time_in_force='day',  # Expires if unfilled
                client_order_id=entry_coid
            ),
            description=f"Entry order for {symbol}"
        )

        if not entry_order:
            error_msg = f"Failed to submit entry order for {symbol} after {self.max_retries} attempts"
            self.logger.error(error_msg)
            raise OrderSubmissionError(error_msg)

        self.logger.info(f"[OK] Entry order submitted: {symbol} {entry_order.id}")

        # ====================================================================
        # SUBMIT STOP LOSS ORDER
        # ====================================================================
        self.logger.debug(f"Submitting stop loss: {symbol} sell {qty} @ ${stop_price}")

        stop_order = self._submit_with_retry(
            lambda: self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',  # Always sell for stop loss
                type='stop',
                stop_price=stop_price,
                time_in_force='gtc',  # Persists until position closes
                client_order_id=stop_coid
            ),
            description=f"Stop order for {symbol}"
        )

        if not stop_order:
            # CRITICAL FAILURE: Entry submitted but stop failed
            # MUST cancel entry to avoid unprotected position
            self.logger.error(
                f"Stop order failed for {symbol}. CANCELING ENTRY {entry_order.id} to prevent unprotected position."
            )

            try:
                self.api.cancel_order(entry_order.id)
                self.logger.warning(f"Entry order {entry_order.id} canceled successfully")
            except Exception as cancel_error:
                self.logger.critical(
                    f"FAILED TO CANCEL ENTRY {entry_order.id}: {cancel_error}. "
                    f"MANUAL INTERVENTION REQUIRED - Check Alpaca dashboard!"
                )

            raise OrderSubmissionError(f"Stop order failed for {symbol}, entry was canceled")

        self.logger.info(f"[OK] Stop order submitted: {symbol} {stop_order.id}")

        # ====================================================================
        # STORE IN DATABASE (atomic transaction)
        # ====================================================================
        try:
            conn = self._get_db_connection()
            conn.execute("BEGIN TRANSACTION")

            # Store entry order
            entry_id = self._store_entry_order(
                conn, symbol, entry_order.id, entry_coid,
                side, qty, 'limit', entry_limit
            )

            # Store stop order
            stop_id = self._store_stop_order(
                conn, entry_id, symbol, stop_order.id, stop_coid,
                qty, stop_price, 'initial'
            )

            # Store pair relationship
            self._store_entry_stop_pair(
                conn, entry_id, stop_id, symbol, entry_limit, stop_price
            )

            conn.commit()
            self.logger.info(f"[OK] Database records created for {symbol} (pair ID: entry={entry_id}, stop={stop_id})")

        except Exception as db_error:
            conn.rollback()
            self.logger.error(f"Database storage failed for {symbol}: {db_error}")

            # Cancel both orders if database storage fails
            try:
                self.api.cancel_order(entry_order.id)
                self.api.cancel_order(stop_order.id)
                self.logger.warning(f"Orders canceled due to database failure: {symbol}")
            except Exception as cancel_error:
                self.logger.critical(
                    f"FAILED TO CANCEL ORDERS AFTER DB ERROR: {cancel_error}. "
                    f"Orders: entry={entry_order.id}, stop={stop_order.id}. MANUAL CHECK REQUIRED!"
                )

            raise DatabaseError(f"Failed to store orders for {symbol}: {db_error}")

        finally:
            conn.close()

        # ====================================================================
        # SUCCESS
        # ====================================================================
        self.logger.info(
            f"[SUCCESS] Entry+Stop submitted for {symbol}: "
            f"Entry ${entry_limit} x{qty} (order {entry_order.id}), "
            f"Stop ${stop_price} (order {stop_order.id})"
        )

        return (entry_order, stop_order)

    # ========================================================================
    # FILL RECONCILIATION (Evening Workflow)
    # ========================================================================

    def reconcile_fills(self) -> Dict[str, int]:
        """
        Check Alpaca API for order status updates.
        Called during evening workflow (not intraday).

        Returns:
            Dict with counts: {'filled': N, 'cancelled': M, 'expired': K}
        """
        self.logger.info("Starting fill reconciliation...")

        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Get all pending entry orders
        cursor.execute("""
            SELECT id, symbol, order_id, client_order_id, submitted_at
            FROM entry_orders
            WHERE status = 'pending'
        """)
        pending_entries = cursor.fetchall()

        counts = {'filled': 0, 'cancelled': 0, 'expired': 0, 'errors': 0}

        for row in pending_entries:
            entry_id = row['id']
            symbol = row['symbol']
            order_id = row['order_id']

            try:
                # Query Alpaca for current status
                order = self.api.get_order(order_id)

                if order.status == 'filled':
                    # Entry filled - update database
                    cursor.execute("""
                        UPDATE entry_orders
                        SET status = 'filled',
                            filled_at = ?,
                            filled_price = ?,
                            filled_qty = ?
                        WHERE id = ?
                    """, (order.filled_at, float(order.filled_avg_price), int(order.filled_qty), entry_id))

                    counts['filled'] += 1
                    self.logger.info(
                        f"[FILL DETECTED] {symbol}: {order.filled_qty} shares @ ${order.filled_avg_price} "
                        f"at {order.filled_at}"
                    )

                elif order.status in ['cancelled', 'expired', 'rejected']:
                    # Entry did not fill - update database and cancel corresponding stop
                    cursor.execute("""
                        UPDATE entry_orders
                        SET status = ?
                        WHERE id = ?
                    """, (order.status, entry_id))

                    # Cancel stop (entry never filled, stop is orphaned)
                    self._cancel_stop_for_entry(cursor, entry_id, reason='entry_unfilled')

                    counts[order.status] += 1
                    self.logger.info(f"[ENTRY {order.status.upper()}] {symbol} - stop canceled")

            except Exception as e:
                self.logger.error(f"Error reconciling entry {order_id} for {symbol}: {e}")
                counts['errors'] += 1
                continue

        conn.commit()
        conn.close()

        self.logger.info(
            f"Fill reconciliation complete: "
            f"{counts['filled']} filled, {counts['cancelled']} cancelled, "
            f"{counts['expired']} expired, {counts['errors']} errors"
        )

        return counts

    def _cancel_stop_for_entry(self, cursor, entry_id: int, reason: str):
        """
        Cancel stop order associated with entry (helper for reconcile_fills).

        Args:
            cursor: Database cursor (in transaction)
            entry_id: Entry order database ID
            reason: Cancellation reason
        """
        # Get stop order ID from pair
        cursor.execute("""
            SELECT s.order_id, s.id
            FROM stop_loss_orders s
            JOIN entry_stop_pairs ep ON s.id = ep.stop_order_id
            WHERE ep.entry_order_id = ?
              AND s.status = 'active'
        """, (entry_id,))

        stop_row = cursor.fetchone()
        if not stop_row:
            self.logger.warning(f"No active stop found for entry {entry_id}")
            return

        stop_order_id = stop_row['order_id']
        stop_db_id = stop_row['id']

        try:
            # Cancel on Alpaca
            self.api.cancel_order(stop_order_id)

            # Update database
            cursor.execute("""
                UPDATE stop_loss_orders
                SET status = 'cancelled',
                    cancelled_at = ?,
                    cancel_reason = ?
                WHERE id = ?
            """, (datetime.now(timezone.utc), reason, stop_db_id))

            # Mark pair as resolved
            cursor.execute("""
                UPDATE entry_stop_pairs
                SET resolved_at = ?,
                    resolution = 'entry_unfilled'
                WHERE entry_order_id = ?
            """, (datetime.now(timezone.utc), entry_id))

            self.logger.debug(f"Stop {stop_order_id} canceled (reason: {reason})")

        except Exception as e:
            self.logger.error(f"Failed to cancel stop {stop_order_id}: {e}")


    # ========================================================================
    # TRAILING STOP MANAGEMENT (Evening Workflow)
    # ========================================================================

    def update_trailing_stops(
        self,
        breakeven_threshold_pct: float = TRAILING_STOP_TRIGGER_PCT,
        lock_in_pct: float = TRAILING_STOP_LOCK_IN_PCT
    ) -> Dict[str, int]:
        """
        Raise stops to protect gains for profitable positions.
        Uses staircase approach: higher gains = more protection.

        Called during evening workflow (not intraday).

        Args:
            breakeven_threshold_pct: Minimum gain to activate trailing (default: 0.08)
            lock_in_pct: Minimum profit to lock in (default: 0.02)

        Returns:
            Dict with counts: {'raised': N, 'unchanged': M, 'errors': K}
        """
        self.logger.info("Updating trailing stops for profitable positions...")

        try:
            positions = self.api.list_positions()
        except Exception as e:
            self.logger.error(f"Failed to fetch positions from Alpaca: {e}")
            return {'raised': 0, 'unchanged': 0, 'errors': 1}

        conn = self._get_db_connection()
        cursor = conn.cursor()

        counts = {'raised': 0, 'unchanged': 0, 'errors': 0, 'emergency_stops': 0}

        for pos in positions:
            try:
                symbol = pos.symbol
                current_price = float(pos.current_price)
                entry_price = float(pos.avg_entry_price)
                current_qty = abs(int(float(pos.qty)))  # Handle fractional shares

                # Calculate unrealized P&L percentage
                unrealized_pnl_pct = (current_price - entry_price) / entry_price

                # Only process profitable positions
                if unrealized_pnl_pct < breakeven_threshold_pct:
                    counts['unchanged'] += 1
                    continue

                # Get current stop
                cursor.execute("""
                    SELECT id, order_id, stop_price, stop_type
                    FROM stop_loss_orders
                    WHERE symbol = ?
                      AND status = 'active'
                    ORDER BY submitted_at DESC
                    LIMIT 1
                """, (symbol,))

                stop_row = cursor.fetchone()

                if not stop_row:
                    self.logger.warning(
                        f"No active stop found for {symbol} (position exists but no stop!) - creating emergency stop"
                    )
                    self._create_emergency_stop(symbol, current_price, current_qty, entry_price)
                    counts['emergency_stops'] += 1
                    continue

                current_stop_id = stop_row['id']
                current_stop_order_id = stop_row['order_id']
                current_stop_price = stop_row['stop_price']
                current_stop_type = stop_row['stop_type']

                # Calculate new stop price using staircase logic
                new_stop_price, new_stop_type = self._calculate_staircase_stop(
                    entry_price, unrealized_pnl_pct
                )

                # Only raise stop, never lower
                if new_stop_price <= current_stop_price:
                    counts['unchanged'] += 1
                    continue

                # Use Alpaca's replace_order() to atomically update the stop price
                # This avoids race conditions from cancel+submit
                new_stop_order = self._submit_with_retry(
                    lambda: self.api.replace_order(
                        current_stop_order_id,
                        qty=str(current_qty),
                        stop_price=str(new_stop_price)
                    ),
                    description=f"Replace trailing stop for {symbol}"
                )

                if not new_stop_order:
                    self.logger.error(f"Failed to replace trailing stop for {symbol}")
                    counts['errors'] += 1
                    continue  # Keep old stop in place

                # Update database (order_id stays the same with replace_order)
                cursor.execute("""
                    UPDATE stop_loss_orders
                    SET stop_price = ?,
                        stop_type = ?,
                        submitted_at = ?
                    WHERE id = ?
                """, (new_stop_price, new_stop_type, datetime.now(timezone.utc), current_stop_id))

                # Update entry_stop_pair if exists (skip for legacy stops)
                cursor.execute("""
                    UPDATE entry_stop_pairs
                    SET stop_price = ?
                    WHERE stop_order_id = ?
                """, (new_stop_price, current_stop_id))

                conn.commit()

                counts['raised'] += 1
                self.logger.info(
                    f"[TRAILING STOP RAISED] {symbol}: "
                    f"${current_stop_price:.2f} -> ${new_stop_price:.2f} "
                    f"(P&L: +{unrealized_pnl_pct:.1%}, Type: {new_stop_type})"
                )

            except Exception as e:
                self.logger.error(f"Error updating trailing stop for {symbol}: {e}")
                counts['errors'] += 1
                conn.rollback()
                continue

        conn.close()

        self.logger.info(
            f"Trailing stop update complete: "
            f"{counts['raised']} raised, {counts['unchanged']} unchanged, "
            f"{counts['emergency_stops']} emergency stops created, {counts['errors']} errors"
        )

        return counts

    def _calculate_staircase_stop(
        self,
        entry_price: float,
        unrealized_pnl_pct: float
    ) -> Tuple[float, str]:
        """
        Calculate trailing stop price based on staircase levels.

        Staircase approach:
        - +8% gain -> lock in +2%
        - +15% gain -> lock in +8%
        - +25% gain -> lock in +15%

        Args:
            entry_price: Original entry price
            unrealized_pnl_pct: Current unrealized P&L percentage

        Returns:
            Tuple of (stop_price, stop_type_label)
        """
        for min_gain, lock_in, stop_type in reversed(TRAILING_STOP_LEVELS):
            if unrealized_pnl_pct >= min_gain:
                stop_price = round(entry_price * (1 + lock_in), 2)
                return (stop_price, stop_type)

        # Below minimum threshold, use initial stop
        stop_price = calculate_stop_price(entry_price)
        return (stop_price, 'initial')

    def _create_emergency_stop(
        self,
        symbol: str,
        current_price: float,
        qty: int,
        entry_price: float
    ):
        """
        Create emergency stop when position exists without protection.

        This should NEVER happen in normal operation (every entry creates a stop).
        If this executes, it indicates a critical system failure.

        Args:
            symbol: Stock ticker
            current_price: Current market price
            qty: Share quantity
            entry_price: Average entry price
        """
        self.logger.critical(
            f"[EMERGENCY STOP] Creating protective stop for {symbol} - "
            f"position exists without stop protection!"
        )

        # Calculate stop at -8% from entry
        stop_price = calculate_stop_price(entry_price)

        timestamp = datetime.now(timezone.utc).isoformat()
        stop_coid = f"{symbol}_emergency_{timestamp}"

        try:
            stop_order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='stop',
                stop_price=stop_price,
                time_in_force='gtc',
                client_order_id=stop_coid
            )

            self.logger.warning(
                f"[EMERGENCY STOP CREATED] {symbol}: {qty} shares @ ${stop_price} "
                f"(order {stop_order.id})"
            )

            # Store in database (use -1 as sentinel for emergency stops without entry_order_id)
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO stop_loss_orders (
                    entry_order_id, symbol, order_id, client_order_id,
                    qty, stop_price, stop_type, status
                ) VALUES (
                    -1, ?, ?, ?, ?, ?, 'initial', 'active'
                )
            """, (symbol, stop_order.id, stop_coid, qty, stop_price))
            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.critical(
                f"[EMERGENCY STOP FAILED] Could not create emergency stop for {symbol}: {e}. "
                f"POSITION IS UNPROTECTED! MANUAL INTERVENTION REQUIRED!"
            )

    # ========================================================================
    # PROFIT-TAKING DETECTION (Evening Workflow)
    # ========================================================================

    def check_profit_taking(
        self,
        profit_target_pct: float = PROFIT_TARGET_PCT,
        require_approval: bool = REQUIRE_MANUAL_APPROVAL_FOR_PROFIT_TAKING
    ) -> Dict[str, any]:
        """
        Check current positions for profit-taking opportunities.
        Flags positions at +16% or better for review.

        If manual approval required, returns list of candidates.
        If auto-approval enabled, submits market sell orders.

        Args:
            profit_target_pct: Profit target threshold (default: 0.16)
            require_approval: Whether to require manual approval (default: True)

        Returns:
            Dict with 'candidates' (list) and 'submitted' (list)
        """
        self.logger.info(f"Checking for profit-taking opportunities (target: +{profit_target_pct:.1%})...")

        try:
            positions = self.api.list_positions()
        except Exception as e:
            self.logger.error(f"Failed to fetch positions from Alpaca: {e}")
            return {'candidates': [], 'submitted': []}

        candidates = []
        submitted = []

        for pos in positions:
            try:
                symbol = pos.symbol
                current_price = float(pos.current_price)
                entry_price = float(pos.avg_entry_price)
                qty = abs(int(float(pos.qty)))  # Handle fractional shares
                unrealized_pl = float(pos.unrealized_pl)
                unrealized_pnl_pct = (current_price - entry_price) / entry_price

                if unrealized_pnl_pct >= profit_target_pct:
                    candidate = {
                        'symbol': symbol,
                        'qty': qty,
                        'entry_price': entry_price,
                        'current_price': current_price,
                        'unrealized_pl': unrealized_pl,
                        'unrealized_pnl_pct': unrealized_pnl_pct
                    }
                    candidates.append(candidate)

                    self.logger.info(
                        f"[PROFIT TARGET HIT] {symbol}: +{unrealized_pnl_pct:.1%} "
                        f"(${unrealized_pl:.2f})"
                    )

            except Exception as e:
                self.logger.error(f"Error checking profit target for {pos.symbol}: {e}")
                continue

        if not candidates:
            self.logger.info("No positions at profit target")
            return {'candidates': [], 'submitted': []}

        # Manual approval mode: return candidates for user review
        if require_approval:
            self.logger.info(
                f"Found {len(candidates)} profit target candidates - "
                f"manual approval required"
            )
            return {'candidates': candidates, 'submitted': []}

        # Auto-approval mode: submit market sells immediately
        self.logger.warning("Auto-approval enabled - submitting profit-taking orders")

        for candidate in candidates:
            symbol = candidate['symbol']
            qty = candidate['qty']

            try:
                # Submit market sell for next trading day
                timestamp = datetime.now(timezone.utc).isoformat()
                sell_coid = f"{symbol}_profit_{timestamp}"

                sell_order = self.api.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side='sell',
                    type='market',
                    time_in_force='day',
                    client_order_id=sell_coid
                )

                # Cancel corresponding stop
                self._cancel_stop_for_symbol(symbol, reason='profit_target_hit')

                submitted.append({
                    'symbol': symbol,
                    'qty': qty,
                    'order_id': sell_order.id,
                    'expected_profit': candidate['unrealized_pl']
                })

                self.logger.info(
                    f"[PROFIT ORDER SUBMITTED] {symbol}: Market sell {qty} shares "
                    f"(order {sell_order.id})"
                )

            except Exception as e:
                self.logger.error(f"Failed to submit profit-taking order for {symbol}: {e}")
                continue

        return {'candidates': candidates, 'submitted': submitted}

    def _cancel_stop_for_symbol(self, symbol: str, reason: str):
        """
        Cancel active stop order for a symbol.

        Args:
            symbol: Stock ticker
            reason: Cancellation reason
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Get active stop
        cursor.execute("""
            SELECT id, order_id
            FROM stop_loss_orders
            WHERE symbol = ?
              AND status = 'active'
            ORDER BY submitted_at DESC
            LIMIT 1
        """, (symbol,))

        stop_row = cursor.fetchone()

        if not stop_row:
            self.logger.warning(f"No active stop found for {symbol} to cancel")
            conn.close()
            return

        stop_id = stop_row['id']
        stop_order_id = stop_row['order_id']

        try:
            # Cancel on Alpaca
            self.api.cancel_order(stop_order_id)

            # Update database
            cursor.execute("""
                UPDATE stop_loss_orders
                SET status = 'cancelled',
                    cancelled_at = ?,
                    cancel_reason = ?
                WHERE id = ?
            """, (datetime.now(timezone.utc), reason, stop_id))

            # Mark pair as resolved
            cursor.execute("""
                UPDATE entry_stop_pairs
                SET resolved_at = ?,
                    resolution = 'manual_exit',
                    notes = ?
                WHERE stop_order_id = ?
            """, (datetime.now(timezone.utc), reason, stop_id))

            conn.commit()
            self.logger.debug(f"Stop {stop_order_id} canceled for {symbol} (reason: {reason})")

        except Exception as e:
            self.logger.error(f"Failed to cancel stop for {symbol}: {e}")
            conn.rollback()

        finally:
            conn.close()

    # ========================================================================
    # ORPHANED STOP CLEANUP (Evening Workflow)
    # ========================================================================

    def cleanup_orphaned_stops(
        self,
        grace_period_minutes: int = ORPHANED_STOP_GRACE_PERIOD
    ) -> Dict[str, int]:
        """
        Cancel stop orders for positions that no longer exist.

        Orphaned stops occur when:
        - Entry expired/cancelled (handled by reconcile_fills)
        - Position sold manually
        - Stop triggered and filled

        Args:
            grace_period_minutes: Wait time before canceling (default: 5 minutes)

        Returns:
            Dict with counts: {'cancelled': N, 'skipped': M}
        """
        self.logger.info("Cleaning up orphaned stop orders...")

        try:
            positions = self.api.list_positions()
            current_position_symbols = {pos.symbol for pos in positions}
        except Exception as e:
            self.logger.error(f"Failed to fetch positions from Alpaca: {e}")
            return {'cancelled': 0, 'skipped': 0}

        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Get all active stops
        cursor.execute("""
            SELECT id, symbol, order_id, submitted_at
            FROM stop_loss_orders
            WHERE status = 'active'
        """)

        active_stops = cursor.fetchall()

        counts = {'cancelled': 0, 'skipped': 0}

        for stop_row in active_stops:
            stop_id = stop_row['id']
            symbol = stop_row['symbol']
            stop_order_id = stop_row['order_id']
            submitted_at = datetime.fromisoformat(stop_row['submitted_at'])

            # Check if position still exists
            if symbol in current_position_symbols:
                counts['skipped'] += 1
                continue

            # Check age (grace period for settlement)
            age_minutes = (datetime.now(timezone.utc) - submitted_at).total_seconds() / 60

            if age_minutes < grace_period_minutes:
                self.logger.debug(
                    f"Skipping recent orphaned stop for {symbol} "
                    f"(age: {age_minutes:.1f}min < {grace_period_minutes}min grace period)"
                )
                counts['skipped'] += 1
                continue

            # Orphaned stop confirmed - cancel it
            try:
                self.api.cancel_order(stop_order_id)

                cursor.execute("""
                    UPDATE stop_loss_orders
                    SET status = 'cancelled',
                        cancelled_at = ?,
                        cancel_reason = 'position_closed'
                    WHERE id = ?
                """, (datetime.now(timezone.utc), stop_id))

                # Mark pair as resolved
                cursor.execute("""
                    UPDATE entry_stop_pairs
                    SET resolved_at = ?,
                        resolution = 'manual_exit',
                        notes = 'Position closed, stop orphaned'
                    WHERE stop_order_id = ?
                """, (datetime.now(timezone.utc), stop_id))

                conn.commit()

                counts['cancelled'] += 1
                self.logger.info(f"[ORPHANED STOP CANCELLED] {symbol} (order {stop_order_id})")

            except Exception as e:
                self.logger.error(f"Failed to cancel orphaned stop {stop_order_id} for {symbol}: {e}")
                conn.rollback()
                continue

        conn.close()

        self.logger.info(
            f"Orphaned stop cleanup complete: "
            f"{counts['cancelled']} cancelled, {counts['skipped']} skipped"
        )

        return counts
