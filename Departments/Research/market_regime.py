"""
Market Regime Analyzer - Assesses current market conditions
Provides advisory regime classification (BULLISH/NEUTRAL/BEARISH) based on:
- SPY (S&P 500) price trend
- VIX (Volatility Index) level
"""

import yfinance as yf
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import uuid

logger = logging.getLogger(__name__)


class MarketRegimeAnalyzer:
    """Analyzes market conditions and classifies regime"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.db_path = project_root / "sentinel.db"
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Create market_regime_assessments table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_regime_assessments (
                assessment_id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                spy_price REAL,
                spy_change_pct REAL,
                vix_level REAL,
                vix_change_pct REAL,
                regime TEXT NOT NULL,
                confidence TEXT,
                recommendation TEXT,
                reasoning TEXT,
                user_decision TEXT,
                trades_executed INTEGER,
                portfolio_change_pct REAL,
                spy_eod_change_pct REAL,
                notes TEXT
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Market regime assessments table verified")

    def get_latest_assessment(self, max_age_hours=3):
        """
        Get most recent regime assessment if it's fresh enough

        Args:
            max_age_hours: Maximum age in hours before assessment is stale

        Returns:
            dict with assessment data or None if no valid assessment
        """
        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            SELECT assessment_id, date, timestamp, spy_price, spy_change_pct,
                   vix_level, vix_change_pct, regime, confidence, recommendation, reasoning
            FROM market_regime_assessments
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (cutoff_str,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'assessment_id': row[0],
                'date': row[1],
                'timestamp': row[2],
                'spy_price': row[3],
                'spy_change_pct': row[4],
                'vix_level': row[5],
                'vix_change_pct': row[6],
                'regime': row[7],
                'confidence': row[8],
                'recommendation': row[9],
                'reasoning': row[10]
            }
        return None

    def analyze_regime(self):
        """
        Analyze current market regime

        Returns:
            dict with regime assessment and reasoning
        """
        logger.info("Analyzing market regime...")

        try:
            # Fetch SPY data (S&P 500)
            spy = yf.Ticker("SPY")
            spy_hist = spy.history(period="5d")

            if len(spy_hist) < 2:
                raise ValueError("Insufficient SPY data")

            spy_current = spy_hist['Close'].iloc[-1]
            spy_previous = spy_hist['Close'].iloc[-2]
            spy_change_pct = ((spy_current - spy_previous) / spy_previous) * 100

            # Fetch VIX data (Volatility Index)
            vix = yf.Ticker("^VIX")
            vix_hist = vix.history(period="5d")

            if len(vix_hist) < 2:
                raise ValueError("Insufficient VIX data")

            vix_current = vix_hist['Close'].iloc[-1]
            vix_previous = vix_hist['Close'].iloc[-2]
            vix_change_pct = ((vix_current - vix_previous) / vix_previous) * 100

            logger.info(f"SPY: ${spy_current:.2f} ({spy_change_pct:+.2f}%), VIX: {vix_current:.2f} ({vix_change_pct:+.2f}%)")

            # Determine regime
            regime, confidence, recommendation, reasoning = self._classify_regime(
                spy_change_pct, vix_current, vix_change_pct
            )

            # Store assessment
            assessment_id = f"REGIME_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

            conn = sqlite3.connect(self.db_path, timeout=30)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO market_regime_assessments (
                    assessment_id, date, timestamp, spy_price, spy_change_pct,
                    vix_level, vix_change_pct, regime, confidence, recommendation, reasoning
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment_id,
                datetime.now().strftime('%Y-%m-%d'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                float(spy_current),
                float(spy_change_pct),
                float(vix_current),
                float(vix_change_pct),
                regime,
                confidence,
                recommendation,
                reasoning
            ))

            conn.commit()
            conn.close()

            logger.info(f"Market regime assessment stored: {assessment_id}")

            return {
                'status': 'SUCCESS',
                'assessment_id': assessment_id,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'spy_price': float(spy_current),
                'spy_change_pct': float(spy_change_pct),
                'vix_level': float(vix_current),
                'vix_change_pct': float(vix_change_pct),
                'regime': regime,
                'confidence': confidence,
                'recommendation': recommendation,
                'reasoning': reasoning
            }

        except Exception as e:
            logger.error(f"Failed to analyze market regime: {e}", exc_info=True)
            return {
                'status': 'ERROR',
                'message': f"Failed to analyze market regime: {e}"
            }

    def _classify_regime(self, spy_change_pct, vix_current, vix_change_pct):
        """
        Classify market regime based on indicators

        Returns:
            tuple: (regime, confidence, recommendation, reasoning)
        """
        reasons = []
        bullish_signals = 0
        bearish_signals = 0

        # Analyze SPY trend
        if spy_change_pct > 0.5:
            bullish_signals += 2
            reasons.append(f"Market trending up ({spy_change_pct:+.2f}% today)")
        elif spy_change_pct > 0:
            bullish_signals += 1
            reasons.append(f"Market slightly positive ({spy_change_pct:+.2f}% today)")
        elif spy_change_pct > -0.5:
            bearish_signals += 1
            reasons.append(f"Market slightly negative ({spy_change_pct:.2f}% today)")
        else:
            bearish_signals += 2
            reasons.append(f"Market declining ({spy_change_pct:.2f}% today)")

        # Analyze VIX level
        if vix_current < 15:
            bullish_signals += 2
            reasons.append(f"Low volatility (VIX = {vix_current:.1f})")
        elif vix_current < 20:
            bullish_signals += 1
            reasons.append(f"Normal volatility (VIX = {vix_current:.1f})")
        elif vix_current < 25:
            bearish_signals += 1
            reasons.append(f"Elevated volatility (VIX = {vix_current:.1f})")
        else:
            bearish_signals += 2
            reasons.append(f"High volatility (VIX = {vix_current:.1f})")

        # Analyze VIX trend
        if vix_change_pct < -5:
            bullish_signals += 1
            reasons.append(f"Fear declining (VIX {vix_change_pct:.1f}%)")
        elif vix_change_pct > 5:
            bearish_signals += 1
            reasons.append(f"Fear rising (VIX {vix_change_pct:+.1f}%)")

        # Determine regime
        net_signal = bullish_signals - bearish_signals

        if net_signal >= 3:
            regime = "BULLISH"
            confidence = "HIGH"
            recommendation = "GOOD DAY TO TRADE"
        elif net_signal >= 1:
            regime = "BULLISH"
            confidence = "MEDIUM"
            recommendation = "FAVORABLE CONDITIONS"
        elif net_signal >= -1:
            regime = "NEUTRAL"
            confidence = "MEDIUM"
            recommendation = "NORMAL CONDITIONS"
        elif net_signal >= -3:
            regime = "BEARISH"
            confidence = "MEDIUM"
            recommendation = "PROCEED WITH CAUTION"
        else:
            regime = "BEARISH"
            confidence = "HIGH"
            recommendation = "UNFAVORABLE CONDITIONS"

        reasoning = " • ".join(reasons)

        return regime, confidence, recommendation, reasoning

    def record_user_decision(self, assessment_id, decision):
        """Record user's decision to proceed or skip"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE market_regime_assessments
            SET user_decision = ?
            WHERE assessment_id = ?
        """, (decision, assessment_id))

        conn.commit()
        conn.close()
        logger.info(f"Recorded user decision: {decision} for {assessment_id}")

    def record_outcome(self, assessment_id, trades_executed, portfolio_change_pct, spy_eod_change_pct):
        """Record outcome of trading day for accuracy tracking"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE market_regime_assessments
            SET trades_executed = ?,
                portfolio_change_pct = ?,
                spy_eod_change_pct = ?
            WHERE assessment_id = ?
        """, (trades_executed, portfolio_change_pct, spy_eod_change_pct, assessment_id))

        conn.commit()
        conn.close()
        logger.info(f"Recorded outcome for {assessment_id}")


if __name__ == "__main__":
    # Test the analyzer
    logging.basicConfig(level=logging.INFO)

    project_root = Path(__file__).parent.parent.parent
    analyzer = MarketRegimeAnalyzer(project_root)

    result = analyzer.analyze_regime()

    if result['status'] == 'SUCCESS':
        print(f"\nMarket Regime: {result['regime']} ({result['confidence']} confidence)")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"\nSPY: ${result['spy_price']:.2f} ({result['spy_change_pct']:+.2f}%)")
        print(f"VIX: {result['vix_level']:.2f} ({result['vix_change_pct']:+.2f}%)")
    else:
        print(f"Error: {result['message']}")
