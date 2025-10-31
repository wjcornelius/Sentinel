"""
SMS Alerter - Week 7 Day 4
Sends SMS alerts via Twilio for urgent portfolio notifications

Features:
- Twilio SMS integration
- Smart alert thresholds (daily P&L moves, milestones, health warnings)
- Alert cooldown to prevent spam
- Quiet hours (no alerts at night)
- Desktop launcher for easy testing

Author: Claude Code (CC)
Week: 7 Day 4
"""

import sys
from pathlib import Path
from datetime import datetime, time
from typing import Dict, List, Optional
import logging

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Twilio imports
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    logging.warning("Twilio not installed. Run: pip install twilio")

from Departments.Executive.executive_department import ExecutiveDepartment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class SMSAlerter:
    """
    Sends SMS alerts via Twilio for urgent portfolio notifications

    Features:
    - Smart alert thresholds (P&L moves, milestones, health warnings)
    - Alert cooldown (prevents spam)
    - Quiet hours (no alerts at night)
    - Simple test interface
    """

    def __init__(self,
                 account_sid: str,
                 auth_token: str,
                 from_phone: str,
                 to_phone: str,
                 quiet_hours_start: time = time(22, 0),  # 10 PM
                 quiet_hours_end: time = time(8, 0),     # 8 AM
                 cooldown_minutes: int = 60):
        """
        Initialize SMS alerter

        Args:
            account_sid: Twilio account SID
            auth_token: Twilio auth token
            from_phone: Twilio phone number (e.g., +15592725166)
            to_phone: Recipient phone number (e.g., +14155312139)
            quiet_hours_start: Start of quiet hours (no alerts)
            quiet_hours_end: End of quiet hours
            cooldown_minutes: Minimum minutes between alerts (default: 60)
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_phone = from_phone
        self.to_phone = to_phone
        self.quiet_hours_start = quiet_hours_start
        self.quiet_hours_end = quiet_hours_end
        self.cooldown_minutes = cooldown_minutes
        self.logger = logging.getLogger(self.__class__.__name__)

        # Alert tracking
        self.last_alert_time = {}  # Track last alert time by alert type

        # Initialize Twilio client
        if TWILIO_AVAILABLE:
            self.client = Client(account_sid, auth_token)
            self.logger.info(f"SMSAlerter initialized: from={from_phone}, to={to_phone}")
        else:
            self.client = None
            self.logger.warning("Twilio not available - SMS alerts disabled")

    def is_quiet_hours(self) -> bool:
        """
        Check if current time is within quiet hours

        Returns:
            True if in quiet hours, False otherwise
        """
        now = datetime.now().time()

        # Handle quiet hours that span midnight
        if self.quiet_hours_start > self.quiet_hours_end:
            # Example: 10 PM to 8 AM (spans midnight)
            return now >= self.quiet_hours_start or now < self.quiet_hours_end
        else:
            # Example: 10 PM to 11 PM (same day)
            return self.quiet_hours_start <= now < self.quiet_hours_end

    def can_send_alert(self, alert_type: str) -> bool:
        """
        Check if alert can be sent (not in cooldown or quiet hours)

        Args:
            alert_type: Type of alert (e.g., 'daily_pnl', 'milestone', 'health')

        Returns:
            True if alert can be sent, False otherwise
        """
        # Check quiet hours
        if self.is_quiet_hours():
            self.logger.info(f"Alert blocked: quiet hours ({alert_type})")
            return False

        # Check cooldown
        if alert_type in self.last_alert_time:
            last_alert = self.last_alert_time[alert_type]
            minutes_since = (datetime.now() - last_alert).total_seconds() / 60

            if minutes_since < self.cooldown_minutes:
                self.logger.info(f"Alert blocked: cooldown ({alert_type}, {minutes_since:.1f} min ago)")
                return False

        return True

    def send_sms(self, message: str, alert_type: str = 'general', override_quiet: bool = False) -> bool:
        """
        Send SMS alert via Twilio

        Args:
            message: SMS message text (max 160 characters recommended)
            alert_type: Type of alert for cooldown tracking
            override_quiet: Send even during quiet hours (use sparingly!)

        Returns:
            True if sent successfully, False otherwise
        """
        if not TWILIO_AVAILABLE or not self.client:
            self.logger.error("Twilio not available - cannot send SMS")
            return False

        # Check if alert can be sent
        if not override_quiet and not self.can_send_alert(alert_type):
            return False

        try:
            # Send SMS via Twilio
            self.logger.info(f"Sending SMS alert: {alert_type}")

            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=self.to_phone
            )

            # Update last alert time
            self.last_alert_time[alert_type] = datetime.now()

            self.logger.info(f"SMS sent successfully: {message_obj.sid}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send SMS: {e}")
            return False

    def check_and_alert(self, data: Dict) -> List[str]:
        """
        Check portfolio data and send alerts if thresholds exceeded

        Args:
            data: Dashboard data from ExecutiveDepartment.get_realtime_dashboard_data()

        Returns:
            List of alert messages sent
        """
        alerts_sent = []
        performance = data.get('performance', {})
        health = data.get('system_health', {})

        # Alert 1: Large daily P&L moves (>5%)
        daily_pnl_pct = performance.get('daily_pnl_pct', 0.0)
        daily_pnl = performance.get('daily_pnl', 0.0)

        if abs(daily_pnl_pct) >= 5.0:
            direction = "UP" if daily_pnl_pct > 0 else "DOWN"
            emoji = "🚀" if daily_pnl_pct > 0 else "⚠️"

            message = (
                f"{emoji} SENTINEL ALERT\n"
                f"Portfolio {direction} {abs(daily_pnl_pct):.1f}%\n"
                f"Daily P&L: ${daily_pnl:,.0f}\n"
                f"Time: {datetime.now().strftime('%I:%M %p')}"
            )

            if self.send_sms(message, alert_type='daily_pnl'):
                alerts_sent.append(f"Large P&L move: {daily_pnl_pct:+.1f}%")

        # Alert 2: Portfolio milestones ($100K, $250K, $500K, $1M)
        total_value = sum(pos['shares'] * pos.get('current_price', pos['entry_price'])
                         for pos in data.get('open_positions', []))

        milestones = [100000, 250000, 500000, 1000000]
        for milestone in milestones:
            if 0.98 * milestone <= total_value <= 1.02 * milestone:  # Within 2% of milestone
                message = (
                    f"🎉 SENTINEL MILESTONE\n"
                    f"Portfolio value: ${total_value:,.0f}\n"
                    f"Milestone reached: ${milestone:,.0f}\n"
                    f"Time: {datetime.now().strftime('%I:%M %p')}"
                )

                if self.send_sms(message, alert_type=f'milestone_{milestone}'):
                    alerts_sent.append(f"Milestone: ${milestone:,.0f}")
                    break  # Only send one milestone alert

        # Alert 3: System health warnings (unhealthy departments)
        departments = health.get('departments', {})
        unhealthy = [dept for dept, status in departments.items()
                    if status.get('status') == 'unhealthy']

        if unhealthy:
            dept_list = ', '.join(d.replace('_', ' ').title() for d in unhealthy[:3])
            message = (
                f"⚠️ SENTINEL HEALTH WARNING\n"
                f"Unhealthy departments: {dept_list}\n"
                f"Action required!\n"
                f"Time: {datetime.now().strftime('%I:%M %p')}"
            )

            if self.send_sms(message, alert_type='health_warning'):
                alerts_sent.append(f"Health warning: {len(unhealthy)} dept(s)")

        # Alert 4: Win rate drops below 50% (with 10+ trades)
        win_rate = performance.get('win_rate_30d', 100.0)
        # Note: We'd need to query trade count, but for now use simple threshold
        if win_rate < 50.0:
            message = (
                f"⚠️ SENTINEL PERFORMANCE ALERT\n"
                f"Win rate dropped to {win_rate:.1f}%\n"
                f"Review strategy!\n"
                f"Time: {datetime.now().strftime('%I:%M %p')}"
            )

            if self.send_sms(message, alert_type='win_rate'):
                alerts_sent.append(f"Low win rate: {win_rate:.1f}%")

        # Alert 5: Sharpe ratio drops below 1.0 (poor risk-adjusted returns)
        sharpe = performance.get('sharpe_ratio_30d', 0.0)
        if sharpe < 1.0 and sharpe > 0:  # Only if we have valid data
            message = (
                f"⚠️ SENTINEL RISK ALERT\n"
                f"Sharpe ratio: {sharpe:.2f}\n"
                f"Risk-adjusted returns low!\n"
                f"Time: {datetime.now().strftime('%I:%M %p')}"
            )

            if self.send_sms(message, alert_type='sharpe_ratio'):
                alerts_sent.append(f"Low Sharpe: {sharpe:.2f}")

        return alerts_sent

    def send_test_alert(self) -> bool:
        """
        Send a test SMS to verify Twilio configuration

        Returns:
            True if sent successfully, False otherwise
        """
        message = (
            f"✅ SENTINEL TEST ALERT\n"
            f"SMS system working!\n"
            f"Time: {datetime.now().strftime('%I:%M %p')}\n"
            f"Ready for live alerts."
        )

        return self.send_sms(message, alert_type='test', override_quiet=True)

    def send_daily_summary_sms(self, data: Dict) -> bool:
        """
        Send brief daily summary via SMS (for end-of-day)

        Args:
            data: Dashboard data from ExecutiveDepartment

        Returns:
            True if sent successfully, False otherwise
        """
        performance = data.get('performance', {})

        daily_pnl = performance.get('daily_pnl', 0.0)
        daily_pnl_pct = performance.get('daily_pnl_pct', 0.0)
        sharpe = performance.get('sharpe_ratio_30d', 0.0)
        win_rate = performance.get('win_rate_30d', 0.0)

        emoji = "🚀" if daily_pnl >= 0 else "📉"

        message = (
            f"{emoji} SENTINEL DAILY SUMMARY\n"
            f"P&L: ${daily_pnl:,.0f} ({daily_pnl_pct:+.1f}%)\n"
            f"Sharpe: {sharpe:.1f} | Win: {win_rate:.0f}%\n"
            f"{datetime.now().strftime('%b %d, %Y')}"
        )

        return self.send_sms(message, alert_type='daily_summary', override_quiet=False)


# Test and standalone usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sentinel SMS Alerter")
    parser.add_argument('--test', action='store_true', help='Send test SMS')
    parser.add_argument('--check', action='store_true', help='Check portfolio and send alerts if needed')
    parser.add_argument('--summary', action='store_true', help='Send daily summary SMS')
    parser.add_argument('--db', type=str, default=None, help='Path to Sentinel database')

    args = parser.parse_args()

    # Load Twilio credentials from config
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import config

        account_sid = config.TWILIO_ACCOUNT_SID
        auth_token = config.TWILIO_AUTH_TOKEN
        from_phone = config.TWILIO_PHONE_NUMBER
        to_phone = config.RECIPIENT_PHONE_NUMBER

        print("=" * 80)
        print("SENTINEL SMS ALERTER")
        print("=" * 80)
        print(f"From: {from_phone}")
        print(f"To: {to_phone}")
        print()

    except ImportError:
        print("ERROR: config.py not found!")
        print("Make sure config.py exists with Twilio credentials.")
        sys.exit(1)

    # Initialize SMS alerter
    alerter = SMSAlerter(
        account_sid=account_sid,
        auth_token=auth_token,
        from_phone=from_phone,
        to_phone=to_phone,
        quiet_hours_start=time(22, 0),  # 10 PM
        quiet_hours_end=time(8, 0),      # 8 AM
        cooldown_minutes=60
    )

    if args.test:
        # Send test SMS
        print("Sending test SMS...")
        success = alerter.send_test_alert()

        if success:
            print("[OK] Test SMS sent successfully!")
            print(f"Check your phone: {to_phone}")
        else:
            print("[FAIL] Failed to send test SMS")
            print("Check your Twilio credentials in config.py")

    elif args.check or args.summary:
        # Initialize Executive Department
        project_root = Path(__file__).parent.parent
        db_path = Path(args.db) if args.db else project_root / "sentinel.db"
        messages_dir = project_root / "Messages"
        reports_dir = project_root / "Reports"

        executive = ExecutiveDepartment(
            db_path=db_path,
            messages_dir=messages_dir,
            reports_dir=reports_dir
        )

        # Fetch dashboard data
        print("Fetching portfolio data...")
        data = executive.get_realtime_dashboard_data()

        if args.check:
            # Check and send alerts
            print("\nChecking alert thresholds...")
            alerts = alerter.check_and_alert(data)

            if alerts:
                print(f"\n[OK] Sent {len(alerts)} alert(s):")
                for alert in alerts:
                    print(f"  - {alert}")
            else:
                print("\n[OK] No alerts triggered (all thresholds OK)")

        elif args.summary:
            # Send daily summary
            print("\nSending daily summary SMS...")
            success = alerter.send_daily_summary_sms(data)

            if success:
                print("[OK] Daily summary sent successfully!")
            else:
                print("[FAIL] Failed to send daily summary")

    else:
        # Show usage
        print("\nUsage:")
        print("  --test      Send test SMS to verify Twilio setup")
        print("  --check     Check portfolio and send alerts if thresholds exceeded")
        print("  --summary   Send brief daily summary SMS")
        print()
        print("Examples:")
        print("  python Utils/sms_alerter.py --test")
        print("  python Utils/sms_alerter.py --check")
        print("  python Utils/sms_alerter.py --summary")
        print()
        print("=" * 80)
