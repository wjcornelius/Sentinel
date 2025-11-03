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

    def __init__(self, api_key: str):
        """
        Initialize GPT-5 optimizer

        Args:
            api_key: OpenAI API key
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-5"  # GPT-5 - most capable model for financial analysis
        logger.info(f"GPT5PortfolioOptimizer initialized (model: {self.model})")

    def optimize_portfolio(
        self,
        candidates: List[Dict],
        available_capital: float,
        market_conditions: Dict,
        current_positions: int = 0,
        max_positions: int = 10
    ) -> Tuple[List[Dict], str]:
        """
        Use GPT-5 to create optimized portfolio allocation

        Args:
            candidates: List of candidates from Portfolio (post-filtering)
            available_capital: Total capital available to deploy
            market_conditions: Current market state
            current_positions: Number of existing positions
            max_positions: Maximum allowed positions

        Returns:
            (optimized_candidates, reasoning)
            - optimized_candidates: List with 'allocated_capital' field added
            - reasoning: GPT-5's written analysis and justification
        """
        logger.info("=" * 80)
        logger.info("GPT-5 PORTFOLIO OPTIMIZATION")
        logger.info("=" * 80)
        logger.info(f"Reviewing {len(candidates)} candidates")
        logger.info(f"Available capital: ${available_capital:,.0f}")
        logger.info(f"Current positions: {current_positions}/{max_positions}")

        # Build comprehensive prompt for GPT-5
        prompt = self._build_optimization_prompt(
            candidates=candidates,
            available_capital=available_capital,
            market_conditions=market_conditions,
            current_positions=current_positions,
            max_positions=max_positions
        )

        # Call GPT-5
        logger.info("Consulting OpenAI GPT-5 for allocation decisions...")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_completion_tokens=8000,  # GPT-5 uses max_completion_tokens instead of max_tokens
                # Note: GPT-5 only supports temperature=1 (default), removed custom temperature
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
                raise ValueError("GPT-5 returned empty response")

            # Extract JSON allocation from response
            allocations, reasoning = self._parse_gpt5_response(response_text)

            # Apply allocations to candidates
            optimized_candidates = self._apply_allocations(candidates, allocations)

            # Log summary
            total_allocated = sum(c['allocated_capital'] for c in optimized_candidates)
            deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0

            logger.info(f"GPT-5 allocated ${total_allocated:,.0f} ({deployment_pct:.1f}% of available)")
            logger.info(f"Selected {len(optimized_candidates)} positions")

            return optimized_candidates, reasoning

        except Exception as e:
            logger.error(f"GPT-5 optimization failed: {e}", exc_info=True)
            # Fallback: select top 10 by score and allocate equally
            logger.warning("Falling back to top-10 selection with equal weighting")
            fallback_candidates = self._fallback_allocation(candidates, available_capital)
            return fallback_candidates, f"GPT-5 unavailable - selected top {len(fallback_candidates)} by composite score with equal weighting"

    def _build_optimization_prompt(
        self,
        candidates: List[Dict],
        available_capital: float,
        market_conditions: Dict,
        current_positions: int,
        max_positions: int
    ) -> str:
        """Build comprehensive prompt for GPT-5"""

        # Format market conditions
        market_summary = f"""
MARKET CONDITIONS:
- SPY: {market_conditions.get('spy_change_pct', 0):.2f}%
- VIX: {market_conditions.get('vix_level', 0):.1f} ({market_conditions.get('vix_status', 'UNKNOWN')})
- Market Sentiment: {market_conditions.get('market_sentiment', 'NEUTRAL')}
"""

        # Format candidates with ALL data
        candidates_data = []
        for i, c in enumerate(candidates, 1):
            # Get sentiment data (could be dict or float)
            sentiment_info = c.get('sentiment', {})
            if isinstance(sentiment_info, dict):
                sentiment_score = sentiment_info.get('score', 50.0)
                sentiment_summary = sentiment_info.get('summary', 'No data')
            else:
                sentiment_score = c.get('sentiment_score', 50.0)
                sentiment_summary = 'No data'

            candidates_data.append(f"""
CANDIDATE #{i}: {c['ticker']} ({c.get('sector', 'Unknown')})
  Scores:
    - Composite: {c.get('composite_score', c.get('research_composite_score', 0)):.1f}/100
    - Technical: {c.get('technical_score', c.get('technical', {}).get('score', 0)):.1f}/100
    - Fundamental: {c.get('fundamental_score', c.get('fundamental', {}).get('score', 0)):.1f}/100
    - Sentiment: {sentiment_score:.1f}/100

  Trading Info:
    - Current Price: ${c.get('current_price', c.get('entry_price', 0)):.2f}
    - Sentiment Summary: {sentiment_summary[:80]}...
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
- CAPITAL EFFICIENCY: Deploy 90-100% of capital across 5-10 positions
- SECTOR DIVERSIFICATION: Don't over-concentrate in any single sector
- SCORE-DRIVEN: Trust the technical, fundamental, and sentiment analysis
- ADAPTIVE: Sell underperformers, buy better opportunities
- VOLATILITY IS GOOD: We WANT volatile stocks - that's what creates swing opportunities

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
- Max Positions: {max_positions} (target: 5-10 for swing trading)

===== STOCKS TO ANALYZE =====

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
   - Higher conviction = More capital (up to 20% per position)
   - Lower conviction = Less capital (minimum 5% per position)
   - Total deployment: 90-100% of available capital

===== ALLOCATION GUIDELINES =====

- Composite 75+: Allocate 15-20% (high conviction)
- Composite 65-74: Allocate 10-15% (moderate conviction)
- Composite 55-64: Allocate 5-10% (low conviction)
- Composite <55: Generally avoid (unless special situation)

- Diversify across sectors (max 30% in any single sector)
- Favor stocks with balanced scores (not just one dimension strong)
- Consider market conditions (defensive in high VIX, aggressive in low VIX)

===== OUTPUT FORMAT =====

Provide your strategic analysis (2-3 paragraphs), then output a JSON object:

```json
{{
  "selected_tickers": [
    {{
      "ticker": "AAPL",
      "allocated_capital": 15000.00,
      "allocation_pct": 15.0,
      "reasoning": "Strong balanced scores (Tech:85, Fund:78, Sent:72). Uptrend with MACD bullish. Tech sector diversification."
    }},
    ...
  ],
  "total_allocated": 95000.00,
  "deployment_pct": 95.0,
  "portfolio_reasoning": "Selected 7 positions across 5 sectors. Emphasis on tech/fundamental strength given stable market conditions (VIX {market_conditions.get('vix_level', 20):.1f}). Holding period: 2-4 days target."
}}
```

Think like an expert swing trader:
1. Scan all stocks - rank by composite score
2. Check sector balance - diversify intelligently
3. Match conviction to allocation - bigger bets on better setups
4. Verify 90-100% capital deployment
5. Provide clear reasoning for each selection

Begin your analysis:"""

        return prompt

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

    def _apply_allocations(self, candidates: List[Dict], allocations: Dict) -> List[Dict]:
        """
        Apply GPT-5's allocations to candidate list

        Returns:
            List of selected candidates with 'allocated_capital' field
        """
        selected_tickers = {
            item['ticker']: item['allocated_capital']
            for item in allocations['selected_tickers']
        }

        optimized = []
        for candidate in candidates:
            ticker = candidate['ticker']
            if ticker in selected_tickers:
                # Add GPT-5's allocation
                candidate['allocated_capital'] = selected_tickers[ticker]
                candidate['gpt5_reasoning'] = next(
                    (item['reasoning'] for item in allocations['selected_tickers'] if item['ticker'] == ticker),
                    "Selected by GPT-5"
                )
                optimized.append(candidate)

        return optimized

    def _fallback_allocation(self, candidates: List[Dict], available_capital: float) -> List[Dict]:
        """
        Fallback allocation if GPT-5 fails

        Strategy: Select top 10 candidates by composite score and allocate equally
        This is much better than allocating to all 50 candidates

        Returns:
            Top 10 candidates with equal capital allocation
        """
        if not candidates:
            return []

        # Sort by composite score (highest first)
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.get('composite_score', x.get('research_composite_score', 0)),
            reverse=True
        )

        # Select top 10 (or fewer if less than 10 available)
        top_candidates = sorted_candidates[:10]

        logger.warning(f"Fallback: Selected top {len(top_candidates)} candidates by composite score")
        if top_candidates:
            logger.info(f"Top candidate: {top_candidates[0]['ticker']} (score: {top_candidates[0].get('composite_score', 0):.1f})")
            logger.info(f"10th candidate: {top_candidates[-1]['ticker']} (score: {top_candidates[-1].get('composite_score', 0):.1f})")

        # Allocate 90% of capital equally across top 10
        target_deployment = available_capital * 0.9
        per_position = target_deployment / len(top_candidates)

        for candidate in top_candidates:
            candidate['allocated_capital'] = per_position
            candidate['gpt5_reasoning'] = f"Fallback: Top {len(top_candidates)} by composite score (equal weight)"

        return top_candidates
