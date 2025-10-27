# -*- coding: utf-8 -*-
# sentinel/tier1_technical_filter.py
# Tier 1: Technical filtering to reduce universe from ~2500 to ~250 stocks

"""
Tier 1 Technical Filter

Applies fast, cheap technical screens to reduce the Russell 3000 universe
(~2500 liquid stocks) down to ~250 technically viable candidates.

Filters Applied:
1. Liquidity: Average daily dollar volume > $1M
2. Price: $5 < price < $500 (avoid penny stocks and expensive shares)
3. Momentum: Positive 20-day trend strength
4. Volatility: ATR-based screens for tradeable range
5. Technical: RSI not extreme (20-80 range)

Cost: Near-zero (uses cached price data from Alpaca)
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd

import alpaca_trade_api as tradeapi

try:
    import config
    DATA_FEED = getattr(config, 'APCA_API_DATA_FEED', 'iex')
except ImportError:
    DATA_FEED = 'iex'  # Default to IEX feed


class Tier1TechnicalFilter:
    """Filter stocks using technical indicators."""

    def __init__(self, api: tradeapi.REST, logger: Optional[logging.Logger] = None):
        """
        Initialize Tier 1 filter.

        Args:
            api: Alpaca REST API instance
            logger: Optional logger instance
        """
        self.api = api
        self.logger = logger or logging.getLogger(__name__)

    def filter_universe(
        self,
        universe_symbols: List[str],
        min_dollar_volume: float = 1_000_000,
        min_price: float = 5.0,
        max_price: float = 500.0,
        min_rsi: float = 20.0,
        max_rsi: float = 80.0,
        target_count: int = 250
    ) -> List[Dict]:
        """
        Apply technical filters to universe.

        Args:
            universe_symbols: List of stock symbols to filter
            min_dollar_volume: Minimum average daily dollar volume
            min_price: Minimum stock price
            max_price: Maximum stock price
            min_rsi: Minimum RSI (avoid oversold extremes)
            max_rsi: Maximum RSI (avoid overbought extremes)
            target_count: Target number of stocks to return

        Returns:
            List of dicts with {symbol, score, metrics} for top candidates
        """
        self.logger.info(f"Starting Tier 1 filtering on {len(universe_symbols)} stocks...")

        candidates = []
        errors = 0

        for symbol in universe_symbols:
            try:
                metrics = self._calculate_technical_metrics(symbol)

                if not metrics:
                    continue

                # Apply hard filters
                if not self._passes_hard_filters(
                    metrics, min_dollar_volume, min_price, max_price, min_rsi, max_rsi
                ):
                    continue

                # Calculate composite score for ranking
                score = self._calculate_composite_score(metrics)

                candidates.append({
                    'symbol': symbol,
                    'score': score,
                    'metrics': metrics
                })

            except Exception as e:
                self.logger.debug(f"Error filtering {symbol}: {e}")
                errors += 1
                continue

        # Sort by score and take top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:target_count]

        self.logger.info(
            f"Tier 1 filtering complete: {len(top_candidates)}/{len(universe_symbols)} passed "
            f"({errors} errors)"
        )

        return top_candidates

    def _calculate_technical_metrics(self, symbol: str) -> Optional[Dict]:
        """
        Calculate technical metrics for a single stock.

        Args:
            symbol: Stock symbol

        Returns:
            Dict of technical metrics or None if data unavailable
        """
        try:
            # Fetch 1 year of daily bars
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)

            bars_obj = self.api.get_bars(
                symbol,
                '1Day',
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                limit=300,  # ~1 year of trading days
                feed=DATA_FEED  # Use IEX feed for paper trading
            )

            bars = bars_obj.df
            if bars.empty or len(bars) < 60:  # Need minimum data
                return None

            closes = bars['close']
            highs = bars['high']
            lows = bars['low']
            volumes = bars['volume']

            # Price metrics
            latest_close = float(closes.iloc[-1])
            latest_volume = float(volumes.iloc[-1])

            # Liquidity metrics
            avg_volume_20d = float(volumes.tail(20).mean())
            avg_dollar_volume = avg_volume_20d * latest_close

            # Trend metrics
            sma_20 = float(closes.rolling(window=20).mean().iloc[-1]) if len(closes) >= 20 else None
            sma_50 = float(closes.rolling(window=50).mean().iloc[-1]) if len(closes) >= 50 else None
            change_20d = ((latest_close - closes.iloc[-21]) / closes.iloc[-21] * 100) if len(closes) > 20 else 0

            # Volatility metrics (ATR)
            atr = self._calculate_atr(highs, lows, closes, period=14)
            atr_percent = (atr / latest_close * 100) if atr and latest_close > 0 else None

            # Momentum metrics
            rsi = self._calculate_rsi(closes, period=14)

            return {
                'price': latest_close,
                'volume': latest_volume,
                'avg_dollar_volume': avg_dollar_volume,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'change_20d': change_20d,
                'atr': atr,
                'atr_percent': atr_percent,
                'rsi': rsi
            }

        except Exception as e:
            self.logger.error(f"Error calculating metrics for {symbol}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _passes_hard_filters(
        self,
        metrics: Dict,
        min_dollar_volume: float,
        min_price: float,
        max_price: float,
        min_rsi: float,
        max_rsi: float
    ) -> bool:
        """
        Check if stock passes all hard filters.

        Args:
            metrics: Technical metrics dict
            min_dollar_volume: Minimum average daily dollar volume
            min_price: Minimum stock price
            max_price: Maximum stock price
            min_rsi: Minimum RSI
            max_rsi: Maximum RSI

        Returns:
            True if passes all filters
        """
        # Liquidity filter
        if metrics['avg_dollar_volume'] < min_dollar_volume:
            return False

        # Price range filter
        if metrics['price'] < min_price or metrics['price'] > max_price:
            return False

        # RSI filter (avoid extremes)
        if metrics['rsi'] is None:
            return False
        if metrics['rsi'] < min_rsi or metrics['rsi'] > max_rsi:
            return False

        # Volatility filter (must have tradeable range)
        if metrics['atr_percent'] is None or metrics['atr_percent'] < 1.0:
            return False

        return True

    def _calculate_composite_score(self, metrics: Dict) -> float:
        """
        Calculate composite score for ranking stocks.

        Higher scores indicate better candidates for deep analysis.

        Scoring factors:
        - Liquidity (20%): Higher volume = better
        - Momentum (40%): Positive 20-day trend + RSI mid-range
        - Trend alignment (20%): Price above moving averages
        - Volatility (20%): ATR in sweet spot (2-5% range)

        Args:
            metrics: Technical metrics dict

        Returns:
            Composite score (0-100)
        """
        score = 0.0

        # Liquidity score (0-20)
        # Log scale: $1M = 10, $10M = 15, $100M = 20
        import math
        dollar_vol_millions = metrics['avg_dollar_volume'] / 1_000_000
        liquidity_score = min(20, 10 + math.log10(dollar_vol_millions) * 5)
        score += liquidity_score

        # Momentum score (0-40)
        # Positive 20-day change is good
        change_score = min(20, max(0, metrics['change_20d']))
        score += change_score

        # RSI mid-range is good (40-60 = best, extremes = worst)
        rsi = metrics['rsi'] or 50
        rsi_distance_from_50 = abs(rsi - 50)
        rsi_score = max(0, 20 - rsi_distance_from_50)
        score += rsi_score

        # Trend alignment score (0-20)
        # Price above SMA20 and SMA50 is good
        trend_score = 0
        if metrics['sma_20'] and metrics['price'] > metrics['sma_20']:
            trend_score += 10
        if metrics['sma_50'] and metrics['price'] > metrics['sma_50']:
            trend_score += 10
        score += trend_score

        # Volatility score (0-20)
        # Sweet spot is 2-5% ATR (enough movement, not crazy)
        atr_pct = metrics['atr_percent'] or 0
        if 2 <= atr_pct <= 5:
            volatility_score = 20
        elif 1 <= atr_pct < 2 or 5 < atr_pct <= 7:
            volatility_score = 10
        else:
            volatility_score = 0
        score += volatility_score

        return score

    def _calculate_atr(
        self,
        highs: pd.Series,
        lows: pd.Series,
        closes: pd.Series,
        period: int = 14
    ) -> Optional[float]:
        """
        Calculate Average True Range.

        Args:
            highs: High prices series
            lows: Low prices series
            closes: Close prices series
            period: ATR period

        Returns:
            ATR value or None
        """
        if len(closes) < period + 1:
            return None

        # True Range = max(high-low, abs(high-prev_close), abs(low-prev_close))
        prev_closes = closes.shift(1)
        tr1 = highs - lows
        tr2 = abs(highs - prev_closes)
        tr3 = abs(lows - prev_closes)
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # ATR = moving average of TR
        atr = tr.rolling(window=period).mean().iloc[-1]
        return float(atr) if not pd.isna(atr) else None

    def _calculate_rsi(self, series: pd.Series, period: int = 14) -> Optional[float]:
        """
        Calculate Relative Strength Index.

        Args:
            series: Price series
            period: RSI period

        Returns:
            RSI value (0-100) or None
        """
        if series is None or len(series) < period + 1:
            return None

        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        if avg_loss.iloc[-1] == 0:
            return 100.0

        rs = avg_gain.iloc[-1] / avg_loss.iloc[-1]
        rsi = 100 - (100 / (1 + rs))

        return float(rsi)


# Convenience function for use in evening workflow
def run_tier1_filter(
    api: tradeapi.REST,
    universe_symbols: List[str],
    logger: Optional[logging.Logger] = None,
    target_count: int = 250
) -> List[Dict]:
    """
    Run Tier 1 technical filtering.

    Args:
        api: Alpaca REST API instance
        universe_symbols: List of symbols to filter
        logger: Optional logger
        target_count: Number of stocks to return

    Returns:
        List of top candidates with scores and metrics
    """
    filter_engine = Tier1TechnicalFilter(api, logger)
    return filter_engine.filter_universe(universe_symbols, target_count=target_count)
