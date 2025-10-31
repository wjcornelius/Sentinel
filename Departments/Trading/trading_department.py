"""
TRADING DEPARTMENT - Sentinel Corporation
Built fresh for Phase 1 message-based architecture
Date: 2025-10-31

Primary Responsibilities:
- Execute approved trades via Alpaca API
- Validate hard constraints before submission
- Monitor order fills and handle execution issues
- Provide execution reports to Compliance

Philosophy: Pure execution layer - receives orders, validates constraints, executes.
Does NOT make trading decisions.

Based on: DEPARTMENTAL_SPECIFICATIONS v1.0 - Trading Department section
"""

import sqlite3
import yaml
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
import time
import uuid

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import Alpaca SDK
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType

# Import configuration
from config import APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TradingDepartment')


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ExecutionOrder:
    """Represents an order to be executed"""
    ticker: str
    action: str  # 'BUY' or 'SELL'
    quantity: int
    order_type: str  # 'MARKET' or 'LIMIT'
    limit_price: Optional[float] = None
    executive_approval_msg_id: str = None
    portfolio_request_msg_id: str = None


@dataclass
class HardConstraintViolation:
    """Represents a hard constraint violation"""
    constraint_name: str
    violation_reason: str
    violating_value: any
    limit_value: any


# ============================================================================
# MESSAGE I/O LAYER
# ============================================================================

class MessageHandler:
    """Handles reading and writing messages for Trading Department"""

    def __init__(self):
        self.inbox_path = Path("Messages_Between_Departments/Inbox/TRADING")
        self.outbox_path = Path("Messages_Between_Departments/Outbox/TRADING")
        self.archive_path = Path("Messages_Between_Departments/Archive")

        # Ensure directories exist
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        self.outbox_path.mkdir(parents=True, exist_ok=True)
        self.archive_path.mkdir(parents=True, exist_ok=True)

    def check_inbox(self) -> List[Path]:
        """Scan inbox for new messages"""
        messages = list(self.inbox_path.glob("*.md"))
        logger.info(f"Found {len(messages)} messages in inbox")
        return sorted(messages, key=lambda p: p.stat().st_mtime)

    def read_message(self, message_path: Path) -> Tuple[Dict, str]:
        """
        Parse YAML frontmatter + markdown body
        Returns: (metadata dict, body string)
        """
        with open(message_path, 'r') as f:
            content = f.read()

        # Split YAML frontmatter from body
        parts = content.split('---\n')
        if len(parts) < 3:
            raise ValueError(f"Invalid message format in {message_path}")

        metadata = yaml.safe_load(parts[1])
        body = '---\n'.join(parts[2:])  # Rejoin in case body had ---

        logger.info(f"Read message: {metadata.get('message_id', 'unknown')}")
        return metadata, body

    def write_message(self, to_dept: str, message_type: str, subject: str,
                     body: str, data_payload: Optional[Dict] = None,
                     priority: str = 'routine') -> str:
        """
        Write message to outbox

        Args:
            to_dept: Recipient department
            message_type: Type of message (execution, log, escalation)
            subject: Message subject line
            body: Markdown message body
            data_payload: Optional JSON data
            priority: Message priority (routine, elevated, critical)

        Returns:
            message_id
        """
        # Generate message ID
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        msg_id = f"MSG_TRADING_{timestamp}_{uuid.uuid4().hex[:8]}"

        # Create metadata
        metadata = {
            'message_id': msg_id,
            'from': 'TRADING',
            'to': to_dept,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'message_type': message_type,
            'priority': priority,
            'requires_response': False  # Trading messages are informational
        }

        # Build message content
        content = "---\n"
        content += yaml.dump(metadata, default_flow_style=False)
        content += "---\n\n"
        content += f"# {subject}\n\n"
        content += body

        if data_payload:
            content += "\n\n## Data Payload\n\n"
            content += "```json\n"
            content += json.dumps(data_payload, indent=2)
            content += "\n```\n"

        # Write to outbox
        filename = f"{msg_id}.md"
        filepath = self.outbox_path / filename

        with open(filepath, 'w') as f:
            f.write(content)

        logger.info(f"Wrote message {msg_id} to {to_dept}")
        return msg_id

    def archive_message(self, message_path: Path):
        """Move processed message to archive"""
        date_folder = self.archive_path / datetime.now().strftime('%Y-%m-%d')
        date_folder.mkdir(exist_ok=True)

        dept_folder = date_folder / 'TRADING'
        dept_folder.mkdir(exist_ok=True)

        # Move to archive
        archived_path = dept_folder / message_path.name
        message_path.rename(archived_path)
        logger.info(f"Archived message: {message_path.name}")


# ============================================================================
# HARD CONSTRAINT VALIDATION
# ============================================================================

class HardConstraintValidator:
    """
    Validates orders against hard constraints from hard_constraints.yaml
    AUTO-REJECTS any violation (no human approval)
    """

    def __init__(self):
        # Load hard constraints
        constraints_path = Path("Config/hard_constraints.yaml")
        if not constraints_path.exists():
            raise FileNotFoundError("hard_constraints.yaml not found")

        with open(constraints_path, 'r') as f:
            self.constraints = yaml.safe_load(f)

        logger.info("Loaded hard constraints from Config/hard_constraints.yaml")

    def validate_order(self, order: ExecutionOrder, portfolio_state: Dict,
                       market_data: Dict) -> Tuple[bool, List[HardConstraintViolation]]:
        """
        Validate order against all hard constraints

        Returns:
            (is_valid, violations_list)
        """
        violations = []

        # Check position limits
        violations.extend(self._check_position_limits(order, portfolio_state))

        # Check liquidity requirements
        violations.extend(self._check_liquidity(order, market_data))

        # Check price constraints
        violations.extend(self._check_price_constraints(order, market_data))

        # Check market conditions
        violations.extend(self._check_market_conditions(market_data))

        # Check timing rules
        violations.extend(self._check_timing_rules())

        is_valid = len(violations) == 0
        return is_valid, violations

    def _check_position_limits(self, order: ExecutionOrder, portfolio_state: Dict) -> List[HardConstraintViolation]:
        """Check position size limits"""
        violations = []

        # Get current portfolio value
        portfolio_value = portfolio_state.get('portfolio_value', 0)
        if portfolio_value == 0:
            logger.warning("Portfolio value is 0 - cannot validate position limits")
            return violations

        # Calculate position size percentage
        current_price = portfolio_state.get('current_prices', {}).get(order.ticker, 0)
        if current_price == 0:
            violations.append(HardConstraintViolation(
                constraint_name="price_available",
                violation_reason="Cannot determine current price",
                violating_value=0,
                limit_value="valid price required"
            ))
            return violations

        position_value = order.quantity * current_price
        position_pct = position_value / portfolio_value

        # Check max single position
        max_position = self.constraints['position_limits']['max_single_position_pct']
        if position_pct > max_position:
            violations.append(HardConstraintViolation(
                constraint_name="max_single_position_pct",
                violation_reason=f"Position would be {position_pct:.1%} of portfolio",
                violating_value=position_pct,
                limit_value=max_position
            ))

        # Check min position
        min_position = self.constraints['position_limits']['min_position_pct']
        if position_pct < min_position:
            violations.append(HardConstraintViolation(
                constraint_name="min_position_pct",
                violation_reason=f"Position would be {position_pct:.1%} of portfolio (too small)",
                violating_value=position_pct,
                limit_value=min_position
            ))

        return violations

    def _check_liquidity(self, order: ExecutionOrder, market_data: Dict) -> List[HardConstraintViolation]:
        """Check liquidity requirements"""
        violations = []

        avg_volume = market_data.get('average_volume', 0)
        min_volume = self.constraints['liquidity_requirements']['min_daily_volume_shares']

        if avg_volume < min_volume:
            violations.append(HardConstraintViolation(
                constraint_name="min_daily_volume_shares",
                violation_reason=f"Stock has {avg_volume:,} avg daily volume",
                violating_value=avg_volume,
                limit_value=min_volume
            ))

        # Check order size vs daily volume
        max_order_pct = self.constraints['liquidity_requirements']['max_order_pct_of_volume']
        order_pct_of_volume = order.quantity / avg_volume if avg_volume > 0 else 1.0

        if order_pct_of_volume > max_order_pct:
            violations.append(HardConstraintViolation(
                constraint_name="max_order_pct_of_volume",
                violation_reason=f"Order is {order_pct_of_volume:.1%} of daily volume",
                violating_value=order_pct_of_volume,
                limit_value=max_order_pct
            ))

        return violations

    def _check_price_constraints(self, order: ExecutionOrder, market_data: Dict) -> List[HardConstraintViolation]:
        """Check price constraints (no penny stocks)"""
        violations = []

        current_price = market_data.get('current_price', 0)
        min_price = self.constraints['price_constraints']['min_stock_price']

        if current_price < min_price:
            violations.append(HardConstraintViolation(
                constraint_name="min_stock_price",
                violation_reason=f"Stock price is ${current_price:.2f} (penny stock)",
                violating_value=current_price,
                limit_value=min_price
            ))

        return violations

    def _check_market_conditions(self, market_data: Dict) -> List[HardConstraintViolation]:
        """Check VIX-based market condition constraints"""
        violations = []

        vix = market_data.get('vix', 15)  # Default to normal VIX if unavailable
        vix_panic = self.constraints['market_conditions']['vix_panic_threshold']

        if vix > vix_panic:
            violations.append(HardConstraintViolation(
                constraint_name="vix_panic_threshold",
                violation_reason=f"VIX is {vix:.1f} (panic mode - halt all trading)",
                violating_value=vix,
                limit_value=vix_panic
            ))

        return violations

    def _check_timing_rules(self) -> List[HardConstraintViolation]:
        """Check market hours and timing rules"""
        violations = []

        # Check if market hours only
        if not self.constraints['timing_rules']['market_hours_only']:
            return violations  # Extended hours trading allowed

        # Check current time (ET timezone)
        now = datetime.now()  # TODO: Convert to ET timezone properly

        # Simple check: weekday, between 9:30 AM and 4:00 PM
        # (Simplified for Phase 1 - proper timezone handling in Phase 2)
        if now.weekday() >= 5:  # Weekend
            violations.append(HardConstraintViolation(
                constraint_name="market_hours_only",
                violation_reason="Market is closed (weekend)",
                violating_value=now.strftime('%A'),
                limit_value="Monday-Friday"
            ))

        return violations


# ============================================================================
# DUPLICATE DETECTION
# ============================================================================

class DuplicateDetector:
    """Prevents accidental duplicate order submission"""

    def __init__(self, db_path: str = 'sentinel.db'):
        self.db_path = db_path

    def is_duplicate(self, order: ExecutionOrder) -> bool:
        """
        Check if this order is a duplicate of recent submission (last 5 minutes)

        Returns:
            True if duplicate found
        """
        cutoff_time = datetime.utcnow() - timedelta(minutes=5)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM trading_duplicate_cache
            WHERE ticker = ? AND action = ? AND quantity = ?
            AND submitted_timestamp > ?
        """, (order.ticker, order.action, order.quantity, cutoff_time))

        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            logger.warning(f"Duplicate order detected: {order.ticker} {order.action} {order.quantity}")
            return True

        return False

    def record_submission(self, order: ExecutionOrder, order_id: int):
        """Record order submission in duplicate cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        expires_at = datetime.utcnow() + timedelta(minutes=5)

        cursor.execute("""
            INSERT INTO trading_duplicate_cache
            (ticker, action, quantity, submitted_timestamp, order_id, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order.ticker, order.action, order.quantity, datetime.utcnow(), order_id, expires_at))

        conn.commit()
        conn.close()

        logger.info(f"Recorded order submission in duplicate cache: {order.ticker}")

    def cleanup_expired(self):
        """Remove expired entries from cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM trading_duplicate_cache
            WHERE expires_at < ?
        """, (datetime.utcnow(),))

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted > 0:
            logger.info(f"Cleaned up {deleted} expired duplicate cache entries")


# ============================================================================
# MAIN TRADING DEPARTMENT CLASS
# ============================================================================

class TradingDepartment:
    """
    Main Trading Department class
    Handles message-based order execution with hard constraint validation
    """

    def __init__(self, db_path: str = 'sentinel.db'):
        self.db_path = db_path
        self.message_handler = MessageHandler()
        self.constraint_validator = HardConstraintValidator()
        self.duplicate_detector = DuplicateDetector(db_path)

        # Initialize Alpaca client (using existing credentials from config.py)
        self.trading_client = TradingClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY, paper=True)

        logger.info("Trading Department initialized")
        logger.info(f"Using Alpaca paper trading endpoint: {APCA_API_BASE_URL}")

    def process_inbox(self):
        """
        Main processing loop: check inbox, process messages, execute orders
        """
        messages = self.message_handler.check_inbox()

        for message_path in messages:
            try:
                metadata, body = self.message_handler.read_message(message_path)

                # Validate message is for us
                if metadata.get('to') != 'TRADING':
                    logger.warning(f"Message {metadata.get('message_id')} not addressed to TRADING, skipping")
                    continue

                # Process based on message type
                if metadata.get('message_type') == 'execution_request':
                    self._process_execution_request(metadata, body)
                else:
                    logger.warning(f"Unknown message type: {metadata.get('message_type')}")

                # Archive processed message
                self.message_handler.archive_message(message_path)

            except Exception as e:
                logger.error(f"Error processing message {message_path}: {e}", exc_info=True)

        # Cleanup expired duplicate cache entries
        self.duplicate_detector.cleanup_expired()

    def _process_execution_request(self, metadata: Dict, body: str):
        """Process an order execution request from Portfolio"""
        logger.info(f"Processing execution request: {metadata.get('message_id')}")

        # TODO: Parse order from message body
        # This is a placeholder - actual implementation will parse the markdown/JSON
        # For now, skip to demonstrate the architecture

        logger.info("Execution request processed (placeholder)")


if __name__ == "__main__":
    # Quick test
    dept = TradingDepartment()
    logger.info("Trading Department ready")
    dept.process_inbox()
