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
            # Fallback: equal weight allocation
            logger.warning("Falling back to equal-weight allocation")
            return self._fallback_allocation(candidates, available_capital), "GPT-5 unavailable - used equal weighting"

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
            candidates_data.append(f"""
CANDIDATE #{i}: {c['ticker']}
  Research Scores:
    - Composite: {c.get('research_composite_score', 0)}/100
    - Technical: {c.get('technical_score', 0)}/100
    - Fundamental: {c.get('fundamental_score', 0)}/100
    - Sentiment: {c.get('sentiment_score', 0)}/100

  Risk Metrics:
    - Entry Price: ${c.get('entry_price', 0):.2f}
    - Stop Loss: ${c.get('stop_loss', 0):.2f}
    - Target Price: ${c.get('target', c.get('target_price', 0)):.2f}
    - Risk/Reward: {c.get('risk_reward_ratio', 0):.2f}:1
    - Risk per Share: ${c.get('risk_per_share', 0):.2f}
    - Total Risk: ${c.get('total_risk', 0):.2f}

  Position Sizing (Risk Dept suggestion):
    - Shares: {c.get('position_size_shares', 0)}
    - Position Value: ${c.get('position_size_value', 0):,.2f}

  Other:
    - Sector: {c.get('sector', 'Unknown')}
""")

        candidates_text = "\n".join(candidates_data)

        prompt = f"""You are the Chief Investment Officer for a quantitative trading firm. Your job is to review candidate stocks and make INTELLIGENT capital allocation decisions.

{market_summary}

PORTFOLIO CONSTRAINTS:
- Available Capital: ${available_capital:,.2f}
- Current Positions: {current_positions}/{max_positions}
- Target Deployment: 90-100% of available capital
- Risk Management: Already validated by Risk Department

CANDIDATES TO REVIEW:
{candidates_text}

YOUR TASK:
1. Review each candidate's scores, risk metrics, and sector
2. Decide which stocks to buy and HOW MUCH capital to allocate to each
3. Weight allocations by conviction:
   - Higher composite scores → More capital
   - Better risk/reward ratios → More capital
   - Diversify across sectors (don't put all eggs in one basket)
4. Ensure total allocation = 90-100% of ${available_capital:,.2f}

ALLOCATION RULES:
- Each position should get between 5% and 20% of available capital
- Higher quality stocks (65+ composite) deserve more capital
- Lower quality stocks (60-64 composite) deserve less capital
- Consider risk/reward - favor stocks with better R:R ratios
- Diversify - don't over-concentrate in one sector

OUTPUT FORMAT:
Provide your analysis and then output ONLY a JSON object with this structure:
```json
{{
  "selected_tickers": [
    {{
      "ticker": "AAPL",
      "allocated_capital": 15000.00,
      "allocation_pct": 15.0,
      "reasoning": "Strong fundamentals (72/100), excellent R:R (2.5:1), tech sector diversification"
    }},
    ...
  ],
  "total_allocated": 95000.00,
  "deployment_pct": 95.0,
  "portfolio_reasoning": "Allocated to 7 high-conviction positions with sector diversification..."
}}
```

Think step-by-step:
1. Rank candidates by composite score and risk/reward
2. Allocate more capital to higher-conviction plays
3. Ensure diversification across sectors
4. Verify total deployment is 90-100%

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
            logger.error(f"Response text: {response_text[:500]}")
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
        Fallback equal-weight allocation if GPT-5 fails

        Returns:
            Candidates with equal capital allocation
        """
        if not candidates:
            return []

        # Allocate 90% of capital equally across all candidates
        target_deployment = available_capital * 0.9
        per_position = target_deployment / len(candidates)

        for candidate in candidates:
            candidate['allocated_capital'] = per_position
            candidate['gpt5_reasoning'] = "Equal-weight fallback allocation"

        return candidates
