"""
OPERATIONS MANAGER DEPARTMENT - Sentinel Corporation
Coordinates workflow across all departments with quality assurance and escalation handling

Primary Responsibilities:
- Coordinate Research → Risk → Portfolio → Compliance workflow
- Validate quality at each stage
- Handle department failures with retry logic
- Escalate issues to CEO when needed
- Track progress and provide transparency

Philosophy: Like a real Operations Manager - coordinates work, ensures quality,
handles problems, keeps CEO informed.

Author: Claude Code (CC)
Architecture: Based on user's corporate structure vision
Date: November 1, 2025
"""

import sys
import yaml
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, date, timezone
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import departments
from Departments.Research.research_department import ResearchDepartment
from Departments.News.news_department import NewsDepartment
from Departments.Risk.risk_department import RiskDepartment
from Departments.Portfolio.portfolio_department import PortfolioDepartment
from Departments.Compliance.compliance_department import ComplianceDepartment
from Departments.Executive.gpt5_portfolio_optimizer import GPT5PortfolioOptimizer
from Departments.Operations.realism_simulator import RealismSimulator

# Import config
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('OperationsManager')


@dataclass
class WorkflowStageResult:
    """Result from a workflow stage"""
    stage: str
    success: bool
    data: Dict
    message: str
    quality_score: int  # 0-100
    issues: List[str]


@dataclass
class Escalation:
    """Issue that needs CEO attention"""
    stage: str
    issue_type: str
    severity: str  # 'INFO', 'WARNING', 'CRITICAL'
    context: Dict
    options: List[str]
    recommendation: str


class OperationsManager:
    """
    Coordinates workflow across all departments
    Handles quality assurance and escalations
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.db_path = project_root / "sentinel.db"
        self.messages_dir = project_root / "Messages_Between_Departments"
        self.config_dir = project_root / "Config"

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("=" * 80)
        self.logger.info("OPERATIONS MANAGER - INITIALIZING")
        self.logger.info("=" * 80)

        # Quality thresholds
        self.min_research_candidates = 3
        self.min_risk_approved = 2
        self.min_portfolio_approved = 1
        self.min_compliance_approved = 1

        # Retry limits
        self.max_retries = 2
        self.retry_count = {}

        # Initialize departments (lazy loading)
        self._research_dept = None
        self._news_dept = None
        self._risk_dept = None
        self._portfolio_dept = None
        self._compliance_dept = None
        self._gpt5_optimizer = None

        # Initialize Realism Simulator
        self.realism_sim = RealismSimulator(project_root)

        # Mandatory sells (injected from external sources like drift monitor)
        self.mandatory_sells = []

        self.logger.info("Operations Manager initialized successfully")
        self.logger.info(f"Project root: {project_root}")
        self.logger.info(f"Database: {self.db_path}")

    def set_mandatory_sells(self, sells: List[Dict]):
        """
        Set mandatory sell orders that must be included in the trading plan.
        These bypass the normal sell decision logic (e.g., position drift trims).

        Args:
            sells: List of sell orders with ticker, shares, reason, source
        """
        self.mandatory_sells = sells
        if sells:
            self.logger.info(f"[OpsManager] Registered {len(sells)} mandatory sell order(s)")
            for sell in sells:
                self.logger.info(f"  - {sell.get('ticker')}: SELL {sell.get('shares')} shares")
                self.logger.info(f"    Source: {sell.get('source', 'unknown')}")

    def generate_trading_plan(self, ai_model: str = 'gpt-4o-mini') -> Dict:
        """
        Coordinate all departments to generate complete trading plan

        Args:
            ai_model: AI model for portfolio optimization (default: gpt-4o-mini)

        Returns:
            Dict with:
            - status: 'SUCCESS', 'ESCALATED', 'FAILED'
            - plan: Final trading plan (if SUCCESS)
            - escalation: Escalation details (if ESCALATED)
            - stage_results: Results from each stage
        """
        # Store model choice for GPT-5 optimizer stage
        self.ai_model = ai_model

        self.logger.info("=" * 80)
        self.logger.info("GENERATING TRADING PLAN - WORKFLOW START")
        self.logger.info("=" * 80)
        self.logger.info(f"AI Model: {ai_model}")

        stage_results = []

        try:
            # STAGE 1: Research Department (50 buy candidates)
            self.logger.info("\n[STAGE 1/3] Research Department - Market Analysis & Candidate Screening")
            research_result = self._run_research_stage()
            stage_results.append(research_result)

            if not research_result.success:
                return self._handle_stage_failure('research', research_result, stage_results)

            # STAGE 2: News Department (sentiment for ALL ~110 stocks: candidates + holdings)
            self.logger.info("\n[STAGE 2/3] News Department - Sentiment Analysis for All Stocks")
            news_result = self._run_news_stage(research_result)
            stage_results.append(news_result)

            if not news_result.success:
                return self._handle_stage_failure('news', news_result, stage_results)

            # STAGE 3: Portfolio Allocator (creates proposed trading plan from all scored stocks)
            model_display = "DETERMINISTIC"
            self.logger.info(f"\n[STAGE 3/3] Portfolio Allocator - Creating Proposed Trading Plan")
            self.logger.info(f"  (Using deterministic logic based on comparative ranking...)")
            gpt5_result = self._run_gpt5_optimization_stage(news_result)  # Function name kept for compatibility
            stage_results.append(gpt5_result)

            if not gpt5_result.success:
                return self._handle_stage_failure('gpt5_optimizer', gpt5_result, stage_results)

            # COMPLIANCE ENFORCEMENT - Reject trades that violate rules
            self.logger.info("\n[COMPLIANCE ENFORCEMENT] Compliance Department - Enforcing Risk Limits")
            self.logger.info("  (Validating all proposed trades against position sizing and risk rules...)")
            compliance_result = self._run_compliance_advisory_loop(gpt5_result)
            stage_results.append(compliance_result)

            # Note: Compliance now ENFORCES rules - rejected trades are blocked
            # The final plan incorporates all agreed-upon improvements

            # ALL STAGES COMPLETE - Aggregate final plan for CEO presentation
            self.logger.info("\n[AGGREGATION] Building final trading plan for CEO review")
            final_plan = self._aggregate_final_plan(stage_results)

            self.logger.info("=" * 80)
            self.logger.info(f"TRADING PLAN GENERATION COMPLETE - {final_plan['summary']['total_trades']} trades")
            self.logger.info("=" * 80)

            return {
                'status': 'SUCCESS',
                'plan': final_plan,
                'stage_results': [self._serialize_result(r) for r in stage_results],
                'generated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }

        except Exception as e:
            self.logger.error(f"WORKFLOW FAILED with exception: {e}", exc_info=True)
            return {
                'status': 'FAILED',
                'error': str(e),
                'stage_results': [self._serialize_result(r) for r in stage_results]
            }

    def _run_research_stage(self) -> WorkflowStageResult:
        """Run Research Department and validate output"""
        try:
            # Initialize Research Department v3.0
            if not self._research_dept:
                self.logger.info("  Initializing Research Department v3.0...")

                # Try to get Alpaca client for current holdings
                alpaca_client = None
                try:
                    from Utils.alpaca_client import AlpacaClient
                    alpaca_client = AlpacaClient()
                    self.logger.info("  Alpaca client available - will fetch current holdings")
                except Exception as e:
                    self.logger.warning(f"  Alpaca client not available: {e}")
                    self.logger.info("  Continuing without current holdings")

                self._research_dept = ResearchDepartment(
                    db_path=str(self.db_path),
                    alpaca_client=alpaca_client
                )

            # Generate daily briefing (this calls the REAL Research Department)
            self.logger.info("  Generating market briefing and candidate screening...")
            self.logger.info("  (This may take 1-2 minutes for full analysis...)")

            message_id = self._research_dept.generate_daily_briefing()

            # Read the message back to get candidate count
            outbox = self.messages_dir / "Outbox" / "RESEARCH"
            msg_file = outbox / f"{message_id}.md"

            if not msg_file.exists():
                raise FileNotFoundError(f"Research output message not found: {msg_file}")

            # Parse message to extract candidate data
            with open(msg_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract JSON payload
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON payload found in Research message")

            candidates = data.get('candidates', [])
            holdings = data.get('current_holdings', [])  # Extract holdings from Research
            candidate_count = len(candidates)

            # Quality validation
            issues = []
            if candidate_count < self.min_research_candidates:
                issues.append(f"Only {candidate_count} candidates found (minimum {self.min_research_candidates})")

            # Calculate quality score based on candidate count AND scores
            if candidates:
                avg_score = sum(c.get('composite_score', 0) for c in candidates) / len(candidates)
                quality_score = min(100, int((candidate_count / max(self.min_research_candidates, 5)) * 50 + (avg_score / 100) * 50))
            else:
                avg_score = 0
                quality_score = 0

            # Allow proceeding with just holdings if we have some (evaluate for potential sells)
            # Only fail if we have BOTH no candidates AND no holdings
            if candidate_count == 0 and len(holdings) > 0:
                self.logger.warning(f"  No new candidates found, but we have {len(holdings)} holdings to evaluate")
                self.logger.warning(f"  Proceeding with holdings-only analysis (may result in sell decisions)")
                success = True  # Allow to proceed
            else:
                success = candidate_count >= self.min_research_candidates

            self.logger.info(f"  Research completed: {candidate_count} candidates found, {len(holdings)} holdings")
            if candidates:
                top_3 = sorted(candidates, key=lambda x: x.get('composite_score', 0), reverse=True)[:3]
                self.logger.info(f"  Top candidates:")
                for c in top_3:
                    self.logger.info(f"    - {c['ticker']}: Score {c.get('composite_score', 0):.1f}/100")

            if issues:
                for issue in issues:
                    self.logger.warning(f"  ISSUE: {issue}")

            avg_score = sum(c.get('composite_score', 0) for c in candidates) / len(candidates) if candidates else 0

            return WorkflowStageResult(
                stage='research',
                success=success,
                data={
                    'message_id': message_id,
                    'candidates': candidates,
                    'current_holdings': holdings,  # Pass holdings forward to News stage
                    'candidate_count': candidate_count,
                    'avg_score': avg_score
                },
                message=f"Research found {candidate_count} candidates (avg score: {avg_score:.1f})" if candidates else f"Research found {candidate_count} candidates",
                quality_score=quality_score,
                issues=issues
            )

        except Exception as e:
            self.logger.error(f"  Research stage FAILED: {e}", exc_info=True)
            return WorkflowStageResult(
                stage='research',
                success=False,
                data={},
                message=f"Research failed: {str(e)}",
                quality_score=0,
                issues=[str(e)]
            )

    def _run_news_stage(self, research_result: WorkflowStageResult) -> WorkflowStageResult:
        """
        Run News Department to enrich candidates with sentiment scores

        Takes Research output and adds sentiment analysis for ALL stocks:
        - Candidates from Research
        - Current holdings from Alpaca (included in Research output)

        Returns WorkflowStageResult with enriched candidate data
        """
        try:
            # Initialize News Department
            if not self._news_dept:
                self.logger.info("  Initializing News Department...")
                self._news_dept = NewsDepartment(
                    db_path=str(self.db_path),
                    perplexity_api_key=config.PERPLEXITY_API_KEY if hasattr(config, 'PERPLEXITY_API_KEY') else None
                )
                self.logger.info("  News Department initialized")

            # Extract candidates from Research result
            candidates = research_result.data.get('candidates', [])
            holdings = research_result.data.get('current_holdings', [])

            # Collect all tickers (candidates + holdings)
            candidate_tickers = [c['ticker'] for c in candidates]
            holding_tickers = [h['ticker'] for h in holdings] if holdings else []
            all_tickers = list(set(candidate_tickers + holding_tickers))  # Deduplicate

            self.logger.info(f"  Scoring sentiment for {len(all_tickers)} stocks:")
            self.logger.info(f"    - Candidates: {len(candidate_tickers)}")
            self.logger.info(f"    - Holdings: {len(holding_tickers)}")

            # Get sentiment scores for all tickers
            sentiment_data = self._news_dept.get_sentiment_scores(all_tickers)

            # Enrich candidates with sentiment
            enriched_candidates = []
            for candidate in candidates:
                ticker = candidate['ticker']
                sent_info = sentiment_data.get(ticker, {})

                # Update sentiment in candidate dict
                candidate['sentiment'] = {
                    'score': sent_info.get('sentiment_score', 50.0),
                    'summary': sent_info.get('news_summary', 'No sentiment data available'),
                    'news_count': 1 if sent_info else 0
                }

                # Recalculate composite score with real sentiment
                tech_score = candidate.get('technical', {}).get('score', 50.0)
                fund_score = candidate.get('fundamental', {}).get('score', 50.0)
                sent_score = candidate['sentiment']['score']

                # Use same weights as Research (40% tech, 40% fund, 20% sent)
                composite_score = (tech_score * 0.4) + (fund_score * 0.4) + (sent_score * 0.2)
                candidate['composite_score'] = round(composite_score, 1)

                enriched_candidates.append(candidate)

            # Enrich holdings with sentiment (for Portfolio/CEO decision making)
            enriched_holdings = []
            for holding in holdings:
                ticker = holding['ticker']
                sent_info = sentiment_data.get(ticker, {})

                holding['sentiment'] = {
                    'score': sent_info.get('sentiment_score', 50.0),
                    'summary': sent_info.get('news_summary', 'No sentiment data available'),
                    'news_count': 1 if sent_info else 0
                }

                enriched_holdings.append(holding)

            # Calculate quality score based on sentiment data coverage
            total_stocks = len(all_tickers)
            scored_stocks = sum(1 for t in all_tickers if sentiment_data.get(t, {}).get('sentiment_score') is not None)
            coverage_rate = scored_stocks / total_stocks if total_stocks > 0 else 0
            quality_score = int(coverage_rate * 100)

            self.logger.info(f"  News stage completed:")
            self.logger.info(f"    - Sentiment coverage: {scored_stocks}/{total_stocks} ({coverage_rate*100:.1f}%)")
            self.logger.info(f"    - Quality score: {quality_score}/100")

            # Show top candidates with sentiment
            if enriched_candidates:
                top_3 = sorted(enriched_candidates, key=lambda x: x.get('composite_score', 0), reverse=True)[:3]
                self.logger.info(f"  Top candidates (with sentiment):")
                for c in top_3:
                    self.logger.info(f"    - {c['ticker']}: Composite {c.get('composite_score', 0):.1f}/100 (Sentiment: {c['sentiment']['score']:.1f})")

            success = coverage_rate >= 0.5  # At least 50% coverage required

            return WorkflowStageResult(
                stage='news',
                success=success,
                data={
                    'message_id': research_result.data.get('message_id'),  # Pass through for Risk
                    'candidates': enriched_candidates,
                    'current_holdings': enriched_holdings,
                    'sentiment_data': sentiment_data,
                    'coverage_rate': coverage_rate,
                    'total_stocks_scored': scored_stocks
                },
                message=f"News enriched {scored_stocks}/{total_stocks} stocks with sentiment",
                quality_score=quality_score,
                issues=[] if success else [f"Low sentiment coverage: {coverage_rate*100:.1f}%"]
            )

        except Exception as e:
            self.logger.error(f"  News stage FAILED: {e}", exc_info=True)
            return WorkflowStageResult(
                stage='news',
                success=False,
                data={},
                message=f"News failed: {str(e)}",
                quality_score=0,
                issues=[str(e)]
            )

    def _run_risk_stage(self, news_result: WorkflowStageResult) -> WorkflowStageResult:
        """Run Risk Department and validate output"""
        try:
            # Initialize Risk Department
            if not self._risk_dept:
                self.logger.info("  Initializing Risk Department...")

                # Risk Department uses default parameters (1% per trade, 5% portfolio heat)
                self._risk_dept = RiskDepartment(
                    max_risk_per_trade_pct=1.0,
                    max_portfolio_heat_pct=5.0
                )

            # Get enriched candidates from News stage
            candidates = news_result.data.get('candidates', [])

            if not candidates:
                raise ValueError("No candidates provided from News stage")

            # Get available capital (simple calculation for now)
            # TODO: Get from Alpaca or database
            available_capital = 100000.0  # Default $100K

            self.logger.info("  Calculating position sizes and risk metrics...")
            self.logger.info(f"  Available capital: ${available_capital:,.2f}")
            self.logger.info("  (Applying risk limits: 1% per trade, 5% portfolio heat...)")

            # Call Risk Department to assess candidates
            assessed_candidates = self._risk_dept.assess_candidates(candidates, available_capital)

            # Risk Department adds risk metrics to ALL candidates (advisory role)
            # No filtering - all candidates passed through with risk scores
            approved_candidates = assessed_candidates
            approved_count = len(approved_candidates)
            rejected_count = 0  # Risk v2.0 doesn't reject

            # Calculate quality metrics
            issues = []
            if approved_count < self.min_risk_approved:
                issues.append(f"Only {approved_count} candidates from Risk (minimum {self.min_risk_approved})")

            # Quality score based on average risk_score (0-100)
            if approved_candidates:
                avg_risk_score = sum(c.get('risk_score', 50) for c in approved_candidates) / len(approved_candidates)
                quality_score = int(avg_risk_score)
            else:
                quality_score = 0

            success = approved_count >= self.min_risk_approved

            self.logger.info(f"  Risk assessment completed: {approved_count} candidates with risk metrics")
            if approved_candidates:
                # Log top 3 by risk_score
                top_3 = sorted(approved_candidates, key=lambda x: x.get('risk_score', 0), reverse=True)[:3]
                self.logger.info(f"  Top risk scores (swing suitability):")
                for c in top_3:
                    ticker = c.get('ticker', 'N/A')
                    risk_score = c.get('risk_score', 0)
                    warnings = c.get('risk_warnings', [])
                    self.logger.info(f"    - {ticker}: {risk_score:.1f}/100 swing score, {len(warnings)} warnings")

            if issues:
                for issue in issues:
                    self.logger.warning(f"  ISSUE: {issue}")

            # Generate RiskAssessment message for Portfolio
            risk_msg_id = self._generate_risk_assessment_message(approved_candidates, available_capital)
            self.logger.info(f"  RiskAssessment message generated: {risk_msg_id}")

            return WorkflowStageResult(
                stage='risk',
                success=success,
                data={
                    'message_id': risk_msg_id,  # For Portfolio to read from outbox
                    'candidates': approved_candidates,  # All candidates with risk metrics added
                    'approved_count': approved_count,
                    'avg_risk_score': sum(c.get('risk_score', 0) for c in approved_candidates) / len(approved_candidates) if approved_candidates else 0
                },
                message=f"Risk assessed {approved_count} candidates (avg risk score {sum(c.get('risk_score', 0) for c in approved_candidates) / len(approved_candidates):.1f}/100)" if approved_candidates else f"Risk assessed {approved_count} candidates",
                quality_score=int(quality_score),
                issues=issues
            )

        except Exception as e:
            self.logger.error(f"  Risk stage FAILED: {e}", exc_info=True)
            return WorkflowStageResult(
                stage='risk',
                success=False,
                data={},
                message=f"Risk assessment failed: {str(e)}",
                quality_score=0,
                issues=[str(e)]
            )

    def _run_portfolio_stage(self, risk_result: WorkflowStageResult) -> WorkflowStageResult:
        """Run Portfolio Department and validate output"""
        try:
            # Initialize Portfolio Department
            if not self._portfolio_dept:
                self.logger.info("  Initializing Portfolio Department...")

                # Portfolio Department requires config_path and db_path
                config_path = self.config_dir / "portfolio_config.yaml"
                if not config_path.exists():
                    raise FileNotFoundError(f"Portfolio config not found: {config_path}")

                self._portfolio_dept = PortfolioDepartment(
                    config_path=config_path,
                    db_path=self.db_path
                )

            # Get Risk message and move to Portfolio inbox
            risk_msg_id = risk_result.data['message_id']
            risk_msg_path = self.messages_dir / "Outbox" / "RISK" / f"{risk_msg_id}.md"

            if not risk_msg_path.exists():
                raise FileNotFoundError(f"Risk message not found: {risk_msg_path}")

            # Copy to Portfolio inbox
            portfolio_inbox = self.messages_dir / "Inbox" / "PORTFOLIO"
            portfolio_inbox.mkdir(parents=True, exist_ok=True)

            import shutil
            shutil.copy(risk_msg_path, portfolio_inbox / risk_msg_path.name)

            # Run Portfolio Department (processes inbox)
            self.logger.info("  Applying portfolio constraints and making final selections...")
            self.logger.info("  (Checking position limits, capital limits, score thresholds...)")

            self._portfolio_dept.run_daily_cycle()

            # Read BuyOrder messages to see what Portfolio selected
            portfolio_outbox = self.messages_dir / "Outbox" / "PORTFOLIO"
            buy_orders = []

            if portfolio_outbox.exists():
                for msg_file in portfolio_outbox.glob("MSG_PORTFOLIO_*.md"):
                    try:
                        with open(msg_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Check if it's a BuyOrder message
                        if 'message_type: BuyOrder' in content or 'Order Type**: BUY' in content:
                            # Extract JSON payload
                            if '```json' in content:
                                json_start = content.find('```json') + 7
                                json_end = content.find('```', json_start)
                                json_str = content[json_start:json_end].strip()
                                data = json.loads(json_str)
                                buy_orders.append(data)

                    except Exception as e:
                        self.logger.warning(f"  Could not parse {msg_file.name}: {e}")

            approved_count = len(buy_orders)

            self.logger.info(f"  Portfolio decisions completed: {approved_count} BuyOrders generated")

            # Log the selected trades
            if buy_orders:
                self.logger.info(f"  Final selections:")
                for order in buy_orders[:5]:  # Show first 5
                    ticker = order.get('ticker', 'N/A')
                    shares = order.get('shares', 0)
                    self.logger.info(f"    - {ticker}: {shares} shares")

            issues = []
            if approved_count < self.min_portfolio_approved:
                issues.append(f"Only {approved_count} trades approved (minimum {self.min_portfolio_approved})")

            success = approved_count >= self.min_portfolio_approved

            # Quality score based on how many made it through
            approval_rate = approved_count / risk_result.data['approved_count'] if risk_result.data['approved_count'] > 0 else 0
            quality_score = min(100, int(approval_rate * 100))

            return WorkflowStageResult(
                stage='portfolio',
                success=success,
                data={
                    'buy_orders': buy_orders,
                    'approved_count': approved_count
                },
                message=f"Portfolio selected {approved_count} final trades (from {risk_result.data['approved_count']} candidates)",
                quality_score=int(quality_score),
                issues=issues
            )

        except Exception as e:
            self.logger.error(f"  Portfolio stage FAILED: {e}", exc_info=True)
            return WorkflowStageResult(
                stage='portfolio',
                success=False,
                data={},
                message=f"Portfolio decisions failed: {str(e)}",
                quality_score=0,
                issues=[str(e)]
            )

    def _run_gpt5_optimization_stage(self, news_result: WorkflowStageResult) -> WorkflowStageResult:
        """
        Run Deterministic Portfolio Allocator (GPT optimizer disabled)

        This stage receives ALL scored stocks from News (candidates + holdings)
        and creates a trading plan using pure deterministic logic:
        - SELL: Holdings below rank threshold or score < 60 (quality floor)
        - BUY: Top-ranked candidates scoring 60+ to fill open slots
        - ALLOCATION: Equal-weight across new positions

        Note: GPT-4o-mini optimizer code preserved but commented out for potential future use.
        """
        try:
            # COMMENTED OUT: GPT optimizer initialization (no longer needed in deterministic mode)
            # if not self._gpt5_optimizer:
            #     selected_model = getattr(self, 'ai_model', 'gpt-4o-mini')
            #     self.logger.info(f"  Initializing Portfolio Optimizer (OpenAI {selected_model})...")
            #     import config as app_config
            #     self._gpt5_optimizer = GPT5PortfolioOptimizer(
            #         api_key=app_config.OPENAI_API_KEY,
            #         model=selected_model
            #     )

            # Set display name for logging
            model_display = "DETERMINISTIC"

            # Get ALL stocks from News stage (candidates + holdings with scores/sentiment)
            candidates = news_result.data.get('candidates', [])
            holdings = news_result.data.get('current_holdings', [])

            if not candidates:
                raise ValueError("No candidates from News stage to optimize")

            # Filter out candidates with PENDING orders to prevent duplicates
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT ticker FROM portfolio_positions WHERE status = 'PENDING'")
            pending_tickers = {row[0] for row in cursor.fetchall()}
            conn.close()

            original_count = len(candidates)
            if pending_tickers:
                candidates = [c for c in candidates if c.get('ticker') not in pending_tickers]
                filtered_count = original_count - len(candidates)
                if filtered_count > 0:
                    self.logger.info(f"  Filtered {filtered_count} candidates with PENDING orders: {', '.join(sorted(pending_tickers))}")

            self.logger.info(f"  {model_display} analyzing complete portfolio:")
            self.logger.info(f"    - {len(candidates)} buy candidates (with scores & sentiment)")
            self.logger.info(f"    - {len(holdings)} current holdings (with scores & sentiment)")
            self.logger.info(f"    - Total stocks under consideration: {len(candidates) + len(holdings)}")

            # ============================================================================
            # MARKET REGIME ANALYSIS - Active Strategy Adjustment
            # ============================================================================
            # Fetch latest market regime assessment and adjust strategy parameters

            regime_info = self._get_latest_regime_assessment()

            if regime_info:
                regime = regime_info.get('regime', 'NEUTRAL')
                confidence = regime_info.get('confidence', 'MEDIUM')
                vix_level = regime_info.get('vix_level', 20.0)

                self.logger.info("")
                self.logger.info("=" * 80)
                self.logger.info("  MARKET REGIME ASSESSMENT (ACTIVE MODE)")
                self.logger.info("=" * 80)
                self.logger.info(f"  Regime: {regime} (Confidence: {confidence})")
                self.logger.info(f"  VIX Level: {vix_level:.1f}")
                self.logger.info(f"  SPY Change: {regime_info.get('spy_change_pct', 0):.2f}%")
                self.logger.info("")

                # Adjust strategy based on regime
                if regime == 'BEARISH' and confidence == 'HIGH':
                    # High-confidence bearish: Defensive posture
                    TARGET_PORTFOLIO_SIZE = 15
                    POSITION_SIZE_MULTIPLIER = 0.6  # Smaller positions
                    self.logger.warning("  BEARISH REGIME (HIGH CONFIDENCE) → Defensive Mode")
                    self.logger.warning(f"    - Target positions: 15 (reduced from 28)")
                    self.logger.warning(f"    - Position sizing: 60% of normal")

                elif regime == 'BEARISH':
                    # Medium/low-confidence bearish: Moderate caution
                    TARGET_PORTFOLIO_SIZE = 20
                    POSITION_SIZE_MULTIPLIER = 0.75
                    self.logger.info("  BEARISH REGIME → Cautious Mode")
                    self.logger.info(f"    - Target positions: 20 (reduced from 28)")
                    self.logger.info(f"    - Position sizing: 75% of normal")

                elif regime == 'BULLISH' and vix_level < 15:
                    # Low volatility bull market: Slightly aggressive
                    TARGET_PORTFOLIO_SIZE = 28
                    POSITION_SIZE_MULTIPLIER = 1.1  # Slightly larger positions
                    self.logger.info("  BULLISH REGIME + LOW VIX → Aggressive Mode")
                    self.logger.info(f"    - Target positions: 28 (full deployment)")
                    self.logger.info(f"    - Position sizing: 110% of normal")

                else:
                    # NEUTRAL or normal BULLISH: Standard strategy
                    TARGET_PORTFOLIO_SIZE = 28
                    POSITION_SIZE_MULTIPLIER = 1.0
                    self.logger.info("  NEUTRAL/NORMAL REGIME → Standard Mode")
                    self.logger.info(f"    - Target positions: 28")
                    self.logger.info(f"    - Position sizing: 100% (normal)")

                self.logger.info("=" * 80)
                self.logger.info("")
            else:
                # No regime data available - use defaults
                TARGET_PORTFOLIO_SIZE = 28
                POSITION_SIZE_MULTIPLIER = 1.0
                self.logger.warning("  No regime data available - using default parameters")
                self.logger.info("")

            # ============================================================================
            # COMPARATIVE RANKING ANALYSIS (Option B Implementation)
            # ============================================================================
            # Compare all holdings vs candidates to determine optimal portfolio composition
            # Philosophy: Portfolio should hold the top N stocks by score (N adjusted by regime)

            ABSOLUTE_SCORE_FLOOR = 60   # Never hold anything below this score (quality threshold)

            mandatory_sells = []
            holdings_to_keep = []

            if holdings:
                self.logger.info("")
                self.logger.info("=" * 80)
                self.logger.info("  COMPARATIVE RANKING ANALYSIS")
                self.logger.info("=" * 80)
                self.logger.info(f"  Quality threshold: {ABSOLUTE_SCORE_FLOOR} (only buy/hold stocks scoring {ABSOLUTE_SCORE_FLOOR}+)")
                self.logger.info("")

                # Step 1: Combine all holdings + candidates into unified ranking
                all_stocks = []

                # Add current holdings
                for holding in holdings:
                    ticker = holding.get('ticker')
                    score = holding.get('research_composite_score', holding.get('composite_score', 50))
                    unrealized_plpc = holding.get('unrealized_plpc', 0)
                    market_value = holding.get('market_value', 0)
                    days_held = self.realism_sim.calculate_days_held(ticker)

                    all_stocks.append({
                        'ticker': ticker,
                        'composite_score': score,
                        'type': 'HOLDING',
                        'market_value': market_value,
                        'unrealized_plpc': unrealized_plpc,
                        'days_held': days_held,
                        'data': holding
                    })

                # Add new candidates
                for candidate in candidates:
                    ticker = candidate.get('ticker')
                    score = candidate.get('composite_score', candidate.get('research_composite_score', 0))

                    all_stocks.append({
                        'ticker': ticker,
                        'composite_score': score,
                        'type': 'CANDIDATE',
                        'data': candidate
                    })

                # Step 2: Sort by composite score (highest first)
                all_stocks.sort(key=lambda x: x['composite_score'], reverse=True)

                # Step 3: Analyze ranking and identify swaps needed
                self.logger.info(f"  Total universe: {len(all_stocks)} stocks ({len(holdings)} holdings + {len(candidates)} candidates)")
                self.logger.info(f"  Target portfolio size: {TARGET_PORTFOLIO_SIZE} positions")
                self.logger.info(f"  Absolute score floor: {ABSOLUTE_SCORE_FLOOR} (never hold below this)")
                self.logger.info("")

                # Determine keeper threshold
                keeper_threshold_rank = TARGET_PORTFOLIO_SIZE

                # Log top performers and identify actions needed
                self.logger.info("  TOP 30 RANKED STOCKS:")
                self.logger.info("  " + "-" * 76)
                self.logger.info(f"  {'Rank':<6} {'Ticker':<8} {'Score':<8} {'Type':<12} {'Action':<20}")
                self.logger.info("  " + "-" * 76)

                holdings_in_top_n = 0
                candidates_in_top_n = 0
                holdings_below_threshold = []

                for i, stock in enumerate(all_stocks[:30]):  # Show top 30 for visibility
                    rank = i + 1
                    ticker = stock['ticker']
                    score = stock['composite_score']
                    stock_type = stock['type']

                    # Determine action based on rank and type
                    if rank <= keeper_threshold_rank:
                        if stock_type == 'HOLDING':
                            action = "✓ KEEP (top performer)"
                            holdings_in_top_n += 1
                        else:
                            action = "→ BUY (top opportunity)"
                            candidates_in_top_n += 1
                    else:
                        if stock_type == 'HOLDING':
                            action = "✗ SELL (below threshold)"
                            holdings_below_threshold.append(stock)
                        else:
                            action = "- Pass (not in top 28)"

                    # Check absolute floor
                    if stock_type == 'HOLDING' and score < ABSOLUTE_SCORE_FLOOR:
                        action = f"✗ SELL (score < {ABSOLUTE_SCORE_FLOOR})"
                        if stock not in holdings_below_threshold:
                            holdings_below_threshold.append(stock)

                    self.logger.info(f"  {rank:<6} {ticker:<8} {score:<8.1f} {stock_type:<12} {action:<20}")

                self.logger.info("  " + "-" * 76)
                self.logger.info("")

                # Step 4: Process holdings for mandatory sells
                self.logger.info("  POSITION QUALITY CHECK:")
                self.logger.info("")

                for holding in holdings:
                    ticker = holding.get('ticker')
                    score = holding.get('research_composite_score', holding.get('composite_score', 50))
                    unrealized_plpc = holding.get('unrealized_plpc', 0)
                    days_held = self.realism_sim.calculate_days_held(ticker)

                    # Find this holding's rank
                    holding_rank = next((i+1 for i, s in enumerate(all_stocks) if s['ticker'] == ticker), None)

                    # Determine if this position MUST be sold
                    must_sell = False
                    sell_reason = None

                    # Rule 1: Score below absolute floor
                    if score < ABSOLUTE_SCORE_FLOOR:
                        must_sell = True
                        sell_reason = f"Score {score:.1f} < {ABSOLUTE_SCORE_FLOOR} absolute minimum"

                    # Rule 2: Ranked below keeper threshold (fell out of top 28)
                    elif holding_rank is not None and holding_rank > keeper_threshold_rank:
                        must_sell = True
                        sell_reason = f"Rank #{holding_rank} (below top {keeper_threshold_rank}), score {score:.1f}"

                    if must_sell:
                        self.logger.warning(f"    ❌ {ticker}: MANDATORY SELL - {sell_reason}")
                        holding['MANDATORY_SELL'] = True
                        holding['MANDATORY_SELL_REASON'] = sell_reason
                        mandatory_sells.append(ticker)
                    else:
                        rank_display = f"Rank #{holding_rank}" if holding_rank else "Not ranked"
                        self.logger.info(f"    ✓ {ticker}: KEEP - {rank_display}, Score {score:.1f}, P&L {unrealized_plpc:+.1f}%")
                        holdings_to_keep.append(ticker)

                self.logger.info("")
                self.logger.info(f"  SUMMARY:")
                self.logger.info(f"    Holdings in top {keeper_threshold_rank}: {holdings_in_top_n}")
                self.logger.info(f"    Candidates in top {keeper_threshold_rank}: {candidates_in_top_n}")
                self.logger.info(f"    Holdings to sell (below threshold): {len(mandatory_sells)}")
                self.logger.info(f"    Open slots for new positions: {len(mandatory_sells)}")

                if mandatory_sells:
                    self.logger.warning(f"  MANDATORY SELLS: {', '.join(mandatory_sells)}")
                else:
                    self.logger.info(f"  All {len(holdings)} holdings are top performers - no sells needed")

                self.logger.info("=" * 80)
                self.logger.info("")

            self.logger.info(f"  ({model_display} will decide which to BUY, which to SELL, and allocation amounts...)")
            if mandatory_sells:
                self.logger.info(f"  ({len(mandatory_sells)} holdings flagged as MANDATORY SELL)")

            # Get portfolio state and market conditions from News result
            market_conditions = news_result.data.get('market_conditions', {
                'spy_change_pct': 0.0,
                'vix_level': 20.0,
                'market_sentiment': 'NEUTRAL'
            })

            # Get REAL buying power from Alpaca (ground truth)
            try:
                from Utils.alpaca_client import AlpacaClient
                alpaca = AlpacaClient()
                account = alpaca.trading_client.get_account()
                buying_power = float(account.buying_power)
                self.logger.info(f"  Alpaca buying power: ${buying_power:,.2f}")
            except Exception as e:
                self.logger.warning(f"  Could not fetch Alpaca buying power: {e}")
                buying_power = 100000.0  # Fallback
                self.logger.info(f"  Using fallback capital: ${buying_power:,.2f}")

            # CRITICAL FIX: Calculate proceeds from MANDATORY sells
            # These positions MUST be sold, so their proceeds are guaranteed capital
            mandatory_sell_proceeds = 0.0
            for holding in holdings:
                if holding.get('MANDATORY_SELL'):
                    proceeds = holding.get('market_value', 0)
                    mandatory_sell_proceeds += proceeds
                    self.logger.info(f"    {holding.get('ticker')}: +${proceeds:,.2f} from mandatory sell")

            # Total available capital = buying power + guaranteed sell proceeds
            available_capital = buying_power + mandatory_sell_proceeds

            if mandatory_sell_proceeds > 0:
                self.logger.info(f"  Mandatory sell proceeds: ${mandatory_sell_proceeds:,.2f}")
                self.logger.info(f"  Total available capital: ${available_capital:,.2f} (buying power + sell proceeds)")
            else:
                self.logger.info(f"  Total available capital: ${available_capital:,.2f} (no mandatory sells)")

            current_positions = len(holdings)
            max_positions = 20

            # ============================================================================
            # GPT OPTIMIZER (DISABLED - COMMENTED OUT FOR DETERMINISTIC MODE)
            # ============================================================================
            # Reason: GPT-4o-mini was making poor decisions (selling high-scoring holdings,
            # hallucinating facts). Replaced with deterministic logic that strictly follows
            # comparative ranking. GPT code preserved for potential future use in:
            # - Report generation / narrative synthesis
            # - Risk assessment commentary
            # - User-facing explanations
            # ============================================================================

            # COMMENTED OUT: GPT optimizer call
            # optimized_candidates, reasoning = self._gpt5_optimizer.optimize_portfolio(
            #     candidates=candidates,
            #     holdings=holdings,
            #     available_capital=available_capital,
            #     market_conditions=market_conditions,
            #     current_positions=current_positions,
            #     max_positions=max_positions
            # )

            # ============================================================================
            # DETERMINISTIC ALLOCATION (ACTIVE)
            # ============================================================================
            # Pure logic-based allocation following comparative ranking
            # No AI hallucinations, no overrides, just clean ranking-based decisions

            self.logger.info("")
            self.logger.info("  Using deterministic allocation (comparative ranking only)")

            # Step 1: Determine how many positions to add
            # IMPORTANT: Exclude untradeable positions (mergers, halts) from active count
            tradeable_holdings = [h for h in holdings if h.get('tradeable', True)]
            untradeable_holdings = [h for h in holdings if not h.get('tradeable', True)]

            if untradeable_holdings:
                self.logger.warning(f"  {len(untradeable_holdings)} FROZEN positions (not counted against limit):")
                for h in untradeable_holdings:
                    self.logger.warning(f"    - {h['ticker']}: ${h.get('market_value', 0):,.2f} (status: {h.get('asset_status', 'UNKNOWN')})")

            holdings_to_keep_count = len([h for h in tradeable_holdings if not h.get('MANDATORY_SELL', False)])
            open_slots = TARGET_PORTFOLIO_SIZE - holdings_to_keep_count

            self.logger.info(f"  Tradeable holdings to keep: {holdings_to_keep_count}")
            self.logger.info(f"  Open slots for new positions: {open_slots}")

            # Step 2: Select top candidates by rank to fill open slots
            # Candidates are already sorted by rank in comparative ranking
            optimized_candidates = []

            if open_slots > 0:
                # Take top N candidates that aren't already held AND meet quality threshold
                held_tickers = {h['ticker'] for h in holdings}
                available_candidates = [
                    c for c in candidates
                    if c['ticker'] not in held_tickers
                    and c.get('composite_score', 0) >= ABSOLUTE_SCORE_FLOOR
                ]

                # Sort by composite score (descending)
                available_candidates.sort(key=lambda x: -x.get('composite_score', 0))

                # Select top candidates to fill slots (may be fewer than open_slots if quality is scarce)
                selected_candidates = available_candidates[:open_slots]

                if len(selected_candidates) < open_slots:
                    self.logger.warning(f"  Only {len(selected_candidates)} candidates meet quality threshold (score ≥ {ABSOLUTE_SCORE_FLOOR})")
                    self.logger.warning(f"  Will leave {open_slots - len(selected_candidates)} slots unfilled rather than buy low-quality stocks")

                # Step 3: Equal-weight allocation across selected candidates
                if len(selected_candidates) > 0:
                    # Load compliance position sizing limits
                    import yaml
                    compliance_config_path = self.project_root / "Config" / "compliance_config.yaml"
                    try:
                        with open(compliance_config_path) as f:
                            compliance_cfg = yaml.safe_load(f)
                        max_position_value = compliance_cfg['position_sizing'].get('max_position_value', 50000)
                        max_position_pct = compliance_cfg['position_sizing'].get('max_position_pct', 0.10)
                    except Exception as e:
                        self.logger.warning(f"  Could not load compliance limits: {e}, using defaults")
                        max_position_value = 50000
                        max_position_pct = 0.10

                    # Calculate max position size (smaller of absolute limit or percentage limit)
                    max_position_from_pct = available_capital * max_position_pct
                    max_allowed_position = min(max_position_value, max_position_from_pct)

                    # Calculate equal-weight per position, capped at compliance limits
                    capital_per_position = available_capital / len(selected_candidates)
                    capital_per_position = min(capital_per_position, max_allowed_position)

                    self.logger.info(f"  Position sizing limits: ${max_position_value:,.0f} absolute, {max_position_pct:.0%} of portfolio (${max_position_from_pct:,.0f})")
                    self.logger.info(f"  Max allowed per position: ${max_allowed_position:,.0f}")

                    for candidate in selected_candidates:
                        entry_price = candidate.get('current_price', candidate.get('entry_price', 0))
                        if entry_price <= 0:
                            continue

                        allocated_capital = capital_per_position
                        shares = int(allocated_capital / entry_price)

                        if shares > 0:
                            candidate['allocated_capital'] = allocated_capital
                            optimized_candidates.append(candidate)

                    self.logger.info(f"  Selected {len(optimized_candidates)} candidates (equal-weight: ${capital_per_position:,.2f} each)")
                else:
                    self.logger.info("  No candidates available for purchase")
            else:
                self.logger.info("  Portfolio is full - no new positions needed")

            # Calculate metrics
            total_allocated = sum(c.get('allocated_capital', 0) for c in optimized_candidates)
            capital_deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0

            self.logger.info(f"  Capital Deployment: ${total_allocated:,.2f} / ${available_capital:,.2f} ({capital_deployment_pct:.1f}%)")

            reasoning = "Deterministic allocation: Top-ranked candidates selected by comparative ranking system, equal-weighted."

            # Build buy orders and sell orders from deterministic allocation
            buy_orders = []
            sell_orders = []

            for candidate in optimized_candidates:
                ticker = candidate['ticker']
                allocated_capital = candidate.get('allocated_capital', 0)

                if allocated_capital > 0:
                    # This is a BUY
                    entry_price = candidate.get('current_price', candidate.get('entry_price', 0))
                    shares = int(allocated_capital / entry_price) if entry_price > 0 else 0

                    buy_order = {
                        'ticker': ticker,
                        'action': 'BUY',
                        'shares': shares,
                        'allocated_capital': allocated_capital,
                        'entry_price': entry_price,
                        'composite_score': candidate.get('composite_score', 0),
                        'sentiment_score': candidate.get('sentiment', {}).get('score', 50),
                        'sentiment_summary': candidate.get('sentiment', {}).get('summary', 'No data'),
                        'sector': candidate.get('sector', 'Unknown'),
                        'gpt5_reasoning': candidate.get('gpt5_reasoning', 'Selected by GPT-5'),
                        'gpt5_allocated': True,
                        'is_position_adjustment': candidate.get('is_position_adjustment', False)
                    }
                    buy_orders.append(buy_order)

            # ============================================================================
            # APPLY REGIME-BASED POSITION SIZING
            # ============================================================================
            # Adjust position sizes based on market regime

            if 'POSITION_SIZE_MULTIPLIER' in locals() and POSITION_SIZE_MULTIPLIER != 1.0:
                self.logger.info("")
                self.logger.info(f"  Applying regime-based position sizing: {POSITION_SIZE_MULTIPLIER:.0%} of normal")

                for order in buy_orders:
                    old_capital = order['allocated_capital']
                    new_capital = old_capital * POSITION_SIZE_MULTIPLIER
                    order['allocated_capital'] = new_capital

                    # Recalculate shares
                    entry_price = order['entry_price']
                    order['shares'] = int(new_capital / entry_price) if entry_price > 0 else 0

                    self.logger.debug(f"    {order['ticker']}: ${old_capital:,.0f} → ${new_capital:,.0f} ({order['shares']} shares)")

                # Recalculate total
                total_allocated = sum(o['allocated_capital'] for o in buy_orders)
                self.logger.info(f"  Adjusted total allocation: ${total_allocated:,.2f}")
                self.logger.info("")

            # ============================================================================
            # PROCESS SELL DECISIONS (GPT-5 + Mandatory Automated Exits)
            # ============================================================================

            # First: Process MANDATORY automated exits (always execute these)
            mandatory_sell_tickers = set()
            for holding in holdings:
                if holding.get('MANDATORY_SELL'):
                    ticker = holding.get('ticker')
                    mandatory_sell_tickers.add(ticker)

                    self.logger.warning(f"  Enforcing MANDATORY SELL: {ticker}")
                    sell_order = {
                        'ticker': ticker,
                        'action': 'SELL',
                        'shares': holding.get('quantity', 0),
                        'sell_pct': 100,
                        'composite_score': holding.get('research_composite_score', holding.get('composite_score', 0)),
                        'current_price': holding.get('current_price', 0),
                        'sentiment_score': holding.get('sentiment_score', holding.get('sentiment', {}).get('score', 50)),
                        'sentiment_summary': holding.get('sentiment_summary', holding.get('sentiment', {}).get('summary', 'No data')),
                        'gpt5_reasoning': f'AUTOMATED EXIT: {holding.get("MANDATORY_SELL_REASON")}',
                        'current_value': holding.get('market_value', 0)
                    }
                    sell_orders.append(sell_order)

            # Second: Process GPT-5's explicit SELL decisions (DISABLED IN DETERMINISTIC MODE)
            # COMMENTED OUT: GPT sell recommendations
            # In deterministic mode, we only sell based on comparative ranking (MANDATORY_SELL flag)
            # No AI override of ranking decisions

            # gpt5_sell_decisions = []
            # if optimized_candidates and len(optimized_candidates) > 0:
            #     gpt5_sell_decisions = optimized_candidates[0].get('gpt5_sell_decisions', [])
            #
            # if gpt5_sell_decisions:
            #     self.logger.info(f"  Processing {model_display}'s {len(gpt5_sell_decisions)} SELL recommendations")
            #     [... GPT sell validation code omitted ...]
            #     sell_orders.append(sell_order)

            # DETERMINISTIC MODE: Only mandatory sells (already processed above)

            # Third: Fallback safety check for any remaining underperformers
            # (Should be unnecessary since comparative ranking catches everything, but kept as safeguard)
            if not mandatory_sell_tickers:
                self.logger.info(f"  No mandatory sells - checking for any stragglers below score threshold")
                for holding in holdings:
                    ticker = holding.get('ticker')
                    composite = holding.get('research_composite_score', holding.get('composite_score', 0))

                    # Only sell if score is genuinely poor (< 60) AND not already processed
                    if composite < ABSOLUTE_SCORE_FLOOR and ticker not in mandatory_sell_tickers:
                        self.logger.warning(f"  Fallback auto-sell: {ticker} (score: {composite:.1f} < {ABSOLUTE_SCORE_FLOOR} threshold)")
                        sell_order = {
                            'ticker': ticker,
                            'action': 'SELL',
                            'shares': holding.get('quantity', 0),
                            'sell_pct': 100,
                            'composite_score': composite,
                            'current_price': holding.get('current_price', 0),
                            'sentiment_score': holding.get('sentiment_score', holding.get('sentiment', {}).get('score', 50)),
                            'sentiment_summary': holding.get('sentiment_summary', holding.get('sentiment', {}).get('summary', 'No data')),
                            'gpt5_reasoning': f'Fallback automatic sell: Score {composite:.1f} below {ABSOLUTE_SCORE_FLOOR} threshold',
                            'current_value': holding.get('market_value', 0)
                        }
                        sell_orders.append(sell_order)
                        mandatory_sell_tickers.add(ticker)  # Track to avoid duplicates
                    elif composite >= ABSOLUTE_SCORE_FLOOR:
                        self.logger.info(f"  Keeping {ticker} (score: {composite:.1f} ≥ {ABSOLUTE_SCORE_FLOOR} threshold)")

            # Fourth: Process externally-injected mandatory sells (e.g., position drift trims)
            if self.mandatory_sells:
                self.logger.info(f"  Processing {len(self.mandatory_sells)} externally-injected mandatory sell(s)")
                for ext_sell in self.mandatory_sells:
                    ticker = ext_sell.get('ticker')
                    shares_to_sell = ext_sell.get('shares', 0)

                    # Skip if already being sold
                    if ticker in mandatory_sell_tickers:
                        self.logger.info(f"    Skipping {ticker} - already in sell orders")
                        continue

                    # Find the holding to get current price
                    holding = next((h for h in holdings if h.get('ticker') == ticker), None)
                    if holding:
                        current_price = holding.get('current_price', 0)
                        current_shares = holding.get('quantity', 0)

                        # Don't sell more than we have
                        actual_shares = min(shares_to_sell, current_shares)

                        if actual_shares > 0:
                            self.logger.warning(f"    DRIFT TRIM: {ticker} - SELL {actual_shares} of {current_shares} shares")
                            sell_order = {
                                'ticker': ticker,
                                'action': 'SELL',
                                'shares': actual_shares,
                                'sell_pct': int((actual_shares / current_shares) * 100) if current_shares > 0 else 100,
                                'composite_score': holding.get('research_composite_score', holding.get('composite_score', 0)),
                                'current_price': current_price,
                                'sentiment_score': holding.get('sentiment_score', 50),
                                'sentiment_summary': 'Position drift trim',
                                'gpt5_reasoning': ext_sell.get('reason', 'Position exceeds size limit - trimming'),
                                'current_value': actual_shares * current_price,
                                'source': ext_sell.get('source', 'position_drift_monitor')
                            }
                            sell_orders.append(sell_order)
                            mandatory_sell_tickers.add(ticker)
                    else:
                        self.logger.warning(f"    Cannot find holding for {ticker} - skipping drift trim")

            total_orders = len(buy_orders) + len(sell_orders)
            self.logger.info(f"  Trading Plan: {len(sell_orders)} SELLs, {len(buy_orders)} BUYs")

            # ============================================================================
            # VALIDATION: CHECK FOR OVER-ALLOCATION (CRITICAL BUG PREVENTION)
            # ============================================================================
            MAX_DEPLOYMENT_PCT = 105.0  # Allow 5% overage for rounding, but no more

            if capital_deployment_pct > MAX_DEPLOYMENT_PCT:
                self.logger.error("=" * 80)
                self.logger.error("CRITICAL ERROR: GPT OVER-ALLOCATED CAPITAL")
                self.logger.error("=" * 80)
                self.logger.error(f"  Requested: ${total_allocated:,.2f}")
                self.logger.error(f"  Available: ${available_capital:,.2f}")
                self.logger.error(f"  Over-allocation: {capital_deployment_pct:.1f}% (max: {MAX_DEPLOYMENT_PCT}%)")
                self.logger.error(f"  Shortfall: ${total_allocated - available_capital:,.2f}")
                self.logger.error("")
                self.logger.error("  This plan CANNOT be executed - insufficient funds!")
                self.logger.error("  Scaling down all positions proportionally...")

                # Scale down all positions to fit within available capital
                scale_factor = (available_capital * 0.95) / total_allocated  # Use 95% to be safe
                self.logger.error(f"  Applying scale factor: {scale_factor:.3f}")

                for order in buy_orders:
                    old_capital = order['allocated_capital']
                    new_capital = old_capital * scale_factor
                    order['allocated_capital'] = new_capital

                    # Recalculate shares
                    entry_price = order['entry_price']
                    order['shares'] = int(new_capital / entry_price) if entry_price > 0 else 0

                    self.logger.error(f"    {order['ticker']}: ${old_capital:,.0f} → ${new_capital:,.0f} ({order['shares']} shares)")

                # Recalculate totals after scaling
                total_allocated = sum(o['allocated_capital'] for o in buy_orders)
                capital_deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0
                self.logger.error(f"  After scaling: ${total_allocated:,.2f} ({capital_deployment_pct:.1f}%)")
                self.logger.error("=" * 80)

            # ============================================================================
            # TIER 1 FIX: CAPITAL DEPLOYMENT VALIDATION (90% MINIMUM)
            # ============================================================================
            # This is a CRITICAL profitability improvement - idle capital earns nothing!
            #
            # Problem: GPT-4o was only selecting 5 positions ($33K of $100K = 33% deployed)
            # Impact: 67% of capital sitting idle = massive profit opportunity loss
            # Fix: Enforce 90% minimum deployment OR auto-fill with next-best candidates

            MIN_DEPLOYMENT_PCT = 90.0
            MIN_POSITIONS = 12  # Reduced from 15 to allow some flexibility

            # Calculate final position count after all trades execute
            positions_after_trades = current_positions - len(sell_orders) + len(buy_orders)

            # Check if plan meets minimum standards
            deployment_ok = capital_deployment_pct >= MIN_DEPLOYMENT_PCT
            diversification_ok = len(buy_orders) >= MIN_POSITIONS

            if not deployment_ok or not diversification_ok:
                self.logger.warning("=" * 80)
                self.logger.warning("CAPITAL DEPLOYMENT VALIDATION FAILED")
                self.logger.warning("=" * 80)
                self.logger.warning(f"  Current deployment: {capital_deployment_pct:.1f}% (minimum: {MIN_DEPLOYMENT_PCT}%)")
                self.logger.warning(f"  New BUY positions: {len(buy_orders)} (minimum: {MIN_POSITIONS})")
                self.logger.warning(f"  Total positions after trades: {positions_after_trades}")
                self.logger.warning("")
                self.logger.warning(f"  This plan would leave ${available_capital - total_allocated:,.0f} idle!")
                self.logger.warning("  Idle capital = lost profit opportunity.")
                self.logger.warning("")
                self.logger.warning("  AUTO-CORRECTION: Adding next-highest-scoring candidates...")

                # Auto-fill with next-best candidates to reach 90% deployment
                # Sort candidates by composite score (descending)
                selected_tickers = {order['ticker'] for order in buy_orders}
                remaining_candidates = [
                    c for c in candidates
                    if c['ticker'] not in selected_tickers and c.get('composite_score', 0) >= ABSOLUTE_SCORE_FLOOR
                ]
                remaining_candidates.sort(key=lambda x: -x.get('composite_score', 0))

                remaining_capital = available_capital - total_allocated
                target_deployment = available_capital * (MIN_DEPLOYMENT_PCT / 100.0)
                capital_needed = target_deployment - total_allocated

                # Load compliance config to get position sizing limits
                import yaml
                compliance_config_path = self.project_root / "Config" / "compliance_config.yaml"
                MIN_POSITION_VALUE = 500  # Default fallback
                MAX_POSITION_VALUE = 50000  # Default fallback
                MAX_POSITION_PCT = 0.10  # Default fallback
                try:
                    with open(compliance_config_path) as f:
                        compliance_cfg = yaml.safe_load(f)
                        position_sizing = compliance_cfg.get('position_sizing', {})
                        MIN_POSITION_VALUE = position_sizing.get('min_position_value', 500)
                        MAX_POSITION_VALUE = position_sizing.get('max_position_value', 50000)
                        MAX_POSITION_PCT = position_sizing.get('max_position_pct', 0.10)
                except Exception as e:
                    self.logger.warning(f"Could not load compliance config, using defaults")

                # Calculate max allowed position (smaller of absolute or percentage limit)
                max_position_from_pct = available_capital * MAX_POSITION_PCT
                max_allowed_position = min(MAX_POSITION_VALUE, max_position_from_pct)

                added_count = 0
                skipped_count = 0
                for candidate in remaining_candidates:
                    if total_allocated >= target_deployment:
                        break
                    if len(buy_orders) >= 30:  # Hard cap at 30 positions (raised from 20)
                        break

                    # Calculate position size (aim for equal weighting of remaining capital)
                    positions_to_add = min(MIN_POSITIONS - len(buy_orders), len(remaining_candidates))
                    if positions_to_add <= 0:
                        break

                    position_size = min(
                        capital_needed / positions_to_add,  # Equal distribution
                        max_allowed_position  # But never more than compliance max
                    )

                    entry_price = candidate.get('current_price', candidate.get('entry_price', 0))
                    if entry_price <= 0:
                        continue

                    # Calculate shares needed to meet MINIMUM position size
                    import math
                    min_shares = math.ceil(MIN_POSITION_VALUE / entry_price) if entry_price > 0 else 0
                    shares = max(min_shares, int(position_size / entry_price))

                    if shares == 0:
                        continue

                    allocated = shares * entry_price

                    # VALIDATION: Skip if position would be below minimum OR above compliance max
                    if allocated < MIN_POSITION_VALUE:
                        self.logger.debug(f"    - Skipped {candidate['ticker']}: ${allocated:,.0f} < ${MIN_POSITION_VALUE} minimum")
                        skipped_count += 1
                        continue

                    if allocated > max_allowed_position:
                        self.logger.debug(f"    - Skipped {candidate['ticker']}: ${allocated:,.0f} > ${max_allowed_position:,.0f} maximum")
                        skipped_count += 1
                        continue

                    buy_order = {
                        'ticker': candidate['ticker'],
                        'action': 'BUY',
                        'shares': shares,
                        'allocated_capital': allocated,
                        'entry_price': entry_price,
                        'composite_score': candidate.get('composite_score', 0),
                        'sentiment_score': candidate.get('sentiment', {}).get('score', 50),
                        'sentiment_summary': candidate.get('sentiment', {}).get('summary', 'No data'),
                        'sector': candidate.get('sector', 'Unknown'),
                        'gpt5_reasoning': f'Auto-added for capital efficiency (score: {candidate.get("composite_score", 0):.1f})',
                        'gpt5_allocated': False,  # Mark as auto-added
                        'is_position_adjustment': False
                    }
                    buy_orders.append(buy_order)
                    total_allocated += allocated
                    added_count += 1
                    selected_tickers.add(candidate['ticker'])

                    self.logger.info(f"    + Added {candidate['ticker']} (score: {candidate.get('composite_score', 0):.1f}): ${allocated:,.0f}")

                # Recalculate metrics
                capital_deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0
                positions_after_trades = current_positions - len(sell_orders) + len(buy_orders)

                self.logger.warning("")
                self.logger.warning(f"  AUTO-CORRECTION COMPLETE:")
                self.logger.warning(f"    - Added {added_count} positions")
                if skipped_count > 0:
                    self.logger.warning(f"    - Skipped {skipped_count} candidates (position size constraints)")
                self.logger.warning(f"    - New deployment: {capital_deployment_pct:.1f}%")
                self.logger.warning(f"    - New BUY positions: {len(buy_orders)}")
                self.logger.warning(f"    - Total positions after trades: {positions_after_trades}")
                self.logger.warning(f"    - Remaining idle capital: ${available_capital - total_allocated:,.0f}")
                self.logger.warning("=" * 80)

            # Quality score based on deployment and diversification
            quality_score = min(100, int(
                (capital_deployment_pct / 90.0 * 70) +  # 70% weight on deployment
                (min(len(buy_orders) / 15.0, 1.0) * 30)  # 30% weight on diversification (target 15)
            ))

            # Recalculate final position count one more time (in case auto-correction changed it)
            positions_after_trades = current_positions - len(sell_orders) + len(buy_orders)

            issues = []
            if capital_deployment_pct < MIN_DEPLOYMENT_PCT:
                issues.append(f"Capital deployment {capital_deployment_pct:.1f}% (target {MIN_DEPLOYMENT_PCT}%+)")
            if len(buy_orders) < MIN_POSITIONS:
                issues.append(f"Limited diversification: {len(buy_orders)} new positions (target {MIN_POSITIONS}-20). Total after trades: {positions_after_trades}")

            success = total_orders > 0

            return WorkflowStageResult(
                stage='portfolio_allocator',
                success=success,
                data={
                    'buy_orders': buy_orders,
                    'sell_orders': sell_orders,
                    'total_orders': total_orders,
                    'total_allocated': total_allocated,
                    'capital_deployment_pct': capital_deployment_pct,
                    'gpt5_reasoning': reasoning,  # Keep key name for compatibility
                    'optimized_candidates': optimized_candidates
                },
                message=f"Deterministic allocator created trading plan: {len(sell_orders)} SELLs, {len(buy_orders)} BUYs (${total_allocated:,.0f} allocated)",
                quality_score=int(quality_score),
                issues=issues
            )

        except Exception as e:
            self.logger.error(f"  Portfolio Optimizer stage FAILED: {e}", exc_info=True)

            # FALLBACK: Simple equal-weight allocation to top candidates
            self.logger.warning("  Falling back to simple equal-weight allocation...")

            # Take top 5 candidates by composite score
            candidates = news_result.data.get('candidates', [])
            top_candidates = sorted(candidates, key=lambda x: x.get('composite_score', 0), reverse=True)[:5]

            available_capital = 100000.0
            per_position = (available_capital * 0.9) / max(len(top_candidates), 1)

            fallback_orders = []
            for candidate in top_candidates:
                entry_price = candidate.get('current_price', 1)
                shares = int(per_position / entry_price) if entry_price > 0 else 0

                fallback_orders.append({
                    'ticker': candidate['ticker'],
                    'action': 'BUY',
                    'shares': shares,
                    'allocated_capital': per_position,
                    'entry_price': entry_price,
                    'composite_score': candidate.get('composite_score', 0),
                    'gpt5_reasoning': 'Fallback allocation - AI optimizer unavailable'
                })

            return WorkflowStageResult(
                stage='gpt5_optimizer',
                success=len(fallback_orders) > 0,
                data={
                    'buy_orders': fallback_orders,
                    'sell_orders': [],
                    'total_orders': len(fallback_orders),
                    'fallback_mode': True
                },
                message=f"AI optimizer failed - using fallback allocation ({len(fallback_orders)} orders)",
                quality_score=50,
                issues=[f"AI optimization failed: {str(e)}", "Using fallback equal-weight allocation"]
            )

    def _generate_risk_assessment_message(self, candidates: List[Dict], available_capital: float) -> str:
        """
        Generate RiskAssessment message for Portfolio Department

        Args:
            candidates: List of candidates with risk metrics from Risk Department
            available_capital: Available capital for trading

        Returns:
            message_id of generated RiskAssessment message
        """
        from datetime import datetime, timezone
        import uuid
        import json
        import yaml

        # Generate message ID
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        unique_id = str(uuid.uuid4())[:8]
        msg_id = f"MSG_RISK_{timestamp_str}_{unique_id}"

        # Get parent message ID (from News or Research)
        parent_msg_id = "MSG_RESEARCH_UNKNOWN"  # TODO: Track this properly

        # Count approved vs rejected
        approved = [c for c in candidates if c.get('risk_score', 0) >= 50]
        rejected = [c for c in candidates if c.get('risk_score', 0) < 50]

        # Create YAML frontmatter
        metadata = {
            'from': 'RISK',
            'to': 'PORTFOLIO',
            'message_type': 'RiskAssessment',
            'message_id': msg_id,
            'parent_message_id': parent_msg_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'priority': 'routine',
            'requires_response': False
        }

        # Create markdown body
        date_str = datetime.now().strftime("%Y-%m-%d")
        body = f"""# Risk Assessment - {date_str}

**Assessment Date**: {date_str}
**Parent Message**: {parent_msg_id}

## Portfolio State
- **Capital**: ${available_capital:,.0f}
- **Current Heat**: $0 (0.00%)
- **Open Positions**: 0

## Risk Assessment Summary
- **Candidates Reviewed**: {len(candidates)}
- **Approved**: {len(approved)}
- **Rejected**: {len(rejected)}

## Approved Candidates

"""

        # Add each approved candidate
        for i, candidate in enumerate(approved, 1):
            ticker = candidate.get('ticker', 'N/A')
            sector = candidate.get('sector', 'Unknown')
            score = candidate.get('composite_score', candidate.get('research_composite_score', 0))
            shares = candidate.get('position_size_shares', 0)
            price = candidate.get('entry_price', candidate.get('current_price', 0))
            value = shares * price
            stop = candidate.get('stop_loss', 0)
            target = candidate.get('target_price', 0)
            rr_ratio = candidate.get('risk_reward_ratio', 0)
            risk_method = candidate.get('stop_loss_method', 'ATR_BASED')
            risk_per_share = candidate.get('risk_per_share', 0)
            total_risk = candidate.get('total_risk', 0)
            risk_pct = (total_risk / available_capital * 100) if available_capital > 0 else 0

            body += f"""### {i}. {ticker} ({sector})
- **Research Score**: {score:.1f}/100
- **Position**: {shares} shares @ ${price:.2f} = ${value:,.0f}
- **Entry**: ${price:.2f} | **Stop**: ${stop:.2f} | **Target**: ${target:.2f}
- **Risk/Reward**: {rr_ratio:.1f}:1 ({risk_method})
- **Risk**: ${total_risk:.0f} ({risk_pct:.2f}% of capital)

"""

        # Add rejected section if any
        if rejected:
            body += "\n## Rejected Candidates\n\n"
            for candidate in rejected:
                ticker = candidate.get('ticker', 'N/A')
                risk_score = candidate.get('risk_score', 0)
                warnings = candidate.get('risk_warnings', [])
                body += f"- **{ticker}**: Risk score {risk_score:.1f}/100"
                if warnings:
                    body += f" - {', '.join(warnings)}"
                body += "\n"

        # Create JSON payload
        payload = {
            'approved_candidates': approved,
            'rejected_candidates': rejected,
            'available_capital': available_capital,
            'total_candidates': len(candidates)
        }

        # Combine into message
        yaml_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        json_str = json.dumps(payload, indent=2)

        message_content = f"""---
{yaml_str}---

{body}

```json
{json_str}
```
"""

        # Write to outbox
        outbox_path = self.messages_dir / "Outbox" / "RISK"
        outbox_path.mkdir(parents=True, exist_ok=True)

        message_file = outbox_path / f"{msg_id}.md"
        with open(message_file, 'w', encoding='utf-8') as f:
            f.write(message_content)

        return msg_id

    def _run_compliance_advisory_loop(self, gpt5_result: WorkflowStageResult) -> WorkflowStageResult:
        """
        Run Compliance Department in ADVISORY mode

        Compliance reviews the GPT-5 proposed plan and provides suggestions.
        This is NOT a pass/fail filter - Compliance advises, CEO/Portfolio incorporate feedback.

        In future iterations, this could involve back-and-forth dialogue.
        For now, we get Compliance's advisory feedback and incorporate reasonable suggestions.
        """
        try:
            self.logger.info("  Compliance reviewing proposed trading plan (advisory mode)...")

            # Initialize Compliance Department
            if not self._compliance_dept:
                self.logger.info("  Initializing Compliance Department...")
                config_path = self.config_dir / "compliance_config.yaml"

                if not config_path.exists():
                    self.logger.warning(f"  Compliance config not found: {config_path}")
                    self.logger.warning("  Continuing without Compliance review")
                    return WorkflowStageResult(
                        stage='compliance_advisory',
                        success=True,
                        data=gpt5_result.data,  # Pass through GPT-5 plan unchanged
                        message="Compliance config not found - skipped advisory review",
                        quality_score=100,
                        issues=[]
                    )

                from Departments.Compliance.compliance_department import ComplianceDepartment
                self._compliance_dept = ComplianceDepartment(
                    config_path=config_path,
                    db_path=self.db_path
                )

            # Get trading plan from GPT-5
            buy_orders = gpt5_result.data.get('buy_orders', [])
            sell_orders = gpt5_result.data.get('sell_orders', [])

            self.logger.info(f"  Reviewing {len(buy_orders)} BUYs and {len(sell_orders)} SELLs...")

            # Compliance checks each order and provides advisory feedback
            compliance_suggestions = []
            approved_buys = []
            flagged_buys = []

            for buy_order in buy_orders:
                # Run through Compliance pre-trade validation (advisory only)
                # Note: We're using Compliance's validate_trade but treating rejections as suggestions
                proposal = {
                    'ticker': buy_order['ticker'],
                    'trade_type': 'BUY',
                    'shares': buy_order['shares'],
                    'price': buy_order['entry_price'],
                    'position_value': buy_order['allocated_capital'],
                    'total_risk': buy_order.get('total_risk', 0),
                    'sector': buy_order.get('sector', 'Unknown'),
                    'stop_loss': buy_order.get('stop_loss', 0),
                    'target': buy_order.get('target_price', 0),
                    'is_position_adjustment': buy_order.get('is_position_adjustment', False)
                }

                is_approved, rejection_reason, rejection_category, check_results = \
                    self._compliance_dept.validator.validate_trade(proposal)

                if is_approved:
                    approved_buys.append(buy_order)
                else:
                    # Compliance REJECTED this - actually reject it
                    flagged_buys.append(buy_order)
                    compliance_suggestions.append({
                        'ticker': buy_order['ticker'],
                        'suggestion_type': rejection_category,
                        'suggestion': rejection_reason,
                        'severity': 'REJECTED'  # Actually block the trade
                    })
                    self.logger.warning(f"    ✗ REJECTED: {buy_order['ticker']} - {rejection_reason}")

            # SELLs don't need pre-trade validation (closing positions)
            approved_sells = sell_orders

            self.logger.info(f"  Compliance Enforcement Summary:")
            self.logger.info(f"    - {len(approved_buys)} BUYs APPROVED")
            self.logger.info(f"    - {len(flagged_buys)} BUYs REJECTED by compliance")
            self.logger.info(f"    - {len(approved_sells)} SELLs approved (no validation needed)")

            if compliance_suggestions:
                self.logger.warning("  Compliance REJECTIONS:")
                for suggestion in compliance_suggestions[:5]:  # Show first 5
                    self.logger.warning(f"    - {suggestion['ticker']}: {suggestion['suggestion']}")

            # Quality score: 100 if no flags, reduced if there are suggestions
            quality_score = max(70, 100 - (len(compliance_suggestions) * 5))

            return WorkflowStageResult(
                stage='compliance_enforcement',
                success=True,
                data={
                    'buy_orders': approved_buys,
                    'sell_orders': approved_sells,
                    'total_orders': len(approved_buys) + len(approved_sells),
                    'compliance_rejections': compliance_suggestions,
                    'rejected_count': len(flagged_buys),
                    'gpt5_reasoning': gpt5_result.data.get('gpt5_reasoning', ''),
                    'total_allocated': gpt5_result.data.get('total_allocated', 0),
                    'capital_deployment_pct': gpt5_result.data.get('capital_deployment_pct', 0)
                },
                message=f"Compliance enforced: {len(approved_buys)} BUYs approved, {len(flagged_buys)} rejected, {len(approved_sells)} SELLs",
                quality_score=int(quality_score),
                issues=[f"{len(flagged_buys)} orders REJECTED by compliance"] if flagged_buys else []
            )

        except Exception as e:
            self.logger.error(f"  Compliance advisory loop FAILED: {e}", exc_info=True)

            # If Compliance fails, continue with GPT-5's plan unchanged
            self.logger.warning("  Continuing with GPT-5 plan (Compliance unavailable)")

            return WorkflowStageResult(
                stage='compliance_advisory',
                success=True,
                data=gpt5_result.data,  # Pass through unchanged
                message=f"Compliance advisory failed: {str(e)} - proceeding with GPT-5 plan",
                quality_score=80,
                issues=[f"Compliance review unavailable: {str(e)}"]
            )

    def _run_compliance_stage(self, gpt5_result: WorkflowStageResult) -> WorkflowStageResult:
        """Run Compliance Department and validate output"""
        try:
            # Initialize Compliance Department
            if not self._compliance_dept:
                self.logger.info("  Initializing Compliance Department...")
                config_path = self.config_dir / "compliance_config.yaml"

                if not config_path.exists():
                    raise FileNotFoundError(f"Compliance config not found: {config_path}")

                self._compliance_dept = ComplianceDepartment(
                    config_path=config_path,
                    db_path=self.db_path
                )

            # Get buy orders from GPT-5 Optimizer (which has dynamic capital allocations)
            buy_orders = gpt5_result.data.get('buy_orders', [])

            if not buy_orders:
                raise ValueError("No buy orders to validate from GPT-5 Optimizer")

            # Validate each trade against compliance rules
            self.logger.info("  Validating trades against compliance rules...")
            self.logger.info(f"  (Checking {len(buy_orders)} trades: position size, sector limits, risk, duplicates, restrictions...)")

            approved_trades = []
            rejected_trades = []

            for order in buy_orders:
                # Format trade proposal for Compliance validator
                # Note: Portfolio uses 'position_size_value' from Risk, not 'position_value'
                position_val = order.get('position_value', order.get('position_size_value', 0))
                entry_price = order.get('price', order.get('entry_price', order.get('current_price', 0)))

                proposal = {
                    'ticker': order.get('ticker', order.get('symbol', 'UNKNOWN')),
                    'trade_type': 'BUY',
                    'shares': order.get('shares', order.get('position_size_shares', order.get('qty', 0))),
                    'price': entry_price,
                    'position_value': position_val,
                    'total_risk': order.get('total_risk', 0),
                    'sector': order.get('sector', 'Unknown'),
                    'stop_loss': order.get('stop_loss', order.get('stop', 0)),
                    'target': order.get('target_price', order.get('target', 0)),
                    'is_position_adjustment': order.get('is_position_adjustment', False)
                }

                # Validate trade
                is_approved, rejection_reason, rejection_category, check_results = \
                    self._compliance_dept.validator.validate_trade(proposal)

                if is_approved:
                    approved_trades.append({
                        **order,
                        'compliance_approved': True,
                        'compliance_checks': check_results
                    })
                else:
                    rejected_trades.append({
                        **order,
                        'compliance_approved': False,
                        'rejection_reason': rejection_reason,
                        'rejection_category': rejection_category,
                        'compliance_checks': check_results
                    })

            approved_count = len(approved_trades)
            rejected_count = len(rejected_trades)

            self.logger.info(f"  Compliance validation completed: {approved_count} approved, {rejected_count} rejected")

            # Log approved trades
            if approved_trades:
                self.logger.info(f"  Approved trades:")
                for trade in approved_trades[:5]:  # Show first 5
                    ticker = trade.get('ticker', trade.get('symbol', 'N/A'))
                    self.logger.info(f"    - {ticker}: All compliance checks passed")

            # Log rejected trades
            if rejected_trades:
                self.logger.warning(f"  Rejected trades:")
                for trade in rejected_trades:
                    ticker = trade.get('ticker', trade.get('symbol', 'N/A'))
                    reason = trade.get('rejection_reason', 'Unknown')
                    self.logger.warning(f"    - {ticker}: {reason}")

            issues = []
            if approved_count < self.min_compliance_approved:
                issues.append(f"Only {approved_count} trades passed compliance (minimum {self.min_compliance_approved})")

            if rejected_count > 0:
                issues.append(f"{rejected_count} trades failed compliance checks")

            success = approved_count >= self.min_compliance_approved

            # Quality score based on pass rate
            pass_rate = approved_count / len(buy_orders) if buy_orders else 0
            quality_score = int(pass_rate * 100)

            return WorkflowStageResult(
                stage='compliance',
                success=success,
                data={
                    'approved_trades': approved_trades,
                    'rejected_trades': rejected_trades,
                    'approved_count': approved_count,
                    'rejected_count': rejected_count
                },
                message=f"Compliance approved {approved_count}/{len(buy_orders)} trades (pass rate {pass_rate*100:.0f}%)",
                quality_score=quality_score,
                issues=issues
            )

        except Exception as e:
            self.logger.error(f"  Compliance stage FAILED: {e}", exc_info=True)
            return WorkflowStageResult(
                stage='compliance',
                success=False,
                data={},
                message=f"Compliance validation failed: {str(e)}",
                quality_score=0,
                issues=[str(e)]
            )

    def _route_message(self, from_dept: str, to_dept: str, message_id: str):
        """Move message from one department's outbox to another's inbox"""
        try:
            source = self.messages_dir / "Outbox" / from_dept / f"{message_id}.md"
            dest_dir = self.messages_dir / "Inbox" / to_dept
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / f"{message_id}.md"

            if source.exists():
                import shutil
                shutil.copy2(source, dest)
                self.logger.debug(f"  Routed message {message_id} from {from_dept} to {to_dept}")
            else:
                self.logger.warning(f"  Source message not found: {source}")

        except Exception as e:
            self.logger.error(f"  Failed to route message: {e}")

    def _handle_stage_failure(self, stage: str, result: WorkflowStageResult,
                             all_results: List[WorkflowStageResult]) -> Dict:
        """Handle when a stage fails quality checks"""
        self.logger.warning(f"\n[STAGE FAILURE] {stage.upper()} stage did not meet quality requirements")
        self.logger.warning(f"  Quality score: {result.quality_score}/100")
        for issue in result.issues:
            self.logger.warning(f"  - {issue}")

        # Create escalation
        escalation = Escalation(
            stage=stage,
            issue_type='quality_failure',
            severity='WARNING' if result.quality_score > 30 else 'CRITICAL',
            context={
                'stage_result': self._serialize_result(result),
                'quality_score': result.quality_score,
                'issues': result.issues
            },
            options=self._get_escalation_options(stage, result),
            recommendation=self._get_recommendation(stage, result)
        )

        return {
            'status': 'ESCALATED',
            'escalation': self._serialize_escalation(escalation),
            'stage_results': [self._serialize_result(r) for r in all_results]
        }

    def _get_escalation_options(self, stage: str, result: WorkflowStageResult) -> List[str]:
        """Get available options for handling escalation"""
        options = []

        if stage == 'research':
            options.append("Accept lower candidate count and proceed")
            options.append("Skip trading today (market conditions unfavorable)")
            options.append("Retry with relaxed screening criteria")

        elif stage == 'risk':
            options.append("Accept lower position count")
            options.append("Ask Research for more candidates")
            options.append("Skip trading today (insufficient opportunities)")

        elif stage == 'portfolio':
            options.append("Accept minimal trades")
            options.append("Relax portfolio constraints")
            options.append("Skip trading today")

        elif stage == 'compliance':
            options.append("Skip trading today (regulatory constraints)")
            options.append("Review and adjust trade sizes")

        return options

    def _get_recommendation(self, stage: str, result: WorkflowStageResult) -> str:
        """Get CEO recommendation for handling escalation"""
        if result.quality_score < 30:
            return f"CRITICAL: {stage} stage produced very low quality results. Recommend skipping trading today."
        elif result.quality_score < 60:
            return f"WARNING: {stage} stage below optimal quality. Recommend reviewing options with user."
        else:
            return f"ACCEPTABLE: {stage} stage marginally below threshold. Recommend proceeding with caution."

    def _aggregate_final_plan(self, stage_results: List[WorkflowStageResult]) -> Dict:
        """Aggregate all stage results into final trading plan"""
        # Extract final orders from compliance advisory stage
        compliance_result = stage_results[-1]  # Compliance advisory is last stage
        buy_orders = compliance_result.data.get('buy_orders', [])
        sell_orders = compliance_result.data.get('sell_orders', [])
        all_trades = buy_orders + sell_orders
        trade_count = len(all_trades)

        # Build comprehensive plan
        plan = {
            'plan_id': f"PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'status': 'READY_FOR_CEO_REVIEW',
            'summary': {
                'total_trades': trade_count,
                'research_candidates': stage_results[0].data.get('candidate_count', 0),
                'gpt5_selected': compliance_result.data.get('total_orders', 0),
                'compliance_flagged': compliance_result.data.get('flagged_count', 0),
                'overall_quality_score': sum(r.quality_score for r in stage_results) // len(stage_results)
            },
            'stage_quality': {
                'research': stage_results[0].quality_score,
                'news': stage_results[1].quality_score,
                'gpt5_optimizer': stage_results[2].quality_score,
                'compliance_advisory': stage_results[3].quality_score
            },
            'trades': all_trades,  # All trades (BUYs + SELLs) including flagged ones
            'gpt5_reasoning': compliance_result.data.get('gpt5_reasoning', ''),
            'compliance_suggestions': compliance_result.data.get('compliance_suggestions', []),
            'workflow_summary': [
                {
                    'stage': r.stage,
                    'message': r.message,
                    'quality_score': r.quality_score,
                    'issues': r.issues
                }
                for r in stage_results
            ]
        }

        return plan

    def _serialize_result(self, result: WorkflowStageResult) -> Dict:
        """Convert WorkflowStageResult to dict"""
        return {
            'stage': result.stage,
            'success': result.success,
            'data': result.data,
            'message': result.message,
            'quality_score': result.quality_score,
            'issues': result.issues
        }

    def _serialize_escalation(self, escalation: Escalation) -> Dict:
        """Convert Escalation to dict"""
        return {
            'stage': escalation.stage,
            'issue_type': escalation.issue_type,
            'severity': escalation.severity,
            'context': escalation.context,
            'options': escalation.options,
            'recommendation': escalation.recommendation
        }

    def _get_latest_regime_assessment(self) -> Optional[Dict]:
        """
        Fetch the latest market regime assessment from database

        Returns:
            Dict with regime info or None if not available
        """
        try:
            import sqlite3
            conn = sqlite3.connect(self.project_root / "sentinel.db", timeout=30)
            cursor = conn.cursor()

            # Get most recent assessment
            cursor.execute("""
                SELECT regime, confidence, spy_price, spy_change_pct, vix_level, vix_change_pct,
                       recommendation, reasoning, timestamp
                FROM market_regime_assessments
                ORDER BY timestamp DESC
                LIMIT 1
            """)

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'regime': row[0],
                    'confidence': row[1],
                    'spy_price': row[2],
                    'spy_change_pct': row[3],
                    'vix_level': row[4],
                    'vix_change_pct': row[5],
                    'recommendation': row[6],
                    'reasoning': row[7],
                    'timestamp': row[8]
                }
            return None

        except Exception as e:
            self.logger.warning(f"Could not fetch regime assessment: {e}")
            return None


if __name__ == "__main__":
    # Test Operations Manager
    logger.info("Testing Operations Manager")

    project_root = Path(__file__).parent.parent.parent
    ops_manager = OperationsManager(project_root)

    # Generate trading plan
    result = ops_manager.generate_trading_plan()

    logger.info("\n" + "=" * 80)
    logger.info("TEST COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Status: {result['status']}")

    if result['status'] == 'SUCCESS':
        plan = result['plan']
        logger.info(f"Plan ID: {plan['plan_id']}")
        logger.info(f"Total Trades: {plan['summary']['total_trades']}")
        logger.info(f"Overall Quality: {plan['summary']['overall_quality_score']}/100")
    elif result['status'] == 'ESCALATED':
        esc = result['escalation']
        logger.info(f"Escalation: {esc['stage']} - {esc['severity']}")
        logger.info(f"Recommendation: {esc['recommendation']}")
