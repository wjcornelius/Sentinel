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


class SentinelControlPanel:
    """
    Control Panel - User Interface to CEO
    """

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.ceo = CEO(self.project_root)
        self.running = True

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
        print("MAIN OPTIONS:")
        print()
        print("  [1] Request Trading Plan")
        print("      (CEO will coordinate all departments to generate a comprehensive plan)")
        print()
        print("  [2] View Portfolio Dashboard")
        print("      (Real-time portfolio status and performance)")
        print()
        print("  [3] Execute Approved Plan")
        print("      (Submit approved trades to market - available when market is open)")
        print()
        print("  [4] Quick Portfolio Summary")
        print("      (Fast overview of current positions)")
        print()
        print("  [0] Exit")
        print()
        print("=" * 80)

    def request_trading_plan(self):
        """Request trading plan from CEO"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(" " * 25 + "REQUEST TRADING PLAN")
        print("=" * 80)
        print("\n[CEO] Understood. I'll have my team prepare a trading plan for you.")
        print("[CEO] This will take a moment while we coordinate all departments...\n")

        input("Press Enter to begin...")
        print()

        # Request plan from CEO
        result = self.ceo.handle_user_request("generate_plan")

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
                allocated = trade.get('allocated_capital', shares * price if shares and price else 0)

                # Show compliance flag if present
                flagged = trade.get('compliance_flagged', False)
                flag_note = " [COMPLIANCE FLAG]" if flagged else ""

                print(f"\n  Trade #{i}: {ticker}{flag_note}")
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
                for key, value in list(perf.items())[:10]:  # Show first 10 metrics
                    if isinstance(value, (int, float)):
                        if 'pct' in key.lower() or 'rate' in key.lower():
                            print(f"  {key}: {value:.2f}%")
                        elif 'pnl' in key.lower() or 'value' in key.lower() or 'capital' in key.lower():
                            print(f"  {key}: ${value:,.2f}")
                        else:
                            print(f"  {key}: {value:.2f}")
                    else:
                        print(f"  {key}: {value}")

            # Display open positions
            if 'open_positions' in dashboard:
                positions = dashboard['open_positions']
                print(f"\nOPEN POSITIONS ({len(positions)}):")
                print("-" * 80)
                for pos in positions[:10]:  # Show first 10
                    ticker = pos.get('ticker', 'N/A')
                    shares = pos.get('shares', 0)
                    entry = pos.get('entry_price', 0)
                    current = pos.get('current_price', 0)
                    pnl = pos.get('unrealized_pl', 0)
                    print(f"  {ticker:6} x{shares:7.2f} @ ${entry:7.2f} → ${current:7.2f} | P&L: ${pnl:+7.2f}")

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

    def run(self):
        """Main control panel loop"""
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
                self.quick_portfolio_summary()

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
