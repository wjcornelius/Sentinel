---
from: RESEARCH
message_id: MSG_RESEARCH_20251112T154520Z_cc8a68dc
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2025-11-12T15:45:20.723975Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2025-11-12

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -0.00%
- **VIX**: 17.5 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 67 swing-suitable stocks
- **Current Holdings**: 33 positions from Alpaca
- **Total Scored**: 100 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **ALGM** - Composite: 22.8/100
   - Technical: 10.0, Fundamental: 22.0
2. **DNOW** - Composite: 36.8/100
   - Technical: 10.0, Fundamental: 57.0
3. **SWKS** - Composite: 46.8/100
   - Technical: 30.0, Fundamental: 62.0
4. **TME** - Composite: 46.8/100
   - Technical: 20.0, Fundamental: 72.0
5. **ALHC** - Composite: 29.6/100
   - Technical: 30.0, Fundamental: 19.0

```json
{
  "market_conditions": {
    "spy_change_pct": -0.0029311173133206303,
    "vix": 17.540000915527344,
    "vix_status": "NORMAL",
    "date": "2025-11-12"
  },
  "candidates": [
    {
      "ticker": "ALGM",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 22.8,
      "current_price": 26.875
    },
    {
      "ticker": "DNOW",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.8,
      "current_price": 13.170000076293945
    },
    {
      "ticker": "SWKS",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 62.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 69.80500030517578
    },
    {
      "ticker": "TME",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 72.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 18.520000457763672
    },
    {
      "ticker": "ALHC",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 19.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 29.6,
      "current_price": 16.670000076293945
    },
    {
      "ticker": "CSGP",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.8,
      "current_price": 67.98999786376953
    },
    {
      "ticker": "FOUR",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.6,
      "current_price": 71.97000122070312
    },
    {
      "ticker": "GPK",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.0,
      "current_price": 16.174999237060547
    },
    {
      "ticker": "KD",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 39.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 37.6,
      "current_price": 26.110000610351562
    },
    {
      "ticker": "ADM",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 46.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.400000000000006,
      "current_price": 57.7599983215332
    },
    {
      "ticker": "ALLY",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 53.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 65.2,
      "current_price": 40.09000015258789
    },
    {
      "ticker": "APLS",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.8,
      "current_price": 19.969999313354492
    },
    {
      "ticker": "APTV",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 30.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.0,
      "current_price": 81.5999984741211
    },
    {
      "ticker": "ARE",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 17.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 20.8,
      "current_price": 54.6349983215332
    },
    {
      "ticker": "ARQT",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 24.00749969482422
    },
    {
      "ticker": "ASTS",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.8,
      "current_price": 69.90499877929688
    },
    {
      "ticker": "AVTR",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 14.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 19.6,
      "current_price": 11.550000190734863
    },
    {
      "ticker": "BA",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 31.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.4,
      "current_price": 195.7032928466797
    },
    {
      "ticker": "BAH",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.0,
      "current_price": 86.79000091552734
    },
    {
      "ticker": "BEAM",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 20.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 26.0,
      "current_price": 22.18000030517578
    },
    {
      "ticker": "BEKE",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 31.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.4,
      "current_price": 16.594999313354492
    },
    {
      "ticker": "BLSH",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 20.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.0,
      "current_price": 45.630001068115234
    },
    {
      "ticker": "BMNR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 12.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 26.8,
      "current_price": 39.59000015258789
    },
    {
      "ticker": "BRO",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 56.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.400000000000006,
      "current_price": 80.3499984741211
    },
    {
      "ticker": "BROS",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 47.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.8,
      "current_price": 59.20000076293945
    },
    {
      "ticker": "BX",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.6,
      "current_price": 146.30999755859375
    },
    {
      "ticker": "CARR",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 33.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 57.48500061035156
    },
    {
      "ticker": "CAVA",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 48.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 33.2,
      "current_price": 50.244998931884766
    },
    {
      "ticker": "CCJ",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 30.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 93.30999755859375
    },
    {
      "ticker": "CDE",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 72.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 15.395000457763672
    },
    {
      "ticker": "CELH",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 24.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 23.6,
      "current_price": 44.04999923706055
    },
    {
      "ticker": "CENX",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 41.6,
      "current_price": 28.8700008392334
    },
    {
      "ticker": "CF",
      "technical": {
        "score": 55.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 85.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.0,
      "current_price": 84.29000091552734
    },
    {
      "ticker": "CG",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 55.05500030517578
    },
    {
      "ticker": "CLF",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 24.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 31.6,
      "current_price": 10.704999923706055
    },
    {
      "ticker": "COLD",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 10.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 22.0,
      "current_price": 11.470000267028809
    },
    {
      "ticker": "CPNG",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 39.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 33.6,
      "current_price": 28.879899978637695
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 44.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.6,
      "current_price": 30.34000015258789
    },
    {
      "ticker": "CRSP",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 26.8,
      "current_price": 53.310001373291016
    },
    {
      "ticker": "CZR",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 10.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.0,
      "current_price": 19.899999618530273
    },
    {
      "ticker": "DG",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 68.0,
      "current_price": 104.51499938964844
    },
    {
      "ticker": "DHI",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 51.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.400000000000006,
      "current_price": 147.06500244140625
    },
    {
      "ticker": "DJT",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 20.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 22.0,
      "current_price": 12.890000343322754
    },
    {
      "ticker": "DKNG",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 8.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 31.75
    },
    {
      "ticker": "DT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 67.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 46.7400016784668
    },
    {
      "ticker": "ELAN",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 22.770000457763672
    },
    {
      "ticker": "EMR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 29.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 33.6,
      "current_price": 129.52999877929688
    },
    {
      "ticker": "ENPH",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 67.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 31.775699615478516
    },
    {
      "ticker": "EQH",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 20.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.0,
      "current_price": 45.40999984741211
    },
    {
      "ticker": "EWY",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 30.0,
        "sector": "Unknown"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.0,
      "current_price": 95.71499633789062
    },
    {
      "ticker": "EXAS",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 68.08000183105469
    },
    {
      "ticker": "FLEX",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 38.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.2,
      "current_price": 63.90999984741211
    },
    {
      "ticker": "FLG",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 27.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.8,
      "current_price": 11.050000190734863
    },
    {
      "ticker": "FLO",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 35.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.0,
      "current_price": 11.604999542236328
    },
    {
      "ticker": "FRSH",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 27.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.8,
      "current_price": 11.539999961853027
    },
    {
      "ticker": "FTI",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 62.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 74.8,
      "current_price": 43.540000915527344
    },
    {
      "ticker": "FTNT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 46.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.400000000000006,
      "current_price": 82.36000061035156
    },
    {
      "ticker": "GEHC",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 53.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.2,
      "current_price": 74.06999969482422
    },
    {
      "ticker": "GENI",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 24.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 27.6,
      "current_price": 10.444999694824219
    },
    {
      "ticker": "GEO",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 70.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.0,
      "current_price": 15.09000015258789
    },
    {
      "ticker": "GLW",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 89.7699966430664
    },
    {
      "ticker": "GLXY",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 14.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 23.6,
      "current_price": 31.239999771118164
    },
    {
      "ticker": "GNTX",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 78.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 61.2,
      "current_price": 23.440000534057617
    },
    {
      "ticker": "GPN",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 77.2300033569336
    },
    {
      "ticker": "GRND",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 25.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.0,
      "current_price": 14.970000267028809
    },
    {
      "ticker": "GSK",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 48.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 69.2,
      "current_price": 47.54999923706055
    },
    {
      "ticker": "HIMS",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 42.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.8,
      "current_price": 40.04999923706055
    }
  ],
  "current_holdings": [
    {
      "ticker": "AAL",
      "technical_score": 100.0,
      "fundamental_score": 34.0,
      "sentiment_score": 50.0,
      "research_composite_score": 63.6,
      "context": "holdings",
      "current_price": 13.279999732971191,
      "sector": "Industrials",
      "quantity": 270.0,
      "market_value": 3605.85,
      "cost_basis": 3574.8,
      "unrealized_pl": 31.05,
      "unrealized_plpc": 0.8685800604229601
    },
    {
      "ticker": "ACGL",
      "technical_score": 85.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.4,
      "context": "holdings",
      "current_price": 91.1500015258789,
      "sector": "Financial Services",
      "quantity": 101.0,
      "market_value": 9251.6,
      "cost_basis": 8950.62,
      "unrealized_pl": 300.98,
      "unrealized_plpc": 3.3626720830512298
    },
    {
      "ticker": "ALAB",
      "technical_score": 30.0,
      "fundamental_score": 52.0,
      "sentiment_score": 50.0,
      "research_composite_score": 42.8,
      "context": "holdings",
      "current_price": 155.5,
      "sector": "Technology",
      "quantity": 27.0,
      "market_value": 4219.02,
      "cost_basis": 4678.83,
      "unrealized_pl": -459.81,
      "unrealized_plpc": -9.82745686421605
    },
    {
      "ticker": "ALKS",
      "technical_score": 75.0,
      "fundamental_score": 64.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.6,
      "context": "holdings",
      "current_price": 29.989999771118164,
      "sector": "Healthcare",
      "quantity": 108.0,
      "market_value": 3305.88,
      "cost_basis": 3534.84,
      "unrealized_pl": -228.96,
      "unrealized_plpc": -6.47723800794378
    },
    {
      "ticker": "APH",
      "technical_score": 100.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 76.0,
      "context": "holdings",
      "current_price": 143.1649932861328,
      "sector": "Technology",
      "quantity": 58.0,
      "market_value": 8258.62,
      "cost_basis": 8081.72,
      "unrealized_pl": 176.9,
      "unrealized_plpc": 2.18889048370891
    },
    {
      "ticker": "APO",
      "technical_score": 85.0,
      "fundamental_score": 77.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.8,
      "context": "holdings",
      "current_price": 135.9499969482422,
      "sector": "Financial Services",
      "quantity": 54.0,
      "market_value": 7245.72,
      "cost_basis": 6997.32,
      "unrealized_pl": 248.4,
      "unrealized_plpc": 3.5499305448371703
    },
    {
      "ticker": "AXTA",
      "technical_score": 85.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.4,
      "context": "holdings",
      "current_price": 29.645000457763672,
      "sector": "Basic Materials",
      "quantity": 123.0,
      "market_value": 3635.88,
      "cost_basis": 3523.95,
      "unrealized_pl": 111.93,
      "unrealized_plpc": 3.1762652705061103
    },
    {
      "ticker": "AZN",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 88.54000091552734,
      "sector": "Healthcare",
      "quantity": 80.0,
      "market_value": 7074.384,
      "cost_basis": 6770.4,
      "unrealized_pl": 303.984,
      "unrealized_plpc": 4.48989719957462
    },
    {
      "ticker": "BANC",
      "technical_score": 90.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.8,
      "context": "holdings",
      "current_price": 17.600000381469727,
      "sector": "Financial Services",
      "quantity": 344.0,
      "market_value": 6035.48,
      "cost_basis": 5968.4,
      "unrealized_pl": 67.08,
      "unrealized_plpc": 1.12391930835735
    },
    {
      "ticker": "BKR",
      "technical_score": 100.0,
      "fundamental_score": 54.0,
      "sentiment_score": 50.0,
      "research_composite_score": 71.6,
      "context": "holdings",
      "current_price": 48.2400016784668,
      "sector": "Energy",
      "quantity": 73.0,
      "market_value": 3505.46,
      "cost_basis": 3573.35,
      "unrealized_pl": -67.89,
      "unrealized_plpc": -1.8998978549540297
    },
    {
      "ticker": "BMRN",
      "technical_score": 85.0,
      "fundamental_score": 49.0,
      "sentiment_score": 50.0,
      "research_composite_score": 63.6,
      "context": "holdings",
      "current_price": 55.099998474121094,
      "sector": "Healthcare",
      "quantity": 61.0,
      "market_value": 3339.14,
      "cost_basis": 3263.5,
      "unrealized_pl": 75.64,
      "unrealized_plpc": 2.3177570093457898
    },
    {
      "ticker": "BMY",
      "technical_score": 80.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 49.42499923706055,
      "sector": "Healthcare",
      "quantity": 109.0,
      "market_value": 5405.855,
      "cost_basis": 5072.86,
      "unrealized_pl": 332.995,
      "unrealized_plpc": 6.56424581005587
    },
    {
      "ticker": "CFG",
      "technical_score": 85.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 53.220001220703125,
      "sector": "Financial Services",
      "quantity": 98.0,
      "market_value": 5187.14,
      "cost_basis": 5078.36,
      "unrealized_pl": 108.78,
      "unrealized_plpc": 2.14203010420687
    },
    {
      "ticker": "COMM",
      "technical_score": 100.0,
      "fundamental_score": 62.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.8,
      "context": "holdings",
      "current_price": 17.725000381469727,
      "sector": "Technology",
      "quantity": 210.0,
      "market_value": 3690.75,
      "cost_basis": 3574.2,
      "unrealized_pl": 116.55,
      "unrealized_plpc": 3.26086956521739
    },
    {
      "ticker": "CRDO",
      "technical_score": 45.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 50.8,
      "context": "holdings",
      "current_price": 159.67999267578125,
      "sector": "Technology",
      "quantity": 20.0,
      "market_value": 3195.076,
      "cost_basis": 3301.15,
      "unrealized_pl": -106.074,
      "unrealized_plpc": -3.21324386956061
    },
    {
      "ticker": "CTSH",
      "technical_score": 90.0,
      "fundamental_score": 59.0,
      "sentiment_score": 50.0,
      "research_composite_score": 69.6,
      "context": "holdings",
      "current_price": 73.63999938964844,
      "sector": "Technology",
      "quantity": 82.0,
      "market_value": 6054.88,
      "cost_basis": 5983.54,
      "unrealized_pl": 71.34,
      "unrealized_plpc": 1.19227079621762
    },
    {
      "ticker": "CVE",
      "technical_score": 85.0,
      "fundamental_score": 58.0,
      "sentiment_score": 50.0,
      "research_composite_score": 67.2,
      "context": "holdings",
      "current_price": 18.104999542236328,
      "sector": "Energy",
      "quantity": 265.0,
      "market_value": 4784.575,
      "cost_basis": 4783.25,
      "unrealized_pl": 1.325,
      "unrealized_plpc": 0.02770083102493
    },
    {
      "ticker": "DBX",
      "technical_score": 85.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 30.885000228881836,
      "sector": "Technology",
      "quantity": 117.0,
      "market_value": 3613.545,
      "cost_basis": 3606.55,
      "unrealized_pl": 6.995,
      "unrealized_plpc": 0.19395266944864
    },
    {
      "ticker": "DVN",
      "technical_score": 85.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 35.26499938964844,
      "sector": "Energy",
      "quantity": 139.0,
      "market_value": 4883.765,
      "cost_basis": 4826.08,
      "unrealized_pl": 57.685,
      "unrealized_plpc": 1.1952764976958499
    },
    {
      "ticker": "EIX",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 57.900001525878906,
      "sector": "Utilities",
      "quantity": 214.0,
      "market_value": 12435.54,
      "cost_basis": 11864.16,
      "unrealized_pl": 571.38,
      "unrealized_plpc": 4.81601731601732
    },
    {
      "ticker": "EMN",
      "technical_score": 85.0,
      "fundamental_score": 45.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.0,
      "context": "holdings",
      "current_price": 61.32500076293945,
      "sector": "Basic Materials",
      "quantity": 72.0,
      "market_value": 4380.48,
      "cost_basis": 4437.36,
      "unrealized_pl": -56.88,
      "unrealized_plpc": -1.2818432581535
    },
    {
      "ticker": "EQT",
      "technical_score": 80.0,
      "fundamental_score": 52.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 60.59000015258789,
      "sector": "Energy",
      "quantity": 89.0,
      "market_value": 5413.0245,
      "cost_basis": 5015.16,
      "unrealized_pl": 397.8645,
      "unrealized_plpc": 7.93323642715287
    },
    {
      "ticker": "FITB",
      "technical_score": 85.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.4,
      "context": "holdings",
      "current_price": 43.45000076293945,
      "sector": "Financial Services",
      "quantity": 118.0,
      "market_value": 5113.53,
      "cost_basis": 5023.26,
      "unrealized_pl": 90.27,
      "unrealized_plpc": 1.7970401691331899
    },
    {
      "ticker": "HST",
      "technical_score": 75.0,
      "fundamental_score": 62.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 18.184999465942383,
      "sector": "Real Estate",
      "quantity": 432.0,
      "market_value": 7840.8,
      "cost_basis": 7391.52,
      "unrealized_pl": 449.28,
      "unrealized_plpc": 6.07831677381648
    },
    {
      "ticker": "MNST",
      "technical_score": 100.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 80.0,
      "context": "holdings",
      "current_price": 71.58999633789062,
      "sector": "Consumer Defensive",
      "quantity": 83.0,
      "market_value": 5974.34,
      "cost_basis": 5965.3,
      "unrealized_pl": 9.04,
      "unrealized_plpc": 0.15154309087556
    },
    {
      "ticker": "NVDA",
      "technical_score": 70.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 193.42750549316406,
      "sector": "Technology",
      "quantity": 37.0,
      "market_value": 7122.5,
      "cost_basis": 7057.64,
      "unrealized_pl": 64.86,
      "unrealized_plpc": 0.9190040863518101
    },
    {
      "ticker": "OPCH",
      "technical_score": 85.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 28.540000915527344,
      "sector": "Healthcare",
      "quantity": 154.0,
      "market_value": 4432.12,
      "cost_basis": 4316.62,
      "unrealized_pl": 115.5,
      "unrealized_plpc": 2.67570460221192
    },
    {
      "ticker": "PDD",
      "technical_score": 100.0,
      "fundamental_score": 68.0,
      "sentiment_score": 50.0,
      "research_composite_score": 77.2,
      "context": "holdings",
      "current_price": 136.27999877929688,
      "sector": "Consumer Cyclical",
      "quantity": 44.0,
      "market_value": 5989.5,
      "cost_basis": 5990.16,
      "unrealized_pl": -0.66,
      "unrealized_plpc": -0.0110180696342
    },
    {
      "ticker": "ROKU",
      "technical_score": 100.0,
      "fundamental_score": 22.0,
      "sentiment_score": 50.0,
      "research_composite_score": 58.8,
      "context": "holdings",
      "current_price": 106.55500030517578,
      "sector": "Communication Services",
      "quantity": 42.0,
      "market_value": 4463.97,
      "cost_basis": 4444.86,
      "unrealized_pl": 19.11,
      "unrealized_plpc": 0.4299348010961
    },
    {
      "ticker": "SLB",
      "technical_score": 100.0,
      "fundamental_score": 50.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.0,
      "context": "holdings",
      "current_price": 37.10499954223633,
      "sector": "Energy",
      "quantity": 185.0,
      "market_value": 6804.7625,
      "cost_basis": 6752.5,
      "unrealized_pl": 52.2625,
      "unrealized_plpc": 0.77397260273973
    },
    {
      "ticker": "SN",
      "technical_score": 85.0,
      "fundamental_score": 60.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 94.55000305175781,
      "sector": "Consumer Cyclical",
      "quantity": 37.0,
      "market_value": 3456.725,
      "cost_basis": 3571.98,
      "unrealized_pl": -115.255,
      "unrealized_plpc": -3.2266418065050804
    },
    {
      "ticker": "SYF",
      "technical_score": 100.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 80.0,
      "context": "holdings",
      "current_price": 75.93000030517578,
      "sector": "Financial Services",
      "quantity": 82.0,
      "market_value": 6209.86,
      "cost_basis": 6150.0,
      "unrealized_pl": 59.86,
      "unrealized_plpc": 0.97333333333333
    },
    {
      "ticker": "WFC",
      "technical_score": 90.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.4,
      "context": "holdings",
      "current_price": 88.30000305175781,
      "sector": "Financial Services",
      "quantity": 114.0,
      "market_value": 9976.14,
      "cost_basis": 9986.4,
      "unrealized_pl": -10.26,
      "unrealized_plpc": -0.1027397260274
    }
  ],
  "screening": {
    "universe_size": 100,
    "candidates_found": 67,
    "holdings_count": 33,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
