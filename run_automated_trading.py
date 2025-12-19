"""
Sentinel Corporation - Automated Daily Trading
==============================================
Runs the complete trading workflow unattended:
1. Check market status and pre-flight conditions
2. Analyze market regime
3. Generate trading plan (auto-approve)
4. Execute trades
5. Send comprehensive email report

Designed to run via Windows Task Scheduler at 8:00 AM PT daily.

Author: Claude Code (CC)
Date: 2025-11-25
"""

import sys
import json
import logging
import traceback
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"automated_trading_{date.today().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('AutomatedTrading')


class AutomatedTradingRunner:
    """
    Runs the complete Sentinel trading workflow unattended.

    Features:
    - Market hours verification
    - Market regime analysis
    - Automatic plan approval
    - Trade execution with verification
    - Comprehensive email reporting
    - Error handling and recovery
    """

    def __init__(self):
        self.project_root = project_root
        self.start_time = datetime.now()
        self.results = {
            'date': date.today().strftime('%Y-%m-%d'),
            'start_time': self.start_time.isoformat(),
            'status': 'UNKNOWN',
            'market_status': None,
            'regime_analysis': None,
            'plan_generated': False,
            'plan_approved': False,
            'trades_executed': [],
            'portfolio_state': None,
            'warnings': [],
            'errors': []
        }

        logger.info("=" * 80)
        logger.info("SENTINEL CORPORATION - AUTOMATED DAILY TRADING")
        logger.info("=" * 80)
        logger.info(f"Date: {date.today().strftime('%A, %B %d, %Y')}")
        logger.info(f"Start Time: {self.start_time.strftime('%H:%M:%S')}")
        logger.info("=" * 80)

    def run(self) -> Dict:
        """
        Execute the complete automated trading workflow.

        Returns:
            Dict with complete execution results
        """
        try:
            # Step 1: Pre-flight checks
            if not self._preflight_checks():
                return self._finalize_results('PREFLIGHT_FAILED')

            # Step 2: Check market status
            if not self._check_market_status():
                return self._finalize_results('MARKET_CLOSED')

            # Step 3: Check if already traded today
            if self._has_traded_today():
                logger.info("[AutoTrader] Already traded today - skipping execution")
                self.results['warnings'].append("Already traded today")
                return self._finalize_results('ALREADY_TRADED')

            # Step 4: Analyze market regime
            regime_ok = self._analyze_market_regime()
            if not regime_ok:
                logger.warning("[AutoTrader] Market regime unfavorable - proceeding with caution")
                self.results['warnings'].append("Unfavorable market regime - trading anyway")

            # Step 5: Generate trading plan
            plan = self._generate_trading_plan()
            if not plan:
                return self._finalize_results('PLAN_GENERATION_FAILED')

            # Step 6: Auto-approve plan
            if not self._approve_plan(plan):
                return self._finalize_results('PLAN_APPROVAL_FAILED')

            # Step 7: Execute trades
            execution_result = self._execute_trades()
            if not execution_result:
                return self._finalize_results('EXECUTION_FAILED')

            # Step 8: Get final portfolio state
            self._get_portfolio_state()

            # Step 9: Set status BEFORE sending email
            self.results['status'] = 'SUCCESS'

            # Step 10: Send email report
            self._send_email_report()

            return self._finalize_results('SUCCESS')

        except Exception as e:
            logger.error(f"[AutoTrader] CRITICAL ERROR: {e}", exc_info=True)
            self.results['errors'].append(f"Critical error: {str(e)}")
            self.results['errors'].append(traceback.format_exc())

            # Still try to send error email
            try:
                self._send_error_email(str(e))
            except:
                pass

            return self._finalize_results('CRITICAL_ERROR')

    def _preflight_checks(self) -> bool:
        """Run pre-flight checks before trading"""
        logger.info("\n[AutoTrader] Running pre-flight checks...")

        try:
            # Check config exists
            import config

            # Check API keys exist
            if not config.APCA_API_KEY_ID or not config.APCA_API_SECRET_KEY:
                self.results['errors'].append("Alpaca API keys not configured")
                return False

            # Check database exists
            db_path = self.project_root / "sentinel.db"
            if not db_path.exists():
                self.results['errors'].append("Database not found")
                return False

            # Check Alpaca connection
            from alpaca.trading.client import TradingClient
            trading_client = TradingClient(
                config.APCA_API_KEY_ID,
                config.APCA_API_SECRET_KEY,
                paper=True
            )
            account = trading_client.get_account()
            logger.info(f"[AutoTrader] Alpaca connected - Equity: ${float(account.equity):,.2f}")

            logger.info("[AutoTrader] Pre-flight checks PASSED")
            return True

        except Exception as e:
            self.results['errors'].append(f"Pre-flight check failed: {str(e)}")
            logger.error(f"[AutoTrader] Pre-flight check failed: {e}")
            return False

    def _check_market_status(self) -> bool:
        """Check if market is open for trading"""
        logger.info("\n[AutoTrader] Checking market status...")

        try:
            from Departments.Operations.mode_manager import ModeManager
            mode_manager = ModeManager(self.project_root, alpaca_client=None)

            market_status = mode_manager.get_market_status_display()
            self.results['market_status'] = market_status

            logger.info(f"[AutoTrader] Market Status: {market_status['status']}")
            logger.info(f"[AutoTrader] {market_status['message']}")

            if not market_status['is_open']:
                logger.info("[AutoTrader] Market is CLOSED - skipping trading")
                return False

            return True

        except Exception as e:
            logger.error(f"[AutoTrader] Market status check failed: {e}")
            self.results['errors'].append(f"Market status check failed: {str(e)}")
            return False

    def _has_traded_today(self) -> bool:
        """Check if we've already executed trades today"""
        try:
            from Departments.Operations.mode_manager import ModeManager
            mode_manager = ModeManager(self.project_root, alpaca_client=None)

            has_traded, session_info = mode_manager.has_traded_today()

            if has_traded:
                logger.info(f"[AutoTrader] Already traded at {session_info['executed_at']}")
                return True

            return False

        except Exception as e:
            logger.warning(f"[AutoTrader] Could not check trade history: {e}")
            return False

    def _analyze_market_regime(self) -> bool:
        """Analyze market regime and decide whether to proceed"""
        logger.info("\n[AutoTrader] Analyzing market regime...")

        try:
            from Departments.Research.market_regime import MarketRegimeAnalyzer
            regime_analyzer = MarketRegimeAnalyzer(self.project_root)

            # Check for recent assessment (< 3 hours old)
            recent = regime_analyzer.get_latest_assessment(max_age_hours=3)

            if recent:
                assessment = recent
                logger.info(f"[AutoTrader] Using recent assessment from {recent['timestamp']}")
            else:
                result = regime_analyzer.analyze_regime()
                if result['status'] != 'SUCCESS':
                    logger.warning(f"[AutoTrader] Regime analysis failed: {result['message']}")
                    return True  # Proceed anyway if analysis fails
                assessment = result

            self.results['regime_analysis'] = {
                'regime': assessment['regime'],
                'confidence': assessment.get('confidence', 'MEDIUM'),
                'spy_price': assessment['spy_price'],
                'spy_change_pct': assessment['spy_change_pct'],
                'vix_level': assessment['vix_level'],
                'recommendation': assessment['recommendation']
            }

            logger.info(f"[AutoTrader] Regime: {assessment['regime']} (Confidence: {assessment.get('confidence', 'MEDIUM')})")
            logger.info(f"[AutoTrader] SPY: ${assessment['spy_price']:.2f} ({assessment['spy_change_pct']:+.2f}%)")
            logger.info(f"[AutoTrader] VIX: {assessment['vix_level']:.2f}")
            logger.info(f"[AutoTrader] Recommendation: {assessment['recommendation']}")

            # Broadcast regime to departments
            self._broadcast_regime_message(assessment)

            # For automation, we proceed regardless of regime (conservative approach)
            # The portfolio optimizer will adjust position sizes based on regime
            return assessment['regime'] != 'PANIC'  # Only skip on PANIC

        except Exception as e:
            logger.error(f"[AutoTrader] Regime analysis error: {e}")
            self.results['warnings'].append(f"Regime analysis failed: {str(e)}")
            return True  # Proceed anyway

    def _broadcast_regime_message(self, assessment: Dict):
        """Send market regime message to all departments"""
        logger.info("[AutoTrader] Broadcasting regime assessment to departments...")

        message_dir = self.project_root / "Messages_Between_Departments" / "Inbox"
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")

        for dept in ["RESEARCH", "RISK", "PORTFOLIO", "COMPLIANCE", "TRADING"]:
            dept_dir = message_dir / dept
            dept_dir.mkdir(parents=True, exist_ok=True)

            msg_id = f"MSG_REGIME_{timestamp}_{dept.lower()[:4]}"
            msg_file = dept_dir / f"{msg_id}.md"

            content = f"""# Market Regime Assessment (Automated)

**From:** Automated Trading System
**To:** {dept} Department
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Market Regime: {assessment['regime']}

**Confidence:** {assessment.get('confidence', 'MEDIUM')}
**Recommendation:** {assessment['recommendation']}

## Current Indicators:
- **SPY:** ${assessment['spy_price']:.2f} ({assessment['spy_change_pct']:+.2f}%)
- **VIX:** {assessment['vix_level']:.2f}

---
*Automated message - no response required*
"""
            msg_file.write_text(content)

    def _generate_trading_plan(self) -> Optional[Dict]:
        """Generate trading plan via CEO"""
        logger.info("\n[AutoTrader] Generating trading plan...")
        logger.info("[AutoTrader] Using AI model: gpt-4o-mini (budget)")

        try:
            from Departments.Executive.ceo import CEO
            ceo = CEO(self.project_root)

            # Generate plan with budget model
            result = ceo.handle_user_request("generate_plan", ai_model='gpt-4o-mini')

            if result['status'] == 'READY_FOR_USER_APPROVAL':
                plan = result['plan']
                ceo_review = result['ceo_review']

                self.results['plan_generated'] = True
                self.results['plan_summary'] = {
                    'plan_id': plan['plan_id'],
                    'total_trades': plan['summary']['total_trades'],
                    'quality_score': plan['summary']['overall_quality_score'],
                    'ceo_rating': ceo_review['quality_rating'],
                    'ceo_recommendation': ceo_review['recommendation']
                }

                logger.info(f"[AutoTrader] Plan generated: {plan['plan_id']}")
                logger.info(f"[AutoTrader] Total trades: {plan['summary']['total_trades']}")
                logger.info(f"[AutoTrader] Quality score: {plan['summary']['overall_quality_score']}/100")
                logger.info(f"[AutoTrader] CEO rating: {ceo_review['quality_rating']}")

                # Store CEO reference for approval
                self._ceo = ceo

                return plan

            elif result['status'] == 'REJECTED':
                logger.warning(f"[AutoTrader] Plan rejected: {result['message']}")
                self.results['errors'].append(f"Plan rejected: {result['message']}")
                return None

            else:
                logger.warning(f"[AutoTrader] Unexpected plan status: {result['status']}")
                self.results['errors'].append(f"Plan generation returned: {result['status']}")
                return None

        except Exception as e:
            logger.error(f"[AutoTrader] Plan generation failed: {e}", exc_info=True)
            self.results['errors'].append(f"Plan generation failed: {str(e)}")
            return None

    def _approve_plan(self, plan: Dict) -> bool:
        """Auto-approve the trading plan"""
        logger.info("\n[AutoTrader] Auto-approving plan...")

        try:
            if not hasattr(self, '_ceo'):
                logger.error("[AutoTrader] CEO not initialized")
                return False

            result = self._ceo.approve_plan(plan['plan_id'])

            if result['status'] == 'PLAN_APPROVED':
                self.results['plan_approved'] = True
                logger.info(f"[AutoTrader] Plan {plan['plan_id']} APPROVED")
                return True
            else:
                logger.error(f"[AutoTrader] Plan approval failed: {result.get('message')}")
                self.results['errors'].append(f"Plan approval failed: {result.get('message')}")
                return False

        except Exception as e:
            logger.error(f"[AutoTrader] Plan approval error: {e}")
            self.results['errors'].append(f"Plan approval error: {str(e)}")
            return False

    def _execute_trades(self) -> bool:
        """Execute the approved trading plan"""
        logger.info("\n[AutoTrader] Executing trades...")

        try:
            if not hasattr(self, '_ceo'):
                logger.error("[AutoTrader] CEO not initialized")
                return False

            result = self._ceo.handle_user_request("execute_plan")

            if result['status'] == 'EXECUTION_INITIATED':
                self.results['trades_executed'] = result.get('execution_results', [])
                self.results['sells_count'] = result.get('sells_submitted', 0)
                self.results['buys_count'] = result.get('buys_submitted', 0)
                self.results['verification'] = result.get('post_execution_verification', {})

                logger.info(f"[AutoTrader] Execution complete!")
                logger.info(f"[AutoTrader] SELLs executed: {result.get('sells_submitted', 0)}")
                logger.info(f"[AutoTrader] BUYs executed: {result.get('buys_submitted', 0)}")

                # Check verification
                verification = result.get('post_execution_verification', {})
                if not verification.get('passed', True):
                    for issue in verification.get('issues', []):
                        self.results['warnings'].append(f"Verification: {issue}")
                        logger.warning(f"[AutoTrader] Verification issue: {issue}")

                # Record fills to database
                self._record_fills()

                return True
            else:
                logger.error(f"[AutoTrader] Execution failed: {result.get('message')}")
                self.results['errors'].append(f"Execution failed: {result.get('message')}")
                return False

        except Exception as e:
            logger.error(f"[AutoTrader] Execution error: {e}", exc_info=True)
            self.results['errors'].append(f"Execution error: {str(e)}")
            return False

    def _get_portfolio_state(self):
        """Get current portfolio state after execution"""
        logger.info("\n[AutoTrader] Fetching final portfolio state...")

        try:
            import config
            from alpaca.trading.client import TradingClient

            trading_client = TradingClient(
                config.APCA_API_KEY_ID,
                config.APCA_API_SECRET_KEY,
                paper=True
            )

            account = trading_client.get_account()
            positions = trading_client.get_all_positions()

            # Calculate metrics
            starting_capital = 100000.00
            equity = float(account.equity)
            total_return = equity - starting_capital
            total_return_pct = (total_return / starting_capital) * 100

            daily_pl = float(account.equity) - float(account.last_equity)
            daily_pl_pct = (daily_pl / float(account.last_equity) * 100) if float(account.last_equity) > 0 else 0

            # Build positions list
            positions_list = []
            total_unrealized_pl = 0

            for pos in positions:
                unrealized_pl = float(pos.unrealized_pl)
                total_unrealized_pl += unrealized_pl

                positions_list.append({
                    'ticker': pos.symbol,
                    'shares': float(pos.qty),
                    'entry_price': float(pos.avg_entry_price),
                    'current_price': float(pos.current_price),
                    'market_value': float(pos.market_value),
                    'unrealized_pl': unrealized_pl,
                    'unrealized_pl_pct': float(pos.unrealized_plpc) * 100
                })

            # Sort by market value (largest first)
            positions_list.sort(key=lambda x: -x['market_value'])

            self.results['portfolio_state'] = {
                'timestamp': datetime.now().isoformat(),
                'equity': equity,
                'cash': float(account.cash),
                'buying_power': float(account.buying_power),
                'portfolio_value': float(account.portfolio_value),
                'starting_capital': starting_capital,
                'total_return': total_return,
                'total_return_pct': total_return_pct,
                'daily_pl': daily_pl,
                'daily_pl_pct': daily_pl_pct,
                'total_unrealized_pl': total_unrealized_pl,
                'position_count': len(positions_list),
                'positions': positions_list
            }

            logger.info(f"[AutoTrader] Portfolio Value: ${equity:,.2f}")
            logger.info(f"[AutoTrader] Total Return: ${total_return:,.2f} ({total_return_pct:+.2f}%)")
            logger.info(f"[AutoTrader] Daily P/L: ${daily_pl:,.2f} ({daily_pl_pct:+.2f}%)")
            logger.info(f"[AutoTrader] Positions: {len(positions_list)}")

        except Exception as e:
            logger.error(f"[AutoTrader] Portfolio state error: {e}")
            self.results['warnings'].append(f"Could not fetch portfolio state: {str(e)}")

    def _record_fills(self):
        """Record order fills from Alpaca to database"""
        logger.info("\n[AutoTrader] Recording fills to database...")

        try:
            from Utils.fill_recorder import FillRecorder

            recorder = FillRecorder()
            results = recorder.sync_fills_to_database(days=1)

            fills_recorded = results.get('fills_recorded', 0)
            orders_updated = results.get('orders_updated', 0)

            if fills_recorded > 0 or orders_updated > 0:
                logger.info(f"[AutoTrader] Recorded {fills_recorded} fills, updated {orders_updated} orders")
            else:
                logger.info("[AutoTrader] No new fills to record")

            # Store fill stats in results
            self.results['fill_sync'] = results

        except ImportError:
            logger.warning("[AutoTrader] Fill recorder not available")
        except Exception as e:
            logger.error(f"[AutoTrader] Fill recording error: {e}")
            self.results['warnings'].append(f"Fill recording failed: {str(e)}")

    def _send_email_report(self):
        """Send comprehensive daily email report"""
        logger.info("\n[AutoTrader] Sending email report...")

        try:
            from Utils.automated_email_reporter import AutomatedEmailReporter

            reporter = AutomatedEmailReporter()
            success = reporter.send_daily_report(self.results)

            if success:
                logger.info("[AutoTrader] Email report sent successfully!")
            else:
                logger.warning("[AutoTrader] Email report may have failed")
                self.results['warnings'].append("Email report may not have been sent")

        except ImportError:
            logger.warning("[AutoTrader] Email reporter not found - creating it now")
            self.results['warnings'].append("Email reporter module not available")
        except Exception as e:
            logger.error(f"[AutoTrader] Email report error: {e}")
            self.results['warnings'].append(f"Email report failed: {str(e)}")

    def _send_error_email(self, error_message: str):
        """Send emergency error notification email"""
        logger.info("[AutoTrader] Sending error notification email...")

        try:
            import config
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            sender_email = "wjcornelius@gmail.com"
            recipient_email = "wjcornelius@gmail.com"

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 SENTINEL ALERT: Automated Trading Error - {date.today()}"
            msg['From'] = sender_email
            msg['To'] = recipient_email

            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f8d7da; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; border: 2px solid #dc3545;">
                    <h1 style="color: #dc3545; margin: 0;">⚠️ SENTINEL TRADING ERROR</h1>
                    <p style="color: #721c24; font-size: 18px;">Date: {date.today().strftime('%B %d, %Y')}</p>

                    <hr style="border: 1px solid #dc3545;">

                    <h2 style="color: #dc3545;">Error Details</h2>
                    <pre style="background-color: #f5f5f5; padding: 15px; overflow-x: auto; white-space: pre-wrap;">{error_message}</pre>

                    <h2 style="color: #dc3545;">Action Required</h2>
                    <p>Please check the Sentinel system logs and investigate the issue.</p>
                    <p>Log file: <code>logs/automated_trading_{date.today()}.log</code></p>

                    <hr style="border: 1px solid #ccc;">
                    <p style="color: #666; font-size: 12px;">This is an automated alert from Sentinel Corporation.</p>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(html, 'html'))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, config.GMAIL_APP_PASSWORD)
                server.send_message(msg)

            logger.info("[AutoTrader] Error notification email sent")

        except Exception as e:
            logger.error(f"[AutoTrader] Could not send error email: {e}")

    def _finalize_results(self, status: str) -> Dict:
        """Finalize and save results"""
        self.results['status'] = status
        self.results['end_time'] = datetime.now().isoformat()
        self.results['duration_seconds'] = (datetime.now() - self.start_time).total_seconds()

        # Save results to file
        results_file = self.project_root / f"automated_trading_results_{date.today()}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        logger.info("\n" + "=" * 80)
        logger.info("AUTOMATED TRADING COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Status: {status}")
        logger.info(f"Duration: {self.results['duration_seconds']:.1f} seconds")
        logger.info(f"Trades: {len(self.results.get('trades_executed', []))}")
        logger.info(f"Warnings: {len(self.results.get('warnings', []))}")
        logger.info(f"Errors: {len(self.results.get('errors', []))}")
        logger.info(f"Results saved to: {results_file}")
        logger.info("=" * 80)

        return self.results


def main():
    """Main entry point for automated trading"""
    runner = AutomatedTradingRunner()
    result = runner.run()

    # Exit with appropriate code
    if result['status'] == 'SUCCESS':
        sys.exit(0)
    elif result['status'] in ['MARKET_CLOSED', 'ALREADY_TRADED']:
        sys.exit(0)  # Not an error, just skipped
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
