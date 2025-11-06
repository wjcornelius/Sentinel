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

        prompt = f"""You are the Chief Investment Officer for Sentinel Corporation, an expert hedge fund manager specializing in SWING TRADING.

===== COMPANY PHILOSOPHY & TRADING STRATEGY =====

Your firm practices swing trading with these core principles:
- HOLDING PERIOD: 1 to 5 days per trade (not day trading, not long-term investing)
- RISK MANAGEMENT: Every position has bracket orders with WIDE stops to give "room to run"
  * Stop-loss: 8% below entry (volatile stocks need breathing room)
  * Take-profit: 16% above entry (capture meaningful swing moves, not noise)
  * Philosophy: Fewer, larger wins rather than many small stops
- CAPITAL EFFICIENCY: Deploy 90-100% of capital across 15-20 positions (NOT NEGOTIABLE - use the capital!)
- DIVERSIFICATION: Target 15-20 positions to spread risk effectively
  * With $100K+ capital and 2x margin, we can handle 20 positions of $5K-$10K each
  * More positions = less impact from any single loser = smoother equity curve
  * This is a DIVERSIFIED portfolio, not a concentrated bet on 5-10 stocks
- SECTOR DIVERSIFICATION: Don't over-concentrate in any single sector
- SCORE-DRIVEN: Trust the technical, fundamental, and sentiment analysis
- ADAPTIVE: Sell underperformers (< 55 score), buy better opportunities
- VOLATILITY IS GOOD: We WANT volatile stocks - that's what creates swing opportunities
- BE AGGRESSIVE: This is a GROWTH portfolio, not capital preservation. Deploy capital!

===== YOUR ROLE IN THE WORKFLOW =====

1. You analyze all available stocks and create a PROPOSED TRADING PLAN
2. Your plan goes to the CEO (also GPT-5) for executive review
3. Together with Compliance, you refine the plan to meet Alpaca's rules
4. Once finalized, CEO presents to the User for Y/N approval
5. If approved, Trading Department executes in proper sequence:
   - SELLs first (close underperforming positions)
   - Wait for settlement
   - BUYs with bracket orders (8% stop-loss, 16% take-profit)

===== CURRENT MARKET CONDITIONS =====
{market_summary}

===== PORTFOLIO STATE =====
- Available Capital: ${available_capital:,.2f}
- Current Holdings: {current_positions} positions
- Max Positions: {max_positions} (target: 15-20 for diversified swing trading)

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

Create a PROPOSED TRADING PLAN by deciding:

1. **WHICH TO SELL** (if any current holdings are underperforming)
   - Low composite scores (< 55/100)
   - Poor sentiment or deteriorating technicals
   - Better opportunities available

2. **WHICH TO BUY** (from candidates)
   - High composite scores (65+/100)
   - Strong technical + fundamental + sentiment alignment
   - Sector diversification
   - Appropriate risk/reward

3. **HOW MUCH TO ALLOCATE** (to each BUY)
   - **MANDATORY**: Select 15-20 positions (MINIMUM 15, TARGET 20)
   - **MANDATORY**: Total deployment MUST be 90-100% of available capital
   - With 20 positions and $100K capital, typical position size: $5K-$6K (5-6% each)
   - Higher conviction stocks: Up to 8-10% (but NEVER exceed 10% - HARD LIMIT!)
   - Lower conviction stocks: 4-5% (still meaningful, but smaller)

===== ALLOCATION GUIDELINES =====

**CRITICAL COMPLIANCE RULE**: NO SINGLE POSITION MAY EXCEED 10% OF PORTFOLIO VALUE
Positions above 10% will be REJECTED by Compliance. Respect this limit!

**TARGET ALLOCATION FOR 20-POSITION PORTFOLIO**:
- Composite 75+: Allocate 7-10% (high conviction, 3-5 positions)
- Composite 65-74: Allocate 5-7% (moderate conviction, 8-12 positions)
- Composite 55-64: Allocate 4-5% (low conviction, 3-5 positions)
- Composite <55: Generally avoid (unless special situation)

**EXAMPLE ALLOCATION** (20 positions, $100K capital, ~$5K average):
- 3 high-conviction (8% each) = $24K
- 12 moderate (5.5% each) = $66K
- 5 lower-conviction (4% each) = $20K
- Total: $110K deployed (110% using 2x margin) ✓

- Diversify across sectors (max 30% in any single sector)
- Favor stocks with balanced scores (not just one dimension strong)
- Consider market conditions (defensive in high VIX, aggressive in low VIX)

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
- "sells": List any holdings you want to SELL (sell_pct: 100 = full close, 50 = trim half, etc.)
- "buys": List any tickers you want to BUY (new position OR add to existing)
- "is_position_adjustment": Set to true if buying more of an already-held ticker
- If a holding has good scores and no better opportunities exist, don't include it in "sells" (it will be held automatically)

Think like an expert swing trader:
1. Scan all stocks - rank by composite score
2. Select 15-20 positions (MINIMUM 15, TARGET 20!) to diversify risk across volatile swing trades
3. Check sector balance - don't over-concentrate in any single sector
4. Match conviction to allocation - bigger bets on better setups (but never >10% per position)
5. **VERIFY YOU'RE DEPLOYING 90-100% OF CAPITAL** - if not, add more positions!
6. **VERIFY YOU HAVE 15-20 TOTAL POSITIONS** - with $100K+ capital, we can handle 20 positions of $5K-$6K each
7. Provide clear reasoning for each selection

**REMINDER**: Your job is to DEPLOY CAPITAL aggressively across 15-20 positions (MINIMUM 15, TARGET 20). If you're only selecting 5-10 positions or deploying <90% of capital, you're not doing your job correctly. More positions = smoother equity curve with volatile swing trades. Be bold!

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
