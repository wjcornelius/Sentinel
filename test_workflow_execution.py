"""
Quick diagnostic: Test workflow execution
"""
import sys
from pathlib import Path

sys.path.insert(0, '.')

from Departments.Executive.ceo import CEO

def test_workflow():
    print("=" * 80)
    print("DIAGNOSTIC: Testing Workflow Execution")
    print("=" * 80)

    try:
        # Initialize CEO
        print("\n[1] Initializing CEO...")
        ceo = CEO(Path('.'))
        print("    [OK] CEO initialized")

        # Request trading plan
        print("\n[2] Requesting trading plan...")
        result = ceo.handle_user_request('generate_plan')

        print(f"\n[3] Result received:")
        print(f"    Status: {result.get('status')}")
        print(f"    Keys: {list(result.keys())}")

        if result.get('status') == 'READY_FOR_USER_APPROVAL':
            print("\n    [OK] Plan ready for approval")
            plan = result.get('plan', {})
            summary = plan.get('summary', {})
            print(f"    Total trades: {summary.get('total_trades', 0)}")
            print(f"    Quality score: {summary.get('overall_quality_score', 0)}")

            # Check what trades are in the plan
            trades = plan.get('trades', [])
            if trades:
                print(f"\n    Proposed trades ({len(trades)}):")
                for trade in trades[:5]:
                    print(f"      - {trade.get('ticker', 'N/A')}: {trade.get('shares', 0)} shares")
            else:
                print("\n    [WARNING] No trades in plan!")

        elif result.get('status') == 'WORKFLOW_FAILED':
            print(f"\n    [ERROR] Workflow failed:")
            print(f"    Error: {result.get('error')}")
            print(f"    CEO Message: {result.get('ceo_message')}")

        elif result.get('status') == 'CRITICAL_ISSUE_REQUIRES_USER_DECISION':
            print(f"\n    ! Critical issue:")
            print(f"    Message: {result.get('message')}")

        else:
            print(f"\n    ? Unexpected status: {result.get('status')}")
            print(f"    Message: {result.get('message')}")

    except Exception as e:
        print(f"\n[ERROR]: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_workflow()
