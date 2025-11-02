"""
Market Status Module
====================
Determines if market is open, closed, or if trading already happened today.
Uses Alpaca Calendar API for market schedule (holidays, etc.)
"""

import os
import sys
from datetime import datetime, time, timedelta
import pytz

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class MarketStatus:
    """
    Handles all market hours and trading status logic.
    """

    def __init__(self, alpaca_api=None):
        """
        Initialize MarketStatus.

        Args:
            alpaca_api: Alpaca API client (optional, for calendar checks)
        """
        self.alpaca_api = alpaca_api
        self.eastern_tz = pytz.timezone('US/Eastern')

        # NYSE trading hours (US Eastern Time)
        self.market_open_time = time(9, 30)   # 9:30 AM ET
        self.market_close_time = time(16, 0)  # 4:00 PM ET

    def get_eastern_time_now(self):
        """
        Get current time in US/Eastern timezone.

        Returns:
            datetime: Current time in Eastern timezone
        """
        return datetime.now(self.eastern_tz)

    def is_market_day_today(self):
        """
        Check if today is a trading day (not weekend, not holiday).
        Uses Alpaca Calendar API if available, otherwise just checks weekend.

        Returns:
            bool: True if market is open today
        """
        eastern_now = self.get_eastern_time_now()
        today = eastern_now.date()

        # Check if weekend
        if eastern_now.weekday() >= 5:  # Saturday=5, Sunday=6
            return False

        # If Alpaca API is available, check calendar for holidays
        if self.alpaca_api:
            try:
                # Get calendar for today
                calendar = self.alpaca_api.get_calendar(
                    start=today.isoformat(),
                    end=today.isoformat()
                )

                # If calendar is empty, market is closed (holiday)
                if not calendar or len(calendar) == 0:
                    return False

                return True

            except Exception as e:
                print(f"Warning: Could not check Alpaca calendar: {e}")
                print("Falling back to weekend-only check")
                return True  # Assume open if can't check (not weekend)

        # If no Alpaca API, assume open (not weekend)
        return True

    def is_market_open_now(self):
        """
        Check if market is currently open (right now).

        Returns:
            bool: True if market is open right now
        """
        # First check if today is a trading day
        if not self.is_market_day_today():
            return False

        # Check if current time is within trading hours
        eastern_now = self.get_eastern_time_now()
        current_time = eastern_now.time()

        return self.market_open_time <= current_time < self.market_close_time

    def get_market_hours_today(self):
        """
        Get market open and close times for today.

        Returns:
            tuple: (open_time, close_time) as datetime objects in Eastern time,
                   or (None, None) if market is closed today
        """
        if not self.is_market_day_today():
            return (None, None)

        eastern_now = self.get_eastern_time_now()
        today = eastern_now.date()

        open_dt = self.eastern_tz.localize(
            datetime.combine(today, self.market_open_time)
        )
        close_dt = self.eastern_tz.localize(
            datetime.combine(today, self.market_close_time)
        )

        return (open_dt, close_dt)

    def already_traded_today(self):
        """
        Check if trading already happened today by querying Alpaca for today's orders.
        This is the GROUND TRUTH check - queries Alpaca API, not database.

        Returns:
            bool: True if orders were submitted today
        """
        if not self.alpaca_api:
            print("Warning: No Alpaca API client provided, cannot check if already traded")
            return False

        try:
            eastern_now = self.get_eastern_time_now()
            today_start = self.eastern_tz.localize(
                datetime.combine(eastern_now.date(), time(0, 0, 0))
            )

            # Get all orders submitted today (use AlpacaClient method)
            orders = self.alpaca_api.get_today_orders()

            # If any orders exist from today, we already traded
            if orders and len(orders) > 0:
                print(f"Found {len(orders)} order(s) submitted today")
                return True

            return False

        except Exception as e:
            print(f"Warning: Could not check Alpaca orders: {e}")
            return False  # Assume not traded if can't check

    def should_be_online(self):
        """
        Determine if SC should be in online (trading) mode.

        Logic:
        1. Market must be open today (not weekend, not holiday)
        2. Market must be currently open (9:30 AM - 4:00 PM ET)
        3. Must NOT have already traded today

        Returns:
            tuple: (should_be_online: bool, reason: str)
        """
        # Check if market day
        if not self.is_market_day_today():
            return (False, "Market is closed today (weekend or holiday)")

        # Check if market hours
        if not self.is_market_open_now():
            eastern_now = self.get_eastern_time_now()
            current_time = eastern_now.time()

            if current_time < self.market_open_time:
                return (False, f"Market not open yet (opens at {self.market_open_time.strftime('%I:%M %p')} ET)")
            else:
                return (False, f"Market is closed (closed at {self.market_close_time.strftime('%I:%M %p')} ET)")

        # Check if already traded
        if self.already_traded_today():
            return (False, "Already traded today")

        # All checks passed - should be online
        return (True, "Market is open and no trades submitted today")

    def get_status_summary(self):
        """
        Get a comprehensive status summary for display.

        Returns:
            dict: Status information
        """
        eastern_now = self.get_eastern_time_now()
        is_market_day = self.is_market_day_today()
        is_open_now = self.is_market_open_now()
        already_traded = self.already_traded_today()
        should_be_online, reason = self.should_be_online()
        market_hours = self.get_market_hours_today()

        return {
            'current_time_et': eastern_now.strftime('%Y-%m-%d %I:%M:%S %p %Z'),
            'is_market_day': is_market_day,
            'is_market_open_now': is_open_now,
            'market_open_time': market_hours[0].strftime('%I:%M %p ET') if market_hours[0] else 'N/A',
            'market_close_time': market_hours[1].strftime('%I:%M %p ET') if market_hours[1] else 'N/A',
            'already_traded_today': already_traded,
            'should_be_online': should_be_online,
            'reason': reason
        }

    def get_next_market_open(self):
        """
        Get the next market open time (useful for "market opens in X hours" messages).

        Returns:
            datetime: Next market open time, or None if can't determine
        """
        eastern_now = self.get_eastern_time_now()
        today = eastern_now.date()

        # Try today first
        if self.is_market_day_today():
            open_dt = self.eastern_tz.localize(
                datetime.combine(today, self.market_open_time)
            )

            if eastern_now < open_dt:
                return open_dt

        # Try next 7 days
        for days_ahead in range(1, 8):
            future_date = today + timedelta(days=days_ahead)
            future_dt = self.eastern_tz.localize(
                datetime.combine(future_date, time(0, 0, 0))
            )

            # Create a temporary MarketStatus for that day to check if it's a market day
            # (This is a bit hacky but works without changing system time)
            if future_dt.weekday() < 5:  # Not weekend
                open_dt = self.eastern_tz.localize(
                    datetime.combine(future_date, self.market_open_time)
                )
                return open_dt

        return None  # Couldn't find next open within 7 days


# Convenience functions for easy imports
def is_market_open_now(alpaca_api=None):
    """Check if market is open right now."""
    ms = MarketStatus(alpaca_api)
    return ms.is_market_open_now()


def is_market_day_today(alpaca_api=None):
    """Check if today is a trading day."""
    ms = MarketStatus(alpaca_api)
    return ms.is_market_day_today()


def already_traded_today(alpaca_api):
    """Check if already traded today (requires Alpaca API)."""
    ms = MarketStatus(alpaca_api)
    return ms.already_traded_today()


def should_be_online(alpaca_api):
    """Determine if should be in online mode (requires Alpaca API)."""
    ms = MarketStatus(alpaca_api)
    return ms.should_be_online()


def get_status_summary(alpaca_api=None):
    """Get comprehensive status summary."""
    ms = MarketStatus(alpaca_api)
    return ms.get_status_summary()


if __name__ == "__main__":
    # Test the market status module
    print("=" * 80)
    print("MARKET STATUS MODULE TEST")
    print("=" * 80)
    print()

    # Test without Alpaca API (basic functionality)
    ms = MarketStatus()
    status = ms.get_status_summary()

    print("Current Status:")
    print(f"  Current Time (ET):     {status['current_time_et']}")
    print(f"  Is Market Day:         {status['is_market_day']}")
    print(f"  Is Market Open Now:    {status['is_market_open_now']}")
    print(f"  Market Hours Today:    {status['market_open_time']} - {status['market_close_time']}")
    print(f"  Already Traded Today:  {status['already_traded_today']} (requires Alpaca API)")
    print(f"  Should Be Online:      {status['should_be_online']}")
    print(f"  Reason:                {status['reason']}")
    print()

    next_open = ms.get_next_market_open()
    if next_open:
        print(f"Next Market Open: {next_open.strftime('%Y-%m-%d %I:%M %p %Z')}")
    else:
        print("Could not determine next market open")

    print()
    print("=" * 80)
    print("Note: Connect Alpaca API for full functionality (holiday detection, trade checking)")
    print("=" * 80)
