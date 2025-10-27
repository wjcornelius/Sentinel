# -*- coding: utf-8 -*-
# sentinel/tier2_ai_screening.py
# Tier 2: AI-powered screening to reduce candidates from ~250 to ~70 stocks

"""
Tier 2 AI Screening

Uses GPT-4o-mini (cheaper, faster model) to quickly triage candidates
from Tier 1 technical filtering.

Objective: Identify which stocks are worth deep analysis
Method: Lightweight AI screening with basic metrics + headlines
Model: GPT-4o-mini (~$0.002 per stock vs $0.05 for GPT-4 Turbo)
Output: Top 70 stocks by screening score (1-10)

Cost: ~$0.50/day (250 stocks × $0.002 each)
"""

import logging
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import yfinance as yf

from openai import OpenAI
import alpaca_trade_api as tradeapi

try:
    import config
    OPENAI_API_KEY = config.OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = None


# Lightweight screening prompt template
SCREENING_PROMPT_TEMPLATE = """You are a quantitative analyst performing rapid triage on stock candidates.

Your task: Rate each stock 1-10 for "worth deeper analysis" based on brief context.

Rating Scale:
- 1-3: Poor candidate (weak fundamentals, bad news, declining trends)
- 4-6: Average candidate (mixed signals, uncertain outlook)
- 7-8: Good candidate (solid metrics, positive trends)
- 9-10: Excellent candidate (strong fundamentals, compelling opportunity)

Consider:
- Sector trends and positioning
- Recent price momentum and technical setup
- News sentiment (bullish/bearish signals)
- Market cap and liquidity
- Risk/reward profile

Be selective: Only ~30% should score 7+

Respond with JSON array:
[
  {"symbol": "AAPL", "score": 8, "reason": "Strong momentum, positive sector outlook"},
  {"symbol": "XYZ", "score": 4, "reason": "Mixed signals, sector headwinds"}
]

Candidates:
<<CANDIDATES>>
"""


class Tier2AIScreening:
    """AI-powered screening using GPT-4o-mini."""

    def __init__(
        self,
        api: tradeapi.REST,
        openai_client: Optional[OpenAI] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize Tier 2 screening.

        Args:
            api: Alpaca REST API instance
            openai_client: Optional OpenAI client (will create if not provided)
            logger: Optional logger instance
        """
        self.api = api
        self.logger = logger or logging.getLogger(__name__)

        if openai_client:
            self.openai = openai_client
        elif OPENAI_API_KEY:
            self.openai = OpenAI(api_key=OPENAI_API_KEY)
        else:
            raise ValueError("OpenAI API key required for Tier 2 screening")

    def screen_candidates(
        self,
        tier1_candidates: List[Dict],
        market_context: Optional[str] = None,
        target_count: int = 70,
        batch_size: int = 15
    ) -> List[Dict]:
        """
        Screen candidates using AI to select finalists for deep analysis.

        Args:
            tier1_candidates: Output from Tier 1 filter (list of dicts with symbol, score, metrics)
            market_context: Optional market context summary
            target_count: Number of finalists to return
            batch_size: Number of stocks to screen per API call

        Returns:
            List of top candidates with screening scores
        """
        self.logger.info(f"Starting Tier 2 AI screening on {len(tier1_candidates)} candidates...")

        # Enrich candidates with sector and news
        enriched_candidates = []
        for candidate in tier1_candidates:
            enriched = self._enrich_candidate(candidate)
            if enriched:
                enriched_candidates.append(enriched)

        self.logger.info(f"Enriched {len(enriched_candidates)} candidates with sector/news data")

        # Screen in batches
        all_scores = []
        errors = 0

        for i in range(0, len(enriched_candidates), batch_size):
            batch = enriched_candidates[i:i + batch_size]

            try:
                batch_results = self._screen_batch(batch, market_context)
                all_scores.extend(batch_results)

                self.logger.info(
                    f"Screened batch {i//batch_size + 1}/{(len(enriched_candidates) + batch_size - 1)//batch_size}: "
                    f"{len(batch)} stocks"
                )
            except Exception as e:
                self.logger.error(f"Error screening batch {i//batch_size + 1}: {e}")
                errors += 1
                # Add candidates with default score to avoid losing them
                for candidate in batch:
                    all_scores.append({
                        'symbol': candidate['symbol'],
                        'tier1_score': candidate['tier1_score'],
                        'tier2_score': 5,  # Default middle score
                        'tier2_reason': f"Screening failed: {str(e)[:50]}",
                        'sector': candidate.get('sector'),
                        'metrics': candidate.get('metrics')
                    })

        # Sort by tier2_score and take top N
        all_scores.sort(key=lambda x: x['tier2_score'], reverse=True)
        finalists = all_scores[:target_count]

        self.logger.info(
            f"Tier 2 screening complete: {len(finalists)}/{len(tier1_candidates)} selected "
            f"({errors} batch errors)"
        )

        return finalists

    def _enrich_candidate(self, candidate: Dict) -> Optional[Dict]:
        """
        Enrich candidate with sector and recent news.

        Args:
            candidate: Tier 1 candidate dict

        Returns:
            Enriched candidate dict or None if data unavailable
        """
        symbol = candidate['symbol']

        try:
            # Get sector from yfinance
            ticker = yf.Ticker(symbol)
            info = ticker.info
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')

            # Get recent headlines from Alpaca
            try:
                news = self.api.get_news(symbol, limit=3)
                headlines = [n.headline for n in news[:3]]
            except:
                headlines = []

            return {
                'symbol': symbol,
                'tier1_score': candidate['score'],
                'sector': sector,
                'industry': industry,
                'metrics': candidate['metrics'],
                'headlines': headlines
            }

        except Exception as e:
            self.logger.debug(f"Error enriching {symbol}: {e}")
            # Return basic version without enrichment
            return {
                'symbol': symbol,
                'tier1_score': candidate['score'],
                'sector': 'Unknown',
                'industry': 'Unknown',
                'metrics': candidate['metrics'],
                'headlines': []
            }

    def _screen_batch(
        self,
        batch: List[Dict],
        market_context: Optional[str] = None
    ) -> List[Dict]:
        """
        Screen a batch of candidates using GPT-4o-mini.

        Args:
            batch: List of enriched candidate dicts
            market_context: Optional market context

        Returns:
            List of screening results with scores
        """
        # Build lightweight candidate summaries
        candidate_summaries = []
        for candidate in batch:
            metrics = candidate['metrics']
            summary = {
                'symbol': candidate['symbol'],
                'sector': candidate['sector'],
                'price': f"${metrics['price']:.2f}",
                'momentum_20d': f"{metrics['change_20d']:+.1f}%",
                'rsi': f"{metrics['rsi']:.0f}",
                'volume': f"${metrics['avg_dollar_volume']/1e6:.0f}M/day",
                'headlines': candidate['headlines'][:2]  # Top 2 headlines only
            }
            candidate_summaries.append(summary)

        # Build prompt
        candidates_json = json.dumps(candidate_summaries, indent=2)
        prompt = SCREENING_PROMPT_TEMPLATE.replace("<<CANDIDATES>>", candidates_json)

        if market_context:
            prompt = f"Market Context:\n{market_context}\n\n{prompt}"

        # Call GPT-4o-mini
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,  # Lower temperature for more consistent scoring
                timeout=30.0
            )

            content = response.choices[0].message.content

            # Parse response - handle both array and object formats
            parsed = json.loads(content)
            if isinstance(parsed, dict) and 'results' in parsed:
                results = parsed['results']
            elif isinstance(parsed, dict) and 'candidates' in parsed:
                results = parsed['candidates']
            elif isinstance(parsed, list):
                results = parsed
            else:
                # Try to find the array in the dict
                for value in parsed.values():
                    if isinstance(value, list):
                        results = value
                        break
                else:
                    raise ValueError(f"Unexpected response format: {parsed}")

            # Map results back to candidates
            screening_results = []
            for candidate in batch:
                symbol = candidate['symbol']

                # Find matching result
                ai_result = next((r for r in results if r.get('symbol') == symbol), None)

                if ai_result:
                    score = ai_result.get('score', 5)
                    reason = ai_result.get('reason', 'No reason provided')
                else:
                    score = 5  # Default if not found
                    reason = 'Not scored by AI'

                screening_results.append({
                    'symbol': symbol,
                    'tier1_score': candidate['tier1_score'],
                    'tier2_score': score,
                    'tier2_reason': reason,
                    'sector': candidate['sector'],
                    'metrics': candidate['metrics'],
                    'headlines': candidate['headlines']
                })

            return screening_results

        except Exception as e:
            self.logger.error(f"Error in AI screening: {e}")
            raise


# Convenience function for use in evening workflow
def run_tier2_screening(
    api: tradeapi.REST,
    tier1_candidates: List[Dict],
    market_context: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    target_count: int = 70
) -> List[Dict]:
    """
    Run Tier 2 AI screening.

    Args:
        api: Alpaca REST API instance
        tier1_candidates: Output from Tier 1 filter
        market_context: Optional market context summary
        logger: Optional logger
        target_count: Number of finalists to return

    Returns:
        List of top candidates with AI screening scores
    """
    screener = Tier2AIScreening(api, logger=logger)
    return screener.screen_candidates(tier1_candidates, market_context, target_count)
