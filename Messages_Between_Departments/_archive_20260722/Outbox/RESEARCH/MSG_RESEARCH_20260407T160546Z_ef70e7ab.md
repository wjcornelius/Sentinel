---
from: RESEARCH
message_id: MSG_RESEARCH_20260407T160546Z_ef70e7ab
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-04-07T16:05:46.132730Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-04-07

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -0.56%
- **VIX**: 26.6 (ELEVATED)

### Candidate Summary
- **Buy Candidates**: 68 swing-suitable stocks
- **Current Holdings**: 9 positions from Alpaca
- **Total Scored**: 77 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **CNM** - Composite: 64.4/100
   - Technical: 85.0, Fundamental: 51.0
2. **EQT** - Composite: 48.0/100
   - Technical: 30.0, Fundamental: 65.0
3. **INDV** - Composite: 60.0/100
   - Technical: 60.0, Fundamental: 65.0
4. **ACI** - Composite: 59.6/100
   - Technical: 85.0, Fundamental: 39.0
5. **ADM** - Composite: 57.6/100
   - Technical: 100.0, Fundamental: 19.0

```json
{
  "market_conditions": {
    "spy_change_pct": -0.5615182565914534,
    "vix": 26.6200008392334,
    "vix_status": "ELEVATED",
    "date": "2026-04-07"
  },
  "candidates": [
    {
      "ticker": "CNM",
      "technical": {
        "score": 85.0,
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
      "composite_score": 64.4,
      "current_price": 50.08000183105469
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
        "score": 65.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.0,
      "current_price": 60.2599983215332
    },
    {
      "ticker": "INDV",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 65.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.0,
      "current_price": 30.190000534057617
    },
    {
      "ticker": "ACI",
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
      "current_price": 18.09000015258789
    },
    {
      "ticker": "ADM",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 19.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.6,
      "current_price": 72.23500061035156
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
        "score": 43.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 51.2,
      "current_price": 21.065000534057617
    },
    {
      "ticker": "ALAB",
      "technical": {
        "score": 60.0,
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
      "composite_score": 60.0,
      "current_price": 117.5
    },
    {
      "ticker": "AMKR",
      "technical": {
        "score": 85.0,
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
      "composite_score": 67.2,
      "current_price": 47.15999984741211
    },
    {
      "ticker": "APG",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 24.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.6,
      "current_price": 42.22999954223633
    },
    {
      "ticker": "APLD",
      "technical": {
        "score": 60.0,
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
      "composite_score": 44.8,
      "current_price": 25.09000015258789
    },
    {
      "ticker": "ARE",
      "technical": {
        "score": 30.0,
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
      "composite_score": 28.8,
      "current_price": 43.690799713134766
    },
    {
      "ticker": "ARM",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 47.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 68.8,
      "current_price": 141.52999877929688
    },
    {
      "ticker": "AXTA",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 53.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 55.2,
      "current_price": 26.170000076293945
    },
    {
      "ticker": "BBWI",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.8,
      "current_price": 17.5
    },
    {
      "ticker": "BBY",
      "technical": {
        "score": 85.0,
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
      "composite_score": 64.8,
      "current_price": 63.70500183105469
    },
    {
      "ticker": "BDX",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 49.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.6,
      "current_price": 154.4199981689453
    },
    {
      "ticker": "BMNR",
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
      "current_price": 19.760000228881836
    },
    {
      "ticker": "BMRN",
      "technical": {
        "score": 60.0,
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
      "composite_score": 53.2,
      "current_price": 55.95500183105469
    },
    {
      "ticker": "BRBR",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 47.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 15.734999656677246
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
      "current_price": 66.27999877929688
    },
    {
      "ticker": "BTU",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 17.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 28.8,
      "current_price": 32.439998626708984
    },
    {
      "ticker": "CARR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 27.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.8,
      "current_price": 54.90999984741211
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
        "score": 80.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.0,
      "current_price": 18.7450008392334
    },
    {
      "ticker": "CELH",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 29.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 29.6,
      "current_price": 34.28499984741211
    },
    {
      "ticker": "COIN",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.0,
      "current_price": 170.41000366210938
    },
    {
      "ticker": "CORZ",
      "technical": {
        "score": 85.0,
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
      "composite_score": 51.6,
      "current_price": 16.145000457763672
    },
    {
      "ticker": "CPRT",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 33.025001525878906
    },
    {
      "ticker": "CRDO",
      "technical": {
        "score": 60.0,
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
      "composite_score": 64.0,
      "current_price": 103.36000061035156
    },
    {
      "ticker": "CRK",
      "technical": {
        "score": 30.0,
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
      "composite_score": 46.8,
      "current_price": 19.2450008392334
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
      "current_price": 83.15170288085938
    },
    {
      "ticker": "DBX",
      "technical": {
        "score": 60.0,
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
      "composite_score": 55.2,
      "current_price": 23.825000762939453
    },
    {
      "ticker": "DD",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 25.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.0,
      "current_price": 45.1349983215332
    },
    {
      "ticker": "DG",
      "technical": {
        "score": 60.0,
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
      "composite_score": 58.0,
      "current_price": 121.87999725341797
    },
    {
      "ticker": "DHI",
      "technical": {
        "score": 60.0,
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
      "composite_score": 53.2,
      "current_price": 136.92999267578125
    },
    {
      "ticker": "DHR",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 64.0,
      "current_price": 189.55999755859375
    },
    {
      "ticker": "DOC",
      "technical": {
        "score": 55.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 36.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.4,
      "current_price": 16.96500015258789
    },
    {
      "ticker": "DOCU",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 49.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 69.6,
      "current_price": 47.599998474121094
    },
    {
      "ticker": "DXCM",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 62.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 63.34000015258789
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
      "current_price": 17.8700008392334
    },
    {
      "ticker": "EGO",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 77.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 64.8,
      "current_price": 35.26940155029297
    },
    {
      "ticker": "EL",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 12.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.8,
      "current_price": 69.4800033569336
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
        "score": 32.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.8,
      "current_price": 22.55500030517578
    },
    {
      "ticker": "ELF",
      "technical": {
        "score": 20.0,
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
      "composite_score": 36.0,
      "current_price": 60.89500045776367
    },
    {
      "ticker": "ENPH",
      "technical": {
        "score": 20.0,
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
      "composite_score": 36.400000000000006,
      "current_price": 31.625
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
      "current_price": 37.7599983215332
    },
    {
      "ticker": "EQX",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 23.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.2,
      "current_price": 14.510000228881836
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
        "score": 52.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.8,
      "current_price": 80.94999694824219
    },
    {
      "ticker": "F",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 14.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.6,
      "current_price": 11.501999855041504
    },
    {
      "ticker": "FIG",
      "technical": {
        "score": 20.0,
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
      "composite_score": 26.8,
      "current_price": 21.010000228881836
    },
    {
      "ticker": "FIS",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 36.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.4,
      "current_price": 46.349998474121094
    },
    {
      "ticker": "FLNC",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 21.0,
        "sector": "Utilities"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 26.4,
      "current_price": 12.859999656677246
    },
    {
      "ticker": "FND",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 33.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 48.0099983215332
    },
    {
      "ticker": "FOUR",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 29.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.6,
      "current_price": 41.189998626708984
    },
    {
      "ticker": "GEHC",
      "technical": {
        "score": 60.0,
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
      "composite_score": 55.2,
      "current_price": 69.44999694824219
    },
    {
      "ticker": "GILD",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 59.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.6,
      "current_price": 138.03500366210938
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
        "score": 17.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 24.8,
      "current_price": 18.079999923706055
    },
    {
      "ticker": "GM",
      "technical": {
        "score": 60.0,
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
      "composite_score": 43.6,
      "current_price": 72.29000091552734
    },
    {
      "ticker": "HIMS",
      "technical": {
        "score": 30.0,
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
      "composite_score": 38.8,
      "current_price": 19.645000457763672
    },
    {
      "ticker": "HMY",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 70.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.0,
      "current_price": 15.630000114440918
    },
    {
      "ticker": "HPQ",
      "technical": {
        "score": 60.0,
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
      "composite_score": 47.2,
      "current_price": 18.725000381469727
    },
    {
      "ticker": "HRL",
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
      "current_price": 21.524999618530273
    },
    {
      "ticker": "HSAI",
      "technical": {
        "score": 30.0,
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
      "composite_score": 41.2,
      "current_price": 20.020000457763672
    },
    {
      "ticker": "HST",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 76.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 74.4,
      "current_price": 19.184999465942383
    },
    {
      "ticker": "HUT",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 21.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.4,
      "current_price": 50.540000915527344
    },
    {
      "ticker": "IAG",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 82.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 76.80000000000001,
      "current_price": 19.104999542236328
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
        "score": 42.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.8,
      "current_price": 28.27989959716797
    },
    {
      "ticker": "IONS",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 10.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.0,
      "current_price": 73.1500015258789
    },
    {
      "ticker": "IREN",
      "technical": {
        "score": 20.0,
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
      "composite_score": 42.8,
      "current_price": 35.130001068115234
    }
  ],
  "current_holdings": [
    {
      "ticker": "ALLY",
      "technical_score": 75.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.4,
      "context": "holdings",
      "current_price": 40.04999923706055,
      "sector": "Financial Services",
      "quantity": 189.0,
      "market_value": 7552.44,
      "cost_basis": 7471.17,
      "unrealized_pl": 81.27,
      "unrealized_plpc": 1.088
    },
    {
      "ticker": "BZ",
      "technical_score": 50.0,
      "fundamental_score": 95.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 13.295000076293945,
      "sector": "Communication Services",
      "quantity": 751.0,
      "market_value": 9958.26,
      "cost_basis": 9980.79,
      "unrealized_pl": -22.53,
      "unrealized_plpc": -0.22599999999999998
    },
    {
      "ticker": "CF",
      "technical_score": 70.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.0,
      "context": "holdings",
      "current_price": 134.5050048828125,
      "sector": "Basic Materials",
      "quantity": 107.0,
      "market_value": 14417.18,
      "cost_basis": 9909.27,
      "unrealized_pl": 4507.91,
      "unrealized_plpc": 45.492
    },
    {
      "ticker": "DOCN",
      "technical_score": 70.0,
      "fundamental_score": 55.0,
      "sentiment_score": 50.0,
      "research_composite_score": 60.0,
      "context": "holdings",
      "current_price": 85.54000091552734,
      "sector": "Technology",
      "quantity": 110.0,
      "market_value": 9342.3,
      "cost_basis": 7466.8,
      "unrealized_pl": 1875.5,
      "unrealized_plpc": 25.118000000000002
    },
    {
      "ticker": "EXEL",
      "technical_score": 85.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.4,
      "context": "holdings",
      "current_price": 44.290000915527344,
      "sector": "Healthcare",
      "quantity": 233.0,
      "market_value": 10299.765,
      "cost_basis": 9984.05,
      "unrealized_pl": 315.715,
      "unrealized_plpc": 3.1620000000000004
    },
    {
      "ticker": "GNTX",
      "technical_score": 85.0,
      "fundamental_score": 95.0,
      "sentiment_score": 50.0,
      "research_composite_score": 82.0,
      "context": "holdings",
      "current_price": 21.440000534057617,
      "sector": "Consumer Cyclical",
      "quantity": 343.0,
      "market_value": 7336.77,
      "cost_basis": 7501.41,
      "unrealized_pl": -164.64,
      "unrealized_plpc": -2.1950000000000003
    },
    {
      "ticker": "GSK",
      "technical_score": 85.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.4,
      "context": "holdings",
      "current_price": 55.599998474121094,
      "sector": "Healthcare",
      "quantity": 177.0,
      "market_value": 9809.34,
      "cost_basis": 9972.18,
      "unrealized_pl": -162.84,
      "unrealized_plpc": -1.633
    },
    {
      "ticker": "HL",
      "technical_score": 85.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.0,
      "context": "holdings",
      "current_price": 19.239999771118164,
      "sector": "Basic Materials",
      "quantity": 508.0,
      "market_value": 9735.82,
      "cost_basis": 9997.44,
      "unrealized_pl": -261.62,
      "unrealized_plpc": -2.617
    },
    {
      "ticker": "SLM",
      "technical_score": 75.0,
      "fundamental_score": 74.0,
      "sentiment_score": 50.0,
      "research_composite_score": 69.6,
      "context": "holdings",
      "current_price": 21.760000228881836,
      "sector": "Financial Services",
      "quantity": 380.0,
      "market_value": 8257.4,
      "cost_basis": 7478.4,
      "unrealized_pl": 779.0,
      "unrealized_plpc": 10.417
    }
  ],
  "screening": {
    "universe_size": 77,
    "candidates_found": 68,
    "holdings_count": 9,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
