"""
Mode Manager - Trading Session Control & Safety Gates
Operations Department - Sentinel Corporation

Responsibilities:
- Enforce market hours (9:30 AM - 4:00 PM ET, Mon-Fri)
- Track daily execution limit (1 execution per trading day)
- Validate plan freshness (4-hour expiration)
- Monitor portfolio losses (graduated circuit breaker)
- Provide market status information

Think of Mode Manager as SC's Floor Manager/Shift Supervisor:
- Controls access to the trading floor
- Enforces trading session rules
- Maintains trading session log
- Implements safety gates

Author: Claude Code
Date: November 7, 2025
"""

import sqlite3
import logging
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple
import pytz

logger = logging.getLogger(__name__)


class ModeManager:
    """
    Mode Manager - Trading Session Control & Safety

    Enforces:
    1. Market hours (9:30 AM - 4:00 PM ET)
    2. Daily execution limit (1 per day)
    3. Plan freshness (4-hour max age)
    4. Graduated circuit breaker (5%/10%/15% alerts)
    """

    def __init__(self, project_root: Path, alpaca_client=None):
        """
        Initialize Mode Manager

        Args:
            project_root: Path to Sentinel project root
            alpaca_client: Alpaca TradingClient for market calendar
        """
        self.project_root = project_root
        self.db_path = project_root / "sentinel.db"
        self.alpaca = alpaca_client
        self.plan_freshness_hours = 4

        # ET timezone for market hours
        self.et_tz = pytz.timezone('America/New_York')

        # Market hours (ET)
        self.market_open_time = (9, 30)   # 9:30 AM
        self.market_close_time = (16, 0)   # 4:00 PM
        self.warning_before_close_minutes = 15

        # Circuit breaker thresholds
        self.yellow_alert_pct = 5.0   # Informational
        self.orange_alert_pct = 10.0  # Block new BUYs
        self.red_alert_pct = 15.0     # Hard block, require override

        self._ensure_database_table()
        logger.info("Mode Manager initialized (Operations Department)")

    def _ensure_database_table(self):
        """Create trading_sessions table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trading_sessions (
                session_id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                plan_generated_at TEXT,
                plan_executed_at TEXT,
                market_status TEXT,
                trades_submitted INTEGER,
                user_override BOOLEAN DEFAULT 0,
                circuit_breaker_level TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Trading sessions table ready")

    def get_current_et_time(self) -> datetime:
        """Get current time in ET timezone"""
        utc_now = datetime.now(timezone.utc)
        et_now = utc_now.astimezone(self.et_tz)
        return et_now

    def is_market_open_now(self) -> Tuple[bool, str]:
        """
        Check if market is currently open

        Returns:
            (is_open, reason) - Boolean and explanation string
        """
        et_now = self.get_current_et_time()

        # Check if weekend
        if et_now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            next_open = self._get_next_market_open(et_now)
            return False, f"Weekend - Market opens {next_open}"

        # Check if within market hours (9:30 AM - 4:00 PM ET)
        current_time = (et_now.hour, et_now.minute)

        if current_time < self.market_open_time:
            # Before market open
            today_str = et_now.strftime("%A, %b %d")
            return False, f"Pre-market - Opens today at 9:30 AM ET ({today_str})"

        if current_time >= self.market_close_time:
            # After market close
            next_open = self._get_next_market_open(et_now)
            return False, f"After hours - Market opens {next_open}"

        # Market hours, check if it's a holiday
        if self.alpaca:
            try:
                from alpaca.trading.requests import GetCalendarRequest
                today = et_now.date()
                request = GetCalendarRequest(
                    start=today,
                    end=today
                )
                calendar = self.alpaca.get_calendar(request)

                if not calendar:
                    # No trading today (holiday)
                    next_open = self._get_next_market_open(et_now)
                    return False, f"Market holiday - Market opens {next_open}"

                # Check for early close
                close_time = calendar[0].close
                if close_time.hour < 16:  # Early close (e.g., 1:00 PM)
                    if current_time >= (close_time.hour, close_time.minute):
                        next_open = self._get_next_market_open(et_now)
                        return False, f"Early close today - Market opens {next_open}"

            except Exception as e:
                logger.warning(f"Could not verify market calendar: {e}")
                # Fall through to assume market is open during normal hours

        # Market is open!
        return True, "Market is OPEN"

    def _get_next_market_open(self, current_et: datetime) -> str:
        """
        Get next market open date and time

        Returns:
            Formatted string: "Monday, Nov 11 at 9:30 AM ET"
        """
        if self.alpaca:
            try:
                from alpaca.trading.requests import GetCalendarRequest
                # Check next 10 days
                end_date = (current_et + timedelta(days=10)).date()
                request = GetCalendarRequest(
                    start=current_et.date(),
                    end=end_date
                )
                calendar = self.alpaca.get_calendar(request)

                if calendar:
                    # Find next open day
                    for day in calendar:
                        open_datetime = day.open
                        if open_datetime > current_et:
                            return open_datetime.strftime("%A, %b %d at %I:%M %p ET").replace(' 0', ' ')

            except Exception as e:
                logger.warning(f"Could not get market calendar: {e}")

        # Fallback: Next weekday at 9:30 AM
        next_day = current_et + timedelta(days=1)
        while next_day.weekday() >= 5:  # Skip weekend
            next_day += timedelta(days=1)

        return next_day.strftime("%A, %b %d at 9:30 AM ET")

    def get_market_status_display(self) -> Dict:
        """
        Get comprehensive market status for display

        Returns:
            {
                'is_open': bool,
                'status': 'OPEN' | 'CLOSED',
                'message': str,
                'current_time_et': str,
                'next_open': str (if closed)
            }
        """
        is_open, reason = self.is_market_open_now()
        et_now = self.get_current_et_time()

        result = {
            'is_open': is_open,
            'status': 'OPEN' if is_open else 'CLOSED',
            'message': reason,
            'current_time_et': et_now.strftime("%I:%M %p ET").lstrip('0'),
            'current_date': et_now.strftime("%A, %B %d, %Y")
        }

        if not is_open:
            result['next_open'] = self._get_next_market_open(et_now)

        return result

    def has_traded_today(self) -> Tuple[bool, Optional[Dict]]:
        """
        Check if a plan has been executed today

        Returns:
            (has_traded, session_info)
        """
        today = date.today().isoformat()

        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT session_id, plan_executed_at, trades_submitted, market_status
            FROM trading_sessions
            WHERE date = ? AND plan_executed_at IS NOT NULL
            ORDER BY plan_executed_at DESC
            LIMIT 1
        """, (today,))

        row = cursor.fetchone()
        conn.close()

        if row:
            session_info = {
                'session_id': row[0],
                'executed_at': row[1],
                'trades_count': row[2],
                'market_status': row[3]
            }
            return True, session_info

        return False, None

    def record_plan_generation(self, plan_id: str) -> str:
        """
        Record that a trading plan was generated

        Returns:
            session_id
        """
        today = date.today().isoformat()
        now = datetime.now().isoformat()
        session_id = f"SESSION_{today}_{plan_id[:8]}"

        market_status = self.get_market_status_display()

        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO trading_sessions
            (session_id, date, plan_generated_at, market_status)
            VALUES (?, ?, ?, ?)
        """, (session_id, today, now, market_status['status']))

        conn.commit()
        conn.close()

        logger.info(f"Recorded plan generation: {session_id}")
        return session_id

    def record_plan_execution(self, session_id: str, trades_count: int,
                             user_override: bool = False, notes: str = None):
        """Record that a trading plan was executed"""
        now = datetime.now().isoformat()
        market_status = self.get_market_status_display()

        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE trading_sessions
            SET plan_executed_at = ?,
                trades_submitted = ?,
                market_status = ?,
                user_override = ?,
                notes = ?
            WHERE session_id = ?
        """, (now, trades_count, market_status['status'],
              1 if user_override else 0, notes, session_id))

        conn.commit()
        conn.close()

        logger.info(f"Recorded plan execution: {session_id} ({trades_count} trades)")

    def check_plan_freshness(self, plan_generated_at: datetime) -> Tuple[bool, str]:
        """
        Check if trading plan is still fresh

        Args:
            plan_generated_at: When plan was generated

        Returns:
            (is_fresh, message)
        """
        now = datetime.now()
        age = now - plan_generated_at
        age_hours = age.total_seconds() / 3600

        if age_hours > self.plan_freshness_hours:
            hours_ago = int(age_hours)
            return False, f"Plan is stale (generated {hours_ago} hours ago, limit {self.plan_freshness_hours} hours)"

        return True, f"Plan is fresh (generated {age_hours:.1f} hours ago)"

    def check_circuit_breaker(self, portfolio_loss_pct: float) -> Tuple[str, str, bool]:
        """
        Check graduated circuit breaker levels

        Args:
            portfolio_loss_pct: Portfolio daily loss percentage (positive number = loss)

        Returns:
            (level, message, allow_new_buys)
            level: 'NORMAL' | 'YELLOW' | 'ORANGE' | 'RED'
        """
        if portfolio_loss_pct < self.yellow_alert_pct:
            return 'NORMAL', 'Portfolio within normal range', True

        if portfolio_loss_pct < self.orange_alert_pct:
            # Yellow Alert: Informational only
            return 'YELLOW', f'YELLOW ALERT: Portfolio down {portfolio_loss_pct:.1f}% today - Monitor closely', True

        if portfolio_loss_pct < self.red_alert_pct:
            # Orange Alert: Block new BUYs, allow SELLs
            return 'ORANGE', f'ORANGE ALERT: Portfolio down {portfolio_loss_pct:.1f}% today - New BUY orders blocked', False

        # Red Alert: Hard block all new trades
        return 'RED', f'RED ALERT - Circuit Breaker Triggered: Portfolio down {portfolio_loss_pct:.1f}% today - All new trades blocked', False

    def can_execute_plan(self, plan_generated_at: datetime,
                         current_portfolio_loss_pct: float = 0.0,
                         allow_override: bool = True) -> Dict:
        """
        Comprehensive check: Can we execute a trading plan right now?

        Checks all gates:
        1. Market status (open/closed)
        2. Daily execution limit
        3. Plan freshness
        4. Circuit breaker

        Returns:
            {
                'can_execute': bool,
                'gates_passed': [list of passed gates],
                'gates_failed': [list of failed gates with reasons],
                'warnings': [list of warnings],
                'requires_override': bool,
                'recommendation': str
            }
        """
        result = {
            'can_execute': True,
            'gates_passed': [],
            'gates_failed': [],
            'warnings': [],
            'requires_override': False,
            'recommendation': ''
        }

        # Gate 1: Market Status
        is_open, reason = self.is_market_open_now()
        if is_open:
            result['gates_passed'].append(f"[OK] Market Status: {reason}")
        else:
            result['can_execute'] = False
            result['gates_failed'].append(f"[BLOCKED] Market Status: {reason}")

        # Gate 2: Daily Execution Limit
        has_traded, session = self.has_traded_today()
        if not has_traded:
            result['gates_passed'].append("[OK] Daily Limit: No execution today (0/1 used)")
        else:
            if allow_override:
                result['requires_override'] = True
                result['warnings'].append(
                    f"Already executed plan today at {session['executed_at']} "
                    f"({session['trades_count']} trades) - Override available"
                )
            else:
                result['can_execute'] = False
                result['gates_failed'].append(
                    f"[BLOCKED] Daily Limit: Already executed at {session['executed_at']} "
                    f"({session['trades_count']} trades)"
                )

        # Gate 3: Plan Freshness
        is_fresh, freshness_msg = self.check_plan_freshness(plan_generated_at)
        if is_fresh:
            result['gates_passed'].append(f"[OK] Plan Freshness: {freshness_msg}")
        else:
            result['requires_override'] = True
            result['warnings'].append(freshness_msg)

        # Gate 4: Circuit Breaker
        cb_level, cb_msg, allow_buys = self.check_circuit_breaker(current_portfolio_loss_pct)

        if cb_level == 'NORMAL':
            result['gates_passed'].append("[OK] Circuit Breaker: Normal operations")
        elif cb_level == 'YELLOW':
            result['gates_passed'].append(f"[OK] Circuit Breaker: {cb_msg}")
            result['warnings'].append(cb_msg)
        elif cb_level == 'ORANGE':
            result['warnings'].append(cb_msg)
            result['warnings'].append("New BUY orders will be blocked (SELLs allowed)")
        elif cb_level == 'RED':
            if allow_override:
                result['requires_override'] = True
                result['warnings'].append(cb_msg)
                result['warnings'].append("CEO override required to proceed")
            else:
                result['can_execute'] = False
                result['gates_failed'].append(f"[BLOCKED] {cb_msg}")

        # Generate recommendation
        if not result['can_execute']:
            result['recommendation'] = "BLOCKED - Cannot execute trades"
        elif result['requires_override']:
            result['recommendation'] = "CAUTION - Override required"
        elif result['warnings']:
            result['recommendation'] = "PROCEED WITH CAUTION"
        else:
            result['recommendation'] = "CLEAR TO TRADE"

        return result


if __name__ == "__main__":
    # Test Mode Manager
    logging.basicConfig(level=logging.INFO)

    project_root = Path("C:/Users/wjcor/OneDrive/Desktop/Sentinel")
    mm = ModeManager(project_root)

    print("\n" + "=" * 80)
    print("MODE MANAGER TEST")
    print("=" * 80)

    # Test market status
    status = mm.get_market_status_display()
    print(f"\nMarket Status: {status['status']}")
    print(f"Message: {status['message']}")
    print(f"Current Time: {status['current_time_et']}")

    # Test daily limit
    has_traded, session = mm.has_traded_today()
    print(f"\nHas traded today: {has_traded}")
    if session:
        print(f"Session: {session}")

    # Test circuit breaker
    for loss in [0, 6, 11, 16]:
        level, msg, allow_buys = mm.check_circuit_breaker(loss)
        print(f"\nLoss {loss}%: {level} - {msg}")
        print(f"  Allow new BUYs: {allow_buys}")

    # Test comprehensive check
    plan_time = datetime.now() - timedelta(hours=2)
    result = mm.can_execute_plan(plan_time, current_portfolio_loss_pct=0)

    print(f"\n\nComprehensive Execution Check:")
    print(f"Can Execute: {result['can_execute']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nPassed Gates:")
    for gate in result['gates_passed']:
        print(f"  {gate}")
    print(f"\nFailed Gates:")
    for gate in result['gates_failed']:
        print(f"  {gate}")
    print(f"\nWarnings:")
    for warning in result['warnings']:
        print(f"  {warning}")
