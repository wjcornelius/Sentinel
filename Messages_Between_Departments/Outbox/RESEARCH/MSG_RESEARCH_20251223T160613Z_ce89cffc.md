---
from: RESEARCH
message_id: MSG_RESEARCH_20251223T160613Z_ce89cffc
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2025-12-23T16:06:13.064203Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2025-12-23

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +0.24%
- **VIX**: 13.7 (LOW)

### Candidate Summary
- **Buy Candidates**: 70 swing-suitable stocks
- **Current Holdings**: 14 positions from Alpaca
- **Total Scored**: 84 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **CHWY** - Composite: 38.4/100
   - Technical: 30.0, Fundamental: 41.0
2. **ADM** - Composite: 40.4/100
   - Technical: 30.0, Fundamental: 46.0
3. **ALAB** - Composite: 64.8/100
   - Technical: 85.0, Fundamental: 52.0
4. **APG** - Composite: 55.6/100
   - Technical: 70.0, Fundamental: 44.0
5. **APTV** - Composite: 46.0/100
   - Technical: 60.0, Fundamental: 30.0

```json
{
  "market_conditions": {
    "spy_change_pct": 0.24385363790750958,
    "vix": 13.729999542236328,
    "vix_status": "LOW",
    "date": "2025-12-23"
  },
  "candidates": [
    {
      "ticker": "CHWY",
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
      "current_price": 31.8799991607666
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
      "current_price": 57.665000915527344
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
      "current_price": 167.22999572753906
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
      "current_price": 39.17499923706055
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
      "current_price": 76.26000213623047
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
      "current_price": 15.9350004196167
    },
    {
      "ticker": "BKR",
      "technical": {
        "score": 20.0,
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
      "composite_score": 39.6,
      "current_price": 45.26499938964844
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
      "current_price": 79.64520263671875
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
      "current_price": 11.100000381469727
    },
    {
      "ticker": "BWA",
      "technical": {
        "score": 100.0,
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
      "composite_score": 61.6,
      "current_price": 45.32500076293945
    },
    {
      "ticker": "BX",
      "technical": {
        "score": 100.0,
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
      "composite_score": 63.6,
      "current_price": 156.2050018310547
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
      "current_price": 53.01499938964844
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
      "current_price": 78.33999633789062
    },
    {
      "ticker": "CMCSA",
      "technical": {
        "score": 85.0,
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
      "composite_score": 60.0,
      "current_price": 29.145000457763672
    },
    {
      "ticker": "CNM",
      "technical": {
        "score": 100.0,
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
      "composite_score": 68.4,
      "current_price": 53.560001373291016
    },
    {
      "ticker": "COHR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 48.8,
      "current_price": 191.33999633789062
    },
    {
      "ticker": "COLB",
      "technical": {
        "score": 70.0,
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
      "composite_score": 59.2,
      "current_price": 28.799999237060547
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
      "current_price": 15.6850004196167
    },
    {
      "ticker": "CPNG",
      "technical": {
        "score": 10.0,
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
      "composite_score": 29.6,
      "current_price": 22.44499969482422
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 100.0,
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
      "composite_score": 67.6,
      "current_price": 30.71500015258789
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
      "current_price": 81.89800262451172
    },
    {
      "ticker": "CRDO",
      "technical": {
        "score": 20.0,
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
      "composite_score": 40.8,
      "current_price": 148.875
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
      "current_price": 66.19000244140625
    },
    {
      "ticker": "CVE",
      "technical": {
        "score": 20.0,
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
      "composite_score": 41.2,
      "current_price": 16.594999313354492
    },
    {
      "ticker": "DBRG",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 25.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.0,
      "current_price": 12.920000076293945
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
      "current_price": 28.260000228881836
    },
    {
      "ticker": "DEI",
      "technical": {
        "score": 10.0,
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
      "composite_score": 20.0,
      "current_price": 11.069999694824219
    },
    {
      "ticker": "DJT",
      "technical": {
        "score": 85.0,
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
      "composite_score": 52.0,
      "current_price": 14.479999542236328
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
      "current_price": 36.185001373291016
    },
    {
      "ticker": "DYN",
      "technical": {
        "score": 70.0,
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
      "composite_score": 44.0,
      "current_price": 20.649999618530273
    },
    {
      "ticker": "ELAN",
      "technical": {
        "score": 75.0,
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
      "composite_score": 54.8,
      "current_price": 22.03499984741211
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
      "current_price": 135.82000732421875
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
      "current_price": 92.19999694824219
    },
    {
      "ticker": "EXE",
      "technical": {
        "score": 20.0,
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
      "composite_score": 32.0,
      "current_price": 109.30999755859375
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
      "current_price": 63.560001373291016
    },
    {
      "ticker": "FLG",
      "technical": {
        "score": 70.0,
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
      "composite_score": 48.8,
      "current_price": 12.854999542236328
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
      "current_price": 10.725000381469727
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
      "current_price": 12.244999885559082
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
      "current_price": 44.93000030517578
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
      "current_price": 80.37999725341797
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
      "current_price": 83.6500015258789
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
      "current_price": 89.0
    },
    {
      "ticker": "GLXY",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.4,
      "current_price": 24.56999969482422
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
      "current_price": 21.380599975585938
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
      "current_price": 23.375
    },
    {
      "ticker": "GPN",
      "technical": {
        "score": 85.0,
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
      "composite_score": 66.8,
      "current_price": 79.96499633789062
    },
    {
      "ticker": "GSK",
      "technical": {
        "score": 70.0,
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
      "composite_score": 57.2,
      "current_price": 48.86000061035156
    },
    {
      "ticker": "HALO",
      "technical": {
        "score": 85.0,
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
      "composite_score": 72.8,
      "current_price": 68.57499694824219
    },
    {
      "ticker": "HST",
      "technical": {
        "score": 100.0,
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
      "composite_score": 74.8,
      "current_price": 18.479999542236328
    },
    {
      "ticker": "INCY",
      "technical": {
        "score": 100.0,
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
      "composite_score": 86.0,
      "current_price": 100.8499984741211
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
      "current_price": 53.121299743652344
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
      "current_price": 79.79000091552734
    },
    {
      "ticker": "IOT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 19.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 29.6,
      "current_price": 37.09000015258789
    },
    {
      "ticker": "IR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 57.6,
      "current_price": 80.80999755859375
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
      "current_price": 42.20000076293945
    },
    {
      "ticker": "JBS",
      "technical": {
        "score": 70.0,
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
      "composite_score": 61.6,
      "current_price": 14.479999542236328
    },
    {
      "ticker": "JD",
      "technical": {
        "score": 50.0,
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
      "composite_score": 48.400000000000006,
      "current_price": 28.815000534057617
    },
    {
      "ticker": "JOBY",
      "technical": {
        "score": 60.0,
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
      "composite_score": 42.8,
      "current_price": 14.426400184631348
    },
    {
      "ticker": "KD",
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
      "current_price": 26.8700008392334
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
      "current_price": 28.104999542236328
    },
    {
      "ticker": "KKR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 59.2,
      "current_price": 130.80999755859375
    },
    {
      "ticker": "KMB",
      "technical": {
        "score": 20.0,
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
      "composite_score": 32.8,
      "current_price": 100.04000091552734
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
      "current_price": 11.800000190734863
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
      "current_price": 16.584999084472656
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
      "current_price": 80.41000366210938
    },
    {
      "ticker": "LTH",
      "technical": {
        "score": 100.0,
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
      "composite_score": 73.2,
      "current_price": 26.690000534057617
    },
    {
      "ticker": "MGM",
      "technical": {
        "score": 100.0,
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
      "composite_score": 61.2,
      "current_price": 37.279998779296875
    },
    {
      "ticker": "MGY",
      "technical": {
        "score": 20.0,
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
      "composite_score": 39.6,
      "current_price": 21.854999542236328
    },
    {
      "ticker": "MMM",
      "technical": {
        "score": 20.0,
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
      "composite_score": 34.8,
      "current_price": 159.0800018310547
    },
    {
      "ticker": "MSTR",
      "technical": {
        "score": 60.0,
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
      "composite_score": 56.8,
      "current_price": 159.64999389648438
    }
  ],
  "current_holdings": [
    {
      "ticker": "AG",
      "technical_score": 100.0,
      "fundamental_score": 35.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 16.939199447631836,
      "sector": "Basic Materials",
      "quantity": 308.0,
      "market_value": 5229.84,
      "cost_basis": 4949.56,
      "unrealized_pl": 280.28,
      "unrealized_plpc": 5.6627255756067205
    },
    {
      "ticker": "CDE",
      "technical_score": 85.0,
      "fundamental_score": 72.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.8,
      "context": "holdings",
      "current_price": 18.514999389648438,
      "sector": "Basic Materials",
      "quantity": 295.0,
      "market_value": 5472.25,
      "cost_basis": 4912.23,
      "unrealized_pl": 560.02,
      "unrealized_plpc": 11.40052481255967
    },
    {
      "ticker": "CWAN",
      "technical_score": 90.0,
      "fundamental_score": 64.0,
      "sentiment_score": 50.0,
      "research_composite_score": 71.6,
      "context": "holdings",
      "current_price": 24.094999313354492,
      "sector": "Technology",
      "quantity": 1151.0,
      "market_value": 27733.345,
      "cost_basis": 22559.6,
      "unrealized_pl": 5173.745,
      "unrealized_plpc": 22.93367346938776
    },
    {
      "ticker": "DT",
      "technical_score": 60.0,
      "fundamental_score": 72.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 43.755001068115234,
      "sector": "Technology",
      "quantity": 109.0,
      "market_value": 4775.29,
      "cost_basis": 4970.4,
      "unrealized_pl": -195.11,
      "unrealized_plpc": -3.92543859649123
    },
    {
      "ticker": "GEO",
      "technical_score": 45.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 56.0,
      "context": "holdings",
      "current_price": 16.3799991607666,
      "sector": "Industrials",
      "quantity": 319.0,
      "market_value": 5244.36,
      "cost_basis": 4973.27,
      "unrealized_pl": 271.09,
      "unrealized_plpc": 5.45094072913797
    },
    {
      "ticker": "HL",
      "technical_score": 100.0,
      "fundamental_score": 55.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 20.125499725341797,
      "sector": "Basic Materials",
      "quantity": 255.0,
      "market_value": 5131.9515,
      "cost_basis": 3972.9,
      "unrealized_pl": 1159.0515,
      "unrealized_plpc": 29.173940949935822
    },
    {
      "ticker": "HRL",
      "technical_score": 100.0,
      "fundamental_score": 39.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.6,
      "context": "holdings",
      "current_price": 23.950000762939453,
      "sector": "Consumer Defensive",
      "quantity": 158.0,
      "market_value": 3784.89,
      "cost_basis": 3790.42,
      "unrealized_pl": -5.53,
      "unrealized_plpc": -0.14589412255106002
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
      "technical_score": 90.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.4,
      "context": "holdings",
      "current_price": 27.174999237060547,
      "sector": "Financial Services",
      "quantity": 125.0,
      "market_value": 3401.875,
      "cost_basis": 3071.25,
      "unrealized_pl": 330.625,
      "unrealized_plpc": 10.76516076516077
    },
    {
      "ticker": "JCI",
      "technical_score": 100.0,
      "fundamental_score": 38.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 120.1500015258789,
      "sector": "Industrials",
      "quantity": 31.0,
      "market_value": 3729.145,
      "cost_basis": 3612.12,
      "unrealized_pl": 117.025,
      "unrealized_plpc": 3.2397871610023996
    },
    {
      "ticker": "LKQ",
      "technical_score": 60.0,
      "fundamental_score": 46.0,
      "sentiment_score": 50.0,
      "research_composite_score": 52.400000000000006,
      "context": "holdings",
      "current_price": 29.489999771118164,
      "sector": "Consumer Cyclical",
      "quantity": 160.0,
      "market_value": 4730.4,
      "cost_basis": 4988.8,
      "unrealized_pl": -258.4,
      "unrealized_plpc": -5.17960230917255
    },
    {
      "ticker": "MAS",
      "technical_score": 60.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 60.400000000000006,
      "context": "holdings",
      "current_price": 63.60499954223633,
      "sector": "Industrials",
      "quantity": 77.0,
      "market_value": 4901.82,
      "cost_basis": 4964.19,
      "unrealized_pl": -62.37,
      "unrealized_plpc": -1.25639832480223
    },
    {
      "ticker": "NVST",
      "technical_score": 100.0,
      "fundamental_score": 37.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 21.780000686645508,
      "sector": "Healthcare",
      "quantity": 229.0,
      "market_value": 4996.78,
      "cost_basis": 4980.75,
      "unrealized_pl": 16.03,
      "unrealized_plpc": 0.32183908045977
    },
    {
      "ticker": "ONB",
      "technical_score": 100.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.4,
      "context": "holdings",
      "current_price": 23.020000457763672,
      "sector": "Financial Services",
      "quantity": 218.0,
      "market_value": 5027.08,
      "cost_basis": 5040.16,
      "unrealized_pl": -13.08,
      "unrealized_plpc": -0.25951557093426
    }
  ],
  "screening": {
    "universe_size": 84,
    "candidates_found": 70,
    "holdings_count": 14,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
