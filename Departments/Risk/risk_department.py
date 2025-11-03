"""
Risk Department v2.1 - Swing Trading Risk Assessment

Phase 1.5 Redesign:
- RECOMMEND, don't REJECT
- Calculate risk metrics (stop-loss, ATR, volatility, etc.)
- Add risk_score (0-100, HIGHER = BETTER SWING TRADE)
- Add risk_warnings list (concerns, not blockers)
- Pass ALL candidates downstream (no filtering)

Swing Trading Philosophy:
- risk_score reflects SWING TRADE SUITABILITY (not traditional safety)
- High volatility (20-40%) = GOOD (motion of the ocean!)
- Wide stops (5-10%) = GOOD (room to run!)
- Low volatility (<15%) = BAD (stagnation risk!)
- See SENTINEL_RISK_PHILOSOPHY.md for complete philosophy

Key Changes from v1:
- Removed approval/rejection authority
- Changed from gatekeeper to advisor
- All candidates pass through with risk assessment
- v2.1: Fixed scoring to align with swing trading (higher = better for SC)
"""

import logging
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class RiskDepartment:
    """
    Risk Department - Advisory Swing Trading Risk Assessment

    Responsibilities:
    1. Calculate risk metrics for each candidate
    2. Assign risk_score (0-100, HIGHER = BETTER SWING TRADE)
    3. Generate risk_warnings list for each candidate
    4. Pass ALL candidates to downstream departments
    5. NO approval/rejection authority

    Philosophy:
    - risk_score = swing trade suitability (NOT traditional safety)
    - High volatility 20-40% = GOOD (motion!)
    - Wide stops 5-10% = GOOD (room to run!)
    - Low volatility <15% = BAD (stagnation risk!)
    - See SENTINEL_RISK_PHILOSOPHY.md for details
    """

    def __init__(self, max_risk_per_trade_pct: float = 1.0, max_portfolio_heat_pct: float = 5.0):
        """
        Initialize Risk Department

        Args:
            max_risk_per_trade_pct: Maximum risk per trade (% of capital)
            max_portfolio_heat_pct: Maximum total portfolio heat (% of capital)
        """
        self.max_risk_per_trade_pct = max_risk_per_trade_pct
        self.max_portfolio_heat_pct = max_portfolio_heat_pct
        self.atr_period = 14
        self.atr_multiplier = 2.0

        logger.info(f"Risk Department v2.0 initialized (advisory role)")
        logger.info(f"  - Max risk per trade: {max_risk_per_trade_pct}%")
        logger.info(f"  - Max portfolio heat: {max_portfolio_heat_pct}%")

    def assess_candidates(self, candidates: List[Dict], available_capital: float) -> List[Dict]:
        """
        Assess risk for all candidates (NO rejections)

        Args:
            candidates: List of stock candidates from Research
            available_capital: Available capital for trading

        Returns:
            Same list with added risk metrics, scores, and warnings
        """
        logger.info("=" * 80)
        logger.info("RISK ASSESSMENT - ADVISORY MODE")
        logger.info("=" * 80)
        logger.info(f"Assessing {len(candidates)} candidates...")
        logger.info(f"Available capital: ${available_capital:,.2f}")

        assessed = []
        for candidate in candidates:
            ticker = candidate['ticker']
            logger.info(f"Processing {ticker}...")

            # Calculate risk metrics
            risk_metrics = self._calculate_risk_metrics(ticker, candidate, available_capital)

            # Calculate risk score (0-100, HIGHER = BETTER SWING TRADE)
            risk_score = self._calculate_risk_score(risk_metrics)

            # Generate warnings
            warnings = self._generate_warnings(ticker, risk_metrics, available_capital)

            # Add to candidate
            candidate['risk_score'] = risk_score
            candidate['risk_warnings'] = warnings
            candidate['risk_metrics'] = risk_metrics

            # Log summary
            if warnings:
                logger.warning(f"{ticker}: Risk score {risk_score:.1f}/100 - {len(warnings)} warnings")
                for warning in warnings:
                    logger.warning(f"  - {warning}")
            else:
                logger.info(f"{ticker}: Risk score {risk_score:.1f}/100 - No warnings")

            assessed.append(candidate)

        logger.info(f"Risk assessment complete: {len(assessed)} candidates assessed")
        logger.info("All candidates passed through (advisory role - no rejections)")
        logger.info("=" * 80)

        return assessed

    def _calculate_risk_metrics(self, ticker: str, candidate: Dict, available_capital: float) -> Dict:
        """
        Calculate comprehensive risk metrics for candidate

        Returns:
            {
                'entry_price': float,
                'stop_loss': float,
                'target_price': float,
                'risk_per_share': float,
                'reward_per_share': float,
                'risk_reward_ratio': float,
                'position_size_shares': int,
                'position_size_value': float,
                'total_risk_dollars': float,
                'total_risk_pct': float,
                'atr': float,
                'volatility_pct': float
            }
        """
        # Get current price
        entry_price = candidate.get('current_price', 0)
        if entry_price == 0:
            entry_price = self._fetch_current_price(ticker)

        # Calculate ATR (for stop-loss)
        atr = self._calculate_atr(ticker)

        # Stop-loss (ATR-based)
        stop_loss = entry_price - (atr * self.atr_multiplier)

        # Target price (2:1 risk/reward minimum)
        risk_per_share = entry_price - stop_loss
        reward_per_share = risk_per_share * 2.0  # 2:1 minimum
        target_price = entry_price + reward_per_share

        # Position sizing (10% of capital - deterministic for now)
        position_size_value = available_capital * 0.10
        position_size_shares = int(position_size_value / entry_price) if entry_price > 0 else 0

        # Total risk
        total_risk_dollars = position_size_shares * risk_per_share
        total_risk_pct = (total_risk_dollars / available_capital * 100) if available_capital > 0 else 0

        # Volatility (annualized std dev)
        volatility_pct = self._calculate_volatility(ticker)

        return {
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'target_price': target_price,
            'risk_per_share': risk_per_share,
            'reward_per_share': reward_per_share,
            'risk_reward_ratio': reward_per_share / risk_per_share if risk_per_share > 0 else 0,
            'position_size_shares': position_size_shares,
            'position_size_value': position_size_value,
            'total_risk_dollars': total_risk_dollars,
            'total_risk_pct': total_risk_pct,
            'atr': atr,
            'volatility_pct': volatility_pct
        }

    def _calculate_risk_score(self, metrics: Dict) -> float:
        """
        Calculate risk score for SWING TRADING (0-100, HIGHER = BETTER)

        Sentinel Corporation Philosophy:
        - This is NOT traditional "safety" scoring
        - High volatility (20-40%) = GOOD (motion of the ocean!)
        - Wide stops (5-10%) = GOOD (room to run!)
        - Low volatility (<15%) = BAD (stagnation risk!)

        Components (25 points each):
        1. Volatility: Want 20-40% (sweet spot for swing trading)
        2. R:R Ratio: Want >=2:1 (asymmetric returns)
        3. Stop Distance: Want 5-10% (room to breathe)
        4. Position Risk: Want <=1.5% (managed exposure)

        See SENTINEL_RISK_PHILOSOPHY.md for complete philosophy
        """
        score = 0.0  # Start at zero, build up

        # 1. VOLATILITY SCORE (25 points) - Want 20-40% for swing trading
        volatility = metrics['volatility_pct']
        if 25 <= volatility <= 35:
            score += 25  # PERFECT sweet spot
        elif 20 <= volatility < 25 or 35 < volatility <= 40:
            score += 20  # EXCELLENT
        elif 15 <= volatility < 20 or 40 < volatility <= 50:
            score += 10  # GOOD
        elif 10 <= volatility < 15 or 50 < volatility <= 60:
            score += 5   # MARGINAL
        else:
            score += 0   # Too boring (<10%) or too volatile (>60%)

        # 2. RISK/REWARD RATIO SCORE (25 points) - Want >=2:1
        rr_ratio = metrics['risk_reward_ratio']
        if rr_ratio >= 3.0:
            score += 25  # EXCELLENT asymmetric setup
        elif rr_ratio >= 2.5:
            score += 20  # VERY GOOD
        elif rr_ratio >= 2.0:
            score += 15  # GOOD minimum
        elif rr_ratio >= 1.5:
            score += 10  # MARGINAL
        else:
            score += 0   # Not worth the risk

        # 3. STOP DISTANCE SCORE (25 points) - Want 5-10% from entry
        entry = metrics['entry_price']
        stop = metrics['stop_loss']
        stop_distance_pct = ((entry - stop) / entry * 100) if entry > 0 else 0

        if 6 <= stop_distance_pct <= 9:
            score += 25  # PERFECT room to run
        elif 5 <= stop_distance_pct < 6 or 9 < stop_distance_pct <= 10:
            score += 20  # EXCELLENT
        elif 4 <= stop_distance_pct < 5 or 10 < stop_distance_pct <= 12:
            score += 15  # GOOD
        elif 3 <= stop_distance_pct < 4 or 12 < stop_distance_pct <= 15:
            score += 10  # MARGINAL
        elif stop_distance_pct < 3:
            score += 5   # Too tight - death by 1000 cuts
        else:  # >15%
            score += 5   # Too wide - over-exposed

        # 4. POSITION RISK SCORE (25 points) - Want <=1.5% of capital
        total_risk_pct = metrics['total_risk_pct']
        if total_risk_pct <= 0.75:
            score += 25  # CONSERVATIVE, safe
        elif total_risk_pct <= 1.0:
            score += 20  # GOOD risk management
        elif total_risk_pct <= 1.5:
            score += 15  # ACCEPTABLE target
        elif total_risk_pct <= 2.0:
            score += 10  # ELEVATED, aggressive
        else:
            score += 5   # EXCESSIVE, over-leveraged

        # Clamp to 0-100
        return max(0.0, min(100.0, score))

    def _generate_warnings(self, ticker: str, metrics: Dict, available_capital: float) -> List[str]:
        """
        Generate risk warnings for SWING TRADING (concerns, not rejections)

        Three warning categories:
        1. "Too Boring" - Low volatility, tight stops, stagnation risk
        2. "Excessive Risk" - Over-leveraged, too volatile
        3. "Poor Setup" - Bad R:R ratio, invalid data

        Returns:
            List of warning strings
        """
        warnings = []

        # CATEGORY 1: "Too Boring for Swing Trading"
        if metrics['volatility_pct'] < 15:
            warnings.append(
                f"LOW VOLATILITY ({metrics['volatility_pct']:.1f}%) - "
                f"Limited profit potential for swing trading (stagnation risk)"
            )

        stop_distance_pct = ((metrics['entry_price'] - metrics['stop_loss']) / metrics['entry_price'] * 100)
        if stop_distance_pct < 3:
            warnings.append(
                f"TIGHT STOP ({stop_distance_pct:.1f}%) - "
                f"Insufficient room to breathe (death by 1000 cuts risk)"
            )

        # CATEGORY 2: "Excessive Risk"
        if metrics['total_risk_pct'] > 2.0:
            warnings.append(
                f"EXCESSIVE POSITION RISK ({metrics['total_risk_pct']:.2f}%) - "
                f"Over-leveraged (${metrics['total_risk_dollars']:.2f} at risk)"
            )

        if metrics['volatility_pct'] > 60:
            warnings.append(
                f"EXTREME VOLATILITY ({metrics['volatility_pct']:.1f}%) - "
                f"Too chaotic for managed swing trading"
            )

        if stop_distance_pct > 15:
            warnings.append(
                f"VERY WIDE STOP ({stop_distance_pct:.1f}%) - "
                f"Over-exposed on single position"
            )

        # CATEGORY 3: "Poor Setup"
        if metrics['risk_reward_ratio'] < 1.5:
            warnings.append(
                f"POOR RISK/REWARD ({metrics['risk_reward_ratio']:.2f}:1) - "
                f"Not worth taking this trade"
            )

        # Data validity
        if metrics['entry_price'] <= 0:
            warnings.append("INVALID DATA - Could not fetch current price")

        return warnings

    def _calculate_atr(self, ticker: str, period: int = 14) -> float:
        """Calculate Average True Range"""
        try:
            data = yf.download(ticker, period='60d', progress=False)
            if data.empty:
                return 0.0

            high = data['High']
            low = data['Low']
            close = data['Close'].shift(1)

            tr1 = high - low
            tr2 = abs(high - close)
            tr3 = abs(low - close)

            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean().iloc[-1]

            return float(atr)

        except Exception as e:
            logger.debug(f"ATR calculation failed for {ticker}: {e}")
            return 0.0

    def _calculate_volatility(self, ticker: str) -> float:
        """Calculate annualized volatility (%)"""
        try:
            data = yf.download(ticker, period='60d', progress=False)
            if data.empty:
                return 0.0

            returns = data['Close'].pct_change().dropna()
            daily_vol = returns.std()
            annual_vol = daily_vol * (252 ** 0.5) * 100  # Annualized %

            return float(annual_vol)

        except Exception as e:
            logger.debug(f"Volatility calculation failed for {ticker}: {e}")
            return 0.0

    def _fetch_current_price(self, ticker: str) -> float:
        """Fetch current price for ticker"""
        try:
            data = yf.download(ticker, period='1d', progress=False)
            if not data.empty:
                return float(data['Close'].iloc[-1])
        except:
            pass
        return 0.0
