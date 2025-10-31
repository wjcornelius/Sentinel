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

        logger.info(f"PortfolioDecisionEngine initialized (max positions: {self.max_positions}, "
                   f"max deployed: {self.max_capital_deployed_pct*100:.0f}%, "
                   f"min score: {self.min_composite_score})")

    def get_open_positions_count(self) -> int:
        """Get count of current open/pending positions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) FROM portfolio_positions
                WHERE status IN ('PENDING', 'OPEN')
            """)

            count = cursor.fetchone()[0]
            conn.close()

            return count

        except Exception as e:
            logger.error(f"Failed to get position count: {e}", exc_info=True)
            return 0

    def get_deployed_capital(self) -> float:
        """Get total capital currently deployed in open/pending positions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT SUM(intended_shares * intended_entry_price) as deployed
                FROM portfolio_positions
                WHERE status IN ('PENDING', 'OPEN')
            """)

            result = cursor.fetchone()[0]
            conn.close()

            return result if result else 0.0

        except Exception as e:
            logger.error(f"Failed to get deployed capital: {e}", exc_info=True)
            return 0.0

    def get_open_tickers(self) -> List[str]:
        """Get list of tickers for open/pending positions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT ticker FROM portfolio_positions
                WHERE status IN ('PENDING', 'OPEN')
                ORDER BY ticker
            """)

            tickers = [row[0] for row in cursor.fetchall()]
            conn.close()

            return tickers

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
                        f"Research composite score {score:.1f} is below minimum threshold {self.min_composite_score:.1f}. "
                        f"Only candidates scoring {self.min_composite_score:.1f}+ are eligible for trading."
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
                    f"This candidate (score {candidate.get('research_composite_score', 0):.1f}) "
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

    print("\n" + "=" * 100)
    print("TEST COMPLETE - PortfolioDecisionEngine Day 1")
    print("=" * 100)
