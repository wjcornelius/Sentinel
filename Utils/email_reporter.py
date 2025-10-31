"""
Email Reporter - Week 7 Day 3
Sends HTML-formatted daily executive summaries via email

Features:
- Beautiful HTML templates with inline CSS
- Color-coded performance metrics
- Embedded tables for positions and trades
- Mobile-responsive design
- SMTP support for Gmail, Outlook, and custom servers
- Automated daily delivery

Author: Claude Code (CC)
Week: 7 Day 3
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Departments.Executive.executive_department import ExecutiveDepartment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class EmailReporter:
    """
    Sends HTML-formatted executive summary reports via email

    Features:
    - Professional HTML templates with inline CSS
    - Color-coded performance metrics
    - SMTP support (Gmail, Outlook, custom)
    - Attachment support for CSV exports
    """

    def __init__(self,
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587,
                 sender_email: str = None,
                 sender_password: str = None,
                 use_tls: bool = True):
        """
        Initialize email reporter

        Args:
            smtp_server: SMTP server address (default: Gmail)
            smtp_port: SMTP port (default: 587 for TLS)
            sender_email: Sender email address
            sender_password: Sender email password (or app password)
            use_tls: Use TLS encryption (default: True)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.use_tls = use_tls
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info(f"EmailReporter initialized: server={smtp_server}:{smtp_port}, tls={use_tls}")

    def generate_html_report(self, data: Dict) -> str:
        """
        Generate HTML-formatted executive summary report

        Args:
            data: Dashboard data from ExecutiveDepartment.get_realtime_dashboard_data()

        Returns:
            HTML string with inline CSS
        """
        performance = data.get('performance', {})
        positions = data.get('open_positions', [])
        health = data.get('system_health', {})
        best_worst = data.get('best_worst_trades', {})

        # Extract performance metrics
        daily_pnl = performance.get('daily_pnl', 0.0)
        daily_pnl_pct = performance.get('daily_pnl_pct', 0.0)
        realized_pnl = performance.get('realized_pnl', 0.0)
        unrealized_pnl = performance.get('unrealized_pnl', 0.0)
        sharpe = performance.get('sharpe_ratio_30d', 0.0)
        win_rate = performance.get('win_rate_30d', 0.0)
        max_dd = performance.get('max_drawdown', 0.0)
        alpha = performance.get('alpha_vs_spy', 0.0)

        # Determine colors
        pnl_color = "#28a745" if daily_pnl >= 0 else "#dc3545"  # green/red
        sharpe_color = "#28a745" if sharpe > 2.0 else "#ffc107" if sharpe > 1.0 else "#dc3545"
        win_rate_color = "#28a745" if win_rate >= 60 else "#ffc107" if win_rate >= 50 else "#dc3545"
        alpha_color = "#28a745" if alpha > 0 else "#dc3545"

        # Build HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel Corporation - Daily Executive Summary</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #007bff;
            margin: 0;
            font-size: 28px;
        }}
        .header .subtitle {{
            color: #6c757d;
            font-size: 14px;
            margin-top: 5px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 15px;
            border-left: 4px solid #007bff;
        }}
        .metric-label {{
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-subvalue {{
            font-size: 14px;
            color: #6c757d;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th {{
            background-color: #007bff;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #e9ecef;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .positive {{
            color: #28a745;
            font-weight: 600;
        }}
        .negative {{
            color: #dc3545;
            font-weight: 600;
        }}
        .warning {{
            color: #ffc107;
            font-weight: 600;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status-healthy {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status-degraded {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .status-unhealthy {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .status-nodata {{
            background-color: #e2e3e5;
            color: #383d41;
        }}
        .footer {{
            text-align: center;
            color: #6c757d;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }}
        @media (max-width: 600px) {{
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            table {{
                font-size: 12px;
            }}
            th, td {{
                padding: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SENTINEL CORPORATION</h1>
            <div class="subtitle">Daily Executive Summary - {datetime.now().strftime('%B %d, %Y')}</div>
        </div>

        <!-- Performance Metrics -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Daily P&L</div>
                <div class="metric-value" style="color: {pnl_color};">${daily_pnl:,.2f}</div>
                <div class="metric-subvalue" style="color: {pnl_color};">({daily_pnl_pct:+.2f}%)</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Sharpe Ratio (30d)</div>
                <div class="metric-value" style="color: {sharpe_color};">{sharpe:.3f}</div>
                <div class="metric-subvalue">Risk-Adjusted Returns</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Win Rate (30d)</div>
                <div class="metric-value" style="color: {win_rate_color};">{win_rate:.1f}%</div>
                <div class="metric-subvalue">Profitable Trades</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Alpha vs SPY (30d)</div>
                <div class="metric-value" style="color: {alpha_color};">{alpha:+.2f}%</div>
                <div class="metric-subvalue">Market Outperformance</div>
            </div>
        </div>

        <!-- P&L Breakdown -->
        <div class="section">
            <div class="section-title">P&L Breakdown</div>
            <table>
                <tr>
                    <th>Category</th>
                    <th style="text-align: right;">Amount</th>
                </tr>
                <tr>
                    <td>Realized P&L</td>
                    <td style="text-align: right;" class="{'positive' if realized_pnl >= 0 else 'negative'}">${realized_pnl:,.2f}</td>
                </tr>
                <tr>
                    <td>Unrealized P&L</td>
                    <td style="text-align: right;" class="{'positive' if unrealized_pnl >= 0 else 'negative'}">${unrealized_pnl:,.2f}</td>
                </tr>
                <tr style="font-weight: bold; background-color: #f8f9fa;">
                    <td>Total P&L</td>
                    <td style="text-align: right;" class="{'positive' if daily_pnl >= 0 else 'negative'}">${daily_pnl:,.2f}</td>
                </tr>
            </table>
        </div>

        <!-- Open Positions -->
        <div class="section">
            <div class="section-title">Open Positions ({len(positions)})</div>
            <table>
                <tr>
                    <th>Ticker</th>
                    <th style="text-align: right;">Shares</th>
                    <th style="text-align: right;">Entry Price</th>
                    <th style="text-align: right;">Current Price</th>
                    <th style="text-align: right;">Position Value</th>
                    <th style="text-align: right;">Unrealized P&L</th>
                </tr>
"""

        # Add position rows
        total_value = 0.0
        total_unrealized = 0.0

        for pos in positions[:10]:  # Show top 10 positions
            ticker = pos['ticker']
            shares = pos['shares']
            entry_price = pos['entry_price']
            current_price = pos.get('current_price', entry_price)
            position_value = shares * current_price
            position_pnl = shares * (current_price - entry_price)

            total_value += position_value
            total_unrealized += position_pnl

            pnl_class = 'positive' if position_pnl >= 0 else 'negative'

            html += f"""
                <tr>
                    <td><strong>{ticker}</strong></td>
                    <td style="text-align: right;">{shares:,}</td>
                    <td style="text-align: right;">${entry_price:.2f}</td>
                    <td style="text-align: right;">${current_price:.2f}</td>
                    <td style="text-align: right;">${position_value:,.2f}</td>
                    <td style="text-align: right;" class="{pnl_class}">${position_pnl:,.2f}</td>
                </tr>
"""

        # Add totals row
        total_class = 'positive' if total_unrealized >= 0 else 'negative'
        html += f"""
                <tr style="font-weight: bold; background-color: #f8f9fa;">
                    <td>TOTAL</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td style="text-align: right;">${total_value:,.2f}</td>
                    <td style="text-align: right;" class="{total_class}">${total_unrealized:,.2f}</td>
                </tr>
            </table>
        </div>
"""

        # System Health
        departments = health.get('departments', {})
        html += f"""
        <div class="section">
            <div class="section-title">System Health</div>
            <table>
                <tr>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Last Activity</th>
                </tr>
"""

        for dept_name, dept_status in departments.items():
            status = dept_status.get('status', 'unknown')
            last_activity = dept_status.get('last_activity', 'N/A')

            if last_activity and last_activity != 'N/A':
                try:
                    dt = datetime.fromisoformat(last_activity)
                    last_activity = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass

            # Status badge
            status_class_map = {
                'healthy': 'status-healthy',
                'degraded': 'status-degraded',
                'unhealthy': 'status-unhealthy',
                'no_data': 'status-nodata'
            }
            badge_class = status_class_map.get(status, 'status-nodata')

            dept_display = dept_name.replace('_', ' ').title()

            html += f"""
                <tr>
                    <td>{dept_display}</td>
                    <td><span class="status-badge {badge_class}">{status.upper().replace('_', ' ')}</span></td>
                    <td>{last_activity}</td>
                </tr>
"""

        html += """
            </table>
        </div>

        <div class="footer">
            <p><strong>Sentinel Corporation</strong> - Automated Trading System</p>
            <p>This report was automatically generated by the Executive Department</p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def send_email(self,
                   recipient_email: str,
                   subject: str,
                   html_content: str,
                   attachments: List[Path] = None) -> bool:
        """
        Send email via SMTP

        Args:
            recipient_email: Recipient email address
            subject: Email subject line
            html_content: HTML content of email
            attachments: Optional list of file paths to attach

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Add attachments if provided
            if attachments:
                for attachment_path in attachments:
                    if attachment_path.exists():
                        with open(attachment_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={attachment_path.name}'
                            )
                            msg.attach(part)

            # Send via SMTP
            self.logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()

                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)

                server.send_message(msg)

            self.logger.info(f"Email sent successfully to {recipient_email}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    def send_daily_summary(self,
                          recipient_email: str,
                          executive_dept: ExecutiveDepartment) -> bool:
        """
        Generate and send daily executive summary email

        Args:
            recipient_email: Recipient email address
            executive_dept: ExecutiveDepartment instance for fetching data

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Fetch dashboard data
            self.logger.info("Fetching dashboard data for email report")
            data = executive_dept.get_realtime_dashboard_data()

            # Generate HTML report
            html_content = self.generate_html_report(data)

            # Create subject line
            daily_pnl = data['performance']['daily_pnl']
            daily_pnl_pct = data['performance']['daily_pnl_pct']

            if daily_pnl >= 0:
                subject = f"📈 Sentinel Daily Summary: +${daily_pnl:,.2f} ({daily_pnl_pct:+.2f}%)"
            else:
                subject = f"📉 Sentinel Daily Summary: ${daily_pnl:,.2f} ({daily_pnl_pct:+.2f}%)"

            # Send email
            return self.send_email(recipient_email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Failed to send daily summary: {e}")
            return False


# Test and standalone usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sentinel Email Reporter")
    parser.add_argument('--to', type=str, required=True, help='Recipient email address')
    parser.add_argument('--from', dest='from_email', type=str, required=True, help='Sender email address')
    parser.add_argument('--password', type=str, required=True, help='Sender email password (or app password)')
    parser.add_argument('--server', type=str, default='smtp.gmail.com', help='SMTP server (default: Gmail)')
    parser.add_argument('--port', type=int, default=587, help='SMTP port (default: 587)')
    parser.add_argument('--db', type=str, default=None, help='Path to Sentinel database')
    parser.add_argument('--test-html', action='store_true', help='Generate HTML file instead of sending email')

    args = parser.parse_args()

    # Initialize email reporter
    reporter = EmailReporter(
        smtp_server=args.server,
        smtp_port=args.port,
        sender_email=args.from_email,
        sender_password=args.password
    )

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

    if args.test_html:
        # Generate HTML and save to file
        print("Generating HTML report...")
        data = executive.get_realtime_dashboard_data()
        html = reporter.generate_html_report(data)

        output_file = project_root / "test_email_report.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"HTML report saved to: {output_file}")
        print("Open this file in a web browser to preview the email.")
    else:
        # Send email
        print(f"Sending daily summary to {args.to}...")
        success = reporter.send_daily_summary(args.to, executive)

        if success:
            print("[OK] Email sent successfully!")
        else:
            print("[FAIL] Failed to send email. Check logs for details.")
