---
from: RESEARCH
message_id: MSG_RESEARCH_20251110T144027Z_bffb164d
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2025-11-10T14:40:27.356087Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2025-11-10

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +1.17%
- **VIX**: 18.3 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 71 swing-suitable stocks
- **Current Holdings**: 22 positions from Alpaca
- **Total Scored**: 93 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **ALGM** - Composite: 26.8/100
   - Technical: 20.0, Fundamental: 22.0
2. **ALKS** - Composite: 73.6/100
   - Technical: 100.0, Fundamental: 59.0
3. **COMM** - Composite: 74.8/100
   - Technical: 100.0, Fundamental: 62.0
4. **DNOW** - Composite: 40.8/100
   - Technical: 20.0, Fundamental: 57.0
5. **ROKU** - Composite: 58.8/100
   - Technical: 100.0, Fundamental: 22.0

```json
{
  "market_conditions": {
    "spy_change_pct": 1.1736739859978584,
    "vix": 18.34000015258789,
    "vix_status": "NORMAL",
    "date": "2025-11-10"
  },
  "candidates": [
    {
      "ticker": "ALGM",
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
      "current_price": 27.760000228881836
    },
    {
      "ticker": "ALKS",
      "technical": {
        "score": 100.0,
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
      "composite_score": 73.6,
      "current_price": 33.0099983215332
    },
    {
      "ticker": "COMM",
      "technical": {
        "score": 100.0,
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
      "composite_score": 74.8,
      "current_price": 16.992000579833984
    },
    {
      "ticker": "DNOW",
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
      "current_price": 13.350000381469727
    },
    {
      "ticker": "ROKU",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.8,
      "current_price": 103.3759994506836
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
      "current_price": 69.95999908447266
    },
    {
      "ticker": "WSC",
      "technical": {
        "score": 10.0,
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
      "composite_score": 29.200000000000003,
      "current_price": 18.15999984741211
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
      "current_price": 16.100000381469727
    },
    {
      "ticker": "CORZ",
      "technical": {
        "score": 70.0,
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
      "composite_score": 46.8,
      "current_price": 20.850000381469727
    },
    {
      "ticker": "CSGP",
      "technical": {
        "score": 10.0,
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
      "composite_score": 26.8,
      "current_price": 66.86499786376953
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
      "current_price": 15.979999542236328
    },
    {
      "ticker": "ONON",
      "technical": {
        "score": 20.0,
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
      "composite_score": 32.8,
      "current_price": 35.0
    },
    {
      "ticker": "OPCH",
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
      "current_price": 27.290000915527344
    },
    {
      "ticker": "SN",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 68.0,
      "current_price": 95.18499755859375
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
        "score": 52.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.8,
      "current_price": 17.579999923706055
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
      "current_price": 55.83000183105469
    },
    {
      "ticker": "ADMA",
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
      "current_price": 14.520000457763672
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
        "score": 52.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.8,
      "current_price": 165.49000549316406
    },
    {
      "ticker": "ALLY",
      "technical": {
        "score": 30.0,
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
      "composite_score": 43.2,
      "current_price": 39.66999816894531
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
      "current_price": 19.469999313354492
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
      "current_price": 83.45999908447266
    },
    {
      "ticker": "ARQT",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.8,
      "current_price": 24.565000534057617
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
      "current_price": 69.19000244140625
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
      "current_price": 11.5
    },
    {
      "ticker": "AXTA",
      "technical": {
        "score": 85.0,
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
      "composite_score": 70.4,
      "current_price": 28.969999313354492
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
      "current_price": 194.91000366210938
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
      "current_price": 87.5801010131836
    },
    {
      "ticker": "BANC",
      "technical": {
        "score": 100.0,
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
      "composite_score": 72.8,
      "current_price": 17.290000915527344
    },
    {
      "ticker": "BBIO",
      "technical": {
        "score": 100.0,
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
      "composite_score": 64.8,
      "current_price": 62.709999084472656
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
      "current_price": 22.799999237060547
    },
    {
      "ticker": "BKR",
      "technical": {
        "score": 85.0,
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
      "composite_score": 65.6,
      "current_price": 48.04499816894531
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
      "current_price": 46.869998931884766
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
      "current_price": 43.404998779296875
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
      "current_price": 52.52000045776367
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
        "score": 56.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.400000000000006,
      "current_price": 78.03500366210938
    },
    {
      "ticker": "BTDR",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 16.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.4,
      "current_price": 22.65999984741211
    },
    {
      "ticker": "BX",
      "technical": {
        "score": 50.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 30.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.0,
      "current_price": 148.2449951171875
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
      "current_price": 57.310001373291016
    },
    {
      "ticker": "CCJ",
      "technical": {
        "score": 70.0,
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
      "composite_score": 50.0,
      "current_price": 95.75
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
        "score": 72.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.8,
      "current_price": 15.390000343322754
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
      "current_price": 43.96900177001953
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
      "current_price": 82.54499816894531
    },
    {
      "ticker": "CG",
      "technical": {
        "score": 20.0,
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
      "composite_score": 34.8,
      "current_price": 53.22999954223633
    },
    {
      "ticker": "CLF",
      "technical": {
        "score": 20.0,
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
      "composite_score": 27.6,
      "current_price": 10.614999771118164
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
      "current_price": 11.710000038146973
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
      "current_price": 29.235000610351562
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 20.0,
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
      "composite_score": 35.6,
      "current_price": 29.875
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
        "score": 16.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 28.4,
      "current_price": 108.63999938964844
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
      "current_price": 170.77000427246094
    },
    {
      "ticker": "CRSP",
      "technical": {
        "score": 20.0,
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
      "composite_score": 30.8,
      "current_price": 57.400901794433594
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
      "current_price": 104.01000213623047
    },
    {
      "ticker": "CVE",
      "technical": {
        "score": 85.0,
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
      "composite_score": 67.2,
      "current_price": 17.575000762939453
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
      "current_price": 20.075000762939453
    },
    {
      "ticker": "DBRG",
      "technical": {
        "score": 30.0,
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
      "composite_score": 32.0,
      "current_price": 10.65999984741211
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
      "current_price": 30.93000030517578
    },
    {
      "ticker": "DG",
      "technical": {
        "score": 30.0,
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
      "composite_score": 46.0,
      "current_price": 98.8499984741211
    },
    {
      "ticker": "DJT",
      "technical": {
        "score": 20.0,
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
      "composite_score": 26.0,
      "current_price": 13.3100004196167
    },
    {
      "ticker": "DKNG",
      "technical": {
        "score": 60.0,
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
      "composite_score": 37.2,
      "current_price": 30.790000915527344
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
      "current_price": 47.150001525878906
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
        "score": 35.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.0,
      "current_price": 17.68000030517578
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
      "current_price": 21.9950008392334
    },
    {
      "ticker": "EMN",
      "technical": {
        "score": 60.0,
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
      "composite_score": 52.0,
      "current_price": 60.67499923706055
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
      "current_price": 130.2899932861328
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
      "current_price": 30.850000381469727
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
      "current_price": 45.35499954223633
    },
    {
      "ticker": "ESI",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 42.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.8,
      "current_price": 27.71500015258789
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
      "current_price": 95.12000274658203
    },
    {
      "ticker": "EXAS",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.8,
      "current_price": 67.58999633789062
    },
    {
      "ticker": "FIG",
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
      "current_price": 44.255001068115234
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
      "current_price": 64.66999816894531
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
      "current_price": 10.944999694824219
    }
  ],
  "current_holdings": [
    {
      "ticker": "ACGL",
      "technical_score": 85.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.4,
      "context": "holdings",
      "current_price": 89.20999908447266,
      "sector": "Financial Services",
      "quantity": 101.0,
      "market_value": 8977.89,
      "cost_basis": 8950.62,
      "unrealized_pl": 27.27,
      "unrealized_plpc": 0.0030467163168585
    },
    {
      "ticker": "APH",
      "technical_score": 90.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 142.6300048828125,
      "sector": "Technology",
      "quantity": 58.0,
      "market_value": 8288.78,
      "cost_basis": 8081.72,
      "unrealized_pl": 207.06,
      "unrealized_plpc": 0.0256207836945601
    },
    {
      "ticker": "APO",
      "technical_score": 85.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.0,
      "context": "holdings",
      "current_price": 134.27749633789062,
      "sector": "Financial Services",
      "quantity": 54.0,
      "market_value": 7280.82,
      "cost_basis": 6997.32,
      "unrealized_pl": 283.5,
      "unrealized_plpc": 0.0405155116530329
    },
    {
      "ticker": "AZN",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 86.6500015258789,
      "sector": "Healthcare",
      "quantity": 80.0,
      "market_value": 6936.2,
      "cost_basis": 6770.4,
      "unrealized_pl": 165.8,
      "unrealized_plpc": 0.0244889519083067
    },
    {
      "ticker": "BMY",
      "technical_score": 85.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.8,
      "context": "holdings",
      "current_price": 47.08000183105469,
      "sector": "Healthcare",
      "quantity": 109.0,
      "market_value": 5128.45,
      "cost_basis": 5072.86,
      "unrealized_pl": 55.59,
      "unrealized_plpc": 0.0109583154275892
    },
    {
      "ticker": "CFG",
      "technical_score": 85.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 52.27000045776367,
      "sector": "Financial Services",
      "quantity": 98.0,
      "market_value": 5116.58,
      "cost_basis": 5078.36,
      "unrealized_pl": 38.22,
      "unrealized_plpc": 0.0075260517174836
    },
    {
      "ticker": "CTVA",
      "technical_score": 85.0,
      "fundamental_score": 47.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 64.63999938964844,
      "sector": "Basic Materials",
      "quantity": 190.0,
      "market_value": 12262.6,
      "cost_basis": 11932.0,
      "unrealized_pl": 330.6,
      "unrealized_plpc": 0.0277070063694268
    },
    {
      "ticker": "DVN",
      "technical_score": 85.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.2,
      "context": "holdings",
      "current_price": 33.61000061035156,
      "sector": "Energy",
      "quantity": 225.0,
      "market_value": 7611.75,
      "cost_basis": 7337.25,
      "unrealized_pl": 274.5,
      "unrealized_plpc": 0.0374118368598589
    },
    {
      "ticker": "EIX",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 57.402000427246094,
      "sector": "Utilities",
      "quantity": 214.0,
      "market_value": 12262.2,
      "cost_basis": 11864.16,
      "unrealized_pl": 398.04,
      "unrealized_plpc": 0.0335497835497835
    },
    {
      "ticker": "EQT",
      "technical_score": 100.0,
      "fundamental_score": 52.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.8,
      "context": "holdings",
      "current_price": 58.494998931884766,
      "sector": "Energy",
      "quantity": 89.0,
      "market_value": 5228.75,
      "cost_basis": 5015.16,
      "unrealized_pl": 213.59,
      "unrealized_plpc": 0.042588870544509
    },
    {
      "ticker": "EXE",
      "technical_score": 100.0,
      "fundamental_score": 35.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 112.57749938964844,
      "sector": "Energy",
      "quantity": 45.0,
      "market_value": 5089.05,
      "cost_basis": 5000.85,
      "unrealized_pl": 88.2,
      "unrealized_plpc": 0.0176370017097093
    },
    {
      "ticker": "FITB",
      "technical_score": 85.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.4,
      "context": "holdings",
      "current_price": 43.130001068115234,
      "sector": "Financial Services",
      "quantity": 118.0,
      "market_value": 5096.42,
      "cost_basis": 5023.26,
      "unrealized_pl": 73.16,
      "unrealized_plpc": 0.0145642471223867
    },
    {
      "ticker": "HST",
      "technical_score": 75.0,
      "fundamental_score": 68.0,
      "sentiment_score": 50.0,
      "research_composite_score": 67.2,
      "context": "holdings",
      "current_price": 18.0049991607666,
      "sector": "Real Estate",
      "quantity": 432.0,
      "market_value": 7771.68,
      "cost_basis": 7391.52,
      "unrealized_pl": 380.16,
      "unrealized_plpc": 0.0514319111630625
    },
    {
      "ticker": "MNST",
      "technical_score": 70.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 69.72000122070312,
      "sector": "Consumer Defensive",
      "quantity": 83.0,
      "market_value": 5766.84,
      "cost_basis": 5965.3,
      "unrealized_pl": -198.46,
      "unrealized_plpc": -0.0332690728043854
    },
    {
      "ticker": "NVDA",
      "technical_score": 70.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 194.6501007080078,
      "sector": "Technology",
      "quantity": 37.0,
      "market_value": 7221.105,
      "cost_basis": 7057.64,
      "unrealized_pl": 163.465,
      "unrealized_plpc": 0.0231614250656027
    },
    {
      "ticker": "PDD",
      "technical_score": 100.0,
      "fundamental_score": 68.0,
      "sentiment_score": 50.0,
      "research_composite_score": 77.2,
      "context": "holdings",
      "current_price": 137.08999633789062,
      "sector": "Consumer Cyclical",
      "quantity": 44.0,
      "market_value": 6024.04,
      "cost_basis": 5990.16,
      "unrealized_pl": 33.88,
      "unrealized_plpc": 0.0056559424122227
    },
    {
      "ticker": "PLD",
      "technical_score": 70.0,
      "fundamental_score": 38.0,
      "sentiment_score": 50.0,
      "research_composite_score": 53.2,
      "context": "holdings",
      "current_price": 125.37000274658203,
      "sector": "Real Estate",
      "quantity": 40.0,
      "market_value": 5014.6,
      "cost_basis": 4970.0,
      "unrealized_pl": 44.6,
      "unrealized_plpc": 0.0089738430583501
    },
    {
      "ticker": "QCOM",
      "technical_score": 70.0,
      "fundamental_score": 44.0,
      "sentiment_score": 50.0,
      "research_composite_score": 55.6,
      "context": "holdings",
      "current_price": 173.13999938964844,
      "sector": "Technology",
      "quantity": 74.0,
      "market_value": 12876.0,
      "cost_basis": 12750.2,
      "unrealized_pl": 125.8,
      "unrealized_plpc": 0.0098665118978526
    },
    {
      "ticker": "SLB",
      "technical_score": 100.0,
      "fundamental_score": 50.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.0,
      "context": "holdings",
      "current_price": 36.439998626708984,
      "sector": "Energy",
      "quantity": 185.0,
      "market_value": 6760.825,
      "cost_basis": 6752.5,
      "unrealized_pl": 8.325,
      "unrealized_plpc": 0.0012328767123288
    },
    {
      "ticker": "SYF",
      "technical_score": 85.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.0,
      "context": "holdings",
      "current_price": 73.97000122070312,
      "sector": "Financial Services",
      "quantity": 82.0,
      "market_value": 6058.16,
      "cost_basis": 6150.0,
      "unrealized_pl": -91.84,
      "unrealized_plpc": -0.0149333333333333
    },
    {
      "ticker": "UPS",
      "technical_score": 100.0,
      "fundamental_score": 37.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.8,
      "context": "holdings",
      "current_price": 93.58000183105469,
      "sector": "Industrials",
      "quantity": 70.0,
      "market_value": 6626.2,
      "cost_basis": 6612.2,
      "unrealized_pl": 14.0,
      "unrealized_plpc": 0.0021172983273343
    },
    {
      "ticker": "WFC",
      "technical_score": 70.0,
      "fundamental_score": 71.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.4,
      "context": "holdings",
      "current_price": 86.76000213623047,
      "sector": "Financial Services",
      "quantity": 114.0,
      "market_value": 9908.88,
      "cost_basis": 9986.4,
      "unrealized_pl": -77.52,
      "unrealized_plpc": -0.0077625570776256
    }
  ],
  "screening": {
    "universe_size": 93,
    "candidates_found": 71,
    "holdings_count": 22,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
