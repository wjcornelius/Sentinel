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


# ============================================================================
# CLASS 3: COMPLIANCE REPORTER (Week 5 Day 3)
# ============================================================================
class ComplianceReporter:
    """
    Generates compliance reports for human review
    Reports: Daily summary, trade log, violations, sector allocation, risk metrics
    """

    def __init__(self, config: Dict, db_path: Path):
        self.db_path = db_path
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        # Report output directory
        self.report_dir = Path(config['reporting']['report_output_dir'])
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"ComplianceReporter initialized: output_dir={self.report_dir}")

    def generate_daily_report(self, report_date: date = None) -> str:
        """
        Generate comprehensive daily compliance report

        Args:
            report_date: Date for report (defaults to today)

        Returns:
            report_file_path: Path to generated markdown report
        """
        if report_date is None:
            report_date = date.today()

        self.logger.info(f"Generating daily compliance report for {report_date}")

        # Gather all data
        trade_stats = self._get_trade_statistics(report_date)
        validation_stats = self._get_validation_statistics(report_date)
        audit_stats = self._get_audit_statistics(report_date)
        violation_stats = self._get_violation_statistics(report_date)
        portfolio_snapshot = self._get_portfolio_snapshot()

        # Build markdown report
        report_lines = [
            f"# Compliance Daily Report",
            f"**Date:** {report_date.strftime('%Y-%m-%d')}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
            f"- **Total Trades:** {trade_stats['total_trades']} ({trade_stats['buy_trades']} BUY, {trade_stats['sell_trades']} SELL)",
            f"- **Approval Rate:** {trade_stats['approval_rate']:.1%} ({trade_stats['approved_trades']}/{trade_stats['total_trades']} approved)",
            f"- **Audit Status:** {audit_stats['pass_count']} PASS, {audit_stats['warn_count']} WARN, {audit_stats['fail_count']} FAIL",
            f"- **Active Violations:** {violation_stats['unresolved_count']} unresolved ({violation_stats['critical_count']} CRITICAL)",
            "",
            "---",
            "",
            "## Trade Summary",
            "",
            f"### Validation Results",
            f"- **Total Validations:** {validation_stats['total_validations']}",
            f"- **Approved:** {validation_stats['approved']} ({validation_stats['approved']/validation_stats['total_validations']*100 if validation_stats['total_validations'] > 0 else 0:.1f}%)",
            f"- **Rejected:** {validation_stats['rejected']} ({validation_stats['rejected']/validation_stats['total_validations']*100 if validation_stats['total_validations'] > 0 else 0:.1f}%)",
            "",
            "### Rejection Breakdown",
        ]

        # Add rejection details
        for category, count in validation_stats['rejection_by_category'].items():
            report_lines.append(f"- **{category}:** {count}")

        report_lines.extend([
            "",
            "---",
            "",
            "## Audit Summary",
            "",
            f"- **Total Audits:** {audit_stats['total_audits']}",
            f"- **PASS:** {audit_stats['pass_count']} ({audit_stats['pass_count']/audit_stats['total_audits']*100 if audit_stats['total_audits'] > 0 else 0:.1f}%)",
            f"- **WARN:** {audit_stats['warn_count']} ({audit_stats['warn_count']/audit_stats['total_audits']*100 if audit_stats['total_audits'] > 0 else 0:.1f}%)",
            f"- **FAIL:** {audit_stats['fail_count']} ({audit_stats['fail_count']/audit_stats['total_audits']*100 if audit_stats['total_audits'] > 0 else 0:.1f}%)",
            "",
            "### Audit Issues",
            f"- **Slippage Warnings:** {audit_stats['slippage_warnings']}",
            f"- **Partial Fill Warnings:** {audit_stats['partial_fill_warnings']}",
            "",
            "---",
            "",
            "## Violations",
            "",
            f"- **Total Violations:** {violation_stats['total_violations']}",
            f"- **Critical:** {violation_stats['critical_count']}",
            f"- **Warnings:** {violation_stats['warn_count']}",
            f"- **Unresolved:** {violation_stats['unresolved_count']}",
            "",
        ])

        # Add recent violations
        if violation_stats['recent_violations']:
            report_lines.append("### Recent Violations")
            report_lines.append("")
            for violation in violation_stats['recent_violations'][:10]:  # Top 10
                report_lines.append(
                    f"- **[{violation['severity']}]** {violation['violation_type']}: "
                    f"{violation['ticker']} - {violation['violation_description'][:100]}"
                )
            report_lines.append("")

        report_lines.extend([
            "---",
            "",
            "## Portfolio Snapshot",
            "",
            f"- **Open Positions:** {portfolio_snapshot['open_positions']}",
            f"- **Pending Positions:** {portfolio_snapshot['pending_positions']}",
            f"- **Deployed Capital:** ${portfolio_snapshot['deployed_capital']:,.2f} ({portfolio_snapshot['deployment_pct']:.1%})",
            f"- **Total Portfolio Risk:** ${portfolio_snapshot['total_risk']:,.2f} ({portfolio_snapshot['risk_pct']:.1%})",
            "",
            "### Position Concentration",
            f"- **Largest Position:** {portfolio_snapshot['largest_position_ticker']} ({portfolio_snapshot['largest_position_pct']:.1%})",
            f"- **Largest Sector:** {portfolio_snapshot['largest_sector']} ({portfolio_snapshot['largest_sector_pct']:.1%})",
            "",
        ])

        # Check for limit breaches
        if portfolio_snapshot['largest_sector_pct'] > 0.30:
            report_lines.append(f"⚠️ **WARNING:** {portfolio_snapshot['largest_sector']} sector exceeds 30% limit")
            report_lines.append("")

        report_lines.extend([
            "---",
            "",
            f"*Report generated by Sentinel Compliance Department*",
            f"*Configuration: {self.config['version']}*"
        ])

        # Write report to file
        report_filename = f"compliance_daily_{report_date.strftime('%Y%m%d')}.md"
        report_path = self.report_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))

        # Save report summary to database
        self._save_report_to_database(report_date, trade_stats, validation_stats, audit_stats, violation_stats, portfolio_snapshot, str(report_path))

        self.logger.info(f"Daily report generated: {report_path}")
        return str(report_path)

    def _get_trade_statistics(self, report_date: date) -> Dict:
        """Get trade statistics for the day"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Count validations by type
            cursor.execute("""
                SELECT
                    SUM(CASE WHEN validation_status = 'APPROVED' THEN 1 ELSE 0 END) as approved,
                    SUM(CASE WHEN validation_status = 'REJECTED' THEN 1 ELSE 0 END) as rejected,
                    SUM(CASE WHEN trade_type = 'BUY' AND validation_status = 'APPROVED' THEN 1 ELSE 0 END) as buy,
                    SUM(CASE WHEN trade_type = 'SELL' AND validation_status = 'APPROVED' THEN 1 ELSE 0 END) as sell,
                    COUNT(*) as total
                FROM compliance_trade_validations
                WHERE DATE(validation_timestamp) = ?
            """, (report_date,))

            row = cursor.fetchone()
            approved = row[0] or 0
            rejected = row[1] or 0
            buy = row[2] or 0
            sell = row[3] or 0
            total = row[4] or 0

            return {
                'approved_trades': approved,
                'rejected_trades': rejected,
                'buy_trades': buy,
                'sell_trades': sell,
                'total_trades': total,
                'approval_rate': approved / total if total > 0 else 0
            }

        finally:
            conn.close()

    def _get_validation_statistics(self, report_date: date) -> Dict:
        """Get validation statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Total validations
            cursor.execute("""
                SELECT COUNT(*) FROM compliance_trade_validations
                WHERE DATE(validation_timestamp) = ?
            """, (report_date,))
            total = cursor.fetchone()[0] or 0

            # Approved/Rejected counts
            cursor.execute("""
                SELECT validation_status, COUNT(*)
                FROM compliance_trade_validations
                WHERE DATE(validation_timestamp) = ?
                GROUP BY validation_status
            """, (report_date,))

            status_counts = {row[0]: row[1] for row in cursor.fetchall()}

            # Rejection breakdown
            cursor.execute("""
                SELECT rejection_category, COUNT(*)
                FROM compliance_trade_validations
                WHERE DATE(validation_timestamp) = ? AND validation_status = 'REJECTED'
                GROUP BY rejection_category
            """, (report_date,))

            rejection_by_category = {row[0]: row[1] for row in cursor.fetchall() if row[0]}

            return {
                'total_validations': total,
                'approved': status_counts.get('APPROVED', 0),
                'rejected': status_counts.get('REJECTED', 0),
                'rejection_by_category': rejection_by_category
            }

        finally:
            conn.close()

    def _get_audit_statistics(self, report_date: date) -> Dict:
        """Get audit statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Total audits and status breakdown
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN audit_status = 'PASS' THEN 1 ELSE 0 END) as pass,
                    SUM(CASE WHEN audit_status = 'WARN' THEN 1 ELSE 0 END) as warn,
                    SUM(CASE WHEN audit_status = 'FAIL' THEN 1 ELSE 0 END) as fail,
                    SUM(CASE WHEN slippage_check = 'WARN' OR slippage_check = 'FAIL' THEN 1 ELSE 0 END) as slippage_warnings,
                    SUM(CASE WHEN partial_fill_check = 'WARN' OR partial_fill_check = 'FAIL' THEN 1 ELSE 0 END) as partial_fill_warnings
                FROM compliance_trade_audits
                WHERE trade_date = ?
            """, (report_date,))

            row = cursor.fetchone()

            return {
                'total_audits': row[0] or 0,
                'pass_count': row[1] or 0,
                'warn_count': row[2] or 0,
                'fail_count': row[3] or 0,
                'slippage_warnings': row[4] or 0,
                'partial_fill_warnings': row[5] or 0
            }

        finally:
            conn.close()

    def _get_violation_statistics(self, report_date: date) -> Dict:
        """Get violation statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Total violations
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END) as critical,
                    SUM(CASE WHEN severity = 'WARN' THEN 1 ELSE 0 END) as warn,
                    SUM(CASE WHEN resolution_status = 'UNRESOLVED' THEN 1 ELSE 0 END) as unresolved
                FROM compliance_violations
                WHERE DATE(violation_timestamp) = ?
            """, (report_date,))

            row = cursor.fetchone()

            # Recent violations
            cursor.execute("""
                SELECT violation_type, severity, ticker, violation_description
                FROM compliance_violations
                WHERE DATE(violation_timestamp) = ?
                ORDER BY violation_timestamp DESC
                LIMIT 10
            """, (report_date,))

            recent_violations = [
                {
                    'violation_type': row[0],
                    'severity': row[1],
                    'ticker': row[2] or 'N/A',
                    'violation_description': row[3]
                }
                for row in cursor.fetchall()
            ]

            return {
                'total_violations': row[0] or 0,
                'critical_count': row[1] or 0,
                'warn_count': row[2] or 0,
                'unresolved_count': row[3] or 0,
                'recent_violations': recent_violations
            }

        finally:
            conn.close()

    def _get_portfolio_snapshot(self) -> Dict:
        """Get current portfolio snapshot"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Position counts
            cursor.execute("""
                SELECT status, COUNT(*)
                FROM portfolio_positions
                GROUP BY status
            """)
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}

            # Deployed capital
            cursor.execute("""
                SELECT SUM(actual_entry_price * actual_shares)
                FROM portfolio_positions
                WHERE status = 'OPEN'
            """)
            deployed_capital = cursor.fetchone()[0] or 0.0

            # Total risk
            cursor.execute("""
                SELECT SUM(total_risk)
                FROM portfolio_positions
                WHERE status IN ('OPEN', 'PENDING')
            """)
            total_risk = cursor.fetchone()[0] or 0.0

            # Largest position
            cursor.execute("""
                SELECT ticker, (actual_entry_price * actual_shares) as position_value
                FROM portfolio_positions
                WHERE status = 'OPEN'
                ORDER BY position_value DESC
                LIMIT 1
            """)
            largest_position = cursor.fetchone()

            # Largest sector
            cursor.execute("""
                SELECT sector, SUM(actual_entry_price * actual_shares) as sector_value
                FROM portfolio_positions
                WHERE status = 'OPEN' AND sector IS NOT NULL
                GROUP BY sector
                ORDER BY sector_value DESC
                LIMIT 1
            """)
            largest_sector = cursor.fetchone()

            total_capital = self.config['capital']['total']

            return {
                'open_positions': status_counts.get('OPEN', 0),
                'pending_positions': status_counts.get('PENDING', 0),
                'deployed_capital': deployed_capital,
                'deployment_pct': deployed_capital / total_capital if total_capital > 0 else 0,
                'total_risk': total_risk,
                'risk_pct': total_risk / total_capital if total_capital > 0 else 0,
                'largest_position_ticker': largest_position[0] if largest_position else 'N/A',
                'largest_position_pct': (largest_position[1] / deployed_capital if deployed_capital > 0 else 0) if largest_position else 0,
                'largest_sector': largest_sector[0] if largest_sector else 'N/A',
                'largest_sector_pct': (largest_sector[1] / deployed_capital if deployed_capital > 0 else 0) if largest_sector else 0
            }

        finally:
            conn.close()

    def _save_report_to_database(self, report_date: date, trade_stats: Dict, validation_stats: Dict,
                                 audit_stats: Dict, violation_stats: Dict, portfolio_snapshot: Dict, report_path: str):
        """Save report summary to compliance_daily_reports table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO compliance_daily_reports (
                    report_date,
                    report_generated_at,
                    total_trades,
                    buy_trades,
                    sell_trades,
                    approved_trades,
                    rejected_trades,
                    total_validations,
                    position_size_failures,
                    sector_limit_failures,
                    risk_limit_failures,
                    duplicate_order_failures,
                    restricted_ticker_failures,
                    total_audits,
                    audit_pass,
                    audit_warn,
                    audit_fail,
                    slippage_warnings,
                    partial_fill_warnings,
                    total_violations,
                    critical_violations,
                    warn_violations,
                    unresolved_violations,
                    positions_count,
                    deployed_capital,
                    total_portfolio_risk,
                    largest_position_pct,
                    largest_sector_pct,
                    report_file_path
                ) VALUES (?, datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                report_date,
                trade_stats['total_trades'],
                trade_stats['buy_trades'],
                trade_stats['sell_trades'],
                trade_stats['approved_trades'],
                trade_stats['rejected_trades'],
                validation_stats['total_validations'],
                validation_stats['rejection_by_category'].get('POSITION_SIZE', 0),
                validation_stats['rejection_by_category'].get('SECTOR_LIMIT', 0),
                validation_stats['rejection_by_category'].get('RISK_LIMIT', 0),
                validation_stats['rejection_by_category'].get('DUPLICATE', 0),
                validation_stats['rejection_by_category'].get('RESTRICTED', 0),
                audit_stats['total_audits'],
                audit_stats['pass_count'],
                audit_stats['warn_count'],
                audit_stats['fail_count'],
                audit_stats['slippage_warnings'],
                audit_stats['partial_fill_warnings'],
                violation_stats['total_violations'],
                violation_stats['critical_count'],
                violation_stats['warn_count'],
                violation_stats['unresolved_count'],
                portfolio_snapshot['open_positions'],
                portfolio_snapshot['deployed_capital'],
                portfolio_snapshot['total_risk'],
                portfolio_snapshot['largest_position_pct'],
                portfolio_snapshot['largest_sector_pct'],
                report_path
            ))

            conn.commit()
            self.logger.info(f"Report summary saved to database for {report_date}")

        finally:
            conn.close()

    def generate_trade_csv(self, report_date: date = None) -> str:
        """
        Generate CSV export of all trade validations for a specific date
        Returns: Path to generated CSV file
        """
        if report_date is None:
            report_date = datetime.now().date()

        # Query all validations for this date
        query = """
            SELECT
                trade_proposal_message_id,
                ticker,
                trade_type,
                shares,
                price,
                position_value,
                sector,
                validation_status,
                position_size_check,
                sector_concentration_check,
                risk_limit_check,
                duplicate_order_check,
                restricted_ticker_check,
                rejection_reason,
                rejection_category,
                validation_timestamp
            FROM compliance_trade_validations
            WHERE DATE(validation_timestamp) = ?
            ORDER BY validation_timestamp ASC
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        rows = cursor.execute(query, (report_date,)).fetchall()
        conn.close()

        # Build CSV
        csv_lines = []

        # Header
        csv_lines.append(",".join([
            "Message ID", "Ticker", "Type", "Shares", "Price", "Position Value",
            "Sector", "Status", "Position Size Check",
            "Sector Check", "Risk Check", "Duplicate Check", "Restricted Check",
            "Rejection Reason", "Rejection Category", "Timestamp"
        ]))

        # Data rows
        for row in rows:
            csv_lines.append(",".join([
                str(row[0]),  # message_id
                str(row[1]),  # ticker
                str(row[2]),  # trade_type
                str(row[3]),  # shares
                f"{row[4]:.2f}" if row[4] else "",  # price
                f"{row[5]:.2f}" if row[5] else "",  # position_value
                str(row[6]) if row[6] else "",  # sector
                str(row[7]),  # validation_status
                str(row[8]) if row[8] else "",  # position_size_check
                str(row[9]) if row[9] else "",  # sector_concentration_check
                str(row[10]) if row[10] else "",  # risk_limit_check
                str(row[11]) if row[11] else "",  # duplicate_order_check
                str(row[12]) if row[12] else "",  # restricted_ticker_check
                f'"{row[13]}"' if row[13] else "",  # rejection_reason (quoted for commas)
                str(row[14]) if row[14] else "",  # rejection_category
                str(row[15])  # validation_timestamp
            ]))

        # Write to file
        csv_path = self.report_dir / f"compliance_trades_{report_date.strftime('%Y%m%d')}.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(csv_lines))

        print(f"  Trade CSV exported: {csv_path}")
        return str(csv_path)

    def generate_violation_csv(self, report_date: date = None) -> str:
        """
        Generate CSV export of all violations for a specific date
        Returns: Path to generated CSV file
        """
        if report_date is None:
            report_date = datetime.now().date()

        # Query all violations for this date
        query = """
            SELECT
                id,
                trade_proposal_message_id,
                position_id,
                ticker,
                violation_type,
                severity,
                rule_name,
                rule_limit,
                actual_value,
                breach_amount,
                violation_description,
                resolution_status,
                resolution_notes,
                resolved_at,
                violation_timestamp
            FROM compliance_violations
            WHERE DATE(violation_timestamp) = ?
            ORDER BY severity DESC, violation_timestamp ASC
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        rows = cursor.execute(query, (report_date,)).fetchall()
        conn.close()

        # Build CSV
        csv_lines = []

        # Header
        csv_lines.append(",".join([
            "ID", "Trade Proposal Message ID", "Position ID", "Ticker",
            "Violation Type", "Severity", "Rule Name", "Rule Limit",
            "Actual Value", "Breach Amount", "Description",
            "Resolution Status", "Resolution Notes", "Resolved At", "Violation Timestamp"
        ]))

        # Data rows
        for row in rows:
            csv_lines.append(",".join([
                str(row[0]),  # id
                str(row[1]) if row[1] else "",  # trade_proposal_message_id
                str(row[2]) if row[2] else "",  # position_id
                str(row[3]) if row[3] else "",  # ticker
                str(row[4]),  # violation_type
                str(row[5]),  # severity
                str(row[6]),  # rule_name
                f"{row[7]:.4f}" if row[7] else "",  # rule_limit
                f"{row[8]:.4f}" if row[8] else "",  # actual_value
                f"{row[9]:.4f}" if row[9] else "",  # breach_amount
                f'"{row[10]}"' if row[10] else "",  # violation_description (quoted)
                str(row[11]),  # resolution_status
                f'"{row[12]}"' if row[12] else "",  # resolution_notes (quoted)
                str(row[13]) if row[13] else "",  # resolved_at
                str(row[14])  # violation_timestamp
            ]))

        # Write to file
        csv_path = self.report_dir / f"compliance_violations_{report_date.strftime('%Y%m%d')}.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(csv_lines))

        print(f"  Violation CSV exported: {csv_path}")
        return str(csv_path)

    def generate_portfolio_json(self) -> str:
        """
        Generate JSON export of current portfolio snapshot
        Returns: Path to generated JSON file
        """
        snapshot = self._get_portfolio_snapshot()

        # Build JSON structure
        portfolio_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "summary": {
                "open_positions": snapshot['open_positions'],
                "pending_positions": snapshot['pending_positions'],
                "capital_deployed": snapshot['deployed_capital'],
                "deployment_percentage": snapshot['deployment_pct']
            },
            "risk": {
                "total_portfolio_risk": snapshot['total_risk'],
                "risk_percentage": snapshot['risk_pct']
            },
            "concentration": {
                "largest_position_ticker": snapshot['largest_position_ticker'],
                "largest_position_percentage": snapshot['largest_position_pct'],
                "largest_sector": snapshot['largest_sector'],
                "largest_sector_percentage": snapshot['largest_sector_pct']
            },
            "positions": []
        }

        # Get all open positions
        query = """
            SELECT
                position_id,
                ticker,
                status,
                actual_shares,
                actual_entry_price,
                intended_stop_loss,
                intended_target,
                total_risk,
                sector,
                actual_entry_date
            FROM portfolio_positions
            WHERE status IN ('PENDING', 'OPEN')
            ORDER BY actual_entry_price * actual_shares DESC
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        rows = cursor.execute(query).fetchall()
        conn.close()

        for row in rows:
            position_value = (row[3] * row[4]) if row[3] and row[4] else 0
            portfolio_data['positions'].append({
                "position_id": row[0],
                "ticker": row[1],
                "status": row[2],
                "shares": row[3],
                "entry_price": row[4],
                "position_value": position_value,
                "stop_loss": row[5],
                "target": row[6],
                "risk": row[7],
                "sector": row[8],
                "entry_date": row[9]
            })

        # Write to file
        import json
        json_path = self.report_dir / f"compliance_portfolio_{datetime.now().strftime('%Y%m%d')}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(portfolio_data, f, indent=2)

        print(f"  Portfolio JSON exported: {json_path}")
        return str(json_path)


# ============================================================================
# CLASS 4: COMPLIANCE DEPARTMENT ORCHESTRATOR (Week 5 Day 4)
# ============================================================================
class ComplianceDepartment:
    """
    Main orchestrator for Compliance Department
    Integrates PreTradeValidator, PostTradeAuditor, and ComplianceReporter
    Handles message-based communication with Portfolio and Trading departments
    """

    def __init__(self, config_path: Path, db_path: Path):
        self.config_path = config_path
        self.db_path = db_path
        self.logger = logging.getLogger(self.__class__.__name__)

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.logger.info(f"Compliance Department initializing...")
        self.logger.info(f"  Config: {config_path}")
        self.logger.info(f"  Database: {db_path}")
        self.logger.info(f"  Version: {self.config['version']}")

        # Initialize components
        self.validator = PreTradeValidator(self.config, self.db_path)
        self.auditor = PostTradeAuditor(self.config, self.db_path)
        self.reporter = ComplianceReporter(self.config, self.db_path)

        # Message directories
        self.inbox_dir = Path("Messages/Compliance/Inbox")
        self.outbox_dir = Path("Messages/Compliance/Outbox")
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.outbox_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("Compliance Department initialized successfully")
        self.logger.info(f"  Inbox: {self.inbox_dir}")
        self.logger.info(f"  Outbox: {self.outbox_dir}")

    def process_trade_proposal(self, proposal_message_path: Path) -> Path:
        """
        Process TradeProposal message from Portfolio Department
        Validate against all compliance rules
        Return TradeApproval or TradeRejection message

        Args:
            proposal_message_path: Path to TradeProposal message file

        Returns:
            response_message_path: Path to TradeApproval/TradeRejection message
        """
        self.logger.info(f"Processing TradeProposal: {proposal_message_path.name}")

        # Read proposal message
        with open(proposal_message_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML frontmatter + Markdown body
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
        else:
            self.logger.error(f"Invalid message format: {proposal_message_path.name}")
            return None

        # Extract proposal data
        proposal_data = frontmatter.get('payload', {})
        message_id = frontmatter.get('message_id')

        self.logger.info(f"  Message ID: {message_id}")
        self.logger.info(f"  Ticker: {proposal_data.get('ticker')}")
        self.logger.info(f"  Type: {proposal_data.get('trade_type')}")
        self.logger.info(f"  Shares: {proposal_data.get('shares')}")
        self.logger.info(f"  Price: ${proposal_data.get('price'):.2f}")

        # Validate trade
        is_approved, rejection_reason, rejection_category, check_results = self.validator.validate_trade(proposal_data)

        # Generate response message
        response_message_id = f"MSG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        if is_approved:
            message_type = "TradeApproval"
            status = "APPROVED"
            self.logger.info(f"  ✅ APPROVED - All compliance checks passed")
        else:
            message_type = "TradeRejection"
            status = "REJECTED"
            self.logger.info(f"  ❌ REJECTED - {rejection_reason}")

        # Build response message
        response = {
            'message_id': response_message_id,
            'message_type': message_type,
            'from': 'Compliance',
            'to': 'Portfolio',
            'timestamp': datetime.now().isoformat(),
            'in_reply_to': message_id,
            'payload': {
                'trade_proposal_message_id': message_id,
                'ticker': proposal_data.get('ticker'),
                'validation_status': status,
                'rejection_reason': rejection_reason,
                'rejection_category': rejection_category,
                'check_results': check_results
            }
        }

        # Write response message
        response_filename = f"{message_type}_{proposal_data.get('ticker')}_{response_message_id}.md"
        response_path = self.outbox_dir / response_filename

        with open(response_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(yaml.dump(response, default_flow_style=False))
            f.write("---\n\n")
            f.write(f"# {message_type}\n\n")
            f.write(f"**Ticker:** {proposal_data.get('ticker')}\n")
            f.write(f"**Status:** {status}\n")
            f.write(f"**Trade Proposal:** {message_id}\n\n")

            if is_approved:
                f.write("## Compliance Checks: PASSED\n\n")
                for check_name, check_result in check_results.items():
                    f.write(f"- ✅ {check_name}: {check_result}\n")
            else:
                f.write(f"## Rejection Details\n\n")
                f.write(f"**Category:** {rejection_category}\n")
                f.write(f"**Reason:** {rejection_reason}\n\n")
                f.write("## Failed Checks\n\n")
                for check_name, check_result in check_results.items():
                    icon = "❌" if check_result == "FAIL" else "✅"
                    f.write(f"- {icon} {check_name}: {check_result}\n")

        self.logger.info(f"  Response message saved: {response_filename}")
        return response_path

    def audit_fill_confirmation(self, fill_message_path: Path) -> Path:
        """
        Audit FillConfirmation message from Trading Department
        Check for slippage, partial fills, parameter accuracy
        Return AuditReport message

        Args:
            fill_message_path: Path to FillConfirmation message file

        Returns:
            audit_report_path: Path to AuditReport message
        """
        self.logger.info(f"Auditing FillConfirmation: {fill_message_path.name}")

        # Read fill confirmation message
        with open(fill_message_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML frontmatter
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
        else:
            self.logger.error(f"Invalid message format: {fill_message_path.name}")
            return None

        fill_data = frontmatter.get('payload', {})
        message_id = frontmatter.get('message_id')

        self.logger.info(f"  Message ID: {message_id}")
        self.logger.info(f"  Position ID: {fill_data.get('position_id')}")
        self.logger.info(f"  Ticker: {fill_data.get('ticker')}")

        # Get position data from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ticker, intended_shares, intended_entry_price,
                intended_stop_loss, intended_target,
                actual_shares, actual_entry_price,
                actual_stop_loss, actual_target
            FROM portfolio_positions
            WHERE position_id = ?
        """, (fill_data.get('position_id'),))

        position = cursor.fetchone()
        conn.close()

        if not position:
            self.logger.error(f"  Position not found: {fill_data.get('position_id')}")
            return None

        # Build position dict
        position_data = {
            'ticker': position[0],
            'intended_shares': position[1],
            'intended_entry_price': position[2],
            'intended_stop_loss': position[3],
            'intended_target': position[4],
            'actual_shares': position[5],
            'actual_entry_price': position[6],
            'actual_stop_loss': position[7],
            'actual_target': position[8]
        }

        # Audit the fill
        audit_result = self.auditor.audit_fill(position_data, fill_data)

        # Generate audit report message
        report_message_id = f"MSG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        self.logger.info(f"  Audit Status: {audit_result['audit_status']}")
        if audit_result['audit_status'] == 'FAIL':
            self.logger.warning(f"  ⚠️ AUDIT FAILED - {len(audit_result['findings'])} issues found")
        elif audit_result['audit_status'] == 'WARN':
            self.logger.warning(f"  ⚠️ WARNINGS - {len([f for f in audit_result['findings'] if 'WARNING' in f])} warnings")

        # Build audit report message
        report = {
            'message_id': report_message_id,
            'message_type': 'AuditReport',
            'from': 'Compliance',
            'to': 'Executive',
            'timestamp': datetime.now().isoformat(),
            'in_reply_to': message_id,
            'payload': {
                'fill_confirmation_message_id': message_id,
                'position_id': fill_data.get('position_id'),
                'ticker': position_data['ticker'],
                'audit_status': audit_result['audit_status'],
                'severity': audit_result['severity'],
                'findings': audit_result['findings'],
                'check_results': audit_result['checks']
            }
        }

        # Write audit report message
        report_filename = f"AuditReport_{position_data['ticker']}_{report_message_id}.md"
        report_path = self.outbox_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(yaml.dump(report, default_flow_style=False))
            f.write("---\n\n")
            f.write(f"# Audit Report\n\n")
            f.write(f"**Position:** {fill_data.get('position_id')}\n")
            f.write(f"**Ticker:** {position_data['ticker']}\n")
            f.write(f"**Status:** {audit_result['audit_status']}\n")
            f.write(f"**Severity:** {audit_result['severity']}\n\n")

            f.write("## Audit Checks\n\n")
            for check_name, check_result in audit_result['checks'].items():
                icon = "✅" if check_result == "PASS" else ("⚠️" if check_result == "WARN" else "❌")
                f.write(f"- {icon} {check_name}: {check_result}\n")

            if audit_result['findings']:
                f.write("\n## Findings\n\n")
                for finding in audit_result['findings']:
                    f.write(f"- {finding}\n")

        self.logger.info(f"  Audit report saved: {report_filename}")
        return report_path

    def run_daily_cycle(self, report_date: date = None) -> Dict[str, str]:
        """
        Run end-of-day compliance cycle
        Generate daily reports in all formats

        Args:
            report_date: Date for reports (defaults to today)

        Returns:
            report_paths: Dict of report type -> file path
        """
        if report_date is None:
            report_date = datetime.now().date()

        self.logger.info(f"Running daily compliance cycle for {report_date}")

        report_paths = {}

        # Generate markdown report
        self.logger.info("  Generating daily report (Markdown)...")
        report_paths['markdown'] = self.reporter.generate_daily_report(report_date)

        # Generate trade CSV
        self.logger.info("  Generating trade CSV...")
        report_paths['trade_csv'] = self.reporter.generate_trade_csv(report_date)

        # Generate violation CSV
        self.logger.info("  Generating violation CSV...")
        report_paths['violation_csv'] = self.reporter.generate_violation_csv(report_date)

        # Generate portfolio JSON
        self.logger.info("  Generating portfolio JSON...")
        report_paths['portfolio_json'] = self.reporter.generate_portfolio_json()

        self.logger.info(f"Daily compliance cycle complete - {len(report_paths)} reports generated")

        return report_paths

    def get_compliance_status(self) -> Dict:
        """
        Get current compliance status summary
        Used by Executive Department for daily briefings

        Returns:
            status: Dict with compliance metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get today's validation stats
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN validation_status = 'APPROVED' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN validation_status = 'REJECTED' THEN 1 ELSE 0 END) as rejected
            FROM compliance_trade_validations
            WHERE DATE(validation_timestamp) = DATE('now')
        """)
        validation_stats = cursor.fetchone()

        # Get today's audit stats
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN audit_status = 'PASS' THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN audit_status = 'WARN' THEN 1 ELSE 0 END) as warned,
                SUM(CASE WHEN audit_status = 'FAIL' THEN 1 ELSE 0 END) as failed
            FROM compliance_trade_audits
            WHERE DATE(trade_date) = DATE('now')
        """)
        audit_stats = cursor.fetchone()

        # Get unresolved violations
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END) as critical,
                SUM(CASE WHEN severity = 'WARN' THEN 1 ELSE 0 END) as warnings
            FROM compliance_violations
            WHERE resolution_status = 'UNRESOLVED'
        """)
        violation_stats = cursor.fetchone()

        conn.close()

        status = {
            'timestamp': datetime.now().isoformat(),
            'validations': {
                'total': validation_stats[0] or 0,
                'approved': validation_stats[1] or 0,
                'rejected': validation_stats[2] or 0,
                'approval_rate': (validation_stats[1] / validation_stats[0] * 100) if validation_stats[0] > 0 else 0.0
            },
            'audits': {
                'total': audit_stats[0] or 0,
                'passed': audit_stats[1] or 0,
                'warned': audit_stats[2] or 0,
                'failed': audit_stats[3] or 0
            },
            'violations': {
                'unresolved': violation_stats[0] or 0,
                'critical': violation_stats[1] or 0,
                'warnings': violation_stats[2] or 0
            }
        }

        return status


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
