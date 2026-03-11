"""
GPT-5 Portfolio Optimizer - The Brain
======================================
Uses GPT-5 to make intelligent capital allocation decisions based on:
- Research scores (technical, fundamental, sentiment)
- Risk metrics (stop-loss, risk/reward, portfolio heat)
- Market conditions
- Available capital

This is where the REAL intelligence happens - not just deterministic formulas.
"""

import openai
import json
import logging
from typing import List, Dict, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class GPT5PortfolioOptimizer:
    """
    Use GPT-5 (OpenAI) as Chief Investment Officer

    Responsibilities:
    1. Review all candidate data comprehensively
    2. Decide which stocks to buy and how much capital to allocate
    3. Weight allocations by conviction (higher scores = more capital)
    4. Ensure total deployment = 90-100% of available capital
    5. Provide written reasoning for each decision
    """

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize portfolio optimizer

        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o for cost efficiency)
                   Options: gpt-4o ($2-3/run), gpt-4o-mini ($0.50/run), gpt-5 ($10-20/run)
        """
        self.client = openai.OpenAI(api_key=api_key, timeout=600.0)  # 10 minute timeout
        self.model = model
        logger.info(f"Portfolio Optimizer initialized (model: {self.model})")

    def optimize_portfolio(
        self,
        candidates: List[Dict],
        available_capital: float,
        market_conditions: Dict,
        current_positions: int = 0,
        max_positions: int = 20,
        holdings: List[Dict] = None
    ) -> Tuple[List[Dict], str]:
        """
        Use GPT-5 to create optimized portfolio allocation

        Args:
            candidates: List of BUY candidates from Research
            available_capital: Total capital available to deploy
            market_conditions: Current market state
            current_positions: Number of existing positions
            max_positions: Maximum allowed positions
            holdings: Current portfolio holdings (for SELL decisions)

        Returns:
            (optimized_candidates, reasoning)
            - optimized_candidates: List with 'allocated_capital' field added
            - reasoning: GPT-5's written analysis and justification
        """
        if holdings is None:
            holdings = []

        logger.info("=" * 80)
        logger.info("GPT-5 PORTFOLIO OPTIMIZATION")
        logger.info("=" * 80)
        logger.info(f"Reviewing {len(candidates)} candidates and {len(holdings)} holdings")
        logger.info(f"Available capital: ${available_capital:,.0f}")
        logger.info(f"Current positions: {current_positions}/{max_positions}")

        # SAFEGUARD: Limit total stocks to prevent prompt from being too long
        # GPT-5 struggles with 50+ stocks. Limit to top 40 candidates + all holdings
        # Need 40 to give optimizer enough options to select 15-20 positions
        MAX_CANDIDATES = 40
        if len(candidates) > MAX_CANDIDATES:
            logger.warning(f"Truncating {len(candidates)} candidates to top {MAX_CANDIDATES} to prevent prompt overflow")
            # Sort by composite score and take top N
            sorted_candidates = sorted(
                candidates,
                key=lambda x: x.get('composite_score', x.get('research_composite_score', 0)),
                reverse=True
            )
            candidates = sorted_candidates[:MAX_CANDIDATES]
            logger.info(f"Using top {len(candidates)} candidates (scores {candidates[0].get('composite_score', 0):.1f} to {candidates[-1].get('composite_score', 0):.1f})")

        # Build comprehensive prompt for GPT-5
        prompt = self._build_optimization_prompt(
            candidates=candidates,
            available_capital=available_capital,
            market_conditions=market_conditions,
            current_positions=current_positions,
            max_positions=max_positions,
            holdings=holdings
        )

        # Call GPT-5
        logger.info("Consulting OpenAI GPT-5 for allocation decisions...")

        try:
            # Adjust token limit based on model
            max_tokens = 16000 if self.model == "gpt-5" else 4096

            response = self.client.chat.completions.create(
                model=self.model,
                max_completion_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse GPT-5's response
            response_text = response.choices[0].message.content
            logger.info("GPT-5 analysis received")

            # Log the actual response for debugging
            if response_text:
                logger.info(f"GPT-5 response length: {len(response_text)} characters")
                logger.debug(f"GPT-5 response preview: {response_text[:500]}...")
            else:
                logger.error("GPT-5 returned empty response!")
                logger.error(f"Full response object: {response}")
                logger.error(f"Response choices: {response.choices if hasattr(response, 'choices') else 'No choices'}")
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    logger.error(f"First choice: {response.choices[0]}")
                    logger.error(f"Message content: {response.choices[0].message.content if hasattr(response.choices[0], 'message') else 'No message'}")
                raise ValueError("GPT-5 returned empty response")

            # Extract JSON allocation from response
            allocations, reasoning = self._parse_gpt5_response(response_text)

            # Apply allocations to candidates and extract SELL decisions
            optimized_candidates, sell_decisions = self._apply_allocations(candidates, holdings, allocations)

            # Log summary
            total_allocated = sum(c['allocated_capital'] for c in optimized_candidates)
            deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0

            logger.info(f"GPT-5 allocated ${total_allocated:,.0f} ({deployment_pct:.1f}% of available)")
            logger.info(f"Selected {len(optimized_candidates)} BUY positions and {len(sell_decisions)} SELL positions")

            # Store sell decisions in the result so Operations Manager can process them
            for candidate in optimized_candidates:
                candidate['gpt5_sell_decisions'] = sell_decisions

            return optimized_candidates, reasoning

        except Exception as e:
            logger.error(f"GPT-5 optimization failed: {e}", exc_info=True)
            # Fallback: select top 10 by score and allocate equally
            logger.warning("Falling back to top-10 selection with equal weighting")
            fallback_candidates, fallback_sells = self._fallback_allocation(candidates, available_capital, holdings)

            # Store sell decisions in fallback results
            for candidate in fallback_candidates:
                candidate['gpt5_sell_decisions'] = fallback_sells

            return fallback_candidates, f"GPT-5 unavailable - selected top {len(fallback_candidates)} by composite score with equal weighting"

    def _build_optimization_prompt(
        self,
        candidates: List[Dict],
        available_capital: float,
        market_conditions: Dict,
        current_positions: int,
        max_positions: int,
        holdings: List[Dict] = None
    ) -> str:
        """Build comprehensive prompt for GPT-5"""
        if holdings is None:
            holdings = []

        # Format market conditions
        market_summary = f"""
MARKET CONDITIONS:
- SPY: {market_conditions.get('spy_change_pct', 0):.2f}%
- VIX: {market_conditions.get('vix_level', 0):.1f} ({market_conditions.get('vix_status', 'UNKNOWN')})
- Market Sentiment: {market_conditions.get('market_sentiment', 'NEUTRAL')}
"""

        # Format candidates - SIMPLIFIED (no redundant news summaries)
        candidates_data = []
        for i, c in enumerate(candidates, 1):
            # Get sentiment score only (summary is redundant)
            sentiment_info = c.get('sentiment', {})
            if isinstance(sentiment_info, dict):
                sentiment_score = sentiment_info.get('score', 50.0)
            else:
                sentiment_score = c.get('sentiment_score', 50.0)

            candidates_data.append(f"""
CANDIDATE #{i}: {c['ticker']} ({c.get('sector', 'Unknown')}) @ ${c.get('current_price', c.get('entry_price', 0)):.2f}
  Composite: {c.get('composite_score', c.get('research_composite_score', 0)):.1f}/100 | Tech: {c.get('technical_score', c.get('technical', {}).get('score', 0)):.1f} | Fund: {c.get('fundamental_score', c.get('fundamental', {}).get('score', 0)):.1f} | Sentiment: {sentiment_score:.1f}
""")

        candidates_text = "\n".join(candidates_data)

        # Calculate position limits based on current holdings
        hard_constraint_max = 30  # From compliance config
        available_slots = hard_constraint_max - current_positions

        # Determine target new positions based on scenario
        if available_slots <= 0:
            # Portfolio is at or over limit - need to trim down
            # We need to sell at least abs(available_slots) MORE than we buy
            # Strategy: Sell the mandatory + extra to get under limit
            # Then we can buy SOME positions with the freed capital, but net is negative
            # Example: 33 positions, need to get to 30 = sell 3 more than we buy
            # If we have $23K capital and sell 5, buy 2: 33 - 5 + 2 = 30 ✓
            # So target buys = at least 1-2 to deploy the capital, but keep net reduction
            target_new_positions = max(1, abs(available_slots))  # At least 1 to deploy capital
        elif available_slots < 10:
            # Close to limit - add what we can, but aim for good capital deployment
            target_new_positions = min(available_slots, 8)
        else:
            # Plenty of room - aim for good diversification (12-15 positions)
            target_new_positions = min(available_slots, 15)

        prompt = f"""You are the Chief Investment Officer for Sentinel Corporation, an expert hedge fund manager specializing in SWING TRADING.

===== COMPANY PHILOSOPHY & TRADING STRATEGY =====

Your firm practices swing trading with these core principles:
- HOLDING PERIOD: 1 to 5 days per trade (not day trading, not long-term investing)
- RISK MANAGEMENT: Every position has bracket orders with WIDE stops to give "room to run"
  * Stop-loss: 8% below entry (volatile stocks need breathing room)
  * Take-profit: 16% above entry (capture meaningful swing moves, not noise)
  * Philosophy: Fewer, larger wins rather than many small stops
- CAPITAL EFFICIENCY: Deploy 90-100% of available capital (NOT NEGOTIABLE - use the capital!)
- DIVERSIFICATION: Spread risk across multiple positions to smooth equity curve
- SECTOR DIVERSIFICATION: Don't over-concentrate in any single sector (max 30%)
- SCORE-DRIVEN: Trust the technical, fundamental, and sentiment analysis
- ADAPTIVE: Sell underperformers (< 55 score), buy better opportunities
- VOLATILITY IS GOOD: We WANT volatile stocks - that's what creates swing opportunities
- BE AGGRESSIVE: This is a GROWTH portfolio, not capital preservation. Deploy capital!

===== YOUR ROLE IN THE WORKFLOW =====

1. You analyze all available stocks and create a PROPOSED TRADING PLAN
2. Your plan goes to the CEO for executive review
3. Together with Compliance, you refine the plan to meet Alpaca's rules
4. Once finalized, CEO presents to the User for Y/N approval
5. If approved, Trading Department executes in proper sequence:
   - SELLs first (close underperforming positions)
   - Wait for settlement
   - BUYs with bracket orders (8% stop-loss, 16% take-profit)

===== CURRENT MARKET CONDITIONS =====
{market_summary}

===== CRITICAL: UNDERSTAND YOUR CONSTRAINTS =====

This is an EXISTING PORTFOLIO with positions already held. You are ADDING new capital to it.

**AVAILABLE CAPITAL TO DEPLOY**: ${available_capital:,.2f}
  - This includes: Buying power + proceeds from mandatory sells
  - This is ALL the cash you have - DO NOT exceed this amount!

**CURRENT PORTFOLIO STATE**:
  - Current holdings: {current_positions} positions
  - Hard position limit: {hard_constraint_max} positions maximum (compliance rule)
  - Positions available: {available_slots} slots remaining{"" if available_slots > 0 else f" (OVER LIMIT by {abs(available_slots)} - must sell to get under {hard_constraint_max})"}

**POSITION COUNT MATH** (CRITICAL):
  - Formula: Final positions = {current_positions} (current) - SELLs + BUYs
  - HARD LIMIT: Final positions MUST be ≤ {hard_constraint_max}
  - Current status: {"Portfolio OVER LIMIT - MUST net reduce position count" if available_slots < 0 else f"Can add up to {available_slots} net new positions"}

  {"**IMMEDIATE ACTION REQUIRED**: You MUST sell at least " + str(abs(available_slots)) + " positions to get under the limit!" if available_slots < 0 else ""}

  - Example calculation:
    * If you sell {2 if available_slots >= 0 else abs(available_slots) + 2} and buy {target_new_positions}: Final = {current_positions} - {2 if available_slots >= 0 else abs(available_slots) + 2} + {target_new_positions} = {current_positions - (2 if available_slots >= 0 else abs(available_slots) + 2) + target_new_positions}
    * This {"VIOLATES" if current_positions - (2 if available_slots >= 0 else abs(available_slots) + 2) + target_new_positions > hard_constraint_max else "SATISFIES"} the ≤ {hard_constraint_max} constraint

===== CURRENT HOLDINGS =====
{self._format_holdings(holdings) if holdings else "No current holdings - fresh portfolio"}

===== NEW BUY CANDIDATES =====

You have {len(candidates)} stocks to consider, each with:
- Technical Score (0-100): RSI, MACD, trend analysis
- Fundamental Score (0-100): Profitability, valuation, growth, financial health
- Sentiment Score (0-100): News sentiment from last 24 hours
- Composite Score: Weighted combination of all three

{candidates_text}

===== YOUR TASK =====

**IMPORTANT CONTEXT**: Our system has already performed COMPARATIVE RANKING of all stocks.
- All holdings + candidates were ranked together by composite score
- Portfolio goal: Hold the top 28 stocks by score (max 30 allowed)
- Holdings ranked below #28 have been automatically flagged for MANDATORY SELL
- Candidates ranked in top 28 are prioritized for BUY

Your job is to allocate capital optimally among the top-ranked buy opportunities.

Create a PROPOSED TRADING PLAN by deciding:

1. **SELLS (Pre-Identified)**
   - Holdings flagged as MANDATORY_SELL have already been identified by ranking system
   - These will be AUTOMATICALLY sold - you don't need to justify them
   - Your only decision: Should you recommend any ADDITIONAL sells? (rare - only if you see major red flags)
   - Criteria for additional sells:
     * Score < 55 (absolute minimum threshold)
     * Severe negative catalyst not reflected in scoring
     * Sector over-concentration requiring rebalancing

2. **BUYS (Your Primary Focus)**
   - Select from top-ranked candidates (those in top 28 by composite score)
   - Prioritize: High scores (65+/100 preferred, minimum 55/100)
   - Consider: Technical + fundamental + sentiment alignment
   - Diversify: No more than 30% in any single sector
   - Risk/reward: Appropriate volatility for swing trading

3. **CAPITAL ALLOCATION (Critical Task)**
   - **MANDATORY**: Deploy 90-100% of available capital (${available_capital:,.2f})
   - **TARGET**: Select {target_new_positions} new positions (adjust based on slots available)
   - **HARD LIMITS**:
     * Total capital deployed MUST be ≤ ${available_capital:,.2f}
     * Final position count MUST be ≤ {hard_constraint_max}
     * No single position > 10% of available capital
   - **Sizing Strategy**: Bigger allocations to higher-conviction (higher-scoring) opportunities

===== ALLOCATION GUIDELINES =====

**YOUR CAPITAL TO DEPLOY**: ${available_capital:,.2f}
  - Minimum deployment: ${available_capital * 0.90:,.2f} (90%)
  - Maximum deployment: ${available_capital:,.2f} (100%)
  - DO NOT EXCEED THIS AMOUNT - you will be auto-scaled down if you do!

**POSITION SIZING** (based on your actual capital):
  - Target {target_new_positions} positions{f" = ~${available_capital / target_new_positions:,.2f} per position" if target_new_positions > 0 else " (TRIM MODE - portfolio over limit)"}
  - Higher conviction (composite 75+): ${available_capital * 0.08:,.2f} to ${available_capital * 0.10:,.2f} (8-10%)
  - Moderate conviction (composite 65-74): ${available_capital * 0.06:,.2f} to ${available_capital * 0.08:,.2f} (6-8%)
  - Lower conviction (composite 55-64): ${available_capital * 0.04:,.2f} to ${available_capital * 0.06:,.2f} (4-6%)

**EXAMPLE ALLOCATION** (using YOUR actual capital of ${available_capital:,.2f}):
  {"- Portfolio is OVER LIMIT - you must sell MORE than you buy to trim position count" if target_new_positions == 0 else f'''- If selecting {target_new_positions} positions with mixed conviction:
  - 3 high-conviction @ 8% each = ${available_capital * 0.24:,.2f}
  - 6 moderate @ 6% each = ${available_capital * 0.36:,.2f}
  - 3 lower @ 5% each = ${available_capital * 0.15:,.2f}
  - Total: ${available_capital * 0.75:,.2f} (75% deployed - needs more to hit 90%!)
  - **Better**: Add 3-5 more positions to reach 90-100% deployment'''}

**POSITION COUNT CONSTRAINT**:
  - Current holdings: {current_positions}
  - If you sell X positions and buy Y positions: Final = {current_positions} - X + Y
  - Final MUST be ≤ {hard_constraint_max}
  - Therefore: Y - X ≤ {hard_constraint_max - current_positions} (net adds limited)

===== OUTPUT FORMAT =====

Provide your strategic analysis (2-3 paragraphs), then output a JSON object with BOTH your BUY and SELL decisions:

```json
{{
  "sells": [
    {{
      "ticker": "XYZ",
      "sell_pct": 100,
      "reasoning": "Composite score dropped to 45. Sentiment turned negative. Better opportunities available."
    }}
  ],
  "buys": [
    {{
      "ticker": "AAPL",
      "allocated_capital": 15000.00,
      "allocation_pct": 15.0,
      "is_position_adjustment": false,
      "reasoning": "Strong balanced scores (Tech:85, Fund:78, Sent:72). Uptrend with MACD bullish. Tech sector diversification."
    }}
  ],
  "total_allocated": 95000.00,
  "deployment_pct": 95.0,
  "portfolio_reasoning": "Closing 2 underperformers, adding 3 new positions. Emphasis on tech/fundamental strength given stable market conditions (VIX {market_conditions.get('vix_level', 20):.1f}). Holding period: 2-4 days target."
}}
```

**CRITICAL NOTES**:
- "sells": Usually empty - mandatory sells are handled automatically by ranking system
  * Only add to "sells" if you see major red flags NOT captured by scoring (rare)
  * Examples: Breaking news scandal, sudden liquidity crisis, sector over-concentration
- "buys": List tickers you want to BUY (new positions only - cannot add to existing holdings)
  * Focus on top-ranked candidates (shown in ranking analysis above)
  * Prioritize candidates with rank ≤ 28 (these are replacing weaker holdings)
- "is_position_adjustment": Always set to false (we don't add to existing positions)

Think like an expert portfolio manager with a RANKING MINDSET:
1. **Understand the ranking**: Holdings ranked > 28 are being sold automatically
2. **Focus on top candidates**: Look for candidates ranked in top 28 (these earned their spot)
3. **Allocate intelligently**:
   - Select {target_new_positions} positions to fill the open slots
   - Match allocation to conviction: Higher scores = Bigger allocations
   - But never >10% in a single position
4. **Verify capital deployment**:
   - Total allocated MUST be ${available_capital * 0.90:,.2f} to ${available_capital:,.2f}
   - If sum < 90%, add more positions or increase allocations!
5. **Verify position count**:
   - Current: {current_positions} positions
   - After sells: {current_positions} - (number of sells)
   - After buys: (result) + (number of buys)
   - Final MUST be ≤ {hard_constraint_max}
6. **Sector diversification**: No sector > 30% of portfolio

**CRITICAL REMINDERS**:
- Available capital: ${available_capital:,.2f} (NOT $100K!)
- MUST deploy: ${available_capital * 0.90:,.2f} to ${available_capital:,.2f} (90-100%)
- CANNOT exceed: ${available_capital:,.2f} total allocation
- Final position count: MUST be ≤ {hard_constraint_max} (current: {current_positions})
- Trust the ranking: Candidates in top 28 have earned their spot via scoring

Begin your analysis:"""

        return prompt

    def _format_holdings(self, holdings: List[Dict]) -> str:
        """Format current holdings for GPT-5 prompt"""
        if not holdings:
            return "No current holdings"

        holdings_text = []
        for i, h in enumerate(holdings, 1):
            holdings_text.append(f"""
HOLDING #{i}: {h.get('ticker', 'UNKNOWN')}
  Position Info:
    - Quantity: {h.get('quantity', 0):.4f} shares
    - Current Price: ${h.get('current_price', 0):.2f}
    - Market Value: ${h.get('market_value', 0):.2f}
    - Cost Basis: ${h.get('cost_basis', 0):.2f}
    - Unrealized P&L: ${h.get('unrealized_pl', 0):.2f} ({h.get('unrealized_plpc', 0):.2f}%)

  Current Scores (if available):
    - Composite: {h.get('composite_score', 'N/A')}/100
    - Technical: {h.get('technical_score', 'N/A')}/100
    - Fundamental: {h.get('fundamental_score', 'N/A')}/100
    - Sentiment: {h.get('sentiment_score', 'N/A')}/100

  **Decision Required**: HOLD (keep position) or SELL (close position)?
  - If scores are still strong (composite 65+), consider HOLD
  - If scores have deteriorated (composite <55), consider SELL
  - If better opportunities exist in candidates, consider SELL to free capital
""")

        return "\n".join(holdings_text)

    def _parse_gpt5_response(self, response_text: str) -> Tuple[Dict, str]:
        """
        Parse GPT-5's response to extract allocations and reasoning

        Returns:
            (allocations_dict, reasoning_text)
        """
        # Extract JSON from response (it should be in a code block)
        try:
            json_start = response_text.find('```json')
            if json_start == -1:
                json_start = response_text.find('{')
            else:
                json_start += 7

            json_end = response_text.find('```', json_start)
            if json_end == -1:
                json_end = len(response_text)

            json_str = response_text[json_start:json_end].strip()

            allocations = json.loads(json_str)

            # Reasoning is everything before the JSON
            reasoning = response_text[:json_start].strip()
            if reasoning.endswith('```json'):
                reasoning = reasoning[:-7].strip()

            return allocations, reasoning

        except Exception as e:
            logger.error(f"Failed to parse GPT-5 response: {e}")
            logger.error(f"Response text (first 1000 chars): {response_text[:1000]}")
            logger.error(f"Response text (last 500 chars): {response_text[-500:]}")
            logger.error(f"Full response length: {len(response_text)}")
            raise ValueError(f"Could not parse GPT-5 allocation response: {e}")

    def _apply_allocations(self, candidates: List[Dict], holdings: List[Dict], allocations: Dict) -> Tuple[List[Dict], List[Dict]]:
        """
        Apply GPT-5's allocations to candidate list and extract SELL decisions

        Args:
            candidates: List of BUY candidates from Research
            holdings: Current holdings
            allocations: GPT-5's allocation decisions (with 'buys' and 'sells' arrays)

        Returns:
            (optimized_candidates, sell_decisions)
            - optimized_candidates: List of selected candidates with 'allocated_capital' field
            - sell_decisions: List of SELL decisions from GPT-5
        """
        # Handle both old format (selected_tickers) and new format (buys/sells)
        if 'buys' in allocations:
            # New format with explicit BUY/SELL decisions
            buy_items = allocations.get('buys', [])
            sell_items = allocations.get('sells', [])
        else:
            # Old format - backwards compatibility
            buy_items = allocations.get('selected_tickers', [])
            sell_items = []

        # Process BUY decisions
        selected_tickers = {
            item['ticker']: item
            for item in buy_items
        }

        optimized = []
        for candidate in candidates:
            ticker = candidate['ticker']
            if ticker in selected_tickers:
                buy_item = selected_tickers[ticker]
                # Add GPT-5's allocation
                candidate['allocated_capital'] = buy_item.get('allocated_capital', 0)
                candidate['gpt5_reasoning'] = buy_item.get('reasoning', "Selected by GPT-5")
                candidate['is_position_adjustment'] = buy_item.get('is_position_adjustment', False)
                optimized.append(candidate)

        # Process SELL decisions (convert to format that Operations Manager can use)
        sell_decisions = []
        for sell_item in sell_items:
            # Find the holding being sold
            holding = next((h for h in holdings if h.get('ticker') == sell_item['ticker']), None)
            if holding:
                sell_pct = sell_item.get('sell_pct', 100)
                quantity_to_sell = holding.get('quantity', 0) * (sell_pct / 100.0)

                sell_decisions.append({
                    'ticker': sell_item['ticker'],
                    'action': 'SELL',
                    'shares': quantity_to_sell,
                    'sell_pct': sell_pct,
                    'current_price': holding.get('current_price', 0),
                    'gpt5_reasoning': sell_item.get('reasoning', 'GPT-5 recommended sell'),
                    'composite_score': holding.get('research_composite_score', holding.get('composite_score', 0)),
                    'current_value': holding.get('market_value', 0) * (sell_pct / 100.0)  # Calculate value being sold
                })

        return optimized, sell_decisions

    def _fallback_allocation(self, candidates: List[Dict], available_capital: float, holdings: List[Dict] = None) -> Tuple[List[Dict], List[Dict]]:
        """
        Fallback allocation if GPT-5 fails

        Strategy:
        - SELL any holdings with composite score < 55
        - BUY top 10 candidates by composite score (excluding already-held tickers)
        - Allocate equally

        Args:
            candidates: List of BUY candidates
            available_capital: Capital available to deploy
            holdings: Current holdings (to check for underperformers and avoid duplicate BUYs)

        Returns:
            (top_candidates, sell_decisions)
        """
        if not candidates:
            return [], []

        # Filter out tickers that are already held (avoid duplicate BUYs)
        if holdings is None:
            holdings = []

        holding_tickers = {h.get('ticker') for h in holdings}
        available_candidates = [c for c in candidates if c.get('ticker') not in holding_tickers]

        # Identify underperforming holdings to SELL (composite < 55)
        sell_decisions = []
        for holding in holdings:
            composite = holding.get('research_composite_score', holding.get('composite_score', 0))
            if composite > 0 and composite < 55:  # Only if we have a score and it's low
                sell_decisions.append({
                    'ticker': holding.get('ticker'),
                    'action': 'SELL',
                    'shares': holding.get('quantity', 0),
                    'sell_pct': 100,
                    'current_price': holding.get('current_price', 0),
                    'gpt5_reasoning': f"Fallback: Composite score {composite:.1f} < 55 threshold",
                    'composite_score': composite,
                    'current_value': holding.get('market_value', 0)
                })

        if sell_decisions:
            logger.info(f"Fallback: Identified {len(sell_decisions)} underperforming holdings to SELL")

        if not available_candidates:
            logger.warning("All candidates are already held - no new BUYs to make")
            return [], sell_decisions

        logger.info(f"Fallback: Filtered {len(candidates)} candidates down to {len(available_candidates)} (excluding {len(holding_tickers)} holdings)")

        # Sort by composite score (highest first)
        sorted_candidates = sorted(
            available_candidates,
            key=lambda x: x.get('composite_score', x.get('research_composite_score', 0)),
            reverse=True
        )

        # Select top 10 (or fewer if less than 10 available)
        top_candidates = sorted_candidates[:10]

        logger.warning(f"Fallback: Selected top {len(top_candidates)} candidates by composite score")
        if top_candidates:
            logger.info(f"Top candidate: {top_candidates[0]['ticker']} (score: {top_candidates[0].get('composite_score', 0):.1f})")
            if len(top_candidates) >= 10:
                logger.info(f"10th candidate: {top_candidates[-1]['ticker']} (score: {top_candidates[-1].get('composite_score', 0):.1f})")

        # Allocate 90% of capital equally across top 10
        target_deployment = available_capital * 0.9
        per_position = target_deployment / len(top_candidates) if top_candidates else 0

        for candidate in top_candidates:
            candidate['allocated_capital'] = per_position
            candidate['gpt5_reasoning'] = f"Fallback: Top {len(top_candidates)} by composite score (equal weight)"
            candidate['is_position_adjustment'] = False

        return top_candidates, sell_decisions
