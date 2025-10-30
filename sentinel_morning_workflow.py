# -*- coding: utf-8 -*-
# sentinel_morning_workflow.py
# Morning Workflow Orchestration - Stop-Loss Only Architecture
# Week 3 Implementation

"""
Morning Workflow - Runs once per day during market hours (ideally 9 AM PT / noon ET)

Workflow Steps:
1. Reconcile fills (check which entry orders filled yesterday)
2. Update trailing stops (protect profits on winning positions)
3. Check profit-taking (identify positions at +16% target)
4. Cleanup orphaned stops (cancel stops for closed positions)
5. Run conviction analysis (3-tier pipeline with Perplexity news + GPT-4)
6A. Execute SELL signals (Tier 3 conviction-based exits - frees up cash)
6B. Submit new BUY entry orders (conviction-weighted allocation with stop-loss pairs)
7. Generate daily summary report

Computer uptime required: 30-45 minutes (includes AI analysis + news gathering)
Frequency: Once per trading day
Timing: During market hours (9 AM - 12 PM PT optimal, adapts to any time)

TIME-ADAPTIVE: System adjusts validation and slippage based on execution time.
Running earlier (closer to market open) = better execution quality.

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
from sentinel.portfolio_optimizer import optimize_portfolio
from sentinel.order_generator import generate_entry_orders
from sentinel.perplexity_news import PerplexityNewsGatherer
import alpaca_trade_api as tradeapi


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging for morning workflow."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_filename = log_dir / f"morning_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

        # Production universe: S&P 500 + Nasdaq 100 (~600 stocks)
        from sentinel.universe import SP500_NASDAQ100_UNIVERSE, UNIVERSE_SIZE

        logger.info("  Loading universe...")
        positions = api.list_positions()
        portfolio_symbols = [p.symbol for p in positions]

        # Full universe = S&P 500 + Nasdaq 100 + currently held positions (for SELL analysis)
        universe = list(set(SP500_NASDAQ100_UNIVERSE + portfolio_symbols))
        logger.info(f"  Universe: {UNIVERSE_SIZE} base stocks + {len(portfolio_symbols)} held = {len(universe)} total")

        # Tier 1: Aggressive Technical Filter (600 → ~100)
        logger.info("  Running Tier 1 (Aggressive Technical Filter)...")
        tier1_candidates = run_tier1_filter(
            api=api,
            universe_symbols=universe,
            logger=logger
            # Uses default aggressive parameters from tier1_technical_filter.py
            # min_dollar_volume=$10M, min_price=$10, target_count=100
        )
        logger.info(f"  Tier 1 complete: {len(tier1_candidates)} candidates")

        if not tier1_candidates:
            logger.warning("  No candidates from Tier 1, skipping analysis")
            return {'success': True, 'signals': [], 'reason': 'no_tier1_candidates'}

        # Tier 2: Enrichment (add sector/news context, no filtering)
        logger.info("  Running Tier 2 (Context Enrichment)...")
        tier2_finalists = run_tier2_screening(
            api=api,
            tier1_candidates=tier1_candidates,
            market_context=market_context,  # Real-time market context
            logger=logger,
            target_count=len(tier1_candidates)  # Pass all through (enrichment only, no filtering)
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


def cleanup_zero_quantity_positions(engine, api, logger):
    """
    Cleanup: Liquidate zero or near-zero quantity positions (artifacts from previous version).

    Args:
        engine: OrderExecutionEngine instance
        api: Alpaca API instance
        logger: Logger instance

    Returns:
        Dict with cleanup results
    """
    logger.info("\n" + "=" * 70)
    logger.info("CLEANUP: Liquidating Zero-Quantity Positions")
    logger.info("=" * 70)

    try:
        positions = api.list_positions()
        zero_positions = []

        for pos in positions:
            qty = abs(float(pos.qty))
            if qty < 0.001:  # Less than 0.001 shares = essentially zero
                zero_positions.append(pos)
                logger.info(f"  Found zero position: {pos.symbol} ({qty} shares)")

        if not zero_positions:
            logger.info("  No zero-quantity positions found")
            return {'success': True, 'liquidated': 0}

        logger.info(f"  Liquidating {len(zero_positions)} zero-quantity positions...")
        liquidated = 0
        failed = 0

        for pos in zero_positions:
            symbol = pos.symbol
            qty = abs(float(pos.qty))

            try:
                result = engine.submit_conviction_sell(
                    symbol=symbol,
                    qty=qty,
                    conviction_score=0,
                    reasoning='Cleanup: Zero-quantity position from previous version'
                )

                if result['success']:
                    liquidated += 1
                    logger.info(f"    -> SUCCESS: Liquidated {symbol} ({qty} shares)")
                else:
                    failed += 1
                    logger.warning(f"    -> FAILED: {symbol} - {result.get('error', 'Unknown error')}")

            except Exception as e:
                failed += 1
                logger.error(f"    -> ERROR liquidating {symbol}: {e}")

        logger.info(f"  Cleanup complete: {liquidated} liquidated, {failed} failed")
        return {'success': True, 'liquidated': liquidated, 'failed': failed}

    except Exception as e:
        logger.error(f"Cleanup failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


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
            qty = abs(float(position.qty))  # Keep fractional shares

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
                # Calculate stop_loss_pct from entry and stop prices
                stop_loss_pct = stop_price / entry_price if entry_price > 0 else 0.92

                entry_order, stop_order = engine.submit_entry_with_stop(
                    symbol=symbol,
                    entry_price=entry_price,
                    qty=qty,
                    stop_loss_pct=stop_loss_pct
                )

                if entry_order and stop_order:
                    submitted += 1
                    logger.info(f"    -> SUCCESS: Entry {entry_order.id}, Stop {stop_order.id}")
                else:
                    failed += 1
                    logger.error(f"    -> FAILED: Orders returned None")

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
    logger.info("SENTINEL MORNING WORKFLOW")
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

        # Get conviction scores from Tier 3
        conviction_results = results['step_5'].get('conviction_results', [])

        logger.info(f"\nTier 3 returned {len(conviction_results)} conviction scores")

        # Cleanup: Liquidate zero-quantity positions (artifacts from previous version)
        results['cleanup'] = cleanup_zero_quantity_positions(engine, api, logger)

        # Get current portfolio state for optimizer
        account = api.get_account()
        positions = api.list_positions()
        current_positions = {p.symbol: p for p in positions}

        account_info = {
            'portfolio_value': float(account.portfolio_value),
            'cash': float(account.cash),
            'buying_power': float(account.buying_power)
        }

        # Step 5.5: Portfolio Optimization (NEW - makes holistic decisions with full information)
        logger.info("\n" + "=" * 70)
        logger.info("STEP 5.5: Portfolio Optimization (Holistic Decision Making)")
        logger.info("=" * 70)
        logger.info("NOTE: Portfolio optimizer now sees ALL conviction scores at once")
        logger.info("      and makes globally optimal rebalancing decisions.")

        optimization_result = optimize_portfolio(
            conviction_scores=conviction_results,
            current_positions=current_positions,
            account_info=account_info,
            logger=logger
        )

        if not optimization_result['success']:
            logger.error(f"Portfolio optimization failed: {optimization_result.get('error')}")
            logger.warning("Falling back to old sequential decision logic...")

            # Fallback: use old logic
            buy_signals = [r for r in conviction_results if r['decision'] == 'BUY']
            sell_signals = [r for r in conviction_results if r['decision'] == 'SELL']
        else:
            # Extract plan from optimizer
            plan = optimization_result['plan']

            # Convert plan to signals format for execution
            sell_signals = []
            for sell in plan.get('sells', []):
                # Find the conviction data
                conv_data = next((r for r in conviction_results if r['symbol'] == sell['symbol']), None)
                if conv_data and sell['symbol'] in current_positions:
                    sell_signals.append({
                        'symbol': sell['symbol'],
                        'conviction_score': sell.get('conviction', conv_data['conviction_score']),
                        'reasoning': sell.get('reason', 'Portfolio optimizer sell decision'),
                        'decision': 'SELL'
                    })

            # Convert buys - but we need to generate orders with the specified allocations
            buy_signals_from_plan = []
            for buy in plan.get('buys', []):
                conv_data = next((r for r in conviction_results if r['symbol'] == buy['symbol']), None)
                if conv_data:
                    buy_signals_from_plan.append({
                        'symbol': buy['symbol'],
                        'conviction_score': buy.get('conviction', conv_data['conviction_score']),
                        'reasoning': buy.get('reason', 'Portfolio optimizer buy decision'),
                        'allocation': buy['allocation'],  # Use optimizer's allocation
                        'latest_price': conv_data['latest_price'],
                        'decision': 'BUY'
                    })

            logger.info(f"\nPortfolio optimizer decisions:")
            logger.info(f"  SELL: {len(sell_signals)} positions")
            logger.info(f"  HOLD: {len(plan.get('holds', []))} positions")
            logger.info(f"  BUY: {len(buy_signals_from_plan)} positions")

        # Step 6A: Execute SELL signals (BEFORE buys to free up cash)
        results['step_6a'] = step_6a_execute_sell_signals(
            engine, logger, sell_signals, current_positions
        )

        # Step 6B: Submit new BUY entry orders from portfolio optimizer
        if optimization_result['success']:
            results['step_6b'] = step_6_submit_new_entries(engine, api, logger, buy_signals_from_plan)
        else:
            # Fallback: filter and execute old way
            filtered_buy_signals = [r for r in buy_signals if r['conviction_score'] >= 70]
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
