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
                message_type = metadata.get('message_type')
                if message_type in ['execution_request', 'ExecutiveApproval']:
                    # Both execution_request and ExecutiveApproval trigger order execution
                    self._process_execution_request(metadata, body)
                else:
                    logger.warning(f"Unknown message type: {message_type}")

                # Archive processed message
                self.message_handler.archive_message(message_path)

            except Exception as e:
                logger.error(f"Error processing message {message_path}: {e}", exc_info=True)

        # Cleanup expired duplicate cache entries
        self.duplicate_detector.cleanup_expired()

    def _process_execution_request(self, metadata: Dict, body: str):
        """Process an order execution request from Executive"""
        logger.info(f"Processing execution request: {metadata.get('message_id')}")

        try:
            # Extract JSON data payload from message body
            data_payload = self._extract_json_payload(body)
            if not data_payload:
                logger.error("No data payload found in message")
                return

            # Parse order details
            order = ExecutionOrder(
                ticker=data_payload.get('ticker'),
                action=data_payload.get('action'),
                quantity=data_payload.get('shares'),
                order_type=data_payload.get('order_type', 'MARKET'),
                limit_price=data_payload.get('limit_price'),
                executive_approval_msg_id=metadata.get('message_id'),
                portfolio_request_msg_id=data_payload.get('proposal_id')
            )

            # Check for duplicate
            if self.duplicate_detector.is_duplicate(order):
                self._handle_duplicate(order, metadata)
                return

            # Get portfolio state and market data for validation
            portfolio_state = self._get_portfolio_state()
            market_data = self._get_market_data(order.ticker)

            # Validate hard constraints
            is_valid, violations = self.constraint_validator.validate_order(
                order, portfolio_state, market_data
            )

            if not is_valid:
                self._handle_constraint_violations(order, violations, metadata)
                return

            # Execute order via Alpaca
            self._execute_order_with_retry(order, metadata)

        except Exception as e:
            logger.error(f"Error processing execution request: {e}", exc_info=True)
            self._escalate_error(metadata, str(e))

    def _extract_json_payload(self, body: str) -> Optional[Dict]:
        """Extract JSON data payload from message body"""
        import re

        # Find JSON code block in markdown
        json_match = re.search(r'```json\n(.*?)\n```', body, re.DOTALL)
        if not json_match:
            return None

        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON payload: {e}")
            return None

    def _get_portfolio_state(self) -> Dict:
        """Get current portfolio state from Alpaca"""
        try:
            account = self.trading_client.get_account()
            positions = self.trading_client.get_all_positions()

            portfolio_value = float(account.portfolio_value)
            current_prices = {}

            for pos in positions:
                current_prices[pos.symbol] = float(pos.current_price)

            return {
                'portfolio_value': portfolio_value,
                'cash': float(account.cash),
                'buying_power': float(account.buying_power),
                'current_prices': current_prices
            }
        except Exception as e:
            logger.error(f"Failed to get portfolio state: {e}")
            return {
                'portfolio_value': 0,
                'cash': 0,
                'buying_power': 0,
                'current_prices': {}
            }

    def _get_market_data(self, ticker: str) -> Dict:
        """Get market data for ticker (placeholder - will use yfinance in production)"""
        # TODO: Implement yfinance data fetching
        # For now, return placeholder data
        return {
            'current_price': 100.00,
            'average_volume': 1000000,
            'vix': 15.0
        }

    def _execute_order_with_retry(self, order: ExecutionOrder, metadata: Dict):
        """
        Execute order via Alpaca with exponential backoff retry logic

        Pattern learned from v6.2's execution_engine.py _submit_with_retry()
        Implementation is FRESH code for message-based architecture
        """
        max_retries = 5
        retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff

        for attempt in range(max_retries):
            try:
                # Submit order to Alpaca
                alpaca_order = self._submit_to_alpaca(order)

                if alpaca_order:
                    # Success - store in database and send confirmation
                    order_id = self._store_order_in_database(order, alpaca_order, metadata)
                    self.duplicate_detector.record_submission(order, order_id)
                    self._send_execution_confirmation(order, alpaca_order, metadata)
                    logger.info(f"Order executed successfully: {order.ticker} {order.action} {order.quantity}")
                    return

            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delays[attempt]
                    logger.warning(
                        f"Order submission failed (attempt {attempt + 1}/{max_retries}): {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Order submission failed after {max_retries} attempts: {e}")
                    self._handle_submission_failure(order, metadata, str(e))

    def _submit_to_alpaca(self, order: ExecutionOrder):
        """Submit order to Alpaca API"""
        # Determine order side
        side = OrderSide.BUY if order.action == 'BUY' else OrderSide.SELL

        # Create order request
        if order.order_type == 'MARKET':
            order_request = MarketOrderRequest(
                symbol=order.ticker,
                qty=order.quantity,
                side=side,
                time_in_force=TimeInForce.DAY
            )
        else:  # LIMIT order
            order_request = LimitOrderRequest(
                symbol=order.ticker,
                qty=order.quantity,
                side=side,
                time_in_force=TimeInForce.DAY,
                limit_price=order.limit_price
            )

        # Submit to Alpaca
        alpaca_order = self.trading_client.submit_order(order_request)
        logger.info(f"Submitted order to Alpaca: {alpaca_order.id}")
        return alpaca_order

    def _store_order_in_database(self, order: ExecutionOrder, alpaca_order, metadata: Dict) -> int:
        """Store order in database with message chain tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Generate internal order ID
        internal_order_id = f"ORD_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        cursor.execute("""
            INSERT INTO trading_orders (
                order_id, alpaca_order_id, ticker, action, quantity, order_type, limit_price,
                executive_approval_msg_id, portfolio_request_msg_id,
                status, submitted_timestamp, hard_constraints_passed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            internal_order_id,
            alpaca_order.id,
            order.ticker,
            order.action,
            order.quantity,
            order.order_type,
            order.limit_price,
            order.executive_approval_msg_id,
            order.portfolio_request_msg_id,
            'SUBMITTED',
            datetime.utcnow(),
            1  # Hard constraints passed
        ))

        order_db_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"Stored order in database: {internal_order_id}")
        return order_db_id

    def _send_execution_confirmation(self, order: ExecutionOrder, alpaca_order, metadata: Dict):
        """Send execution confirmation to Portfolio and Compliance"""
        data_payload = {
            'order_id': alpaca_order.id,
            'ticker': order.ticker,
            'action': order.action,
            'shares': order.quantity,
            'order_type': order.order_type,
            'status': 'SUBMITTED',
            'submitted_at': alpaca_order.submitted_at.isoformat() if alpaca_order.submitted_at else datetime.utcnow().isoformat(),
            'alpaca_order_id': alpaca_order.id
        }

        # Send to Portfolio
        self.message_handler.write_message(
            to_dept='PORTFOLIO',
            message_type='execution',
            subject=f"Order Submitted: {order.ticker} {order.action} {order.quantity}",
            body=f"## Order Confirmation\n\nYour order has been submitted to Alpaca.\n\n"
                 f"- **Ticker:** {order.ticker}\n"
                 f"- **Action:** {order.action}\n"
                 f"- **Quantity:** {order.quantity}\n"
                 f"- **Order Type:** {order.order_type}\n"
                 f"- **Alpaca Order ID:** {alpaca_order.id}\n",
            data_payload=data_payload
        )

        # Send to Compliance
        self.message_handler.write_message(
            to_dept='COMPLIANCE',
            message_type='log',
            subject=f"Trade Executed: {order.ticker} {order.action} {order.quantity}",
            body=f"## Execution Log\n\nTrade executed via Alpaca.\n\n"
                 f"- **Ticker:** {order.ticker}\n"
                 f"- **Action:** {order.action}\n"
                 f"- **Quantity:** {order.quantity}\n"
                 f"- **Alpaca Order ID:** {alpaca_order.id}\n",
            data_payload=data_payload
        )

        logger.info(f"Sent execution confirmations to Portfolio and Compliance")

    def _handle_duplicate(self, order: ExecutionOrder, metadata: Dict):
        """Handle duplicate order detection"""
        logger.warning(f"Duplicate order blocked: {order.ticker} {order.action} {order.quantity}")

        # Store rejection in database
        self._store_rejection(order, metadata, "DUPLICATE", "Duplicate order detected (submitted within last 5 minutes)")

        # Send rejection notice to Executive
        self.message_handler.write_message(
            to_dept='EXECUTIVE',
            message_type='escalation',
            subject=f"DUPLICATE ORDER BLOCKED: {order.ticker}",
            body=f"## Duplicate Order Detected\n\n"
                 f"A duplicate order was automatically blocked:\n\n"
                 f"- **Ticker:** {order.ticker}\n"
                 f"- **Action:** {order.action}\n"
                 f"- **Quantity:** {order.quantity}\n\n"
                 f"**Reason:** Same order submitted within last 5 minutes.\n\n"
                 f"**Action Required:** Review if this was intentional or a bug.",
            priority='elevated'
        )

    def _handle_constraint_violations(self, order: ExecutionOrder, violations: List[HardConstraintViolation], metadata: Dict):
        """Handle hard constraint violations"""
        logger.warning(f"Order rejected due to {len(violations)} hard constraint violation(s)")

        # Format violations for message
        violations_text = "\n".join([
            f"- **{v.constraint_name}:** {v.violation_reason} (limit: {v.limit_value}, actual: {v.violating_value})"
            for v in violations
        ])

        # Store rejection in database
        violation_json = json.dumps([{
            'constraint': v.constraint_name,
            'reason': v.violation_reason,
            'limit': str(v.limit_value),
            'actual': str(v.violating_value)
        } for v in violations])

        self._store_rejection(order, metadata, "HARD_CONSTRAINT", violation_json)

        # Send rejection notice to Executive
        self.message_handler.write_message(
            to_dept='EXECUTIVE',
            message_type='escalation',
            subject=f"ORDER REJECTED: {order.ticker} (Hard Constraint Violations)",
            body=f"## Hard Constraint Violations\n\n"
                 f"Order was automatically rejected due to hard constraint violations:\n\n"
                 f"**Order Details:**\n"
                 f"- **Ticker:** {order.ticker}\n"
                 f"- **Action:** {order.action}\n"
                 f"- **Quantity:** {order.quantity}\n\n"
                 f"**Violations:**\n{violations_text}\n\n"
                 f"**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.",
            priority='elevated'
        )

    def _handle_submission_failure(self, order: ExecutionOrder, metadata: Dict, error_msg: str):
        """Handle Alpaca submission failure after retries"""
        logger.error(f"Order submission failed: {error_msg}")

        # Store rejection in database
        self._store_rejection(order, metadata, "ALPACA", error_msg)

        # Escalate to Executive
        self.message_handler.write_message(
            to_dept='EXECUTIVE',
            message_type='escalation',
            subject=f"ORDER SUBMISSION FAILED: {order.ticker}",
            body=f"## Alpaca Submission Failure\n\n"
                 f"Order failed to submit to Alpaca after 5 retry attempts:\n\n"
                 f"**Order Details:**\n"
                 f"- **Ticker:** {order.ticker}\n"
                 f"- **Action:** {order.action}\n"
                 f"- **Quantity:** {order.quantity}\n\n"
                 f"**Error:** {error_msg}\n\n"
                 f"**Action Required:** Check Alpaca API status or manually submit order if urgent.",
            priority='critical'
        )

    def _store_rejection(self, order: ExecutionOrder, metadata: Dict, rejection_source: str, rejection_reason: str):
        """Store order rejection in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # First, create order record with REJECTED status
        internal_order_id = f"ORD_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        cursor.execute("""
            INSERT INTO trading_orders (
                order_id, ticker, action, quantity, order_type, limit_price,
                executive_approval_msg_id, portfolio_request_msg_id,
                status, hard_constraints_passed, constraint_violations
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            internal_order_id,
            order.ticker,
            order.action,
            order.quantity,
            order.order_type,
            order.limit_price,
            order.executive_approval_msg_id,
            order.portfolio_request_msg_id,
            'REJECTED',
            0 if rejection_source == 'HARD_CONSTRAINT' else 1,
            rejection_reason if rejection_source == 'HARD_CONSTRAINT' else None
        ))

        order_db_id = cursor.lastrowid

        # Then, create rejection record
        cursor.execute("""
            INSERT INTO trading_rejections (
                order_id, rejection_reason, rejection_code, rejection_timestamp, rejection_source
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            order_db_id,
            rejection_reason,
            None,  # rejection_code (Alpaca error code if available)
            datetime.utcnow(),
            rejection_source
        ))

        conn.commit()
        conn.close()

        logger.info(f"Stored rejection in database: {internal_order_id}")

    def _escalate_error(self, metadata: Dict, error_msg: str):
        """Escalate unexpected error to Executive"""
        self.message_handler.write_message(
            to_dept='EXECUTIVE',
            message_type='escalation',
            subject="TRADING DEPARTMENT ERROR",
            body=f"## Unexpected Error\n\n"
                 f"An unexpected error occurred while processing execution request:\n\n"
                 f"**Message ID:** {metadata.get('message_id')}\n\n"
                 f"**Error:** {error_msg}\n\n"
                 f"**Action Required:** Review logs and investigate.",
            priority='critical'
        )


if __name__ == "__main__":
    # Quick test
    dept = TradingDepartment()
    logger.info("Trading Department ready")
    dept.process_inbox()
