# Sentinel Trading Bot - Changelog

All notable changes to the Sentinel trading system will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) principles.

---

## [Week 3 - Session 2] - 2025-10-27

### Critical Bug Fixes 🐛

#### Conviction Scoring System (CRITICAL)
Two related bugs completely broke the conviction-weighted allocation system:

1. **Conviction Clamping Bug** - `sentinel/tier3_conviction_analysis.py:444`
   - **Problem**: Tier 3 scores were being clamped to max of 10 instead of 100
   - **Impact**: Lost 90% of scoring granularity needed for position sizing
   - **Fix**: Changed `max(1, min(10, conviction))` → `max(1, min(100, conviction))`
   - **Result**: Full 1-100 conviction range now preserved

2. **Conviction Weighting Formula Bug** - `sentinel/order_generator.py:295`
   - **Problem**: Formula divided by 10.0 instead of 100.0 when normalizing scores
   - **Impact**: All scores ≥10 were normalized to 1.0, getting identical position sizes
   - **Fix**: Changed `conviction / 10.0` → `conviction / 100.0`
   - **Result**: High-conviction trades (95) now get significantly more capital than medium (75) or low (50)

**Combined Impact**: These bugs meant position sizing was essentially random. A 95 conviction score got the same allocation as a 50 conviction score. This completely defeated the purpose of the conviction-weighted system.

---

### New Features ✨

#### 1. Perplexity AI Real-Time News Integration
**New File**: `sentinel/perplexity_news.py`

Fills a critical gap - GPT-4-Turbo alone cannot access current news and events. Perplexity specializes in real-time web search with citations.

**Key Methods**:
- `gather_ticker_news()`: Fetch recent news for specific stocks
  - Earnings reports, analyst upgrades/downgrades
  - Partnerships, acquisitions, product launches
  - Regulatory issues, lawsuits, leadership changes
  - Returns sentiment analysis and key events

- `gather_market_overview()`: Overall market conditions
  - Bull/bear sentiment, economic data releases
  - Sector rotation, Fed commentary
  - Volatility trends (VIX), major index performance

- `gather_batch_news()`: Efficiently gather news for multiple tickers

**Cost**: ~$0.005 per query (or $20/month unlimited)
**Model**: "sonar" (Perplexity's online search model)
**Testing**: ✅ Successfully validated with NVDA ticker and market overview

---

#### 2. Conviction-Based SELL Execution
**Files Modified**:
- `sentinel/execution_engine.py`: New `submit_conviction_sell()` method
- `database_migrations/004_add_conviction_sells.sql`: New database table

**Critical Gap Filled**: System could only generate BUY signals. Positions could only exit via stop-loss or manual intervention. Now Tier 3 can recommend SELL decisions based on deteriorating fundamentals.

**New Database Table**: `conviction_sells`
- Tracks all conviction-based SELL orders (separate from stop-loss exits)
- Records conviction score (1-100), reasoning, P&L, fill status
- Enables performance analysis: "Do conviction-based exits outperform stops?"

**New Method**: `ExecutionEngine.submit_conviction_sell()`
- Submits market sell order based on Tier 3 recommendation
- Automatically cancels associated stop-loss order (prevents double-exit)
- Records full details in `conviction_sells` table
- Returns order ID and success status

**Integration**: Used in workflow Step 6A (SELL signals execute BEFORE BUY signals)

---

#### 3. BUY Conviction Filtering Threshold
**Files Modified**:
- `sentinel_morning_workflow.py:589-618`
- `sentinel_evening_workflow.py:586-615`

**Feature**: Added `BUY_CONVICTION_THRESHOLD = 70` (out of 100)

**Rationale**:
- Only execute BUY signals with conviction ≥70
- Avoids marginal trades that consume capital without strong edge
- Low-conviction signals are logged but not executed
- With 70+ threshold, system only commits capital to high-conviction opportunities

**Important**: SELL signals still execute regardless of conviction (safety first - exit deteriorating positions immediately)

**Logging**: Detailed logs show which signals were filtered:
```
BUY signal filtering: 12/18 above 70 threshold
  Filtered out: XYZ (conviction: 65)
  Filtered out: ABC (conviction: 58)
```

---

#### 4. Real-Time Market Context Integration
**Files Modified**:
- `sentinel_morning_workflow.py:183-192, 225, 239`
- `sentinel_evening_workflow.py:180-189, 225, 239`

**Feature**: Integrated Perplexity market overview at start of Step 5 (before Tier 2/3 analysis)

**Replaces**: Hardcoded placeholder "Market conditions vary - see detailed analysis"

**Provides to Tier 2 & Tier 3**:
- Real-time market sentiment (bullish/bearish/mixed)
- Economic data releases and Fed commentary
- Sector rotation and leadership
- Geopolitical events affecting markets
- VIX and volatility trends

**Graceful Degradation**: Falls back to generic context if Perplexity API fails

**Impact**: AI analysis now has current market context instead of analyzing "blind"

---

#### 5. Morning Workflow Implementation
**New File**: `sentinel_morning_workflow.py`

Complete morning execution workflow (9 AM PT / Noon ET) with all Week 3 features integrated:
- ✅ BUY conviction filtering (70/100 threshold)
- ✅ Real-time Perplexity market overview
- ✅ SELL-then-BUY sequencing for cash management
- ✅ Conviction-based position sizing (1-100 scale)
- ✅ Graceful error handling and fallbacks

**Workflow Steps**:
1. Initialize logging and connections
2. Check market hours (abort if market closed)
3. Fetch current positions and calculate available cash
4. Tier 1: Technical filtering (~3000 stocks → ~300 candidates)
5. Tier 2: AI screening with market context (~300 → ~70 finalists)
6. Tier 3: Deep conviction analysis with news (~70 → BUY/SELL/HOLD)
7. Step 6A: Execute SELL signals (free cash first)
8. Step 6B: Execute BUY signals (filtered by conviction ≥70)

---

### Known Issues & Limitations ⚠️

1. **Stock Universe Hardcoded**
   - Currently limited to 40 handpicked tickers
   - Need configuration system to choose: 40 / SP500 / Russell 3000
   - Priority: MEDIUM (testing convenience vs scalability)

2. **Zero Testing Performed**
   - All Week 3 features are untested
   - Need comprehensive dry-run before live trading
   - Priority: CRITICAL (testing required before going live)

3. **PDT Compliance Validation Pending**
   - No explicit day trade counting logic visible
   - Need to verify system prevents 4th day trade in 5-day window
   - Priority: HIGH (paper trading account can still be suspended for 90 days)

4. **Analytics Placeholders**
   - Win rate, avg win/loss, profit factor still using placeholder values
   - Can be calculated from `conviction_sells` and filled orders
   - Priority: LOW (cosmetic, doesn't affect trading logic)

---

### Technical Debt 📝

- [ ] Make stock universe configurable (via config or CLI argument)
- [ ] Create comprehensive dry-run test plan
- [ ] Validate PDT day trade counting logic
- [ ] Test conviction weighting with real scores (95 vs 75 vs 50)
- [ ] Test SELL-then-BUY cash sequencing
- [ ] Test Perplexity error handling and rate limits
- [ ] Replace analytics placeholders with real calculations

---

### Testing Status 🧪

| Component | Status | Notes |
|-----------|--------|-------|
| Conviction clamping fix | ⚠️ Untested | Bug fix needs validation |
| Conviction weighting fix | ⚠️ Untested | Need to test with various scores |
| BUY filtering threshold | ⚠️ Untested | Need to verify filtering logic |
| SELL execution | ⚠️ Untested | Need to test cash sequencing |
| Perplexity integration | ✅ Tested | Manual test with NVDA successful |
| Market context integration | ⚠️ Untested | Need workflow-level test |
| Morning workflow | ⚠️ Untested | Complete dry-run required |

**Recommendation**: DO NOT go live tomorrow. Run comprehensive dry-run tests first.

---

## [Week 2 - Complete] - 2025-10-21

### Summary
Full conviction system integrated with three-tier analysis, stop-loss only architecture, and database infrastructure.

**Key Achievements**:
- ✅ Three-tier conviction analysis pipeline (Tier 1 → Tier 2 → Tier 3)
- ✅ GPT-4-Turbo integration for deep analysis
- ✅ Stop-loss only architecture (every entry has protective stop)
- ✅ Database schema for orders, positions, stops, fills
- ✅ Execution engine with order lifecycle management
- ✅ Position sizing based on conviction scores
- ✅ Evening workflow implementation (6 PM PT execution)

**Key Commits**:
- `3c53f96` - Week 2 Complete: Full Conviction System Integrated
- `58a10bb` - Week 2 Session 4: Order Generator Complete
- `48f6ac3` - Week 2 Session 3: Context Builder + Tier 3 Analysis Complete
- `ee8cdcd` - Week 2 Session 2: Tier 2 AI Screening Complete
- `3ae56a2` - Week 2 Session 1: Tier 1 Technical Filter Complete

---

## Project Context

**What is Sentinel?**
An AI-powered equity trading bot that combines technical analysis with GPT-4-Turbo conviction scoring to identify high-probability trades.

**Architecture Philosophy**:
- Stop-loss only (no profit targets) - let winners run
- Conviction-weighted allocation - more capital to higher-conviction ideas
- Three-tier funnel - aggressive filtering before expensive AI analysis
- Safety first - all SELL signals execute, BUYs are filtered by conviction

**AI Stack**:
- Perplexity AI: Real-time news and market context ($0.005/query)
- GPT-4-Turbo: Deep conviction analysis ($0.02/query)
- Total cost: ~$1.75/day for 70 stocks analyzed

**Development Timeline**:
- Week 1: Project setup, database design, core infrastructure
- Week 2: Three-tier conviction analysis pipeline
- Week 3: SELL execution, Perplexity integration, conviction fixes
- Week 4 (upcoming): Testing, debugging, initial live deployment

---

## Glossary

**Conviction Score**: 1-100 rating of trade quality. Higher scores get more capital allocation.

**Tier 1**: Technical filtering using pandas_ta indicators. Fast, cheap, filters 3000 → 300.

**Tier 2**: AI-powered screening using GPT-3.5-Turbo. Moderate cost, filters 300 → 70.

**Tier 3**: Deep conviction analysis using Perplexity (news) + GPT-4-Turbo (analysis). Expensive, filters 70 → final BUY/SELL/HOLD decisions.

**Stop-Loss Only Architecture**: Every entry has protective stop, no profit targets. Lets winners run, cuts losers quickly.

**PDT (Pattern Day Trader)**: SEC rule limiting accounts <$25K to 3 day trades per 5 business days. Paper trading accounts still subject to 90-day suspension for violations.

**Conviction Sells**: Exits triggered by Tier 3 analysis (deteriorating fundamentals) vs stop-loss exits (price-based).

---

*This CHANGELOG is maintained to provide a human-readable summary of project evolution. For detailed commit history, see `git log`.*
