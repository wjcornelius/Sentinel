"""
Sentinel Corporation - Control Panel
=====================================
User's interface to the CEO

This is your single point of contact with Sentinel Corporation.
You interact ONLY with the CEO, who manages all departments on your behalf.

Philosophy: Like calling your investment manager - you state what you want,
they handle all the details, and present you with final recommendations.

Author: Claude Code (CC)
Architecture: Proper corporate structure per user vision
Date: November 1, 2025
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import CEO (our single interface)
from Departments.Executive.ceo import CEO
from Departments.Research.market_regime import MarketRegimeAnalyzer
from Departments.Operations.mode_manager import ModeManager


class SentinelControlPanel:
    """
    Control Panel - User Interface to CEO
    """

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.ceo = CEO(self.project_root)
        self.regime_analyzer = MarketRegimeAnalyzer(self.project_root)
        self.mode_manager = ModeManager(self.project_root, alpaca_client=None)  # Will get Alpaca from CEO if needed
        self.running = True
        self.selected_model = 'gpt-4o-mini'  # Default AI model

    def clear_screen(self):
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display welcome header"""
        print("\n" + "=" * 80)
        print(" " * 25 + "SENTINEL CORPORATION")
        print(" " * 28 + "Control Panel")
        print("=" * 80)
        print("\n[CEO] Good day! How may I assist you?\n")

    def display_main_menu(self):
        """Display main menu options"""
        # Get market status and trading session info
        market_status = self.mode_manager.get_market_status_display()
        has_traded, session_info = self.mode_manager.has_traded_today()

        # Display market status banner
        print("=" * 80)
        print(f"Market Status: {market_status['status']} ", end="")
        if market_status['is_open']:
            print(f"({market_status['current_time_et']})")
        else:
            print()
            print(f"  {market_status['message']}")

        # Display trading session status
        if has_traded:
            print(f"Today's Trading: EXECUTED at {session_info['executed_at']} ({session_info['trades_count']} trades)")
        else:
            if market_status['is_open']:
                print("Today's Trading: NOT EXECUTED (ready to trade)")
            else:
                print("Today's Trading: NOT EXECUTED (market closed)")
        print("=" * 80)
        print()

        print("MAIN OPTIONS:")
        print()

        # Option 1: Request Trading Plan
        plan_indicator = "[Market OPEN]" if market_status['is_open'] else "[Market CLOSED]"
        print(f"  [1] Request Trading Plan {plan_indicator}")
        print("      (CEO will coordinate all departments to generate a comprehensive plan)")
        print()

        # Option 2: View Portfolio Dashboard
        print("  [2] View Portfolio Dashboard")
        print("      (Real-time portfolio status and performance)")
        print()

        # Option 3: Execute Approved Plan
        if has_traded:
            exec_indicator = "[Already executed today]"
        elif market_status['is_open']:
            exec_indicator = "[Market OPEN - Ready]"
        else:
            exec_indicator = "[Market CLOSED]"
        print(f"  [3] Execute Approved Plan {exec_indicator}")
        print("      (Submit approved trades to market - available when market is open)")
        print()

        # Option 4: Select AI Model
        print("  [4] Select AI Model")
        print(f"      (Current: {self.selected_model} - Change before generating plan)")
        print()

        # Option 5: Refresh Universe (Weekends only)
        print("  [5] Refresh Trading Universe [Weekend Only]")
        print("      (Generate optimized swing trading stock universe for upcoming week)")
        print()

        print("  [0] Exit")
        print()
        print("=" * 80)

    def check_market_regime(self):
        """Check market regime and get user decision to proceed"""
        print("\n" + "=" * 120)
        print(" " * 45 + "MARKET REGIME ANALYSIS")
        print("=" * 120)

        print("\n[CEO] Analyzing current market conditions before generating plan...")
        print()

        # Check for recent assessment (< 3 hours old)
        recent = self.regime_analyzer.get_latest_assessment(max_age_hours=3)

        if recent:
            print(f"[CEO] Using recent market assessment from {recent['timestamp']}")
            assessment = recent
        else:
            print("[CEO] Fetching fresh market data...")
            result = self.regime_analyzer.analyze_regime()

            if result['status'] != 'SUCCESS':
                print(f"\n[CEO] {result['message']}")
                return False

            assessment = result

        # Display regime analysis
        print("\n" + "-" * 120)
        print("MARKET INDICATORS:")
        print(f"  SPY:  ${assessment['spy_price']:.2f}  {assessment['spy_change_pct']:+.2f}%  {'✓' if assessment['spy_change_pct'] > 0 else '✗'}")
        print(f"  VIX:  {assessment['vix_level']:.2f}   {assessment['vix_change_pct']:+.2f}%   {'✓ LOW' if assessment['vix_level'] < 20 else '⚠ ELEVATED'}")
        print()

        # Show regime assessment
        regime_icon = "✓" if assessment['regime'] == "BULLISH" else ("⚠" if assessment['regime'] == "BEARISH" else "~")
        print(f"REGIME ASSESSMENT: {assessment['regime']} {regime_icon} ({assessment.get('confidence', 'MEDIUM')} CONFIDENCE)")
        print()

        # Show reasoning
        print("ANALYSIS:")
        for reason in assessment['reasoning'].split(' • '):
            print(f"  • {reason}")
        print()

        # Show recommendation
        print(f"RECOMMENDATION: {assessment['recommendation']}")

        if assessment['regime'] == "BULLISH":
            print("  Market conditions appear favorable for initiating new positions.")
        elif assessment['regime'] == "BEARISH":
            print("  Market conditions suggest caution. Consider skipping today or reducing exposure.")
        else:
            print("  Market conditions are mixed. Normal trading protocols apply.")

        print("-" * 120)

        # Get user decision
        print()
        proceed = input("\nWould you like to proceed with generating a trading plan? (y/n): ").strip().lower()

        # Record decision
        if 'assessment_id' in assessment:
            decision = "PROCEED" if proceed == 'y' else "SKIP"
            self.regime_analyzer.record_user_decision(assessment['assessment_id'], decision)

        # Send regime message to all departments
        if proceed == 'y':
            self._broadcast_regime_message(assessment)

        return proceed == 'y'

    def _broadcast_regime_message(self, assessment):
        """Send market regime message to all departments"""
        print("\n[CEO] Broadcasting market regime assessment to all departments...")

        message_dir = self.project_root / "Messages_Between_Departments" / "Inbox"
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")

        for dept in ["RESEARCH", "RISK", "PORTFOLIO", "COMPLIANCE", "TRADING"]:
            dept_dir = message_dir / dept
            dept_dir.mkdir(parents=True, exist_ok=True)

            msg_id = f"MSG_REGIME_{timestamp}_{dept.lower()[:4]}"
            msg_file = dept_dir / f"{msg_id}.md"

            content = f"""# Market Regime Assessment

**From:** CEO / Market Regime Analyzer
**To:** {dept} Department
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Assessment ID:** {assessment.get('assessment_id', 'N/A')}

## Market Regime: {assessment['regime']}

**Confidence:** {assessment.get('confidence', 'MEDIUM')}
**Recommendation:** {assessment['recommendation']}

## Current Indicators:
- **SPY:** ${assessment['spy_price']:.2f} ({assessment['spy_change_pct']:+.2f}%)
- **VIX:** {assessment['vix_level']:.2f} ({assessment['vix_change_pct']:+.2f}%)

## Analysis:
{assessment['reasoning']}

## User Decision:
Proceeding with trading plan generation.

---
*This is an informational message. Departments should be aware of current market conditions but continue normal operations for now. Future phases will implement regime-responsive behavior.*
"""

            msg_file.write_text(content)

        print("[CEO] Market regime assessment delivered to all departments.")

    def request_trading_plan(self):
        """Request trading plan from CEO"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 25 + "REQUEST TRADING PLAN")
        print("=" * 80)

        # Check market regime first
        if not self.check_market_regime():
            print("\n[CEO] Understood. Skipping trading plan generation for today.")
            input("\nPress Enter to continue...")
            return

        print("\n[CEO] Understood. I'll have my team prepare a trading plan for you.")
        print(f"[CEO] Using AI model: {self.selected_model}")
        print("[CEO] This will take a moment while we coordinate all departments...\n")

        input("Press Enter to begin...")
        print()

        # Request plan from CEO with selected model
        result = self.ceo.handle_user_request("generate_plan", ai_model=self.selected_model)

        # Handle different outcomes
        if result['status'] == 'READY_FOR_USER_APPROVAL':
            self._display_plan_for_approval(result)

        elif result['status'] == 'CRITICAL_ISSUE_REQUIRES_USER_DECISION':
            self._display_critical_escalation(result)

        elif result['status'] == 'CEO_RECOMMENDS_USER_REVIEW':
            self._display_ceo_recommendation(result)

        elif result['status'] == 'WORKFLOW_FAILED':
            self._display_workflow_failure(result)

        else:
            print(f"\n[CEO] {result.get('message', 'Unexpected response')}")
            input("\nPress Enter to continue...")

    def _display_plan_for_approval(self, result: dict):
        """Display plan and ask for user approval"""
        plan = result['plan']
        ceo_review = result['ceo_review']

        print("\n" + "=" * 80)
        print(" " * 25 + "TRADING PLAN READY")
        print("=" * 80)

        # CEO's Executive Summary
        print(f"\n[CEO] {ceo_review['overall_assessment']}")
        print(f"\nQuality Rating: {ceo_review['quality_rating']}")
        print(f"Recommendation: {ceo_review['recommendation']}")

        # Plan Summary
        print(f"\n" + "-" * 80)
        print("PLAN SUMMARY:")
        print("-" * 80)
        summary = plan['summary']
        print(f"  Total Trades Proposed: {summary['total_trades']}")
        print(f"  Research Candidates Analyzed: {summary['research_candidates']}")
        print(f"  GPT-5 Selected: {summary.get('gpt5_selected', 0)}")
        print(f"  Compliance Flagged: {summary.get('compliance_flagged', 0)} (advisory notes)")
        print(f"  Overall Quality Score: {summary['overall_quality_score']}/100")

        # Capital Flow Summary
        print(f"\n" + "-" * 80)
        print("CAPITAL FLOW SUMMARY:")
        print("-" * 80)

        # Calculate capital from SELLs and BUYs
        trades = plan.get('trades', [])
        total_sell_value = 0
        total_buy_value = 0

        for trade in trades:
            action = trade.get('action', 'BUY').upper()
            if action == 'SELL':
                sell_value = trade.get('current_value', trade.get('market_value', 0))
                total_sell_value += sell_value
            else:  # BUY
                buy_value = trade.get('allocated_capital', 0)
                total_buy_value += buy_value

        net_capital_change = total_sell_value - total_buy_value

        # Get actual account data from Alpaca for accurate capital calculations
        from alpaca.trading.client import TradingClient
        api_key = os.getenv('APCA_API_KEY_ID')
        api_secret = os.getenv('APCA_API_SECRET_KEY')

        if api_key and api_secret:
            try:
                trading_client = TradingClient(api_key, api_secret, paper=True)
                account = trading_client.get_account()
                cash_value = float(account.cash)
                equity_value = float(account.equity)
                buying_power = float(account.buying_power)
                portfolio_value = float(account.portfolio_value)
            except Exception as e:
                # Fallback to approximation if Alpaca fetch fails
                buying_power = summary.get('available_capital', 0)
                cash_value = buying_power / 2  # Approximate
                equity_value = cash_value
                portfolio_value = cash_value
        else:
            # Fallback if no API keys
            buying_power = summary.get('available_capital', 0)
            cash_value = buying_power / 2
            equity_value = cash_value
            portfolio_value = cash_value

        # After trades
        projected_cash = cash_value + net_capital_change
        projected_leverage_used = total_buy_value / equity_value if equity_value > 0 else 0

        print(f"  Capital from Liquidations: ${total_sell_value:,.2f}")
        print(f"  Capital for New Positions: ${total_buy_value:,.2f}")
        print(f"  Net Capital Change: ${net_capital_change:+,.2f}")
        print(f"")
        print(f"  Current Buying Power: ${buying_power:,.2f} (includes 2x margin)")
        print(f"  Projected Cash After Trades: ${projected_cash:,.2f}")
        print(f"  Leverage Used: {projected_leverage_used:.1%} of portfolio value")

        # Workflow Summary
        print(f"\n" + "-" * 80)
        print("WORKFLOW SUMMARY:")
        print("-" * 80)
        for stage in plan['workflow_summary']:
            status = "[OK]" if not stage['issues'] else "[!]"
            print(f"  {status} {stage['stage'].upper()}: {stage['message']}")
            if stage['issues']:
                for issue in stage['issues']:
                    print(f"      - {issue}")

        # Display actual trades
        trades = plan.get('trades', [])
        if trades:
            print(f"\n" + "-" * 80)
            print("PROPOSED TRADES:")
            print("-" * 80)
            for i, trade in enumerate(trades, 1):
                ticker = trade.get('ticker', trade.get('symbol', 'N/A'))
                shares = trade.get('shares', trade.get('qty', 0))
                price = trade.get('entry_price', trade.get('current_price', trade.get('price', 0)))

                # Determine action label
                action = trade.get('action', 'BUY').upper()

                # For SELL orders, use current_value or market_value instead of allocated_capital
                if action == 'SELL':
                    allocated = trade.get('current_value', trade.get('market_value', shares * price if shares and price else 0))
                else:
                    allocated = trade.get('allocated_capital', shares * price if shares and price else 0)
                is_position_adjustment = trade.get('is_position_adjustment', False)
                sell_pct = trade.get('sell_pct', 100)

                # Create descriptive action label
                if action == 'SELL':
                    if sell_pct == 100:
                        action_label = "LIQUIDATE"
                    else:
                        action_label = f"TRIM ({sell_pct}%)"
                elif action == 'BUY':
                    if is_position_adjustment:
                        action_label = "INCREASE"
                    else:
                        action_label = "BUY"
                else:
                    action_label = action

                # Show compliance flag if present
                flagged = trade.get('compliance_flagged', False)
                flag_note = " [COMPLIANCE FLAG]" if flagged else ""

                print(f"\n  Trade #{i}: {action_label} {ticker}{flag_note}")
                print(f"    Shares: {shares:.0f} @ ${price:.2f} = ${allocated:,.2f}")

                # Show scores if available
                if 'composite_score' in trade:
                    print(f"    Composite Score: {trade['composite_score']:.1f}/100")

                if 'sector' in trade:
                    print(f"    Sector: {trade['sector']}")

                # Show compliance note if flagged
                if flagged and 'compliance_note' in trade:
                    print(f"    Note: {trade['compliance_note']}")

        # CEO's Strengths and Concerns
        if ceo_review['strengths']:
            print(f"\n" + "-" * 80)
            print("STRENGTHS:")
            print("-" * 80)
            for strength in ceo_review['strengths']:
                print(f"  + {strength}")

        if ceo_review['concerns']:
            print(f"\n" + "-" * 80)
            print("CONCERNS:")
            print("-" * 80)
            for concern in ceo_review['concerns']:
                print(f"  - {concern}")

        # User Decision
        print(f"\n" + "=" * 80)
        print("YOUR DECISION:")
        print("=" * 80)
        print("\n  [A] Approve Plan - Lock it in for execution")
        print("  [R] Reject Plan - Return to menu")
        print("  [V] View Detailed Analysis - (Future: show full department reports)")
        print("  [M] Monitor Departments - (Future: check individual status)")

        choice = input("\nYour choice: ").strip().upper()

        if choice == 'A':
            # Approve plan
            approval_result = self.ceo.approve_plan(plan['plan_id'])
            print(f"\n[CEO] {approval_result['message']}")
            print("\nNext Steps:")
            for step in approval_result['next_steps']:
                print(f"  - {step}")

        elif choice == 'R':
            print("\n[CEO] Understood. Plan rejected. We can try again with different criteria if you'd like.")

        else:
            print("\n[CEO] I didn't catch that. Returning to main menu.")

        input("\nPress Enter to continue...")

    def _display_critical_escalation(self, result: dict):
        """Display critical escalation requiring user decision"""
        escalation = result['escalation']
        ceo_analysis = result['ceo_analysis']

        print("\n" + "=" * 80)
        print(" " * 25 + "CRITICAL ISSUE")
        print("=" * 80)

        print(f"\n[CEO] {result['message']}")
        print(f"\nStage: {escalation['stage'].upper()}")
        print(f"Severity: {escalation['severity']}")

        print(f"\n{ceo_analysis['summary']}")
        print(f"Impact: {ceo_analysis['impact']}")

        print(f"\n" + "-" * 80)
        print("OPTIONS AVAILABLE:")
        print("-" * 80)
        for i, opt_analysis in enumerate(ceo_analysis['options_analysis'], 1):
            print(f"\n  [{i}] {opt_analysis['option']}")
            print(f"      CEO Assessment: {opt_analysis['ceo_assessment']}")

        print(f"\n[CEO] My Recommendation: {ceo_analysis['ceo_recommendation']}")

        input("\nPress Enter to return to menu (manual resolution required)...")

    def _display_ceo_recommendation(self, result: dict):
        """Display CEO's recommendation for handling warning"""
        escalation = result['escalation']
        ceo_decision = result['ceo_decision']

        print("\n" + "=" * 80)
        print(" " * 25 + "CEO RECOMMENDATION")
        print("=" * 80)

        print(f"\n[CEO] {result['message']}")
        print(f"\nStage: {escalation['stage'].upper()}")
        print(f"Issue: {escalation['issue_type']}")

        print(f"\n[CEO] My Analysis: {ceo_decision['rationale']}")
        print(f"[CEO] Recommendation: {ceo_decision['recommendation']}")

        input("\nPress Enter to continue...")

    def _display_workflow_failure(self, result: dict):
        """Display workflow failure"""
        print("\n" + "=" * 80)
        print(" " * 25 + "WORKFLOW ERROR")
        print("=" * 80)

        print(f"\n[CEO] {result['ceo_message']}")
        print(f"\nError: {result['error']}")
        print(f"Recommendation: {result['recommendation']}")

        input("\nPress Enter to continue...")

    def view_dashboard(self):
        """View portfolio dashboard"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 25 + "PORTFOLIO DASHBOARD")
        print("=" * 80)
        print("\n[CEO] Retrieving your dashboard...")

        result = self.ceo.handle_user_request("view_dashboard")

        if result['status'] == 'SUCCESS':
            dashboard = result['dashboard']

            # Display performance
            if 'performance' in dashboard:
                perf = dashboard['performance']
                print("\nPORTFOLIO PERFORMANCE:")
                print("-" * 80)

                # Primary metrics (always show these first)
                print(f"  Starting Capital:    ${perf.get('starting_capital', 100000):>12,.2f}")
                print(f"  Current Equity:      ${perf.get('current_equity', 0):>12,.2f}")
                print(f"  Total Return:        ${perf.get('total_return_dollars', 0):>12,.2f}  ({perf.get('total_return_pct', 0):+.2f}%)")
                print()
                print(f"  Today's P/L:         ${perf.get('daily_pl', 0):>12,.2f}  ({perf.get('daily_pl_pct', 0):+.2f}%)")
                print(f"  Cash Available:      ${perf.get('cash', 0):>12,.2f}")
                print(f"  Buying Power:        ${perf.get('buying_power', 0):>12,.2f}")
                print(f"  Open Positions:      {perf.get('positions_count', 0):>12}")
                print()

                # Circuit breaker status indicator
                daily_loss_pct = abs(perf.get('daily_pl_pct', 0)) if perf.get('daily_pl_pct', 0) < 0 else 0
                if daily_loss_pct >= 15:
                    print(f"  Circuit Breaker:     RED ALERT ({daily_loss_pct:.1f}% loss today)")
                elif daily_loss_pct >= 10:
                    print(f"  Circuit Breaker:     ORANGE ({daily_loss_pct:.1f}% loss today - new BUYs blocked)")
                elif daily_loss_pct >= 5:
                    print(f"  Circuit Breaker:     YELLOW ({daily_loss_pct:.1f}% loss today - monitor)")
                else:
                    print(f"  Circuit Breaker:     NORMAL")

            # Display open positions
            if 'open_positions' in dashboard:
                positions = dashboard['open_positions']
                print(f"\nOPEN POSITIONS ({len(positions)}):")
                print("-" * 120)
                print(f"  {'TICKER':<6} {'QTY':>7} {'ENTRY':>9} {'CURRENT':>9} {'COST BASIS':>12} {'MKT VALUE':>12} {'P&L':>10}")
                print("-" * 120)

                total_cost_basis = 0
                total_market_value = 0
                total_pnl = 0

                for pos in positions:  # Show all positions
                    ticker = pos.get('ticker', 'N/A')
                    shares = pos.get('shares', 0)
                    entry = pos.get('entry_price', 0)
                    current = pos.get('current_price', 0)
                    pnl = pos.get('unrealized_pl', 0)

                    cost_basis = shares * entry
                    market_value = shares * current

                    total_cost_basis += cost_basis
                    total_market_value += market_value
                    total_pnl += pnl

                    print(f"  {ticker:<6} {shares:>7.2f} ${entry:>8.2f} ${current:>8.2f} ${cost_basis:>11.2f} ${market_value:>11.2f} ${pnl:>+9.2f}")

                # Print totals
                print("-" * 120)
                print(f"  {'TOTAL':<6} {'':<7} {'':<9} {'':<9} ${total_cost_basis:>11.2f} ${total_market_value:>11.2f} ${total_pnl:>+9.2f}")
                print("-" * 120)

            print(f"\n[CEO] Dashboard displayed. {result['message']}")

        else:
            print(f"\n[CEO] {result['message']}")

        input("\nPress Enter to continue...")

    def quick_portfolio_summary(self):
        """Quick portfolio summary"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 25 + "QUICK PORTFOLIO SUMMARY")
        print("=" * 80)

        result = self.ceo.handle_user_request("get_portfolio_summary")

        if result['status'] == 'SUCCESS':
            summary = result['summary']
            print(f"\n[CEO] Here's your current portfolio at a glance:")
            print(f"\n  Open Positions: {summary['position_count']}")
            print(f"  Cash Balance: ${summary['cash_balance']:,.2f}")
            print(f"  Total Portfolio Value: ${summary['portfolio_value']:,.2f}")

            if summary['positions']:
                print(f"\n  Top Positions:")
                for pos in summary['positions']:
                    ticker = pos.get('ticker', pos.get('symbol', 'N/A'))
                    shares = pos.get('shares', pos.get('qty', 0))
                    print(f"    - {ticker}: {shares} shares")

        else:
            print(f"\n[CEO] {result['message']}")

        input("\nPress Enter to continue...")

    def execute_approved_plan(self):
        """Execute approved trading plan"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 25 + "EXECUTE APPROVED PLAN")
        print("=" * 80)

        # Check execution gates
        print("\n[Mode Manager] Checking execution gates...")
        print()

        # For now, assume plan was generated recently (would need to track this in real implementation)
        plan_time = datetime.now()  # Placeholder - should get from approved plan file

        # Check if we can execute
        gate_check = self.mode_manager.can_execute_plan(
            plan_generated_at=plan_time,
            current_portfolio_loss_pct=0.0,  # Placeholder - would fetch real P&L
            allow_override=True
        )

        # Display gate results
        print("EXECUTION GATES:")
        print("-" * 80)

        for gate in gate_check['gates_passed']:
            print(f"  {gate}")

        for gate in gate_check['gates_failed']:
            print(f"  {gate}")

        print()
        print(f"RECOMMENDATION: {gate_check['recommendation']}")
        print("-" * 80)
        print()

        # Display warnings if any
        if gate_check['warnings']:
            print("WARNINGS:")
            for warning in gate_check['warnings']:
                print(f"  - {warning}")
            print()

        # Handle blocks
        if not gate_check['can_execute']:
            print("[Mode Manager] Execution BLOCKED. Cannot proceed with trades.")
            input("\nPress Enter to return to menu...")
            return

        # Handle overrides
        if gate_check['requires_override']:
            print("[Mode Manager] Override required to proceed.")
            override = input("\nDo you want to override and proceed anyway? (yes/no): ").strip().lower()
            if override != 'yes':
                print("\n[Mode Manager] Execution cancelled by user.")
                input("\nPress Enter to return to menu...")
                return
            print("\n[Mode Manager] User override confirmed. Proceeding with execution...")
            print()

        print("\n[CEO] Checking for approved plan...")

        result = self.ceo.handle_user_request("execute_plan")

        if result['status'] == 'EXECUTION_INITIATED':
            print(f"\n[CEO] {result['message']}")
            print(f"\nPlan ID: {result['plan_id']}")
            print(f"Trades Submitted: {result['trades_submitted']}")
            print("\n[CEO] Execution is underway. I'll keep you informed of progress.")

        else:
            print(f"\n[CEO] {result['message']}")

        input("\nPress Enter to continue...")

    def select_ai_model(self):
        """Allow user to select AI model for portfolio optimization"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 25 + "SELECT AI MODEL")
        print("=" * 80)
        print("\n[CEO] Choose the AI model for portfolio analysis:\n")

        models = {
            '1': {'name': 'gpt-4o-mini', 'cost': '$0.50/run', 'speed': 'Fast (2-3 min)', 'quality': 'Good'},
            '2': {'name': 'gpt-4o', 'cost': '$2-3/run', 'speed': 'Fast (2-3 min)', 'quality': 'Excellent'},
            '3': {'name': 'gpt-5', 'cost': '$10-20/run', 'speed': 'Slow (10-15 min)', 'quality': 'Best'}
        }

        print("  [1] GPT-4o-mini (Budget) - $0.50/run")
        print("      Fast, efficient, good for daily trading")
        print("      Monthly cost: ~$10-20 (20 trading days)")
        print()
        print("  [2] GPT-4o (Balanced) - $2-3/run")
        print("      Fast, excellent reasoning, best balance")
        print("      Monthly cost: ~$40-60 (20 trading days)")
        print()
        print("  [3] GPT-5 (Premium) - $10-20/run")
        print("      Extended reasoning, best quality, very slow")
        print("      Monthly cost: ~$200-400 (20 trading days)")
        print()
        print(f"Current selection: {getattr(self, 'selected_model', 'gpt-4o-mini')}")
        print()

        choice = input("Select model (1-3, or press Enter to keep current): ").strip()

        if choice in models:
            model_info = models[choice]
            self.selected_model = model_info['name']
            print(f"\n[CEO] Model set to {model_info['name']}")
            print(f"     Cost: {model_info['cost']}, Speed: {model_info['speed']}")
            print(f"     This will be used for your next trading plan request.")
        elif choice == '':
            print(f"\n[CEO] Keeping current model: {getattr(self, 'selected_model', 'gpt-4o-mini')}")
        else:
            print("\n[CEO] Invalid choice. Keeping current model.")

        input("\nPress Enter to continue...")

    def refresh_universe(self):
        """Run weekly universe refresh script"""
        from datetime import date
        import subprocess

        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 20 + "WEEKLY UNIVERSE REFRESH")
        print("=" * 80)
        print("\n[CEO] This will generate an optimized swing trading universe for the week.\n")

        # Check if weekend
        today = date.today()
        day_name = today.strftime('%A')
        is_weekend = today.weekday() >= 5

        if not is_weekend:
            print(f"[CEO] Today is {day_name} - Universe refresh should run on weekends only.")
            print()
            print("This operation screens thousands of stocks and takes 10-20 minutes.")
            print("It's recommended to run this on Saturday or Sunday when markets are closed.")
            print()
            response = input("Run anyway? (yes/no): ").strip().lower()

            if response not in ['yes', 'y']:
                print("\n[CEO] Understood. Cancelled.")
                input("\nPress Enter to return to main menu...")
                return
        else:
            print(f"[CEO] Today is {day_name} - Perfect time for universe refresh!")
            print()

        print("[CEO] Starting universe refresh...")
        print()
        print("This will:")
        print("  1. Screen all tradeable US stocks (~8000)")
        print("  2. Apply swing trading filters (market cap, volume, volatility)")
        print("  3. Generate optimized universe (~800 stocks)")
        print("  4. Update ticker_universe.txt for Monday's trading")
        print()
        print("Expected time: 10-20 minutes")
        print()

        # Run refresh script
        try:
            result = subprocess.run(
                ['python', 'refresh_universe.py'],
                capture_output=False,
                text=True
            )

            if result.returncode == 0:
                print("\n[CEO] Universe refresh completed successfully!")
                print("     New universe will be used starting Monday.")
            else:
                print("\n[CEO] Universe refresh encountered issues. Please check the output above.")

        except Exception as e:
            print(f"\n[CEO] ERROR running refresh script: {e}")

        input("\nPress Enter to return to main menu...")

    def run(self):
        """Main control panel loop"""
        # Initialize default model
        if not hasattr(self, 'selected_model'):
            self.selected_model = 'gpt-4o-mini'  # Budget-friendly default

        while self.running:
            self.clear_screen()
            self.display_header()
            self.display_main_menu()

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.request_trading_plan()

            elif choice == '2':
                self.view_dashboard()

            elif choice == '3':
                self.execute_approved_plan()

            elif choice == '4':
                self.select_ai_model()

            elif choice == '5':
                self.refresh_universe()

            elif choice == '0':
                self.clear_screen()
                print("\n" + "=" * 80)
                print(" " * 25 + "SENTINEL CORPORATION")
                print("=" * 80)
                print("\n[CEO] Thank you for your business. Have a great day!")
                print()
                self.running = False

            else:
                print("\n[CEO] I didn't understand that. Please choose from the menu.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    panel = SentinelControlPanel()
    panel.run()
