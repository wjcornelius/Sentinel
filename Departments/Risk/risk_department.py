"""
Risk Department v2.0 - Advisory Role Only (No Rejections)

Phase 1 Redesign:
- RECOMMEND, don't REJECT
- Calculate risk metrics (stop-loss, ATR, volatility, etc.)
- Add risk_score (0-100) for each candidate
- Add risk_warnings list (concerns, not blockers)
- Pass ALL candidates downstream (no filtering)

Key Changes from v1:
- Removed approval/rejection authority
- Changed from gatekeeper to advisor
- All candidates pass through with risk assessment
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
    Risk Department - Advisory Risk Assessment

    Responsibilities:
    1. Calculate risk metrics for each candidate
    2. Assign risk_score (0-100, higher = safer)
    3. Generate risk_warnings list for each candidate
    4. Pass ALL candidates to downstream departments
    5. NO approval/rejection authority
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

            # Calculate risk score (0-100, higher = safer)
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
        Calculate risk score (0-100, higher = safer)

        Based on:
        - Risk/reward ratio (higher = better)
        - Total risk % (lower = better)
        - Volatility (lower = better)
        - ATR relative to price (lower = better)
        """
        score = 50.0  # Start neutral

        # Risk/reward component (0-25 points)
        rr_ratio = metrics['risk_reward_ratio']
        if rr_ratio >= 3.0:
            score += 25
        elif rr_ratio >= 2.0:
            score += 15
        elif rr_ratio >= 1.5:
            score += 5
        else:
            score -= 10  # Poor risk/reward

        # Total risk component (0-25 points)
        total_risk_pct = metrics['total_risk_pct']
        if total_risk_pct <= 0.5:
            score += 25
        elif total_risk_pct <= 1.0:
            score += 15
        elif total_risk_pct <= 2.0:
            score += 5
        else:
            score -= 10  # High risk

        # Volatility component (0-25 points)
        volatility = metrics['volatility_pct']
        if volatility <= 20:
            score += 25
        elif volatility <= 40:
            score += 15
        elif volatility <= 60:
            score += 5
        else:
            score -= 10  # Very volatile

        # Stop-loss distance component (0-25 points)
        entry = metrics['entry_price']
        stop = metrics['stop_loss']
        stop_distance_pct = ((entry - stop) / entry * 100) if entry > 0 else 0

        if stop_distance_pct <= 3:
            score += 25
        elif stop_distance_pct <= 5:
            score += 15
        elif stop_distance_pct <= 10:
            score += 5
        else:
            score -= 10  # Wide stop

        # Clamp to 0-100
        return max(0.0, min(100.0, score))

    def _generate_warnings(self, ticker: str, metrics: Dict, available_capital: float) -> List[str]:
        """
        Generate risk warnings (concerns, not rejections)

        Returns:
            List of warning strings
        """
        warnings = []

        # Check risk per trade
        if metrics['total_risk_pct'] > self.max_risk_per_trade_pct:
            warnings.append(
                f"Risk {metrics['total_risk_pct']:.2f}% exceeds {self.max_risk_per_trade_pct}% limit "
                f"(${metrics['total_risk_dollars']:.2f} at risk)"
            )

        # Check volatility
        if metrics['volatility_pct'] > 60:
            warnings.append(f"High volatility: {metrics['volatility_pct']:.1f}% annualized")

        # Check risk/reward ratio
        if metrics['risk_reward_ratio'] < 1.5:
            warnings.append(f"Poor risk/reward ratio: {metrics['risk_reward_ratio']:.2f}:1")

        # Check stop-loss distance
        stop_distance_pct = ((metrics['entry_price'] - metrics['stop_loss']) / metrics['entry_price'] * 100)
        if stop_distance_pct > 10:
            warnings.append(f"Wide stop-loss: {stop_distance_pct:.1f}% from entry")

        # Check price validity
        if metrics['entry_price'] <= 0:
            warnings.append("Invalid entry price (could not fetch current price)")

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
