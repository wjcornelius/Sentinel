# -*- coding: utf-8 -*-
# sentinel/context_builder.py
# Hierarchical context builder: market → sector → stock

"""
Hierarchical Context Builder

Builds multi-level context to improve AI analysis quality:
1. Market Context: Broad market trends and macroeconomic environment
2. Sector Context: Trends and dynamics within each sector
3. Stock Context: Individual stock positioned within sector context

This hierarchical approach helps the AI make more coherent decisions
by understanding the broader context before analyzing individual stocks.
"""

import logging
from typing import List, Dict, Optional
from collections import defaultdict
import json

from openai import OpenAI

try:
    import config
    OPENAI_API_KEY = config.OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = None


# Market context prompt template
MARKET_CONTEXT_PROMPT = """You are a macro analyst summarizing current market conditions.

Analyze the following market news and data to provide a concise market context briefing.

Focus on:
- Overall market direction and sentiment
- Key macroeconomic factors (interest rates, inflation, employment)
- Sector rotation trends
- Risk factors and opportunities

Keep the summary to 3-4 paragraphs maximum.

Market News and Data:
<<MARKET_DATA>>

Provide a concise market context summary:
"""


# Sector context prompt template
SECTOR_CONTEXT_PROMPT = """You are a sector analyst summarizing trends within a specific sector.

Sector: <<SECTOR_NAME>>

Stocks in this sector (with recent performance):
<<SECTOR_STOCKS>>

Market Context:
<<MARKET_CONTEXT>>

Analyze:
- Sector-wide trends and momentum
- Key drivers and headwinds
- Relative strength vs market
- Investment themes and opportunities

Keep the summary to 2-3 paragraphs.

Provide a sector context summary:
"""


class ContextBuilder:
    """Build hierarchical context for stock analysis."""

    def __init__(
        self,
        openai_client: Optional[OpenAI] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize context builder.

        Args:
            openai_client: Optional OpenAI client (will create if not provided)
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

        if openai_client:
            self.openai = openai_client
        elif OPENAI_API_KEY:
            self.openai = OpenAI(api_key=OPENAI_API_KEY)
        else:
            raise ValueError("OpenAI API key required for context building")

    def build_market_context(self, market_news: Optional[str] = None) -> str:
        """
        Build high-level market context summary.

        Args:
            market_news: Optional market news/data string

        Returns:
            Market context summary
        """
        self.logger.info("Building market context...")

        if not market_news:
            # Default context if no news provided
            self.logger.warning("No market news provided, using default context")
            return (
                "Market conditions are mixed with ongoing economic uncertainty. "
                "Investors are focused on interest rate policy and inflation trends. "
                "Technology and healthcare sectors showing relative strength."
            )

        try:
            prompt = MARKET_CONTEXT_PROMPT.replace("<<MARKET_DATA>>", market_news)

            response = self.openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500,
                timeout=30.0
            )

            market_context = response.choices[0].message.content.strip()
            self.logger.info("Market context built successfully")
            return market_context

        except Exception as e:
            self.logger.error(f"Error building market context: {e}")
            # Return default on error
            return (
                "Unable to fetch current market context. "
                "Proceeding with general market analysis."
            )

    def build_sector_contexts(
        self,
        tier2_finalists: List[Dict],
        market_context: str
    ) -> Dict[str, str]:
        """
        Build sector-level context summaries.

        Args:
            tier2_finalists: List of finalists from Tier 2 (with sector info)
            market_context: Market context summary

        Returns:
            Dict mapping sector name to sector context summary
        """
        self.logger.info("Building sector contexts...")

        # Group finalists by sector
        sectors = defaultdict(list)
        for finalist in tier2_finalists:
            sector = finalist.get('sector', 'Unknown')
            sectors[sector].append(finalist)

        self.logger.info(f"Found {len(sectors)} unique sectors")

        # Build context for each sector
        sector_contexts = {}
        for sector, stocks in sectors.items():
            if sector == 'Unknown':
                sector_contexts[sector] = "Sector information not available."
                continue

            try:
                context = self._build_single_sector_context(
                    sector, stocks, market_context
                )
                sector_contexts[sector] = context
                self.logger.info(f"Built context for {sector} ({len(stocks)} stocks)")

            except Exception as e:
                self.logger.error(f"Error building context for {sector}: {e}")
                sector_contexts[sector] = f"Unable to build context for {sector}."

        return sector_contexts

    def _build_single_sector_context(
        self,
        sector: str,
        stocks: List[Dict],
        market_context: str
    ) -> str:
        """
        Build context summary for a single sector.

        Args:
            sector: Sector name
            stocks: List of stocks in this sector
            market_context: Market context summary

        Returns:
            Sector context summary
        """
        # Build stock summary
        stock_summaries = []
        for stock in stocks:
            metrics = stock.get('metrics', {})
            summary = (
                f"- {stock['symbol']}: "
                f"{metrics.get('change_20d', 0):+.1f}% (20d), "
                f"Tier2 score: {stock.get('tier2_score', 'N/A')}"
            )
            stock_summaries.append(summary)

        stocks_text = "\n".join(stock_summaries)

        # Build prompt
        prompt = SECTOR_CONTEXT_PROMPT.replace("<<SECTOR_NAME>>", sector)
        prompt = prompt.replace("<<SECTOR_STOCKS>>", stocks_text)
        prompt = prompt.replace("<<MARKET_CONTEXT>>", market_context)

        # Call AI
        response = self.openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=400,
            timeout=30.0
        )

        return response.choices[0].message.content.strip()

    def build_hierarchical_context(
        self,
        tier2_finalists: List[Dict],
        market_news: Optional[str] = None
    ) -> Dict:
        """
        Build complete hierarchical context.

        Args:
            tier2_finalists: List of finalists from Tier 2
            market_news: Optional market news/data

        Returns:
            Dict with:
            - 'market_context': str
            - 'sector_contexts': Dict[sector, context]
            - 'finalists_by_sector': Dict[sector, List[stocks]]
        """
        self.logger.info("Building hierarchical context...")

        # Build market context
        market_context = self.build_market_context(market_news)

        # Build sector contexts
        sector_contexts = self.build_sector_contexts(tier2_finalists, market_context)

        # Group finalists by sector for easy lookup
        finalists_by_sector = defaultdict(list)
        for finalist in tier2_finalists:
            sector = finalist.get('sector', 'Unknown')
            finalists_by_sector[sector].append(finalist)

        self.logger.info(
            f"Hierarchical context complete: "
            f"1 market context, {len(sector_contexts)} sector contexts"
        )

        return {
            'market_context': market_context,
            'sector_contexts': dict(sector_contexts),
            'finalists_by_sector': dict(finalists_by_sector)
        }


# Convenience function for use in evening workflow
def build_context(
    tier2_finalists: List[Dict],
    market_news: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> Dict:
    """
    Build hierarchical context for stock analysis.

    Args:
        tier2_finalists: List of finalists from Tier 2 screening
        market_news: Optional market news/data string
        logger: Optional logger

    Returns:
        Dict with market_context, sector_contexts, and finalists_by_sector
    """
    builder = ContextBuilder(logger=logger)
    return builder.build_hierarchical_context(tier2_finalists, market_news)
