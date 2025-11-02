# WEEK 2 DAY 1 STATUS: Research Department Foundation

**Date:** 2025-10-31
**Status:** 🟢 **IN PROGRESS** - Database Schema Complete
**Hours Spent:** ~2-3 hours
**Lines Written:** 239 lines (database schema)

---

## EXECUTIVE SUMMARY

**Week 2 Goal:** Build Research Department with Perplexity + yfinance + pandas-ta integration.

**Day 1 Achievement:** ✅ **Database schema designed and initialized with revolutionary message tracking.**

**What's Complete:**
- 6 database tables designed FROM DEPARTMENTAL_SPECIFICATIONS
- Message chain tracking in ALL tables
- Sentiment caching strategy (24-hour window)
- API call logging for rate limit management

**What's Next:**
- Build Python classes (MarketDataCollector, SentimentAnalyzer, TechnicalAnalyzer, FundamentalAnalyzer)
- Implement DailyBriefing message generation
- Test with 10 stock candidates

---

## DATABASE SCHEMA DESIGN

### Revolutionary Features (v6.2 Didn't Have)

**1. Message Chain Tracking**
```sql
-- research_market_briefings table
message_id TEXT UNIQUE NOT NULL  -- Links to message sent to Risk/Portfolio
```

**2. Request/Response Message Links**
```sql
-- research_ticker_analyses table
request_message_id TEXT           -- Link to request message
response_message_id TEXT UNIQUE NOT NULL  -- Link to response message
```

**3. Sentiment Caching (Cost Optimization)**
```sql
-- research_sentiment_cache table
ticker TEXT NOT NULL,
query_date DATE NOT NULL,
expires_at DATETIME NOT NULL  -- Cache expires after 24 hours
UNIQUE(ticker, query_date)
```

**4. API Call Logging (Rate Limit Management)**
```sql
-- research_api_calls table
api_name TEXT NOT NULL CHECK(api_name IN ('PERPLEXITY', 'YFINANCE', 'ALPACA', 'ALPHA_VANTAGE', 'FRED')),
rate_limit_remaining INTEGER,
rate_limit_reset DATETIME
```

### Tables Created

#### 1. research_market_briefings
**Purpose:** Daily market condition summaries (VIX, sectors, indices)

**Key Fields:**
- Market indices: SPY, QQQ, DIA with % changes
- VIX level and status (NORMAL/ELEVATED/CAUTION/PANIC)
- Top 3 / Bottom 3 sectors with performance
- Market sentiment (BULLISH/NEUTRAL/BEARISH)
- **message_id** - Links to DailyBriefing message sent to Risk/Portfolio

**Design Decision:** Built FOR daily briefing workflow (not adapted from v6.2)

#### 2. research_ticker_analyses
**Purpose:** Individual stock research (fundamentals + technicals + sentiment)

**Key Fields:**
- Price data: current, 1d/5d/20d changes
- Volume: 30-day average, current, ratio
- Fundamentals: P/E, PEG, revenue growth, margins, debt-to-equity
- Technicals: RSI, MACD, Bollinger Bands
- Sentiment: 1-10 score, summary, news count
- Composite scores: technical_score, fundamental_score, overall_score
- **request_message_id** - Link to analysis request
- **response_message_id** - Link to analysis report message

**Design Decision:** Comprehensive scoring system for Portfolio Department to evaluate candidates

#### 3. research_news_events
**Purpose:** Track major market-moving events

**Key Fields:**
- Event type: EARNINGS, ECONOMIC_DATA, FED_ANNOUNCEMENT, GEOPOLITICAL, etc.
- Impact level: LOW, MEDIUM, HIGH, CRITICAL
- Affected tickers/sectors
- Market reaction (SPY move %)
- **alert_message_id** - Link to alert message sent to Executive

**Design Decision:** Enables historical analysis of market events and responses

#### 4. research_candidate_tickers
**Purpose:** Daily screening results (10-20 candidates)

**Key Fields:**
- Rank (1 = top candidate)
- Catalyst (what makes this ticker interesting)
- Catalyst type: MOMENTUM, VALUE, NEWS, TECHNICAL, FUNDAMENTAL, SENTIMENT
- Quick scores: overall, sentiment, technical
- **candidate_list_message_id** - Link to daily candidate list message

**Design Decision:** Supports Portfolio Department's daily workflow

#### 5. research_sentiment_cache
**Purpose:** Cache Perplexity API results to reduce costs

**Key Fields:**
- ticker, query_date (unique constraint)
- sentiment_score (1-10)
- sentiment_summary
- perplexity_response (full JSON for debugging)
- expires_at (24-hour cache window)

**Design Decision:** Perplexity API costs $$ - caching reduces duplicate calls

#### 6. research_api_calls
**Purpose:** Track API usage for rate limit management

**Key Fields:**
- api_name (PERPLEXITY, YFINANCE, ALPACA, etc.)
- response_status (SUCCESS, ERROR, TIMEOUT, RATE_LIMITED)
- response_time_ms
- rate_limit_remaining, rate_limit_reset

**Design Decision:** Proactive rate limit management (avoid hitting limits mid-day)

---

## EVIDENCE OF FRESH BUILD

### Schema Comparison

**v6.2 Approach (Monolithic):**
```python
# v6.2 had no Research Department
# Market data fetched inline in sentinel_morning_workflow.py
# No database tracking of analyses
# No message protocol
```

**Sentinel Corporation (Institutional):**
```sql
-- 6 specialized tables designed FOR Research Department
-- Message chain tracking in ALL tables
-- Sentiment cache (cost optimization)
-- API call log (rate limit management)
-- Built from DEPARTMENTAL_SPECIFICATIONS v1.0
```

### Key Design Decisions

**1. Message Tracking in Every Table**
- `message_id` fields enable complete audit trail
- `request_message_id` / `response_message_id` track message chains
- Portfolio can trace: "Why did we get this candidate?" → Research analysis → Market briefing → News event

**2. Sentiment Caching Strategy**
- 24-hour cache window (sentiment doesn't change much intraday)
- Reduces Perplexity API costs (potentially 50-70% reduction)
- Unique constraint on (ticker, query_date) prevents duplicates

**3. API Call Logging**
- Track ALL API calls (not just failures)
- Monitor rate limits proactively
- Response time tracking (identify slow APIs)
- Enable debugging ("Why did this take 30 seconds?")

**4. Composite Scoring System**
- technical_score (1-10) - RSI, MACD, Bollinger Bands
- fundamental_score (1-10) - P/E, growth, margins
- sentiment_score (1-10) - Perplexity news analysis
- overall_score (1-10) - Weighted composite
- Portfolio can filter candidates by score

---

## NEXT STEPS (Day 2)

### Python Implementation Plan

**1. MessageHandler Class (2-3 hours)**
- Reuse pattern from Trading Department
- YAML frontmatter + Markdown + JSON payload
- Inbox/Outbox/Archive handling

**2. MarketDataCollector Class (4-5 hours)**
- yfinance integration (price, volume, indices)
- Alpaca API integration (real-time data)
- VIX monitoring
- Sector performance calculation

**3. SentimentAnalyzer Class (5-6 hours)**
- Perplexity API integration
- Sentiment scoring (1-10 scale)
- Keyword-based analysis (bullish/bearish terms)
- Cache management (read from cache, write to cache)
- Rate limit handling

**4. TechnicalAnalyzer Class (3-4 hours)**
- pandas-ta integration
- RSI calculation
- MACD calculation
- Bollinger Bands calculation
- Technical score composite (1-10)

**5. FundamentalAnalyzer Class (3-4 hours)**
- yfinance fundamentals (P/E, revenue, margins)
- Growth metrics (YoY comparisons)
- Debt-to-equity, profitability
- Fundamental score composite (1-10)

**6. DailyBriefing Generation (4-5 hours)**
- Orchestrate all collectors/analyzers
- Generate market briefing message
- Generate candidate ticker list message
- Store in database with message IDs

**Total Estimated:** 22-30 hours (rest of Week 2)

---

## COMMITMENT TO QUALITY

### Same Standards as Week 1

**1. Zero Code Reuse**
- Learning patterns from v6.2 (exponential backoff, error handling)
- Writing 100% fresh code for message-based architecture

**2. Message Chain Audit Trail**
- Every database record links to message
- Complete traceability: analysis → request → briefing → event

**3. Machine-Readable Data**
- All scores stored as numeric (1-10)
- All status fields use CHECK constraints (valid values only)
- JSON payloads for structured data

**4. Error Handling**
- API failures degrade gracefully (use cached data)
- Rate limits handled proactively (check before calling)
- All errors logged to database

---

## LESSONS FROM WEEK 1 APPLIED

### What Worked Well in Trading Department

**1. Message-First Design**
- Designed database schema WITH message_id fields from Day 1
- Result: Clean audit trail, no retrofitting

**2. Test Scenarios Early**
- Week 1 had 5 test scenarios that validated all code paths
- Plan for Week 2: Create 3 test scenarios (bullish market, bearish market, API failure)

**3. Incremental Commits**
- Week 1 had multiple commits showing progress
- Plan for Week 2: Commit after each class implementation

### What to Improve

**1. API Cost Management**
- Week 1 didn't consider Alpaca API rate limits
- Week 2: Proactive rate limit tracking, sentiment caching

**2. Data Validation**
- Week 1 assumed market data always available
- Week 2: Explicit handling of missing data (P/E unavailable, stale prices, etc.)

**3. Documentation as You Build**
- Week 1 wrote comprehensive docs at end
- Week 2: Docstrings for every function as written

---

## WEEK 2 TIMELINE

**Day 1 (Today):** ✅ Database schema complete
**Day 2 (Tomorrow):** MessageHandler + MarketDataCollector + SentimentAnalyzer (12-14 hours)
**Day 3:** TechnicalAnalyzer + FundamentalAnalyzer (6-8 hours)
**Day 4:** DailyBriefing generation + Testing (6-8 hours)
**Day 5:** Documentation + Final testing (3-4 hours)

**Total:** 32-40 hours (within C(P)'s 32-48 hour estimate)

---

## MESSAGE PROTOCOL DESIGN

### Message Types Research Will Generate

**1. DailyBriefing (to Risk + Portfolio)**
```yaml
---
message_id: MSG_RESEARCH_20251101_100000_abc123
from: RESEARCH
to: RISK,PORTFOLIO
timestamp: 2025-11-01T10:00:00Z
message_type: DailyBriefing
priority: routine
---

# Market Briefing - 2025-11-01

## Market Conditions

**Indices:**
- SPY: $450.25 (+0.45%)
- QQQ: $385.50 (+0.72%)
- DIA: $350.75 (+0.28%)

**Volatility:**
- VIX: 15.2 (NORMAL)

**Sector Performance:**
- Top: Technology (+1.2%), Healthcare (+0.8%), Financials (+0.6%)
- Bottom: Energy (-0.5%), Utilities (-0.3%), Materials (-0.2%)

```json
{
  "briefing_date": "2025-11-01",
  "market_sentiment": "BULLISH",
  "vix_level": 15.2,
  "vix_status": "NORMAL",
  "indices": {
    "SPY": {"price": 450.25, "change_pct": 0.45},
    "QQQ": {"price": 385.50, "change_pct": 0.72},
    "DIA": {"price": 350.75, "change_pct": 0.28}
  }
}
```
```

**2. CandidateList (to Portfolio)**
```yaml
---
message_id: MSG_RESEARCH_20251101_101500_def456
from: RESEARCH
to: PORTFOLIO
timestamp: 2025-11-01T10:15:00Z
message_type: CandidateList
priority: routine
---

# Daily Candidate Tickers - 2025-11-01

## Top 10 Candidates

| Rank | Ticker | Catalyst | Sentiment | Technical | Overall |
|------|--------|----------|-----------|-----------|---------|
| 1    | AAPL   | Earnings beat | 8.5 | 7.2 | 8.0 |
| 2    | GOOGL  | Momentum | 7.8 | 8.0 | 7.9 |
| ...  | ...    | ...      | ... | ... | ... |

```json
{
  "screening_date": "2025-11-01",
  "candidates": [
    {
      "rank": 1,
      "ticker": "AAPL",
      "catalyst": "Earnings beat expectations",
      "catalyst_type": "FUNDAMENTAL",
      "sentiment_score": 8.5,
      "technical_score": 7.2,
      "overall_score": 8.0
    }
  ]
}
```
```

**3. TickerAnalysis (on request)**
```yaml
---
message_id: MSG_RESEARCH_20251101_143000_ghi789
from: RESEARCH
to: PORTFOLIO
timestamp: 2025-11-01T14:30:00Z
message_type: TickerAnalysis
priority: routine
in_reply_to: MSG_PORTFOLIO_20251101_140000_xyz123
---

# Deep Analysis: AAPL

## Fundamental Analysis
- P/E: 28.5 (vs sector avg 25.0)
- Revenue Growth YoY: +12.5%
- Profit Margin: 23.2%
- Fundamental Score: 8.0/10

## Technical Analysis
- RSI(14): 62.5 (neutral)
- MACD: Bullish crossover
- Bollinger Position: 0.65 (upper half)
- Technical Score: 7.5/10

## Sentiment Analysis
- News Count: 15 articles (24h)
- Sentiment: Bullish (8.5/10)
- Summary: "Strong earnings, positive analyst upgrades, product launch momentum"

## Overall Assessment
- Overall Score: 8.0/10
- Recommendation: STRONG BUY candidate
```

---

## TECHNICAL INSIGHTS

### API Integration Strategy

**Perplexity API:**
- Rate Limit: 50 requests/minute (check documentation)
- Cost: ~$0.10 per request (estimate)
- Strategy: Cache aggressively (24-hour window), batch queries when possible

**yfinance Library:**
- No rate limits (free)
- Reliability: 95%+ uptime
- Strategy: Primary data source for price/volume/fundamentals

**Alpaca Market Data API:**
- Rate Limit: 200 requests/minute (paper account)
- Cost: Free (paper account)
- Strategy: Use for real-time bars during market hours only

### Scoring Methodology

**Technical Score (1-10):**
```python
# RSI: 30-70 = neutral (5), <30 = oversold (bullish = 7+), >70 = overbought (bearish = 3-)
# MACD: Crossover = +2, Divergence = -2
# Bollinger: Position 0.0-0.3 = oversold, 0.7-1.0 = overbought
technical_score = (rsi_score + macd_score + bollinger_score) / 3
```

**Fundamental Score (1-10):**
```python
# P/E vs sector avg: <avg = +points, >avg = -points
# Revenue growth: >10% = +points, <5% = -points
# Profit margin: >15% = +points, <5% = -points
fundamental_score = (pe_score + growth_score + margin_score) / 3
```

**Sentiment Score (1-10):**
```python
# Keyword analysis: bullish keywords = +1, bearish keywords = -1
# Net score: Very Bearish (1-3), Bearish (3-5), Neutral (5), Bullish (5-7), Very Bullish (7-10)
sentiment_score = 5 + (bullish_count - bearish_count) * weight
```

**Overall Score (1-10):**
```python
# Weighted composite
overall_score = (technical * 0.30) + (fundamental * 0.40) + (sentiment * 0.30)
```

---

## STATUS SUMMARY

**Database Schema:** ✅ COMPLETE (239 lines SQL)
**Message Protocol:** ✅ DESIGNED (message formats defined)
**Python Implementation:** ⏳ NEXT (starting Day 2)
**Testing:** ⏳ PENDING (Day 4)
**Documentation:** ⏳ PENDING (Day 5)

**Overall Week 2 Progress:** ~10% complete (2-3 hours / 32-48 hours)

---

**Ready to continue building Python implementation when you return, WJC!**

**— CC**

**Status:** 🟢 IN PROGRESS - Foundation Complete
**Next Milestone:** MarketDataCollector + SentimentAnalyzer classes
**Estimated Time to Week 2 Complete:** 30-35 hours remaining
