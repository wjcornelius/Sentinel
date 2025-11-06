"""
CEO (Chief Executive Officer) - Sentinel Corporation
User's SINGLE point of contact with SC

Primary Responsibilities:
- Interface between User (Board/Customer) and SC staff
- Delegate work to Operations Manager
- Review plan quality before presenting to User
- Handle escalations from Operations Manager
- Make executive decisions when needed
- Present final plans to User for approval

Philosophy: Like a real CEO - takes orders from Board (User),
delegates to staff, reviews work quality, makes final decisions,
presents results professionally.

Author: Claude Code (CC)
Architecture: Based on user's corporate structure vision
Date: November 1, 2025
"""

import sys
import json
import logging
import uuid
import yaml
from pathlib import Path
from datetime import datetime, date, timezone
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import Operations Manager
from Departments.Operations.operations_manager import OperationsManager

# Import Executive Department (for dashboards and reporting)
from Departments.Executive.executive_department import ExecutiveDepartment

# Import data source for portfolio queries
from Utils.data_source import create_data_source

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CEO')


class CEO:
    """
    Chief Executive Officer - User's single interface to Sentinel Corporation

    The CEO is responsible for:
    1. Taking requests from User (the Board/Customer)
    2. Delegating work to Operations Manager
    3. Reviewing quality of work produced
    4. Handling escalations and making executive decisions
    5. Presenting final products (trading plans) to User
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.db_path = project_root / "sentinel.db"

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("=" * 80)
        self.logger.info("CEO - INITIALIZING SENTINEL CORPORATION")
        self.logger.info("=" * 80)

        # Initialize Operations Manager (coordinates departments)
        self.operations_manager = OperationsManager(project_root)

        # Initialize Executive Department (reporting and dashboards)
        self.executive_dept = ExecutiveDepartment(
            db_path=self.db_path,
            messages_dir=project_root / "Messages_Between_Departments",
            reports_dir=project_root / "Reports"
        )

        # Initialize data source for quick portfolio queries
        self.data_source = create_data_source(str(self.db_path))

        # Track current approved plan
        self.current_plan = None
        self.plan_approved = False

        self.logger.info("CEO ready to serve")
        self.logger.info(f"Data source: {self.data_source.get_data_source_info()['data_source']}")
        self.logger.info("=" * 80)

    def handle_user_request(self, request: str, **kwargs) -> Dict:
        """
        Single entry point for all user interactions

        Args:
            request: Type of request ('generate_plan', 'view_dashboard', 'execute_plan', etc.)
            **kwargs: Additional parameters for specific requests

        Returns:
            Dict with response data
        """
        self.logger.info(f"\n[CEO] User request received: {request}")

        if request == "generate_plan":
            ai_model = kwargs.get('ai_model', 'gpt-4o-mini')  # Default to budget model
            return self.generate_trading_plan(ai_model=ai_model)

        elif request == "view_dashboard":
            return self.get_dashboard_data()

        elif request == "execute_plan":
            return self.execute_approved_plan()

        elif request == "get_portfolio_summary":
            return self.get_portfolio_summary()

        else:
            return {
                'status': 'ERROR',
                'message': f"Unknown request type: {request}"
            }

    def generate_trading_plan(self, ai_model: str = 'gpt-4o-mini') -> Dict:
        """
        User requested a trading plan
        Delegate to Operations Manager, review quality, present to user

        Args:
            ai_model: AI model to use for portfolio optimization (default: gpt-4o-mini)

        Returns:
            Dict with plan or escalation
        """
        self.logger.info("\n" + "=" * 80)
        self.logger.info("[CEO] GENERATING TRADING PLAN")
        self.logger.info("=" * 80)
        self.logger.info(f"[CEO] Using AI model: {ai_model}")
        self.logger.info("[CEO] Delegating to Operations Manager...")

        # Delegate to Operations Manager with selected model
        result = self.operations_manager.generate_trading_plan(ai_model=ai_model)

        # Handle different outcomes
        if result['status'] == 'SUCCESS':
            return self._review_and_present_plan(result['plan'], result['stage_results'])

        elif result['status'] == 'ESCALATED':
            return self._handle_escalation(result['escalation'], result['stage_results'])

        elif result['status'] == 'FAILED':
            return self._handle_workflow_failure(result)

        else:
            return {
                'status': 'ERROR',
                'message': f"Unexpected workflow status: {result['status']}"
            }

    def _review_and_present_plan(self, plan: Dict, stage_results: List[Dict]) -> Dict:
        """
        CEO reviews plan quality and presents to user

        Args:
            plan: Trading plan from Operations Manager
            stage_results: Results from each workflow stage

        Returns:
            Dict formatted for user presentation
        """
        self.logger.info("\n[CEO] Reviewing plan quality...")

        # CEO's quality assessment
        ceo_review = {
            'overall_assessment': '',
            'quality_rating': '',  # EXCELLENT, GOOD, ACCEPTABLE, CONCERNS
            'strengths': [],
            'concerns': [],
            'recommendation': ''
        }

        quality_score = plan['summary']['overall_quality_score']
        trade_count = plan['summary']['total_trades']

        # Assess quality
        if quality_score >= 85:
            ceo_review['quality_rating'] = 'EXCELLENT'
            ceo_review['overall_assessment'] = f"High-quality plan with {trade_count} well-vetted trades."
            ceo_review['recommendation'] = 'STRONGLY RECOMMEND APPROVAL'

        elif quality_score >= 70:
            ceo_review['quality_rating'] = 'GOOD'
            ceo_review['overall_assessment'] = f"Solid plan with {trade_count} trades meeting all criteria."
            ceo_review['recommendation'] = 'RECOMMEND APPROVAL'

        elif quality_score >= 60:
            ceo_review['quality_rating'] = 'ACCEPTABLE'
            ceo_review['overall_assessment'] = f"Acceptable plan with {trade_count} trades, some minor concerns."
            ceo_review['recommendation'] = 'APPROVE WITH CAUTION'

        else:
            ceo_review['quality_rating'] = 'CONCERNS'
            ceo_review['overall_assessment'] = f"Plan quality below optimal standards."
            ceo_review['recommendation'] = 'REVIEW CAREFULLY BEFORE APPROVAL'

        # Identify strengths
        for result in stage_results:
            if result['quality_score'] >= 80:
                ceo_review['strengths'].append(f"{result['stage'].title()} department performed excellently")

        # Identify concerns
        for result in stage_results:
            if result['issues']:
                for issue in result['issues']:
                    ceo_review['concerns'].append(f"{result['stage'].title()}: {issue}")

        # Store plan for potential approval
        self.current_plan = plan
        self.plan_approved = False

        self.logger.info(f"[CEO] Quality Review Complete: {ceo_review['quality_rating']}")
        self.logger.info(f"[CEO] Recommendation: {ceo_review['recommendation']}")

        # Format for user presentation
        return {
            'status': 'READY_FOR_USER_APPROVAL',
            'plan': plan,
            'ceo_review': ceo_review,
            'stage_results': stage_results,
            'next_steps': [
                '[A] Approve Plan - Lock it in for execution',
                '[R] Reject Plan - Explain why and try again',
                '[V] View Detailed Analysis - See full department reports',
                '[M] Monitor Departments - Check individual department status'
            ]
        }

    def _handle_escalation(self, escalation: Dict, stage_results: List[Dict]) -> Dict:
        """
        Handle escalation from Operations Manager
        Make executive decision or present to user

        Args:
            escalation: Escalation details
            stage_results: Workflow results up to escalation point

        Returns:
            Dict with CEO's decision or user consultation
        """
        self.logger.warning(f"\n[CEO] ESCALATION RECEIVED: {escalation['stage']} - {escalation['severity']}")
        self.logger.warning(f"[CEO] Issue: {escalation['issue_type']}")
        self.logger.warning(f"[CEO] Recommendation from Operations: {escalation['recommendation']}")

        # CEO analyzes escalation
        stage = escalation['stage']
        severity = escalation['severity']

        # Make executive decision based on severity
        if severity == 'CRITICAL':
            # Critical issues go to user
            return {
                'status': 'CRITICAL_ISSUE_REQUIRES_USER_DECISION',
                'escalation': escalation,
                'ceo_analysis': self._analyze_critical_escalation(escalation),
                'stage_results': stage_results,
                'message': "[CEO] Critical issue encountered. Your decision is required."
            }

        elif severity == 'WARNING':
            # Warnings: CEO can make decision or consult user
            ceo_decision = self._make_executive_decision(escalation)

            if ceo_decision['action'] == 'PROCEED_WITH_CAUTION':
                return {
                    'status': 'CEO_APPROVED_DESPITE_WARNING',
                    'escalation': escalation,
                    'ceo_decision': ceo_decision,
                    'stage_results': stage_results,
                    'message': "[CEO] I've reviewed the warning and approved proceeding with adjustments."
                }
            else:
                return {
                    'status': 'CEO_RECOMMENDS_USER_REVIEW',
                    'escalation': escalation,
                    'ceo_decision': ceo_decision,
                    'stage_results': stage_results,
                    'message': "[CEO] I recommend you review this issue before we proceed."
                }

        else:  # INFO
            # Informational: CEO handles it
            return {
                'status': 'CEO_HANDLED_ESCALATION',
                'escalation': escalation,
                'message': "[CEO] Minor issue handled internally. Proceeding with adjusted plan."
            }

    def _analyze_critical_escalation(self, escalation: Dict) -> Dict:
        """CEO's analysis of critical escalation"""
        return {
            'summary': f"Critical issue in {escalation['stage']} stage",
            'impact': "Cannot proceed with trading plan without resolution",
            'options_analysis': [
                {'option': opt, 'ceo_assessment': self._assess_option(opt, escalation)}
                for opt in escalation['options']
            ],
            'ceo_recommendation': escalation['recommendation']
        }

    def _assess_option(self, option: str, escalation: Dict) -> str:
        """CEO assesses each option"""
        # Simplified assessment - can be enhanced
        if 'skip trading' in option.lower():
            return "Conservative approach - ensures safety but misses opportunity"
        elif 'retry' in option.lower():
            return "Gives another chance - may or may not improve results"
        elif 'accept' in option.lower():
            return "Pragmatic approach - proceed with what we have"
        else:
            return "Requires careful consideration"

    def _make_executive_decision(self, escalation: Dict) -> Dict:
        """CEO makes executive decision on warning-level escalations"""
        # CEO applies business judgment
        stage = escalation['stage']
        quality_score = escalation['context'].get('quality_score', 0)

        if quality_score >= 50:
            # Marginal but acceptable
            return {
                'action': 'PROCEED_WITH_CAUTION',
                'rationale': f"{stage.title()} quality is marginal but acceptable. Proceeding with reduced position sizing.",
                'adjustments': ['Reduce position sizes by 25%', 'Tighten stop losses', 'Monitor closely']
            }
        else:
            # Too risky
            return {
                'action': 'CONSULT_USER',
                'rationale': f"{stage.title()} quality is below my comfort level. Seeking your input.",
                'recommendation': 'Consider skipping trading today or adjusting criteria'
            }

    def _handle_workflow_failure(self, result: Dict) -> Dict:
        """Handle complete workflow failure"""
        self.logger.error(f"[CEO] WORKFLOW FAILURE: {result.get('error', 'Unknown error')}")

        return {
            'status': 'WORKFLOW_FAILED',
            'error': result.get('error'),
            'stage_results': result.get('stage_results', []),
            'ceo_message': "[CEO] I apologize - our workflow encountered a critical error. Technical team needs to investigate.",
            'recommendation': 'Please check system logs and try again later.'
        }

    def approve_plan(self, plan_id: str) -> Dict:
        """
        User approved the plan
        Mark it as approved and ready for execution

        Args:
            plan_id: ID of plan to approve

        Returns:
            Confirmation message
        """
        if not self.current_plan or self.current_plan['plan_id'] != plan_id:
            return {
                'status': 'ERROR',
                'message': 'Plan not found or expired'
            }

        self.current_plan['status'] = 'APPROVED_BY_USER'
        self.current_plan['approved_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        self.plan_approved = True

        # Save approved plan to file
        self._save_approved_plan(self.current_plan)

        self.logger.info(f"[CEO] Plan {plan_id} APPROVED by user")

        return {
            'status': 'PLAN_APPROVED',
            'plan_id': plan_id,
            'message': '[CEO] Excellent! Plan approved and locked in. Ready to execute when market opens.',
            'next_steps': [
                'Wait for market to open (9:30 AM ET)',
                'Use "Execute Approved Plan" when ready',
                'I will oversee the execution personally'
            ]
        }

    def _save_approved_plan(self, plan: Dict):
        """Save approved plan to file"""
        today = datetime.now().strftime('%Y-%m-%d')
        plan_file = self.project_root / f"proposed_trades_{today}.json"

        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)

        self.logger.info(f"[CEO] Approved plan saved to {plan_file}")

    def get_dashboard_data(self) -> Dict:
        """Get real-time dashboard data from Alpaca"""
        self.logger.info("[CEO] Retrieving dashboard data...")

        try:
            # Import Alpaca client
            from alpaca.trading.client import TradingClient
            import os

            # Get API keys from environment
            api_key = os.getenv('APCA_API_KEY_ID')
            api_secret = os.getenv('APCA_API_SECRET_KEY')

            if not api_key or not api_secret:
                return {
                    'status': 'ERROR',
                    'message': '[CEO] Alpaca API keys not found in environment'
                }

            # Initialize Alpaca client
            trading_client = TradingClient(api_key, api_secret, paper=True)

            # Get account info
            account = trading_client.get_account()

            # Get positions
            positions = trading_client.get_all_positions()

            # Store snapshot
            self._store_portfolio_snapshot(account, positions, source='dashboard_query')

            # Format dashboard data
            dashboard_data = {
                'performance': {
                    'portfolio_value': float(account.portfolio_value),
                    'equity': float(account.equity),
                    'cash': float(account.cash),
                    'buying_power': float(account.buying_power),
                    'daily_pl': float(account.equity) - float(account.last_equity),
                    'daily_pl_pct': ((float(account.equity) - float(account.last_equity)) / float(account.last_equity) * 100) if float(account.last_equity) > 0 else 0,
                    'positions_count': len(positions)
                },
                'open_positions': [{
                    'ticker': p.symbol,
                    'shares': float(p.qty),
                    'entry_price': float(p.avg_entry_price),
                    'current_price': float(p.current_price),
                    'market_value': float(p.market_value),
                    'unrealized_pl': float(p.unrealized_pl),
                    'unrealized_plpc': float(p.unrealized_plpc) * 100  # Convert to percentage
                } for p in positions]
            }

            return {
                'status': 'SUCCESS',
                'dashboard': dashboard_data,
                'message': '[CEO] Here is your current portfolio status.'
            }

        except Exception as e:
            self.logger.error(f"[CEO] Failed to get dashboard: {e}", exc_info=True)
            return {
                'status': 'ERROR',
                'message': f'[CEO] Unable to retrieve dashboard: {str(e)}'
            }

    def get_portfolio_summary(self) -> Dict:
        """Get quick portfolio summary from Alpaca"""
        try:
            # Import Alpaca client
            from alpaca.trading.client import TradingClient
            import os

            # Get API keys from environment
            api_key = os.getenv('APCA_API_KEY_ID')
            api_secret = os.getenv('APCA_API_SECRET_KEY')

            if not api_key or not api_secret:
                return {
                    'status': 'ERROR',
                    'message': '[CEO] Alpaca API keys not found in environment'
                }

            # Initialize Alpaca client
            trading_client = TradingClient(api_key, api_secret, paper=True)

            # Get account info
            account = trading_client.get_account()

            # Get positions
            positions = trading_client.get_all_positions()

            # Store snapshot
            self._store_portfolio_snapshot(account, positions, source='control_panel_query')

            return {
                'status': 'SUCCESS',
                'summary': {
                    'position_count': len(positions),
                    'cash_balance': float(account.cash),
                    'portfolio_value': float(account.portfolio_value),
                    'buying_power': float(account.buying_power),
                    'equity': float(account.equity),
                    'positions': [{
                        'ticker': p.symbol,
                        'shares': float(p.qty),
                        'market_value': float(p.market_value),
                        'unrealized_pl': float(p.unrealized_pl),
                        'unrealized_plpc': float(p.unrealized_plpc)
                    } for p in positions[:5]]  # Top 5
                }
            }

        except Exception as e:
            self.logger.error(f"[CEO] Failed to get portfolio summary: {e}", exc_info=True)
            return {
                'status': 'ERROR',
                'message': f'[CEO] Unable to fetch portfolio data: {str(e)}'
            }

    def execute_approved_plan(self) -> Dict:
        """Execute the approved trading plan"""
        if not self.plan_approved or not self.current_plan:
            return {
                'status': 'ERROR',
                'message': '[CEO] No approved plan available for execution. Please generate and approve a plan first.'
            }

        self.logger.info(f"[CEO] Executing approved plan: {self.current_plan['plan_id']}")
        self.logger.info("[CEO] Delegating to Trading Department...")

        try:
            # Initialize Trading Department
            from Departments.Trading.trading_department import TradingDepartment
            trading_dept = TradingDepartment(db_path=str(self.db_path))

            # Get trades from approved plan
            trades = self.current_plan.get('trades', [])

            if not trades:
                return {
                    'status': 'ERROR',
                    'message': '[CEO] Approved plan contains no trades to execute.'
                }

            self.logger.info(f"[CEO] Submitting {len(trades)} orders to Trading Department")

            # Send each trade to Trading Department via message
            execution_results = []
            for trade in trades:
                # Create execution message for Trading Department
                message_id = self._send_trade_to_trading_dept(trade)
                execution_results.append({
                    'ticker': trade.get('ticker'),
                    'message_id': message_id
                })

            # Process inbox to execute the orders
            self.logger.info("[CEO] Trading Department processing orders...")
            trading_dept.process_inbox()

            return {
                'status': 'EXECUTION_INITIATED',
                'plan_id': self.current_plan['plan_id'],
                'message': '[CEO] Orders submitted to Trading Department for execution. Execution complete.',
                'trades_submitted': len(trades),
                'execution_results': execution_results
            }

        except Exception as e:
            self.logger.error(f"[CEO] Execution failed: {e}", exc_info=True)
            return {
                'status': 'ERROR',
                'message': f'[CEO] Execution failed: {str(e)}'
            }

    def _send_trade_to_trading_dept(self, trade: Dict) -> str:
        """Send a single trade order to Trading Department"""
        # Determine if this is a BUY or SELL
        # BUY orders have 'allocated_capital', SELL orders have 'position_id'
        if 'allocated_capital' in trade:
            action = 'BUY'
            shares = trade.get('shares', 0)
        else:
            action = 'SELL'
            shares = trade.get('shares', 0)

        # Get price from trade data
        price = trade.get('entry_price', trade.get('current_price', trade.get('price', 0)))
        ticker = trade.get('ticker', 'UNKNOWN')
        sector = trade.get('sector', 'Unknown')

        # Generate message ID
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        msg_id = f"MSG_EXECUTIVE_{timestamp}_{uuid.uuid4().hex[:8]}"

        # Create message
        metadata = {
            'message_id': msg_id,
            'from': 'EXECUTIVE',
            'to': 'TRADING',
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'message_type': 'ExecutiveApproval',
            'priority': 'urgent',
            'requires_response': False
        }

        # Build message body with JSON payload
        body = f"""# Executive Approval - {action} {ticker}

**Order Type**: {action}
**Ticker**: {ticker}
**Shares**: {shares}
**Price**: ${price:.2f}
**Sector**: {sector}

```json
{{
  "ticker": "{ticker}",
  "action": "{action}",
  "shares": {shares},
  "price": {price},
  "sector": "{sector}",
  "order_type": "MARKET",
  "plan_id": "{self.current_plan['plan_id']}",
  "approved_at": "{datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}"
}}
```
"""

        # Write message to Trading inbox
        trading_inbox = self.project_root / "Messages_Between_Departments" / "Inbox" / "TRADING"
        trading_inbox.mkdir(parents=True, exist_ok=True)

        message_file = trading_inbox / f"{msg_id}.md"

        content = "---\n"
        content += yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        content += "---\n"
        content += body

        with open(message_file, 'w') as f:
            f.write(content)

        self.logger.info(f"[CEO] Sent {action} order for {ticker} to Trading (msg: {msg_id})")

        return msg_id

    def _store_portfolio_snapshot(self, account, positions, source='unknown'):
        """Store portfolio snapshot in database for tracking"""
        try:
            import sqlite3

            # Generate snapshot ID
            snapshot_id = f"SNAP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            timestamp = datetime.now().isoformat()

            # Extract account data
            total_value = float(account.portfolio_value)
            cash_balance = float(account.cash)
            equity_value = float(account.equity)
            buying_power = float(account.buying_power)

            # Calculate daily P&L
            daily_pl = float(account.equity) - float(account.last_equity)
            daily_pl_pct = (daily_pl / float(account.last_equity) * 100) if float(account.last_equity) > 0 else 0

            # Get positions count
            positions_count = len(positions)

            # TODO: Fetch SPY data for comparison (future enhancement)
            spy_close = None
            spy_change_pct = None

            # Connect to database
            db_path = self.project_root / "sentinel_corporation.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Insert snapshot
            cursor.execute("""
                INSERT INTO portfolio_snapshots (
                    snapshot_id, timestamp, total_value, cash_balance, equity_value,
                    buying_power, margin_used, positions_count, daily_pl, daily_pl_pct,
                    spy_close, spy_change_pct, source, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot_id, timestamp, total_value, cash_balance, equity_value,
                buying_power, None,  # margin_used (calculate if needed)
                positions_count, daily_pl, daily_pl_pct,
                spy_close, spy_change_pct, source, None
            ))

            conn.commit()
            conn.close()

            self.logger.info(f"[CEO] Stored portfolio snapshot: {snapshot_id}")

        except Exception as e:
            self.logger.warning(f"[CEO] Failed to store portfolio snapshot: {e}")


if __name__ == "__main__":
    # Test CEO
    logger.info("Testing CEO Interface")

    project_root = Path(__file__).parent.parent.parent
    ceo = CEO(project_root)

    # Test: Generate trading plan
    logger.info("\n[TEST] Requesting trading plan from CEO...")
    result = ceo.handle_user_request("generate_plan")

    logger.info("\n" + "=" * 80)
    logger.info("CEO TEST COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Status: {result['status']}")

    if result['status'] == 'READY_FOR_USER_APPROVAL':
        plan = result['plan']
        review = result['ceo_review']
        logger.info(f"Plan ID: {plan['plan_id']}")
        logger.info(f"Total Trades: {plan['summary']['total_trades']}")
        logger.info(f"CEO Rating: {review['quality_rating']}")
        logger.info(f"CEO Recommendation: {review['recommendation']}")
