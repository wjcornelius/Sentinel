"""
COMPLIANCE DEPARTMENT - Week 5
Guards Sentinel Corporation with pre-trade validation, post-trade auditing, and regulatory reporting

Architecture:
1. PreTradeValidator: Validates trades before execution (position size, sector, risk limits)
2. PostTradeAuditor: Audits executed trades (slippage, partial fills, parameter accuracy)
3. ComplianceReporter: Generates daily compliance reports
4. ComplianceDepartment: Main orchestrator

Author: Claude Code (CC)
Architect: Claude from Poe (C(P))
Week: 5 of 7
"""

import yaml
import json
import sqlite3
import logging
import uuid
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ComplianceDepartment')


# ============================================================================
# CLASS 1: PRE-TRADE VALIDATOR (Week 5 Day 1)
# ============================================================================
class PreTradeValidator:
    """
    Validates trades before execution
    Enforces position sizing, sector concentration, risk limits, duplicate prevention,
    and restricted ticker rules
    """

    def __init__(self, config: Dict, db_path: Path):
        self.db_path = db_path
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        # Load rules from config
        self.max_position_pct = config['position_sizing']['max_position_pct']
        self.min_position_value = config['position_sizing']['min_position_value']
        self.max_position_value = config['position_sizing']['max_position_value']

        self.max_sector_concentration = config['sector_limits']['max_concentration_pct']
        self.sector_specific_limits = config['sector_limits'].get('sector_specific', {})

        self.max_risk_per_trade_pct = config['risk_limits']['max_risk_per_trade_pct']
        self.max_portfolio_risk_pct = config['risk_limits']['max_portfolio_risk_pct']

        self.restricted_blocklist = config['restricted_tickers']['blocklist']
        self.restricted_allowlist = config['restricted_tickers']['allowlist']
        self.min_ticker_price = config['restricted_tickers']['min_price']

        self.total_capital = config['capital']['total']

        self.logger.info(
            f"PreTradeValidator initialized: "
            f"max_position={self.max_position_pct:.1%}, "
            f"max_sector={self.max_sector_concentration:.1%}, "
            f"max_risk={self.max_risk_per_trade_pct:.1%}"
        )

    def validate_trade(self, proposal: Dict) -> Tuple[bool, Optional[str], Optional[str], Dict]:
        """
        Validate trade against all compliance rules

        Args:
            proposal: Dict with trade details:
                - ticker: str
                - trade_type: 'BUY' or 'SELL'
                - shares: int
                - price: float
                - position_value: float
                - total_risk: float
                - sector: str
                - stop_loss: float (for BUY orders)
                - target: float (for BUY orders)

        Returns:
            (is_approved, rejection_reason, rejection_category, check_results)
        """
        ticker = proposal['ticker']
        trade_type = proposal['trade_type']
        position_value = proposal['position_value']
        sector = proposal.get('sector', 'Unknown')

        # Initialize check results
        check_results = {
            'position_size_check': 'SKIP',
            'sector_concentration_check': 'SKIP',
            'risk_limit_check': 'SKIP',
            'duplicate_order_check': 'SKIP',
            'restricted_ticker_check': 'SKIP'
        }

        # Only validate BUY orders (SELL orders are exits, no pre-validation needed)
        if trade_type == 'SELL':
            self.logger.info(f"SELL order for {ticker} - skipping pre-trade validation")
            check_results = {k: 'SKIP' for k in check_results}
            return True, None, None, check_results

        # Check 1: Restricted Ticker
        is_restricted, reason = self._check_restricted_ticker(ticker, proposal.get('price', 0))
        check_results['restricted_ticker_check'] = 'FAIL' if is_restricted else 'PASS'

        if is_restricted:
            self.logger.warning(f"REJECTED: {ticker} - {reason}")
            return False, reason, 'RESTRICTED', check_results

        # Check 2: Position Size
        exceeds_size, reason = self._check_position_size(ticker, position_value)
        check_results['position_size_check'] = 'FAIL' if exceeds_size else 'PASS'

        if exceeds_size:
            self.logger.warning(f"REJECTED: {ticker} - {reason}")
            return False, reason, 'POSITION_SIZE', check_results

        # Check 3: Sector Concentration
        exceeds_sector, reason = self._check_sector_concentration(ticker, sector, position_value)
        check_results['sector_concentration_check'] = 'FAIL' if exceeds_sector else 'PASS'

        if exceeds_sector:
            self.logger.warning(f"REJECTED: {ticker} - {reason}")
            return False, reason, 'SECTOR_LIMIT', check_results

        # Check 4: Risk Limits
        exceeds_risk, reason = self._check_risk_limits(ticker, proposal.get('total_risk', 0))
        check_results['risk_limit_check'] = 'FAIL' if exceeds_risk else 'PASS'

        if exceeds_risk:
            self.logger.warning(f"REJECTED: {ticker} - {reason}")
            return False, reason, 'RISK_LIMIT', check_results

        # Check 5: Duplicate Orders
        is_duplicate, reason = self._check_duplicate_order(ticker)
        check_results['duplicate_order_check'] = 'FAIL' if is_duplicate else 'PASS'

        if is_duplicate:
            self.logger.warning(f"REJECTED: {ticker} - {reason}")
            return False, reason, 'DUPLICATE', check_results

        # All checks passed
        self.logger.info(f"APPROVED: {ticker} - All compliance checks passed")
        return True, None, None, check_results

    def _check_restricted_ticker(self, ticker: str, price: float) -> Tuple[bool, Optional[str]]:
        """Check if ticker is on restricted list or below minimum price"""

        # Check allowlist first (overrides all restrictions)
        if ticker in self.restricted_allowlist:
            return False, None

        # Check blocklist
        if ticker in self.restricted_blocklist:
            return True, f"Ticker {ticker} is on restricted blocklist"

        # Check minimum price (penny stock filter)
        if self.config['restricted_tickers']['enforce_min_price']:
            if price > 0 and price < self.min_ticker_price:
                return True, f"Ticker {ticker} price ${price:.2f} below minimum ${self.min_ticker_price:.2f} (penny stock)"

        return False, None

    def _check_position_size(self, ticker: str, position_value: float) -> Tuple[bool, Optional[str]]:
        """Check if position size exceeds limits"""

        # Check minimum position value
        if self.config['position_sizing']['enforce_min_position_value']:
            if position_value < self.min_position_value:
                return True, (
                    f"Position value ${position_value:,.2f} below minimum "
                    f"${self.min_position_value:,.2f}"
                )

        # Check maximum position value (absolute cap)
        if self.config['position_sizing']['enforce_max_position_value']:
            if position_value > self.max_position_value:
                return True, (
                    f"Position value ${position_value:,.2f} exceeds maximum "
                    f"${self.max_position_value:,.2f}"
                )

        # Check maximum position as % of portfolio
        if self.config['position_sizing']['enforce_max_position_pct']:
            position_pct = position_value / self.total_capital

            if position_pct > self.max_position_pct:
                return True, (
                    f"Position size {position_pct:.1%} of portfolio exceeds maximum "
                    f"{self.max_position_pct:.1%} (${position_value:,.2f} of ${self.total_capital:,.2f})"
                )

        return False, None

    def _check_sector_concentration(self, ticker: str, sector: str, position_value: float) -> Tuple[bool, Optional[str]]:
        """Check if adding this position would exceed sector concentration limits"""

        if not self.config['sector_limits']['enforce_max_concentration']:
            return False, None

        # Get current sector allocation
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Calculate current sector value
            cursor.execute("""
                SELECT SUM(actual_entry_price * actual_shares) as sector_value
                FROM portfolio_positions
                WHERE status = 'OPEN' AND sector = ?
            """, (sector,))

            row = cursor.fetchone()
            current_sector_value = row[0] if row[0] else 0.0

            # Calculate total portfolio value
            cursor.execute("""
                SELECT SUM(actual_entry_price * actual_shares) as total_value
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)

            row = cursor.fetchone()
            current_portfolio_value = row[0] if row[0] else 0.0

            # Calculate new sector allocation after adding this position
            new_sector_value = current_sector_value + position_value
            new_portfolio_value = current_portfolio_value + position_value

            new_sector_pct = new_sector_value / new_portfolio_value if new_portfolio_value > 0 else 0

            # Check against sector-specific limit (if exists) or default limit
            sector_limit = self.sector_specific_limits.get(sector, self.max_sector_concentration)

            if new_sector_pct > sector_limit:
                return True, (
                    f"Adding {ticker} would increase {sector} allocation to {new_sector_pct:.1%}, "
                    f"exceeding limit of {sector_limit:.1%} "
                    f"(${new_sector_value:,.2f} of ${new_portfolio_value:,.2f})"
                )

            return False, None

        finally:
            conn.close()

    def _check_risk_limits(self, ticker: str, trade_risk: float) -> Tuple[bool, Optional[str]]:
        """Check if trade risk exceeds limits"""

        # Check risk per trade
        if self.config['risk_limits']['enforce_max_risk_per_trade']:
            risk_pct = trade_risk / self.total_capital

            if risk_pct > self.max_risk_per_trade_pct:
                return True, (
                    f"Trade risk {risk_pct:.2%} exceeds maximum {self.max_risk_per_trade_pct:.2%} "
                    f"(${trade_risk:,.2f} of ${self.total_capital:,.2f})"
                )

        # Check portfolio risk (total risk across all open positions + this trade)
        if self.config['risk_limits']['enforce_max_portfolio_risk']:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    SELECT SUM(total_risk) as portfolio_risk
                    FROM portfolio_positions
                    WHERE status IN ('OPEN', 'PENDING')
                """)

                row = cursor.fetchone()
                current_portfolio_risk = row[0] if row[0] else 0.0

                new_portfolio_risk = current_portfolio_risk + trade_risk
                new_portfolio_risk_pct = new_portfolio_risk / self.total_capital

                if new_portfolio_risk_pct > self.max_portfolio_risk_pct:
                    return True, (
                        f"Adding trade would increase portfolio risk to {new_portfolio_risk_pct:.2%}, "
                        f"exceeding limit of {self.max_portfolio_risk_pct:.2%} "
                        f"(${new_portfolio_risk:,.2f} of ${self.total_capital:,.2f})"
                    )

            finally:
                conn.close()

        return False, None

    def _check_duplicate_order(self, ticker: str) -> Tuple[bool, Optional[str]]:
        """Check for duplicate pending or open positions"""

        if not self.config['duplicate_prevention']['check_pending_orders'] and \
           not self.config['duplicate_prevention']['check_open_positions']:
            return False, None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check for PENDING positions
            if self.config['duplicate_prevention']['check_pending_orders']:
                cursor.execute("""
                    SELECT COUNT(*) FROM portfolio_positions
                    WHERE ticker = ? AND status = 'PENDING'
                """, (ticker,))

                pending_count = cursor.fetchone()[0]
                if pending_count > 0:
                    return True, f"Duplicate order: {pending_count} PENDING position(s) already exist for {ticker}"

            # Check for OPEN positions
            if self.config['duplicate_prevention']['check_open_positions']:
                cursor.execute("""
                    SELECT COUNT(*) FROM portfolio_positions
                    WHERE ticker = ? AND status = 'OPEN'
                """, (ticker,))

                open_count = cursor.fetchone()[0]
                if open_count > 0:
                    return True, f"Duplicate order: {open_count} OPEN position(s) already exist for {ticker}"

            # Check for recently closed positions (reopen cooldown)
            if not self.config['duplicate_prevention']['allow_reopens']:
                cooldown_hours = self.config['duplicate_prevention']['reopen_cooldown_hours']
                cooldown_time = datetime.now() - timedelta(hours=cooldown_hours)

                cursor.execute("""
                    SELECT COUNT(*) FROM portfolio_positions
                    WHERE ticker = ?
                    AND status = 'CLOSED'
                    AND updated_at > ?
                """, (ticker, cooldown_time.isoformat()))

                recent_closed = cursor.fetchone()[0]
                if recent_closed > 0:
                    return True, (
                        f"Reopen cooldown: {ticker} was closed within last {cooldown_hours}h. "
                        "Must wait before reopening."
                    )

            return False, None

        finally:
            conn.close()


# ============================================================================
# CLASS 2: POST-TRADE AUDITOR (Week 5 Day 2)
# ============================================================================
class PostTradeAuditor:
    """
    Audits executed trades for compliance violations
    Checks slippage, partial fills, stop-loss/target accuracy
    """

    def __init__(self, config: Dict, db_path: Path):
        self.db_path = db_path
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        # Load audit thresholds
        self.slippage_warn_pct = config['audit_thresholds']['slippage']['warn_threshold_pct']
        self.slippage_fail_pct = config['audit_thresholds']['slippage']['fail_threshold_pct']

        self.partial_fill_warn_pct = config['audit_thresholds']['partial_fill']['warn_threshold_pct']
        self.partial_fill_fail_pct = config['audit_thresholds']['partial_fill']['fail_threshold_pct']

        self.param_accuracy_warn_pct = config['audit_thresholds']['parameter_accuracy']['warn_threshold_pct']
        self.param_accuracy_fail_pct = config['audit_thresholds']['parameter_accuracy']['fail_threshold_pct']

        self.logger.info(
            f"PostTradeAuditor initialized: "
            f"slippage_warn={self.slippage_warn_pct:.1%}, "
            f"partial_fill_warn={self.partial_fill_warn_pct:.1%}"
        )

    def audit_fill(self, position: Dict, fill_data: Dict) -> Dict:
        """
        Audit FillConfirmation against intended trade parameters

        Args:
            position: Dict from portfolio_positions table with intended parameters
            fill_data: Dict with actual fill details from Trading

        Returns:
            audit_result: Dict with:
                - audit_status: 'PASS', 'WARN', or 'FAIL'
                - slippage_check: check result
                - slippage_pct: actual slippage percentage
                - partial_fill_check: check result
                - fill_rate: actual fill rate
                - findings: list of issues found
                - severity: 'INFO', 'WARN', or 'CRITICAL'
        """
        ticker = position['ticker']
        position_id = position['position_id']

        # Initialize audit result
        audit_result = {
            'position_id': position_id,
            'ticker': ticker,
            'audit_status': 'PASS',
            'slippage_check': 'PASS',
            'slippage_pct': 0.0,
            'slippage_amount': 0.0,
            'partial_fill_check': 'PASS',
            'fill_rate': 1.0,
            'stop_loss_accuracy_check': 'PASS',
            'stop_loss_deviation_pct': 0.0,
            'target_accuracy_check': 'PASS',
            'target_deviation_pct': 0.0,
            'findings': [],
            'severity': 'INFO'
        }

        # Check 1: Slippage
        slippage_status, slippage_finding = self._check_slippage(
            position['intended_entry_price'],
            fill_data['fill_price']
        )

        audit_result['slippage_check'] = slippage_status
        audit_result['slippage_pct'] = abs((fill_data['fill_price'] - position['intended_entry_price']) / position['intended_entry_price'])
        audit_result['slippage_amount'] = fill_data['fill_price'] - position['intended_entry_price']

        if slippage_finding:
            audit_result['findings'].append(slippage_finding)

        # Check 2: Partial Fill
        partial_status, partial_finding = self._check_partial_fill(
            position['intended_shares'],
            fill_data['filled_shares']
        )

        audit_result['partial_fill_check'] = partial_status
        audit_result['fill_rate'] = fill_data['filled_shares'] / position['intended_shares'] if position['intended_shares'] > 0 else 1.0

        if partial_finding:
            audit_result['findings'].append(partial_finding)

        # Check 3: Stop-Loss Accuracy (only for new positions, not applicable to exits)
        if 'intended_stop_loss' in position and position.get('status') != 'CLOSED':
            stop_status, stop_finding = self._check_parameter_accuracy(
                'stop_loss',
                position['intended_stop_loss'],
                position.get('actual_stop_loss', position['intended_stop_loss'])
            )

            audit_result['stop_loss_accuracy_check'] = stop_status
            if position['intended_stop_loss'] != 0:
                audit_result['stop_loss_deviation_pct'] = abs(
                    (position.get('actual_stop_loss', position['intended_stop_loss']) - position['intended_stop_loss']) / position['intended_stop_loss']
                )

            if stop_finding:
                audit_result['findings'].append(stop_finding)

        # Check 4: Target Accuracy
        if 'intended_target' in position and position.get('status') != 'CLOSED':
            target_status, target_finding = self._check_parameter_accuracy(
                'target',
                position['intended_target'],
                position.get('actual_target', position['intended_target'])
            )

            audit_result['target_accuracy_check'] = target_status
            if position['intended_target'] != 0:
                audit_result['target_deviation_pct'] = abs(
                    (position.get('actual_target', position['intended_target']) - position['intended_target']) / position['intended_target']
                )

            if target_finding:
                audit_result['findings'].append(target_finding)

        # Determine overall audit status and severity
        check_statuses = [
            audit_result['slippage_check'],
            audit_result['partial_fill_check'],
            audit_result['stop_loss_accuracy_check'],
            audit_result['target_accuracy_check']
        ]

        if 'FAIL' in check_statuses:
            audit_result['audit_status'] = 'FAIL'
            audit_result['severity'] = 'CRITICAL'
        elif 'WARN' in check_statuses:
            audit_result['audit_status'] = 'WARN'
            audit_result['severity'] = 'WARN'
        else:
            audit_result['audit_status'] = 'PASS'
            audit_result['severity'] = 'INFO'

        # Log audit result
        if audit_result['audit_status'] == 'PASS':
            self.logger.info(f"Audit PASS: {ticker} ({position_id})")
        elif audit_result['audit_status'] == 'WARN':
            self.logger.warning(f"Audit WARN: {ticker} ({position_id}) - {len(audit_result['findings'])} issue(s)")
        else:
            self.logger.error(f"Audit FAIL: {ticker} ({position_id}) - {len(audit_result['findings'])} issue(s)")

        return audit_result

    def _check_slippage(self, intended_price: float, actual_price: float) -> Tuple[str, Optional[str]]:
        """Check if slippage exceeds thresholds"""

        if intended_price == 0:
            return 'PASS', None

        slippage_pct = abs((actual_price - intended_price) / intended_price)

        if slippage_pct > self.slippage_fail_pct:
            return 'FAIL', (
                f"CRITICAL: Slippage {slippage_pct:.2%} exceeds FAIL threshold {self.slippage_fail_pct:.2%} "
                f"(intended ${intended_price:.2f}, actual ${actual_price:.2f})"
            )
        elif slippage_pct > self.slippage_warn_pct:
            return 'WARN', (
                f"WARNING: Slippage {slippage_pct:.2%} exceeds WARN threshold {self.slippage_warn_pct:.2%} "
                f"(intended ${intended_price:.2f}, actual ${actual_price:.2f})"
            )

        return 'PASS', None

    def _check_partial_fill(self, intended_shares: int, actual_shares: int) -> Tuple[str, Optional[str]]:
        """Check if partial fill rate is acceptable"""

        if intended_shares == 0:
            return 'PASS', None

        fill_rate = actual_shares / intended_shares

        if fill_rate < self.partial_fill_fail_pct:
            return 'FAIL', (
                f"CRITICAL: Fill rate {fill_rate:.1%} below FAIL threshold {self.partial_fill_fail_pct:.1%} "
                f"({actual_shares}/{intended_shares} shares filled)"
            )
        elif fill_rate < self.partial_fill_warn_pct:
            return 'WARN', (
                f"WARNING: Partial fill {fill_rate:.1%} below WARN threshold {self.partial_fill_warn_pct:.1%} "
                f"({actual_shares}/{intended_shares} shares filled)"
            )

        return 'PASS', None

    def _check_parameter_accuracy(self, param_name: str, intended: float, actual: float) -> Tuple[str, Optional[str]]:
        """Check if stop-loss/target parameters match intended values"""

        if intended == 0:
            return 'PASS', None

        deviation_pct = abs((actual - intended) / intended)

        if deviation_pct > self.param_accuracy_fail_pct:
            return 'FAIL', (
                f"CRITICAL: {param_name} deviation {deviation_pct:.2%} exceeds FAIL threshold {self.param_accuracy_fail_pct:.2%} "
                f"(intended ${intended:.2f}, actual ${actual:.2f})"
            )
        elif deviation_pct > self.param_accuracy_warn_pct:
            return 'WARN', (
                f"WARNING: {param_name} deviation {deviation_pct:.2%} exceeds WARN threshold {self.param_accuracy_warn_pct:.2%} "
                f"(intended ${intended:.2f}, actual ${actual:.2f})"
            )

        return 'PASS', None

    def save_audit_to_database(self, audit_result: Dict):
        """Save audit result to compliance_trade_audits table"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO compliance_trade_audits (
                    position_id,
                    ticker,
                    intended_entry_price,
                    actual_entry_price,
                    intended_shares,
                    actual_shares,
                    intended_stop_loss,
                    intended_target,
                    audit_status,
                    audit_timestamp,
                    slippage_check,
                    slippage_pct,
                    slippage_amount,
                    partial_fill_check,
                    fill_rate,
                    stop_loss_accuracy_check,
                    stop_loss_deviation_pct,
                    target_accuracy_check,
                    target_deviation_pct,
                    findings,
                    severity,
                    trade_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
            """, (
                audit_result['position_id'],
                audit_result['ticker'],
                audit_result.get('intended_entry_price', 0.0),
                audit_result.get('actual_entry_price', 0.0),
                audit_result.get('intended_shares', 0),
                audit_result.get('actual_shares', 0),
                audit_result.get('intended_stop_loss', 0.0),
                audit_result.get('intended_target', 0.0),
                audit_result['audit_status'],
                audit_result['slippage_check'],
                audit_result['slippage_pct'],
                audit_result['slippage_amount'],
                audit_result['partial_fill_check'],
                audit_result['fill_rate'],
                audit_result['stop_loss_accuracy_check'],
                audit_result['stop_loss_deviation_pct'],
                audit_result['target_accuracy_check'],
                audit_result['target_deviation_pct'],
                ' | '.join(audit_result['findings']) if audit_result['findings'] else None,
                audit_result['severity']
            ))

            conn.commit()
            self.logger.info(f"Audit result saved for {audit_result['ticker']} ({audit_result['position_id']})")

        finally:
            conn.close()


if __name__ == "__main__":
    # Test PreTradeValidator
    logger.info("Compliance Department - Testing PreTradeValidator (Day 1)")

    # Load config
    config_path = Path("Config/compliance_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize validator
    validator = PreTradeValidator(config, Path("sentinel.db"))

    print("\n" + "=" * 100)
    print("TESTING: PreTradeValidator")
    print("=" * 100)

    # Test 1: Valid trade
    print("\n[TEST 1] Valid Trade:")
    print("-" * 100)

    valid_proposal = {
        'ticker': 'AAPL',
        'trade_type': 'BUY',
        'shares': 56,
        'price': 175.50,
        'position_value': 9828.00,
        'total_risk': 574.00,
        'sector': 'Technology',
        'stop_loss': 165.25,
        'target': 185.75
    }

    approved, reason, category, checks = validator.validate_trade(valid_proposal)
    print(f"  Ticker: {valid_proposal['ticker']}")
    print(f"  Position Value: ${valid_proposal['position_value']:,.2f}")
    print(f"  Result: {'APPROVED' if approved else 'REJECTED'}")
    if not approved:
        print(f"  Reason: {reason}")
        print(f"  Category: {category}")
    print(f"  Checks: {checks}")
    print()

    # Test 2: Oversized position
    print("[TEST 2] Oversized Position (>10% of portfolio):")
    print("-" * 100)

    oversized_proposal = {
        'ticker': 'TSLA',
        'trade_type': 'BUY',
        'shares': 100,
        'price': 250.00,
        'position_value': 25000.00,  # 25% of $100K portfolio
        'total_risk': 1000.00,
        'sector': 'Consumer Cyclical',
        'stop_loss': 240.00,
        'target': 260.00
    }

    approved, reason, category, checks = validator.validate_trade(oversized_proposal)
    print(f"  Ticker: {oversized_proposal['ticker']}")
    print(f"  Position Value: ${oversized_proposal['position_value']:,.2f} ({oversized_proposal['position_value']/100000:.1%} of portfolio)")
    print(f"  Result: {'APPROVED' if approved else 'REJECTED'}")
    if not approved:
        print(f"  Reason: {reason}")
        print(f"  Category: {category}")
    print(f"  Checks: {checks}")
    print()

    # Test 3: Restricted ticker
    print("[TEST 3] Restricted Ticker (GME):")
    print("-" * 100)

    restricted_proposal = {
        'ticker': 'GME',
        'trade_type': 'BUY',
        'shares': 100,
        'price': 25.00,
        'position_value': 2500.00,
        'total_risk': 250.00,
        'sector': 'Consumer Cyclical',
        'stop_loss': 22.50,
        'target': 27.50
    }

    approved, reason, category, checks = validator.validate_trade(restricted_proposal)
    print(f"  Ticker: {restricted_proposal['ticker']}")
    print(f"  Result: {'APPROVED' if approved else 'REJECTED'}")
    if not approved:
        print(f"  Reason: {reason}")
        print(f"  Category: {category}")
    print(f"  Checks: {checks}")
    print()

    print("=" * 100)
    print("PreTradeValidator tests complete")
    print("=" * 100)
