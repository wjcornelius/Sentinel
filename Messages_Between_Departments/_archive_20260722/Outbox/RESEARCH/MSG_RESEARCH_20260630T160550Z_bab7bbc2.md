---
from: RESEARCH
message_id: MSG_RESEARCH_20260630T160550Z_bab7bbc2
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-06-30T16:05:50.480535Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-06-30

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +0.69%
- **VIX**: 16.8 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 75 swing-suitable stocks
- **Current Holdings**: 12 positions from Alpaca
- **Total Scored**: 87 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **JEF** - Composite: 42.0/100
   - Technical: 20.0, Fundamental: 60.0
2. **ACI** - Composite: 27.2/100
   - Technical: 20.0, Fundamental: 23.0
3. **CCI** - Composite: 30.0/100
   - Technical: 20.0, Fundamental: 30.0
4. **FRO** - Composite: 54.0/100
   - Technical: 30.0, Fundamental: 80.0
5. **OLN** - Composite: 23.6/100
   - Technical: 20.0, Fundamental: 14.0

```json
{
  "market_conditions": {
    "spy_change_pct": 0.692308351256754,
    "vix": 16.84000015258789,
    "vix_status": "NORMAL",
    "date": "2026-06-30"
  },
  "candidates": [
    {
      "ticker": "JEF",
      "technical": {
        "score": 20.0,
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
      "composite_score": 42.0,
      "current_price": 49.90999984741211
    },
    {
      "ticker": "ACI",
      "technical": {
        "score": 20.0,
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
      "composite_score": 27.200000000000003,
      "current_price": 13.295000076293945
    },
    {
      "ticker": "CCI",
      "technical": {
        "score": 20.0,
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
      "composite_score": 30.0,
      "current_price": 76.09500122070312
    },
    {
      "ticker": "FRO",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 80.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.0,
      "current_price": 35.0
    },
    {
      "ticker": "OLN",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 14.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 23.6,
      "current_price": 19.78499984741211
    },
    {
      "ticker": "AA",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 47.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.8,
      "current_price": 52.96500015258789
    },
    {
      "ticker": "ABNB",
      "technical": {
        "score": 100.0,
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
      "composite_score": 71.6,
      "current_price": 145.2449951171875
    },
    {
      "ticker": "ADM",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 27.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.8,
      "current_price": 77.5719985961914
    },
    {
      "ticker": "AG",
      "technical": {
        "score": 30.0,
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
      "composite_score": 52.0,
      "current_price": 17.03499984741211
    },
    {
      "ticker": "AGI",
      "technical": {
        "score": 30.0,
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
      "composite_score": 56.0,
      "current_price": 30.270000457763672
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
      "current_price": 133.80999755859375
    },
    {
      "ticker": "AMKR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 61.2,
      "current_price": 84.197998046875
    },
    {
      "ticker": "APG",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 39.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 37.6,
      "current_price": 41.470001220703125
    },
    {
      "ticker": "APO",
      "technical": {
        "score": 20.0,
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
      "composite_score": 28.0,
      "current_price": 115.6500015258789
    },
    {
      "ticker": "AR",
      "technical": {
        "score": 85.0,
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
      "composite_score": 72.0,
      "current_price": 35.61000061035156
    },
    {
      "ticker": "ARES",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 46.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.400000000000006,
      "current_price": 110.26000213623047
    },
    {
      "ticker": "AU",
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
      "current_price": 81.51000213623047
    },
    {
      "ticker": "BDX",
      "technical": {
        "score": 100.0,
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
      "composite_score": 64.4,
      "current_price": 151.27499389648438
    },
    {
      "ticker": "BEAM",
      "technical": {
        "score": 100.0,
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
      "composite_score": 62.8,
      "current_price": 35.040000915527344
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
        "score": 47.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 13.017800331115723
    },
    {
      "ticker": "BZ",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 91.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.4,
      "current_price": 12.899999618530273
    },
    {
      "ticker": "CDE",
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
      "current_price": 16.239999771118164
    },
    {
      "ticker": "CG",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 42.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.8,
      "current_price": 41.45000076293945
    },
    {
      "ticker": "CHYM",
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
      "current_price": 19.934999465942383
    },
    {
      "ticker": "CMG",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 34.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.6,
      "current_price": 33.661598205566406
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
      "current_price": 47.900001525878906
    },
    {
      "ticker": "COIN",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 36.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.4,
      "current_price": 145.23500061035156
    },
    {
      "ticker": "CORZ",
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
      "current_price": 25.139999389648438
    },
    {
      "ticker": "CPRT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 73.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 51.2,
      "current_price": 28.155000686645508
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 23.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 28.354999542236328
    },
    {
      "ticker": "CRWV",
      "technical": {
        "score": 30.0,
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
      "composite_score": 26.8,
      "current_price": 97.43930053710938
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
        "score": 37.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.8,
      "current_price": 28.59000015258789
    },
    {
      "ticker": "CVNA",
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
      "current_price": 64.29000091552734
    },
    {
      "ticker": "CZR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 43.6,
      "current_price": 29.90999984741211
    },
    {
      "ticker": "DAR",
      "technical": {
        "score": 30.0,
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
      "composite_score": 35.6,
      "current_price": 55.130001068115234
    },
    {
      "ticker": "DEI",
      "technical": {
        "score": 45.0,
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
      "composite_score": 32.0,
      "current_price": 11.944999694824219
    },
    {
      "ticker": "DHT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 77.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 16.8700008392334
    },
    {
      "ticker": "DNOW",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 32.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.8,
      "current_price": 12.859999656677246
    },
    {
      "ticker": "DOCN",
      "technical": {
        "score": 45.0,
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
      "composite_score": 46.400000000000006,
      "current_price": 154.7449951171875
    },
    {
      "ticker": "EBAY",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 59.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 73.6,
      "current_price": 110.80999755859375
    },
    {
      "ticker": "ENPH",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 28.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.2,
      "current_price": 48.849998474121094
    },
    {
      "ticker": "EQH",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 33.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 51.2,
      "current_price": 43.630001068115234
    },
    {
      "ticker": "EQT",
      "technical": {
        "score": 85.0,
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
      "composite_score": 72.0,
      "current_price": 53.54999923706055
    },
    {
      "ticker": "EW",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 55.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.0,
      "current_price": 90.33499908447266
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
      "current_price": 91.90499877929688
    },
    {
      "ticker": "FIG",
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
      "current_price": 17.985000610351562
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
        "score": 49.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.6,
      "current_price": 162.96499633789062
    },
    {
      "ticker": "FLUT",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.8,
      "current_price": 100.81999969482422
    },
    {
      "ticker": "FOXA",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 56.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.400000000000006,
      "current_price": 51.18000030517578
    },
    {
      "ticker": "FTI",
      "technical": {
        "score": 30.0,
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
      "composite_score": 46.0,
      "current_price": 66.5
    },
    {
      "ticker": "GFS",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 35.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.0,
      "current_price": 81.23999786376953
    },
    {
      "ticker": "GSK",
      "technical": {
        "score": 85.0,
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
      "composite_score": 66.8,
      "current_price": 52.45000076293945
    },
    {
      "ticker": "HAL",
      "technical": {
        "score": 10.0,
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
      "composite_score": 38.400000000000006,
      "current_price": 34.19499969482422
    },
    {
      "ticker": "HBM",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 79.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.6,
      "current_price": 23.69499969482422
    },
    {
      "ticker": "HIMS",
      "technical": {
        "score": 100.0,
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
      "composite_score": 54.4,
      "current_price": 33.73189926147461
    },
    {
      "ticker": "HOOD",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 101.68000030517578
    },
    {
      "ticker": "IAG",
      "technical": {
        "score": 30.0,
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
      "composite_score": 52.8,
      "current_price": 15.8149995803833
    },
    {
      "ticker": "INTC",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 18.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.2,
      "current_price": 140.38330078125
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
        "score": 62.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 53.349998474121094
    },
    {
      "ticker": "IVZ",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 35.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.0,
      "current_price": 26.44499969482422
    },
    {
      "ticker": "KDP",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 49.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 69.6,
      "current_price": 33.19499969482422
    },
    {
      "ticker": "KKR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 26.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.4,
      "current_price": 90.69000244140625
    },
    {
      "ticker": "KTOS",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.0,
      "current_price": 49.27000045776367
    },
    {
      "ticker": "LVS",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 61.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.400000000000006,
      "current_price": 46.05500030517578
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
        "score": 58.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.2,
      "current_price": 25.825000762939453
    },
    {
      "ticker": "MIR",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 37.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.8,
      "current_price": 17.719999313354492
    },
    {
      "ticker": "MOS",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 31.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.4,
      "current_price": 21.225000381469727
    },
    {
      "ticker": "MTCH",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 64.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 69.6,
      "current_price": 37.43000030517578
    },
    {
      "ticker": "NKE",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 44.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.6,
      "current_price": 41.17499923706055
    },
    {
      "ticker": "NVT",
      "technical": {
        "score": 45.0,
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
      "composite_score": 44.0,
      "current_price": 167.2899932861328
    },
    {
      "ticker": "NXT",
      "technical": {
        "score": 30.0,
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
      "composite_score": 38.0,
      "current_price": 115.20999908447266
    },
    {
      "ticker": "OKE",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 71.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.4,
      "current_price": 89.2699966430664
    },
    {
      "ticker": "OKLO",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 30.0,
        "sector": "Utilities"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.0,
      "current_price": 51.119998931884766
    },
    {
      "ticker": "OMC",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.8,
      "current_price": 72.77999877929688
    },
    {
      "ticker": "ORLY",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 56.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.4,
      "current_price": 91.70999908447266
    }
  ],
  "current_holdings": [
    {
      "ticker": "AFRM",
      "technical_score": 90.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 67.2,
      "context": "holdings",
      "current_price": 81.0,
      "sector": "Financial Services",
      "quantity": 135.0,
      "market_value": 10966.725,
      "cost_basis": 10025.1,
      "unrealized_pl": 941.625,
      "unrealized_plpc": 9.393
    },
    {
      "ticker": "ALLY",
      "technical_score": 100.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.8,
      "context": "holdings",
      "current_price": 46.474998474121094,
      "sector": "Financial Services",
      "quantity": 218.0,
      "market_value": 10143.54,
      "cost_basis": 9973.5,
      "unrealized_pl": 170.04,
      "unrealized_plpc": 1.7049999999999998
    },
    {
      "ticker": "BRO",
      "technical_score": 100.0,
      "fundamental_score": 56.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.4,
      "context": "holdings",
      "current_price": 63.34000015258789,
      "sector": "Financial Services",
      "quantity": 128.0,
      "market_value": 8103.68,
      "cost_basis": 7454.72,
      "unrealized_pl": 648.96,
      "unrealized_plpc": 8.705
    },
    {
      "ticker": "C",
      "technical_score": 70.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.0,
      "context": "holdings",
      "current_price": 140.3800048828125,
      "sector": "Financial Services",
      "quantity": 52.0,
      "market_value": 7299.76,
      "cost_basis": 6754.8,
      "unrealized_pl": 544.96,
      "unrealized_plpc": 8.068
    },
    {
      "ticker": "COLB",
      "technical_score": 90.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 76.0,
      "context": "holdings",
      "current_price": 32.11000061035156,
      "sector": "Financial Services",
      "quantity": 200.0,
      "market_value": 6424.0,
      "cost_basis": 5986.0,
      "unrealized_pl": 438.0,
      "unrealized_plpc": 7.317
    },
    {
      "ticker": "DG",
      "technical_score": 100.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.4,
      "context": "holdings",
      "current_price": 115.2699966430664,
      "sector": "Consumer Defensive",
      "quantity": 55.0,
      "market_value": 6346.45,
      "cost_basis": 6009.3,
      "unrealized_pl": 337.15,
      "unrealized_plpc": 5.609999999999999
    },
    {
      "ticker": "DHR",
      "technical_score": 100.0,
      "fundamental_score": 45.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 190.03500366210938,
      "sector": "Healthcare",
      "quantity": 51.0,
      "market_value": 9711.165,
      "cost_basis": 9843.409989,
      "unrealized_pl": -132.244989,
      "unrealized_plpc": -1.343
    },
    {
      "ticker": "ENTG",
      "technical_score": 100.0,
      "fundamental_score": 40.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.0,
      "context": "holdings",
      "current_price": 174.3300018310547,
      "sector": "Technology",
      "quantity": 59.0,
      "market_value": 10336.21,
      "cost_basis": 9865.39,
      "unrealized_pl": 470.82,
      "unrealized_plpc": 4.772
    },
    {
      "ticker": "GNTX",
      "technical_score": 45.0,
      "fundamental_score": 91.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.4,
      "context": "holdings",
      "current_price": 25.209999084472656,
      "sector": "Consumer Cyclical",
      "quantity": 343.0,
      "market_value": 8652.175,
      "cost_basis": 7501.41,
      "unrealized_pl": 1150.765,
      "unrealized_plpc": 15.341
    },
    {
      "ticker": "HAYW",
      "technical_score": 90.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.4,
      "context": "holdings",
      "current_price": 17.045000076293945,
      "sector": "Industrials",
      "quantity": 657.0,
      "market_value": 11201.85,
      "cost_basis": 9992.97,
      "unrealized_pl": 1208.88,
      "unrealized_plpc": 12.097
    },
    {
      "ticker": "KMB",
      "technical_score": 90.0,
      "fundamental_score": 48.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 109.62000274658203,
      "sector": "Consumer Defensive",
      "quantity": 59.0,
      "market_value": 6471.8575,
      "cost_basis": 5916.52,
      "unrealized_pl": 555.3375,
      "unrealized_plpc": 9.386
    },
    {
      "ticker": "M",
      "technical_score": 45.0,
      "fundamental_score": 51.0,
      "sentiment_score": 50.0,
      "research_composite_score": 48.400000000000006,
      "context": "holdings",
      "current_price": 23.364999771118164,
      "sector": "Consumer Cyclical",
      "quantity": 261.0,
      "market_value": 6100.875,
      "cost_basis": 6008.22,
      "unrealized_pl": 92.655,
      "unrealized_plpc": 1.542
    }
  ],
  "screening": {
    "universe_size": 87,
    "candidates_found": 75,
    "holdings_count": 12,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
