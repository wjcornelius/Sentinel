---
from: RESEARCH
message_id: MSG_RESEARCH_20260515T160458Z_eab05ca4
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-05-15T16:04:58.878049Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-05-15

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -1.11%
- **VIX**: 18.5 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 65 swing-suitable stocks
- **Current Holdings**: 11 positions from Alpaca
- **Total Scored**: 76 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **TREX** - Composite: 42.8/100
   - Technical: 30.0, Fundamental: 52.0
2. **G** - Composite: 45.6/100
   - Technical: 20.0, Fundamental: 69.0
3. **LKQ** - Composite: 34.4/100
   - Technical: 20.0, Fundamental: 41.0
4. **LRN** - Composite: 42.0/100
   - Technical: 20.0, Fundamental: 60.0
5. **ABNB** - Composite: 39.6/100
   - Technical: 20.0, Fundamental: 54.0

```json
{
  "market_conditions": {
    "spy_change_pct": -1.1080177160792015,
    "vix": 18.459999084472656,
    "vix_status": "NORMAL",
    "date": "2026-05-15"
  },
  "candidates": [
    {
      "ticker": "TREX",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 52.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.8,
      "current_price": 37.28499984741211
    },
    {
      "ticker": "G",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 69.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.6,
      "current_price": 29.25
    },
    {
      "ticker": "LKQ",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 41.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.400000000000006,
      "current_price": 25.06999969482422
    },
    {
      "ticker": "LRN",
      "technical": {
        "score": 20.0,
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
      "composite_score": 42.0,
      "current_price": 87.91000366210938
    },
    {
      "ticker": "ABNB",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 54.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.6,
      "current_price": 132.43499755859375
    },
    {
      "ticker": "ACI",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 23.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.2,
      "current_price": 16.40999984741211
    },
    {
      "ticker": "AG",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 65.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.0,
      "current_price": 20.049999237060547
    },
    {
      "ticker": "ALB",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.8,
      "current_price": 182.66000366210938
    },
    {
      "ticker": "ALGM",
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
      "current_price": 42.560001373291016
    },
    {
      "ticker": "ALHC",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 31.6,
      "current_price": 16.18000030517578
    },
    {
      "ticker": "AMKR",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 58.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 51.2,
      "current_price": 70.79499816894531
    },
    {
      "ticker": "APH",
      "technical": {
        "score": 20.0,
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
      "composite_score": 42.8,
      "current_price": 125.27999877929688
    },
    {
      "ticker": "ASTS",
      "technical": {
        "score": 85.0,
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
      "composite_score": 52.8,
      "current_price": 79.36329650878906
    },
    {
      "ticker": "AVTR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 17.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 28.8,
      "current_price": 7.730000019073486
    },
    {
      "ticker": "BBIO",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 35.6,
      "current_price": 67.79499816894531
    },
    {
      "ticker": "BBY",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 52.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.8,
      "current_price": 56.43000030517578
    },
    {
      "ticker": "BDX",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 36.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.4,
      "current_price": 142.94000244140625
    },
    {
      "ticker": "BEAM",
      "technical": {
        "score": 45.0,
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
      "composite_score": 40.8,
      "current_price": 28.209999084472656
    },
    {
      "ticker": "BRO",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 61.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.400000000000006,
      "current_price": 56.2599983215332
    },
    {
      "ticker": "BTDR",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 33.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 63.2,
      "current_price": 13.289999961853027
    },
    {
      "ticker": "C",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 70.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 56.0,
      "current_price": 123.16999816894531
    },
    {
      "ticker": "CART",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 76.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.400000000000006,
      "current_price": 39.43000030517578
    },
    {
      "ticker": "CCI",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 30.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 86.01000213623047
    },
    {
      "ticker": "CCJ",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 51.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.400000000000006,
      "current_price": 108.03500366210938
    },
    {
      "ticker": "CDE",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 75.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 64.0,
      "current_price": 17.645000457763672
    },
    {
      "ticker": "CELH",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 29.764999389648438
    },
    {
      "ticker": "CENX",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 63.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 56.83000183105469
    },
    {
      "ticker": "CHTR",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 41.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.400000000000006,
      "current_price": 142.30999755859375
    },
    {
      "ticker": "CHYM",
      "technical": {
        "score": 20.0,
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
      "composite_score": 28.8,
      "current_price": 17.43000030517578
    },
    {
      "ticker": "CLSK",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 15.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.0,
      "current_price": 13.050000190734863
    },
    {
      "ticker": "CMG",
      "technical": {
        "score": 30.0,
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
      "composite_score": 37.6,
      "current_price": 32.584999084472656
    },
    {
      "ticker": "CNK",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.0,
      "current_price": 26.260000228881836
    },
    {
      "ticker": "CNM",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 51.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.400000000000006,
      "current_price": 47.09000015258789
    },
    {
      "ticker": "COIN",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 31.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.4,
      "current_price": 192.88999938964844
    },
    {
      "ticker": "COLB",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 75.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 28.6299991607666
    },
    {
      "ticker": "CORZ",
      "technical": {
        "score": 100.0,
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
      "composite_score": 60.8,
      "current_price": 23.635000228881836
    },
    {
      "ticker": "CRDO",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 75.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 175.57000732421875
    },
    {
      "ticker": "CVNA",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 68.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.2,
      "current_price": 68.4800033569336
    },
    {
      "ticker": "DAR",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 51.6,
      "current_price": 62.470001220703125
    },
    {
      "ticker": "DD",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 29.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 61.6,
      "current_price": 49.279998779296875
    },
    {
      "ticker": "DXCM",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 67.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 70.8,
      "current_price": 61.755001068115234
    },
    {
      "ticker": "EBC",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 19.25
    },
    {
      "ticker": "ENTG",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.0,
      "current_price": 133.36000061035156
    },
    {
      "ticker": "EQT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 70.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.0,
      "current_price": 56.5
    },
    {
      "ticker": "EW",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.0,
      "current_price": 81.55000305175781
    },
    {
      "ticker": "EXE",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 61.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 68.4,
      "current_price": 96.94999694824219
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
      "current_price": 13.390000343322754
    },
    {
      "ticker": "FND",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 29.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 33.6,
      "current_price": 44.560001373291016
    },
    {
      "ticker": "FOUR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 26.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.4,
      "current_price": 42.22999954223633
    },
    {
      "ticker": "FTI",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.0,
      "current_price": 71.68000030517578
    },
    {
      "ticker": "GM",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 24.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 31.6,
      "current_price": 75.41000366210938
    },
    {
      "ticker": "GME",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 41.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.400000000000006,
      "current_price": 21.899999618530273
    },
    {
      "ticker": "GSK",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 49.56999969482422
    },
    {
      "ticker": "GTLB",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.8,
      "current_price": 23.594999313354492
    },
    {
      "ticker": "HAL",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 51.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.400000000000006,
      "current_price": 41.22740173339844
    },
    {
      "ticker": "HALO",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 70.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 78.0,
      "current_price": 67.19000244140625
    },
    {
      "ticker": "HAYW",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 76.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.400000000000006,
      "current_price": 13.645000457763672
    },
    {
      "ticker": "HIMS",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 11.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.4,
      "current_price": 24.920000076293945
    },
    {
      "ticker": "HL",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 62.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.8,
      "current_price": 17.600000381469727
    },
    {
      "ticker": "HPQ",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 33.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 41.2,
      "current_price": 20.725000381469727
    },
    {
      "ticker": "INSM",
      "technical": {
        "score": 30.0,
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
      "composite_score": 30.8,
      "current_price": 110.74500274658203
    },
    {
      "ticker": "IONS",
      "technical": {
        "score": 75.0,
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
      "composite_score": 48.8,
      "current_price": 74.5
    },
    {
      "ticker": "JBS",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 54.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.6,
      "current_price": 13.6850004196167
    },
    {
      "ticker": "JCI",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 46.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.400000000000006,
      "current_price": 142.06500244140625
    },
    {
      "ticker": "JOBY",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 10.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.0,
      "current_price": 10.312800407409668
    }
  ],
  "current_holdings": [
    {
      "ticker": "ALAB",
      "technical_score": 100.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 76.0,
      "context": "holdings",
      "current_price": 228.64500427246094,
      "sector": "Technology",
      "quantity": 51.0,
      "market_value": 11685.63,
      "cost_basis": 6389.28,
      "unrealized_pl": 5296.35,
      "unrealized_plpc": 82.894
    },
    {
      "ticker": "ARM",
      "technical_score": 70.0,
      "fundamental_score": 60.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.0,
      "context": "holdings",
      "current_price": 212.08999633789062,
      "sector": "Technology",
      "quantity": 41.0,
      "market_value": 8711.68,
      "cost_basis": 6607.97,
      "unrealized_pl": 2103.71,
      "unrealized_plpc": 31.836
    },
    {
      "ticker": "BANC",
      "technical_score": 45.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 54.400000000000006,
      "context": "holdings",
      "current_price": 18.270000457763672,
      "sector": "Financial Services",
      "quantity": 532.0,
      "market_value": 9754.22,
      "cost_basis": 9990.96,
      "unrealized_pl": -236.74,
      "unrealized_plpc": -2.37
    },
    {
      "ticker": "BZ",
      "technical_score": 100.0,
      "fundamental_score": 95.0,
      "sentiment_score": 50.0,
      "research_composite_score": 88.0,
      "context": "holdings",
      "current_price": 14.0,
      "sector": "Communication Services",
      "quantity": 751.0,
      "market_value": 10536.53,
      "cost_basis": 9980.79,
      "unrealized_pl": 555.74,
      "unrealized_plpc": 5.568
    },
    {
      "ticker": "DOCN",
      "technical_score": 90.0,
      "fundamental_score": 46.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.4,
      "context": "holdings",
      "current_price": 152.18499755859375,
      "sector": "Technology",
      "quantity": 73.0,
      "market_value": 11149.655,
      "cost_basis": 7006.54,
      "unrealized_pl": 4143.115,
      "unrealized_plpc": 59.132
    },
    {
      "ticker": "EBAY",
      "technical_score": 90.0,
      "fundamental_score": 59.0,
      "sentiment_score": 50.0,
      "research_composite_score": 69.6,
      "context": "holdings",
      "current_price": 114.23500061035156,
      "sector": "Consumer Cyclical",
      "quantity": 70.0,
      "market_value": 8005.9,
      "cost_basis": 7565.6,
      "unrealized_pl": 440.3,
      "unrealized_plpc": 5.82
    },
    {
      "ticker": "FOXA",
      "technical_score": 100.0,
      "fundamental_score": 56.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.4,
      "context": "holdings",
      "current_price": 64.20999908447266,
      "sector": "Communication Services",
      "quantity": 151.0,
      "market_value": 9697.975,
      "cost_basis": 9975.06,
      "unrealized_pl": -277.085,
      "unrealized_plpc": -2.778
    },
    {
      "ticker": "GNTX",
      "technical_score": 45.0,
      "fundamental_score": 91.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.4,
      "context": "holdings",
      "current_price": 23.049999237060547,
      "sector": "Consumer Cyclical",
      "quantity": 343.0,
      "market_value": 7892.43,
      "cost_basis": 7501.41,
      "unrealized_pl": 391.02,
      "unrealized_plpc": 5.213
    },
    {
      "ticker": "HST",
      "technical_score": 45.0,
      "fundamental_score": 72.0,
      "sentiment_score": 50.0,
      "research_composite_score": 56.8,
      "context": "holdings",
      "current_price": 21.235000610351562,
      "sector": "Real Estate",
      "quantity": 328.0,
      "market_value": 6963.44,
      "cost_basis": 7245.52,
      "unrealized_pl": -282.08,
      "unrealized_plpc": -3.893
    },
    {
      "ticker": "IREN",
      "technical_score": 100.0,
      "fundamental_score": 30.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.0,
      "context": "holdings",
      "current_price": 53.62969970703125,
      "sector": "Financial Services",
      "quantity": 124.0,
      "market_value": 6669.96,
      "cost_basis": 7590.04,
      "unrealized_pl": -920.08,
      "unrealized_plpc": -12.122
    },
    {
      "ticker": "MAT",
      "technical_score": 85.0,
      "fundamental_score": 52.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 15.1899995803833,
      "sector": "Consumer Cyclical",
      "quantity": 660.0,
      "market_value": 10032.0,
      "cost_basis": 10005.6,
      "unrealized_pl": 26.4,
      "unrealized_plpc": 0.264
    }
  ],
  "screening": {
    "universe_size": 76,
    "candidates_found": 65,
    "holdings_count": 11,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
