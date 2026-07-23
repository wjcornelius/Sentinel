---
from: RESEARCH
message_id: MSG_RESEARCH_20260610T160555Z_fefb0a0d
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-06-10T16:05:55.255519Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-06-10

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -0.79%
- **VIX**: 22.4 (ELEVATED)

### Candidate Summary
- **Buy Candidates**: 73 swing-suitable stocks
- **Current Holdings**: 14 positions from Alpaca
- **Total Scored**: 87 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **BZ** - Composite: 58.4/100
   - Technical: 30.0, Fundamental: 91.0
2. **MCHP** - Composite: 38.8/100
   - Technical: 45.0, Fundamental: 27.0
3. **AA** - Composite: 40.8/100
   - Technical: 30.0, Fundamental: 47.0
4. **ABNB** - Composite: 43.6/100
   - Technical: 30.0, Fundamental: 54.0
5. **ACI** - Composite: 31.2/100
   - Technical: 30.0, Fundamental: 23.0

```json
{
  "market_conditions": {
    "spy_change_pct": -0.7869191898823957,
    "vix": 22.399999618530273,
    "vix_status": "ELEVATED",
    "date": "2026-06-10"
  },
  "candidates": [
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
      "current_price": 13.46500015258789
    },
    {
      "ticker": "MCHP",
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
      "current_price": 89.1500015258789
    },
    {
      "ticker": "AA",
      "technical": {
        "score": 30.0,
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
      "composite_score": 40.8,
      "current_price": 66.80780029296875
    },
    {
      "ticker": "ABNB",
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
      "current_price": 129.85000610351562
    },
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
      "current_price": 15.505000114440918
    },
    {
      "ticker": "ADM",
      "technical": {
        "score": 70.0,
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
      "composite_score": 48.8,
      "current_price": 82.00499725341797
    },
    {
      "ticker": "AFRM",
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
      "current_price": 64.20999908447266
    },
    {
      "ticker": "AG",
      "technical": {
        "score": 20.0,
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
      "composite_score": 48.0,
      "current_price": 16.0
    },
    {
      "ticker": "AI",
      "technical": {
        "score": 100.0,
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
      "composite_score": 58.0,
      "current_price": 11.050000190734863
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
      "current_price": 44.904998779296875
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
      "current_price": 70.69499969482422
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
        "score": 25.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.0,
      "current_price": 134.0500030517578
    },
    {
      "ticker": "AR",
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
      "current_price": 35.55500030517578
    },
    {
      "ticker": "ASX",
      "technical": {
        "score": 45.0,
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
      "composite_score": 46.8,
      "current_price": 34.7599983215332
    },
    {
      "ticker": "BBIO",
      "technical": {
        "score": 85.0,
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
      "composite_score": 57.6,
      "current_price": 68.4198989868164
    },
    {
      "ticker": "BDX",
      "technical": {
        "score": 85.0,
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
      "composite_score": 58.4,
      "current_price": 150.0850067138672
    },
    {
      "ticker": "BEAM",
      "technical": {
        "score": 70.0,
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
      "composite_score": 50.8,
      "current_price": 30.19499969482422
    },
    {
      "ticker": "BILL",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Unknown"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.0,
      "current_price": 32.78499984741211
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
      "current_price": 16.045000076293945
    },
    {
      "ticker": "BTU",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 21.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.4,
      "current_price": 26.975000381469727
    },
    {
      "ticker": "CCI",
      "technical": {
        "score": 70.0,
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
      "composite_score": 50.0,
      "current_price": 91.93000030517578
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
      "current_price": 15.699999809265137
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
      "current_price": 44.7599983215332
    },
    {
      "ticker": "CLF",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 28.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 49.2,
      "current_price": 12.625
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
      "current_price": 30.774999618530273
    },
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
      "current_price": 49.64500045776367
    },
    {
      "ticker": "COF",
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
      "current_price": 179.72000122070312
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
        "score": 31.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 34.4,
      "current_price": 158.4499969482422
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
      "current_price": 25.899999618530273
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
        "score": 37.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.8,
      "current_price": 34.4900016784668
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
      "current_price": 59.02000045776367
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
        "score": 45.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.0,
      "current_price": 185.61000061035156
    },
    {
      "ticker": "DNOW",
      "technical": {
        "score": 100.0,
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
      "composite_score": 62.8,
      "current_price": 13.785699844360352
    },
    {
      "ticker": "DOCN",
      "technical": {
        "score": 70.0,
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
      "composite_score": 56.400000000000006,
      "current_price": 171.60000610351562
    },
    {
      "ticker": "DOCU",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 54.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 43.6,
      "current_price": 45.79999923706055
    },
    {
      "ticker": "EBAY",
      "technical": {
        "score": 35.0,
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
      "composite_score": 47.6,
      "current_price": 108.42500305175781
    },
    {
      "ticker": "ELF",
      "technical": {
        "score": 85.0,
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
      "composite_score": 54.8,
      "current_price": 59.86000061035156
    },
    {
      "ticker": "ENTG",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 130.85000610351562
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
        "score": 70.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.0,
      "current_price": 53.415000915527344
    },
    {
      "ticker": "EWY",
      "technical": {
        "score": 45.0,
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
      "composite_score": 40.0,
      "current_price": 182.99000549316406
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
      "current_price": 90.16000366210938
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
      "current_price": 20.43000030517578
    },
    {
      "ticker": "FLEX",
      "technical": {
        "score": 45.0,
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
      "composite_score": 47.6,
      "current_price": 140.48500061035156
    },
    {
      "ticker": "FLG",
      "technical": {
        "score": 85.0,
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
      "composite_score": 54.8,
      "current_price": 14.574999809265137
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
      "current_price": 69.91000366210938
    },
    {
      "ticker": "GBTC",
      "technical": {
        "score": 10.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 5.0,
        "sector": "Unknown"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 16.0,
      "current_price": 48.459999084472656
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
      "current_price": 74.33499908447266
    },
    {
      "ticker": "GLW",
      "technical": {
        "score": 30.0,
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
      "composite_score": 45.2,
      "current_price": 170.7100067138672
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
        "score": 32.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.8,
      "current_price": 62.72999954223633
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
        "score": 27.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 29.3799991607666
    },
    {
      "ticker": "HAL",
      "technical": {
        "score": 45.0,
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
      "composite_score": 48.400000000000006,
      "current_price": 40.41999816894531
    },
    {
      "ticker": "HAYW",
      "technical": {
        "score": 85.0,
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
      "composite_score": 74.4,
      "current_price": 14.390000343322754
    },
    {
      "ticker": "HBM",
      "technical": {
        "score": 45.0,
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
      "composite_score": 59.6,
      "current_price": 25.25
    },
    {
      "ticker": "HL",
      "technical": {
        "score": 20.0,
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
      "composite_score": 42.8,
      "current_price": 14.194999694824219
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
        "score": 50.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 70.0,
      "current_price": 88.12010192871094
    },
    {
      "ticker": "HPQ",
      "technical": {
        "score": 70.0,
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
      "composite_score": 56.400000000000006,
      "current_price": 25.075000762939453
    },
    {
      "ticker": "IBKR",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 59.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 61.6,
      "current_price": 85.8550033569336
    },
    {
      "ticker": "INTC",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 23.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 37.2,
      "current_price": 107.0916976928711
    },
    {
      "ticker": "IOT",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 24.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 59.6,
      "current_price": 33.77000045776367
    },
    {
      "ticker": "IVZ",
      "technical": {
        "score": 70.0,
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
      "composite_score": 52.0,
      "current_price": 27.600000381469727
    },
    {
      "ticker": "KTOS",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.0,
      "current_price": 55.08000183105469
    },
    {
      "ticker": "KVYO",
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
      "current_price": 14.944999694824219
    },
    {
      "ticker": "LYFT",
      "technical": {
        "score": 85.0,
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
      "composite_score": 70.0,
      "current_price": 13.805000305175781
    },
    {
      "ticker": "LYV",
      "technical": {
        "score": 70.0,
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
      "composite_score": 50.8,
      "current_price": 168.61500549316406
    },
    {
      "ticker": "M",
      "technical": {
        "score": 100.0,
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
      "composite_score": 70.4,
      "current_price": 22.954999923706055
    },
    {
      "ticker": "MARA",
      "technical": {
        "score": 45.0,
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
      "composite_score": 34.8,
      "current_price": 13.0
    },
    {
      "ticker": "MIR",
      "technical": {
        "score": 30.0,
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
      "composite_score": 36.8,
      "current_price": 16.1200008392334
    },
    {
      "ticker": "MP",
      "technical": {
        "score": 30.0,
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
      "composite_score": 32.8,
      "current_price": 54.1349983215332
    },
    {
      "ticker": "MSTR",
      "technical": {
        "score": 20.0,
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
      "composite_score": 30.8,
      "current_price": 118.55000305175781
    },
    {
      "ticker": "MTCH",
      "technical": {
        "score": 30.0,
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
      "composite_score": 47.6,
      "current_price": 34.52000045776367
    },
    {
      "ticker": "OBDC",
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
      "current_price": 11.11870002746582
    },
    {
      "ticker": "OKE",
      "technical": {
        "score": 70.0,
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
      "composite_score": 66.4,
      "current_price": 90.80000305175781
    },
    {
      "ticker": "ON",
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
      "current_price": 110.78199768066406
    }
  ],
  "current_holdings": [
    {
      "ticker": "ALLY",
      "technical_score": 85.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.8,
      "context": "holdings",
      "current_price": 42.369998931884766,
      "sector": "Financial Services",
      "quantity": 138.0,
      "market_value": 5845.68,
      "cost_basis": 5974.02,
      "unrealized_pl": -128.34,
      "unrealized_plpc": -2.1479999999999997
    },
    {
      "ticker": "BRO",
      "technical_score": 85.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.4,
      "context": "holdings",
      "current_price": 61.220001220703125,
      "sector": "Financial Services",
      "quantity": 128.0,
      "market_value": 7829.12,
      "cost_basis": 7454.72,
      "unrealized_pl": 374.4,
      "unrealized_plpc": 5.022
    },
    {
      "ticker": "C",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 133.05999755859375,
      "sector": "Financial Services",
      "quantity": 52.0,
      "market_value": 6927.18,
      "cost_basis": 6754.8,
      "unrealized_pl": 172.38,
      "unrealized_plpc": 2.552
    },
    {
      "ticker": "COLB",
      "technical_score": 100.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 80.0,
      "context": "holdings",
      "current_price": 30.475000381469727,
      "sector": "Financial Services",
      "quantity": 200.0,
      "market_value": 6098.0,
      "cost_basis": 5986.0,
      "unrealized_pl": 112.0,
      "unrealized_plpc": 1.871
    },
    {
      "ticker": "CTSH",
      "technical_score": 85.0,
      "fundamental_score": 63.0,
      "sentiment_score": 50.0,
      "research_composite_score": 69.2,
      "context": "holdings",
      "current_price": 52.6150016784668,
      "sector": "Technology",
      "quantity": 143.0,
      "market_value": 7527.52,
      "cost_basis": 7513.22,
      "unrealized_pl": 14.3,
      "unrealized_plpc": 0.19
    },
    {
      "ticker": "DG",
      "technical_score": 85.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.4,
      "context": "holdings",
      "current_price": 109.9000015258789,
      "sector": "Consumer Defensive",
      "quantity": 55.0,
      "market_value": 6037.625,
      "cost_basis": 6009.3,
      "unrealized_pl": 28.325,
      "unrealized_plpc": 0.471
    },
    {
      "ticker": "EW",
      "technical_score": 100.0,
      "fundamental_score": 60.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.0,
      "context": "holdings",
      "current_price": 86.45999908447266,
      "sector": "Healthcare",
      "quantity": 121.0,
      "market_value": 10461.66,
      "cost_basis": 9946.2,
      "unrealized_pl": 515.46,
      "unrealized_plpc": 5.1819999999999995
    },
    {
      "ticker": "FOXA",
      "technical_score": 100.0,
      "fundamental_score": 56.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.4,
      "context": "holdings",
      "current_price": 68.52999877929688,
      "sector": "Communication Services",
      "quantity": 88.0,
      "market_value": 6029.32,
      "cost_basis": 5944.4,
      "unrealized_pl": 84.92,
      "unrealized_plpc": 1.429
    },
    {
      "ticker": "G",
      "technical_score": 85.0,
      "fundamental_score": 69.0,
      "sentiment_score": 50.0,
      "research_composite_score": 71.6,
      "context": "holdings",
      "current_price": 32.33000183105469,
      "sector": "Technology",
      "quantity": 232.0,
      "market_value": 7505.2,
      "cost_basis": 7498.539976,
      "unrealized_pl": 6.660024,
      "unrealized_plpc": 0.089
    },
    {
      "ticker": "GNTX",
      "technical_score": 80.0,
      "fundamental_score": 91.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.4,
      "context": "holdings",
      "current_price": 25.020000457763672,
      "sector": "Consumer Cyclical",
      "quantity": 343.0,
      "market_value": 8569.855,
      "cost_basis": 7501.41,
      "unrealized_pl": 1068.445,
      "unrealized_plpc": 14.243
    },
    {
      "ticker": "GSK",
      "technical_score": 85.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.8,
      "context": "holdings",
      "current_price": 51.290000915527344,
      "sector": "Healthcare",
      "quantity": 117.0,
      "market_value": 6002.1,
      "cost_basis": 5971.68,
      "unrealized_pl": 30.42,
      "unrealized_plpc": 0.509
    },
    {
      "ticker": "JCI",
      "technical_score": 100.0,
      "fundamental_score": 46.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.4,
      "context": "holdings",
      "current_price": 141.94500732421875,
      "sector": "Industrials",
      "quantity": 41.0,
      "market_value": 5824.665,
      "cost_basis": 5923.000015,
      "unrealized_pl": -98.335015,
      "unrealized_plpc": -1.66
    },
    {
      "ticker": "KMB",
      "technical_score": 100.0,
      "fundamental_score": 53.0,
      "sentiment_score": 50.0,
      "research_composite_score": 71.2,
      "context": "holdings",
      "current_price": 101.75650024414062,
      "sector": "Consumer Defensive",
      "quantity": 59.0,
      "market_value": 6000.89,
      "cost_basis": 5916.52,
      "unrealized_pl": 84.37,
      "unrealized_plpc": 1.426
    },
    {
      "ticker": "LVS",
      "technical_score": 60.0,
      "fundamental_score": 61.0,
      "sentiment_score": 50.0,
      "research_composite_score": 58.400000000000006,
      "context": "holdings",
      "current_price": 50.68000030517578,
      "sector": "Consumer Cyclical",
      "quantity": 116.0,
      "market_value": 5876.56,
      "cost_basis": 5972.84,
      "unrealized_pl": -96.28,
      "unrealized_plpc": -1.6119999999999999
    }
  ],
  "screening": {
    "universe_size": 87,
    "candidates_found": 73,
    "holdings_count": 14,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
