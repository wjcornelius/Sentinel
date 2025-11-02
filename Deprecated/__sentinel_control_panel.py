"""
Sentinel Corporation - Control Panel
=====================================
Main user interface for Sentinel Corporation trading system.

Features:
- Display current mode (ONLINE/OFFLINE) and market status
- Generate portfolio plan (offline mode)
- Preview/approve/reject trading plans
- Execute approved plan (online mode)
- View dashboard, positions, account info
- Manual mode override controls

Author: Claude Code (CC)
Architecture: Claude from Poe (C(P))
"""

import os
import sys
import json
from datetime import datetime, date
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from Utils.alpaca_client import create_alpaca_client
from Utils.mode_manager import create_mode_manager
from Utils.data_source import create_data_source
from workflow_orchestrator import WorkflowOrchestrator


class SentinelControlPanel:
    """
    Main control panel for Sentinel Corporation.
    """

    def __init__(self):
        """Initialize control panel."""
        self.alpaca_client = None
        self.mode_manager = None
        self.data_source = None

        # Initialize Alpaca if enabled
        if config.ALPACA_PAPER_TRADING_ENABLED:
            try:
                self.alpaca_client = create_alpaca_client()
                if self.alpaca_client.is_connected():
                    self.mode_manager = create_mode_manager(self.alpaca_client)
                    self.data_source = create_data_source()
                else:
                    print("[WARNING] Alpaca enabled but not connected")
                    config.ALPACA_PAPER_TRADING_ENABLED = False
            except Exception as e:
                print(f"[ERROR] Failed to connect to Alpaca: {e}")
                config.ALPACA_PAPER_TRADING_ENABLED = False

        # Create mode manager even if Alpaca disabled (will be in OFFLINE mode)
        if not self.mode_manager:
            self.mode_manager = create_mode_manager()
            self.data_source = create_data_source()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self):
        """Display control panel header with mode and status."""
        print("=" * 80)
        print(" " * 25 + "SENTINEL CORPORATION")
        print(" " * 28 + "Control Panel")
        print("=" * 80)
        print()

        # Get mode summary
        mode_summary = self.mode_manager.get_mode_summary()

        # Display mode
        mode = mode_summary['mode']
        mode_color = '[ONLINE]' if mode == 'ONLINE' else '[OFFLINE]'
        print(f"Current Mode: {mode_color}")
        print(f"Reason: {mode_summary['reason']}")
        print()

        # Display market status if available
        if 'market_status' in mode_summary:
            ms = mode_summary['market_status']
            print(f"Market Status:")
            print(f"  Current Time (ET): {ms['current_time_et']}")
            print(f"  Market Open:       {ms['is_market_open_now']}")
            print(f"  Already Traded:    {ms['already_traded_today']}")
            print()

        # Display account info if Alpaca connected
        if mode_summary['alpaca_connected']:
            account = self.data_source.get_account_balance()
            buying_power = self.data_source.get_buying_power()
            portfolio_value = self.data_source.get_portfolio_value()

            print(f"Account Info (Alpaca GROUND TRUTH):")
            print(f"  Cash:           ${account:,.2f}")
            print(f"  Buying Power:   ${buying_power:,.2f}")
            print(f"  Portfolio Value: ${portfolio_value:,.2f}")
        else:
            print(f"Account Info: Alpaca not connected (simulation mode)")

        print()
        print(f"Data Source: {self.data_source.get_data_source_info()['data_source']}")
        print()
        print("=" * 80)
        print()

    def show_main_menu(self):
        """Display main menu options."""
        print("Main Menu:")
        print()

        # Get available actions from mode manager
        actions = self.mode_manager.get_available_actions()
        action_num = 1

        # Trading actions
        if self.mode_manager.is_online():
            print(f"  {action_num}. Execute Approved Trading Plan (SUBMIT ORDERS)")
            action_num += 1

        # Portfolio plan actions
        print(f"  {action_num}. Generate Portfolio Plan (offline analysis)")
        action_num += 1

        if self._has_saved_plan():
            print(f"  {action_num}. View Saved Portfolio Plan")
            action_num += 1
            print(f"  {action_num}. Approve Plan for Execution")
            action_num += 1
            print(f"  {action_num}. Reject Plan (delete)")
            action_num += 1

        # View actions
        print()
        print(f"  {action_num}. View Current Positions")
        action_num += 1
        print(f"  {action_num}. View Account Summary")
        action_num += 1
        print(f"  {action_num}. View Dashboard")
        action_num += 1

        # Mode controls
        print()
        if self.mode_manager.is_offline():
            if 'force_online' in actions:
                print(f"  {action_num}. Force ONLINE Mode (manual override)")
                action_num += 1
        else:
            print(f"  {action_num}. Force OFFLINE Mode (manual override)")
            action_num += 1

        if self.mode_manager._manual_override is not None:
            print(f"  {action_num}. Clear Manual Override (auto-detect mode)")
            action_num += 1

        print()
        print(f"  0. Exit")
        print()

    def _has_saved_plan(self) -> bool:
        """Check if a saved portfolio plan exists."""
        today = datetime.now().strftime('%Y-%m-%d')
        plan_file = Path(f"proposed_trades_{today}.json")
        return plan_file.exists()

    def _load_saved_plan(self):
        """Load saved portfolio plan from file."""
        today = datetime.now().strftime('%Y-%m-%d')
        plan_file = Path(f"proposed_trades_{today}.json")

        if plan_file.exists():
            with open(plan_file, 'r') as f:
                return json.load(f)
        return None

    def _save_plan(self, plan_data):
        """Save portfolio plan to file."""
        today = datetime.now().strftime('%Y-%m-%d')
        plan_file = Path(f"proposed_trades_{today}.json")

        with open(plan_file, 'w') as f:
            json.dump(plan_data, f, indent=2)

        print(f"[SUCCESS] Plan saved to {plan_file}")

    def _delete_plan(self):
        """Delete saved portfolio plan."""
        today = datetime.now().strftime('%Y-%m-%d')
        plan_file = Path(f"proposed_trades_{today}.json")

        if plan_file.exists():
            plan_file.unlink()
            print(f"[SUCCESS] Plan deleted: {plan_file}")
        else:
            print(f"[INFO] No plan file to delete")

    def generate_portfolio_plan(self):
        """Generate portfolio plan (offline analysis)."""
        print()
        print("=" * 80)
        print("GENERATE PORTFOLIO PLAN")
        print("=" * 80)
        print()

        print("[INFO] This will run SC's analysis pipeline:")
        print("  1. Research Department: Screen and analyze stocks (STUBBED)")
        print("  2. Risk Department: Calculate position sizes (STUBBED)")
        print("  3. Portfolio Department: Apply constraints (STUBBED)")
        print()
        print("[NOTE] Full department integration coming soon")
        print("[NOTE] Currently using mock data for testing")
        print()

        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("[CANCELLED]")
            return

        print()

        # Run workflow orchestrator
        try:
            orchestrator = WorkflowOrchestrator()
            plan_data = orchestrator.generate_portfolio_plan()

            # Plan is already saved by orchestrator
            print("[SUCCESS] Portfolio plan generated and saved!")
            print()
            print("[INFO] Use 'View Saved Portfolio Plan' to preview")
            print("[INFO] Use 'Approve Plan for Execution' to approve it")
            print()

        except Exception as e:
            print()
            print(f"[ERROR] Failed to generate plan: {e}")
            print()
            import traceback
            traceback.print_exc()

        input("Press Enter to continue...")

    def view_saved_plan(self):
        """View saved portfolio plan."""
        plan = self._load_saved_plan()

        if not plan:
            print()
            print("[INFO] No saved plan found")
            print()
            input("Press Enter to continue...")
            return

        print()
        print("=" * 80)
        print("SAVED PORTFOLIO PLAN")
        print("=" * 80)
        print()

        print(f"Generated: {plan['generated_at']}")
        print(f"Status: {plan['status']}")
        print()

        print(f"Orders ({plan['summary']['total_orders']}):")
        print()

        for order in plan['orders']:
            print(f"  {order['action']:4} {order['ticker']:6} x{order['shares']:3} @ ${order['estimated_price']:.2f}")

        print()
        print(f"Total Value: ${plan['summary']['total_value']:,.2f}")
        print()
        print("=" * 80)
        print()
        input("Press Enter to continue...")

    def approve_plan(self):
        """Approve saved plan for execution."""
        plan = self._load_saved_plan()

        if not plan:
            print()
            print("[INFO] No saved plan found")
            print()
            input("Press Enter to continue...")
            return

        print()
        print("=" * 80)
        print("APPROVE PLAN FOR EXECUTION")
        print("=" * 80)
        print()

        print(f"Orders ({plan['summary']['total_orders']}):")
        for order in plan['orders']:
            print(f"  {order['action']:4} {order['ticker']:6} x{order['shares']:3} @ ${order['estimated_price']:.2f}")

        print()
        confirm = input("Approve this plan? This will allow execution when market opens. (y/n): ").strip().lower()

        if confirm == 'y':
            plan['status'] = 'APPROVED'
            plan['approved_at'] = datetime.now().isoformat()
            self._save_plan(plan)

            print()
            print("[SUCCESS] Plan approved for execution!")
            print("[INFO] Run 'Execute Approved Trading Plan' when market is open to submit orders")
        else:
            print()
            print("[CANCELLED]")

        print()
        input("Press Enter to continue...")

    def reject_plan(self):
        """Reject and delete saved plan."""
        print()
        print("=" * 80)
        print("REJECT PLAN")
        print("=" * 80)
        print()

        confirm = input("Delete saved plan? (y/n): ").strip().lower()

        if confirm == 'y':
            self._delete_plan()
            print("[INFO] You can generate a new plan anytime")
        else:
            print("[CANCELLED]")

        print()
        input("Press Enter to continue...")

    def execute_approved_plan(self):
        """Execute approved trading plan (submit orders to Alpaca)."""
        plan = self._load_saved_plan()

        if not plan:
            print()
            print("[ERROR] No saved plan found")
            print()
            input("Press Enter to continue...")
            return

        if plan['status'] != 'APPROVED':
            print()
            print("[ERROR] Plan not approved yet")
            print("[INFO] Use 'Approve Plan for Execution' first")
            print()
            input("Press Enter to continue...")
            return

        # Check if can submit orders
        can_submit, reason = self.mode_manager.can_submit_orders()

        if not can_submit:
            print()
            print(f"[ERROR] Cannot submit orders: {reason}")
            print()
            input("Press Enter to continue...")
            return

        print()
        print("=" * 80)
        print("EXECUTE APPROVED PLAN")
        print("=" * 80)
        print()

        print("[WARNING] This will submit REAL orders to Alpaca!")
        print()

        for order in plan['orders']:
            print(f"  {order['action']:4} {order['ticker']:6} x{order['shares']:3}")

        print()
        confirm = input("Submit these orders to Alpaca? (y/n): ").strip().lower()

        if confirm != 'y':
            print()
            print("[CANCELLED]")
            print()
            input("Press Enter to continue...")
            return

        print()
        print("[INFO] Submitting orders to Alpaca...")
        print()

        # Submit orders to Alpaca
        submitted_orders = []
        failed_orders = []

        for order_spec in plan['orders']:
            try:
                ticker = order_spec['ticker']
                shares = order_spec['shares']
                action = order_spec['action']

                print(f"  Submitting: {action} {ticker} x{shares}...")

                # Submit market order to Alpaca
                if action.upper() == 'BUY':
                    order = self.alpaca_client.submit_market_order(
                        symbol=ticker,
                        qty=shares,
                        side='buy',
                        time_in_force='day'
                    )
                elif action.upper() == 'SELL':
                    order = self.alpaca_client.submit_market_order(
                        symbol=ticker,
                        qty=shares,
                        side='sell',
                        time_in_force='day'
                    )
                else:
                    raise ValueError(f"Unknown action: {action}")

                if order:
                    submitted_orders.append({
                        'ticker': ticker,
                        'order_id': order.id,
                        'status': 'SUBMITTED',
                    })
                    print(f"    [SUCCESS] Order ID: {order.id}")
                else:
                    failed_orders.append(ticker)
                    print(f"    [FAILED] No order returned")

            except Exception as e:
                failed_orders.append(ticker)
                print(f"    [ERROR] {e}")

        print()

        # Update plan status
        plan['status'] = 'EXECUTED'
        plan['executed_at'] = datetime.now().isoformat()
        plan['submitted_orders'] = submitted_orders
        plan['failed_orders'] = failed_orders
        self._save_plan(plan)

        # Show summary
        print("=" * 80)
        print(f"Submitted: {len(submitted_orders)} orders")
        if failed_orders:
            print(f"Failed:    {len(failed_orders)} orders ({', '.join(failed_orders)})")
        print("=" * 80)
        print()

        if submitted_orders:
            print("[SUCCESS] Orders submitted to Alpaca!")
            print("[INFO] SC will now auto-switch to OFFLINE mode (already traded today)")
        else:
            print("[WARNING] No orders were successfully submitted")

        print()
        input("Press Enter to continue...")

    def view_positions(self):
        """View current positions."""
        print()
        print("=" * 80)
        print("CURRENT POSITIONS")
        print("=" * 80)
        print()

        positions = self.data_source.get_open_positions()

        if not positions:
            print("[INFO] No open positions")
        else:
            print(f"Open Positions ({len(positions)}):")
            print()

            for pos in positions:
                ticker = pos.get('ticker') or pos.get('symbol', 'UNKNOWN')
                shares = pos.get('actual_shares') or pos.get('qty', 0)
                entry_price = pos.get('actual_entry_price') or pos.get('avg_entry_price', 0)
                current_price = pos.get('current_price', 0)
                unrealized_pl = pos.get('unrealized_pl', 0)

                print(f"  {ticker:6} x{shares:7.2f} @ ${entry_price:7.2f} | Current: ${current_price:7.2f} | P&L: ${unrealized_pl:7.2f}")

        print()
        print("=" * 80)
        print()
        input("Press Enter to continue...")

    def view_account_summary(self):
        """View account summary."""
        print()
        print("=" * 80)
        print("ACCOUNT SUMMARY")
        print("=" * 80)
        print()

        cash = self.data_source.get_account_balance()
        buying_power = self.data_source.get_buying_power()
        portfolio_value = self.data_source.get_portfolio_value()
        deployed_capital = self.data_source.get_deployed_capital()

        print(f"  Cash Balance:     ${cash:,.2f}")
        print(f"  Buying Power:     ${buying_power:,.2f}")
        print(f"  Portfolio Value:  ${portfolio_value:,.2f}")
        print(f"  Deployed Capital: ${deployed_capital:,.2f}")
        print()

        position_count = self.data_source.get_position_count()
        print(f"  Open Positions:   {position_count}")

        print()
        print(f"Data Source: {self.data_source.get_data_source_info()['data_source']}")

        print()
        print("=" * 80)
        print()
        input("Press Enter to continue...")

    def run(self):
        """Run the control panel."""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_main_menu()

            choice = input("Enter choice: ").strip()

            if choice == '0':
                print()
                print("Exiting Sentinel Corporation Control Panel")
                print()
                break
            elif choice == '1':
                if self.mode_manager.is_online():
                    self.execute_approved_plan()
                else:
                    self.generate_portfolio_plan()
            elif choice == '2':
                if self.mode_manager.is_online():
                    self.generate_portfolio_plan()
                elif self._has_saved_plan():
                    self.view_saved_plan()
                else:
                    self.view_positions()
            elif choice == '3':
                if self._has_saved_plan():
                    self.approve_plan()
                else:
                    self.view_account_summary()
            else:
                print()
                print("[ERROR] Invalid choice")
                print()
                input("Press Enter to continue...")


if __name__ == "__main__":
    panel = SentinelControlPanel()
    panel.run()
