# -*- coding: utf-8 -*-
# sentinel/order_generator.py
# Convert BUY signals into entry+stop order pairs for v8 execution engine

"""
Order Generator

Converts conviction analysis results (BUY signals) into executable order pairs
(entry + stop) for the v8 execution engine.

Key features:
- Conviction-weighted capital allocation
- 90% invested rule
- 10% max position size
- Risk limits from risk_config.py
- Generates entry+stop pairs (not OCO brackets)
"""

import logging
from typing import List, Dict, Optional, Tuple
import math

import alpaca_trade_api as tradeapi

try:
    from sentinel.risk_config import (
        INITIAL_STOP_LOSS_PCT,
        MAX_POSITION_SIZE_PCT,
        TARGET_INVESTED_RATIO,
        MIN_TRADE_DOLLAR_THRESHOLD,
        calculate_stop_price,
        calculate_position_size,
        validate_order_pair
    )
except ImportError:
    # Fallback defaults
    INITIAL_STOP_LOSS_PCT = 0.08
    MAX_POSITION_SIZE_PCT = 0.10
    TARGET_INVESTED_RATIO = 0.90
    MIN_TRADE_DOLLAR_THRESHOLD = 25.0

    def calculate_stop_price(entry_price: float) -> float:
        return round(entry_price * (1 - INITIAL_STOP_LOSS_PCT), 2)

    def calculate_position_size(portfolio_value: float, conviction_weight: float) -> float:
        return portfolio_value * MAX_POSITION_SIZE_PCT * conviction_weight

    def validate_order_pair(entry_price: float, stop_price: float, qty: int) -> Tuple[bool, str]:
        if entry_price <= 0 or qty <= 0:
            return False, "Invalid entry price or quantity"
        if stop_price >= entry_price:
            return False, "Stop price must be below entry price"
        return True, "Valid"


# Conviction weighting parameters
CONVICTION_WEIGHT_EXP = 1.6
MIN_WEIGHT_FLOOR = 0.05


class OrderGenerator:
    """Generate entry+stop order pairs from conviction analysis."""

    def __init__(
        self,
        api: tradeapi.REST,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize order generator.

        Args:
            api: Alpaca REST API instance
            logger: Optional logger instance
        """
        self.api = api
        self.logger = logger or logging.getLogger(__name__)

    def generate_orders(
        self,
        conviction_results: List[Dict],
        portfolio_value: float,
        current_positions: Optional[Dict] = None
    ) -> Dict:
        """
        Generate entry+stop order pairs from conviction analysis.

        Args:
            conviction_results: List of conviction analysis results
            portfolio_value: Current portfolio value
            current_positions: Optional dict of current positions (symbol -> position)

        Returns:
            Dict with:
            - 'orders': List of order pairs {symbol, side, qty, entry_price, stop_price}
            - 'allocation_summary': Dict with allocation details
            - 'notes': List of allocation notes/warnings
        """
        self.logger.info(f"Generating orders from {len(conviction_results)} conviction results...")

        current_positions = current_positions or {}

        # Filter BUY signals only
        buy_signals = [r for r in conviction_results if r['decision'] == 'BUY']

        self.logger.info(f"Found {len(buy_signals)} BUY signals")

        if not buy_signals:
            return {
                'orders': [],
                'allocation_summary': {
                    'total_capital': portfolio_value,
                    'investable_capital': portfolio_value * TARGET_INVESTED_RATIO,
                    'allocated': 0.0,
                    'cash_remaining': portfolio_value * TARGET_INVESTED_RATIO
                },
                'notes': ['No BUY signals generated']
            }

        # Calculate allocations using conviction weighting
        allocations, notes = self._calculate_allocations(
            buy_signals,
            portfolio_value,
            current_positions
        )

        # Generate order pairs
        orders = []
        total_allocated = 0.0

        for signal in buy_signals:
            symbol = signal['symbol']
            allocation = allocations.get(symbol, 0.0)

            if allocation < MIN_TRADE_DOLLAR_THRESHOLD:
                notes.append(f"{symbol}: Allocation ${allocation:.2f} below minimum threshold")
                continue

            # Calculate order details
            entry_price = signal['latest_price']
            stop_price = calculate_stop_price(entry_price)
            qty = int(allocation / entry_price)

            if qty <= 0:
                notes.append(f"{symbol}: Calculated qty is 0, skipping")
                continue

            # Validate order pair
            is_valid, validation_msg = validate_order_pair(entry_price, stop_price, qty)
            if not is_valid:
                notes.append(f"{symbol}: Validation failed - {validation_msg}")
                continue

            # Calculate actual allocation (after rounding qty)
            actual_allocation = qty * entry_price
            total_allocated += actual_allocation

            orders.append({
                'symbol': symbol,
                'side': 'buy',
                'qty': qty,
                'entry_price': entry_price,
                'stop_price': stop_price,
                'conviction_score': signal['conviction_score'],
                'allocation': actual_allocation,
                'rationale': signal['rationale']
            })

            self.logger.info(
                f"  {symbol}: {qty} shares @ ${entry_price:.2f}, "
                f"stop @ ${stop_price:.2f} (${actual_allocation:.2f})"
            )

        # Build allocation summary
        investable_capital = portfolio_value * TARGET_INVESTED_RATIO
        allocation_summary = {
            'total_capital': portfolio_value,
            'investable_capital': investable_capital,
            'allocated': total_allocated,
            'cash_remaining': investable_capital - total_allocated,
            'allocation_pct': (total_allocated / portfolio_value * 100) if portfolio_value > 0 else 0
        }

        self.logger.info(
            f"Order generation complete: {len(orders)} orders, "
            f"${total_allocated:.2f} allocated ({allocation_summary['allocation_pct']:.1f}%)"
        )

        return {
            'orders': orders,
            'allocation_summary': allocation_summary,
            'notes': notes
        }

    def _calculate_allocations(
        self,
        buy_signals: List[Dict],
        portfolio_value: float,
        current_positions: Dict
    ) -> Tuple[Dict[str, float], List[str]]:
        """
        Calculate dollar allocations for each BUY signal using conviction weighting.

        Args:
            buy_signals: List of BUY conviction results
            portfolio_value: Total portfolio value
            current_positions: Dict of current positions

        Returns:
            Tuple of (allocations dict, notes list)
        """
        investable_capital = portfolio_value * TARGET_INVESTED_RATIO
        max_position_value = portfolio_value * MAX_POSITION_SIZE_PCT
        notes = []

        # Calculate conviction weights
        weights = {}
        for signal in buy_signals:
            symbol = signal['symbol']
            conviction = signal['conviction_score']
            weight = self._conviction_to_weight(conviction)
            weights[symbol] = weight

        total_weight = sum(weights.values())

        if total_weight == 0:
            # Fallback to equal weighting
            for symbol in weights:
                weights[symbol] = 1.0
            total_weight = len(weights)
            notes.append("Conviction scores resulted in zero weight; using equal weighting")

        # Calculate raw allocations
        allocations = {}
        for signal in buy_signals:
            symbol = signal['symbol']

            # Base allocation from conviction weight
            raw_allocation = investable_capital * (weights[symbol] / total_weight)

            # Cap at max position size
            allocation = min(raw_allocation, max_position_value)

            allocations[symbol] = allocation

            if raw_allocation > max_position_value:
                notes.append(
                    f"{symbol}: Allocation capped at ${max_position_value:.2f} "
                    f"(would have been ${raw_allocation:.2f})"
                )

        # Redistribute overflow from capped positions
        overflow = sum(
            investable_capital * (weights[s] / total_weight) - allocations[s]
            for s in allocations
            if investable_capital * (weights[s] / total_weight) > allocations[s]
        )

        if overflow > 1.0:
            # Find positions with room to grow
            uncapped = [
                s for s in allocations
                if allocations[s] < max_position_value - 1.0
            ]

            if uncapped:
                # Redistribute overflow proportionally
                uncapped_weight = sum(weights[s] for s in uncapped)
                if uncapped_weight > 0:
                    for symbol in uncapped:
                        additional = overflow * (weights[symbol] / uncapped_weight)
                        new_allocation = min(allocations[symbol] + additional, max_position_value)
                        allocations[symbol] = new_allocation
                    notes.append(f"Redistributed ${overflow:.2f} overflow to uncapped positions")
            else:
                notes.append(
                    f"${overflow:.2f} could not be allocated (all positions at max cap)"
                )

        return allocations, notes

    def _conviction_to_weight(self, conviction: int) -> float:
        """
        Convert conviction score (1-10) to allocation weight.

        Uses exponential weighting to give higher conviction scores
        disproportionately more weight.

        Args:
            conviction: Conviction score (1-10)

        Returns:
            Weight (0.0-1.0)
        """
        normalized = max(1, min(10, conviction)) / 10.0
        weight = normalized ** CONVICTION_WEIGHT_EXP
        return max(MIN_WEIGHT_FLOOR, weight)


# Convenience function for use in evening workflow
def generate_entry_orders(
    api: tradeapi.REST,
    conviction_results: List[Dict],
    portfolio_value: float,
    current_positions: Optional[Dict] = None,
    logger: Optional[logging.Logger] = None
) -> Dict:
    """
    Generate entry+stop order pairs from conviction analysis.

    Args:
        api: Alpaca REST API instance
        conviction_results: List of conviction analysis results
        portfolio_value: Current portfolio value
        current_positions: Optional dict of current positions
        logger: Optional logger

    Returns:
        Dict with orders, allocation_summary, and notes
    """
    generator = OrderGenerator(api, logger)
    return generator.generate_orders(conviction_results, portfolio_value, current_positions)
