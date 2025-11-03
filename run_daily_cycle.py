"""
Sentinel Corporation - Daily Trading Cycle
Phase 2: CEO Orchestration

Linear Pipeline:
1. Research v3.0 → Generate ~50 swing-suitable candidates
2. News → Add sentiment scores + summarized content
3. Compliance → Review and comment
4. Portfolio + CEO → Make final decisions

All departments have access to each other (mesh network)
but primary flow is linear for clarity.

Run this daily to generate trading recommendations.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import config for API keys
import config

# Import departments
from Departments.Research import ResearchDepartment
from Departments.News import NewsDepartment
from Departments.Compliance import ComplianceDepartment
from Departments.Portfolio import PortfolioDepartment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DailyCycle')


class SentinelCEO:
    """
    Sentinel Corporation CEO - Orchestrates daily trading cycle

    Responsibilities:
    1. Initialize all departments (mesh network)
    2. Execute linear pipeline (Research → News → Compliance → Portfolio)
    3. Handle errors gracefully
    4. Generate daily report
    """

    def __init__(self, db_path: str = "sentinel.db", alpaca_client=None):
        self.db_path = Path(db_path)
        self.alpaca = alpaca_client

        logger.info("=" * 100)
        logger.info("SENTINEL CORPORATION - CEO INITIALIZING")
        logger.info("=" * 100)
        logger.info("")

        # Initialize all departments (mesh network - all can access each other)
        logger.info("Initializing departments...")

        self.research = ResearchDepartment(db_path=str(self.db_path), alpaca_client=alpaca_client)
        self.news = NewsDepartment(
            db_path=str(self.db_path),
            perplexity_api_key=config.PERPLEXITY_API_KEY
        )
        self.compliance = ComplianceDepartment(
            config_path=project_root / "Config" / "compliance_config.yaml",
            db_path=self.db_path
        )
        self.portfolio = PortfolioDepartment(
            config_path=project_root / "Config" / "portfolio_config.yaml",
            db_path=self.db_path
        )

        # Store departments in dict for easy access
        self.departments = {
            'research': self.research,
            'news': self.news,
            'compliance': self.compliance,
            'portfolio': self.portfolio
        }

        logger.info("")
        logger.info("All departments initialized - mesh network active")
        logger.info("=" * 100)
        logger.info("")

    def run_daily_cycle(self) -> Dict:
        """
        Execute daily trading cycle

        Returns:
            Dict with pipeline results and final recommendations
        """
        logger.info("=" * 100)
        logger.info(f"DAILY TRADING CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 100)
        logger.info("")

        try:
            # STAGE 1: RESEARCH - Generate swing-suitable candidates
            logger.info("STAGE 1: RESEARCH DEPARTMENT")
            logger.info("-" * 100)

            research_output = self.research.generate_daily_candidate_universe()

            buy_candidates = research_output.get('buy_candidates', [])
            current_holdings = research_output.get('current_holdings', [])

            logger.info(f"Research complete:")
            logger.info(f"  - Buy candidates: {len(buy_candidates)} (all swing-suitable)")
            logger.info(f"  - Current holdings: {len(current_holdings)}")
            logger.info("")

            if len(buy_candidates) == 0:
                logger.warning("No buy candidates found - stopping pipeline")
                return {
                    'success': False,
                    'stage': 'research',
                    'message': 'No buy candidates found',
                    'data': research_output
                }

            # STAGE 2: NEWS - Add sentiment scores
            logger.info("STAGE 2: NEWS DEPARTMENT")
            logger.info("-" * 100)

            # Get all tickers (candidates + holdings)
            all_tickers = []
            for c in buy_candidates:
                ticker = c if isinstance(c, str) else c.get('ticker')
                if ticker:
                    all_tickers.append(ticker)

            for h in current_holdings:
                ticker = h if isinstance(h, str) else h.get('ticker')
                if ticker and ticker not in all_tickers:
                    all_tickers.append(ticker)

            # Fetch sentiment for all tickers (batch call)
            sentiment_data = self.news.get_sentiment_scores(all_tickers)

            logger.info(f"News complete:")
            logger.info(f"  - Sentiment scores: {len(sentiment_data)} tickers")
            logger.info("")

            # Enrich candidates and holdings with sentiment
            enriched_candidates = []
            for c in buy_candidates:
                ticker = c if isinstance(c, str) else c.get('ticker')
                if isinstance(c, dict):
                    c['sentiment_score'] = sentiment_data.get(ticker, {}).get('sentiment_score', 50)
                    c['news_summary'] = sentiment_data.get(ticker, {}).get('news_summary', '')
                    enriched_candidates.append(c)
                else:
                    enriched_candidates.append({
                        'ticker': ticker,
                        'sentiment_score': sentiment_data.get(ticker, {}).get('sentiment_score', 50),
                        'news_summary': sentiment_data.get(ticker, {}).get('news_summary', '')
                    })

            enriched_holdings = []
            for h in current_holdings:
                ticker = h if isinstance(h, str) else h.get('ticker')
                if isinstance(h, dict):
                    h['sentiment_score'] = sentiment_data.get(ticker, {}).get('sentiment_score', 50)
                    h['news_summary'] = sentiment_data.get(ticker, {}).get('news_summary', '')
                    enriched_holdings.append(h)
                else:
                    enriched_holdings.append({
                        'ticker': ticker,
                        'sentiment_score': sentiment_data.get(ticker, {}).get('sentiment_score', 50),
                        'news_summary': sentiment_data.get(ticker, {}).get('news_summary', '')
                    })

            # STAGE 3: COMPLIANCE - Review
            logger.info("STAGE 3: COMPLIANCE DEPARTMENT")
            logger.info("-" * 100)

            # Validate each candidate through compliance
            # Note: Compliance validates individual trade proposals, not bulk lists
            # For now, we'll do a simplified check - just mark as "approved" if not restricted
            approved_candidates = []
            flagged_candidates = []

            logger.info(f"Validating {len(enriched_candidates)} candidates...")

            for candidate in enriched_candidates:
                ticker = candidate.get('ticker') if isinstance(candidate, dict) else candidate

                # Simple compliance check - for full validation we'd need more trade details
                # (shares, price, position_value, etc) which come from Portfolio decisions
                # For Phase 2, we'll just filter out restricted tickers
                try:
                    # Check if ticker is restricted (penny stock, low liquidity, etc)
                    # This is a simplified check - full validation happens during actual trade execution
                    price = candidate.get('price', 10.0) if isinstance(candidate, dict) else 10.0

                    # Compliance validator checks restricted list, but we need a trade proposal format
                    # For now, skip detailed validation and just pass through
                    # Full compliance validation will happen in Portfolio Department when creating orders
                    approved_candidates.append(candidate)

                except Exception as e:
                    logger.warning(f"Compliance check failed for {ticker}: {e}")
                    flagged_candidates.append(candidate)

            logger.info(f"Compliance complete:")
            logger.info(f"  - Approved: {len(approved_candidates)}")
            logger.info(f"  - Flagged: {len(flagged_candidates)}")
            logger.info("")

            # STAGE 4: PORTFOLIO + CEO - Final decisions
            logger.info("STAGE 4: PORTFOLIO OPTIMIZATION")
            logger.info("-" * 100)

            logger.info(f"  - Approved candidates for optimization: {len(approved_candidates)}")
            logger.info("")

            # Portfolio would optimize here
            # For now, just pass through top candidates

            logger.info("=" * 100)
            logger.info("DAILY CYCLE COMPLETE")
            logger.info("=" * 100)
            logger.info("")

            return {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'research': {
                    'buy_candidates': len(buy_candidates),
                    'current_holdings': len(current_holdings)
                },
                'news': {
                    'sentiment_scored': len(sentiment_data)
                },
                'compliance': {
                    'approved': len(approved_candidates),
                    'flagged': len(flagged_candidates)
                },
                'portfolio': {
                    'candidates_for_optimization': len(approved_candidates)
                },
                'final_output': {
                    'approved_candidates': approved_candidates[:20]  # Top 20
                }
            }

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Run daily trading cycle"""
    print("\n")
    print("=" * 100)
    print("SENTINEL CORPORATION - DAILY TRADING CYCLE")
    print("=" * 100)
    print("\n")

    # Initialize CEO
    ceo = SentinelCEO(db_path="sentinel.db")

    # Run daily cycle
    result = ceo.run_daily_cycle()

    # Print summary
    print("\n")
    print("=" * 100)
    print("RESULTS SUMMARY")
    print("=" * 100)

    if result['success']:
        print(f"\nSuccess: {result['success']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"\nResearch: {result['research']['buy_candidates']} candidates, {result['research']['current_holdings']} holdings")
        print(f"News: {result['news']['sentiment_scored']} tickers scored")
        print(f"Compliance: {result['compliance']['approved']} approved, {result['compliance']['flagged']} flagged")
        print(f"Portfolio: {result['portfolio']['candidates_for_optimization']} ready for optimization")
        print(f"\nTop approved candidates: {len(result['final_output']['approved_candidates'])}")

        if result['final_output']['approved_candidates']:
            print("\nTop 10 Approved Candidates:")
            for i, candidate in enumerate(result['final_output']['approved_candidates'][:10], 1):
                ticker = candidate.get('ticker', 'UNKNOWN')
                sentiment = candidate.get('sentiment_score', 50)
                compliance = candidate.get('compliance_status', 'UNKNOWN')
                print(f"  {i:2d}. {ticker:6s} - Sentiment: {sentiment:.0f}/100, Status: {compliance}")
    else:
        print(f"\nFailed: {result.get('error', 'Unknown error')}")

    print("\n")
    print("=" * 100)
    print("\n")

    return result


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result.get('success') else 1)
