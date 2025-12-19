"""
Automated Email Reporter - Sentinel Corporation
================================================
Sends comprehensive daily trading reports via email.

Features:
- Complete execution summary
- Portfolio holdings with P&L
- Trade details (buys and sells)
- Market regime analysis
- Performance metrics (daily, YTD)
- Emergency warnings
- Beautiful HTML formatting

Author: Claude Code (CC)
Date: 2025-11-25
"""

import sys
import smtplib
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config

logger = logging.getLogger('AutomatedEmailReporter')


class AutomatedEmailReporter:
    """
    Generates and sends comprehensive daily trading reports.
    """

    def __init__(self):
        self.sender_email = "wjcornelius@gmail.com"
        self.recipient_email = "wjcornelius@gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.app_password = config.GMAIL_APP_PASSWORD

    def send_daily_report(self, results: Dict) -> bool:
        """
        Generate and send daily trading report.

        Args:
            results: Complete trading results from AutomatedTradingRunner

        Returns:
            True if sent successfully
        """
        try:
            html_content = self._generate_html_report(results)
            subject = self._generate_subject(results)

            return self._send_email(subject, html_content)

        except Exception as e:
            logger.error(f"Failed to send daily report: {e}")
            return False

    def _generate_subject(self, results: Dict) -> str:
        """Generate email subject line"""
        status = results.get('status', 'UNKNOWN')
        portfolio = results.get('portfolio_state', {})

        daily_pl = portfolio.get('daily_pl', 0)
        daily_pl_pct = portfolio.get('daily_pl_pct', 0)

        if status == 'SUCCESS':
            if daily_pl >= 0:
                return f"📈 Sentinel Daily: +${daily_pl:,.2f} ({daily_pl_pct:+.2f}%) - {date.today().strftime('%b %d')}"
            else:
                return f"📉 Sentinel Daily: ${daily_pl:,.2f} ({daily_pl_pct:+.2f}%) - {date.today().strftime('%b %d')}"
        elif status == 'MARKET_CLOSED':
            return f"📊 Sentinel: Market Closed - {date.today().strftime('%b %d')}"
        elif status == 'ALREADY_TRADED':
            return f"📊 Sentinel: Already Traded - {date.today().strftime('%b %d')}"
        else:
            return f"⚠️ Sentinel Alert: {status} - {date.today().strftime('%b %d')}"

    def _generate_html_report(self, results: Dict) -> str:
        """Generate comprehensive HTML report"""
        status = results.get('status', 'UNKNOWN')
        portfolio = results.get('portfolio_state', {})
        regime = results.get('regime_analysis', {})
        plan = results.get('plan_summary', {})
        warnings = results.get('warnings', [])
        errors = results.get('errors', [])

        # Extract key metrics
        equity = portfolio.get('equity', 0)
        cash = portfolio.get('cash', 0)
        daily_pl = portfolio.get('daily_pl', 0)
        daily_pl_pct = portfolio.get('daily_pl_pct', 0)
        total_return = portfolio.get('total_return', 0)
        total_return_pct = portfolio.get('total_return_pct', 0)
        starting_capital = portfolio.get('starting_capital', 100000)
        positions = portfolio.get('positions', [])

        # Color coding
        daily_color = "#28a745" if daily_pl >= 0 else "#dc3545"
        total_color = "#28a745" if total_return >= 0 else "#dc3545"
        status_color = "#28a745" if status == 'SUCCESS' else "#ffc107" if status in ['MARKET_CLOSED', 'ALREADY_TRADED'] else "#dc3545"

        # Regime styling
        regime_name = regime.get('regime', 'UNKNOWN')
        regime_color = "#28a745" if regime_name == 'BULLISH' else "#dc3545" if regime_name == 'BEARISH' else "#6c757d"

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentinel Daily Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
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
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            letter-spacing: 2px;
        }}
        .header .date {{
            font-size: 16px;
            opacity: 0.9;
            margin-top: 8px;
        }}
        .status-banner {{
            background-color: {status_color};
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }}
        .content {{
            padding: 30px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #3949ab;
        }}
        .metric-card.highlight {{
            border-left-color: {daily_color};
        }}
        .metric-label {{
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .metric-value {{
            font-size: 28px;
            font-weight: bold;
            margin: 5px 0;
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
            color: #1a237e;
            border-bottom: 2px solid #3949ab;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        th {{
            background-color: #3949ab;
            color: white;
            padding: 12px 10px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 10px;
            border-bottom: 1px solid #e9ecef;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .positive {{ color: #28a745; font-weight: 600; }}
        .negative {{ color: #dc3545; font-weight: 600; }}
        .neutral {{ color: #6c757d; }}
        .warning-box {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        .error-box {{
            background-color: #f8d7da;
            border: 1px solid #dc3545;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        .regime-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            color: white;
            background-color: {regime_color};
        }}
        .trade-buy {{ background-color: #d4edda; }}
        .trade-sell {{ background-color: #f8d7da; }}
        .footer {{
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            color: #6c757d;
            font-size: 12px;
        }}
        @media (max-width: 600px) {{
            .metrics-grid {{ grid-template-columns: 1fr; }}
            table {{ font-size: 12px; }}
            th, td {{ padding: 8px 5px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SENTINEL CORPORATION</h1>
            <div class="date">{date.today().strftime('%A, %B %d, %Y')}</div>
        </div>

        <div class="status-banner">
            Automated Trading Status: {status}
        </div>

        <div class="content">
"""

        # Performance Metrics Section
        html += f"""
            <div class="metrics-grid">
                <div class="metric-card highlight">
                    <div class="metric-label">Today's P&L</div>
                    <div class="metric-value" style="color: {daily_color};">${daily_pl:,.2f}</div>
                    <div class="metric-subvalue" style="color: {daily_color};">({daily_pl_pct:+.2f}%)</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Total Return (YTD)</div>
                    <div class="metric-value" style="color: {total_color};">${total_return:,.2f}</div>
                    <div class="metric-subvalue" style="color: {total_color};">({total_return_pct:+.2f}%)</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Portfolio Value</div>
                    <div class="metric-value">${equity:,.2f}</div>
                    <div class="metric-subvalue">Started: ${starting_capital:,.2f}</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Cash Available</div>
                    <div class="metric-value">${cash:,.2f}</div>
                    <div class="metric-subvalue">{len(positions)} positions</div>
                </div>
            </div>
"""

        # Warnings Section
        if warnings:
            html += """
            <div class="section">
                <div class="section-title">⚠️ Warnings</div>
"""
            for warning in warnings:
                html += f"""
                <div class="warning-box">{warning}</div>
"""
            html += """
            </div>
"""

        # Errors Section
        if errors:
            html += """
            <div class="section">
                <div class="section-title">🚨 Errors</div>
"""
            for error in errors[:5]:  # Limit to 5 errors
                html += f"""
                <div class="error-box">{error}</div>
"""
            html += """
            </div>
"""

        # Market Regime Section
        if regime:
            html += f"""
            <div class="section">
                <div class="section-title">📊 Market Regime</div>
                <table>
                    <tr>
                        <td>Regime</td>
                        <td><span class="regime-badge">{regime.get('regime', 'N/A')}</span></td>
                    </tr>
                    <tr>
                        <td>Confidence</td>
                        <td>{regime.get('confidence', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td>SPY</td>
                        <td>${regime.get('spy_price', 0):.2f} ({regime.get('spy_change_pct', 0):+.2f}%)</td>
                    </tr>
                    <tr>
                        <td>VIX</td>
                        <td>{regime.get('vix_level', 0):.2f}</td>
                    </tr>
                    <tr>
                        <td>Recommendation</td>
                        <td>{regime.get('recommendation', 'N/A')}</td>
                    </tr>
                </table>
            </div>
"""

        # Trading Plan Section
        if plan:
            html += f"""
            <div class="section">
                <div class="section-title">📋 Trading Plan</div>
                <table>
                    <tr>
                        <td>Plan ID</td>
                        <td>{plan.get('plan_id', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td>Total Trades</td>
                        <td>{plan.get('total_trades', 0)}</td>
                    </tr>
                    <tr>
                        <td>Quality Score</td>
                        <td>{plan.get('quality_score', 0)}/100</td>
                    </tr>
                    <tr>
                        <td>CEO Rating</td>
                        <td>{plan.get('ceo_rating', 'N/A')}</td>
                    </tr>
                </table>
            </div>
"""

        # Trades Section - Categorize by actual outcome
        trades = results.get('trades_executed', [])
        if trades:
            # Categorize trades by status
            sells = [t for t in trades if t.get('action') == 'SELL']
            buys = [t for t in trades if t.get('action') == 'BUY']

            # Check verification to determine what actually filled
            verification = results.get('verification', {})
            positions_after = results.get('portfolio_state', {}).get('positions', [])
            position_tickers = {p['ticker'] for p in positions_after}

            # Categorize sells
            sells_filled = []
            sells_skipped = []
            for t in sells:
                if t.get('status') == 'SKIPPED':
                    sells_skipped.append(t)
                else:
                    # If the position is still there, sell didn't fill
                    if t.get('ticker') in position_tickers:
                        t['_unfilled_reason'] = 'Position still held'
                        sells_skipped.append(t)
                    else:
                        sells_filled.append(t)

            # Categorize buys
            buys_filled = []
            buys_pending = []
            for t in buys:
                if t.get('status') == 'SKIPPED':
                    buys_pending.append(t)
                else:
                    # If position exists, buy filled
                    if t.get('ticker') in position_tickers:
                        buys_filled.append(t)
                    else:
                        t['_unfilled_reason'] = 'Insufficient cash'
                        buys_pending.append(t)

            # Count totals
            total_filled = len(sells_filled) + len(buys_filled)
            total_pending = len(sells_skipped) + len(buys_pending)

            html += f"""
            <div class="section">
                <div class="section-title">📈 Trade Activity</div>
                <p style="margin-bottom: 15px; color: #6c757d;">
                    <strong>{total_filled}</strong> filled, <strong>{total_pending}</strong> pending/skipped out of {len(trades)} submitted
                </p>
"""
            # Sells section
            if sells:
                html += f"""
                <h4>Sells ({len(sells_filled)} filled, {len(sells_skipped)} skipped)</h4>
                <table>
                    <tr>
                        <th>Ticker</th>
                        <th>Status</th>
                        <th>Notes</th>
                    </tr>
"""
                for trade in sells_filled:
                    html += f"""
                    <tr class="trade-sell">
                        <td>{trade.get('ticker', 'N/A')}</td>
                        <td class="positive">FILLED</td>
                        <td>-</td>
                    </tr>
"""
                for trade in sells_skipped:
                    reason = trade.get('reason', trade.get('_unfilled_reason', 'Unknown'))
                    html += f"""
                    <tr style="background-color: #fff3cd;">
                        <td>{trade.get('ticker', 'N/A')}</td>
                        <td class="neutral">SKIPPED</td>
                        <td style="font-size: 12px;">{reason}</td>
                    </tr>
"""
                html += """
                </table>
"""

            # Buys section
            if buys:
                html += f"""
                <h4>Buys ({len(buys_filled)} filled, {len(buys_pending)} pending)</h4>
                <table>
                    <tr>
                        <th>Ticker</th>
                        <th>Status</th>
                        <th>Notes</th>
                    </tr>
"""
                for trade in buys_filled:
                    html += f"""
                    <tr class="trade-buy">
                        <td>{trade.get('ticker', 'N/A')}</td>
                        <td class="positive">FILLED</td>
                        <td>-</td>
                    </tr>
"""
                for trade in buys_pending:
                    reason = trade.get('reason', trade.get('_unfilled_reason', 'Pending'))
                    html += f"""
                    <tr style="background-color: #fff3cd;">
                        <td>{trade.get('ticker', 'N/A')}</td>
                        <td class="neutral">PENDING</td>
                        <td style="font-size: 12px;">{reason}</td>
                    </tr>
"""
                html += """
                </table>
"""
            html += """
            </div>
"""

        # Portfolio Holdings Section
        if positions:
            total_market_value = sum(p['market_value'] for p in positions)
            total_unrealized_pl = sum(p['unrealized_pl'] for p in positions)

            html += f"""
            <div class="section">
                <div class="section-title">💼 Portfolio Holdings ({len(positions)} positions)</div>
                <table>
                    <tr>
                        <th>Ticker</th>
                        <th style="text-align: right;">Shares</th>
                        <th style="text-align: right;">Entry</th>
                        <th style="text-align: right;">Current</th>
                        <th style="text-align: right;">Value</th>
                        <th style="text-align: right;">P&L</th>
                    </tr>
"""
            for pos in positions[:20]:  # Show top 20
                pnl = pos['unrealized_pl']
                pnl_class = 'positive' if pnl >= 0 else 'negative'

                html += f"""
                    <tr>
                        <td><strong>{pos['ticker']}</strong></td>
                        <td style="text-align: right;">{pos['shares']:,.0f}</td>
                        <td style="text-align: right;">${pos['entry_price']:.2f}</td>
                        <td style="text-align: right;">${pos['current_price']:.2f}</td>
                        <td style="text-align: right;">${pos['market_value']:,.2f}</td>
                        <td style="text-align: right;" class="{pnl_class}">${pnl:+,.2f}</td>
                    </tr>
"""

            total_pnl_class = 'positive' if total_unrealized_pl >= 0 else 'negative'
            html += f"""
                    <tr style="font-weight: bold; background-color: #f8f9fa;">
                        <td>TOTAL</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style="text-align: right;">${total_market_value:,.2f}</td>
                        <td style="text-align: right;" class="{total_pnl_class}">${total_unrealized_pl:+,.2f}</td>
                    </tr>
                </table>
            </div>
"""

        # Execution Details
        # Calculate actual fills vs submissions from trades_executed
        trades = results.get('trades_executed', [])
        positions_after = results.get('portfolio_state', {}).get('positions', [])
        position_tickers = {p['ticker'] for p in positions_after}

        # Count from trades_executed (more reliable than counts which may exclude skipped)
        all_sells = [t for t in trades if t.get('action') == 'SELL']
        all_buys = [t for t in trades if t.get('action') == 'BUY']
        sells_submitted = len(all_sells)
        buys_submitted = len(all_buys)

        # Count actual fills
        sells_filled = sum(1 for t in all_sells
                          if t.get('status') != 'SKIPPED'
                          and t.get('ticker') not in position_tickers)
        buys_filled = sum(1 for t in all_buys
                         if t.get('ticker') in position_tickers)

        html += f"""
            <div class="section">
                <div class="section-title">⚙️ Execution Details</div>
                <table>
                    <tr>
                        <td>Start Time</td>
                        <td>{results.get('start_time', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td>End Time</td>
                        <td>{results.get('end_time', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td>Duration</td>
                        <td>{results.get('duration_seconds', 0):.1f} seconds</td>
                    </tr>
                    <tr>
                        <td>Sells</td>
                        <td>{sells_filled} filled / {sells_submitted} submitted</td>
                    </tr>
                    <tr>
                        <td>Buys</td>
                        <td>{buys_filled} filled / {buys_submitted} submitted</td>
                    </tr>
                </table>
            </div>
"""

        # Footer
        html += f"""
        </div>

        <div class="footer">
            <p><strong>Sentinel Corporation</strong> - Automated Trading System</p>
            <p>Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="color: #999; font-size: 11px;">This is an automated report. Do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def _send_email(self, subject: str, html_content: str) -> bool:
        """Send HTML email via SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {self.recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False


# Test function
if __name__ == "__main__":
    # Create sample results for testing
    sample_results = {
        'date': date.today().strftime('%Y-%m-%d'),
        'status': 'SUCCESS',
        'start_time': datetime.now().isoformat(),
        'end_time': datetime.now().isoformat(),
        'duration_seconds': 45.2,
        'sells_count': 2,
        'buys_count': 3,
        'regime_analysis': {
            'regime': 'BULLISH',
            'confidence': 'HIGH',
            'spy_price': 595.50,
            'spy_change_pct': 0.85,
            'vix_level': 14.2,
            'recommendation': 'Full position sizing'
        },
        'plan_summary': {
            'plan_id': 'PLAN_20251125_TEST',
            'total_trades': 5,
            'quality_score': 82,
            'ceo_rating': 'GOOD'
        },
        'trades_executed': [
            {'ticker': 'OLD1', 'action': 'SELL'},
            {'ticker': 'OLD2', 'action': 'SELL'},
            {'ticker': 'NEW1', 'action': 'BUY'},
            {'ticker': 'NEW2', 'action': 'BUY'},
            {'ticker': 'NEW3', 'action': 'BUY'}
        ],
        'portfolio_state': {
            'equity': 105250.00,
            'cash': 15000.00,
            'starting_capital': 100000.00,
            'total_return': 5250.00,
            'total_return_pct': 5.25,
            'daily_pl': 325.00,
            'daily_pl_pct': 0.31,
            'position_count': 12,
            'positions': [
                {'ticker': 'AAPL', 'shares': 50, 'entry_price': 175.00, 'current_price': 180.25, 'market_value': 9012.50, 'unrealized_pl': 262.50},
                {'ticker': 'MSFT', 'shares': 25, 'entry_price': 380.00, 'current_price': 385.00, 'market_value': 9625.00, 'unrealized_pl': 125.00},
                {'ticker': 'NVDA', 'shares': 15, 'entry_price': 520.00, 'current_price': 510.00, 'market_value': 7650.00, 'unrealized_pl': -150.00}
            ]
        },
        'warnings': ['Test warning message'],
        'errors': []
    }

    reporter = AutomatedEmailReporter()

    # Generate HTML and save for preview
    html = reporter._generate_html_report(sample_results)
    preview_file = Path(__file__).parent.parent / "test_email_preview.html"
    preview_file.write_text(html)
    print(f"HTML preview saved to: {preview_file}")

    # Optionally send test email
    # reporter.send_daily_report(sample_results)
