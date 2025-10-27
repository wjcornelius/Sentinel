# -*- coding: utf-8 -*-
# sentinel_evening_workflow.py
# Evening Workflow Orchestration - Stop-Loss Only Architecture
# Week 1 Implementation

"""
Evening Workflow - Runs once per day after market close (7:00 PM or later)

Workflow Steps:
1. Reconcile fills (check which entry orders filled today)
2. Update trailing stops (protect profits on winning positions)
3. Check profit-taking (identify positions at +16% target)
4. Cleanup orphaned stops (cancel stops for closed positions)
5. Run conviction analysis (generate tomorrow's signals) - PLACEHOLDER
6. Submit new entry orders (queue for tomorrow) - PLACEHOLDER
7. Generate daily summary report

Computer uptime required: 15-20 minutes
Frequency: Once per trading day
Timing: After market close (7:00 PM or later)
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from sentinel.execution_engine import OrderExecutionEngine
from sentinel.risk_config import (
    EVENING_WORKFLOW_STEPS,
    EVENING_WORKFLOW_TIMEOUT,
    SEND_DAILY_SUMMARY_EMAIL,
    SEND_EMAIL_ON_ERRORS
)
import alpaca_trade_api as tradeapi


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging for evening workflow."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_filename = log_dir / f"evening_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


# ============================================================================
# WORKFLOW STEPS
# ============================================================================

def step_1_reconcile_fills(engine, logger):
    """Step 1: Reconcile order fills from today."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 1: Reconcile Fills")
    logger.info("=" * 70)

    try:
        counts = engine.reconcile_fills()

        logger.info(f"  Filled: {counts['filled']}")
        logger.info(f"  Cancelled: {counts['cancelled']}")
        logger.info(f"  Expired: {counts['expired']}")
        logger.info(f"  Errors: {counts['errors']}")

        return {'success': True, 'counts': counts}

    except Exception as e:
        logger.error(f"Step 1 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def step_2_update_trailing_stops(engine, logger):
    """Step 2: Update trailing stops for profitable positions."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 2: Update Trailing Stops")
    logger.info("=" * 70)

    try:
        counts = engine.update_trailing_stops()

        logger.info(f"  Raised: {counts['raised']}")
        logger.info(f"  Unchanged: {counts['unchanged']}")
        logger.info(f"  Emergency stops: {counts.get('emergency_stops', 0)}")
        logger.info(f"  Errors: {counts['errors']}")

        return {'success': True, 'counts': counts}

    except Exception as e:
        logger.error(f"Step 2 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def step_3_check_profit_taking(engine, logger):
    """Step 3: Check for profit-taking opportunities."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 3: Check Profit-Taking Opportunities")
    logger.info("=" * 70)

    try:
        result = engine.check_profit_taking()

        candidates = result.get('candidates', [])
        submitted = result.get('submitted', [])

        if not candidates:
            logger.info("  No positions at profit target")
        else:
            logger.info(f"  Found {len(candidates)} profit target candidates:")
            for candidate in candidates:
                logger.info(
                    f"    {candidate['symbol']}: +{candidate['unrealized_pnl_pct']:.1%} "
                    f"(${candidate['unrealized_pl']:.2f})"
                )

            if submitted:
                logger.info(f"  Submitted {len(submitted)} profit-taking orders")
            else:
                logger.info("  Manual approval required - review candidates above")

        return {'success': True, 'candidates': candidates, 'submitted': submitted}

    except Exception as e:
        logger.error(f"Step 3 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def step_4_cleanup_orphaned_stops(engine, logger):
    """Step 4: Cleanup orphaned stop orders."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 4: Cleanup Orphaned Stops")
    logger.info("=" * 70)

    try:
        counts = engine.cleanup_orphaned_stops()

        logger.info(f"  Cancelled: {counts['cancelled']}")
        logger.info(f"  Skipped: {counts['skipped']}")

        return {'success': True, 'counts': counts}

    except Exception as e:
        logger.error(f"Step 4 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def step_5_run_conviction_analysis(logger):
    """Step 5: Run conviction analysis (PLACEHOLDER - Week 2)."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 5: Run Conviction Analysis")
    logger.info("=" * 70)

    logger.info("  [PLACEHOLDER] Conviction analysis not yet implemented")
    logger.info("  This will be implemented in Week 2 with three-tier filtering")

    return {'success': True, 'signals': []}


def step_6_submit_new_entries(engine, logger, signals):
    """Step 6: Submit new entry orders (PLACEHOLDER - Week 2)."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 6: Submit New Entry Orders")
    logger.info("=" * 70)

    logger.info(f"  [PLACEHOLDER] Would submit {len(signals)} entry orders")
    logger.info("  This will be implemented in Week 2 after conviction analysis")

    return {'success': True, 'submitted': 0}


def step_7_generate_summary(logger, results, api):
    """Step 7: Generate daily summary report."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 7: Daily Summary Report")
    logger.info("=" * 70)

    try:
        # Get current account status
        account = api.get_account()
        positions = api.list_positions()

        logger.info("\n=== ACCOUNT STATUS ===")
        logger.info(f"  Portfolio Value: ${float(account.portfolio_value):,.2f}")
        logger.info(f"  Cash: ${float(account.cash):,.2f}")
        logger.info(f"  Buying Power: ${float(account.buying_power):,.2f}")
        logger.info(f"  Active Positions: {len(positions)}")

        if positions:
            total_unrealized = sum(float(pos.unrealized_pl) for pos in positions)
            logger.info(f"  Total Unrealized P&L: ${total_unrealized:,.2f}")

        logger.info("\n=== WORKFLOW RESULTS ===")

        # Step 1: Fills
        if results['step_1']['success']:
            counts = results['step_1']['counts']
            logger.info(f"  Fills Reconciled: {counts['filled']} filled, {counts['expired']} expired")

        # Step 2: Trailing stops
        if results['step_2']['success']:
            counts = results['step_2']['counts']
            logger.info(f"  Trailing Stops: {counts['raised']} raised, {counts.get('emergency_stops', 0)} emergency")

        # Step 3: Profit-taking
        if results['step_3']['success']:
            candidates = results['step_3'].get('candidates', [])
            logger.info(f"  Profit Targets: {len(candidates)} candidates found")

        # Step 4: Cleanup
        if results['step_4']['success']:
            counts = results['step_4']['counts']
            logger.info(f"  Orphaned Stops: {counts['cancelled']} cancelled")

        logger.info("\n=== WORKFLOW COMPLETE ===")

        return {'success': True}

    except Exception as e:
        logger.error(f"Summary generation failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def run_evening_workflow():
    """
    Execute complete evening workflow.

    Returns:
        0 on success, 1 on failure
    """
    logger = setup_logging()

    logger.info("\n" + "=" * 70)
    logger.info("SENTINEL EVENING WORKFLOW")
    logger.info("=" * 70)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Mode: {'LIVE PAPER TRADING' if config.LIVE_TRADING else 'SAFE MODE'}")

    # Initialize Alpaca API
    try:
        logger.info("\nConnecting to Alpaca API...")
        api = tradeapi.REST(
            config.APCA_API_KEY_ID,
            config.APCA_API_SECRET_KEY,
            config.APCA_API_BASE_URL,
            api_version='v2'
        )
        logger.info("  Connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Alpaca: {e}", exc_info=True)
        return 1

    # Initialize execution engine
    engine = OrderExecutionEngine(api)

    # Track results
    results = {}

    # Execute workflow steps
    try:
        # Step 1: Reconcile fills
        results['step_1'] = step_1_reconcile_fills(engine, logger)

        # Step 2: Update trailing stops
        results['step_2'] = step_2_update_trailing_stops(engine, logger)

        # Step 3: Check profit-taking
        results['step_3'] = step_3_check_profit_taking(engine, logger)

        # Step 4: Cleanup orphaned stops
        results['step_4'] = step_4_cleanup_orphaned_stops(engine, logger)

        # Step 5: Run conviction analysis (PLACEHOLDER)
        results['step_5'] = step_5_run_conviction_analysis(logger)

        # Step 6: Submit new entries (PLACEHOLDER)
        signals = results['step_5'].get('signals', [])
        results['step_6'] = step_6_submit_new_entries(engine, logger, signals)

        # Step 7: Generate summary
        results['step_7'] = step_7_generate_summary(logger, results, api)

    except KeyboardInterrupt:
        logger.warning("\nWorkflow interrupted by user")
        return 1

    except Exception as e:
        logger.error(f"\nWorkflow failed with unexpected error: {e}", exc_info=True)
        return 1

    # Check for errors
    errors = [step for step, result in results.items() if not result['success']]

    if errors:
        logger.warning(f"\nWorkflow completed with errors in: {', '.join(errors)}")
        return 1
    else:
        logger.info("\nWorkflow completed successfully with no errors")
        return 0


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    sys.exit(run_evening_workflow())
