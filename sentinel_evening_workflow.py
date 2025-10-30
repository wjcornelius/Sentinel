# -*- coding: utf-8 -*-
# sentinel_evening_workflow.py
# Evening Workflow Orchestration - Stop-Loss Only Architecture
# Week 1+2 Implementation

"""
Evening Workflow - Runs once per day after market close (7:00 PM or later)

Workflow Steps:
1. Reconcile fills (check which entry orders filled today)
2. Update trailing stops (protect profits on winning positions)
3. Check profit-taking (identify positions at +16% target)
4. Cleanup orphaned stops (cancel stops for closed positions)
5. Run conviction analysis (3-tier pipeline: technical -> AI screening -> deep analysis)
6A. Execute SELL signals (Tier 3 conviction-based exits - frees up cash)
6B. Submit new BUY entry orders (conviction-weighted allocation with stop-loss pairs)
7. Generate daily summary report

Computer uptime required: 30-45 minutes (includes AI analysis)
Frequency: Once per trading day
Timing: After market close (7:00 PM or later)

NOTE: Step 6A executes BEFORE 6B to ensure SELL orders free up cash for BUY orders.
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
from sentinel.tier1_technical_filter import run_tier1_filter
from sentinel.tier2_ai_screening import run_tier2_screening
from sentinel.context_builder import build_context
from sentinel.tier3_conviction_analysis import run_tier3_analysis
from sentinel.order_generator import generate_entry_orders
from sentinel.perplexity_news import PerplexityNewsGatherer
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


def step_5_run_conviction_analysis(api, logger):
    """Step 5: Run conviction analysis (Three-Tier Pipeline)."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 5: Run Conviction Analysis (3-Tier Pipeline)")
    logger.info("=" * 70)

    try:
        # Get real-time market overview (Perplexity)
        logger.info("  Gathering real-time market overview...")
        try:
            perplexity = PerplexityNewsGatherer(logger=logger)
            market_overview = perplexity.gather_market_overview(max_words=300)
            market_context = market_overview.get('market_summary', 'Market conditions vary - see detailed analysis')
            logger.info(f"  Market overview gathered: {len(market_context)} chars")
        except Exception as e:
            logger.warning(f"  Could not fetch market overview: {e}. Using fallback.")
            market_context = "Market conditions vary - see detailed analysis"

        # Get test universe (for now, use a subset - will expand to Russell 3000 later)
        logger.info("  Fetching universe...")
        positions = api.list_positions()
        portfolio_symbols = [p.symbol for p in positions]

        # For now, use portfolio + common stocks as universe
        universe = list(set(portfolio_symbols + [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AMD',
            'NFLX', 'ADBE', 'CRM', 'ORCL', 'AVGO', 'CSCO', 'INTC', 'QCOM',
            'TXN', 'AMAT', 'MU', 'KLAC', 'LRCX', 'ASML', 'SHOP',
            'PYPL', 'V', 'MA', 'JPM', 'BAC', 'WFC', 'GS', 'MS',
            'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'LLY'
        ]))
        logger.info(f"  Universe: {len(universe)} symbols")

        # Tier 1: Technical Filter
        logger.info("  Running Tier 1 (Technical Filter)...")
        tier1_candidates = run_tier1_filter(
            api=api,
            universe_symbols=universe,
            logger=logger,
            target_count=250
        )
        logger.info(f"  Tier 1 complete: {len(tier1_candidates)} candidates")

        if not tier1_candidates:
            logger.warning("  No candidates from Tier 1, skipping analysis")
            return {'success': True, 'signals': [], 'reason': 'no_tier1_candidates'}

        # Tier 2: AI Screening (with real market context)
        logger.info("  Running Tier 2 (AI Screening)...")
        tier2_finalists = run_tier2_screening(
            api=api,
            tier1_candidates=tier1_candidates,
            market_context=market_context,  # Real-time market context now!
            logger=logger,
            target_count=70
        )
        logger.info(f"  Tier 2 complete: {len(tier2_finalists)} finalists")

        if not tier2_finalists:
            logger.warning("  No finalists from Tier 2, skipping analysis")
            return {'success': True, 'signals': [], 'reason': 'no_tier2_finalists'}

        # Context Builder (with real market context)
        logger.info("  Building hierarchical context...")
        hierarchical_context = build_context(
            tier2_finalists=tier2_finalists,
            market_news=market_context,  # Real-time market context now!
            logger=logger
        )
        logger.info(f"  Context built: {len(hierarchical_context['sector_contexts'])} sectors")

        # Tier 3: Deep Conviction Analysis
        logger.info("  Running Tier 3 (Deep Conviction Analysis)...")
        current_positions = {p.symbol: p for p in positions}
        conviction_results = run_tier3_analysis(
            api=api,
            tier2_finalists=tier2_finalists,
            hierarchical_context=hierarchical_context,
            current_positions=current_positions,
            logger=logger
        )
        logger.info(f"  Tier 3 complete: {len(conviction_results)} analyzed")

        # Filter BUY signals
        buy_signals = [r for r in conviction_results if r['decision'] == 'BUY']
        hold_signals = [r for r in conviction_results if r['decision'] == 'HOLD']
        sell_signals = [r for r in conviction_results if r['decision'] == 'SELL']

        logger.info(f"  Conviction results: {len(buy_signals)} BUY, {len(hold_signals)} HOLD, {len(sell_signals)} SELL")

        return {
            'success': True,
            'signals': buy_signals,
            'conviction_results': conviction_results,
            'tier1_count': len(tier1_candidates),
            'tier2_count': len(tier2_finalists),
            'tier3_count': len(conviction_results)
        }

    except Exception as e:
        logger.error(f"  ERROR in conviction analysis: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e), 'signals': []}


def step_6a_execute_sell_signals(engine, logger, sell_signals, current_positions):
    """
    Step 6A: Execute SELL signals from Tier 3 conviction analysis.

    This handles conviction-based exits (different from stop-losses or profit targets).
    If Tier 3 says "SELL this position", we exit immediately at market.

    CRITICAL: Execute SELL signals BEFORE BUY signals to free up cash first.

    Args:
        engine: OrderExecutionEngine instance
        logger: Logger instance
        sell_signals: List of SELL signals from Tier 3
        current_positions: Dict mapping symbol -> position object

    Returns:
        Dict with execution results
    """
    logger.info("\n" + "=" * 70)
    logger.info("STEP 6A: Execute SELL Signals (Tier 3 Conviction-Based)")
    logger.info("=" * 70)

    try:
        if not sell_signals:
            logger.info("  No SELL signals from Tier 3")
            return {'success': True, 'executed': 0, 'signals': []}

        logger.info(f"  Received {len(sell_signals)} SELL signals from Tier 3")

        # Filter SELL signals to only existing positions
        positions_to_sell = []
        for signal in sell_signals:
            symbol = signal['symbol']
            if symbol in current_positions:
                positions_to_sell.append(signal)
                logger.info(
                    f"  {symbol}: SELL conviction {signal['conviction_score']}/100 - "
                    f"{signal.get('reasoning', 'No reasoning provided')[:80]}"
                )
            else:
                logger.debug(f"  {symbol}: SELL signal but no position held (skipping)")

        if not positions_to_sell:
            logger.info("  No SELL signals match current positions")
            return {'success': True, 'executed': 0, 'signals': []}

        # Execute sells
        executed = 0
        failed = 0
        executed_details = []

        for signal in positions_to_sell:
            symbol = signal['symbol']
            position = current_positions[symbol]
            qty = abs(int(float(position.qty)))

            try:
                logger.info(f"  Submitting market SELL for {symbol}: {qty} shares")

                result = engine.submit_conviction_sell(
                    symbol=symbol,
                    qty=qty,
                    conviction_score=signal['conviction_score'],
                    reasoning=signal.get('reasoning', 'Tier 3 SELL signal')
                )

                if result['success']:
                    executed += 1
                    executed_details.append({
                        'symbol': symbol,
                        'qty': qty,
                        'order_id': result['order_id'],
                        'conviction_score': signal['conviction_score']
                    })
                    logger.info(f"    -> SUCCESS: Sell order {result['order_id']}")
                else:
                    failed += 1
                    logger.error(f"    -> FAILED: {result.get('error', 'Unknown error')}")

            except Exception as e:
                failed += 1
                logger.error(f"    -> ERROR selling {symbol}: {e}")

        logger.info(f"  SELL execution complete: {executed} executed, {failed} failed")

        return {
            'success': True,
            'executed': executed,
            'failed': failed,
            'signals': positions_to_sell,
            'executed_details': executed_details
        }

    except Exception as e:
        logger.error(f"  ERROR executing SELL signals: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e), 'executed': 0}


def step_6_submit_new_entries(engine, api, logger, signals):
    """Step 6: Submit new entry orders (with order generation)."""
    logger.info("\n" + "=" * 70)
    logger.info("STEP 6: Submit New Entry Orders")
    logger.info("=" * 70)

    try:
        if not signals:
            logger.info("  No BUY signals to process")
            return {'success': True, 'submitted': 0}

        logger.info(f"  Processing {len(signals)} BUY signals")

        # Get portfolio value and current positions
        account = api.get_account()
        portfolio_value = float(account.portfolio_value)
        positions = api.list_positions()
        current_positions = {p.symbol: p for p in positions}

        logger.info(f"  Portfolio value: ${portfolio_value:,.2f}")

        # Generate orders
        logger.info("  Generating entry+stop order pairs...")
        order_result = generate_entry_orders(
            api=api,
            conviction_results=signals,
            portfolio_value=portfolio_value,
            current_positions=current_positions,
            logger=logger
        )

        orders = order_result['orders']
        allocation_summary = order_result['allocation_summary']
        notes = order_result['notes']

        logger.info(f"  Orders generated: {len(orders)}")
        logger.info(f"  Total allocation: ${allocation_summary['allocated']:,.2f} ({allocation_summary['allocation_pct']:.1f}%)")

        # Submit orders using execution engine
        submitted = 0
        failed = 0

        for order in orders:
            symbol = order['symbol']
            qty = order['qty']
            entry_price = order['entry_price']
            stop_price = order['stop_price']

            logger.info(f"  Submitting {symbol}: {qty} shares @ ${entry_price:.2f}, stop @ ${stop_price:.2f}")

            try:
                result = engine.submit_entry_with_stop(
                    symbol=symbol,
                    qty=qty,
                    limit_price=entry_price,
                    stop_price=stop_price
                )

                if result['success']:
                    submitted += 1
                    logger.info(f"    -> SUCCESS: Entry {result['entry_order_id']}, Stop {result['stop_order_id']}")
                else:
                    failed += 1
                    logger.error(f"    -> FAILED: {result.get('error', 'Unknown error')}")

            except Exception as e:
                failed += 1
                logger.error(f"    -> ERROR submitting {symbol}: {e}")

        logger.info(f"  Order submission complete: {submitted} submitted, {failed} failed")

        # Log allocation notes
        if notes:
            logger.info("  Allocation notes:")
            for note in notes:
                logger.info(f"    - {note}")

        return {
            'success': True,
            'submitted': submitted,
            'failed': failed,
            'allocation_summary': allocation_summary
        }

    except Exception as e:
        logger.error(f"  ERROR submitting orders: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e), 'submitted': 0}


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

        # Step 6A: Conviction sells
        if 'step_6a' in results and results['step_6a']['success']:
            executed = results['step_6a']['executed']
            failed = results['step_6a'].get('failed', 0)
            if executed > 0 or failed > 0:
                logger.info(f"  Conviction SELL Orders: {executed} executed, {failed} failed")

        # Step 6B: New entries
        if 'step_6b' in results and results['step_6b']['success']:
            submitted = results['step_6b']['submitted']
            failed = results['step_6b'].get('failed', 0)
            if submitted > 0 or failed > 0:
                logger.info(f"  New BUY Orders: {submitted} submitted, {failed} failed")

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

        # Step 5: Run conviction analysis (3-Tier Pipeline)
        results['step_5'] = step_5_run_conviction_analysis(api, logger)

        # Extract signals by decision type
        conviction_results = results['step_5'].get('conviction_results', [])
        buy_signals = [r for r in conviction_results if r['decision'] == 'BUY']
        sell_signals = [r for r in conviction_results if r['decision'] == 'SELL']
        hold_signals = [r for r in conviction_results if r['decision'] == 'HOLD']

        # Filter BUY signals by conviction threshold (only execute high-conviction buys)
        BUY_CONVICTION_THRESHOLD = 70  # Only execute BUYs with 70+ conviction (out of 100)
        filtered_buy_signals = [
            r for r in buy_signals
            if r['conviction_score'] >= BUY_CONVICTION_THRESHOLD
        ]

        logger.info(
            f"BUY signal filtering: {len(filtered_buy_signals)}/{len(buy_signals)} "
            f"above {BUY_CONVICTION_THRESHOLD} threshold"
        )
        if len(buy_signals) > len(filtered_buy_signals):
            filtered_out = [r for r in buy_signals if r['conviction_score'] < BUY_CONVICTION_THRESHOLD]
            for signal in filtered_out:
                logger.info(
                    f"  Filtered out: {signal['symbol']} (conviction: {signal['conviction_score']})"
                )

        # Get current positions for SELL signal filtering
        positions = api.list_positions()
        current_positions = {p.symbol: p for p in positions}

        # Step 6A: Execute SELL signals (BEFORE buys to free up cash)
        # NOTE: ALL SELL signals execute regardless of conviction score (safety first)
        results['step_6a'] = step_6a_execute_sell_signals(
            engine, logger, sell_signals, current_positions
        )

        # Step 6B: Submit new BUY entry orders (only high-conviction signals)
        results['step_6b'] = step_6_submit_new_entries(engine, api, logger, filtered_buy_signals)

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
