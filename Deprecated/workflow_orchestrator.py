"""
Workflow Orchestrator
=====================
Coordinates SC's departments to generate portfolio plan.

Flow:
1. Research Department: Screen and analyze stocks
2. Risk Department: Calculate position sizes
3. Portfolio Department: Apply constraints and generate orders
4. Save orders as JSON plan for preview/approval

This is called by the Control Panel when user selects "Generate Portfolio Plan".
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, date

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from Utils.data_source import create_data_source


class WorkflowOrchestrator:
    """
    Orchestrates SC departments to generate trading plan.
    """

    def __init__(self):
        """Initialize orchestrator."""
        self.project_root = Path(__file__).parent
        self.db_path = self.project_root / "sentinel.db"
        self.messages_dir = self.project_root / "Messages_Between_Departments"

        # Initialize data source
        self.data_source = create_data_source(str(self.db_path))

    def generate_portfolio_plan(self) -> dict:
        """
        Generate portfolio plan by running SC departments.

        Returns:
            dict: Portfolio plan with proposed trades
        """
        print()
        print("=" * 80)
        print("SENTINEL CORPORATION - PORTFOLIO PLAN GENERATION")
        print("=" * 80)
        print()

        # Get current portfolio state
        print("[1/4] Checking current portfolio state...")
        current_positions = self.data_source.get_position_count()
        deployed_capital = self.data_source.get_deployed_capital()
        cash_balance = self.data_source.get_account_balance()
        buying_power = self.data_source.get_buying_power()

        print(f"  Current Positions: {current_positions}")
        print(f"  Deployed Capital:  ${deployed_capital:,.2f}")
        print(f"  Cash Balance:      ${cash_balance:,.2f}")
        print(f"  Buying Power:      ${buying_power:,.2f}")
        print()

        # Step 1: Research Department (screening + analysis)
        print("[2/4] Running Research Department...")
        print("  [INFO] This step is currently STUBBED (would run GPT-4 + Perplexity)")
        print("  [INFO] Skipping to save AI API costs")
        print("  [INFO] Using mock research data for testing")
        print()

        # Mock research results (replace with real call later)
        research_results = {
            'candidates': [
                {
                    'ticker': 'AAPL',
                    'research_composite_score': 85.0,
                    'current_price': 180.50,
                    'recommendation': 'BUY',
                },
                {
                    'ticker': 'GOOGL',
                    'research_composite_score': 82.0,
                    'current_price': 140.25,
                    'recommendation': 'BUY',
                },
                {
                    'ticker': 'MSFT',
                    'research_composite_score': 88.0,
                    'current_price': 415.30,
                    'recommendation': 'BUY',
                },
            ]
        }

        print(f"  Found {len(research_results['candidates'])} candidates")
        print()

        # Step 2: Risk Department (position sizing)
        print("[3/4] Running Risk Department...")
        print("  [INFO] This step is currently STUBBED")
        print("  [INFO] Using simple position sizing for testing")
        print()

        # Mock risk calculations (replace with real call later)
        max_position_size = buying_power * 0.10  # 10% per position

        risk_results = []
        for candidate in research_results['candidates']:
            shares = int(max_position_size / candidate['current_price'])
            position_value = shares * candidate['current_price']

            risk_results.append({
                'ticker': candidate['ticker'],
                'price': candidate['current_price'],
                'shares': shares,
                'position_value': position_value,
                'score': candidate['research_composite_score'],
            })

        print(f"  Calculated position sizes for {len(risk_results)} candidates")
        print()

        # Step 3: Portfolio Department (constraint filtering)
        print("[4/4] Running Portfolio Department...")
        print("  [INFO] This step is currently STUBBED")
        print("  [INFO] Applying basic constraints for testing")
        print()

        # Mock portfolio filtering (replace with real call later)
        max_positions = 10
        available_slots = max_positions - current_positions

        approved_trades = []
        if available_slots > 0:
            # Take top N candidates by score
            sorted_candidates = sorted(risk_results, key=lambda x: x['score'], reverse=True)
            approved_trades = sorted_candidates[:available_slots]

        print(f"  Approved {len(approved_trades)} trades (max {available_slots} slots available)")
        print()

        # Generate plan summary
        total_value = sum(t['position_value'] for t in approved_trades)

        plan_data = {
            'generated_at': datetime.now().isoformat(),
            'status': 'PENDING_APPROVAL',
            'current_state': {
                'positions': current_positions,
                'deployed_capital': deployed_capital,
                'cash_balance': cash_balance,
                'buying_power': buying_power,
            },
            'orders': [
                {
                    'ticker': t['ticker'],
                    'action': 'BUY',
                    'shares': t['shares'],
                    'estimated_price': t['price'],
                    'estimated_value': t['position_value'],
                    'score': t['score'],
                }
                for t in approved_trades
            ],
            'summary': {
                'total_orders': len(approved_trades),
                'total_value': total_value,
                'available_cash': cash_balance,
                'remaining_cash': cash_balance - total_value,
            }
        }

        print("=" * 80)
        print("PORTFOLIO PLAN GENERATED")
        print("=" * 80)
        print()
        print(f"Total Orders:    {plan_data['summary']['total_orders']}")
        print(f"Total Value:     ${plan_data['summary']['total_value']:,.2f}")
        print(f"Available Cash:  ${plan_data['summary']['available_cash']:,.2f}")
        print(f"Remaining Cash:  ${plan_data['summary']['remaining_cash']:,.2f}")
        print()

        if approved_trades:
            print("Proposed Trades:")
            for order in plan_data['orders']:
                print(f"  BUY {order['ticker']:6} x{order['shares']:3} @ ${order['estimated_price']:.2f} "
                      f"= ${order['estimated_value']:,.2f} (score: {order['score']:.1f})")
            print()

        return plan_data


def test_workflow():
    """Test the workflow orchestrator."""
    orchestrator = WorkflowOrchestrator()
    plan = orchestrator.generate_portfolio_plan()

    # Save plan to file
    today = datetime.now().strftime('%Y-%m-%d')
    plan_file = Path(f"proposed_trades_{today}.json")

    with open(plan_file, 'w') as f:
        json.dump(plan, f, indent=2)

    print(f"Plan saved to: {plan_file}")
    print()
    print("=" * 80)
    print("[SUCCESS] Workflow test completed")
    print("=" * 80)


if __name__ == "__main__":
    test_workflow()
