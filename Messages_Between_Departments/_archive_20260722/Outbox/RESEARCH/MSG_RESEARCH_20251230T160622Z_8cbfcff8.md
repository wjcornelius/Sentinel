---
from: RESEARCH
message_id: MSG_RESEARCH_20251230T160622Z_8cbfcff8
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2025-12-30T16:06:22.443848Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2025-12-30

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +0.00%
- **VIX**: 14.2 (LOW)

### Candidate Summary
- **Buy Candidates**: 71 swing-suitable stocks
- **Current Holdings**: 14 positions from Alpaca
- **Total Scored**: 85 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **CPNG** - Composite: 49.6/100
   - Technical: 60.0, Fundamental: 39.0
2. **ACI** - Composite: 54.8/100
   - Technical: 60.0, Fundamental: 52.0
3. **ADM** - Composite: 40.4/100
   - Technical: 30.0, Fundamental: 46.0
4. **ALAB** - Composite: 64.8/100
   - Technical: 85.0, Fundamental: 52.0
5. **ALHC** - Composite: 35.6/100
   - Technical: 45.0, Fundamental: 19.0

```json
{
  "market_conditions": {
    "spy_change_pct": 0.0029104502377697017,
    "vix": 14.229999542236328,
    "vix_status": "LOW",
    "date": "2025-12-30"
  },
  "candidates": [
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
      "current_price": 23.809999465942383
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
        "score": 52.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.8,
      "current_price": 17.334999084472656
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
      "current_price": 58.20000076293945
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
      "current_price": 173.36680603027344
    },
    {
      "ticker": "ALHC",
      "technical": {
        "score": 45.0,
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
      "composite_score": 35.6,
      "current_price": 19.084999084472656
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
      "current_price": 39.20000076293945
    },
    {
      "ticker": "APO",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 72.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.8,
      "current_price": 147.75
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
      "current_price": 76.88999938964844
    },
    {
      "ticker": "ARES",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 51.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.400000000000006,
      "current_price": 165.19000244140625
    },
    {
      "ticker": "BEKE",
      "technical": {
        "score": 30.0,
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
      "composite_score": 34.4,
      "current_price": 15.954999923706055
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
      "current_price": 45.814998626708984
    },
    {
      "ticker": "BMNR",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 28.840900421142578
    },
    {
      "ticker": "BRBR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 55.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.0,
      "current_price": 26.639999389648438
    },
    {
      "ticker": "BRO",
      "technical": {
        "score": 85.0,
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
      "composite_score": 66.4,
      "current_price": 80.38999938964844
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
      "current_price": 11.149999618530273
    },
    {
      "ticker": "CADE",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.8,
      "current_price": 43.21500015258789
    },
    {
      "ticker": "CF",
      "technical": {
        "score": 60.0,
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
      "composite_score": 66.0,
      "current_price": 77.16999816894531
    },
    {
      "ticker": "CHWY",
      "technical": {
        "score": 60.0,
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
      "composite_score": 50.400000000000006,
      "current_price": 33.18000030517578
    },
    {
      "ticker": "CNM",
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
      "current_price": 53.095001220703125
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
        "score": 53.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 49.2,
      "current_price": 28.184999465942383
    },
    {
      "ticker": "CORZ",
      "technical": {
        "score": 30.0,
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
      "composite_score": 30.8,
      "current_price": 14.9350004196167
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 45.0,
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
      "composite_score": 45.6,
      "current_price": 30.274999618530273
    },
    {
      "ticker": "CRCL",
      "technical": {
        "score": 60.0,
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
      "composite_score": 40.4,
      "current_price": 81.48999786376953
    },
    {
      "ticker": "CRWV",
      "technical": {
        "score": 60.0,
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
      "composite_score": 38.8,
      "current_price": 75.24739837646484
    },
    {
      "ticker": "CSGP",
      "technical": {
        "score": 85.0,
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
      "composite_score": 56.8,
      "current_price": 67.41000366210938
    },
    {
      "ticker": "CVE",
      "technical": {
        "score": 30.0,
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
      "composite_score": 45.2,
      "current_price": 17.06999969482422
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
      "current_price": 11.744999885559082
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
      "current_price": 27.780000686645508
    },
    {
      "ticker": "DD",
      "technical": {
        "score": 70.0,
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
      "composite_score": 53.2,
      "current_price": 40.779998779296875
    },
    {
      "ticker": "DEI",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 15.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 11.140000343322754
    },
    {
      "ticker": "DVN",
      "technical": {
        "score": 45.0,
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
      "composite_score": 49.2,
      "current_price": 36.65999984741211
    },
    {
      "ticker": "EMN",
      "technical": {
        "score": 70.0,
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
      "composite_score": 56.0,
      "current_price": 63.549198150634766
    },
    {
      "ticker": "EMR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 49.6,
      "current_price": 135.49000549316406
    },
    {
      "ticker": "EQH",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.0,
      "current_price": 48.130001068115234
    },
    {
      "ticker": "EQT",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 52.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.8,
      "current_price": 54.599998474121094
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
      "current_price": 98.71499633789062
    },
    {
      "ticker": "FLG",
      "technical": {
        "score": 45.0,
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
      "composite_score": 38.8,
      "current_price": 12.720000267028809
    },
    {
      "ticker": "FLO",
      "technical": {
        "score": 85.0,
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
      "composite_score": 58.0,
      "current_price": 10.994999885559082
    },
    {
      "ticker": "FRSH",
      "technical": {
        "score": 45.0,
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
      "composite_score": 38.8,
      "current_price": 12.404999732971191
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
        "score": 57.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.8,
      "current_price": 44.90999984741211
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
      "current_price": 80.81999969482422
    },
    {
      "ticker": "GEHC",
      "technical": {
        "score": 70.0,
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
      "composite_score": 59.2,
      "current_price": 83.44000244140625
    },
    {
      "ticker": "GLXY",
      "technical": {
        "score": 50.0,
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
      "composite_score": 42.4,
      "current_price": 23.170000076293945
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
        "score": 54.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.6,
      "current_price": 20.604999542236328
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
      "current_price": 23.66510009765625
    },
    {
      "ticker": "GPN",
      "technical": {
        "score": 45.0,
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
      "composite_score": 50.8,
      "current_price": 79.19999694824219
    },
    {
      "ticker": "HL",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 55.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.0,
      "current_price": 19.575000762939453
    },
    {
      "ticker": "HST",
      "technical": {
        "score": 70.0,
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
      "composite_score": 62.8,
      "current_price": 18.28499984741211
    },
    {
      "ticker": "INCY",
      "technical": {
        "score": 30.0,
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
      "composite_score": 58.0,
      "current_price": 98.20010375976562
    },
    {
      "ticker": "IONQ",
      "technical": {
        "score": 30.0,
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
      "composite_score": 32.8,
      "current_price": 46.459999084472656
    },
    {
      "ticker": "IONS",
      "technical": {
        "score": 45.0,
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
      "composite_score": 36.8,
      "current_price": 78.87000274658203
    },
    {
      "ticker": "IR",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 49.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 69.6,
      "current_price": 80.61000061035156
    },
    {
      "ticker": "IREN",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 62.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.8,
      "current_price": 39.349998474121094
    },
    {
      "ticker": "JD",
      "technical": {
        "score": 60.0,
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
      "composite_score": 52.400000000000006,
      "current_price": 28.71500015258789
    },
    {
      "ticker": "JOBY",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.8,
      "current_price": 13.500100135803223
    },
    {
      "ticker": "KD",
      "technical": {
        "score": 100.0,
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
      "composite_score": 63.6,
      "current_price": 26.889999389648438
    },
    {
      "ticker": "KDP",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 48.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 28.174999237060547
    },
    {
      "ticker": "KKR",
      "technical": {
        "score": 45.0,
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
      "composite_score": 49.2,
      "current_price": 129.6750030517578
    },
    {
      "ticker": "KMB",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 101.19000244140625
    },
    {
      "ticker": "LI",
      "technical": {
        "score": 85.0,
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
      "composite_score": 58.8,
      "current_price": 17.434999465942383
    },
    {
      "ticker": "LKQ",
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
      "current_price": 30.514999389648438
    },
    {
      "ticker": "LMND",
      "technical": {
        "score": 45.0,
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
      "composite_score": 34.4,
      "current_price": 72.4749984741211
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
      "current_price": 144.30999755859375
    },
    {
      "ticker": "MGM",
      "technical": {
        "score": 70.0,
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
      "composite_score": 49.2,
      "current_price": 37.040000915527344
    },
    {
      "ticker": "MGY",
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
      "current_price": 22.18000030517578
    },
    {
      "ticker": "MMM",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 42.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.8,
      "current_price": 161.03750610351562
    },
    {
      "ticker": "MSTR",
      "technical": {
        "score": 50.0,
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
      "composite_score": 52.8,
      "current_price": 155.38999938964844
    },
    {
      "ticker": "NBIS",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 86.47000122070312
    },
    {
      "ticker": "NU",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.0,
      "current_price": 16.895000457763672
    },
    {
      "ticker": "NVST",
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
      "current_price": 21.94499969482422
    },
    {
      "ticker": "OKLO",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 25.0,
        "sector": "Utilities"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 28.0,
      "current_price": 73.51490020751953
    }
  ],
  "current_holdings": [
    {
      "ticker": "AG",
      "technical_score": 70.0,
      "fundamental_score": 35.0,
      "sentiment_score": 50.0,
      "research_composite_score": 52.0,
      "context": "holdings",
      "current_price": 16.990100860595703,
      "sector": "Basic Materials",
      "quantity": 308.0,
      "market_value": 5251.8928,
      "cost_basis": 4949.56,
      "unrealized_pl": 302.3328,
      "unrealized_plpc": 6.10827629122589
    },
    {
      "ticker": "BX",
      "technical_score": 100.0,
      "fundamental_score": 34.0,
      "sentiment_score": 50.0,
      "research_composite_score": 63.6,
      "context": "holdings",
      "current_price": 155.38999938964844,
      "sector": "Financial Services",
      "quantity": 32.0,
      "market_value": 4970.24,
      "cost_basis": 4964.48,
      "unrealized_pl": 5.76,
      "unrealized_plpc": 0.11602423617378
    },
    {
      "ticker": "CARR",
      "technical_score": 85.0,
      "fundamental_score": 33.0,
      "sentiment_score": 50.0,
      "research_composite_score": 57.2,
      "context": "holdings",
      "current_price": 53.5099983215332,
      "sector": "Industrials",
      "quantity": 93.0,
      "market_value": 4976.43,
      "cost_basis": 4986.66,
      "unrealized_pl": -10.23,
      "unrealized_plpc": -0.20514733308467
    },
    {
      "ticker": "CART",
      "technical_score": 70.0,
      "fundamental_score": 76.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.4,
      "context": "holdings",
      "current_price": 45.2599983215332,
      "sector": "Consumer Cyclical",
      "quantity": 110.0,
      "market_value": 4979.7,
      "cost_basis": 4980.8,
      "unrealized_pl": -1.1,
      "unrealized_plpc": -0.022084805653710002
    },
    {
      "ticker": "CDE",
      "technical_score": 100.0,
      "fundamental_score": 72.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.8,
      "context": "holdings",
      "current_price": 18.295000076293945,
      "sector": "Basic Materials",
      "quantity": 295.0,
      "market_value": 5414.725,
      "cost_basis": 4912.23,
      "unrealized_pl": 502.495,
      "unrealized_plpc": 10.22946808272414
    },
    {
      "ticker": "CG",
      "technical_score": 100.0,
      "fundamental_score": 37.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 60.399898529052734,
      "sector": "Financial Services",
      "quantity": 82.0,
      "market_value": 4950.34,
      "cost_basis": 4979.86,
      "unrealized_pl": -29.52,
      "unrealized_plpc": -0.59278774905319
    },
    {
      "ticker": "CWAN",
      "technical_score": 80.0,
      "fundamental_score": 64.0,
      "sentiment_score": 50.0,
      "research_composite_score": 67.6,
      "context": "holdings",
      "current_price": 24.094999313354492,
      "sector": "Technology",
      "quantity": 1151.0,
      "market_value": 27727.59,
      "cost_basis": 22559.6,
      "unrealized_pl": 5167.99,
      "unrealized_plpc": 22.90816326530612
    },
    {
      "ticker": "DT",
      "technical_score": 60.0,
      "fundamental_score": 72.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 44.220001220703125,
      "sector": "Technology",
      "quantity": 109.0,
      "market_value": 4817.8,
      "cost_basis": 4970.4,
      "unrealized_pl": -152.6,
      "unrealized_plpc": -3.07017543859649
    },
    {
      "ticker": "HRL",
      "technical_score": 70.0,
      "fundamental_score": 39.0,
      "sentiment_score": 50.0,
      "research_composite_score": 53.6,
      "context": "holdings",
      "current_price": 23.989999771118164,
      "sector": "Consumer Defensive",
      "quantity": 158.0,
      "market_value": 3792.79,
      "cost_basis": 3790.42,
      "unrealized_pl": 2.37,
      "unrealized_plpc": 0.06252605252188
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
      "technical_score": 70.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.400000000000006,
      "context": "holdings",
      "current_price": 26.690000534057617,
      "sector": "Financial Services",
      "quantity": 125.0,
      "market_value": 3338.75,
      "cost_basis": 3071.25,
      "unrealized_pl": 267.5,
      "unrealized_plpc": 8.70980870980871
    },
    {
      "ticker": "JBS",
      "technical_score": 70.0,
      "fundamental_score": 59.0,
      "sentiment_score": 50.0,
      "research_composite_score": 61.6,
      "context": "holdings",
      "current_price": 14.470000267028809,
      "sector": "Consumer Defensive",
      "quantity": 344.0,
      "market_value": 4975.96,
      "cost_basis": 4988.0,
      "unrealized_pl": -12.04,
      "unrealized_plpc": -0.24137931034482998
    },
    {
      "ticker": "JCI",
      "technical_score": 100.0,
      "fundamental_score": 38.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 121.51000213623047,
      "sector": "Industrials",
      "quantity": 31.0,
      "market_value": 3768.67,
      "cost_basis": 3612.12,
      "unrealized_pl": 156.55,
      "unrealized_plpc": 4.3340199107449395
    },
    {
      "ticker": "MAS",
      "technical_score": 100.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 76.4,
      "context": "holdings",
      "current_price": 64.27999877929688,
      "sector": "Industrials",
      "quantity": 77.0,
      "market_value": 4950.33,
      "cost_basis": 4964.19,
      "unrealized_pl": -13.86,
      "unrealized_plpc": -0.27919962773383
    }
  ],
  "screening": {
    "universe_size": 85,
    "candidates_found": 71,
    "holdings_count": 14,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
