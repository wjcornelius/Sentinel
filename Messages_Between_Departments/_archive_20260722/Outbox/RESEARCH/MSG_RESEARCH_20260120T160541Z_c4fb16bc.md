---
from: RESEARCH
message_id: MSG_RESEARCH_20260120T160541Z_c4fb16bc
message_type: DailyBriefing
priority: routine
requires_response: false
timestamp: '2026-01-20T16:05:41.478569Z'
to: PORTFOLIO
---

# Daily Market Briefing - 2026-01-20

## Research Department v3.0 - Two-Stage Filtering

### Market Conditions
- **SPY Change**: -1.20%
- **VIX**: 19.0 (NORMAL)

### Candidate Summary
- **Buy Candidates**: 73 swing-suitable stocks
- **Current Holdings**: 2 positions from Alpaca
- **Total Scored**: 75 stocks

### Filtering Process
1. Stage 1: Swing suitability scoring (volatility, liquidity, ATR)
2. Stage 2: Technical analysis (RSI, MACD, trend)
3. Output: Candidates with BOTH swing suitability AND technical setups

### Note on Sentiment
All stocks have sentiment_score = 50.0 (neutral placeholder)
News Department will enrich with Perplexity sentiment analysis

### Top Candidates
1. **KVYO** - Composite: 22.8/100
   - Technical: 10.0, Fundamental: 22.0
2. **MBLY** - Composite: 35.6/100
   - Technical: 30.0, Fundamental: 34.0
3. **ABNB** - Composite: 46.4/100
   - Technical: 45.0, Fundamental: 46.0
4. **ADM** - Composite: 64.4/100
   - Technical: 90.0, Fundamental: 46.0
5. **AES** - Composite: 40.0/100
   - Technical: 30.0, Fundamental: 45.0

```json
{
  "market_conditions": {
    "spy_change_pct": -1.198562639045686,
    "vix": 19.0,
    "vix_status": "NORMAL",
    "date": "2026-01-20"
  },
  "candidates": [
    {
      "ticker": "KVYO",
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
      "current_price": 24.314300537109375
    },
    {
      "ticker": "MBLY",
      "technical": {
        "score": 30.0,
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
      "composite_score": 35.6,
      "current_price": 10.658599853515625
    },
    {
      "ticker": "ABNB",
      "technical": {
        "score": 45.0,
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
      "composite_score": 46.400000000000006,
      "current_price": 131.7100067138672
    },
    {
      "ticker": "ADM",
      "technical": {
        "score": 90.0,
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
      "composite_score": 64.4,
      "current_price": 65.19000244140625
    },
    {
      "ticker": "AES",
      "technical": {
        "score": 30.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 45.0,
        "sector": "Utilities"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.0,
      "current_price": 13.75
    },
    {
      "ticker": "AG",
      "technical": {
        "score": 90.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 35.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 60.0,
      "current_price": 22.180099487304688
    },
    {
      "ticker": "ALAB",
      "technical": {
        "score": 100.0,
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
      "composite_score": 70.8,
      "current_price": 186.76010131835938
    },
    {
      "ticker": "ALLY",
      "technical": {
        "score": 35.0,
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
      "composite_score": 45.2,
      "current_price": 43.11000061035156
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
        "score": 39.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.6,
      "current_price": 48.0
    },
    {
      "ticker": "APG",
      "technical": {
        "score": 100.0,
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
      "composite_score": 65.6,
      "current_price": 42.584999084472656
    },
    {
      "ticker": "APLD",
      "technical": {
        "score": 90.0,
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
      "composite_score": 54.8,
      "current_price": 34.744998931884766
    },
    {
      "ticker": "APLS",
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
      "current_price": 19.94499969482422
    },
    {
      "ticker": "APO",
      "technical": {
        "score": 45.0,
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
      "composite_score": 56.8,
      "current_price": 142.5500030517578
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
      "current_price": 168.52000427246094
    },
    {
      "ticker": "ARM",
      "technical": {
        "score": 60.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 60.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 58.0,
      "current_price": 109.41999816894531
    },
    {
      "ticker": "ASAN",
      "technical": {
        "score": 10.0,
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
      "composite_score": 18.8,
      "current_price": 10.760000228881836
    },
    {
      "ticker": "ASTS",
      "technical": {
        "score": 90.0,
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
      "composite_score": 54.8,
      "current_price": 114.69499969482422
    },
    {
      "ticker": "ATEC",
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
      "current_price": 17.350000381469727
    },
    {
      "ticker": "AXTA",
      "technical": {
        "score": 70.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 61.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.400000000000006,
      "current_price": 33.16999816894531
    },
    {
      "ticker": "BBY",
      "technical": {
        "score": 30.0,
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
      "composite_score": 35.2,
      "current_price": 66.56999969482422
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
        "score": 31.0,
        "sector": "Real Estate"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 56.4,
      "current_price": 17.969999313354492
    },
    {
      "ticker": "BKR",
      "technical": {
        "score": 75.0,
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
      "composite_score": 61.6,
      "current_price": 51.404998779296875
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
      "current_price": 29.040000915527344
    },
    {
      "ticker": "BTDR",
      "technical": {
        "score": 75.0,
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
      "composite_score": 44.8,
      "current_price": 14.90999984741211
    },
    {
      "ticker": "BWA",
      "technical": {
        "score": 45.0,
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
      "composite_score": 39.6,
      "current_price": 46.59000015258789
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
      "current_price": 159.17999267578125
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
        "score": 80.0,
        "sector": "Communication Services"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 54.0,
      "current_price": 19.110000610351562
    },
    {
      "ticker": "C",
      "technical": {
        "score": 45.0,
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
      "composite_score": 47.6,
      "current_price": 115.87000274658203
    },
    {
      "ticker": "CARR",
      "technical": {
        "score": 100.0,
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
      "composite_score": 63.2,
      "current_price": 55.209999084472656
    },
    {
      "ticker": "CF",
      "technical": {
        "score": 90.0,
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
      "composite_score": 80.0,
      "current_price": 89.0
    },
    {
      "ticker": "CG",
      "technical": {
        "score": 70.0,
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
      "composite_score": 52.8,
      "current_price": 64.08000183105469
    },
    {
      "ticker": "CHWY",
      "technical": {
        "score": 85.0,
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
      "composite_score": 60.400000000000006,
      "current_price": 33.36000061035156
    },
    {
      "ticker": "CIFR",
      "technical": {
        "score": 85.0,
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
      "composite_score": 52.8,
      "current_price": 18.399999618530273
    },
    {
      "ticker": "CLSK",
      "technical": {
        "score": 85.0,
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
      "composite_score": 72.8,
      "current_price": 12.95009994506836
    },
    {
      "ticker": "CMCSA",
      "technical": {
        "score": 70.0,
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
      "composite_score": 54.0,
      "current_price": 28.174999237060547
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
      "current_price": 56.845001220703125
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
      "current_price": 195.48500061035156
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
      "current_price": 30.184999465942383
    },
    {
      "ticker": "CRDO",
      "technical": {
        "score": 85.0,
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
      "composite_score": 66.8,
      "current_price": 156.19000244140625
    },
    {
      "ticker": "CRWV",
      "technical": {
        "score": 90.0,
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
      "composite_score": 50.8,
      "current_price": 95.34230041503906
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
      "current_price": 64.45999908447266
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
      "current_price": 18.014999389648438
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
      "current_price": 12.505000114440918
    },
    {
      "ticker": "DAR",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.0,
      "current_price": 39.34000015258789
    },
    {
      "ticker": "DBX",
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
      "current_price": 26.045000076293945
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
      "current_price": 42.224998474121094
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
      "current_price": 10.739999771118164
    },
    {
      "ticker": "DT",
      "technical": {
        "score": 20.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 72.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 46.8,
      "current_price": 39.599998474121094
    },
    {
      "ticker": "DVN",
      "technical": {
        "score": 100.0,
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
      "composite_score": 71.2,
      "current_price": 36.86000061035156
    },
    {
      "ticker": "DYN",
      "technical": {
        "score": 20.0,
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
      "composite_score": 24.0,
      "current_price": 16.405000686645508
    },
    {
      "ticker": "EBC",
      "technical": {
        "score": 100.0,
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
      "composite_score": 64.0,
      "current_price": 19.225000381469727
    },
    {
      "ticker": "EL",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 8.0,
        "sector": "Consumer Defensive"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 53.2,
      "current_price": 114.08999633789062
    },
    {
      "ticker": "ELAN",
      "technical": {
        "score": 90.0,
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
      "composite_score": 60.8,
      "current_price": 24.770000457763672
    },
    {
      "ticker": "EMR",
      "technical": {
        "score": 90.0,
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
      "composite_score": 57.6,
      "current_price": 147.1999969482422
    },
    {
      "ticker": "EQH",
      "technical": {
        "score": 45.0,
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
      "composite_score": 36.0,
      "current_price": 46.709999084472656
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
        "score": 52.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 42.8,
      "current_price": 51.125
    },
    {
      "ticker": "EXE",
      "technical": {
        "score": 30.0,
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
      "composite_score": 36.0,
      "current_price": 103.91000366210938
    },
    {
      "ticker": "FCX",
      "technical": {
        "score": 90.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 50.0,
        "sector": "Basic Materials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 66.0,
      "current_price": 59.960899353027344
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
      "current_price": 12.779999732971191
    },
    {
      "ticker": "FLNC",
      "technical": {
        "score": 100.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 7.0,
        "sector": "Utilities"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 52.8,
      "current_price": 25.239999771118164
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
        "score": 39.0,
        "sector": "Technology"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 49.6,
      "current_price": 63.6150016784668
    },
    {
      "ticker": "FRSH",
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
      "current_price": 11.100000381469727
    },
    {
      "ticker": "FTNT",
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
      "current_price": 75.48999786376953
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
      "current_price": 79.55999755859375
    },
    {
      "ticker": "GFS",
      "technical": {
        "score": 90.0,
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
      "composite_score": 59.2,
      "current_price": 43.68000030517578
    },
    {
      "ticker": "GILD",
      "technical": {
        "score": 100.0,
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
      "composite_score": 74.4,
      "current_price": 124.91000366210938
    },
    {
      "ticker": "GM",
      "technical": {
        "score": 45.0,
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
      "composite_score": 39.6,
      "current_price": 78.75
    },
    {
      "ticker": "GME",
      "technical": {
        "score": 60.0,
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
      "composite_score": 55.6,
      "current_price": 21.045000076293945
    },
    {
      "ticker": "GNTX",
      "technical": {
        "score": 45.0,
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
      "composite_score": 59.2,
      "current_price": 23.56999969482422
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
        "score": 57.0,
        "sector": "Industrials"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 40.8,
      "current_price": 73.87999725341797
    },
    {
      "ticker": "HAL",
      "technical": {
        "score": 90.0,
        "rsi": null,
        "macd": null,
        "details": "new_buys"
      },
      "fundamental": {
        "score": 40.0,
        "sector": "Energy"
      },
      "sentiment": {
        "score": 50.0,
        "summary": "Pending News Department analysis",
        "news_count": 0
      },
      "composite_score": 62.0,
      "current_price": 32.529998779296875
    },
    {
      "ticker": "HALO",
      "technical": {
        "score": 45.0,
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
      "composite_score": 56.8,
      "current_price": 70.33000183105469
    },
    {
      "ticker": "HPE",
      "technical": {
        "score": 10.0,
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
      "composite_score": 24.4,
      "current_price": 20.485000610351562
    }
  ],
  "current_holdings": [
    {
      "ticker": "ESI",
      "technical_score": 90.0,
      "fundamental_score": 42.0,
      "sentiment_score": 50.0,
      "research_composite_score": 62.8,
      "context": "holdings",
      "current_price": 28.832500457763672,
      "sector": "Basic Materials",
      "quantity": 372.0,
      "market_value": 10737.78,
      "cost_basis": 10021.68,
      "unrealized_pl": 716.1,
      "unrealized_plpc": 7.145508537490721
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
    }
  ],
  "screening": {
    "universe_size": 75,
    "candidates_found": 73,
    "holdings_count": 2,
    "filtering_method": "two_stage_swing_suitability",
    "version": "3.0"
  }
}
```
