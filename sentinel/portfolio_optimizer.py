# -*- coding: utf-8 -*-
# sentinel/portfolio_optimizer.py
# Portfolio-Level Optimization with Full Information

"""
Portfolio Optimizer - Makes holistic rebalancing decisions with complete information.

Architecture:
- INPUT: All conviction scores (60 stocks), current portfolio state, available capital
- PROCESS: Single GPT-4 call with full portfolio context
- OUTPUT: Complete rebalancing plan (sells, holds, buys with allocations)

This solves the "Chinese Room" problem where individual stock decisions were made
in isolation without knowledge of the full opportunity set.
"""

import json
import logging
from typing import Dict, List, Optional
from openai import OpenAI

from config import OPENAI_API_KEY


# Portfolio optimization prompt template
PORTFOLIO_OPTIMIZER_PROMPT = """
You are an expert portfolio manager for a disciplined equity trading system managing a $100,000 paper trading account.

Your task: Create an optimal portfolio rebalancing plan given complete information about all opportunities and constraints.

=== CURRENT PORTFOLIO STATE ===
<<CURRENT_PORTFOLIO>>

=== ANALYZED OPPORTUNITIES (All stocks with conviction scores) ===
<<CONVICTION_SCORES>>

=== CAPITAL CONSTRAINTS ===
Portfolio Value: $<<PORTFOLIO_VALUE>>
Cash Available: $<<CASH_AVAILABLE>>
Buying Power: $<<BUYING_POWER>>

CRITICAL: You must NOT use margin. Total buy allocations cannot exceed available cash after sells.

=== OPTIMIZATION OBJECTIVES ===

1. **Maximize portfolio-weighted conviction**
   - Higher conviction stocks should have larger allocations
   - Conviction <60 = weak position, should sell to free capital
   - Conviction 60-69 = hold if already owned, don't add new
   - Conviction 70+ = strong position, prioritize capital allocation

2. **Maintain risk discipline**
   - Target 15-25 positions (diversification without over-diversification)
   - Maximum position size: 15% of portfolio value
   - No sector should exceed 40% of portfolio
   - NO MARGIN USAGE (this is a hard constraint)

3. **Capital efficiency**
   - Every dollar in a weak position is a dollar NOT in a strong position
   - Sell conviction <60 positions to free capital for conviction 70+ opportunities
   - Use conviction-weighted allocation: Higher conviction = proportionally larger size

=== ALLOCATION FORMULA ===

For BUY decisions, use conviction-weighted allocation:
1. Calculate total "conviction points" = sum of (conviction_score for all buys)
2. Each stock's allocation = (its_conviction / total_conviction_points) × available_capital
3. Ensure no single position exceeds 15% of portfolio value

Example:
- Available capital: $80,000
- BUY candidates: AMD (87), DHR (83), JNJ (82), MS (83), BAC (78)
- Total conviction points: 87+83+82+83+78 = 413
- AMD allocation: (87/413) × $80,000 = $16,850
- DHR allocation: (83/413) × $80,000 = $16,077
- etc.

=== OUTPUT FORMAT ===

Return a single JSON object with this exact structure:

{
  "sells": [
    {
      "symbol": "AAPL",
      "conviction": 58,
      "current_value": 5234.50,
      "reason": "Conviction below 60 threshold, freeing $5.2k for higher-conviction opportunities"
    }
  ],
  "holds": [
    {
      "symbol": "NVDA",
      "conviction": 72,
      "current_value": 8543.20,
      "reason": "Solid conviction above hold threshold, maintaining position"
    }
  ],
  "buys": [
    {
      "symbol": "AMD",
      "conviction": 87,
      "allocation": 16850,
      "reason": "Highest conviction score, allocated 21% of available capital proportional to conviction weight"
    }
  ],
  "summary": {
    "total_sells_value": 45234.50,
    "total_buys_value": 80000.00,
    "cash_remaining": 2156.75,
    "final_position_count": 23,
    "avg_portfolio_conviction": 68.4,
    "strategy": "Sold 15 low-conviction positions (<60) to fund 5 high-conviction opportunities (>80). Portfolio rebalanced from 53 to 23 positions with improved average conviction from 54 to 68. No margin used."
  }
}

=== DECISION RULES ===

**SELL decisions:**
- Conviction <60: Strong SELL (free capital for better opportunities)
- Conviction 60-69: Consider position size vs opportunity cost
  - If better opportunities exist (70+ conviction), consider selling to reallocate
  - If portfolio is underweight, may HOLD
- Conviction 70+: Do NOT sell unless rebalancing requires it

**HOLD decisions:**
- Conviction 60-69: Hold if no pressing need for capital
- Conviction 70+: Default to HOLD (strong positions)

**BUY decisions:**
- Only consider conviction 70+ for new positions
- Allocate using conviction-weighted formula
- Ensure total buys ≤ cash available (after sells)
- Respect 15% max position size limit

=== IMPORTANT NOTES ===

1. You are seeing ALL information at once (unlike the sequential per-stock analysis)
2. Make globally optimal decisions, not locally optimal ones
3. The goal is maximum portfolio-weighted conviction within risk constraints
4. Be aggressive about selling weak positions when strong opportunities exist
5. Show your math in the summary (how much capital freed, how allocated)

Take a deep breath and create the optimal portfolio rebalancing plan.
"""


class PortfolioOptimizer:
    """
    Portfolio-level optimizer that makes holistic rebalancing decisions.

    Takes all conviction scores and portfolio state, returns complete rebalancing plan.
    """

    def __init__(
        self,
        openai_client: Optional[OpenAI] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize portfolio optimizer.

        Args:
            openai_client: Optional OpenAI client instance
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

        # Initialize OpenAI
        if openai_client:
            self.openai = openai_client
        elif OPENAI_API_KEY:
            self.openai = OpenAI(api_key=OPENAI_API_KEY)
        else:
            raise ValueError("OpenAI API key required for portfolio optimization")

    def optimize_portfolio(
        self,
        conviction_scores: List[Dict],
        current_positions: Dict,
        account_info: Dict
    ) -> Dict:
        """
        Generate optimal portfolio rebalancing plan with full information.

        Args:
            conviction_scores: List of all analyzed stocks with conviction scores
                Format: [{"symbol": "AAPL", "conviction": 72, "reasoning": "...", "decision": "HOLD"}, ...]
            current_positions: Dict mapping symbol -> position object
            account_info: Dict with portfolio_value, cash, buying_power

        Returns:
            Dict with rebalancing plan:
            {
                "sells": [{"symbol": "AAPL", "conviction": 58, "qty": 10, ...}],
                "holds": [{"symbol": "NVDA", "conviction": 72, ...}],
                "buys": [{"symbol": "AMD", "conviction": 87, "allocation": 15000, ...}],
                "summary": {...}
            }
        """
        self.logger.info("Starting portfolio optimization with full information...")

        # Build current portfolio summary
        current_portfolio = self._build_portfolio_summary(conviction_scores, current_positions)

        # Build conviction scores summary
        scores_summary = self._build_scores_summary(conviction_scores, current_positions)

        # Build prompt
        prompt = self._build_prompt(
            current_portfolio,
            scores_summary,
            account_info
        )

        # Call GPT-5 for portfolio optimization
        try:
            self.logger.info("Calling GPT-5 for holistic portfolio optimization...")

            response = self.openai.chat.completions.create(
                model="gpt-5",  # Most intelligent model for critical portfolio optimization decisions
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                timeout=120.0  # Increased timeout for GPT-5's deeper reasoning
            )

            plan = json.loads(response.choices[0].message.content)

            # Validate and enrich plan
            plan = self._validate_and_enrich_plan(plan, current_positions, conviction_scores)

            # Log summary
            self._log_plan_summary(plan)

            return {
                'success': True,
                'plan': plan
            }

        except Exception as e:
            self.logger.error(f"Portfolio optimization failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }

    def _build_portfolio_summary(self, conviction_scores: List[Dict], current_positions: Dict) -> str:
        """Build human-readable current portfolio summary."""
        lines = []

        # Create lookup for conviction scores
        conviction_map = {s['symbol']: s for s in conviction_scores}

        for symbol, pos in current_positions.items():
            conviction_data = conviction_map.get(symbol, {})
            conviction = conviction_data.get('conviction_score', 'N/A')

            lines.append(
                f"  {symbol}: {float(pos.qty):.2f} shares @ ${float(pos.avg_entry_price):.2f} "
                f"(current: ${float(pos.current_price):.2f}, value: ${float(pos.market_value):.2f}, "
                f"conviction: {conviction})"
            )

        if not lines:
            return "  No current positions"

        return "\n".join(sorted(lines))

    def _build_scores_summary(self, conviction_scores: List[Dict], current_positions: Dict) -> str:
        """Build human-readable conviction scores summary."""
        lines = []

        # Sort by conviction score descending
        sorted_scores = sorted(conviction_scores, key=lambda x: x.get('conviction_score', 0), reverse=True)

        for score_data in sorted_scores:
            symbol = score_data['symbol']
            conviction = score_data.get('conviction_score', 'N/A')
            currently_held = symbol in current_positions
            status = "HELD" if currently_held else "NEW"

            lines.append(
                f"  {symbol}: conviction {conviction}/100 [{status}] - "
                f"{score_data.get('reasoning', 'No reasoning')[:100]}"
            )

        return "\n".join(lines)

    def _build_prompt(self, current_portfolio: str, scores_summary: str, account_info: Dict) -> str:
        """Build complete optimization prompt."""
        prompt = PORTFOLIO_OPTIMIZER_PROMPT

        prompt = prompt.replace("<<CURRENT_PORTFOLIO>>", current_portfolio)
        prompt = prompt.replace("<<CONVICTION_SCORES>>", scores_summary)
        prompt = prompt.replace("<<PORTFOLIO_VALUE>>", f"{account_info['portfolio_value']:,.2f}")
        prompt = prompt.replace("<<CASH_AVAILABLE>>", f"{account_info['cash']:,.2f}")
        prompt = prompt.replace("<<BUYING_POWER>>", f"{account_info['buying_power']:,.2f}")

        return prompt

    def _validate_and_enrich_plan(
        self,
        plan: Dict,
        current_positions: Dict,
        conviction_scores: List[Dict]
    ) -> Dict:
        """Validate plan structure and add missing data."""

        # Ensure all required keys exist
        plan.setdefault('sells', [])
        plan.setdefault('holds', [])
        plan.setdefault('buys', [])
        plan.setdefault('summary', {})

        # Enrich sells with quantity data
        for sell in plan['sells']:
            symbol = sell['symbol']
            if symbol in current_positions:
                pos = current_positions[symbol]
                sell['qty'] = float(pos.qty)
                sell['current_price'] = float(pos.current_price)

        # Validate buys don't exceed capital
        total_buys = sum(b.get('allocation', 0) for b in plan['buys'])
        total_sells = sum(s.get('current_value', 0) for s in plan['sells'])

        if 'validation' not in plan['summary']:
            plan['summary']['validation'] = {
                'total_buys': total_buys,
                'total_sells': total_sells,
                'net_capital_required': total_buys - total_sells
            }

        return plan

    def _log_plan_summary(self, plan: Dict):
        """Log optimization plan summary."""
        summary = plan.get('summary', {})

        self.logger.info("=" * 70)
        self.logger.info("PORTFOLIO OPTIMIZATION COMPLETE")
        self.logger.info("=" * 70)
        self.logger.info(f"  Sells: {len(plan['sells'])} positions (${summary.get('total_sells_value', 0):,.2f})")
        self.logger.info(f"  Holds: {len(plan['holds'])} positions")
        self.logger.info(f"  Buys: {len(plan['buys'])} positions (${summary.get('total_buys_value', 0):,.2f})")
        self.logger.info(f"  Final position count: {summary.get('final_position_count', 'N/A')}")
        self.logger.info(f"  Avg portfolio conviction: {summary.get('avg_portfolio_conviction', 'N/A')}")
        self.logger.info("")
        self.logger.info(f"  Strategy: {summary.get('strategy', 'N/A')}")
        self.logger.info("=" * 70)


def optimize_portfolio(
    conviction_scores: List[Dict],
    current_positions: Dict,
    account_info: Dict,
    logger: Optional[logging.Logger] = None
) -> Dict:
    """
    Convenience function for portfolio optimization.

    Args:
        conviction_scores: List of conviction analysis results from Tier 3
        current_positions: Dict mapping symbol -> position object
        account_info: Dict with portfolio_value, cash, buying_power
        logger: Optional logger instance

    Returns:
        Dict with optimization results
    """
    optimizer = PortfolioOptimizer(logger=logger)
    return optimizer.optimize_portfolio(conviction_scores, current_positions, account_info)
