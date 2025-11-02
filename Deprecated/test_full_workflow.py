"""
Test Full Workflow
==================
Simulates the complete user workflow:
1. Generate portfolio plan
2. View plan
3. Approve plan
4. (Would execute on Monday when market opens)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow_orchestrator import WorkflowOrchestrator


def test_full_workflow():
    """Test the complete workflow."""
    print()
    print("=" * 80)
    print("SENTINEL CORPORATION - FULL WORKFLOW TEST")
    print("=" * 80)
    print()

    # Step 1: Generate Plan
    print("[STEP 1] Generate Portfolio Plan")
    print("-" * 80)
    orchestrator = WorkflowOrchestrator()
    plan = orchestrator.generate_portfolio_plan()
    print()

    # Step 2: View Plan
    print("[STEP 2] View Saved Plan")
    print("-" * 80)
    today = datetime.now().strftime('%Y-%m-%d')
    plan_file = Path(f"proposed_trades_{today}.json")

    with open(plan_file, 'r') as f:
        loaded_plan = json.load(f)

    print(f"Plan Status: {loaded_plan['status']}")
    print(f"Total Orders: {loaded_plan['summary']['total_orders']}")
    print(f"Total Value: ${loaded_plan['summary']['total_value']:,.2f}")
    print()

    print("Orders:")
    for order in loaded_plan['orders']:
        print(f"  {order['action']:4} {order['ticker']:6} x{order['shares']:3} "
              f"@ ${order['estimated_price']:.2f} = ${order['estimated_value']:,.2f}")
    print()

    # Step 3: Approve Plan
    print("[STEP 3] Approve Plan for Execution")
    print("-" * 80)
    loaded_plan['status'] = 'APPROVED'
    loaded_plan['approved_at'] = datetime.now().isoformat()

    with open(plan_file, 'w') as f:
        json.dump(loaded_plan, f, indent=2)

    print(f"[SUCCESS] Plan approved and saved")
    print(f"Status: {loaded_plan['status']}")
    print()

    # Step 4: Show what would happen on Monday
    print("[STEP 4] Ready for Execution (Monday Morning)")
    print("-" * 80)
    print("[INFO] When market opens Monday 9:30 AM:")
    print("  1. SC detects ONLINE mode (market open, no trades today)")
    print("  2. User selects 'Execute Approved Trading Plan'")
    print("  3. Orders are submitted to Alpaca:")
    for order in loaded_plan['orders']:
        print(f"     - BUY {order['ticker']} x{order['shares']} (market order)")
    print("  4. SC auto-switches to OFFLINE mode (already traded today)")
    print("  5. User can safely continue development")
    print()

    print("=" * 80)
    print("[SUCCESS] Full workflow test completed!")
    print("=" * 80)
    print()
    print(f"Plan file: {plan_file}")
    print(f"Status: {loaded_plan['status']}")
    print()


if __name__ == "__main__":
    test_full_workflow()
