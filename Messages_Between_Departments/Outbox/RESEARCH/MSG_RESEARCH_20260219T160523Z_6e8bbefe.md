---
from: RESEARCH
message_id: MSG_RESEARCH_20260219T160523Z_6e8bbefe
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-02-19T16:05:23.995118Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-02-19

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -0.24%
- **VIX**: 20.1 (ELEVATED)

### Candidate Summary
- **Buy Candidates**: 70 swing-suitable stocks
- **Current Holdings**: 12 positions from Alpaca
- **Total Scored**: 82 stocks

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
2. **CG** - Composite: 50.8/100
   - Technical: 30.0, Fundamental: 72.0
3. **CTSH** - Composite: 47.2/100
   - Technical: 20.0, Fundamental: 73.0
4. **DT** - Composite: 48.8/100
   - Technical: 60.0, Fundamental: 37.0
5. **JEF** - Composite: 40.0/100
   - Technical: 30.0, Fundamental: 45.0

```json
{
  "market_conditions": {
    "spy_change_pct": -0.23968854984914856,
    "vix": 20.079999923706055,
    "vix_status": "ELEVATED",
    "date": "2026-02-19"
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
      "current_price": 118.38999938964844
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
        "score": 72.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 50.8,
      "current_price": 52.09000015258789
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
      "current_price": 64.29499816894531
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
      "current_price": 36.20000076293945
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
      "current_price": 53.45000076293945
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
        "score": 80.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 70.0,
      "current_price": 48.220001220703125
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
      "current_price": 72.13999938964844
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
      "current_price": 51.529998779296875
    },
    {
      "ticker": "BTU",
      "technical": {
        "score": 45.0,
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
      "composite_score": 34.8,
      "current_price": 33.7400016784668
    },
    {
      "ticker": "BX",
      "technical": {
        "score": 30.0,
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
      "composite_score": 45.6,
      "current_price": 125.62000274658203
    },
    {
      "ticker": "DLO",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 64.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 47.6,
      "current_price": 12.664999961853027
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
      "current_price": 86.44999694824219
    },
    {
      "ticker": "FLEX",
      "technical": {
        "score": 85.0,
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
      "composite_score": 60.8,
      "current_price": 65.41000366210938
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
      "current_price": 13.305000305175781
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
        "score": 50.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.0,
      "current_price": 80.5
    },
    {
      "ticker": "G",
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
      "current_price": 38.720001220703125
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
      "current_price": 18.344999313354492
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
        "score": 61.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.400000000000006,
      "current_price": 30.479999542236328
    },
    {
      "ticker": "NU",
      "technical": {
        "score": 45.0,
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
      "composite_score": 52.0,
      "current_price": 17.40999984741211
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
      "current_price": 12.3100004196167
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
        "score": 27.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 44.8,
      "current_price": 89.7300033569336
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
      "current_price": 21.059999465942383
    },
    {
      "ticker": "TWLO",
      "technical": {
        "score": 20.0,
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
      "composite_score": 32.8,
      "current_price": 110.62000274658203
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
        "score": 60.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.0,
      "current_price": 60.209999084472656
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
      "current_price": 13.354999542236328
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
        "score": 46.0,
        "sector": "Consumer Cyclical"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.400000000000006,
      "current_price": 124.2699966430664
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
      "current_price": 212.19500732421875
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
      "current_price": 16.290000915527344
    },
    {
      "ticker": "AFRM",
      "technical": {
        "score": 20.0,
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
      "composite_score": 39.2,
      "current_price": 51.39500045776367
    },
    {
      "ticker": "AI",
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
      "current_price": 10.484999656677246
    },
    {
      "ticker": "ALB",
      "technical": {
        "score": 45.0,
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
      "composite_score": 40.8,
      "current_price": 169.36000061035156
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
      "current_price": 36.959999084472656
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
      "current_price": 52.439998626708984
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
        "score": 66.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 48.400000000000006,
      "current_price": 41.38999938964844
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
        "score": 58.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 45.2,
      "current_price": 46.7400016784668
    },
    {
      "ticker": "APTV",
      "technical": {
        "score": 75.0,
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
      "composite_score": 50.4,
      "current_price": 79.98999786376953
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
      "current_price": 126.12999725341797
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
        "score": 43.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 67.2,
      "current_price": 34.84000015258789
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
      "current_price": 19.829999923706055
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
      "current_price": 21.415000915527344
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
      "current_price": 66.19999694824219
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
      "current_price": 45.209999084472656
    },
    {
      "ticker": "BLSH",
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
      "current_price": 31.155000686645508
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
      "current_price": 69.2300033569336
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
      "current_price": 17.424999237060547
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
      "current_price": 115.3499984741211
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
      "current_price": 62.887001037597656
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
      "current_price": 87.08999633789062
    },
    {
      "ticker": "CCJ",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 47.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 116.5
    },
    {
      "ticker": "CDE",
      "technical": {
        "score": 70.0,
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
      "composite_score": 62.8,
      "current_price": 24.325000762939453
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
      "current_price": 49.525001525878906
    },
    {
      "ticker": "CHWY",
      "technical": {
        "score": 20.0,
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
      "composite_score": 34.400000000000006,
      "current_price": 25.342199325561523
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
      "current_price": 20.389999389648438
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
      "current_price": 37.88999938964844
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
      "current_price": 38.334999084472656
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
        "score": 45.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.0,
      "current_price": 163.05499267578125
    },
    {
      "ticker": "COMM",
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
      "current_price": 18.90999984741211
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
      "current_price": 17.55500030517578
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
      "current_price": 18.475000381469727
    },
    {
      "ticker": "CPRI",
      "technical": {
        "score": 60.0,
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
      "composite_score": 35.6,
      "current_price": 20.790000915527344
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
      "current_price": 37.744998931884766
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
      "current_price": 30.485000610351562
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
        "score": 21.0,
        "sector": "Financial Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.4,
      "current_price": 60.9375
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
      "current_price": 19.966299057006836
    },
    {
      "ticker": "CRWV",
      "technical": {
        "score": 70.0,
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
      "composite_score": 42.8,
      "current_price": 95.49500274658203
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
      "current_price": 48.81999969482422
    },
    {
      "ticker": "CWAN",
      "technical": {
        "score": 45.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 64.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.6,
      "current_price": 23.4950008392334
    },
    {
      "ticker": "CX",
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
      "current_price": 12.6899995803833
    },
    {
      "ticker": "CZR",
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
      "current_price": 21.40999984741211
    }
  ],
  "current_holdings": [
    {
      "ticker": "AEM",
      "technical_score": 100.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 82.0,
      "context": "holdings",
      "current_price": 222.82000732421875,
      "sector": "Basic Materials",
      "quantity": 31.0,
      "market_value": 6938.73,
      "cost_basis": 5881.63,
      "unrealized_pl": 1057.1,
      "unrealized_plpc": 17.973
    },
    {
      "ticker": "AES",
      "technical_score": 90.0,
      "fundamental_score": 45.0,
      "sentiment_score": 50.0,
      "research_composite_score": 64.0,
      "context": "holdings",
      "current_price": 16.34000015258789,
      "sector": "Utilities",
      "quantity": 385.0,
      "market_value": 6294.75,
      "cost_basis": 5990.6,
      "unrealized_pl": 304.15,
      "unrealized_plpc": 5.077
    },
    {
      "ticker": "AGI",
      "technical_score": 100.0,
      "fundamental_score": 62.0,
      "sentiment_score": 50.0,
      "research_composite_score": 74.8,
      "context": "holdings",
      "current_price": 43.7400016784668,
      "sector": "Basic Materials",
      "quantity": 224.0,
      "market_value": 10328.64,
      "cost_basis": 10035.2,
      "unrealized_pl": 293.44,
      "unrealized_plpc": 2.924
    },
    {
      "ticker": "ANET",
      "technical_score": 45.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 60.0,
      "context": "holdings",
      "current_price": 139.5399932861328,
      "sector": "Technology",
      "quantity": 53.0,
      "market_value": 7248.81,
      "cost_basis": 7535.54,
      "unrealized_pl": -286.73,
      "unrealized_plpc": -3.805
    },
    {
      "ticker": "APG",
      "technical_score": 100.0,
      "fundamental_score": 39.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.6,
      "context": "holdings",
      "current_price": 44.15999984741211,
      "sector": "Industrials",
      "quantity": 168.0,
      "market_value": 7444.08,
      "cost_basis": 7512.96,
      "unrealized_pl": -68.88,
      "unrealized_plpc": -0.9169999999999999
    },
    {
      "ticker": "AU",
      "technical_score": 70.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 66.0,
      "context": "holdings",
      "current_price": 107.44999694824219,
      "sector": "Basic Materials",
      "quantity": 71.0,
      "market_value": 7637.47,
      "cost_basis": 7572.86,
      "unrealized_pl": 64.61,
      "unrealized_plpc": 0.853
    },
    {
      "ticker": "CF",
      "technical_score": 100.0,
      "fundamental_score": 80.0,
      "sentiment_score": 50.0,
      "research_composite_score": 82.0,
      "context": "holdings",
      "current_price": 101.30500030517578,
      "sector": "Basic Materials",
      "quantity": 107.0,
      "market_value": 10840.17,
      "cost_basis": 9909.27,
      "unrealized_pl": 930.9,
      "unrealized_plpc": 9.394
    },
    {
      "ticker": "CMCSA",
      "technical_score": 90.0,
      "fundamental_score": 49.0,
      "sentiment_score": 50.0,
      "research_composite_score": 65.6,
      "context": "holdings",
      "current_price": 31.600000381469727,
      "sector": "Communication Services",
      "quantity": 196.0,
      "market_value": 6168.12,
      "cost_basis": 5989.76,
      "unrealized_pl": 178.36,
      "unrealized_plpc": 2.978
    },
    {
      "ticker": "CNM",
      "technical_score": 45.0,
      "fundamental_score": 46.0,
      "sentiment_score": 50.0,
      "research_composite_score": 46.400000000000006,
      "context": "holdings",
      "current_price": 56.130001068115234,
      "sector": "Industrials",
      "quantity": 173.0,
      "market_value": 9718.275,
      "cost_basis": 9964.8,
      "unrealized_pl": -246.525,
      "unrealized_plpc": -2.474
    },
    {
      "ticker": "DNOW",
      "technical_score": 70.0,
      "fundamental_score": 57.0,
      "sentiment_score": 50.0,
      "research_composite_score": 60.8,
      "context": "holdings",
      "current_price": 16.280000686645508,
      "sector": "Industrials",
      "quantity": 467.0,
      "market_value": 7612.1,
      "cost_basis": 7514.03,
      "unrealized_pl": 98.07,
      "unrealized_plpc": 1.3050000000000002
    },
    {
      "ticker": "DOCN",
      "technical_score": 90.0,
      "fundamental_score": 64.0,
      "sentiment_score": 50.0,
      "research_composite_score": 71.6,
      "context": "holdings",
      "current_price": 68.05999755859375,
      "sector": "Technology",
      "quantity": 167.0,
      "market_value": 11377.71,
      "cost_basis": 10038.37,
      "unrealized_pl": 1339.34,
      "unrealized_plpc": 13.342
    },
    {
      "ticker": "RRC",
      "technical_score": 100.0,
      "fundamental_score": 70.0,
      "sentiment_score": 50.0,
      "research_composite_score": 78.0,
      "context": "holdings",
      "current_price": 39.11000061035156,
      "sector": "Energy",
      "quantity": 167.0,
      "market_value": 6554.75,
      "cost_basis": 5980.27,
      "unrealized_pl": 574.48,
      "unrealized_plpc": 9.606
    }
  ],
  "screening": {
    "universe_size": 82,
    "candidates_found": 70,
    "holdings_count": 12,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
