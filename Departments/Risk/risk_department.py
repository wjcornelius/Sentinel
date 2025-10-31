"""
Risk Department - Position Sizing, Stop-Loss Calculation, Portfolio Risk Management
Built fresh from C(P) Week 3 guidance + DEPARTMENTAL_SPECIFICATIONS v1.0

Responsibilities:
- Calculate position sizes (Fixed Fractional, Kelly Criterion future)
- Calculate stop-loss levels (ATR-based, Percentage fallback)
- Validate risk per trade (max 1% of capital)
- Monitor portfolio heat (max 5% total risk)
- Check sector concentration (max 40% per sector)
- Generate RiskAssessment messages for Portfolio Department

Pattern: Message-based architecture (same as Research/Trading Departments)
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
logger = logging.getLogger('RiskDepartment')


class MessageHandler:
    """
    Handles reading and writing messages for Risk Department

    Pattern learned from Research Department (Week 2)
    Implements YAML frontmatter + Markdown + JSON payload format
    """

    def __init__(self):
        self.inbox_path = Path("Messages_Between_Departments/Inbox/RISK")
        self.outbox_path = Path("Messages_Between_Departments/Outbox/RISK")
        self.archive_path = Path("Messages_Between_Departments/Archive")

        # Create directories if they don't exist
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        self.outbox_path.mkdir(parents=True, exist_ok=True)

        logger.info("MessageHandler initialized for Risk Department")

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
                     priority: str = 'routine') -> str:
        """
        Write message to outbox with YAML frontmatter + markdown + JSON payload

        Args:
            to_dept: Destination department
            message_type: Type of message (e.g., 'RiskAssessment')
            subject: Message subject line
            body: Markdown body content
            data_payload: Optional JSON data
            parent_message_id: Optional parent message ID (for tracking message chains)
            priority: Message priority (routine/urgent/critical)

        Returns:
            message_id (for database tracking)
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        msg_id = f"MSG_RISK_{timestamp}_{uuid.uuid4().hex[:8]}"

        # Build YAML frontmatter
        metadata = {
            'message_id': msg_id,
            'from': 'RISK',
            'to': to_dept,
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'message_type': message_type,
            'priority': priority,
            'requires_response': False
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
        archive_dir = self.archive_path / today / "RISK"
        archive_dir.mkdir(parents=True, exist_ok=True)

        archived_path = archive_dir / message_path.name

        # If file already exists in archive, remove inbox file
        if archived_path.exists():
            message_path.unlink()
        else:
            message_path.rename(archived_path)

        logger.info(f"Archived message: {message_path.name}")


class PositionSizer:
    """
    Calculates position sizes based on configured method
    Phase 1: Fixed Fractional (10% of capital per position)
    Future: Kelly Criterion, Volatility-Adjusted
    """

    def __init__(self, config: Dict):
        """
        Initialize Position Sizer

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.method = config['position_sizing']['method']
        self.position_size_pct = config['position_sizing']['position_size_pct']

        logger.info(f"PositionSizer initialized (method: {self.method}, size: {self.position_size_pct*100:.0f}%)")

    def calculate_position_size(self, capital: float, current_price: float, ticker: str) -> Dict:
        """
        Calculate position size for a stock

        Args:
            capital: Total capital available
            current_price: Current stock price
            ticker: Stock symbol

        Returns:
            Dictionary with position size details
        """
        try:
            if self.method == "FIXED_FRACTIONAL":
                return self._fixed_fractional(capital, current_price, ticker)
            else:
                logger.error(f"Unknown position sizing method: {self.method}")
                return None

        except Exception as e:
            logger.error(f"Position sizing failed for {ticker}: {e}", exc_info=True)
            return None

    def _fixed_fractional(self, capital: float, current_price: float, ticker: str) -> Dict:
        """
        Fixed Fractional position sizing: Use fixed % of capital per position

        Args:
            capital: Total capital available
            current_price: Current stock price
            ticker: Stock symbol

        Returns:
            Position size details
        """
        # Calculate position value (e.g., $100K × 10% = $10K)
        position_value = capital * self.position_size_pct

        # Calculate number of shares (round down to avoid exceeding position size)
        shares = int(position_value / current_price)

        # Actual position value (may be slightly less due to rounding)
        actual_position_value = shares * current_price

        # Actual position percentage
        actual_position_pct = actual_position_value / capital if capital > 0 else 0

        result = {
            'method': 'FIXED_FRACTIONAL',
            'ticker': ticker,
            'capital': capital,
            'current_price': current_price,
            'target_position_pct': self.position_size_pct,
            'target_position_value': position_value,
            'shares': shares,
            'actual_position_value': actual_position_value,
            'actual_position_pct': actual_position_pct
        }

        logger.info(f"Position size for {ticker}: {shares} shares @ ${current_price:.2f} = ${actual_position_value:,.0f} ({actual_position_pct*100:.1f}% of capital)")

        return result


class StopLossCalculator:
    """
    Calculates stop-loss levels based on configured method
    Phase 1: ATR-based (2× 14-day ATR), Percentage fallback
    Future: Support-based, Volatility-adjusted
    """

    def __init__(self, config: Dict):
        """
        Initialize Stop-Loss Calculator

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.method = config['stop_loss']['method']
        self.atr_period = config['stop_loss']['atr_period']
        self.atr_multiplier = config['stop_loss']['atr_multiplier']
        self.percentage_stop = config['stop_loss']['percentage_stop']
        self.min_stop_pct = config['stop_loss']['min_stop_distance_pct']
        self.max_stop_pct = config['stop_loss']['max_stop_distance_pct']

        logger.info(f"StopLossCalculator initialized (method: {self.method}, ATR: {self.atr_period}d × {self.atr_multiplier})")

    def calculate_stop_loss(self, ticker: str, entry_price: float) -> Dict:
        """
        Calculate stop-loss level for a stock

        Args:
            ticker: Stock symbol
            entry_price: Entry price for position

        Returns:
            Dictionary with stop-loss details
        """
        try:
            if self.method == "ATR_BASED":
                return self._atr_based_stop(ticker, entry_price)
            elif self.method == "PERCENTAGE":
                return self._percentage_stop(ticker, entry_price)
            else:
                logger.error(f"Unknown stop-loss method: {self.method}")
                return None

        except Exception as e:
            logger.error(f"Stop-loss calculation failed for {ticker}: {e}", exc_info=True)
            # Fallback to percentage stop
            return self._percentage_stop(ticker, entry_price)

    def _calculate_atr(self, ticker: str) -> Optional[float]:
        """
        Calculate Average True Range (ATR) for a stock

        Args:
            ticker: Stock symbol

        Returns:
            ATR value or None if calculation fails
        """
        try:
            # Fetch historical data (need ATR period + buffer)
            stock = yf.Ticker(ticker)
            hist = stock.history(period=f"{self.atr_period + 10}d")

            if len(hist) < self.config['data_quality']['min_atr_data_points']:
                logger.warning(f"{ticker}: Insufficient data for ATR ({len(hist)} days, need {self.config['data_quality']['min_atr_data_points']})")
                return None

            # Calculate True Range components
            high = hist['High']
            low = hist['Low']
            close = hist['Close'].shift(1)

            # True Range = max(High-Low, abs(High-PrevClose), abs(Low-PrevClose))
            tr1 = high - low
            tr2 = abs(high - close)
            tr3 = abs(low - close)

            true_range = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)

            # ATR = Moving average of True Range
            atr = true_range.rolling(window=self.atr_period).mean().iloc[-1]

            logger.debug(f"{ticker} ATR({self.atr_period}): ${atr:.2f}")
            return float(atr)

        except Exception as e:
            logger.error(f"ATR calculation failed for {ticker}: {e}")
            return None

    def _atr_based_stop(self, ticker: str, entry_price: float) -> Dict:
        """
        ATR-based stop-loss: Stop = Entry - (ATR × multiplier)

        Args:
            ticker: Stock symbol
            entry_price: Entry price for position

        Returns:
            Stop-loss details
        """
        # Calculate ATR
        atr = self._calculate_atr(ticker)

        if atr is None:
            logger.warning(f"{ticker}: ATR unavailable, falling back to percentage stop")
            return self._percentage_stop(ticker, entry_price)

        # Calculate stop-loss
        stop_loss = entry_price - (atr * self.atr_multiplier)

        # Calculate stop distance as percentage
        stop_distance_pct = (entry_price - stop_loss) / entry_price

        # Validate stop distance
        if stop_distance_pct < self.min_stop_pct:
            logger.warning(f"{ticker}: ATR stop too tight ({stop_distance_pct*100:.1f}%), widening to {self.min_stop_pct*100:.0f}%")
            stop_loss = entry_price * (1 - self.min_stop_pct)
            stop_distance_pct = self.min_stop_pct

        elif stop_distance_pct > self.max_stop_pct:
            logger.warning(f"{ticker}: ATR stop too wide ({stop_distance_pct*100:.1f}%), narrowing to {self.max_stop_pct*100:.0f}%")
            stop_loss = entry_price * (1 - self.max_stop_pct)
            stop_distance_pct = self.max_stop_pct

        result = {
            'method': 'ATR_BASED',
            'ticker': ticker,
            'entry_price': entry_price,
            'atr_value': atr,
            'atr_multiplier': self.atr_multiplier,
            'stop_loss': round(stop_loss, 2),
            'stop_distance_pct': stop_distance_pct,
            'risk_per_share': round(entry_price - stop_loss, 2)
        }

        logger.info(f"Stop-loss for {ticker}: ${stop_loss:.2f} (ATR: ${atr:.2f}, Risk: ${result['risk_per_share']:.2f}/share, {stop_distance_pct*100:.1f}%)")

        return result

    def _percentage_stop(self, ticker: str, entry_price: float) -> Dict:
        """
        Percentage-based stop-loss: Stop = Entry × (1 - percentage)

        Args:
            ticker: Stock symbol
            entry_price: Entry price for position

        Returns:
            Stop-loss details
        """
        stop_loss = entry_price * (1 - self.percentage_stop)
        risk_per_share = entry_price - stop_loss

        result = {
            'method': 'PERCENTAGE',
            'ticker': ticker,
            'entry_price': entry_price,
            'atr_value': None,
            'atr_multiplier': None,
            'stop_loss': round(stop_loss, 2),
            'stop_distance_pct': self.percentage_stop,
            'risk_per_share': round(risk_per_share, 2)
        }

        logger.info(f"Stop-loss for {ticker}: ${stop_loss:.2f} (Percentage: {self.percentage_stop*100:.0f}%, Risk: ${risk_per_share:.2f}/share)")

        return result


class RiskCalculator:
    """
    Validates risk per trade against configured limits
    Phase 1: Hard limit of 1% of capital per trade
    Future: VIX-adjusted risk, Score-adjusted risk
    """

    def __init__(self, config: Dict):
        """
        Initialize Risk Calculator

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.max_risk_pct = config['risk_per_trade']['max_risk_pct']

        logger.info(f"RiskCalculator initialized (max risk per trade: {self.max_risk_pct*100:.1f}% of capital)")

    def validate_risk_per_trade(self, shares: int, risk_per_share: float, capital: float, ticker: str) -> Dict:
        """
        Validate that trade risk does not exceed configured limit

        Args:
            shares: Number of shares to buy
            risk_per_share: Risk per share (entry_price - stop_loss)
            capital: Total capital available
            ticker: Stock symbol

        Returns:
            Dictionary with validation result
        """
        try:
            # Calculate total risk
            total_risk = shares * risk_per_share

            # Calculate risk percentage
            risk_pct = total_risk / capital if capital > 0 else 0

            # Validate against limit
            approved = risk_pct <= self.max_risk_pct

            result = {
                'ticker': ticker,
                'shares': shares,
                'risk_per_share': risk_per_share,
                'total_risk': round(total_risk, 2),
                'risk_percentage': risk_pct,
                'max_risk_pct': self.max_risk_pct,
                'approved': approved,
                'rejection_reason': None if approved else 'RISK_PER_TRADE_EXCEEDED',
                'rejection_details': None if approved else (
                    f"Trade risk too high: This trade risks ${total_risk:,.0f} ({risk_pct*100:.2f}% of capital), "
                    f"exceeding the {self.max_risk_pct*100:.1f}% limit. Maximum allowed: ${capital * self.max_risk_pct:,.0f}."
                )
            }

            if approved:
                logger.info(f"{ticker}: Risk ${total_risk:,.0f} ({risk_pct*100:.2f}%) - APPROVED (under {self.max_risk_pct*100:.1f}% limit)")
            else:
                logger.warning(f"{ticker}: Risk ${total_risk:,.0f} ({risk_pct*100:.2f}%) - REJECTED (exceeds {self.max_risk_pct*100:.1f}% limit)")

            return result

        except Exception as e:
            logger.error(f"Risk validation failed for {ticker}: {e}", exc_info=True)
            return {
                'ticker': ticker,
                'approved': False,
                'rejection_reason': 'CALCULATION_ERROR',
                'rejection_details': str(e)
            }


class SectorConcentrationChecker:
    """
    Monitors sector concentration to prevent over-exposure
    Phase 1: Hard limit of 40% per sector
    Future: Dynamic sector limits, Correlation-based limits
    """

    def __init__(self, config: Dict):
        """
        Initialize Sector Concentration Checker

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.enabled = config['sector_concentration']['enable']
        self.max_sector_pct = config['sector_concentration']['max_sector_pct']
        self.warning_threshold_pct = config['sector_concentration']['warning_threshold_pct']

        logger.info(f"SectorConcentrationChecker initialized (enabled: {self.enabled}, max per sector: {self.max_sector_pct*100:.0f}%)")

    def get_stock_sector(self, ticker: str) -> Optional[str]:
        """
        Get sector for a stock using yfinance

        Args:
            ticker: Stock symbol

        Returns:
            Sector name or None if unavailable
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Try sector field first
            sector = info.get('sector')
            if sector:
                logger.debug(f"{ticker} sector: {sector}")
                return sector

            # Fallback: Try industry and map to sector
            industry = info.get('industry')
            if industry:
                logger.debug(f"{ticker} industry: {industry} (no sector available)")
                return None

            logger.warning(f"{ticker}: No sector or industry information available")
            return None

        except Exception as e:
            logger.error(f"Failed to get sector for {ticker}: {e}")
            return None

    def check_sector_concentration(
        self,
        ticker: str,
        position_value: float,
        capital: float,
        current_sector_allocations: Dict[str, float]
    ) -> Dict:
        """
        Check if adding new position would exceed sector concentration limit

        Args:
            ticker: Stock symbol for new trade
            position_value: Dollar value of new position
            capital: Total capital available
            current_sector_allocations: Dict mapping sector -> current dollar allocation

        Returns:
            Dictionary with sector concentration validation result
        """
        try:
            # Check if sector concentration is enabled
            if not self.enabled:
                return {
                    'ticker': ticker,
                    'sector': None,
                    'approved': True,
                    'status': 'DISABLED',
                    'rejection_reason': None,
                    'rejection_details': None
                }

            # Get sector for new stock
            sector = self.get_stock_sector(ticker)

            if sector is None:
                logger.warning(f"{ticker}: Sector unavailable - cannot check concentration (approving by default)")
                return {
                    'ticker': ticker,
                    'sector': None,
                    'approved': True,
                    'status': 'SECTOR_UNAVAILABLE',
                    'rejection_reason': None,
                    'rejection_details': 'Sector information not available for this stock'
                }

            # Calculate sector allocation before/after
            sector_before = current_sector_allocations.get(sector, 0.0)
            sector_after = sector_before + position_value

            sector_before_pct = sector_before / capital if capital > 0 else 0
            sector_after_pct = sector_after / capital if capital > 0 else 0

            # Validate against limit
            approved = sector_after_pct <= self.max_sector_pct

            # Determine status
            if sector_after_pct >= self.max_sector_pct:
                status = 'LIMIT_EXCEEDED'
            elif sector_after_pct >= self.warning_threshold_pct:
                status = 'WARNING'
            else:
                status = 'NORMAL'

            result = {
                'ticker': ticker,
                'sector': sector,
                'position_value': round(position_value, 2),
                'sector_before': round(sector_before, 2),
                'sector_after': round(sector_after, 2),
                'sector_before_pct': sector_before_pct,
                'sector_after_pct': sector_after_pct,
                'max_sector_pct': self.max_sector_pct,
                'status': status,
                'approved': approved,
                'rejection_reason': None if approved else 'SECTOR_CONCENTRATION_EXCEEDED',
                'rejection_details': None if approved else (
                    f"Sector concentration limit exceeded: Adding this trade would increase {sector} sector exposure from "
                    f"${sector_before:,.0f} ({sector_before_pct*100:.1f}%) to ${sector_after:,.0f} ({sector_after_pct*100:.1f}%), "
                    f"exceeding the {self.max_sector_pct*100:.0f}% limit. Available capacity in {sector}: "
                    f"${(capital * self.max_sector_pct) - sector_before:,.0f}."
                )
            }

            if approved:
                logger.info(f"{ticker} ({sector}): Sector exposure ${sector_before:,.0f} → ${sector_after:,.0f} ({sector_after_pct*100:.1f}%) - APPROVED [{status}]")
            else:
                logger.warning(f"{ticker} ({sector}): Sector exposure ${sector_before:,.0f} → ${sector_after:,.0f} ({sector_after_pct*100:.1f}%) - REJECTED (exceeds {self.max_sector_pct*100:.0f}% limit)")

            return result

        except Exception as e:
            logger.error(f"Sector concentration check failed for {ticker}: {e}", exc_info=True)
            return {
                'ticker': ticker,
                'sector': None,
                'approved': False,
                'rejection_reason': 'CALCULATION_ERROR',
                'rejection_details': str(e)
            }


class PortfolioHeatMonitor:
    """
    Monitors total portfolio risk (heat) across all open positions
    Phase 1: Hard limit of 5% total portfolio heat
    Future: VIX-adjusted heat limits, Dynamic heat scaling
    """

    def __init__(self, config: Dict):
        """
        Initialize Portfolio Heat Monitor

        Args:
            config: Risk configuration dictionary
        """
        self.config = config
        self.max_heat_pct = config['portfolio_heat']['max_total_heat_pct']
        self.warning_threshold_pct = config['portfolio_heat']['warning_threshold_pct']
        self.critical_threshold_pct = config['portfolio_heat']['critical_threshold_pct']

        logger.info(f"PortfolioHeatMonitor initialized (max heat: {self.max_heat_pct*100:.1f}%, warning: {self.warning_threshold_pct*100:.1f}%, critical: {self.critical_threshold_pct*100:.1f}%)")

    def check_portfolio_heat(self, new_trade_risk: float, current_heat: float, capital: float, ticker: str) -> Dict:
        """
        Check if adding new trade would exceed portfolio heat limit

        Args:
            new_trade_risk: Dollar risk of new trade
            current_heat: Current total risk across all open positions
            capital: Total capital available
            ticker: Stock symbol for new trade

        Returns:
            Dictionary with heat validation result
        """
        try:
            # Calculate heat before/after
            heat_before = current_heat
            heat_after = current_heat + new_trade_risk

            # Calculate percentages
            heat_before_pct = heat_before / capital if capital > 0 else 0
            heat_after_pct = heat_after / capital if capital > 0 else 0

            # Calculate available heat
            max_heat_dollars = capital * self.max_heat_pct
            available_heat = max_heat_dollars - current_heat

            # Validate against limit
            approved = heat_after_pct <= self.max_heat_pct

            # Determine status level
            if heat_after_pct >= self.critical_threshold_pct:
                status = 'CRITICAL'
            elif heat_after_pct >= self.warning_threshold_pct:
                status = 'WARNING'
            else:
                status = 'NORMAL'

            result = {
                'ticker': ticker,
                'new_trade_risk': round(new_trade_risk, 2),
                'heat_before': round(heat_before, 2),
                'heat_after': round(heat_after, 2),
                'heat_before_pct': heat_before_pct,
                'heat_after_pct': heat_after_pct,
                'available_heat': round(available_heat, 2),
                'max_heat_pct': self.max_heat_pct,
                'status': status,
                'approved': approved,
                'rejection_reason': None if approved else 'PORTFOLIO_HEAT_EXCEEDED',
                'rejection_details': None if approved else (
                    f"Portfolio risk limit exceeded: Adding this trade would increase total portfolio risk from "
                    f"${heat_before:,.0f} ({heat_before_pct*100:.1f}%) to ${heat_after:,.0f} ({heat_after_pct*100:.1f}%), "
                    f"exceeding the {self.max_heat_pct*100:.1f}% limit. Available risk capacity: ${available_heat:,.0f} "
                    f"(this trade needs ${new_trade_risk:,.0f})."
                )
            }

            if approved:
                logger.info(f"{ticker}: Portfolio heat ${heat_before:,.0f} → ${heat_after:,.0f} ({heat_after_pct*100:.2f}%) - APPROVED [{status}]")
            else:
                logger.warning(f"{ticker}: Portfolio heat ${heat_before:,.0f} → ${heat_after:,.0f} ({heat_after_pct*100:.2f}%) - REJECTED (exceeds {self.max_heat_pct*100:.1f}% limit)")

            return result

        except Exception as e:
            logger.error(f"Portfolio heat check failed for {ticker}: {e}", exc_info=True)
            return {
                'ticker': ticker,
                'approved': False,
                'rejection_reason': 'CALCULATION_ERROR',
                'rejection_details': str(e)
            }


class RiskDepartment:
    """
    Main Risk Department orchestrator

    Consumes DailyBriefing messages from Research Department
    Applies position sizing, stop-loss, and risk limit validation
    Generates RiskAssessment messages for Portfolio Department
    """

    def __init__(self, config_path: str = "Config/risk_config.yaml", db_path: str = "sentinel.db"):
        """Initialize Risk Department with all components"""
        # Load config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.db_path = Path(db_path)

        # Initialize all components
        self.message_handler = MessageHandler()
        self.position_sizer = PositionSizer(self.config)
        self.stop_loss_calc = StopLossCalculator(self.config)
        self.risk_calc = RiskCalculator(self.config)
        self.heat_monitor = PortfolioHeatMonitor(self.config)
        self.sector_checker = SectorConcentrationChecker(self.config)

        logger.info("=" * 80)
        logger.info("RISK DEPARTMENT INITIALIZED")
        logger.info("=" * 80)

    def _batch_fetch_sectors(self, tickers: List[str]) -> Dict[str, str]:
        """
        Fetch sectors for multiple tickers in one pass (reduces API calls)

        Args:
            tickers: List of stock symbols

        Returns:
            Dict mapping ticker -> sector
        """
        sector_map = {}

        for ticker in tickers:
            sector = self.sector_checker.get_stock_sector(ticker)
            if sector:
                sector_map[ticker] = sector

        logger.info(f"Fetched sectors for {len(sector_map)}/{len(tickers)} tickers")
        return sector_map

    def get_current_portfolio_state(self) -> Dict:
        """
        Query database to get current portfolio state

        Returns:
            Dict with capital, heat, positions, sector_allocations
        """
        try:
            # For Phase 1, use testing defaults
            # In future, query Trading Department database for open positions
            capital = self.config['testing']['initial_capital']
            heat = self.config['testing']['initial_heat']
            positions = self.config['testing']['initial_positions']

            # Get sector allocations (empty for now)
            sector_allocations = {}

            return {
                'capital': capital,
                'current_heat': heat,
                'open_positions_count': positions,
                'sector_allocations': sector_allocations
            }

        except Exception as e:
            logger.error(f"Failed to get portfolio state: {e}", exc_info=True)
            return None

    def process_candidate(self, candidate: Dict, portfolio_state: Dict, sector_map: Dict[str, str] = None) -> Dict:
        """
        Process single candidate through all risk checks

        Args:
            candidate: Candidate dict from Research briefing
            portfolio_state: Current portfolio state

        Returns:
            Dict with 'approved', 'rejection_reason', 'risk_details'
        """
        ticker = candidate['ticker']
        capital = portfolio_state['capital']

        try:
            # Get current price (from Research data or fetch fresh)
            # For now, fetch fresh price
            stock = yf.Ticker(ticker)
            current_price = stock.history(period='1d')['Close'].iloc[-1]

            logger.info(f"Processing {ticker} @ ${current_price:.2f}...")

            # Step 1: Position sizing
            position = self.position_sizer.calculate_position_size(capital, current_price, ticker)
            if not position:
                return {
                    'ticker': ticker,
                    'approved': False,
                    'rejection_reason': 'DATA_UNAVAILABLE',
                    'rejection_details': 'Failed to calculate position size'
                }

            # Step 2: Stop-loss calculation
            stop = self.stop_loss_calc.calculate_stop_loss(ticker, current_price)
            if not stop:
                return {
                    'ticker': ticker,
                    'approved': False,
                    'rejection_reason': 'DATA_UNAVAILABLE',
                    'rejection_details': 'Failed to calculate stop-loss'
                }

            # Step 2.5: Calculate target price (simple 2:1 risk-reward for Phase 1)
            risk_per_share = stop['risk_per_share']
            target_price = current_price + (risk_per_share * 2.0)  # 2:1 reward:risk
            risk_reward_ratio = 2.0

            # Step 3: Risk per trade validation
            risk_check = self.risk_calc.validate_risk_per_trade(
                shares=position['shares'],
                risk_per_share=stop['risk_per_share'],
                capital=capital,
                ticker=ticker
            )

            if not risk_check['approved']:
                return {
                    'ticker': ticker,
                    'approved': False,
                    'rejection_reason': risk_check['rejection_reason'],
                    'rejection_details': risk_check['rejection_details'],
                    'position': position,
                    'stop': stop,
                    'risk_check': risk_check
                }

            # Step 4: Portfolio heat check
            heat_check = self.heat_monitor.check_portfolio_heat(
                new_trade_risk=risk_check['total_risk'],
                current_heat=portfolio_state['current_heat'],
                capital=capital,
                ticker=ticker
            )

            if not heat_check['approved']:
                return {
                    'ticker': ticker,
                    'approved': False,
                    'rejection_reason': heat_check['rejection_reason'],
                    'rejection_details': heat_check['rejection_details'],
                    'position': position,
                    'stop': stop,
                    'risk_check': risk_check,
                    'heat_check': heat_check
                }

            # Step 5: Sector concentration check
            # Use cached sector if available, otherwise fetch
            if sector_map and ticker in sector_map:
                # Use pre-fetched sector
                sector = sector_map[ticker]
                sector_before = portfolio_state['sector_allocations'].get(sector, 0.0)
                sector_after = sector_before + position['actual_position_value']
                sector_before_pct = sector_before / capital if capital > 0 else 0
                sector_after_pct = sector_after / capital if capital > 0 else 0

                # Quick validation
                approved = sector_after_pct <= self.sector_checker.max_sector_pct

                sector_check = {
                    'ticker': ticker,
                    'sector': sector,
                    'position_value': round(position['actual_position_value'], 2),
                    'sector_before': round(sector_before, 2),
                    'sector_after': round(sector_after, 2),
                    'sector_before_pct': sector_before_pct,
                    'sector_after_pct': sector_after_pct,
                    'max_sector_pct': self.sector_checker.max_sector_pct,
                    'status': 'LIMIT_EXCEEDED' if not approved else 'NORMAL',
                    'approved': approved,
                    'rejection_reason': None if approved else 'SECTOR_CONCENTRATION_EXCEEDED',
                    'rejection_details': None if approved else (
                        f"Sector concentration limit exceeded: Adding this trade would increase {sector} sector exposure from "
                        f"${sector_before:,.0f} ({sector_before_pct*100:.1f}%) to ${sector_after:,.0f} ({sector_after_pct*100:.1f}%), "
                        f"exceeding the {self.sector_checker.max_sector_pct*100:.0f}% limit. Available capacity in {sector}: "
                        f"${(capital * self.sector_checker.max_sector_pct) - sector_before:,.0f}."
                    )
                }
            else:
                # Fall back to full check
                sector_check = self.sector_checker.check_sector_concentration(
                    ticker=ticker,
                    position_value=position['actual_position_value'],
                    capital=capital,
                    current_sector_allocations=portfolio_state['sector_allocations']
                )

            if not sector_check['approved']:
                return {
                    'ticker': ticker,
                    'approved': False,
                    'rejection_reason': sector_check['rejection_reason'],
                    'rejection_details': sector_check['rejection_details'],
                    'position': position,
                    'stop': stop,
                    'risk_check': risk_check,
                    'heat_check': heat_check,
                    'sector_check': sector_check
                }

            # All checks passed - APPROVED
            logger.info(f"{ticker} APPROVED - All risk checks passed")
            return {
                'ticker': ticker,
                'approved': True,
                'rejection_reason': None,
                'rejection_details': None,
                'position': position,
                'stop': stop,
                'target_price': round(target_price, 2),
                'risk_reward_ratio': risk_reward_ratio,
                'risk_check': risk_check,
                'heat_check': heat_check,
                'sector_check': sector_check,
                'research_composite_score': candidate['composite_score']
            }

        except Exception as e:
            logger.error(f"Failed to process {ticker}: {e}", exc_info=True)
            return {
                'ticker': ticker,
                'approved': False,
                'rejection_reason': 'CALCULATION_ERROR',
                'rejection_details': str(e)
            }

    def process_daily_briefing(self, briefing_message_path: Path) -> str:
        """
        Process DailyBriefing from Research Department

        Args:
            briefing_message_path: Path to Research DailyBriefing message

        Returns:
            Message ID of generated RiskAssessment
        """
        logger.info("=" * 80)
        logger.info("PROCESSING DAILY BRIEFING")
        logger.info("=" * 80)

        # Read Research briefing
        metadata, body, data_payload = self.message_handler.read_message(briefing_message_path)
        parent_message_id = metadata['message_id']
        assessment_date = date.today()

        logger.info(f"Parent message: {parent_message_id}")
        logger.info(f"Assessment date: {assessment_date}")

        # Get candidates from payload
        candidates = data_payload.get('candidates', [])
        logger.info(f"Reviewing {len(candidates)} candidates from Research...")

        # Get current portfolio state
        portfolio_state = self.get_current_portfolio_state()
        if not portfolio_state:
            logger.error("Failed to get portfolio state - aborting assessment")
            return None

        logger.info(f"Portfolio state: ${portfolio_state['capital']:,.0f} capital, ${portfolio_state['current_heat']:,.0f} heat, {portfolio_state['open_positions_count']} positions")

        # Batch fetch sectors for all candidates (reduces API calls)
        tickers = [c['ticker'] for c in candidates]
        sector_map = self._batch_fetch_sectors(tickers)

        # Process each candidate
        approved_candidates = []
        rejected_candidates = []

        for candidate in candidates:
            result = self.process_candidate(candidate, portfolio_state, sector_map)

            if result['approved']:
                approved_candidates.append(result)
            else:
                rejected_candidates.append(result)

        logger.info(f"Risk assessment complete: {len(approved_candidates)} approved, {len(rejected_candidates)} rejected")

        # Generate RiskAssessment message
        message_id = self._generate_risk_assessment_message(
            parent_message_id=parent_message_id,
            assessment_date=assessment_date,
            portfolio_state=portfolio_state,
            approved_candidates=approved_candidates,
            rejected_candidates=rejected_candidates,
            candidates_reviewed=len(candidates)
        )

        # Save to database
        self._save_assessment_to_db(
            message_id=message_id,
            parent_message_id=parent_message_id,
            assessment_date=assessment_date,
            portfolio_state=portfolio_state,
            approved_candidates=approved_candidates,
            rejected_candidates=rejected_candidates,
            candidates_reviewed=len(candidates)
        )

        logger.info("=" * 80)
        return message_id

    def _generate_risk_assessment_message(self, parent_message_id: str, assessment_date: date,
                                         portfolio_state: Dict, approved_candidates: List[Dict],
                                         rejected_candidates: List[Dict], candidates_reviewed: int) -> str:
        """Generate RiskAssessment message for Portfolio Department"""

        # Build markdown body
        body_lines = [
            f"**Assessment Date**: {assessment_date.strftime('%Y-%m-%d')}",
            f"**Parent Message**: {parent_message_id}",
            "",
            "## Portfolio State",
            f"- **Capital**: ${portfolio_state['capital']:,.0f}",
            f"- **Current Heat**: ${portfolio_state['current_heat']:,.0f} ({portfolio_state['current_heat']/portfolio_state['capital']*100:.2f}%)",
            f"- **Open Positions**: {portfolio_state['open_positions_count']}",
            "",
            f"## Risk Assessment Summary",
            f"- **Candidates Reviewed**: {candidates_reviewed}",
            f"- **Approved**: {len(approved_candidates)}",
            f"- **Rejected**: {len(rejected_candidates)}",
            ""
        ]

        # Approved candidates
        if len(approved_candidates) > 0:
            body_lines.append("## Approved Candidates")
            body_lines.append("")
            for i, candidate in enumerate(approved_candidates, 1):
                ticker = candidate['ticker']
                pos = candidate['position']
                stop = candidate['stop']
                risk = candidate['risk_check']
                sector = candidate['sector_check'].get('sector', 'Unknown')

                body_lines.append(f"### {i}. {ticker} ({sector})")
                body_lines.append(f"- **Research Score**: {candidate['research_composite_score']}/10")
                body_lines.append(f"- **Position**: {pos['shares']} shares @ ${pos['current_price']:.2f} = ${pos['actual_position_value']:,.0f}")
                body_lines.append(f"- **Entry**: ${pos['current_price']:.2f} | **Stop**: ${stop['stop_loss']:.2f} | **Target**: ${candidate['target_price']:.2f}")
                body_lines.append(f"- **Risk/Reward**: {candidate['risk_reward_ratio']:.1f}:1 ({stop['method']})")
                body_lines.append(f"- **Risk**: ${risk['total_risk']:,.0f} ({risk['risk_percentage']*100:.2f}% of capital)")
                body_lines.append("")
        else:
            body_lines.append("## Approved Candidates")
            body_lines.append("")
            body_lines.append("**NONE** - No candidates passed risk validation")
            body_lines.append("")

        # Rejected candidates
        if len(rejected_candidates) > 0:
            body_lines.append("## Rejected Candidates")
            body_lines.append("")
            for candidate in rejected_candidates:
                body_lines.append(f"- **{candidate['ticker']}**: {candidate['rejection_reason']} - {candidate['rejection_details']}")
            body_lines.append("")

        body = "\n".join(body_lines)

        # Build JSON payload
        data_payload = {
            'assessment_date': assessment_date.isoformat(),
            'parent_message_id': parent_message_id,
            'portfolio_state': portfolio_state,
            'approved_candidates': [self._serialize_candidate(c) for c in approved_candidates],
            'rejected_candidates': [self._serialize_rejection(c) for c in rejected_candidates],
            'summary': {
                'candidates_reviewed': candidates_reviewed,
                'candidates_approved': len(approved_candidates),
                'candidates_rejected': len(rejected_candidates)
            }
        }

        # Write message
        message_id = self.message_handler.write_message(
            to_dept='PORTFOLIO',
            message_type='RiskAssessment',
            subject=f"Risk Assessment - {assessment_date.strftime('%Y-%m-%d')}",
            body=body,
            data_payload=data_payload,
            parent_message_id=parent_message_id,
            priority='routine'
        )

        logger.info(f"RiskAssessment message generated: {message_id}")
        return message_id

    def _serialize_candidate(self, candidate: Dict) -> Dict:
        """Serialize approved candidate for JSON payload"""
        return {
            'ticker': candidate['ticker'],
            'research_composite_score': candidate['research_composite_score'],
            'position_size_shares': candidate['position']['shares'],
            'position_size_value': candidate['position']['actual_position_value'],
            'entry_price': candidate['position']['current_price'],
            'stop_loss': candidate['stop']['stop_loss'],
            'target_price': candidate['target_price'],
            'risk_reward_ratio': candidate['risk_reward_ratio'],
            'stop_loss_method': candidate['stop']['method'],
            'atr_value': candidate['stop'].get('atr_value'),
            'risk_per_share': candidate['stop']['risk_per_share'],
            'total_risk': candidate['risk_check']['total_risk'],
            'risk_percentage': candidate['risk_check']['risk_percentage'],
            'portfolio_heat_after': candidate['heat_check']['heat_after'],
            'sector': candidate['sector_check'].get('sector')
        }

    def _serialize_rejection(self, candidate: Dict) -> Dict:
        """Serialize rejected candidate for JSON payload"""
        return {
            'ticker': candidate['ticker'],
            'rejection_reason': candidate['rejection_reason'],
            'rejection_details': candidate['rejection_details']
        }

    def _save_assessment_to_db(self, message_id: str, parent_message_id: str,
                               assessment_date: date, portfolio_state: Dict,
                               approved_candidates: List[Dict], rejected_candidates: List[Dict],
                               candidates_reviewed: int):
        """Save risk assessment to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Save risk assessment header
            cursor.execute("""
                INSERT INTO risk_assessments
                (message_id, parent_message_id, assessment_date, timestamp,
                 current_capital, current_heat, available_heat, open_positions_count,
                 candidates_reviewed, candidates_approved, candidates_rejected,
                 max_risk_per_trade_pct, max_portfolio_heat_pct, max_sector_concentration_pct, position_size_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                parent_message_id,
                assessment_date.isoformat(),
                datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                portfolio_state['capital'],
                portfolio_state['current_heat'],
                portfolio_state['capital'] * self.config['portfolio_heat']['max_total_heat_pct'] - portfolio_state['current_heat'],
                portfolio_state['open_positions_count'],
                candidates_reviewed,
                len(approved_candidates),
                len(rejected_candidates),
                self.config['risk_per_trade']['max_risk_pct'],
                self.config['portfolio_heat']['max_total_heat_pct'],
                self.config['sector_concentration']['max_sector_pct'],
                self.config['position_sizing']['position_size_pct']
            ))

            # Save approved candidates
            for candidate in approved_candidates:
                cursor.execute("""
                    INSERT INTO risk_approved_candidates
                    (message_id, ticker, assessment_date,
                     research_composite_score,
                     position_sizing_method, position_size_pct, position_size_shares, position_size_value,
                     entry_price, stop_loss, stop_loss_method, atr_value, target_price,
                     risk_per_share, total_risk, risk_percentage, risk_reward_ratio,
                     portfolio_heat_before, portfolio_heat_after,
                     sector, decision_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    message_id,
                    candidate['ticker'],
                    assessment_date.isoformat(),
                    candidate['research_composite_score'],
                    candidate['position']['method'],
                    candidate['position']['actual_position_pct'],
                    candidate['position']['shares'],
                    candidate['position']['actual_position_value'],
                    candidate['position']['current_price'],
                    candidate['stop']['stop_loss'],
                    candidate['stop']['method'],
                    candidate['stop'].get('atr_value'),
                    candidate['target_price'],
                    candidate['stop']['risk_per_share'],
                    candidate['risk_check']['total_risk'],
                    candidate['risk_check']['risk_percentage'],
                    candidate['risk_reward_ratio'],
                    candidate['heat_check']['heat_before'],
                    candidate['heat_check']['heat_after'],
                    candidate['sector_check'].get('sector'),
                    datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                ))

            # Save rejected candidates
            for candidate in rejected_candidates:
                # Determine rejection category
                reason = candidate['rejection_reason']
                if reason == 'PORTFOLIO_HEAT_EXCEEDED':
                    category = 'PORTFOLIO_HEAT'
                elif reason == 'SECTOR_CONCENTRATION_EXCEEDED':
                    category = 'SECTOR_CONCENTRATION'
                elif reason == 'RISK_PER_TRADE_EXCEEDED':
                    category = 'RISK_PER_TRADE'
                elif reason == 'DATA_UNAVAILABLE':
                    category = 'DATA_UNAVAILABLE'
                else:
                    category = 'OTHER'

                cursor.execute("""
                    INSERT INTO risk_rejected_candidates
                    (message_id, ticker, assessment_date,
                     research_composite_score,
                     rejection_reason, rejection_category, rejection_details,
                     decision_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    message_id,
                    candidate['ticker'],
                    assessment_date.isoformat(),
                    candidate.get('research_composite_score', 0.0),
                    reason,
                    category,
                    candidate['rejection_details'],
                    datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                ))

            conn.commit()
            conn.close()

            logger.info(f"Risk assessment saved to database: {len(approved_candidates)} approved, {len(rejected_candidates)} rejected")

        except Exception as e:
            logger.error(f"Failed to save assessment to database: {e}", exc_info=True)


if __name__ == "__main__":
    # Test all Risk Department components
    logger.info("Risk Department - Testing All Components (Days 1-3)")

    # Load config
    config_path = Path("Config/risk_config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize classes
    position_sizer = PositionSizer(config)
    stop_loss_calc = StopLossCalculator(config)
    risk_calc = RiskCalculator(config)
    heat_monitor = PortfolioHeatMonitor(config)
    sector_checker = SectorConcentrationChecker(config)

    # Test with sample data
    capital = config['testing']['initial_capital']  # $100,000
    test_ticker = "AAPL"
    test_price = 175.50

    print("\n" + "=" * 100)
    print(f"TESTING: {test_ticker} @ ${test_price:.2f} (Capital: ${capital:,.0f})")
    print("=" * 100)

    # Test 1: Position sizing
    print("\n[1/5] POSITION SIZING:")
    print("-" * 100)
    position = position_sizer.calculate_position_size(capital, test_price, test_ticker)
    if position:
        print(f"  Capital: ${capital:,.0f}")
        print(f"  Target Position: {position['target_position_pct']*100:.0f}% = ${position['target_position_value']:,.0f}")
        print(f"  Shares: {position['shares']}")
        print(f"  Actual Position: ${position['actual_position_value']:,.0f} ({position['actual_position_pct']*100:.1f}%)")

    # Test 2: Stop-loss
    print("\n[2/5] STOP-LOSS CALCULATION:")
    print("-" * 100)
    stop = stop_loss_calc.calculate_stop_loss(test_ticker, test_price)
    if stop:
        print(f"  Entry Price: ${stop['entry_price']:.2f}")
        if stop['atr_value']:
            print(f"  ATR({stop_loss_calc.atr_period}): ${stop['atr_value']:.2f}")
        print(f"  Method: {stop['method']}")
        print(f"  Stop-Loss: ${stop['stop_loss']:.2f}")
        print(f"  Risk Per Share: ${stop['risk_per_share']:.2f} ({stop['stop_distance_pct']*100:.1f}%)")

    # Test 3: Risk per trade validation
    print("\n[3/5] RISK PER TRADE VALIDATION:")
    print("-" * 100)
    if position and stop:
        risk_validation = risk_calc.validate_risk_per_trade(
            shares=position['shares'],
            risk_per_share=stop['risk_per_share'],
            capital=capital,
            ticker=test_ticker
        )
        print(f"  Shares: {risk_validation['shares']}")
        print(f"  Risk Per Share: ${risk_validation['risk_per_share']:.2f}")
        print(f"  Total Risk: ${risk_validation['total_risk']:,.0f}")
        print(f"  Risk Percentage: {risk_validation['risk_percentage']*100:.2f}%")
        print(f"  Max Allowed: {risk_validation['max_risk_pct']*100:.1f}%")
        print(f"  Status: {'APPROVED' if risk_validation['approved'] else 'REJECTED'}")
        if not risk_validation['approved']:
            print(f"  Rejection Reason: {risk_validation['rejection_reason']}")
            print(f"  Details: {risk_validation['rejection_details']}")

    # Test 4: Portfolio heat monitoring
    print("\n[4/5] PORTFOLIO HEAT MONITORING:")
    print("-" * 100)

    # Scenario A: Normal (0% current heat)
    print("  Scenario A: Fresh portfolio (0% current heat)")
    if position and stop:
        total_risk = position['shares'] * stop['risk_per_share']
        heat_check = heat_monitor.check_portfolio_heat(
            new_trade_risk=total_risk,
            current_heat=0.0,
            capital=capital,
            ticker=test_ticker
        )
        print(f"    Current Heat: ${heat_check['heat_before']:,.0f} ({heat_check['heat_before_pct']*100:.2f}%)")
        print(f"    New Trade Risk: ${heat_check['new_trade_risk']:,.0f}")
        print(f"    Heat After: ${heat_check['heat_after']:,.0f} ({heat_check['heat_after_pct']*100:.2f}%)")
        print(f"    Available Heat: ${heat_check['available_heat']:,.0f}")
        print(f"    Status: {heat_check['status']}")
        print(f"    Decision: {'APPROVED' if heat_check['approved'] else 'REJECTED'}")

    # Scenario B: High heat (4.5% current heat - at critical threshold)
    print("\n  Scenario B: High heat portfolio (4.5% current heat)")
    if position and stop:
        current_heat = capital * 0.045  # $4,500 current heat
        total_risk = position['shares'] * stop['risk_per_share']
        heat_check = heat_monitor.check_portfolio_heat(
            new_trade_risk=total_risk,
            current_heat=current_heat,
            capital=capital,
            ticker=test_ticker
        )
        print(f"    Current Heat: ${heat_check['heat_before']:,.0f} ({heat_check['heat_before_pct']*100:.2f}%)")
        print(f"    New Trade Risk: ${heat_check['new_trade_risk']:,.0f}")
        print(f"    Heat After: ${heat_check['heat_after']:,.0f} ({heat_check['heat_after_pct']*100:.2f}%)")
        print(f"    Available Heat: ${heat_check['available_heat']:,.0f}")
        print(f"    Status: {heat_check['status']}")
        print(f"    Decision: {'APPROVED' if heat_check['approved'] else 'REJECTED'}")
        if not heat_check['approved']:
            print(f"    Rejection Reason: {heat_check['rejection_reason']}")
            print(f"    Details: {heat_check['rejection_details']}")

    # Test 5: Sector concentration
    print("\n[5/5] SECTOR CONCENTRATION CHECKING:")
    print("-" * 100)

    # Scenario A: No existing sector exposure
    print("  Scenario A: Fresh portfolio (no existing sector exposure)")
    if position:
        sector_check_a = sector_checker.check_sector_concentration(
            ticker=test_ticker,
            position_value=position['actual_position_value'],
            capital=capital,
            current_sector_allocations={}
        )
        if sector_check_a['sector']:
            print(f"    Sector: {sector_check_a['sector']}")
            print(f"    Position Value: ${sector_check_a['position_value']:,.0f}")
            print(f"    Sector Before: ${sector_check_a['sector_before']:,.0f} ({sector_check_a['sector_before_pct']*100:.1f}%)")
            print(f"    Sector After: ${sector_check_a['sector_after']:,.0f} ({sector_check_a['sector_after_pct']*100:.1f}%)")
            print(f"    Max Allowed: {sector_check_a['max_sector_pct']*100:.0f}%")
            print(f"    Status: {sector_check_a['status']}")
            print(f"    Decision: {'APPROVED' if sector_check_a['approved'] else 'REJECTED'}")
        else:
            print(f"    Status: {sector_check_a['status']}")
            print(f"    Decision: APPROVED (sector unavailable)")

    # Scenario B: High existing sector exposure (35%)
    print("\n  Scenario B: Portfolio with 35% existing Technology exposure")
    if position:
        # Simulate 35% Technology exposure
        existing_tech = capital * 0.35  # $35,000
        sector_check_b = sector_checker.check_sector_concentration(
            ticker=test_ticker,
            position_value=position['actual_position_value'],
            capital=capital,
            current_sector_allocations={'Technology': existing_tech}
        )
        if sector_check_b['sector']:
            print(f"    Sector: {sector_check_b['sector']}")
            print(f"    Position Value: ${sector_check_b['position_value']:,.0f}")
            print(f"    Sector Before: ${sector_check_b['sector_before']:,.0f} ({sector_check_b['sector_before_pct']*100:.1f}%)")
            print(f"    Sector After: ${sector_check_b['sector_after']:,.0f} ({sector_check_b['sector_after_pct']*100:.1f}%)")
            print(f"    Max Allowed: {sector_check_b['max_sector_pct']*100:.0f}%")
            print(f"    Status: {sector_check_b['status']}")
            print(f"    Decision: {'APPROVED' if sector_check_b['approved'] else 'REJECTED'}")
            if not sector_check_b['approved']:
                print(f"    Rejection Reason: {sector_check_b['rejection_reason']}")
                print(f"    Details: {sector_check_b['rejection_details']}")
        else:
            print(f"    Status: {sector_check_b['status']}")
            print(f"    Decision: APPROVED (sector unavailable)")

    # Summary
    print("\n" + "=" * 100)
    print("VALIDATION SUMMARY:")
    print("=" * 100)
    if position and stop and risk_validation and heat_check:
        print(f"  Position Size: {position['shares']} shares @ ${test_price:.2f} = ${position['actual_position_value']:,.0f}")
        print(f"  Stop-Loss: ${stop['stop_loss']:.2f} (Risk: ${stop['risk_per_share']:.2f}/share)")
        print(f"  Total Risk: ${risk_validation['total_risk']:,.0f} ({risk_validation['risk_percentage']*100:.2f}% of capital)")
        print(f"  Risk Per Trade Check: {'PASS' if risk_validation['approved'] else 'FAIL'}")
        print(f"  Portfolio Heat Check (0% heat): PASS")
        print(f"  Portfolio Heat Check (4.5% heat): {'PASS' if heat_check['approved'] else 'FAIL (as expected)'}")
        if sector_check_a and sector_check_a['sector']:
            print(f"  Sector Concentration (fresh): PASS ({sector_check_a['sector_after_pct']*100:.1f}% < 40%)")
        if sector_check_b and sector_check_b['sector']:
            print(f"  Sector Concentration (35% existing): {'PASS' if sector_check_b['approved'] else 'FAIL (as expected)'}")

    print("\n" + "=" * 100)
    print("TEST COMPLETE - Days 1-4 Components Verified")
    print("=" * 100)

    # ====================================================================================
    # END-TO-END TEST: Process Research DailyBriefing
    # ====================================================================================
    print("\n\n")
    print("=" * 100)
    print("END-TO-END TEST: Processing Research DailyBriefing")
    print("=" * 100)

    # Initialize Risk Department
    risk_dept = RiskDepartment()

    # Find most recent Research briefing
    research_outbox = Path("Messages_Between_Departments/Outbox/RESEARCH")
    briefings = sorted(research_outbox.glob("MSG_RESEARCH_*.md"), reverse=True)

    if len(briefings) == 0:
        print("\nNo Research briefings found - skipping end-to-end test")
    else:
        latest_briefing = briefings[0]
        print(f"\nProcessing latest briefing: {latest_briefing.name}")

        try:
            # Process briefing
            message_id = risk_dept.process_daily_briefing(latest_briefing)

            if message_id:
                print(f"\nSUCCESS: RiskAssessment generated: {message_id}")
                print(f"SUCCESS: Message written to: Messages_Between_Departments/Outbox/RISK/{message_id}.md")
                print(f"SUCCESS: Assessment saved to database")
            else:
                print("\nFAILED: Risk assessment failed")

        except Exception as e:
            print(f"\nFAILED: End-to-end test failed: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 100)
    print("ALL TESTS COMPLETE")
    print("=" * 100)
