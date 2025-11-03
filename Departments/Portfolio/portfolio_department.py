"""
Portfolio Department - Trade Decision Engine, Position Tracking, Exit Signal Generation
Built fresh from C(P) Week 4 specifications

Responsibilities:
- Consume RiskAssessment messages from Risk Department
- Apply portfolio-level constraints (max positions, capital limits)
- Generate TradeOrder messages for Trading Department
- Monitor open positions for exit signals (stop/target/time/downgrade)
- Maintain portfolio state (PENDING → OPEN → CLOSED lifecycle)

Pattern: Message-based architecture (same as Research/Risk Departments)
Zero code reuse from v6.2 (100% fresh implementation)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging
import json
import yaml
import uuid
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Import unified data source (routes to Alpaca or database)
from Utils.data_source import create_data_source

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PortfolioDepartment')


class MessageHandler:
    """
    Handles reading and writing messages for Portfolio Department

    Pattern learned from Risk Department (Week 3)
    Implements YAML frontmatter + Markdown + JSON payload format
    """

    def __init__(self):
        self.inbox_path = Path("Messages_Between_Departments/Inbox/PORTFOLIO")
        self.outbox_path = Path("Messages_Between_Departments/Outbox/PORTFOLIO")
        self.archive_path = Path("Messages_Between_Departments/Archive")

        # Create directories if they don't exist
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        self.outbox_path.mkdir(parents=True, exist_ok=True)

        logger.info("MessageHandler initialized for Portfolio Department")

    def read_message(self, message_path: Path) -> Tuple[Dict, str, Dict]:
        """
        Read message from file and parse YAML frontmatter + markdown body + JSON payload

        Returns:
            (metadata_dict, body_string, data_payload_dict)
        """
        with open(message_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split YAML frontmatter from body
        parts = content.split('---\n')
        if len(parts) < 3:
            raise ValueError(f"Invalid message format in {message_path}")

        metadata = yaml.safe_load(parts[1])
        body_and_json = '---\n'.join(parts[2:]).strip()

        # Extract JSON payload if present
        data_payload = None
        body = body_and_json

        if '```json' in body_and_json:
            body_parts = body_and_json.split('```json')
            body = body_parts[0].strip()
            json_str = body_parts[1].split('```')[0].strip()
            data_payload = json.loads(json_str)

        logger.info(f"Read message: {metadata.get('message_id')}")
        return metadata, body, data_payload

    def write_message(self, to_dept: str, message_type: str, subject: str,
                     body: str, data_payload: Optional[Dict] = None,
                     parent_message_id: Optional[str] = None,
                     priority: str = 'routine',
                     requires_response: bool = False) -> str:
        """
        Write message to outbox with YAML frontmatter + markdown + JSON payload

        Args:
            to_dept: Destination department
            message_type: Type of message (e.g., 'TradeOrder', 'PortfolioDecision')
            subject: Message subject line
            body: Markdown body content
            data_payload: Optional JSON data
            parent_message_id: Optional parent message ID (for tracking message chains)
            priority: Message priority (routine/high/urgent/critical)
            requires_response: Whether this message requires a response

        Returns:
            message_id (for database tracking)
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        msg_id = f"MSG_PORTFOLIO_{timestamp}_{uuid.uuid4().hex[:8]}"

        # Build YAML frontmatter
        metadata = {
            'message_id': msg_id,
            'from': 'PORTFOLIO',
            'to': to_dept,
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'message_type': message_type,
            'priority': priority,
            'requires_response': requires_response
        }

        # Add parent message ID if provided (for message chain tracking)
        if parent_message_id:
            metadata['parent_message_id'] = parent_message_id

        # Build message content
        content = "---\n"
        content += yaml.dump(metadata, default_flow_style=False)
        content += "---\n\n"
        content += f"# {subject}\n\n"
        content += body

        # Add JSON payload if provided
        if data_payload:
            content += "\n\n```json\n"
            content += json.dumps(data_payload, indent=2)
            content += "\n```\n"

        # Write to outbox
        filename = f"{msg_id}.md"
        filepath = self.outbox_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Wrote message {msg_id} to {to_dept}")
        return msg_id

    def archive_message(self, message_path: Path):
        """Move processed message to archive"""
        today = datetime.now().strftime('%Y-%m-%d')
        archive_dir = self.archive_path / today / "PORTFOLIO"
        archive_dir.mkdir(parents=True, exist_ok=True)

        archived_path = archive_dir / message_path.name

        # If file already exists in archive, remove inbox file
        if archived_path.exists():
            message_path.unlink()
        else:
            message_path.rename(archived_path)

        logger.info(f"Archived message: {message_path.name}")


class PortfolioDecisionEngine:
    """
    Makes final buy decisions based on portfolio constraints

    Applies:
    - Minimum composite score filter
    - Maximum position count limit
    - Maximum capital deployment limit
    Ranks candidates by score when capacity limited
    """

    def __init__(self, config: Dict, db_path: Path):
        self.config = config
        self.db_path = db_path

        # Load limits from config
        self.max_positions = config['limits']['max_positions']
        self.max_capital_deployed_pct = config['limits']['max_capital_deployed_pct']
        self.min_composite_score = config['filters']['min_composite_score']
        self.total_capital = config['capital']['total']

        # Initialize data source (routes to Alpaca or database)
        self.data_source = create_data_source(str(db_path))

        logger.info(f"PortfolioDecisionEngine initialized (max positions: {self.max_positions}, "
                   f"max deployed: {self.max_capital_deployed_pct*100:.0f}%, "
                   f"min score: {self.min_composite_score})")
        logger.info(f"Data source: {self.data_source.get_data_source_info()['data_source']}")

    def get_open_positions_count(self) -> int:
        """Get count of current open/pending positions (from Alpaca or database)"""
        try:
            return self.data_source.get_position_count()
        except Exception as e:
            logger.error(f"Failed to get position count: {e}", exc_info=True)
            return 0

    def get_deployed_capital(self) -> float:
        """Get total capital currently deployed in open/pending positions (from Alpaca or database)"""
        try:
            return self.data_source.get_deployed_capital()
        except Exception as e:
            logger.error(f"Failed to get deployed capital: {e}", exc_info=True)
            return 0.0

    def get_open_tickers(self) -> List[str]:
        """Get list of tickers for open/pending positions (from Alpaca or database)"""
        try:
            return self.data_source.get_open_tickers()
        except Exception as e:
            logger.error(f"Failed to get open tickers: {e}", exc_info=True)
            return []

    def apply_score_filter(self, candidates: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Filter out candidates below minimum composite score

        Returns:
            (accepted_candidates, rejected_candidates)
        """
        accepted = []
        rejected = []

        for candidate in candidates:
            score = candidate.get('research_composite_score', 0.0)

            if score >= self.min_composite_score:
                accepted.append(candidate)
            else:
                rejected.append({
                    'ticker': candidate['ticker'],
                    'rejection_reason': 'LOW_SCORE',
                    'rejection_category': 'SCORE',
                    'rejection_details': (
                        f"Research composite score {score:.1f}/100 is below minimum threshold {self.min_composite_score:.1f}/100. "
                        f"Only candidates scoring {self.min_composite_score:.1f}/100+ are eligible for trading."
                    ),
                    'would_be_shares': candidate.get('position_size_shares'),
                    'would_be_position_value': candidate.get('position_size_value'),
                    'would_be_risk': candidate.get('total_risk'),
                    'research_composite_score': score
                })

        logger.info(f"Score filter: {len(accepted)} passed, {len(rejected)} rejected (min score: {self.min_composite_score})")
        return accepted, rejected

    def apply_position_limits(self, candidates: List[Dict], current_positions: int) -> Tuple[List[Dict], List[Dict]]:
        """
        Enforce maximum position count

        Returns:
            (accepted_candidates, rejected_candidates)
        """
        available_slots = self.max_positions - current_positions

        if available_slots <= 0:
            # Reject all - portfolio at capacity
            open_tickers = self.get_open_tickers()
            rejected = []
            for candidate in candidates:
                rejected.append({
                    'ticker': candidate['ticker'],
                    'rejection_reason': 'MAX_POSITIONS_REACHED',
                    'rejection_category': 'CAPACITY',
                    'rejection_details': (
                        f"Portfolio is at maximum capacity ({current_positions}/{self.max_positions} positions). "
                        f"Cannot open new positions until existing positions close. "
                        f"Current positions: {', '.join(open_tickers)}"
                    ),
                    'would_be_shares': candidate.get('position_size_shares'),
                    'would_be_position_value': candidate.get('position_size_value'),
                    'would_be_risk': candidate.get('total_risk'),
                    'research_composite_score': candidate.get('research_composite_score')
                })

            logger.warning(f"Position limit: Rejected all {len(rejected)} candidates (capacity full: {current_positions}/{self.max_positions})")
            return [], rejected

        # Sort by composite score (highest first)
        sorted_candidates = sorted(candidates,
                                  key=lambda x: x.get('research_composite_score', 0.0),
                                  reverse=True)

        # Take top N that fit
        accepted = sorted_candidates[:available_slots]
        rejected_ranked_out = sorted_candidates[available_slots:]

        # Add rejection details for ranked-out candidates
        rejected = []
        for candidate in rejected_ranked_out:
            rejected.append({
                'ticker': candidate['ticker'],
                'rejection_reason': 'INSUFFICIENT_CAPACITY',
                'rejection_category': 'CAPACITY',
                'rejection_details': (
                    f"Portfolio has {available_slots} available slots out of {self.max_positions} max positions. "
                    f"This candidate (score {candidate.get('research_composite_score', 0):.1f}/100) "
                    f"ranked below the cutoff. "
                    f"Accepted candidates: {', '.join([c['ticker'] for c in accepted])}"
                ),
                'would_be_shares': candidate.get('position_size_shares'),
                'would_be_position_value': candidate.get('position_size_value'),
                'would_be_risk': candidate.get('total_risk'),
                'research_composite_score': candidate.get('research_composite_score')
            })

        logger.info(f"Position limit: {len(accepted)} accepted, {len(rejected)} rejected (slots: {available_slots}/{self.max_positions})")
        return accepted, rejected

    def apply_capital_limits(self, candidates: List[Dict], deployed_capital: float) -> Tuple[List[Dict], List[Dict]]:
        """
        Ensure we don't over-deploy capital

        Returns:
            (accepted_candidates, rejected_candidates)
        """
        max_deploy = self.total_capital * self.max_capital_deployed_pct
        available = max_deploy - deployed_capital

        accepted = []
        rejected = []

        running_total = 0

        for candidate in candidates:
            position_value = candidate.get('position_size_value', 0.0)

            if running_total + position_value <= available:
                accepted.append(candidate)
                running_total += position_value
            else:
                rejected.append({
                    'ticker': candidate['ticker'],
                    'rejection_reason': 'INSUFFICIENT_CAPITAL',
                    'rejection_category': 'CAPITAL',
                    'rejection_details': (
                        f"Insufficient capital to deploy. "
                        f"Available: ${available:,.0f}, "
                        f"Required for this position: ${position_value:,.0f}, "
                        f"Already allocated to other accepted trades: ${running_total:,.0f}. "
                        f"Total deployed capital: ${deployed_capital:,.0f} of ${max_deploy:,.0f} max."
                    ),
                    'would_be_shares': candidate.get('position_size_shares'),
                    'would_be_position_value': position_value,
                    'would_be_risk': candidate.get('total_risk'),
                    'research_composite_score': candidate.get('research_composite_score')
                })

        logger.info(f"Capital limit: {len(accepted)} accepted, {len(rejected)} rejected (available: ${available:,.0f})")
        return accepted, rejected

    def process_risk_assessment(self, risk_message_metadata: Dict, risk_data: Dict) -> Tuple[List[Dict], List[Dict]]:
        """
        Process Risk's approved candidates and decide which to buy

        Args:
            risk_message_metadata: Message metadata from Risk
            risk_data: JSON payload from RiskAssessment

        Returns:
            (accepted_candidates, rejected_candidates)
        """
        logger.info("=" * 80)
        logger.info("PROCESSING RISK ASSESSMENT")
        logger.info("=" * 80)

        approved = risk_data.get('approved_candidates', [])
        logger.info(f"Risk approved {len(approved)} candidates")

        # Get current portfolio state
        current_positions = self.get_open_positions_count()
        deployed_capital = self.get_deployed_capital()

        logger.info(f"Portfolio state: {current_positions} positions, ${deployed_capital:,.0f} deployed")

        # Apply filters in sequence
        all_rejected = []

        # Filter 1: Score filter
        candidates, rejected = self.apply_score_filter(approved)
        all_rejected.extend(rejected)

        # Filter 2: Position limits
        if len(candidates) > 0:
            candidates, rejected = self.apply_position_limits(candidates, current_positions)
            all_rejected.extend(rejected)

        # Filter 3: Capital limits
        if len(candidates) > 0:
            candidates, rejected = self.apply_capital_limits(candidates, deployed_capital)
            all_rejected.extend(rejected)

        logger.info(f"Portfolio decision: {len(candidates)} accepted, {len(all_rejected)} rejected")
        logger.info("=" * 80)

        return candidates, all_rejected

    def generate_position_id(self, ticker: str, trade_date: date) -> str:
        """
        Generate unique position ID

        Format: POS_{YYYYMMDD}_{TICKER}_{UUID8}
        Example: POS_20251031_AAPL_a7b3c2d1
        """
        date_str = trade_date.strftime('%Y%m%d')
        uuid_short = uuid.uuid4().hex[:8]
        position_id = f"POS_{date_str}_{ticker}_{uuid_short}"

        logger.debug(f"Generated position ID: {position_id}")
        return position_id

    def generate_buy_order(self, candidate: Dict, risk_message_id: str,
                          message_handler: MessageHandler) -> Tuple[str, str]:
        """
        Generate BuyOrder message for Trading Department

        Args:
            candidate: Accepted candidate from Risk
            risk_message_id: Parent RiskAssessment message ID
            message_handler: MessageHandler instance for writing message

        Returns:
            (buy_order_message_id, position_id)
        """
        ticker = candidate['ticker']

        # Generate position ID
        position_id = self.generate_position_id(ticker, date.today())

        # Build markdown body
        body_lines = [
            f"**Order Type**: BUY",
            f"**Position ID**: {position_id}",
            "",
            "## Order Details",
            f"- **Ticker**: {ticker}",
            f"- **Shares**: {candidate['position_size_shares']}",
            f"- **Order Type**: MARKET",
            f"- **Stop-Loss**: ${candidate['stop_loss']:.2f}",
            f"- **Target**: ${candidate['target_price']:.2f}",
            "",
            "## Risk Parameters",
            f"- **Risk Per Share**: ${candidate['risk_per_share']:.2f}",
            f"- **Total Risk**: ${candidate['total_risk']:.2f} ({candidate['risk_percentage']*100:.2f}% of capital)",
            f"- **Risk-Reward**: {candidate['risk_reward_ratio']:.1f}:1",
            "",
            "## Context",
            f"- **Research Score**: {candidate['research_composite_score']:.1f}/100",
            f"- **Sector**: {candidate.get('sector', 'Unknown')}",
            f"- **Entry Reason**: Passed all risk checks, portfolio has capacity"
        ]

        body = "\n".join(body_lines)

        # Build JSON payload
        data_payload = {
            'order_type': 'BUY',
            'ticker': ticker,
            'shares': candidate['position_size_shares'],
            'execution_type': 'MARKET',
            'limit_price': None,
            'stop_loss': candidate['stop_loss'],
            'target_price': candidate['target_price'],
            'position_id': position_id,
            'risk_per_share': candidate['risk_per_share'],
            'total_risk': candidate['total_risk'],
            'timeout_seconds': 300
        }

        # Write message
        message_id = message_handler.write_message(
            to_dept='TRADING',
            message_type='TradeOrder',
            subject=f"Trade Order - BUY {ticker}",
            body=body,
            data_payload=data_payload,
            parent_message_id=risk_message_id,
            priority='high',
            requires_response=True
        )

        logger.info(f"BuyOrder generated: {message_id} for {ticker} (position: {position_id})")
        return message_id, position_id


class ExitSignalGenerator:
    """
    Monitors open positions for exit signals

    Exit Conditions:
    1. Stop-Loss Hit: current_price <= stop_loss
    2. Target Hit: current_price >= target_price
    3. Time-Based: days_held > max_hold_days
    4. Research Downgrade: new Research score < threshold
    """

    def __init__(self, config: Dict, db_path: Path):
        self.config = config
        self.db_path = db_path

        # Load exit rules from config
        self.max_hold_days = config['exits']['max_hold_days']
        self.downgrade_threshold = config['exits']['downgrade_score']
        self.exit_priority = config['exits']['priority']

        logger.info(f"ExitSignalGenerator initialized (max hold: {self.max_hold_days} days, "
                   f"downgrade threshold: {self.downgrade_threshold})")

    def get_open_positions(self) -> List[Dict]:
        """Get all open positions from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT position_id, ticker, intended_shares, actual_shares,
                       intended_entry_price, actual_entry_price, actual_entry_date,
                       intended_stop_loss, intended_target, sector
                FROM portfolio_positions
                WHERE status = 'OPEN'
                ORDER BY actual_entry_date
            """)

            positions = []
            for row in cursor.fetchall():
                positions.append({
                    'position_id': row[0],
                    'ticker': row[1],
                    'intended_shares': row[2],
                    'actual_shares': row[3],
                    'intended_entry_price': row[4],
                    'actual_entry_price': row[5],
                    'actual_entry_date': datetime.strptime(row[6], '%Y-%m-%d').date() if row[6] else None,
                    'stop_loss': row[7],
                    'target_price': row[8],
                    'sector': row[9]
                })

            conn.close()
            return positions

        except Exception as e:
            logger.error(f"Failed to get open positions: {e}", exc_info=True)
            return []

    def fetch_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        Fetch current prices for multiple tickers

        Returns:
            Dict mapping ticker -> current_price
        """
        prices = {}

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period='1d')

                if len(hist) > 0:
                    current_price = hist['Close'].iloc[-1]
                    prices[ticker] = float(current_price)
                    logger.debug(f"{ticker}: Current price ${current_price:.2f}")
                else:
                    logger.warning(f"{ticker}: No price data available")

            except Exception as e:
                logger.error(f"Failed to fetch price for {ticker}: {e}")

        return prices

    def get_latest_research_score(self, ticker: str) -> Optional[float]:
        """
        Get most recent Research composite score for ticker

        Returns:
            Latest composite score or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT quick_score
                FROM research_candidate_tickers
                WHERE ticker = ?
                ORDER BY screening_date DESC
                LIMIT 1
            """)

            result = cursor.fetchone()
            conn.close()

            if result:
                return float(result[0])
            else:
                return None

        except Exception as e:
            logger.error(f"Failed to get Research score for {ticker}: {e}", exc_info=True)
            return None

    def check_exit_conditions(self, position: Dict, current_price: float) -> Optional[Dict]:
        """
        Check if any exit condition is triggered

        Args:
            position: Position dict
            current_price: Current market price

        Returns:
            Exit signal dict or None
        """
        ticker = position['ticker']

        # Condition 1: Stop-loss hit
        if current_price <= position['stop_loss']:
            return {
                'reason': 'STOP_LOSS',
                'priority': 1,
                'details': (
                    f"Price ${current_price:.2f} hit stop-loss ${position['stop_loss']:.2f}. "
                    f"Protecting capital - closing position to limit loss."
                ),
                'exit_price': current_price
            }

        # Condition 2: Target hit
        if current_price >= position['target_price']:
            return {
                'reason': 'TARGET',
                'priority': 2,
                'details': (
                    f"Price ${current_price:.2f} hit target ${position['target_price']:.2f}. "
                    f"Taking profit at target price."
                ),
                'exit_price': current_price
            }

        # Condition 3: Time-based exit
        if position['actual_entry_date']:
            days_held = (date.today() - position['actual_entry_date']).days

            if days_held > self.max_hold_days:
                return {
                    'reason': 'TIME',
                    'priority': 4,
                    'details': (
                        f"Position held {days_held} days, exceeds maximum {self.max_hold_days} days. "
                        f"Closing position to free up capital for new opportunities."
                    ),
                    'exit_price': current_price
                }

        # Condition 4: Research downgrade
        latest_score = self.get_latest_research_score(ticker)
        if latest_score and latest_score < self.downgrade_threshold:
            return {
                'reason': 'DOWNGRADE',
                'priority': 3,
                'details': (
                    f"Research score downgraded to {latest_score:.1f}, below threshold {self.downgrade_threshold:.1f}. "
                    f"Fundamentals deteriorated - exiting position."
                ),
                'exit_price': current_price
            }

        # No exit triggered
        return None

    def check_all_exits(self) -> List[Tuple[Dict, Dict]]:
        """
        Check all open positions for exit signals

        Returns:
            List of (position, exit_signal) tuples
        """
        logger.info("=" * 80)
        logger.info("CHECKING EXIT SIGNALS")
        logger.info("=" * 80)

        open_positions = self.get_open_positions()
        logger.info(f"Monitoring {len(open_positions)} open positions")

        if len(open_positions) == 0:
            logger.info("No open positions to monitor")
            logger.info("=" * 80)
            return []

        # Fetch current prices for all tickers
        tickers = [p['ticker'] for p in open_positions]
        current_prices = self.fetch_current_prices(tickers)

        # Check each position for exit signals
        exits_triggered = []

        for position in open_positions:
            ticker = position['ticker']
            current_price = current_prices.get(ticker)

            if not current_price:
                logger.warning(f"{ticker}: No price data, skipping exit check")
                continue

            # Check exit conditions
            exit_signal = self.check_exit_conditions(position, current_price)

            if exit_signal:
                exits_triggered.append((position, exit_signal))
                logger.info(f"{ticker}: EXIT TRIGGERED - {exit_signal['reason']} - {exit_signal['details']}")
            else:
                logger.debug(f"{ticker}: No exit conditions met (price: ${current_price:.2f})")

        logger.info(f"Exit check complete: {len(exits_triggered)} exits triggered")
        logger.info("=" * 80)

        return exits_triggered

    def generate_sell_order(self, position: Dict, exit_signal: Dict,
                           message_handler: MessageHandler) -> str:
        """
        Generate SellOrder message for Trading Department

        Args:
            position: Position being closed
            exit_signal: Exit signal details
            message_handler: MessageHandler instance

        Returns:
            sell_order_message_id
        """
        ticker = position['ticker']
        shares = position['actual_shares'] or position['intended_shares']

        # Calculate performance if we have entry price
        entry_price = position['actual_entry_price'] or position['intended_entry_price']
        exit_price = exit_signal['exit_price']
        gain_per_share = exit_price - entry_price
        total_gain = gain_per_share * shares
        return_pct = (gain_per_share / entry_price * 100) if entry_price > 0 else 0

        # Calculate days held
        days_held = 0
        if position['actual_entry_date']:
            days_held = (date.today() - position['actual_entry_date']).days

        # Build markdown body
        body_lines = [
            f"**Order Type**: SELL",
            f"**Position ID**: {position['position_id']}",
            f"**Exit Reason**: {exit_signal['reason']}",
            "",
            "## Order Details",
            f"- **Ticker**: {ticker}",
            f"- **Shares**: {shares} (close full position)",
            f"- **Order Type**: MARKET",
            f"- **Current Price**: ${exit_price:.2f}",
            "",
            "## Exit Signal",
            f"- **Reason**: {exit_signal['reason']}",
            f"- **Details**: {exit_signal['details']}",
            "",
            "## Performance",
            f"- **Entry**: ${entry_price:.2f}",
            f"- **Exit**: ${exit_price:.2f} (estimated)",
            f"- **Gain**: ${gain_per_share:.2f}/share × {shares} = ${total_gain:.2f}",
            f"- **Return**: {return_pct:+.2f}%",
            f"- **Days Held**: {days_held}"
        ]

        body = "\n".join(body_lines)

        # Build JSON payload
        data_payload = {
            'order_type': 'SELL',
            'ticker': ticker,
            'shares': shares,
            'execution_type': 'MARKET',
            'position_id': position['position_id'],
            'exit_reason': exit_signal['reason'],
            'exit_price': exit_price,
            'timeout_seconds': 60  # Exits are urgent, shorter timeout
        }

        # Write message
        message_id = message_handler.write_message(
            to_dept='TRADING',
            message_type='TradeOrder',
            subject=f"Trade Order - SELL {ticker}",
            body=body,
            data_payload=data_payload,
            parent_message_id=position['position_id'],
            priority='urgent',  # Exits are urgent
            requires_response=True
        )

        logger.info(f"SellOrder generated: {message_id} for {ticker} ({exit_signal['reason']})")
        return message_id


# ============================================================================
# CLASS 4: POSITION TRACKER (Day 3)
# ============================================================================
class PositionTracker:
    """
    Tracks position lifecycle: PENDING → OPEN → CLOSED
    Handles fill confirmations, partial fills, and reconciliation
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_pending_position(self,
                               candidate: Dict,
                               order_message_id: str,
                               risk_assessment_message_id: str) -> str:
        """
        Create new position with status='PENDING' after BuyOrder sent

        Args:
            candidate: Approved candidate dict with ticker, entry, shares, etc.
            order_message_id: The BuyOrder message_id sent to Trading
            risk_assessment_message_id: Parent RiskAssessment message_id

        Returns:
            position_id: The position_id that was created
        """
        position_id = candidate['position_id']
        ticker = candidate['ticker']

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO portfolio_positions (
                    position_id,
                    ticker,
                    status,
                    intended_entry_price,
                    intended_shares,
                    intended_stop_loss,
                    intended_target,
                    risk_per_share,
                    total_risk,
                    sector,
                    entry_order_message_id,
                    risk_assessment_message_id,
                    created_at,
                    updated_at
                ) VALUES (?, ?, 'PENDING', ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                position_id,
                ticker,
                candidate['entry_price'],
                candidate['shares'],
                candidate['stop_loss'],
                candidate['target_price'],
                candidate.get('risk_per_share', 0.0),
                candidate.get('total_risk', 0.0),
                candidate.get('sector', 'Unknown'),
                order_message_id,
                risk_assessment_message_id
            ))

            conn.commit()
            self.logger.info(f"Position created: {position_id} - {ticker} (PENDING)")

        except sqlite3.IntegrityError as e:
            self.logger.error(f"Position already exists: {position_id}")
            raise
        finally:
            conn.close()

        return position_id

    def update_position_on_fill(self,
                               position_id: str,
                               fill_data: Dict) -> bool:
        """
        Update position to OPEN status when FillConfirmation received
        Handles both full and partial fills

        Args:
            position_id: Position to update
            fill_data: Dict with fill details:
                - filled_shares: int (how many shares filled)
                - fill_price: float (average fill price)
                - fill_date: str (ISO date)
                - fill_message_id: str (Trading's FillConfirmation message_id)

        Returns:
            success: True if updated, False if position not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if position exists and is PENDING
            cursor.execute("""
                SELECT position_id, intended_shares, ticker
                FROM portfolio_positions
                WHERE position_id = ? AND status = 'PENDING'
            """, (position_id,))

            row = cursor.fetchone()
            if not row:
                self.logger.warning(f"Position {position_id} not found or not PENDING")
                return False

            intended_shares = row[1]
            ticker = row[2]
            filled_shares = fill_data['filled_shares']

            # Determine if partial fill
            is_partial = filled_shares < intended_shares

            # Update position
            cursor.execute("""
                UPDATE portfolio_positions
                SET status = 'OPEN',
                    actual_entry_price = ?,
                    actual_entry_date = ?,
                    actual_shares = ?,
                    fill_message_id = ?,
                    updated_at = datetime('now')
                WHERE position_id = ?
            """, (
                fill_data['fill_price'],
                fill_data['fill_date'],
                filled_shares,
                fill_data['fill_message_id'],
                position_id
            ))

            conn.commit()

            if is_partial:
                self.logger.warning(
                    f"PARTIAL FILL: {position_id} - {ticker} - "
                    f"{filled_shares}/{intended_shares} shares @ ${fill_data['fill_price']:.2f}"
                )
            else:
                self.logger.info(
                    f"FULL FILL: {position_id} - {ticker} - "
                    f"{filled_shares} shares @ ${fill_data['fill_price']:.2f}"
                )

            return True

        finally:
            conn.close()

    def close_position(self,
                      position_id: str,
                      exit_data: Dict) -> bool:
        """
        Close position when SellOrder filled

        Args:
            position_id: Position to close
            exit_data: Dict with exit details:
                - exit_price: float
                - exit_date: str (ISO date)
                - exit_reason: str (STOP_LOSS, TARGET, DOWNGRADE, TIME)
                - exit_message_id: str (SellOrder message_id)

        Returns:
            success: True if closed, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Verify position exists and is OPEN
            cursor.execute("""
                SELECT position_id, ticker, actual_shares, actual_entry_price, actual_entry_date
                FROM portfolio_positions
                WHERE position_id = ? AND status = 'OPEN'
            """, (position_id,))

            row = cursor.fetchone()
            if not row:
                self.logger.warning(f"Position {position_id} not found or not OPEN")
                return False

            ticker = row[1]
            shares = row[2]
            entry_price = row[3]
            entry_date = row[4]

            # Calculate performance
            exit_price = exit_data['exit_price']
            gain_per_share = exit_price - entry_price
            total_gain = gain_per_share * shares
            return_pct = (gain_per_share / entry_price) * 100

            # Calculate days held
            entry_dt = datetime.fromisoformat(entry_date)
            exit_dt = datetime.fromisoformat(exit_data['exit_date'])
            days_held = (exit_dt - entry_dt).days

            # Update position
            cursor.execute("""
                UPDATE portfolio_positions
                SET status = 'CLOSED',
                    exit_reason = ?,
                    exit_price = ?,
                    exit_date = ?,
                    exit_order_message_id = ?,
                    updated_at = datetime('now')
                WHERE position_id = ?
            """, (
                exit_data['exit_reason'],
                exit_price,
                exit_data['exit_date'],
                exit_data['exit_message_id'],
                position_id
            ))

            conn.commit()

            self.logger.info(
                f"Position CLOSED: {position_id} - {ticker} - "
                f"${entry_price:.2f} → ${exit_price:.2f} - "
                f"{return_pct:+.2f}% over {days_held} days - "
                f"Reason: {exit_data['exit_reason']}"
            )

            return True

        finally:
            conn.close()

    def reconcile_with_trading(self) -> Dict[str, List[str]]:
        """
        Check for stale PENDING positions and price discrepancies

        Returns:
            issues: Dict with keys 'stale_pending', 'price_discrepancies'
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        issues = {
            'stale_pending': [],
            'price_discrepancies': []
        }

        try:
            # Find PENDING positions older than 1 hour
            cursor.execute("""
                SELECT position_id, ticker, created_at
                FROM portfolio_positions
                WHERE status = 'PENDING'
                AND datetime(created_at, '+1 hour') < datetime('now')
            """)

            stale_rows = cursor.fetchall()
            for row in stale_rows:
                position_id, ticker, created_at = row
                age_hours = (datetime.now() - datetime.fromisoformat(created_at)).total_seconds() / 3600

                issues['stale_pending'].append(position_id)
                self.logger.warning(
                    f"STALE PENDING: {position_id} - {ticker} - "
                    f"created {age_hours:.1f} hours ago"
                )

            # Check for price discrepancies (intended vs actual > 5%)
            cursor.execute("""
                SELECT position_id, ticker, intended_entry_price, actual_entry_price
                FROM portfolio_positions
                WHERE status = 'OPEN'
                AND actual_entry_price IS NOT NULL
                AND abs((actual_entry_price - intended_entry_price) / intended_entry_price) > 0.05
            """)

            discrepancy_rows = cursor.fetchall()
            for row in discrepancy_rows:
                position_id, ticker, intended, actual = row
                diff_pct = ((actual - intended) / intended) * 100

                issues['price_discrepancies'].append(position_id)
                self.logger.warning(
                    f"PRICE DISCREPANCY: {position_id} - {ticker} - "
                    f"intended ${intended:.2f} vs actual ${actual:.2f} ({diff_pct:+.1f}%)"
                )

        finally:
            conn.close()

        return issues

    def get_position_details(self, position_id: str) -> Optional[Dict]:
        """
        Retrieve all details for a specific position

        Args:
            position_id: Position to look up

        Returns:
            position_dict or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM portfolio_positions
                WHERE position_id = ?
            """, (position_id,))

            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

        finally:
            conn.close()

    def get_portfolio_summary(self) -> Dict:
        """
        Get current portfolio status summary

        Returns:
            summary: Dict with counts, capital deployed, performance metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Count positions by status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM portfolio_positions
                GROUP BY status
            """)

            status_counts = {row[0]: row[1] for row in cursor.fetchall()}

            # Calculate deployed capital (OPEN positions)
            cursor.execute("""
                SELECT SUM(actual_entry_price * actual_shares) as deployed
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)

            deployed = cursor.fetchone()[0] or 0.0

            # Calculate unrealized P&L for OPEN positions
            cursor.execute("""
                SELECT ticker, actual_shares, actual_entry_price
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)

            open_positions = cursor.fetchall()

            # Fetch current prices for open positions
            if open_positions:
                tickers = [row[0] for row in open_positions]
                current_prices = self._fetch_current_prices(tickers)

                unrealized_pnl = 0.0
                for ticker, shares, entry_price in open_positions:
                    current_price = current_prices.get(ticker, entry_price)
                    unrealized_pnl += (current_price - entry_price) * shares
            else:
                unrealized_pnl = 0.0

            # Calculate realized P&L for CLOSED positions
            cursor.execute("""
                SELECT SUM((exit_price - actual_entry_price) * actual_shares) as realized
                FROM portfolio_positions
                WHERE status = 'CLOSED'
                AND exit_price IS NOT NULL
                AND actual_entry_price IS NOT NULL
            """)

            realized_pnl = cursor.fetchone()[0] or 0.0

            summary = {
                'pending_positions': status_counts.get('PENDING', 0),
                'open_positions': status_counts.get('OPEN', 0),
                'closed_positions': status_counts.get('CLOSED', 0),
                'rejected_positions': status_counts.get('REJECTED', 0),
                'capital_deployed': deployed,
                'unrealized_pnl': unrealized_pnl,
                'realized_pnl': realized_pnl,
                'total_pnl': unrealized_pnl + realized_pnl
            }

            return summary

        finally:
            conn.close()

    def _fetch_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        """Fetch current prices using yfinance (batch)"""
        import yfinance as yf

        prices = {}
        try:
            data = yf.download(tickers, period='1d', progress=False)

            if len(tickers) == 1:
                ticker = tickers[0]
                if not data.empty and 'Close' in data.columns:
                    prices[ticker] = float(data['Close'].iloc[-1])
            else:
                if not data.empty and 'Close' in data.columns:
                    for ticker in tickers:
                        try:
                            prices[ticker] = float(data['Close'][ticker].iloc[-1])
                        except:
                            self.logger.warning(f"Could not fetch price for {ticker}")
        except Exception as e:
            self.logger.error(f"Error fetching prices: {e}")

        return prices


# ============================================================================
# CLASS 5: PORTFOLIO REBALANCER (Day 4)
# ============================================================================
class PortfolioRebalancer:
    """
    Monitors portfolio deployment and requests new candidates when under-deployed
    Ensures capital stays fully invested per target allocation
    """

    def __init__(self, config: Dict, db_path: Path):
        self.db_path = db_path
        self.logger = logging.getLogger(self.__class__.__name__)

        # Load configuration
        self.total_capital = config['capital']['total']
        self.target_deployment_pct = config['limits']['max_capital_deployed_pct']
        self.max_positions = config['limits']['max_positions']

        # Rebalancing thresholds
        self.min_deployment_threshold = config.get('rebalancing', {}).get('min_deployment_threshold', 0.90)
        self.rebalance_buffer_pct = config.get('rebalancing', {}).get('buffer_pct', 0.05)

    def check_deployment_status(self) -> Dict:
        """
        Check current capital deployment vs target

        Returns:
            status: Dict with deployment metrics and rebalancing recommendation
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Count positions by status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM portfolio_positions
                GROUP BY status
            """)

            status_counts = {row[0]: row[1] for row in cursor.fetchall()}
            open_positions = status_counts.get('OPEN', 0)
            pending_positions = status_counts.get('PENDING', 0)

            # Calculate deployed capital (OPEN + PENDING)
            cursor.execute("""
                SELECT SUM(actual_entry_price * actual_shares) as deployed_open
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)
            deployed_open = cursor.fetchone()[0] or 0.0

            cursor.execute("""
                SELECT SUM(intended_entry_price * intended_shares) as deployed_pending
                FROM portfolio_positions
                WHERE status = 'PENDING'
            """)
            deployed_pending = cursor.fetchone()[0] or 0.0

            total_deployed = deployed_open + deployed_pending

            # Calculate metrics
            target_capital = self.total_capital * self.target_deployment_pct
            deployment_pct = (total_deployed / self.total_capital) if self.total_capital > 0 else 0.0
            available_capital = target_capital - total_deployed
            available_positions = self.max_positions - (open_positions + pending_positions)

            # Determine if rebalancing needed
            under_deployed = deployment_pct < (self.target_deployment_pct * self.min_deployment_threshold)
            has_capacity = available_positions > 0 and available_capital > 0

            needs_rebalancing = under_deployed and has_capacity

            status = {
                'timestamp': datetime.now().isoformat(),
                'open_positions': open_positions,
                'pending_positions': pending_positions,
                'total_positions': open_positions + pending_positions,
                'max_positions': self.max_positions,
                'deployed_capital': total_deployed,
                'target_capital': target_capital,
                'available_capital': max(0, available_capital),
                'deployment_pct': deployment_pct,
                'target_deployment_pct': self.target_deployment_pct,
                'under_deployed': under_deployed,
                'has_capacity': has_capacity,
                'needs_rebalancing': needs_rebalancing,
                'available_positions': max(0, available_positions)
            }

            if needs_rebalancing:
                self.logger.info(
                    f"REBALANCING NEEDED: Deployed {deployment_pct:.1%} vs target {self.target_deployment_pct:.1%}, "
                    f"{available_positions} positions available, ${available_capital:,.0f} capital available"
                )
            else:
                self.logger.info(
                    f"Portfolio status OK: {deployment_pct:.1%} deployed, "
                    f"{open_positions + pending_positions}/{self.max_positions} positions"
                )

            return status

        finally:
            conn.close()

    def generate_candidate_request(self, message_handler: MessageHandler) -> str:
        """
        Generate message to Research Department requesting new candidates

        Args:
            message_handler: MessageHandler instance for writing messages

        Returns:
            message_id: The CandidateRequest message ID
        """
        # Get current deployment status
        status = self.check_deployment_status()

        # Build request message
        subject = "Candidate Request - Portfolio Under-Deployed"

        body_lines = [
            "# Candidate Request",
            "",
            "The Portfolio Department requires additional stock candidates to maintain target capital deployment.",
            "",
            "## Current Portfolio Status",
            f"- **Current Deployment**: {status['deployment_pct']:.1%}",
            f"- **Target Deployment**: {status['target_deployment_pct']:.1%}",
            f"- **Deployed Capital**: ${status['deployed_capital']:,.0f}",
            f"- **Available Capital**: ${status['available_capital']:,.0f}",
            f"- **Open Positions**: {status['open_positions']}/{status['max_positions']}",
            f"- **Pending Positions**: {status['pending_positions']}",
            "",
            "## Request Parameters",
            f"- **Available Position Slots**: {status['available_positions']}",
            f"- **Capital Available for New Positions**: ${status['available_capital']:,.0f}",
            f"- **Minimum Composite Score**: 6.0",
            "",
            "## Action Required",
            "Please run daily screening and provide candidates that:",
            "1. Meet minimum composite score threshold (6.0+)",
            "2. Pass sector diversification requirements",
            "3. Fit within available capital constraints",
            "",
            "Priority: **High** - Portfolio is significantly under-deployed"
        ]

        body = "\n".join(body_lines)

        # Build JSON payload
        data_payload = {
            'request_type': 'CANDIDATE_REQUEST',
            'deployment_status': {
                'current_deployment_pct': status['deployment_pct'],
                'target_deployment_pct': status['target_deployment_pct'],
                'available_capital': status['available_capital'],
                'available_positions': status['available_positions']
            },
            'criteria': {
                'min_composite_score': 6.0,
                'max_candidates': status['available_positions'],
                'require_sector_diversification': True
            }
        }

        # Write message to Research Department
        message_id = message_handler.write_message(
            to_dept='RESEARCH',
            message_type='CandidateRequest',
            subject=subject,
            body=body,
            data_payload=data_payload,
            priority='high',
            requires_response=True
        )

        self.logger.info(f"Candidate request sent to Research: {message_id}")
        return message_id

    def check_sector_concentration(self) -> Dict[str, float]:
        """
        Calculate sector concentration in current portfolio

        Returns:
            sector_weights: Dict mapping sector -> weight percentage
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get total portfolio value
            cursor.execute("""
                SELECT SUM(actual_entry_price * actual_shares) as total
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)

            total_value = cursor.fetchone()[0] or 0.0

            if total_value == 0:
                return {}

            # Calculate sector weights
            cursor.execute("""
                SELECT sector, SUM(actual_entry_price * actual_shares) as sector_value
                FROM portfolio_positions
                WHERE status = 'OPEN'
                GROUP BY sector
            """)

            sector_weights = {}
            for sector, value in cursor.fetchall():
                if sector and value:
                    sector_weights[sector] = (value / total_value)

            # Log if any sector is over-concentrated (>30%)
            for sector, weight in sector_weights.items():
                if weight > 0.30:
                    self.logger.warning(
                        f"SECTOR CONCENTRATION: {sector} is {weight:.1%} of portfolio (>30% threshold)"
                    )

            return sector_weights

        finally:
            conn.close()

    def generate_rebalancing_report(self) -> Dict:
        """
        Generate comprehensive rebalancing report

        Returns:
            report: Dict with deployment status, sector allocation, recommendations
        """
        deployment_status = self.check_deployment_status()
        sector_allocation = self.check_sector_concentration()

        # Calculate position metrics
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Average position size
            cursor.execute("""
                SELECT AVG(actual_entry_price * actual_shares) as avg_size,
                       MIN(actual_entry_price * actual_shares) as min_size,
                       MAX(actual_entry_price * actual_shares) as max_size
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)

            row = cursor.fetchone()
            avg_size = row[0] or 0.0
            min_size = row[1] or 0.0
            max_size = row[2] or 0.0

            # Position concentration (largest position as % of portfolio)
            largest_position_pct = (max_size / deployment_status['deployed_capital']) if deployment_status['deployed_capital'] > 0 else 0.0

            report = {
                'timestamp': datetime.now().isoformat(),
                'deployment': deployment_status,
                'sector_allocation': sector_allocation,
                'position_metrics': {
                    'average_size': avg_size,
                    'min_size': min_size,
                    'max_size': max_size,
                    'largest_position_pct': largest_position_pct
                },
                'recommendations': []
            }

            # Generate recommendations
            if deployment_status['needs_rebalancing']:
                report['recommendations'].append({
                    'priority': 'HIGH',
                    'action': 'REQUEST_CANDIDATES',
                    'reason': f"Portfolio {deployment_status['deployment_pct']:.1%} deployed vs {deployment_status['target_deployment_pct']:.1%} target"
                })

            if largest_position_pct > 0.15:
                report['recommendations'].append({
                    'priority': 'MEDIUM',
                    'action': 'POSITION_SIZING_REVIEW',
                    'reason': f"Largest position is {largest_position_pct:.1%} of portfolio (>15% threshold)"
                })

            for sector, weight in sector_allocation.items():
                if weight > 0.30:
                    report['recommendations'].append({
                        'priority': 'MEDIUM',
                        'action': 'SECTOR_DIVERSIFICATION',
                        'reason': f"{sector} is {weight:.1%} of portfolio (>30% threshold)"
                    })

            return report

        finally:
            conn.close()


# ============================================================================
# CLASS 6: PORTFOLIO DEPARTMENT - MAIN ORCHESTRATOR (Day 5)
# ============================================================================
class PortfolioDepartment:
    """
    Main orchestrator for Portfolio Department
    Ties together all 5 components into daily workflow:
    1. PortfolioDecisionEngine: Makes buy decisions
    2. ExitSignalGenerator: Makes sell decisions
    3. PositionTracker: Manages position lifecycle
    4. PortfolioRebalancer: Monitors deployment
    5. MessageHandler: Inter-department communication
    """

    def __init__(self, config_path: Path, db_path: Path):
        self.logger = logging.getLogger(self.__class__.__name__)

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.db_path = db_path

        # Initialize all components
        self.message_handler = MessageHandler()
        self.decision_engine = PortfolioDecisionEngine(self.config, db_path)
        self.exit_generator = ExitSignalGenerator(self.config, db_path)
        self.position_tracker = PositionTracker(db_path)
        self.rebalancer = PortfolioRebalancer(self.config, db_path)

        self.logger.info("Portfolio Department initialized")

    def run_daily_cycle(self):
        """
        Execute complete daily Portfolio workflow

        1. Process RiskAssessment messages (buy decisions)
        2. Check exit signals (sell decisions)
        3. Update position states (reconciliation)
        4. Check rebalancing needs
        5. Generate summary report
        """
        self.logger.info("=" * 80)
        self.logger.info("PORTFOLIO DEPARTMENT - DAILY CYCLE START")
        self.logger.info("=" * 80)

        # Step 1: Process buy decisions from Risk
        self._process_buy_decisions()

        # Step 2: Check exit signals
        self._process_exit_signals()

        # Step 3: Reconcile positions
        self._reconcile_positions()

        # Step 4: Check rebalancing
        self._check_rebalancing()

        # Step 5: Generate summary
        self._generate_daily_summary()

        self.logger.info("=" * 80)
        self.logger.info("PORTFOLIO DEPARTMENT - DAILY CYCLE COMPLETE")
        self.logger.info("=" * 80)

    def _process_buy_decisions(self):
        """Process RiskAssessment messages and generate BuyOrders"""
        self.logger.info("STEP 1: Processing Buy Decisions")

        # Read RiskAssessment messages from inbox
        risk_messages = self._read_risk_assessments()

        if len(risk_messages) == 0:
            self.logger.info("  No RiskAssessment messages to process")
            return

        self.logger.info(f"  Found {len(risk_messages)} RiskAssessment messages")

        for risk_msg in risk_messages:
            self._process_single_risk_assessment(risk_msg)

    def _read_risk_assessments(self) -> List[Tuple[Dict, Dict, Path]]:
        """Read unprocessed RiskAssessment messages from inbox"""
        inbox_path = self.message_handler.inbox_path
        messages = []

        if not inbox_path.exists():
            self.logger.warning(f"Inbox path does not exist: {inbox_path}")
            return messages

        for msg_file in inbox_path.glob("MSG_RISK_*.md"):
            try:
                metadata, body, data = self.message_handler.read_message(msg_file)

                # Only process RiskAssessment messages
                if metadata.get('message_type') == 'RiskAssessment':
                    messages.append((metadata, data, msg_file))

            except Exception as e:
                self.logger.error(f"  Failed to read {msg_file.name}: {e}")

        return messages

    def _process_single_risk_assessment(self, risk_msg: Tuple[Dict, Dict, Path]):
        """Process one RiskAssessment message"""
        metadata, data, msg_file = risk_msg

        self.logger.info(f"  Processing: {metadata['message_id']}")

        # Extract candidates from data payload
        candidates = data.get('approved_candidates', [])

        if not candidates:
            self.logger.info("    No candidates in this RiskAssessment")
            return

        # Get current portfolio state
        summary = self.position_tracker.get_portfolio_summary()
        current_positions = summary['open_positions'] + summary['pending_positions']
        deployed_capital = summary['capital_deployed']

        # Apply portfolio filters
        # Step 1: Score filter
        accepted, rejected = self.decision_engine.apply_score_filter(candidates)

        # Step 2: Position limit filter
        if accepted:
            accepted, position_rejected = self.decision_engine.apply_position_limits(
                accepted, current_positions
            )
            rejected.extend(position_rejected)

        # Step 3: Capital limit filter
        if accepted:
            accepted, capital_rejected = self.decision_engine.apply_capital_limits(
                accepted, deployed_capital
            )
            rejected.extend(capital_rejected)

        self.logger.info(f"    Candidates: {len(candidates)} total, {len(accepted)} accepted, {len(rejected)} rejected")

        # Generate BuyOrders for accepted candidates
        for candidate in accepted:
            # Add position_id to candidate
            candidate['position_id'] = self.decision_engine.generate_position_id(
                candidate['ticker'],
                date.today()
            )

            # Generate BuyOrder message
            msg_id, pos_id = self.decision_engine.generate_buy_order(
                candidate,
                metadata['message_id'],
                self.message_handler
            )

            # Create PENDING position in database
            self.position_tracker.create_pending_position(
                candidate,
                msg_id,
                metadata['message_id']
            )

            self.logger.info(f"    BuyOrder generated: {pos_id} - {candidate['ticker']}")

        # Log rejections to database
        if rejected:
            self._log_portfolio_rejections(rejected, metadata['message_id'])

        # Log overall decision to database
        self._log_portfolio_decision(
            metadata,
            accepted,
            rejected,
            current_positions,
            deployed_capital
        )

    def _process_exit_signals(self):
        """Check all open positions for exit signals"""
        self.logger.info("STEP 2: Checking Exit Signals")

        exits = self.exit_generator.check_all_exits()

        if len(exits) == 0:
            self.logger.info("  No exit signals triggered")
            return

        self.logger.info(f"  Found {len(exits)} exit signals")

        for position, signal in exits:
            # Generate SellOrder
            msg_id = self.exit_generator.generate_sell_order(
                position,
                signal,
                self.message_handler
            )

            self.logger.info(
                f"  SellOrder generated: {position['position_id']} - "
                f"{position['ticker']} ({signal['reason']})"
            )

    def _reconcile_positions(self):
        """Check for stale positions and discrepancies"""
        self.logger.info("STEP 3: Reconciling Positions")

        issues = self.position_tracker.reconcile_with_trading()

        if issues['stale_pending']:
            self.logger.warning(
                f"  Found {len(issues['stale_pending'])} stale PENDING positions"
            )

        if issues['price_discrepancies']:
            self.logger.warning(
                f"  Found {len(issues['price_discrepancies'])} price discrepancies"
            )

        if not issues['stale_pending'] and not issues['price_discrepancies']:
            self.logger.info("  No issues found - all positions reconciled")

    def _check_rebalancing(self):
        """Check if portfolio needs rebalancing"""
        self.logger.info("STEP 4: Checking Rebalancing Needs")

        status = self.rebalancer.check_deployment_status()

        if status['needs_rebalancing']:
            self.logger.info(
                f"  Portfolio under-deployed ({status['deployment_pct']:.1%}) - "
                "requesting candidates"
            )
            self.rebalancer.generate_candidate_request(self.message_handler)
        else:
            self.logger.info(
                f"  Portfolio adequately deployed: {status['deployment_pct']:.1%}"
            )

    def _generate_daily_summary(self):
        """Generate end-of-day summary report"""
        self.logger.info("STEP 5: Generating Daily Summary")

        summary = self.position_tracker.get_portfolio_summary()

        self.logger.info("  Portfolio Status:")
        self.logger.info(f"    PENDING: {summary['pending_positions']}")
        self.logger.info(f"    OPEN: {summary['open_positions']}")
        self.logger.info(f"    CLOSED: {summary['closed_positions']}")
        self.logger.info(f"    Deployed Capital: ${summary['capital_deployed']:,.2f}")
        self.logger.info(f"    Unrealized P&L: ${summary['unrealized_pnl']:,.2f}")
        self.logger.info(f"    Realized P&L: ${summary['realized_pnl']:,.2f}")
        self.logger.info(f"    Total P&L: ${summary['total_pnl']:,.2f}")

    def _log_portfolio_rejections(self, rejected: List[Dict], decision_msg_id: str):
        """Log rejected candidates to portfolio_rejections table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            for rejection in rejected:
                cursor.execute("""
                    INSERT INTO portfolio_rejections (
                        decision_message_id,
                        ticker,
                        decision_date,
                        rejection_reason,
                        rejection_category,
                        rejection_details,
                        would_be_shares,
                        would_be_position_value,
                        would_be_risk,
                        research_composite_score,
                        decision_timestamp
                    ) VALUES (?, ?, date('now'), ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    decision_msg_id,
                    rejection['ticker'],
                    rejection['rejection_reason'],
                    rejection['rejection_category'],
                    rejection.get('rejection_details', ''),
                    rejection.get('shares', 0),
                    rejection.get('position_size_value', 0.0),
                    rejection.get('total_risk', 0.0),
                    rejection.get('research_composite_score', 0.0)
                ))

            conn.commit()
            self.logger.info(f"  Logged {len(rejected)} rejections to database")

        finally:
            conn.close()

    def _log_portfolio_decision(self, metadata: Dict, accepted: List, rejected: List,
                               positions_before: int, capital_before: float):
        """Log Portfolio decision to portfolio_decisions table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Calculate positions/capital after this decision
            positions_after = positions_before + len(accepted)

            # Estimate capital after (sum of accepted position values)
            capital_added = sum(c.get('position_size_value', 0.0) for c in accepted)
            capital_after = capital_before + capital_added

            total_capital = self.config['capital']['total']
            deployment_before = capital_before / total_capital if total_capital > 0 else 0.0
            deployment_after = capital_after / total_capital if total_capital > 0 else 0.0

            cursor.execute("""
                INSERT INTO portfolio_decisions (
                    message_id,
                    parent_message_id,
                    decision_type,
                    decision_date,
                    decision_timestamp,
                    positions_before,
                    positions_after,
                    capital_deployed_before,
                    capital_deployed_after,
                    deployment_pct_before,
                    deployment_pct_after,
                    buy_orders_count,
                    rejected_count,
                    max_positions,
                    max_capital_deployed_pct,
                    min_composite_score
                ) VALUES (?, ?, 'BUY', date('now'), datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"MSG_PORTFOLIO_{datetime.now().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}",
                metadata['message_id'],
                positions_before,
                positions_after,
                capital_before,
                capital_after,
                deployment_before,
                deployment_after,
                len(accepted),
                len(rejected),
                self.config['limits']['max_positions'],
                self.config['limits']['max_capital_deployed_pct'],
                self.config['filters']['min_composite_score']
            ))

            conn.commit()
            self.logger.info("  Decision logged to database")

        finally:
            conn.close()

    def handle_trading_rejection(self, position_id: str, rejection_data: Dict):
        """
        Handle when Trading Department rejects a BuyOrder

        Args:
            position_id: Position that was rejected
            rejection_data: Dict with rejection details from Trading
                - rejection_reason: str
                - rejection_details: str
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Update position status to REJECTED
            cursor.execute("""
                UPDATE portfolio_positions
                SET status = 'REJECTED',
                    updated_at = datetime('now')
                WHERE position_id = ? AND status = 'PENDING'
            """, (position_id,))

            conn.commit()

            # Free up capacity - Portfolio can now accept new candidates
            self.logger.warning(
                f"Position REJECTED by Trading: {position_id} - "
                f"Reason: {rejection_data.get('rejection_reason', 'Unknown')}"
            )

            # Trigger rebalancing check (now have capacity)
            status = self.rebalancer.check_deployment_status()

            if status['needs_rebalancing']:
                self.logger.info("Triggering candidate request after rejection")
                self.rebalancer.generate_candidate_request(self.message_handler)

        finally:
            conn.close()


if __name__ == "__main__":
    # Test Portfolio Decision Engine
    logger.info("Portfolio Department - Testing Decision Engine (Day 1)")

    # Load config
    config_path = Path("Config/portfolio_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize components
    message_handler = MessageHandler()
    decision_engine = PortfolioDecisionEngine(config, Path("sentinel.db"))

    print("\n" + "=" * 100)
    print("TESTING: PortfolioDecisionEngine")
    print("=" * 100)

    # Test with mock RiskAssessment data
    print("\n[1/3] Testing Score Filter:")
    print("-" * 100)

    mock_candidates = [
        {'ticker': 'AAPL', 'research_composite_score': 7.5, 'position_size_shares': 56, 'position_size_value': 9828, 'total_risk': 574},
        {'ticker': 'MSFT', 'research_composite_score': 6.2, 'position_size_shares': 40, 'position_size_value': 10000, 'total_risk': 500},
        {'ticker': 'TSLA', 'research_composite_score': 4.5, 'position_size_shares': 50, 'position_size_value': 9500, 'total_risk': 600},
    ]

    accepted, rejected = decision_engine.apply_score_filter(mock_candidates)
    print(f"  Input: 3 candidates (scores: 7.5, 6.2, 4.5)")
    print(f"  Min Score: {config['filters']['min_composite_score']}")
    print(f"  Accepted: {len(accepted)} - {[c['ticker'] for c in accepted]}")
    print(f"  Rejected: {len(rejected)} - {[r['ticker'] for r in rejected]}")
    if len(rejected) > 0:
        print(f"  Rejection: {rejected[0]['rejection_details'][:100]}...")

    print("\n[2/3] Testing Position Limits:")
    print("-" * 100)

    # Simulate 9 open positions
    current_positions = 9
    print(f"  Current Positions: {current_positions}/{config['limits']['max_positions']}")
    print(f"  Available Slots: {config['limits']['max_positions'] - current_positions}")

    accepted, rejected = decision_engine.apply_position_limits(accepted, current_positions)
    print(f"  Accepted: {len(accepted)} - {[c['ticker'] for c in accepted]}")
    print(f"  Rejected: {len(rejected)} - {[r['ticker'] for r in rejected]}")

    print("\n[3/3] Testing Capital Limits:")
    print("-" * 100)

    deployed_capital = 85000  # $85K already deployed
    max_capital = config['capital']['total'] * config['limits']['max_capital_deployed_pct']
    available = max_capital - deployed_capital

    print(f"  Deployed: ${deployed_capital:,.0f}")
    print(f"  Max Deploy: ${max_capital:,.0f}")
    print(f"  Available: ${available:,.0f}")

    accepted, rejected = decision_engine.apply_capital_limits(accepted, deployed_capital)
    print(f"  Accepted: {len(accepted)} - {[c['ticker'] for c in accepted]}")
    print(f"  Rejected: {len(rejected)} - {[r['ticker'] for r in rejected]}")

    print("\n[4/4] Testing BuyOrder Generation:")
    print("-" * 100)

    # Generate BuyOrder for accepted candidate
    if len(accepted) > 0:
        test_candidate = {
            'ticker': 'AAPL',
            'research_composite_score': 7.5,
            'position_size_shares': 56,
            'position_size_value': 9828,
            'entry_price': 175.50,
            'stop_loss': 165.25,
            'target_price': 185.75,
            'risk_per_share': 10.25,
            'total_risk': 574,
            'risk_percentage': 0.00574,
            'risk_reward_ratio': 2.0,
            'sector': 'Technology'
        }

        risk_message_id = "MSG_RISK_20251031T100000Z_test123"
        message_id, position_id = decision_engine.generate_buy_order(
            test_candidate,
            risk_message_id,
            message_handler
        )

        print(f"  BuyOrder Message ID: {message_id}")
        print(f"  Position ID: {position_id}")
        print(f"  Message File: Messages_Between_Departments/Outbox/PORTFOLIO/{message_id}.md")

        # Read back the message to verify
        message_path = Path(f"Messages_Between_Departments/Outbox/PORTFOLIO/{message_id}.md")
        if message_path.exists():
            print(f"  Message Created: SUCCESS")
            with open(message_path, 'r') as f:
                first_30_lines = ''.join(f.readlines()[:30])
                print(f"\n  First 30 lines of message:")
                print("  " + "-" * 96)
                for line in first_30_lines.split('\n'):
                    print(f"  {line}")

    print("\n" + "=" * 100)
    print("TEST COMPLETE - PortfolioDecisionEngine Day 1 (All Components)")
    print("=" * 100)
