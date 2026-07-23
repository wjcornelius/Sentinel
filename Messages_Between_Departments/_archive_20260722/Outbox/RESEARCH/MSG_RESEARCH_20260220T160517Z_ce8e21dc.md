---
from: RESEARCH
message_id: MSG_RESEARCH_20260220T160517Z_ce8e21dc
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-02-20T16:05:17.358592Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-02-20

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: +0.62%
- **VIX**: 19.0 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 73 swing-suitable stocks
- **Current Holdings**: 11 positions from Alpaca
- **Total Scored**: 84 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **APO** - Composite: 45.2/100
   - Technical: 30.0, Fundamental: 58.0
2. **CG** - Composite: 48.8/100
   - Technical: 30.0, Fundamental: 67.0
3. **CTSH** - Composite: 47.2/100
   - Technical: 20.0, Fundamental: 73.0
4. **DT** - Composite: 48.8/100
   - Technical: 60.0, Fundamental: 37.0
5. **JEF** - Composite: 40.0/100
   - Technical: 30.0, Fundamental: 45.0

```json
{
  "market_conditions": {
    "spy_change_pct": 0.619446931299783,
    "vix": 19.020000457763672,
    "vix_status": "NORMAL",
    "date": "2026-02-20"
  },
  "candidates": [
    {
      "ticker": "APO",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 58.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.2,
      "current_price": 120.19000244140625
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
        "score": 67.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.8,
      "current_price": 53.57500076293945
    },
    {
      "ticker": "CTSH",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 73.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.2,
      "current_price": 64.86000061035156
    },
    {
      "ticker": "DT",
      "technical": {
        "score": 60.0,
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
      "composite_score": 48.8,
      "current_price": 36.4900016784668
    },
    {
      "ticker": "JEF",
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
      "current_price": 53.185001373291016
    },
    {
      "ticker": "MGM",
      "technical": {
        "score": 85.0,
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
      "composite_score": 62.0,
      "current_price": 36.36000061035156
    },
    {
      "ticker": "ARES",
      "technical": {
        "score": 30.0,
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
      "composite_score": 34.0,
      "current_price": 127.93000030517578
    },
    {
      "ticker": "AS",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 70.0,
      "current_price": 42.23500061035156
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
        "score": 37.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.8,
      "current_price": 68.41500091552734
    },
    {
      "ticker": "BBY",
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
      "current_price": 65.11499786376953
    },
    {
      "ticker": "BROS",
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
      "current_price": 48.47999954223633
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
      "current_price": 32.797298431396484
    },
    {
      "ticker": "BX",
      "technical": {
        "score": 20.0,
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
      "composite_score": 41.6,
      "current_price": 124.16000366210938
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
        "score": 38.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 37.2,
      "current_price": 37.61000061035156
    },
    {
      "ticker": "CRBG",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 22.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 30.8,
      "current_price": 29.600000381469727
    },
    {
      "ticker": "DEI",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 26.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 32.4,
      "current_price": 10.239999771118164
    },
    {
      "ticker": "EBAY",
      "technical": {
        "score": 30.0,
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
      "composite_score": 44.400000000000006,
      "current_price": 87.83000183105469
    },
    {
      "ticker": "FTNT",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 82.76000213623047
    },
    {
      "ticker": "FTV",
      "technical": {
        "score": 70.0,
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
      "composite_score": 48.4,
      "current_price": 58.31999969482422
    },
    {
      "ticker": "G",
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
      "current_price": 38.625
    },
    {
      "ticker": "GTX",
      "technical": {
        "score": 45.0,
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
      "composite_score": 44.400000000000006,
      "current_price": 19.049999237060547
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
        "score": 29.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.6,
      "current_price": 18.33009910583496
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
        "score": 18.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 29.2,
      "current_price": 26.360000610351562
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
        "score": 61.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 68.4,
      "current_price": 31.31999969482422
    },
    {
      "ticker": "OBDC",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 54.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 55.6,
      "current_price": 11.524999618530273
    },
    {
      "ticker": "OWL",
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
      "current_price": 11.21500015258789
    },
    {
      "ticker": "ROKU",
      "technical": {
        "score": 60.0,
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
      "composite_score": 46.8,
      "current_price": 89.75749969482422
    },
    {
      "ticker": "SFM",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 67.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.8,
      "current_price": 65.94999694824219
    },
    {
      "ticker": "SIRI",
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
      "current_price": 20.7549991607666
    },
    {
      "ticker": "TWLO",
      "technical": {
        "score": 60.0,
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
      "composite_score": 48.8,
      "current_price": 113.83999633789062
    },
    {
      "ticker": "AAL",
      "technical": {
        "score": 30.0,
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
      "composite_score": 31.6,
      "current_price": 13.42650032043457
    },
    {
      "ticker": "ABNB",
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
      "current_price": 126.12999725341797
    },
    {
      "ticker": "ACI",
      "technical": {
        "score": 100.0,
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
      "composite_score": 65.6,
      "current_price": 17.69499969482422
    },
    {
      "ticker": "ACN",
      "technical": {
        "score": 20.0,
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
      "composite_score": 39.2,
      "current_price": 214.11000061035156
    },
    {
      "ticker": "ADMA",
      "technical": {
        "score": 60.0,
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
      "composite_score": 58.8,
      "current_price": 16.43000030517578
    },
    {
      "ticker": "AFRM",
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
      "current_price": 51.95000076293945
    },
    {
      "ticker": "AG",
      "technical": {
        "score": 70.0,
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
      "composite_score": 55.2,
      "current_price": 25.139999389648438
    },
    {
      "ticker": "AI",
      "technical": {
        "score": 60.0,
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
      "composite_score": 42.0,
      "current_price": 10.729999542236328
    },
    {
      "ticker": "AKAM",
      "technical": {
        "score": 75.0,
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
      "composite_score": 63.2,
      "current_price": 99.45500183105469
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
      "current_price": 36.2599983215332
    },
    {
      "ticker": "ALK",
      "technical": {
        "score": 45.0,
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
      "composite_score": 35.6,
      "current_price": 52.185001373291016
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
      "current_price": 48.6150016784668
    },
    {
      "ticker": "APTV",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 26.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 38.4,
      "current_price": 80.29000091552734
    },
    {
      "ticker": "AXTA",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 48.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 69.2,
      "current_price": 34.709999084472656
    },
    {
      "ticker": "B",
      "technical": {
        "score": 70.0,
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
      "composite_score": 72.0,
      "current_price": 48.54999923706055
    },
    {
      "ticker": "BANC",
      "technical": {
        "score": 30.0,
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
      "composite_score": 50.0,
      "current_price": 19.809999465942383
    },
    {
      "ticker": "BAX",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 28.0,
        "sector": "Healthcare"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 61.2,
      "current_price": 21.21500015258789
    },
    {
      "ticker": "BILL",
      "technical": {
        "score": 85.0,
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
      "composite_score": 55.6,
      "current_price": 47.08000183105469
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
      "current_price": 32.76359939575195
    },
    {
      "ticker": "BRBR",
      "technical": {
        "score": 40.0,
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
      "composite_score": 44.8,
      "current_price": 19.149599075317383
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
      "current_price": 38.25
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
      "current_price": 69.45999908447266
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
        "score": 85.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 56.0,
      "current_price": 17.68000030517578
    },
    {
      "ticker": "C",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 49.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 41.6,
      "current_price": 115.55000305175781
    },
    {
      "ticker": "CADE",
      "technical": {
        "score": 30.0,
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
      "composite_score": 48.0,
      "current_price": 42.11000061035156
    },
    {
      "ticker": "CARR",
      "technical": {
        "score": 70.0,
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
      "composite_score": 48.8,
      "current_price": 63.744998931884766
    },
    {
      "ticker": "CART",
      "technical": {
        "score": 60.0,
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
      "composite_score": 57.2,
      "current_price": 35.84000015258789
    },
    {
      "ticker": "CAVA",
      "technical": {
        "score": 100.0,
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
      "composite_score": 69.2,
      "current_price": 68.0199966430664
    },
    {
      "ticker": "CCI",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 26.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.4,
      "current_price": 87.2699966430664
    },
    {
      "ticker": "CDE",
      "technical": {
        "score": 100.0,
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
      "composite_score": 78.0,
      "current_price": 23.635000228881836
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
        "score": 29.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 49.6,
      "current_price": 52.5
    },
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
      "current_price": 25.719999313354492
    },
    {
      "ticker": "CHYM",
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
      "current_price": 20.96500015258789
    },
    {
      "ticker": "CNM",
      "technical": {
        "score": 70.0,
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
      "composite_score": 56.400000000000006,
      "current_price": 56.54999923706055
    },
    {
      "ticker": "COGT",
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
      "current_price": 37.83000183105469
    },
    {
      "ticker": "COIN",
      "technical": {
        "score": 60.0,
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
      "composite_score": 50.0,
      "current_price": 174.1199951171875
    },
    {
      "ticker": "COMM",
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
      "current_price": 18.540000915527344
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
        "score": 22.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 36.8,
      "current_price": 17.75
    },
    {
      "ticker": "CPRI",
      "technical": {
        "score": 85.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 4.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.6,
      "current_price": 21.559999465942383
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
        "score": 72.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.8,
      "current_price": 37.650001525878906
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
      "current_price": 65.12999725341797
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
      "current_price": 50.41999816894531
    },
    {
      "ticker": "CWAN",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 39.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 37.6,
      "current_price": 23.395000457763672
    }
  ],
  "current_holdings": [
    {
      "ticker": "AEM",
      "technical_score": 90.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 224.1649932861328,
      "sector": "Basic Materials",
      "quantity": 31.0,
      "market_value": 6925.245,
      "cost_basis": 5881.63,
      "unrealized_pl": 1043.615,
      "unrealized_plpc": 17.744
    },
    {
      "ticker": "AES",
      "technical_score": 90.0,
      "fundamental_score": 45.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 16.399999618530273,
      "sector": "Utilities",
      "quantity": 385.0,
      "market_value": 6304.375,
      "cost_basis": 5990.6,
      "unrealized_pl": 313.775,
      "unrealized_plpc": 5.238
    },
    {
      "ticker": "AGI",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 45.83000183105469,
      "sector": "Basic Materials",
      "quantity": 224.0,
      "market_value": 10232.32,
      "cost_basis": 10035.2,
      "unrealized_pl": 197.12,
      "unrealized_plpc": 1.9640000000000002
    },
    {
      "ticker": "ANET",
      "technical_score": 45.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 60.0,
      "context": "holdings",
      "current_price": 137.97000122070312,
      "sector": "Technology",
      "quantity": 53.0,
      "market_value": 7308.17,
      "cost_basis": 7535.54,
      "unrealized_pl": -227.37,
      "unrealized_plpc": -3.017
    },
    {
      "ticker": "APG",
      "technical_score": 60.0,
      "fundamental_score": 39.0,
      "sentiment_score": 50.0,
      "research_composite_score": 49.6,
      "context": "holdings",
      "current_price": 44.619998931884766,
      "sector": "Industrials",
      "quantity": 168.0,
      "market_value": 7494.48,
      "cost_basis": 7512.96,
      "unrealized_pl": -18.48,
      "unrealized_plpc": -0.246
    },
    {
      "ticker": "AU",
      "technical_score": 90.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.0,
      "context": "holdings",
      "current_price": 111.90499877929688,
      "sector": "Basic Materials",
      "quantity": 71.0,
      "market_value": 7912.95,
      "cost_basis": 7572.86,
      "unrealized_pl": 340.09,
      "unrealized_plpc": 4.491
    },
    {
      "ticker": "CF",
      "technical_score": 70.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 70.0,
      "context": "holdings",
      "current_price": 96.16999816894531,
      "sector": "Basic Materials",
      "quantity": 107.0,
      "market_value": 10280.56,
      "cost_basis": 9909.27,
      "unrealized_pl": 371.29,
      "unrealized_plpc": 3.7470000000000003
    },
    {
      "ticker": "CMCSA",
      "technical_score": 70.0,
      "fundamental_score": 49.0,
      "sentiment_score": 50.0,
      "research_composite_score": 57.6,
      "context": "holdings",
      "current_price": 31.284400939941406,
      "sector": "Communication Services",
      "quantity": 196.0,
      "market_value": 6130.88,
      "cost_basis": 5989.76,
      "unrealized_pl": 141.12,
      "unrealized_plpc": 2.3560000000000003
    },
    {
      "ticker": "DNOW",
      "technical_score": 30.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 44.8,
      "context": "holdings",
      "current_price": 13.210000038146973,
      "sector": "Industrials",
      "quantity": 467.0,
      "market_value": 6187.75,
      "cost_basis": 7514.03,
      "unrealized_pl": -1326.28,
      "unrealized_plpc": -17.651
    },
    {
      "ticker": "DOCN",
      "technical_score": 100.0,
      "fundamental_score": 64.0,
      "sentiment_score": 50.0,
      "research_composite_score": 75.6,
      "context": "holdings",
      "current_price": 65.94999694824219,
      "sector": "Technology",
      "quantity": 167.0,
      "market_value": 10947.685,
      "cost_basis": 10038.37,
      "unrealized_pl": 909.315,
      "unrealized_plpc": 9.058
    },
    {
      "ticker": "RRC",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 38.939998626708984,
      "sector": "Energy",
      "quantity": 167.0,
      "market_value": 6492.96,
      "cost_basis": 5980.27,
      "unrealized_pl": 512.69,
      "unrealized_plpc": 8.573
    }
  ],
  "screening": {
    "universe_size": 84,
    "candidates_found": 73,
    "holdings_count": 11,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
