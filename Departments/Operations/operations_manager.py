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
from Departments.Risk.risk_department import RiskDepartment
from Departments.Portfolio.portfolio_department import PortfolioDepartment
from Departments.Compliance.compliance_department import ComplianceDepartment
from Departments.Executive.gpt5_portfolio_optimizer import GPT5PortfolioOptimizer

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
        self._risk_dept = None
        self._portfolio_dept = None
        self._compliance_dept = None
        self._gpt5_optimizer = None

        self.logger.info("Operations Manager initialized successfully")
        self.logger.info(f"Project root: {project_root}")
        self.logger.info(f"Database: {self.db_path}")

    def generate_trading_plan(self) -> Dict:
        """
        Coordinate all departments to generate complete trading plan

        Returns:
            Dict with:
            - status: 'SUCCESS', 'ESCALATED', 'FAILED'
            - plan: Final trading plan (if SUCCESS)
            - escalation: Escalation details (if ESCALATED)
            - stage_results: Results from each stage
        """
        self.logger.info("=" * 80)
        self.logger.info("GENERATING TRADING PLAN - WORKFLOW START")
        self.logger.info("=" * 80)

        stage_results = []

        try:
            # STAGE 1: Research Department
            self.logger.info("\n[STAGE 1/4] Research Department - Market Analysis & Candidate Screening")
            research_result = self._run_research_stage()
            stage_results.append(research_result)

            if not research_result.success:
                return self._handle_stage_failure('research', research_result, stage_results)

            # STAGE 2: Risk Department
            self.logger.info("\n[STAGE 2/4] Risk Department - Position Sizing & Risk Assessment")
            risk_result = self._run_risk_stage(research_result)
            stage_results.append(risk_result)

            if not risk_result.success:
                return self._handle_stage_failure('risk', risk_result, stage_results)

            # STAGE 3: Portfolio Department
            self.logger.info("\n[STAGE 3/5] Portfolio Department - Constraint Application & Selection")
            portfolio_result = self._run_portfolio_stage(risk_result)
            stage_results.append(portfolio_result)

            if not portfolio_result.success:
                return self._handle_stage_failure('portfolio', portfolio_result, stage_results)

            # STAGE 4: GPT-5 Portfolio Optimizer (NEW - AI-driven capital allocation)
            self.logger.info("\n[STAGE 4/5] GPT-5 Portfolio Optimizer - Intelligent Capital Allocation")
            gpt5_result = self._run_gpt5_optimization_stage(portfolio_result, risk_result)
            stage_results.append(gpt5_result)

            if not gpt5_result.success:
                return self._handle_stage_failure('gpt5_optimizer', gpt5_result, stage_results)

            # STAGE 5: Compliance Department
            self.logger.info("\n[STAGE 5/5] Compliance Department - Pre-Trade Validation")
            compliance_result = self._run_compliance_stage(gpt5_result)
            stage_results.append(compliance_result)

            if not compliance_result.success:
                return self._handle_stage_failure('compliance', compliance_result, stage_results)

            # ALL STAGES PASSED - Aggregate final plan
            self.logger.info("\n[AGGREGATION] All stages passed - building final plan")
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
            # Initialize Research Department
            if not self._research_dept:
                self.logger.info("  Initializing Research Department...")
                config_path = self.config_dir / "research_config.yaml"

                if not config_path.exists():
                    raise FileNotFoundError(f"Research config not found: {config_path}")

                with open(config_path, 'r') as f:
                    research_config = yaml.safe_load(f)

                # Check if PERPLEXITY_API_KEY is configured
                if not hasattr(config, 'PERPLEXITY_API_KEY') or not config.PERPLEXITY_API_KEY:
                    self.logger.warning("  PERPLEXITY_API_KEY not configured - Research will use basic analysis only")
                    perplexity_key = None
                else:
                    perplexity_key = config.PERPLEXITY_API_KEY

                self._research_dept = ResearchDepartment(
                    config=research_config,
                    perplexity_api_key=perplexity_key,
                    db_path=self.db_path
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
                quality_score = 0

            success = candidate_count >= self.min_research_candidates

            self.logger.info(f"  Research completed: {candidate_count} candidates found")
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

    def _run_risk_stage(self, research_result: WorkflowStageResult) -> WorkflowStageResult:
        """Run Risk Department and validate output"""
        try:
            # Initialize Risk Department
            if not self._risk_dept:
                self.logger.info("  Initializing Risk Department...")
                config_path = self.config_dir / "risk_config.yaml"

                if not config_path.exists():
                    raise FileNotFoundError(f"Risk config not found: {config_path}")

                self._risk_dept = RiskDepartment(
                    config_path=str(config_path),
                    db_path=str(self.db_path)
                )

            # Get Research message path
            research_msg_id = research_result.data['message_id']
            research_msg_path = self.messages_dir / "Outbox" / "RESEARCH" / f"{research_msg_id}.md"

            if not research_msg_path.exists():
                raise FileNotFoundError(f"Research message not found: {research_msg_path}")

            # Process daily briefing (calls REAL Risk Department)
            self.logger.info("  Calculating position sizes and risk metrics...")
            self.logger.info("  (Applying risk limits: 1% per trade, 5% portfolio heat, 40% sector max...)")

            risk_msg_id = self._risk_dept.process_daily_briefing(research_msg_path)

            if not risk_msg_id:
                raise ValueError("Risk Department failed to generate RiskAssessment message")

            # Read the RiskAssessment message to get results
            risk_msg_path = self.messages_dir / "Outbox" / "RISK" / f"{risk_msg_id}.md"

            if not risk_msg_path.exists():
                raise FileNotFoundError(f"Risk output message not found: {risk_msg_path}")

            # Parse message to extract approved candidate data
            with open(risk_msg_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract JSON payload
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON payload found in Risk message")

            approved_candidates = data.get('approved_candidates', [])
            rejected_candidates = data.get('rejected_candidates', [])
            approved_count = len(approved_candidates)
            rejected_count = len(rejected_candidates)

            # Calculate quality metrics
            issues = []
            if approved_count < self.min_risk_approved:
                issues.append(f"Only {approved_count} candidates approved by Risk (minimum {self.min_risk_approved})")

            # Quality score based on approval rate and average risk/reward
            if approved_candidates:
                avg_risk_reward = sum(c.get('risk_reward_ratio', 0) for c in approved_candidates) / len(approved_candidates)
                approval_rate = approved_count / (approved_count + rejected_count) if (approved_count + rejected_count) > 0 else 0

                # Quality = 50% approval rate + 50% risk/reward quality
                quality_score = min(100, int(
                    (approval_rate * 50) +
                    (min(avg_risk_reward / 3.0, 1.0) * 50)  # R/R of 3:1 = perfect score
                ))
            else:
                quality_score = 0

            success = approved_count >= self.min_risk_approved

            self.logger.info(f"  Risk assessment completed: {approved_count} approved, {rejected_count} rejected")
            if approved_candidates:
                # Log top 3 by risk/reward
                top_3 = sorted(approved_candidates, key=lambda x: x.get('risk_reward_ratio', 0), reverse=True)[:3]
                self.logger.info(f"  Top risk/reward ratios:")
                for c in top_3:
                    ticker = c.get('ticker', 'N/A')
                    rr = c.get('risk_reward_ratio', 0)
                    shares = c['position'].get('shares', 0) if 'position' in c else 0
                    self.logger.info(f"    - {ticker}: {rr:.2f}:1 R/R, {shares:.2f} shares")

            if issues:
                for issue in issues:
                    self.logger.warning(f"  ISSUE: {issue}")

            return WorkflowStageResult(
                stage='risk',
                success=success,
                data={
                    'message_id': risk_msg_id,
                    'approved_candidates': approved_candidates,
                    'rejected_candidates': rejected_candidates,
                    'approved_count': approved_count,
                    'rejected_count': rejected_count,
                    'avg_risk_reward': sum(c.get('risk_reward_ratio', 0) for c in approved_candidates) / len(approved_candidates) if approved_candidates else 0
                },
                message=f"Risk approved {approved_count} candidates (avg R/R {sum(c.get('risk_reward_ratio', 0) for c in approved_candidates) / len(approved_candidates):.2f}:1)" if approved_candidates else f"Risk approved {approved_count} candidates",
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

    def _run_gpt5_optimization_stage(self, portfolio_result: WorkflowStageResult, risk_result: WorkflowStageResult) -> WorkflowStageResult:
        """Run GPT-5 Portfolio Optimizer for intelligent capital allocation"""
        try:
            # Initialize GPT-5 Optimizer
            if not self._gpt5_optimizer:
                self.logger.info("  Initializing GPT-5 Portfolio Optimizer (OpenAI GPT-5)...")
                # Get OpenAI API key from config
                import config as app_config
                self._gpt5_optimizer = GPT5PortfolioOptimizer(api_key=app_config.OPENAI_API_KEY)

            # Get candidates from Portfolio and Risk
            buy_orders = portfolio_result.data.get('buy_orders', [])
            approved_candidates = risk_result.data.get('approved_candidates', [])

            if not buy_orders:
                raise ValueError("No buy orders from Portfolio to optimize")

            # Merge data: buy_orders from Portfolio + full candidate data from Risk
            # Build comprehensive candidate list for GPT-5
            candidates_for_gpt5 = []
            for order in buy_orders:
                ticker = order.get('ticker', order.get('symbol'))

                # Find matching candidate from Risk to get full data
                risk_candidate = next((c for c in approved_candidates if c.get('ticker') == ticker), None)

                if risk_candidate:
                    # Combine Portfolio order with Risk candidate data
                    merged = {
                        'ticker': ticker,
                        'research_composite_score': risk_candidate.get('research_composite_score', 0),
                        'technical_score': risk_candidate.get('technical_score', 0),
                        'fundamental_score': risk_candidate.get('fundamental_score', 0),
                        'sentiment_score': risk_candidate.get('sentiment_score', 0),
                        'risk_reward_ratio': risk_candidate.get('risk_reward_ratio', 0),
                        'position_size_shares': order.get('shares', order.get('position_size_shares', 0)),
                        'position_size_value': order.get('position_size_value', order.get('position_value', 0)),
                        'entry_price': order.get('price', order.get('entry_price', 0)),
                        'stop_loss': order.get('stop_loss', order.get('stop', 0)),
                        'target': order.get('target_price', order.get('target', 0)),
                        'sector': order.get('sector', 'Unknown'),
                        'total_risk': order.get('total_risk', 0),
                        'portfolio_heat': risk_candidate.get('portfolio_heat', 0)
                    }
                    candidates_for_gpt5.append(merged)

            self.logger.info(f"  Sending {len(candidates_for_gpt5)} candidates to GPT-5 for intelligent allocation...")
            self.logger.info("  (GPT-5 will analyze scores, risk/reward, and determine optimal capital allocation...)")

            # Get current portfolio state
            # TODO: Query database for current positions and available capital
            # For now, use placeholder values
            available_capital = 100000.0  # $100K default
            current_positions = 0
            max_positions = 10

            # Get market conditions
            # TODO: Query actual SPY, VIX data
            market_conditions = {
                'spy_change_pct': 0.0,
                'vix_level': 20.0,
                'market_sentiment': 'neutral',
                'timestamp': datetime.now().isoformat()
            }

            # Call GPT-5 optimizer
            optimized_candidates, reasoning = self._gpt5_optimizer.optimize_portfolio(
                candidates=candidates_for_gpt5,
                available_capital=available_capital,
                market_conditions=market_conditions,
                current_positions=current_positions,
                max_positions=max_positions
            )

            self.logger.info(f"  GPT-5 optimization completed for {len(optimized_candidates)} candidates")

            # Log GPT-5's reasoning
            self.logger.info("  GPT-5 Chief Investment Officer Analysis:")
            for line in reasoning.split('\n')[:10]:  # First 10 lines
                if line.strip():
                    self.logger.info(f"    {line.strip()}")

            # Calculate total allocated capital
            total_allocated = sum(c.get('allocated_capital', 0) for c in optimized_candidates)
            capital_deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0

            self.logger.info(f"  Capital Deployment: ${total_allocated:,.2f} / ${available_capital:,.2f} ({capital_deployment_pct:.1f}%)")

            # Update buy_orders with GPT-5's allocations
            optimized_orders = []
            for candidate in optimized_candidates:
                ticker = candidate['ticker']
                allocated_capital = candidate.get('allocated_capital', 0)

                # Find original order
                original_order = next((o for o in buy_orders if o.get('ticker', o.get('symbol')) == ticker), None)

                if original_order and allocated_capital > 0:
                    # Recalculate shares based on GPT-5's capital allocation
                    entry_price = candidate.get('entry_price', original_order.get('price', 1))
                    new_shares = allocated_capital / entry_price if entry_price > 0 else 0

                    # Update order with GPT-5's allocation
                    optimized_order = original_order.copy()
                    optimized_order['position_value'] = allocated_capital
                    optimized_order['position_size_value'] = allocated_capital
                    optimized_order['shares'] = new_shares
                    optimized_order['position_size_shares'] = new_shares
                    optimized_order['gpt5_allocated'] = True
                    optimized_order['gpt5_conviction'] = candidate.get('conviction_level', 'medium')

                    optimized_orders.append(optimized_order)

            approved_count = len(optimized_orders)

            # Quality score based on capital deployment and diversification
            quality_score = min(100, int(
                (capital_deployment_pct / 90.0 * 70) +  # 70% weight on capital deployment (90%+ target)
                (min(approved_count / 5.0, 1.0) * 30)   # 30% weight on diversification (5+ positions ideal)
            ))

            issues = []
            if capital_deployment_pct < 80:
                issues.append(f"Capital deployment below target: {capital_deployment_pct:.1f}% (target 90%+)")
            if approved_count < 5:
                issues.append(f"Limited diversification: {approved_count} positions (target 5+)")

            success = approved_count > 0 and capital_deployment_pct >= 50  # At least 50% deployed

            return WorkflowStageResult(
                stage='gpt5_optimizer',
                success=success,
                data={
                    'buy_orders': optimized_orders,
                    'approved_count': approved_count,
                    'total_allocated': total_allocated,
                    'capital_deployment_pct': capital_deployment_pct,
                    'gpt5_reasoning': reasoning,
                    'optimized_candidates': optimized_candidates
                },
                message=f"GPT-5 optimized {approved_count} positions (${total_allocated:,.0f} allocated, {capital_deployment_pct:.1f}% deployment)",
                quality_score=int(quality_score),
                issues=issues
            )

        except Exception as e:
            self.logger.error(f"  GPT-5 Optimizer stage FAILED: {e}", exc_info=True)

            # FALLBACK: Use Portfolio's original orders if GPT-5 fails
            self.logger.warning("  Falling back to Portfolio's original allocations...")
            buy_orders = portfolio_result.data.get('buy_orders', [])

            return WorkflowStageResult(
                stage='gpt5_optimizer',
                success=len(buy_orders) > 0,
                data={
                    'buy_orders': buy_orders,
                    'approved_count': len(buy_orders),
                    'fallback_mode': True
                },
                message=f"GPT-5 failed, using fallback allocation ({len(buy_orders)} orders)",
                quality_score=50,  # Reduced score for fallback
                issues=[f"GPT-5 optimization failed: {str(e)}", "Using fallback allocation"]
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
                    'target': order.get('target_price', order.get('target', 0))
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
        # Extract final trade count from compliance stage
        compliance_result = stage_results[-1]
        trade_count = compliance_result.data.get('approved_count', 0)
        approved_trades = compliance_result.data.get('approved_trades', [])

        # Build comprehensive plan
        plan = {
            'plan_id': f"PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'status': 'READY_FOR_CEO_REVIEW',
            'summary': {
                'total_trades': trade_count,
                'research_candidates': stage_results[0].data.get('candidate_count', 0),
                'risk_approved': stage_results[1].data.get('approved_count', 0),
                'portfolio_selected': stage_results[2].data.get('approved_count', 0),
                'compliance_approved': trade_count,
                'overall_quality_score': sum(r.quality_score for r in stage_results) // len(stage_results)
            },
            'stage_quality': {
                'research': stage_results[0].quality_score,
                'risk': stage_results[1].quality_score,
                'portfolio': stage_results[2].quality_score,
                'compliance': stage_results[3].quality_score
            },
            'trades': approved_trades,  # Real approved trades from Compliance
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
