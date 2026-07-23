---
from: RESEARCH
message_id: MSG_RESEARCH_20260427T160816Z_d3cadcab
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-04-27T16:08:16.755776Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-04-27

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -0.03%
- **VIX**: 18.7 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 64 swing-suitable stocks
- **Current Holdings**: 11 positions from Alpaca
- **Total Scored**: 75 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **ACI** - Composite: 31.2/100
   - Technical: 30.0, Fundamental: 23.0
2. **ADM** - Composite: 35.6/100
   - Technical: 45.0, Fundamental: 19.0
3. **ALK** - Composite: 53.2/100
   - Technical: 85.0, Fundamental: 23.0
4. **APA** - Composite: 46.0/100
   - Technical: 45.0, Fundamental: 45.0
5. **APLD** - Composite: 58.8/100
   - Technical: 100.0, Fundamental: 22.0

```json
{
  "market_conditions": {
    "spy_change_pct": -0.03081935982418571,
    "vix": 18.690000534057617,
    "vix_status": "NORMAL",
    "date": "2026-04-27"
  },
  "candidates": [
    {
      "ticker": "ACI",
      "technical": {
        "score": 30.0,
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
      "composite_score": 31.200000000000003,
      "current_price": 16.739999771118164
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
        "score": 19.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 35.6,
      "current_price": 70.16999816894531
    },
    {
      "ticker": "ALK",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 23.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.2,
      "current_price": 40.709999084472656
    },
    {
      "ticker": "APA",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.0,
      "current_price": 38.08000183105469
    },
    {
      "ticker": "APLD",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.8,
      "current_price": 33.724998474121094
    },
    {
      "ticker": "BEKE",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 16.020000457763672
    },
    {
      "ticker": "BMNR",
      "technical": {
        "score": 100.0,
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
      "composite_score": 68.8,
      "current_price": 21.514999389648438
    },
    {
      "ticker": "BRKR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 25.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.0,
      "current_price": 36.290000915527344
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
      "current_price": 66.56749725341797
    },
    {
      "ticker": "BTDR",
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
      "current_price": 11.419500350952148
    },
    {
      "ticker": "CHTR",
      "technical": {
        "score": 30.0,
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
      "composite_score": 38.400000000000006,
      "current_price": 177.4600067138672
    },
    {
      "ticker": "CIFR",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.8,
      "current_price": 17.95009994506836
    },
    {
      "ticker": "CNK",
      "technical": {
        "score": 70.0,
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
      "composite_score": 48.0,
      "current_price": 29.53499984741211
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
      "current_price": 50.689998626708984
    },
    {
      "ticker": "COIN",
      "technical": {
        "score": 85.0,
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
      "composite_score": 60.0,
      "current_price": 196.7449951171875
    },
    {
      "ticker": "CPRT",
      "technical": {
        "score": 85.0,
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
      "composite_score": 68.0,
      "current_price": 33.48500061035156
    },
    {
      "ticker": "CRCL",
      "technical": {
        "score": 30.0,
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
      "composite_score": 35.6,
      "current_price": 96.06749725341797
    },
    {
      "ticker": "CRWV",
      "technical": {
        "score": 100.0,
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
      "composite_score": 54.8,
      "current_price": 107.05000305175781
    },
    {
      "ticker": "DAR",
      "technical": {
        "score": 45.0,
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
      "composite_score": 41.6,
      "current_price": 60.584999084472656
    },
    {
      "ticker": "DBX",
      "technical": {
        "score": 85.0,
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
      "composite_score": 65.2,
      "current_price": 24.270000457763672
    },
    {
      "ticker": "DD",
      "technical": {
        "score": 55.0,
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
      "composite_score": 42.0,
      "current_price": 46.529998779296875
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
      "current_price": 118.63999938964844
    },
    {
      "ticker": "DHR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 180.40750122070312
    },
    {
      "ticker": "DLTR",
      "technical": {
        "score": 60.0,
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
      "composite_score": 52.0,
      "current_price": 97.73500061035156
    },
    {
      "ticker": "DOC",
      "technical": {
        "score": 30.0,
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
      "composite_score": 36.4,
      "current_price": 16.475000381469727
    },
    {
      "ticker": "DVN",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 47.93000030517578
    },
    {
      "ticker": "DXCM",
      "technical": {
        "score": 60.0,
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
      "composite_score": 60.8,
      "current_price": 61.64500045776367
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
      "current_price": 18.174999237060547
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
      "current_price": 19.795000076293945
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
      "current_price": 59.38999938964844
    },
    {
      "ticker": "EW",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.0,
      "current_price": 84.4000015258789
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
        "score": 61.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.400000000000006,
      "current_price": 96.55000305175781
    },
    {
      "ticker": "F",
      "technical": {
        "score": 85.0,
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
      "composite_score": 49.6,
      "current_price": 12.489999771118164
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
      "current_price": 13.96500015258789
    },
    {
      "ticker": "FLNC",
      "technical": {
        "score": 60.0,
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
      "composite_score": 42.4,
      "current_price": 12.710000038146973
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
      "current_price": 49.619998931884766
    },
    {
      "ticker": "FOXA",
      "technical": {
        "score": 100.0,
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
      "composite_score": 74.0,
      "current_price": 63.86000061035156
    },
    {
      "ticker": "FTI",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 48.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 57.2,
      "current_price": 74.58499908447266
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
      "current_price": 70.51000213623047
    },
    {
      "ticker": "GH",
      "technical": {
        "score": 85.0,
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
      "composite_score": 58.8,
      "current_price": 90.20989990234375
    },
    {
      "ticker": "GILD",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 64.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.6,
      "current_price": 128.65390014648438
    },
    {
      "ticker": "GM",
      "technical": {
        "score": 85.0,
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
      "composite_score": 53.6,
      "current_price": 77.65160369873047
    },
    {
      "ticker": "GSK",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 66.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.400000000000006,
      "current_price": 54.564998626708984
    },
    {
      "ticker": "GTLB",
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
      "current_price": 21.6200008392334
    },
    {
      "ticker": "HAL",
      "technical": {
        "score": 100.0,
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
      "composite_score": 70.4,
      "current_price": 40.25849914550781
    },
    {
      "ticker": "HOOD",
      "technical": {
        "score": 100.0,
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
      "composite_score": 68.4,
      "current_price": 83.41500091552734
    },
    {
      "ticker": "HPQ",
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
      "current_price": 19.584999084472656
    },
    {
      "ticker": "IONS",
      "technical": {
        "score": 30.0,
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
      "composite_score": 26.0,
      "current_price": 73.16999816894531
    },
    {
      "ticker": "JBS",
      "technical": {
        "score": 30.0,
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
      "composite_score": 43.6,
      "current_price": 16.354999542236328
    },
    {
      "ticker": "JD",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 38.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.2,
      "current_price": 29.850000381469727
    },
    {
      "ticker": "KMX",
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
      "current_price": 38.22999954223633
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
        "score": 40.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.0,
      "current_price": 63.11000061035156
    },
    {
      "ticker": "KVYO",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.8,
      "current_price": 19.864999771118164
    },
    {
      "ticker": "LVS",
      "technical": {
        "score": 30.0,
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
      "composite_score": 46.400000000000006,
      "current_price": 54.064998626708984
    },
    {
      "ticker": "MDLZ",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 31.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 56.4,
      "current_price": 57.94499969482422
    },
    {
      "ticker": "MGY",
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
      "current_price": 29.3799991607666
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
      "current_price": 144.7899932861328
    },
    {
      "ticker": "MP",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 63.13999938964844
    },
    {
      "ticker": "NBIS",
      "technical": {
        "score": 70.0,
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
      "composite_score": 52.8,
      "current_price": 140.25
    },
    {
      "ticker": "NCLH",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 43.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 39.2,
      "current_price": 18.350000381469727
    },
    {
      "ticker": "OBDC",
      "technical": {
        "score": 100.0,
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
      "composite_score": 68.8,
      "current_price": 11.199999809265137
    },
    {
      "ticker": "OKE",
      "technical": {
        "score": 100.0,
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
      "composite_score": 73.2,
      "current_price": 87.20999908447266
    },
    {
      "ticker": "ONB",
      "technical": {
        "score": 100.0,
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
      "composite_score": 80.0,
      "current_price": 23.790000915527344
    },
    {
      "ticker": "PATH",
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
      "current_price": 10.425000190734863
    }
  ],
  "current_holdings": [
    {
      "ticker": "ALAB",
      "technical_score": 80.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 194.69000244140625,
      "sector": "Technology",
      "quantity": 51.0,
      "market_value": 9967.695,
      "cost_basis": 6389.28,
      "unrealized_pl": 3578.415,
      "unrealized_plpc": 56.007
    },
    {
      "ticker": "ALLY",
      "technical_score": 100.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.8,
      "context": "holdings",
      "current_price": 44.47999954223633,
      "sector": "Financial Services",
      "quantity": 189.0,
      "market_value": 8389.71,
      "cost_basis": 7471.17,
      "unrealized_pl": 918.54,
      "unrealized_plpc": 12.293999999999999
    },
    {
      "ticker": "ARM",
      "technical_score": 90.0,
      "fundamental_score": 47.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 213.82000732421875,
      "sector": "Technology",
      "quantity": 41.0,
      "market_value": 8785.275,
      "cost_basis": 6607.97,
      "unrealized_pl": 2177.305,
      "unrealized_plpc": 32.95
    },
    {
      "ticker": "BANC",
      "technical_score": 100.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 76.4,
      "context": "holdings",
      "current_price": 18.594999313354492,
      "sector": "Financial Services",
      "quantity": 360.0,
      "market_value": 6692.4,
      "cost_basis": 6717.6,
      "unrealized_pl": -25.2,
      "unrealized_plpc": -0.375
    },
    {
      "ticker": "BZ",
      "technical_score": 85.0,
      "fundamental_score": 95.0,
      "sentiment_score": 50.0,
      "research_composite_score": 82.0,
      "context": "holdings",
      "current_price": 13.595000267028809,
      "sector": "Communication Services",
      "quantity": 751.0,
      "market_value": 10209.845,
      "cost_basis": 9980.79,
      "unrealized_pl": 229.055,
      "unrealized_plpc": 2.2950000000000004
    },
    {
      "ticker": "COLB",
      "technical_score": 100.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 80.0,
      "context": "holdings",
      "current_price": 29.579999923706055,
      "sector": "Financial Services",
      "quantity": 231.0,
      "market_value": 6823.74,
      "cost_basis": 6696.69,
      "unrealized_pl": 127.05,
      "unrealized_plpc": 1.897
    },
    {
      "ticker": "DOCN",
      "technical_score": 100.0,
      "fundamental_score": 55.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 95.94000244140625,
      "sector": "Technology",
      "quantity": 73.0,
      "market_value": 7014.57,
      "cost_basis": 7006.54,
      "unrealized_pl": 8.03,
      "unrealized_plpc": 0.11499999999999999
    },
    {
      "ticker": "EXEL",
      "technical_score": 100.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.4,
      "context": "holdings",
      "current_price": 45.04499816894531,
      "sector": "Healthcare",
      "quantity": 233.0,
      "market_value": 10508.3,
      "cost_basis": 9984.05,
      "unrealized_pl": 524.25,
      "unrealized_plpc": 5.251
    },
    {
      "ticker": "GNTX",
      "technical_score": 65.0,
      "fundamental_score": 81.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.4,
      "context": "holdings",
      "current_price": 24.329999923706055,
      "sector": "Consumer Cyclical",
      "quantity": 343.0,
      "market_value": 8340.045,
      "cost_basis": 7501.41,
      "unrealized_pl": 838.635,
      "unrealized_plpc": 11.18
    },
    {
      "ticker": "HMY",
      "technical_score": 85.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 16.40999984741211,
      "sector": "Basic Materials",
      "quantity": 383.0,
      "market_value": 6279.285,
      "cost_basis": 6001.61,
      "unrealized_pl": 277.675,
      "unrealized_plpc": 4.627
    },
    {
      "ticker": "SLM",
      "technical_score": 100.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.4,
      "context": "holdings",
      "current_price": 23.479999542236328,
      "sector": "Financial Services",
      "quantity": 380.0,
      "market_value": 8905.3,
      "cost_basis": 7478.4,
      "unrealized_pl": 1426.9,
      "unrealized_plpc": 19.08
    }
  ],
  "screening": {
    "universe_size": 75,
    "candidates_found": 64,
    "holdings_count": 11,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
