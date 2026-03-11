---
from: RESEARCH
message_id: MSG_RESEARCH_20251209T160516Z_8eec3fd2
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2025-12-09T16:05:16.402350Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2025-12-09

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +0.16%
- **VIX**: 16.9 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 70 swing-suitable stocks
- **Current Holdings**: 15 positions from Alpaca
- **Total Scored**: 85 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **HALO** - Composite: 46.8/100
   - Technical: 20.0, Fundamental: 72.0
2. **WAY** - Composite: 44.4/100
   - Technical: 30.0, Fundamental: 56.0
3. **ADM** - Composite: 40.4/100
   - Technical: 30.0, Fundamental: 46.0
4. **AG** - Composite: 62.0/100
   - Technical: 90.0, Fundamental: 40.0
5. **ALAB** - Composite: 64.8/100
   - Technical: 85.0, Fundamental: 52.0

```json
{
  "market_conditions": {
    "spy_change_pct": 0.16163428475310937,
    "vix": 16.850000381469727,
    "vix_status": "NORMAL",
    "date": "2025-12-09"
  },
  "candidates": [
    {
      "ticker": "HALO",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 72.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 62.2400016784668
    },
    {
      "ticker": "WAY",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 56.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.400000000000006,
      "current_price": 31.510000228881836
    },
    {
      "ticker": "ADM",
      "technical": {
        "score": 30.0,
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
      "composite_score": 40.400000000000006,
      "current_price": 58.099998474121094
    },
    {
      "ticker": "AG",
      "technical": {
        "score": 90.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.0,
      "current_price": 15.385000228881836
    },
    {
      "ticker": "ALAB",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 52.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 64.8,
      "current_price": 175.74000549316406
    },
    {
      "ticker": "APG",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 44.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 55.6,
      "current_price": 38.564998626708984
    },
    {
      "ticker": "APH",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 65.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 64.0,
      "current_price": 140.05999755859375
    },
    {
      "ticker": "APTV",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.0,
      "current_price": 76.81500244140625
    },
    {
      "ticker": "ASTS",
      "technical": {
        "score": 75.0,
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
      "composite_score": 48.8,
      "current_price": 74.0
    },
    {
      "ticker": "AXTA",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 66.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.400000000000006,
      "current_price": 28.709999084472656
    },
    {
      "ticker": "BBWI",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 56.8,
      "current_price": 19.2450008392334
    },
    {
      "ticker": "BEAM",
      "technical": {
        "score": 85.0,
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
      "composite_score": 52.0,
      "current_price": 26.809999465942383
    },
    {
      "ticker": "BEKE",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.4,
      "current_price": 16.225000381469727
    },
    {
      "ticker": "BKR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 54.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.6,
      "current_price": 47.7130012512207
    },
    {
      "ticker": "BLSH",
      "technical": {
        "score": 85.0,
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
      "composite_score": 56.8,
      "current_price": 46.65999984741211
    },
    {
      "ticker": "BMRN",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 54.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.6,
      "current_price": 53.290000915527344
    },
    {
      "ticker": "BRO",
      "technical": {
        "score": 60.0,
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
      "composite_score": 56.400000000000006,
      "current_price": 77.63999938964844
    },
    {
      "ticker": "BTDR",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 17.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 12.0
    },
    {
      "ticker": "BWA",
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
      "current_price": 42.220001220703125
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
      "current_price": 53.189998626708984
    },
    {
      "ticker": "CF",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 80.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.0,
      "current_price": 77.33000183105469
    },
    {
      "ticker": "CHWY",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 28.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 55.2,
      "current_price": 34.619998931884766
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
        "score": 25.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 28.0,
      "current_price": 23.795000076293945
    },
    {
      "ticker": "CNM",
      "technical": {
        "score": 75.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 59.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 63.6,
      "current_price": 52.33000183105469
    },
    {
      "ticker": "CORZ",
      "technical": {
        "score": 75.0,
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
      "composite_score": 48.8,
      "current_price": 17.690000534057617
    },
    {
      "ticker": "CPNG",
      "technical": {
        "score": 60.0,
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
      "composite_score": 49.6,
      "current_price": 27.024999618530273
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 75.0,
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
      "composite_score": 57.6,
      "current_price": 30.459999084472656
    },
    {
      "ticker": "CRCL",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 16.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.4,
      "current_price": 83.95999908447266
    },
    {
      "ticker": "CRDO",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.8,
      "current_price": 178.94000244140625
    },
    {
      "ticker": "CRWV",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 12.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 86.23999786376953
    },
    {
      "ticker": "CSGP",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.8,
      "current_price": 66.625
    },
    {
      "ticker": "CVE",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 58.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 51.2,
      "current_price": 17.875
    },
    {
      "ticker": "CX",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 27.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.8,
      "current_price": 10.975000381469727
    },
    {
      "ticker": "DBX",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 53.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.2,
      "current_price": 29.28499984741211
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
        "score": 38.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 65.2,
      "current_price": 41.005001068115234
    },
    {
      "ticker": "DT",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 72.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.8,
      "current_price": 45.09000015258789
    },
    {
      "ticker": "DVN",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 53.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 71.2,
      "current_price": 37.425201416015625
    },
    {
      "ticker": "DYN",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 15.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.0,
      "current_price": 19.329999923706055
    },
    {
      "ticker": "ELAN",
      "technical": {
        "score": 30.0,
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
      "composite_score": 36.8,
      "current_price": 21.079999923706055
    },
    {
      "ticker": "EMN",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.0,
      "current_price": 61.380001068115234
    },
    {
      "ticker": "EOSE",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.6,
      "current_price": 15.430000305175781
    },
    {
      "ticker": "EQH",
      "technical": {
        "score": 85.0,
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
      "composite_score": 52.0,
      "current_price": 46.040000915527344
    },
    {
      "ticker": "EWY",
      "technical": {
        "score": 100.0,
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
      "composite_score": 62.0,
      "current_price": 95.06999969482422
    },
    {
      "ticker": "EXE",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 35.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.0,
      "current_price": 118.88999938964844
    },
    {
      "ticker": "FLNC",
      "technical": {
        "score": 90.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 7.0,
        "sector": "Utilities"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 23.3799991607666
    },
    {
      "ticker": "FLO",
      "technical": {
        "score": 60.0,
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
      "composite_score": 48.0,
      "current_price": 10.6850004196167
    },
    {
      "ticker": "FOXA",
      "technical": {
        "score": 90.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 70.0,
      "current_price": 69.43499755859375
    },
    {
      "ticker": "FRSH",
      "technical": {
        "score": 90.0,
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
      "composite_score": 56.8,
      "current_price": 13.079999923706055
    },
    {
      "ticker": "FTNT",
      "technical": {
        "score": 85.0,
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
      "composite_score": 62.400000000000006,
      "current_price": 83.52999877929688
    },
    {
      "ticker": "GLXY",
      "technical": {
        "score": 85.0,
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
      "composite_score": 56.4,
      "current_price": 28.68000030517578
    },
    {
      "ticker": "GNTX",
      "technical": {
        "score": 85.0,
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
      "composite_score": 75.2,
      "current_price": 23.094999313354492
    },
    {
      "ticker": "GPK",
      "technical": {
        "score": 30.0,
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
      "composite_score": 40.0,
      "current_price": 14.484999656677246
    },
    {
      "ticker": "GSK",
      "technical": {
        "score": 45.0,
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
      "composite_score": 47.2,
      "current_price": 47.474998474121094
    },
    {
      "ticker": "HRL",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 39.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 59.6,
      "current_price": 23.655000686645508
    },
    {
      "ticker": "HST",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 62.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 17.2450008392334
    },
    {
      "ticker": "HWM",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 65.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.0,
      "current_price": 193.27999877929688
    },
    {
      "ticker": "INCY",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 90.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 64.0,
      "current_price": 96.98999786376953
    },
    {
      "ticker": "IONQ",
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
      "current_price": 55.18009948730469
    },
    {
      "ticker": "IONS",
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
      "current_price": 79.20500183105469
    },
    {
      "ticker": "JBS",
      "technical": {
        "score": 75.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 59.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 63.6,
      "current_price": 13.979999542236328
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
        "score": 38.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.2,
      "current_price": 115.51499938964844
    },
    {
      "ticker": "JD",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 46.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.400000000000006,
      "current_price": 29.920000076293945
    },
    {
      "ticker": "KD",
      "technical": {
        "score": 75.0,
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
      "composite_score": 53.6,
      "current_price": 25.979999542236328
    },
    {
      "ticker": "LCID",
      "technical": {
        "score": 60.0,
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
      "composite_score": 45.6,
      "current_price": 12.760000228881836
    },
    {
      "ticker": "LI",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 17.175500869750977
    },
    {
      "ticker": "LKQ",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 46.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.400000000000006,
      "current_price": 28.639999389648438
    },
    {
      "ticker": "LMND",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 16.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.4,
      "current_price": 78.11000061035156
    },
    {
      "ticker": "LTH",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 58.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.2,
      "current_price": 25.65999984741211
    },
    {
      "ticker": "LYB",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 17.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 28.8,
      "current_price": 43.310001373291016
    },
    {
      "ticker": "LYV",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 56.8,
      "current_price": 139.18499755859375
    }
  ],
  "current_holdings": [
    {
      "ticker": "BZ",
      "technical_score": 60.0,
      "fundamental_score": 85.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 20.81049919128418,
      "sector": "Communication Services",
      "quantity": 241.0,
      "market_value": 5023.645,
      "cost_basis": 4957.37,
      "unrealized_pl": 66.275,
      "unrealized_plpc": 1.33689839572193
    },
    {
      "ticker": "CLSK",
      "technical_score": 85.0,
      "fundamental_score": 72.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.8,
      "context": "holdings",
      "current_price": 13.890000343322754,
      "sector": "Financial Services",
      "quantity": 202.0,
      "market_value": 3073.43,
      "cost_basis": 3058.28,
      "unrealized_pl": 15.15,
      "unrealized_plpc": 0.49537648612946
    },
    {
      "ticker": "CWAN",
      "technical_score": 100.0,
      "fundamental_score": 64.0,
      "sentiment_score": 50.0,
      "research_composite_score": 75.6,
      "context": "holdings",
      "current_price": 21.954999923706055,
      "sector": "Technology",
      "quantity": 1151.0,
      "market_value": 25275.96,
      "cost_basis": 22559.6,
      "unrealized_pl": 2716.36,
      "unrealized_plpc": 12.04081632653061
    },
    {
      "ticker": "DNOW",
      "technical_score": 75.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 14.029999732971191,
      "sector": "Industrials",
      "quantity": 370.0,
      "market_value": 5187.4,
      "cost_basis": 4987.6,
      "unrealized_pl": 199.8,
      "unrealized_plpc": 4.00593471810089
    },
    {
      "ticker": "FTI",
      "technical_score": 70.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 60.8,
      "context": "holdings",
      "current_price": 45.93000030517578,
      "sector": "Energy",
      "quantity": 175.0,
      "market_value": 8041.25,
      "cost_basis": 7595.0,
      "unrealized_pl": 446.25,
      "unrealized_plpc": 5.875576036866359
    },
    {
      "ticker": "GEHC",
      "technical_score": 90.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 67.2,
      "context": "holdings",
      "current_price": 82.79000091552734,
      "sector": "Healthcare",
      "quantity": 60.0,
      "market_value": 4966.8,
      "cost_basis": 4908.0,
      "unrealized_pl": 58.8,
      "unrealized_plpc": 1.19804400977995
    },
    {
      "ticker": "GEO",
      "technical_score": 75.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 16.521299362182617,
      "sector": "Industrials",
      "quantity": 319.0,
      "market_value": 5269.88,
      "cost_basis": 4973.27,
      "unrealized_pl": 296.61,
      "unrealized_plpc": 5.96408399302672
    },
    {
      "ticker": "GPN",
      "technical_score": 75.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 78.12999725341797,
      "sector": "Industrials",
      "quantity": 64.0,
      "market_value": 4998.4,
      "cost_basis": 4960.0,
      "unrealized_pl": 38.4,
      "unrealized_plpc": 0.7741935483871
    },
    {
      "ticker": "HAYW",
      "technical_score": 45.0,
      "fundamental_score": 62.0,
      "sentiment_score": 50.0,
      "research_composite_score": 52.8,
      "context": "holdings",
      "current_price": 15.78499984741211,
      "sector": "Industrials",
      "quantity": 311.0,
      "market_value": 4906.025,
      "cost_basis": 5007.1,
      "unrealized_pl": -101.075,
      "unrealized_plpc": -2.01863354037267
    },
    {
      "ticker": "HL",
      "technical_score": 100.0,
      "fundamental_score": 60.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.0,
      "context": "holdings",
      "current_price": 15.850000381469727,
      "sector": "Basic Materials",
      "quantity": 255.0,
      "market_value": 4301.8245,
      "cost_basis": 3972.9,
      "unrealized_pl": 328.9245,
      "unrealized_plpc": 8.27920410783055
    },
    {
      "ticker": "HSAI",
      "technical_score": 85.0,
      "fundamental_score": 52.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 19.889999389648438,
      "sector": "Consumer Cyclical",
      "quantity": 254.0,
      "market_value": 5059.68,
      "cost_basis": 5003.8,
      "unrealized_pl": 55.88,
      "unrealized_plpc": 1.11675126903553
    },
    {
      "ticker": "IPG",
      "technical_score": 60.0,
      "fundamental_score": 55.0,
      "sentiment_score": 50.0,
      "research_composite_score": 56.0,
      "context": "holdings",
      "current_price": 24.56999969482422,
      "sector": "Communication Services",
      "quantity": 151.0,
      "market_value": 3710.07,
      "cost_basis": 3815.77,
      "unrealized_pl": -105.7,
      "unrealized_plpc": -2.7700831024930697
    },
    {
      "ticker": "IVZ",
      "technical_score": 80.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.4,
      "context": "holdings",
      "current_price": 26.530000686645508,
      "sector": "Financial Services",
      "quantity": 125.0,
      "market_value": 3310.0,
      "cost_basis": 3071.25,
      "unrealized_pl": 238.75,
      "unrealized_plpc": 7.773707773707771
    },
    {
      "ticker": "KDP",
      "technical_score": 100.0,
      "fundamental_score": 48.0,
      "sentiment_score": 50.0,
      "research_composite_score": 69.2,
      "context": "holdings",
      "current_price": 28.979999542236328,
      "sector": "Consumer Defensive",
      "quantity": 175.0,
      "market_value": 5063.625,
      "cost_basis": 4975.25,
      "unrealized_pl": 88.375,
      "unrealized_plpc": 1.7762926486106199
    },
    {
      "ticker": "MNST",
      "technical_score": 70.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 73.3550033569336,
      "sector": "Consumer Defensive",
      "quantity": 83.0,
      "market_value": 6083.9,
      "cost_basis": 5965.3,
      "unrealized_pl": 118.6,
      "unrealized_plpc": 1.98816488692941
    }
  ],
  "screening": {
    "universe_size": 85,
    "candidates_found": 70,
    "holdings_count": 15,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
