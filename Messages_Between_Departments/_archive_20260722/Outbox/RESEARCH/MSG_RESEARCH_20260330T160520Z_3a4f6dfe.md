---
from: RESEARCH
message_id: MSG_RESEARCH_20260330T160520Z_3a4f6dfe
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-03-30T16:05:20.027262Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-03-30

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +0.37%
- **VIX**: 29.7 (ELEVATED)

### Candidate Summary
- **Buy Candidates**: 66 swing-suitable stocks
- **Current Holdings**: 12 positions from Alpaca
- **Total Scored**: 78 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **INDV** - Composite: 44.0/100
   - Technical: 20.0, Fundamental: 65.0
2. **BZ** - Composite: 72.0/100
   - Technical: 60.0, Fundamental: 95.0
3. **AA** - Composite: 60.0/100
   - Technical: 70.0, Fundamental: 55.0
4. **ACI** - Composite: 59.6/100
   - Technical: 85.0, Fundamental: 39.0
5. **ADM** - Composite: 57.6/100
   - Technical: 100.0, Fundamental: 19.0

```json
{
  "market_conditions": {
    "spy_change_pct": 0.3658701747080606,
    "vix": 29.709999084472656,
    "vix_status": "ELEVATED",
    "date": "2026-03-30"
  },
  "candidates": [
    {
      "ticker": "INDV",
      "technical": {
        "score": 20.0,
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
      "composite_score": 44.0,
      "current_price": 28.860000610351562
    },
    {
      "ticker": "BZ",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 95.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.0,
      "current_price": 13.515000343322754
    },
    {
      "ticker": "AA",
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
      "current_price": 65.19999694824219
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
      "current_price": 17.454999923706055
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
      "current_price": 72.83000183105469
    },
    {
      "ticker": "AFRM",
      "technical": {
        "score": 60.0,
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
      "composite_score": 55.2,
      "current_price": 44.119998931884766
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
        "score": 43.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 35.2,
      "current_price": 20.274999618530273
    },
    {
      "ticker": "ALAB",
      "technical": {
        "score": 30.0,
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
      "composite_score": 48.0,
      "current_price": 103.34500122070312
    },
    {
      "ticker": "ALK",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 19.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 25.6,
      "current_price": 34.30500030517578
    },
    {
      "ticker": "AMKR",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 63.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 41.866600036621094
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
        "score": 29.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 33.6,
      "current_price": 39.5
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
        "score": 75.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.0,
      "current_price": 92.55000305175781
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
      "current_price": 27.09000015258789
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
        "score": 36.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.4,
      "current_price": 191.4600067138672
    },
    {
      "ticker": "BANC",
      "technical": {
        "score": 60.0,
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
      "composite_score": 62.0,
      "current_price": 17.084999084472656
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
        "score": 49.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 41.6,
      "current_price": 154.73500061035156
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
        "score": 37.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.8,
      "current_price": 18.75
    },
    {
      "ticker": "BMRN",
      "technical": {
        "score": 20.0,
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
      "composite_score": 37.2,
      "current_price": 54.869998931884766
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
        "score": 47.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 15.65999984741211
    },
    {
      "ticker": "BRO",
      "technical": {
        "score": 30.0,
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
      "composite_score": 44.400000000000006,
      "current_price": 65.43000030517578
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
      "current_price": 54.89500045776367
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
        "score": 80.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.0,
      "current_price": 17.075000762939453
    },
    {
      "ticker": "CENX",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 16.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.4,
      "current_price": 54.58000183105469
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
      "current_price": 17.610000610351562
    },
    {
      "ticker": "CMCSA",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 49.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 41.6,
      "current_price": 29.114999771118164
    },
    {
      "ticker": "CNM",
      "technical": {
        "score": 60.0,
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
      "composite_score": 54.400000000000006,
      "current_price": 48.66999816894531
    },
    {
      "ticker": "COGT",
      "technical": {
        "score": 60.0,
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
      "composite_score": 38.0,
      "current_price": 35.68000030517578
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
        "score": 45.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 163.32000732421875
    },
    {
      "ticker": "COLB",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 65.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.0,
      "current_price": 26.9950008392334
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
        "score": 19.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 29.6,
      "current_price": 14.300000190734863
    },
    {
      "ticker": "CPRT",
      "technical": {
        "score": 20.0,
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
      "composite_score": 42.0,
      "current_price": 32.88750076293945
    },
    {
      "ticker": "CRDO",
      "technical": {
        "score": 30.0,
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
      "composite_score": 52.0,
      "current_price": 90.17500305175781
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
      "current_price": 69.62999725341797
    },
    {
      "ticker": "DD",
      "technical": {
        "score": 60.0,
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
      "composite_score": 44.0,
      "current_price": 45.10499954223633
    },
    {
      "ticker": "DHR",
      "technical": {
        "score": 60.0,
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
      "composite_score": 54.0,
      "current_price": 185.3000030517578
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
      "current_price": 107.0
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
      "current_price": 16.731000900268555
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
        "score": 67.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 62.53499984741211
    },
    {
      "ticker": "DYN",
      "technical": {
        "score": 30.0,
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
      "composite_score": 30.0,
      "current_price": 17.079999923706055
    },
    {
      "ticker": "EGO",
      "technical": {
        "score": 20.0,
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
      "composite_score": 48.8,
      "current_price": 32.77000045776367
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
        "score": 58.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 41.2,
      "current_price": 61.369998931884766
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
        "score": 46.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.400000000000006,
      "current_price": 37.01969909667969
    },
    {
      "ticker": "EQH",
      "technical": {
        "score": 60.0,
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
      "composite_score": 42.0,
      "current_price": 36.439998626708984
    },
    {
      "ticker": "EQX",
      "technical": {
        "score": 20.0,
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
      "composite_score": 27.200000000000003,
      "current_price": 13.114999771118164
    },
    {
      "ticker": "EW",
      "technical": {
        "score": 20.0,
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
      "composite_score": 38.8,
      "current_price": 79.76000213623047
    },
    {
      "ticker": "EXEL",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 71.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 72.4,
      "current_price": 42.08000183105469
    },
    {
      "ticker": "F",
      "technical": {
        "score": 20.0,
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
      "composite_score": 23.6,
      "current_price": 11.305000305175781
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
      "current_price": 20.5049991607666
    },
    {
      "ticker": "FIS",
      "technical": {
        "score": 30.0,
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
      "composite_score": 36.4,
      "current_price": 47.712501525878906
    },
    {
      "ticker": "FLNC",
      "technical": {
        "score": 50.0,
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
      "composite_score": 38.4,
      "current_price": 13.399999618530273
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
      "current_price": 43.560001373291016
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
      "current_price": 69.6050033569336
    },
    {
      "ticker": "GLW",
      "technical": {
        "score": 45.0,
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
      "composite_score": 49.2,
      "current_price": 128.0800018310547
    },
    {
      "ticker": "GLXY",
      "technical": {
        "score": 30.0,
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
      "composite_score": 28.8,
      "current_price": 18.0
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
        "score": 61.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 68.4,
      "current_price": 54.380001068115234
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
        "score": 65.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.0,
      "current_price": 17.690000534057617
    },
    {
      "ticker": "HMY",
      "technical": {
        "score": 20.0,
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
      "composite_score": 46.0,
      "current_price": 14.40999984741211
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
        "score": 47.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.8,
      "current_price": 23.18000030517578
    },
    {
      "ticker": "HUT",
      "technical": {
        "score": 30.0,
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
      "composite_score": 30.4,
      "current_price": 45.709999084472656
    },
    {
      "ticker": "IAG",
      "technical": {
        "score": 20.0,
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
      "composite_score": 50.800000000000004,
      "current_price": 17.940000534057617
    },
    {
      "ticker": "IONS",
      "technical": {
        "score": 60.0,
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
      "composite_score": 38.0,
      "current_price": 72.63999938964844
    },
    {
      "ticker": "JCI",
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
      "current_price": 128.00999450683594
    },
    {
      "ticker": "KLAR",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.8,
      "current_price": 12.6850004196167
    },
    {
      "ticker": "KTOS",
      "technical": {
        "score": 20.0,
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
      "composite_score": 34.0,
      "current_price": 67.12999725341797
    },
    {
      "ticker": "LKNCY",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 57.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 32.349998474121094
    },
    {
      "ticker": "LKQ",
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
      "current_price": 29.334999084472656
    }
  ],
  "current_holdings": [
    {
      "ticker": "ALLY",
      "technical_score": 85.0,
      "fundamental_score": 66.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.4,
      "context": "holdings",
      "current_price": 38.5,
      "sector": "Financial Services",
      "quantity": 189.0,
      "market_value": 7288.785,
      "cost_basis": 7471.17,
      "unrealized_pl": -182.385,
      "unrealized_plpc": -2.4410000000000003
    },
    {
      "ticker": "CF",
      "technical_score": 90.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 137.75100708007812,
      "sector": "Basic Materials",
      "quantity": 107.0,
      "market_value": 14817.36,
      "cost_basis": 9909.27,
      "unrealized_pl": 4908.09,
      "unrealized_plpc": 49.53
    },
    {
      "ticker": "DELL",
      "technical_score": 100.0,
      "fundamental_score": 58.0,
      "sentiment_score": 50.0,
      "research_composite_score": 73.2,
      "context": "holdings",
      "current_price": 167.93499755859375,
      "sector": "Technology",
      "quantity": 67.0,
      "market_value": 11301.225,
      "cost_basis": 8236.98,
      "unrealized_pl": 3064.245,
      "unrealized_plpc": 37.201
    },
    {
      "ticker": "DOCN",
      "technical_score": 100.0,
      "fundamental_score": 55.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 78.19000244140625,
      "sector": "Technology",
      "quantity": 110.0,
      "market_value": 8607.5,
      "cost_basis": 7466.8,
      "unrealized_pl": 1140.7,
      "unrealized_plpc": 15.277
    },
    {
      "ticker": "DVN",
      "technical_score": 80.0,
      "fundamental_score": 50.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.0,
      "context": "holdings",
      "current_price": 52.314998626708984,
      "sector": "Energy",
      "quantity": 121.0,
      "market_value": 6341.61,
      "cost_basis": 6004.02,
      "unrealized_pl": 337.59,
      "unrealized_plpc": 5.623
    },
    {
      "ticker": "EBC",
      "technical_score": 85.0,
      "fundamental_score": 51.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.4,
      "context": "holdings",
      "current_price": 19.229999542236328,
      "sector": "Financial Services",
      "quantity": 311.0,
      "market_value": 5985.195,
      "cost_basis": 5968.09,
      "unrealized_pl": 17.105,
      "unrealized_plpc": 0.28700000000000003
    },
    {
      "ticker": "EQT",
      "technical_score": 70.0,
      "fundamental_score": 65.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 64.875,
      "sector": "Energy",
      "quantity": 89.0,
      "market_value": 5789.005,
      "cost_basis": 5929.18,
      "unrealized_pl": -140.175,
      "unrealized_plpc": -2.3640000000000003
    },
    {
      "ticker": "FOXA",
      "technical_score": 85.0,
      "fundamental_score": 60.0,
      "sentiment_score": 50.0,
      "research_composite_score": 68.0,
      "context": "holdings",
      "current_price": 59.119998931884766,
      "sector": "Communication Services",
      "quantity": 104.0,
      "market_value": 6156.28,
      "cost_basis": 5968.56,
      "unrealized_pl": 187.72,
      "unrealized_plpc": 3.145
    },
    {
      "ticker": "GNTX",
      "technical_score": 60.0,
      "fundamental_score": 95.0,
      "sentiment_score": 50.0,
      "research_composite_score": 72.0,
      "context": "holdings",
      "current_price": 21.540000915527344,
      "sector": "Consumer Cyclical",
      "quantity": 343.0,
      "market_value": 7400.225,
      "cost_basis": 7501.41,
      "unrealized_pl": -101.185,
      "unrealized_plpc": -1.349
    },
    {
      "ticker": "HST",
      "technical_score": 60.0,
      "fundamental_score": 76.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.4,
      "context": "holdings",
      "current_price": 19.010000228881836,
      "sector": "Real Estate",
      "quantity": 313.0,
      "market_value": 5954.825,
      "cost_basis": 5975.17,
      "unrealized_pl": -20.345,
      "unrealized_plpc": -0.33999999999999997
    },
    {
      "ticker": "RRC",
      "technical_score": 90.0,
      "fundamental_score": 75.0,
      "sentiment_score": 50.0,
      "research_composite_score": 76.0,
      "context": "holdings",
      "current_price": 46.345001220703125,
      "sector": "Energy",
      "quantity": 167.0,
      "market_value": 7752.14,
      "cost_basis": 5980.27,
      "unrealized_pl": 1771.87,
      "unrealized_plpc": 29.629
    },
    {
      "ticker": "SLM",
      "technical_score": 85.0,
      "fundamental_score": 74.0,
      "sentiment_score": 50.0,
      "research_composite_score": 73.6,
      "context": "holdings",
      "current_price": 20.690000534057617,
      "sector": "Financial Services",
      "quantity": 380.0,
      "market_value": 7862.2,
      "cost_basis": 7478.4,
      "unrealized_pl": 383.8,
      "unrealized_plpc": 5.132
    }
  ],
  "screening": {
    "universe_size": 78,
    "candidates_found": 66,
    "holdings_count": 12,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
