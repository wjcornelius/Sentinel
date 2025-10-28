# -*- coding: utf-8 -*-
# sentinel/tier3_conviction_analysis.py
# Tier 3: Deep conviction analysis using GPT-4 Turbo

"""
Tier 3 Deep Conviction Analysis

Performs comprehensive analysis on the top 70 finalists from Tier 2.
Uses Perplexity AI (real-time news) + GPT-4 Turbo (deep analysis).

Output: BUY/SELL/HOLD decision + conviction score (1-100)
Cost: ~$0.005 per ticker (Perplexity) + $0.02 per ticker (GPT-4) = ~$0.025/ticker
Total: ~$1.75/day for 70 stocks (Perplexity + GPT-4)
"""

import logging
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

from openai import OpenAI
import alpaca_trade_api as tradeapi
from sentinel.perplexity_news import PerplexityNewsGatherer

try:
    import config
    OPENAI_API_KEY = config.OPENAI_API_KEY
    DATA_FEED = getattr(config, 'APCA_API_DATA_FEED', 'iex')
except ImportError:
    OPENAI_API_KEY = None
    DATA_FEED = 'iex'


# Analysis prompt template (extracted from main_script.py)
ANALYSIS_PROMPT_TEMPLATE = """
You are Sentinel, a disciplined equity analyst tasked with evaluating a single stock for a daily trading system. You will receive the following JSON payload:

Payload:
<<PAYLOAD>>

Your job is to decide whether the trading system should BUY, SELL, or HOLD this ticker tomorrow and to assign a conviction score between 1 and 100. Follow these instructions exactly:

1. Decision categories
   • BUY – add or increase exposure.
   • SELL – exit or reduce exposure.
   • HOLD – maintain the current position size.

2. Conviction scale (use the full range 1-100)
   • 95-100 – Exceptional edge. Multiple independent, high-quality signals align in a compelling way. Very rare; reserve for best-in-class setups.
   • 85-94 – Strong, actionable idea with clear catalysts and supportive data across most dimensions.
   • 75-84 – Good setup with solid evidence. Above-average conviction with minor concerns.
   • 70-74 – Mild positive bias. Decent setup but some mixed signals or moderate concerns.
   • 60-69 – Slight positive lean. Evidence is somewhat supportive but not compelling.
   • 50-59 – Neutral to slightly negative. Signals conflict or lack sufficient edge. Prefer HOLD.
   • 40-49 – Notable caution. Signals lean bearish or thesis is deteriorating.
   • 30-39 – Significant concerns. Multiple negative signals or broken technical setup.
   • 20-29 – Strong sell signal. Clear deterioration with urgent need to exit or avoid.
   • 1-19 – Acute risk/urgency. Severe red flags, broken thesis, or imminent negative catalysts. Use sparingly.

   Important: Use the full 1-100 range to capture nuances. Don't cluster around 70-80. Push scores toward extremes when data justifies it. This granularity is critical for position sizing.

3. Rationale
   • Provide 2–3 concise bullet points (no more than ~40 words each) covering the strongest drivers of your decision.
   • Mention concrete evidence: earnings momentum, valuation shifts, technical breaks, macro tailwinds/headwinds, regulatory news, etc.
   • If data conflicts, call it out.

4. Output format
   • Return a single JSON object on one line with the keys: symbol, decision, conviction, rationale (array of bullet strings).
   • Ensure valid JSON (double quotes, no trailing commas).

5. Tone & discipline
   • Be analytical, impartial, and data-driven.
   • Do not reference this prompt or the fact you are an AI.
   • If critical data is missing, mention it in the rationale and adjust conviction downward.

Take a moment to weigh all inputs carefully before responding. The trading engine relies on your conviction spread to size positions—make each score count.
"""


class Tier3ConvictionAnalysis:
    """Deep conviction analysis using GPT-4 Turbo."""

    def __init__(
        self,
        api: tradeapi.REST,
        openai_client: Optional[OpenAI] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize Tier 3 analysis.

        Args:
            api: Alpaca REST API instance
            openai_client: Optional OpenAI client
            logger: Optional logger instance
        """
        self.api = api
        self.logger = logger or logging.getLogger(__name__)

        # Initialize OpenAI
        if openai_client:
            self.openai = openai_client
        elif OPENAI_API_KEY:
            self.openai = OpenAI(api_key=OPENAI_API_KEY)
        else:
            raise ValueError("OpenAI API key required for Tier 3 analysis")

        # Initialize Perplexity for real-time news
        try:
            self.perplexity = PerplexityNewsGatherer(logger=self.logger)
            self.logger.info("Perplexity news gatherer initialized successfully")
        except Exception as e:
            self.logger.warning(f"Perplexity initialization failed: {e}. News context will be limited.")
            self.perplexity = None

    def analyze_finalists(
        self,
        tier2_finalists: List[Dict],
        hierarchical_context: Dict,
        current_positions: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Perform deep conviction analysis on finalists.

        Args:
            tier2_finalists: List of finalists from Tier 2
            hierarchical_context: Context from context_builder
            current_positions: Optional dict of current positions (symbol -> position obj)

        Returns:
            List of conviction analysis results
        """
        self.logger.info(f"Starting Tier 3 deep analysis on {len(tier2_finalists)} finalists...")

        market_context = hierarchical_context['market_context']
        sector_contexts = hierarchical_context['sector_contexts']

        # PHASE 1: Batch gather news for all tickers (Perplexity)
        news_context = {}
        if self.perplexity:
            self.logger.info("Gathering real-time news for all tickers via Perplexity...")
            symbols = [f['symbol'] for f in tier2_finalists]
            news_context = self.perplexity.gather_batch_news(symbols, days_back=7)
            successful_news = sum(1 for n in news_context.values() if n['success'])
            self.logger.info(f"News gathered: {successful_news}/{len(symbols)} successful")
        else:
            self.logger.warning("Perplexity not available - proceeding without real-time news")

        # PHASE 2: Analyze each ticker with news context (GPT-4)
        results = []
        errors = 0

        for i, finalist in enumerate(tier2_finalists, 1):
            symbol = finalist['symbol']
            sector = finalist.get('sector', 'Unknown')

            try:
                self.logger.info(f"Analyzing {symbol} ({i}/{len(tier2_finalists)})...")

                # Build complete dossier with news context
                dossier = self._build_dossier(
                    finalist,
                    market_context,
                    sector_contexts.get(sector, ''),
                    current_positions,
                    news_context.get(symbol, {})  # Add news context
                )

                if not dossier:
                    self.logger.warning(f"Could not build dossier for {symbol}, skipping")
                    continue

                # Get AI conviction analysis
                analysis = self._get_ai_conviction(dossier)

                if analysis:
                    results.append(analysis)
                    self.logger.info(
                        f"  → {analysis['decision']} (conviction: {analysis['conviction_score']})"
                    )
                else:
                    errors += 1

            except Exception as e:
                self.logger.error(f"Error analyzing {symbol}: {e}")
                errors += 1
                continue

        self.logger.info(
            f"Tier 3 analysis complete: {len(results)} analyzed, {errors} errors"
        )

        return results

    def _build_dossier(
        self,
        finalist: Dict,
        market_context: str,
        sector_context: str,
        current_positions: Optional[Dict],
        news_context: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Build complete dossier for a stock.

        Args:
            finalist: Tier 2 finalist dict
            market_context: Market context summary
            sector_context: Sector context summary
            current_positions: Dict of current positions
            news_context: Optional Perplexity news context

        Returns:
            Complete dossier dict or None
        """
        symbol = finalist['symbol']

        try:
            # Get price/volume data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)

            bars_obj = self.api.get_bars(
                symbol,
                '1Day',
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                feed=DATA_FEED
            )

            bars = bars_obj.df
            if bars.empty:
                return None

            # Calculate technicals
            closes = bars['close']
            technicals = self._calculate_technicals(bars)

            # Get fundamentals from yfinance
            ticker = yf.Ticker(symbol)
            info = ticker.info
            fundamentals = {
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'price_to_book': info.get('priceToBook'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow')
            }

            # Get news headlines from Alpaca (basic fallback)
            try:
                news = self.api.get_news(symbol, limit=5)
                headlines = [{'headline': n.headline, 'summary': n.summary} for n in news[:5]]
            except:
                headlines = []

            # Add Perplexity real-time news context (enhanced)
            perplexity_news = {}
            if news_context and news_context.get('success'):
                perplexity_news = {
                    'summary': news_context.get('news_summary', 'No recent news available'),
                    'key_events': news_context.get('key_events', []),
                    'sentiment': news_context.get('sentiment', 'neutral'),
                    'sources': news_context.get('sources', [])[:3],  # First 3 sources
                    'timestamp': news_context.get('timestamp', '')
                }
            else:
                perplexity_news = {
                    'summary': 'Real-time news unavailable',
                    'key_events': [],
                    'sentiment': 'unknown',
                    'sources': []
                }

            # Build position context if held
            position_context = {}
            if current_positions and symbol in current_positions:
                pos = current_positions[symbol]
                position_context = {
                    'currently_held': True,
                    'quantity': float(pos.qty),
                    'avg_entry_price': float(pos.avg_entry_price),
                    'current_price': float(pos.current_price),
                    'unrealized_pl_pct': (float(pos.current_price) - float(pos.avg_entry_price)) / float(pos.avg_entry_price)
                }
            else:
                position_context = {'currently_held': False}

            # Assemble complete dossier
            dossier = {
                'symbol': symbol,
                'company_name': info.get('longName', symbol),
                'latest_price': float(closes.iloc[-1]),
                'technicals': technicals,
                'fundamentals': fundamentals,
                'news_headlines': headlines,  # Alpaca news (fallback)
                'perplexity_news': perplexity_news,  # Real-time news from Perplexity
                'position_context': position_context,
                'tier1_score': finalist['tier1_score'],
                'tier2_score': finalist['tier2_score'],
                'tier2_reason': finalist['tier2_reason'],
                'macro_context': {
                    'market_briefing': market_context,
                    'sector_briefing': sector_context
                }
            }

            return dossier

        except Exception as e:
            self.logger.error(f"Error building dossier for {symbol}: {e}")
            return None

    def _calculate_technicals(self, bars: pd.DataFrame) -> Dict:
        """Calculate technical indicators."""
        closes = bars['close']
        highs = bars['high']
        lows = bars['low']
        volumes = bars['volume']

        latest_close = float(closes.iloc[-1])
        prev_close = float(closes.iloc[-2]) if len(closes) > 1 else latest_close

        # Price changes
        change_1d = ((latest_close - prev_close) / prev_close * 100) if prev_close else 0.0
        change_5d = ((latest_close - closes.iloc[-6]) / closes.iloc[-6] * 100) if len(closes) > 5 else 0.0
        change_20d = ((latest_close - closes.iloc[-21]) / closes.iloc[-21] * 100) if len(closes) > 20 else 0.0
        change_60d = ((latest_close - closes.iloc[-61]) / closes.iloc[-61] * 100) if len(closes) > 60 else 0.0

        # Moving averages
        sma_20 = float(closes.rolling(window=20).mean().iloc[-1]) if len(closes) >= 20 else None
        sma_50 = float(closes.rolling(window=50).mean().iloc[-1]) if len(closes) >= 50 else None
        sma_200 = float(closes.rolling(window=200).mean().iloc[-1]) if len(closes) >= 200 else None

        # RSI
        rsi_14 = self._calculate_rsi(closes, period=14)

        # 52-week range
        year_high = float(highs.rolling(window=min(len(highs), 252)).max().iloc[-1])
        year_low = float(lows.rolling(window=min(len(lows), 252)).min().iloc[-1])

        # Volume
        avg_volume_20d = float(volumes.tail(20).mean())

        return {
            'latest_close': latest_close,
            'change_1d': change_1d,
            'change_5d': change_5d,
            'change_20d': change_20d,
            'change_60d': change_60d,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'sma_200': sma_200,
            'rsi_14': rsi_14,
            'year_high': year_high,
            'year_low': year_low,
            'avg_volume_20d': avg_volume_20d
        }

    def _calculate_rsi(self, series: pd.Series, period: int = 14) -> Optional[float]:
        """Calculate RSI."""
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

    def _get_ai_conviction(self, dossier: Dict) -> Optional[Dict]:
        """
        Get AI conviction analysis.

        Args:
            dossier: Complete stock dossier

        Returns:
            Analysis dict with decision, conviction, rationale
        """
        symbol = dossier['symbol']

        # Build analysis payload
        analysis_payload = {
            "symbol": dossier.get("symbol"),
            "company_name": dossier.get("company_name"),
            "sector": dossier.get("fundamentals", {}).get("sector"),
            "industry": dossier.get("fundamentals", {}).get("industry"),
            "price": dossier.get("latest_price"),
            "market_cap": dossier.get("fundamentals", {}).get("market_cap"),
            "technicals": dossier.get("technicals", {}),
            "fundamentals": dossier.get("fundamentals", {}),
            "news_headlines": dossier.get("news_headlines", []),
            "position_context": dossier.get("position_context", {}),
            "tier2_context": {
                "tier1_score": dossier.get("tier1_score"),
                "tier2_score": dossier.get("tier2_score"),
                "tier2_reason": dossier.get("tier2_reason")
            },
            "macro_context": dossier.get("macro_context", {})
        }

        prompt = ANALYSIS_PROMPT_TEMPLATE.replace("<<PAYLOAD>>", json.dumps(analysis_payload, indent=2))

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                timeout=45.0
            )

            analysis = json.loads(response.choices[0].message.content)

            required_keys = {'symbol', 'decision', 'conviction', 'rationale'}
            if not required_keys.issubset(analysis.keys()):
                self.logger.error(f"AI response for {symbol} missing keys: {analysis.keys()}")
                return None

            # Normalize decision
            decision = str(analysis.get("decision", "HOLD")).strip().upper()
            if decision not in {"BUY", "SELL", "HOLD"}:
                decision = "HOLD"

            # Sanitize conviction (1-100 scale)
            conviction = analysis.get("conviction", 50)
            try:
                conviction = max(1, min(100, int(conviction)))
            except:
                conviction = 50

            # Format rationale
            rationale = analysis.get("rationale", [])
            if isinstance(rationale, list):
                rationale_text = " | ".join(str(item).strip() for item in rationale if item)
            else:
                rationale_text = str(rationale).strip()

            if not rationale_text:
                rationale_text = "No rationale provided."

            return {
                'symbol': symbol,
                'decision': decision,
                'conviction_score': conviction,
                'rationale': rationale_text,
                'tier1_score': dossier.get('tier1_score'),
                'tier2_score': dossier.get('tier2_score'),
                'latest_price': dossier.get('latest_price'),
                'sector': dossier.get('fundamentals', {}).get('sector')
            }

        except Exception as e:
            self.logger.error(f"Failed to get AI analysis for {symbol}: {e}")
            return None


# Convenience function for use in evening workflow
def run_tier3_analysis(
    api: tradeapi.REST,
    tier2_finalists: List[Dict],
    hierarchical_context: Dict,
    current_positions: Optional[Dict] = None,
    logger: Optional[logging.Logger] = None
) -> List[Dict]:
    """
    Run Tier 3 deep conviction analysis.

    Args:
        api: Alpaca REST API instance
        tier2_finalists: List of finalists from Tier 2
        hierarchical_context: Context from context_builder
        current_positions: Optional dict of current positions
        logger: Optional logger

    Returns:
        List of conviction analysis results (BUY/SELL/HOLD + scores)
    """
    analyzer = Tier3ConvictionAnalysis(api, logger=logger)
    return analyzer.analyze_finalists(tier2_finalists, hierarchical_context, current_positions)
