# Sentinel Trading Bot - Changelog

All notable changes to the Sentinel trading system will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) principles.

---

## [Week 7 - Complete] - 2025-10-31

### 🎉 WEEK 7 COMPLETE: System Integration & Live Trading Preparation

**Status**: 100% TEST PASS RATE ACHIEVED (35/35 tests passing)

#### Added

**Day 1: Market Data Integration**
- `Utils/market_data_provider.py` (456 lines) - Real-time market data via yfinance
- Retry logic with exponential backoff (3 attempts)
- Circuit breaker pattern (5-failure threshold, 60-second timeout)
- File-based caching with TTL (5-min for prices, 60-min for history)
- Graceful degradation to placeholders on API failure

**Day 2: Terminal Dashboard**
- `Utils/terminal_dashboard.py` (447 lines) - Real-time terminal UI
- Rich library integration (14.2.0) for terminal rendering
- Auto-refresh every 5 seconds (configurable)
- Color-coded metrics (green for gains, red for losses)
- 60" TV compatible (no scrolling required)
- `Launch_Dashboard.bat` - Desktop launcher

**Day 3: Email Reporting**
- `Utils/email_reporter.py` (550 lines) - HTML email reports via Gmail SMTP
- Beautiful HTML templates with inline CSS
- Performance metrics, positions table, system health
- Successfully sent 10,357-byte reports to user
- `Send_Email_Report.bat` - Desktop launcher
- `Preview_Email_Report.bat` - Browser preview launcher

**Day 4: SMS Alerts**
- `Utils/sms_alerter.py` (427 lines) - Twilio SMS integration
- 5 alert types (P&L moves, milestones, health, win rate, Sharpe)
- Quiet hours (10 PM - 8 AM, no alerts during sleep)
- Cooldown logic (60-minute minimum between same alert type)
- Twilio confirmed working (carrier blocking due to no A2P approval)
- `Test_SMS_Alert.bat` - Desktop launcher
- `Check_Portfolio_Alerts.bat` - Desktop launcher
- `Send_Daily_SMS_Summary.bat` - Desktop launcher

**Day 5: End-to-End Testing**
- `test_end_to_end.py` (352 lines) - Comprehensive integration test
- 7 test suites covering all components
- Database verification (17 tables)
- File structure validation
- API integration testing
- `Run_System_Test.bat` - Desktop launcher
- `Sentinel_Control_Panel.bat` - Master control panel

**Database Tables Created:**
- `research_market_briefings` - Research Department daily analysis
- `trading_orders` - Order tracking
- `trading_fills` - Execution details
- `trading_rejections` - Failed orders
- `trading_daily_logs` - Daily execution summaries
- `trading_duplicate_cache` - Prevent duplicate submissions

**Documentation:**
- `WEEK7_DAY5_COMPLETE.md` - Day 5 completion summary
- `WEEK7_COMPLETION_FOR_CP_REVIEW.md` - Comprehensive review for C(P)
- `URGENT_FINDINGS.md` - Alpaca disconnect discovery
- `TESTING_GUIDE.md` - Full testing documentation
- `QUICK_START.txt` - Quick reference card
- `DAILY_CHECKLIST.txt` - Daily operation guide

**Utility Scripts:**
- `check_alpaca.py` - Check real Alpaca account status
- `init_missing_departments.py` - Initialize departments
- `create_missing_tables.py` - Create database tables

#### Changed

**Executive Department:**
- Updated `executive_department.py` (lines 89-118) - Real unrealized P&L calculation
- Updated `executive_department.py` (lines 499-588) - Real SPY benchmark data
- Unrealized P&L: $0 → $60,426.62 (real current prices)
- SPY 30-day return: 0.83% (placeholder) → 1.70% (real data)

**Configuration:**
- Fixed `config.py` line 32 syntax error (invalid Python → valid variable)

#### Test Results

**Before Week 7 Day 5:**
- Tests Passed: 30/33 (90.9%)
- Tests Failed: 3/33 (9.1%)

**After Week 7 Day 5:**
- Tests Passed: 35/35 (100.0%)
- Tests Failed: 0
- Warnings: 0

#### Known Issues

**Minor (Non-Critical):**
1. Email metrics display quirks (data structure mismatch) - Deferred
2. SMS carrier blocking (no A2P approval) - External issue
3. pandas-ta incompatible with Python 3.14 - Waiting for library update

**Major (Awaiting Decision):**
1. Alpaca Integration Strategy - Simulation mode vs live trading
2. Real portfolio disconnect - Dashboard shows test data ($65K), Alpaca has $102K with 92 positions

#### Security

**API Keys:**
- Sanitized all documentation (phone numbers, Twilio SID, other secrets)
- `.gitignore` protects `config.py` and `sentinel.db`
- Keys remain in local `config.py` only (not committed)

#### Manual Operation Mode

**Rationale:** User constraints (computer crashes, sleep mode required, probation monitoring)

**Solution:** 9 desktop launchers for double-click execution:
1. `Sentinel_Control_Panel.bat` - Master menu
2. `Run_System_Test.bat` - Test runner
3. `Launch_Dashboard.bat` - Real-time dashboard
4. `Launch_Sentinel.bat` - Full launcher with checks
5. `Preview_Email_Report.bat` - HTML preview
6. `Send_Email_Report.bat` - Send email
7. `Test_SMS_Alert.bat` - Test SMS
8. `Check_Portfolio_Alerts.bat` - Check alerts
9. `Send_Daily_SMS_Summary.bat` - Daily summary

**Automation Deferred:** Will revisit when user has stable infrastructure or dedicated server

#### Next Steps

**Awaiting C(P) Review:**
- Architecture assessment
- Alpaca integration strategy recommendation
- Testing sufficiency validation
- Security review
- Week 8 planning approval

**Documentation References:**
- See `WEEK7_COMPLETION_FOR_CP_REVIEW.md` for comprehensive review
- See `URGENT_FINDINGS.md` for Alpaca disconnect details
- See `WEEK7_DAY5_COMPLETE.md` for Day 5 summary

---

## [Week 3 - Session 3] - 2025-10-28

### 🏆 MAJOR ARCHITECTURAL UPGRADE: Production-Ready Racehorse

**Revolutionary Change**: Complete system redesign to solve fundamental "Chinese Room" problem identified by user.

#### Problem Identified
The system was making sequential, myopic decisions - analyzing each stock individually without knowledge of the full opportunity set. This led to:
- Suboptimal capital allocation (locally optimal, globally suboptimal)
- Forced margin usage ($78k shortfall when 8 BUY signals wanted capital but only 4 SELL signals freed cash)
- Too conservative SELL discipline (48 HOLD, 4 SELL, 8 BUY observed in first live run)

#### Solution Implemented: Two-Stage Architecture
1. **Stage 1 (Analysis)**: Tier 3 generates conviction scores for ALL stocks
2. **Stage 2 (Optimization)**: GPT-5 sees ALL scores + portfolio state + cash constraint → makes ONE globally optimal decision

**Analogy**: Previously like a blindfolded hedge fund manager evaluating stocks one-at-a-time. Now the manager sees the full portfolio and all opportunities before making any decisions.

---

### Added

#### 1. Portfolio Optimizer Module (GPT-5)
**New File**: `sentinel/portfolio_optimizer.py` (368 lines)

**Revolutionary Feature**: Holistic portfolio optimization with full information

**How It Works**:
- Input: ALL ~100 conviction scores + current portfolio (53 positions) + cash available
- Processing: Single GPT-5 API call with complete context
- Output: Complete rebalancing plan {sells: [...], holds: [...], buys: [{symbol, allocation}]}

**Constraints Enforced**:
- NO MARGIN (hard constraint - optimizer sees cash limit)
- Max 15% position size
- Max 40% sector concentration
- Target 15-25 total positions

**Conviction-Weighted Allocation Formula**:
```python
# For BUY decisions:
total_conviction_points = sum(conviction_score for all buys)
allocation = (stock_conviction / total_conviction_points) × available_capital

# Example with $80k available:
# AMD (87): (87/413) × $80k = $16,850
# DHR (83): (83/413) × $80k = $16,077
```

**Cost**: ~$0.30 per run (ONE critical decision vs 60 sequential calls)
**Model**: GPT-5 (upgraded from GPT-4-Turbo)

---

#### 2. Production Trading Universe
**New File**: `sentinel/universe.py`

**Universe**: S&P 500 + Nasdaq 100 = ~600 stocks
- S&P 500: 500 stocks
- Nasdaq 100: 100 stocks
- Overlap: ~15 stocks
- **Total unique**: ~585 stocks

**Benefits**:
- Consistent, high-quality universe (no daily changes)
- Slight tech tilt (aligns with user expertise)
- Covers 99% of meaningful market opportunities
- No penny stocks or illiquid names

**Exports**:
- `SP500_NASDAQ100_UNIVERSE`: Full list of symbols
- `UNIVERSE_SIZE`: Count of unique stocks

---

#### 3. Zero-Quantity Position Cleanup
**File Modified**: `sentinel_morning_workflow.py` (lines 282-344)

**New Function**: `cleanup_zero_quantity_positions()`

**Purpose**: Automatically liquidate positions < 0.001 shares (artifacts from previous system versions)

**Execution**: Runs BEFORE Step 6A (SELL signals) in main workflow

**Logic**:
```python
for pos in positions:
    qty = abs(float(pos.qty))
    if qty < 0.001:  # Essentially zero
        submit_conviction_sell(symbol, qty, "Cleanup: Zero-quantity position")
```

**Impact**: Observed 5 zero-quantity positions in first live run → will be auto-cleaned on next run

---

#### 4. Fractional Share Trading Support
**Files Modified**:
- `sentinel/order_generator.py:142` - Changed `int(allocation / price)` → `round(allocation / price, 9)`
- `sentinel/execution_engine.py:593` - Changed `abs(int(float(qty)))` → `abs(float(qty))`
- `sentinel/execution_engine.py:829` - Same change for profit-taking logic
- `sentinel_morning_workflow.py:336` - Keep fractional shares in SELL quantity calculation

**Benefit**: Maximize capital efficiency
- Before: 2 shares of AVGO @ $618 = $1,236 (wasted $364 of $1,600 allocation)
- After: 2.589 shares @ $618 = $1,600 (perfect allocation)

**Precision**: Up to 9 decimal places (Alpaca's limit)

---

### Changed

#### 1. Portfolio Optimizer: GPT-4-Turbo → GPT-5
**File**: `sentinel/portfolio_optimizer.py:221`

**Change**: `model="gpt-4-turbo"` → `model="gpt-5"`
**Timeout**: 60s → 120s (allow deeper reasoning)

**Rationale**: Portfolio optimization is the MOST CRITICAL decision
- GPT-5 has superior reasoning for complex constraint optimization
- Shows chain-of-thought (can see its reasoning process)
- Worth $0.20-0.40 extra cost for quality improvement on $100k portfolio

**Cost Impact**: +$0.20-0.40 per run

---

#### 2. Aggressive Tier 1 Filtering (Racehorse Quality)
**File**: `sentinel/tier1_technical_filter.py:52-57`

**Philosophy**: "Breeding a racehorse, not a pony for a little kid" (user quote)

**Previous**: 75 → 60 stocks (20% rejection, very lenient)
**New**: 600 → ~100 stocks (83% rejection, aggressive)

**Parameter Changes**:
| Parameter | Before | After | Impact |
|-----------|--------|-------|--------|
| `min_dollar_volume` | $1M | $10M | Only highly liquid stocks |
| `min_price` | $5 | $10 | No penny stocks |
| `max_price` | $500 | $1000 | Allow TSLA, GOOG, etc. |
| `min_rsi` | 20 | 30 | Avoid oversold disasters |
| `max_rsi` | 80 | 75 | Avoid overbought bubbles |
| `target_count` | 250 | 100 | Soft target (adaptive 80-120) |

**Adaptive Behavior**:
- Bullish markets: More stocks pass momentum filters → ~120 output
- Bearish markets: Fewer stocks pass momentum filters → ~80 output
- **Target**: ~100 stocks for manageable Tier 3 cost

---

#### 3. Tier 2 Role: Filtering → Enrichment Only
**File**: `sentinel_morning_workflow.py:221-229`

**Previous**: Light filtering (reduce count somewhat)
**New**: Pure enrichment (pass ALL ~100 candidates through)

**Functionality**: Adds sector classification + recent news headlines
**Rationale**: Tier 1 already aggressive enough; Tier 2 adds context, not filtering

**Implementation**: `target_count=len(tier1_candidates)` (pass all through)

---

#### 4. Workflow Universe Integration
**File**: `sentinel_morning_workflow.py:195-214`

**Previous**: Hardcoded 40-stock test list
**New**: S&P 500 + Nasdaq 100 (600 stocks) + currently held positions

**Import**: `from sentinel.universe import SP500_NASDAQ100_UNIVERSE, UNIVERSE_SIZE`

**Logic**:
```python
universe = list(set(SP500_NASDAQ100_UNIVERSE + portfolio_symbols))
# Base 585 stocks + currently held (for SELL analysis) = ~600 total
```

**Logging**: `Universe: 585 base stocks + 53 held = 638 total`

---

#### 5. AI Conviction Prompt (More Aggressive Selling)
**File**: `sentinel/tier3_conviction_analysis.py:37-96`

**Major Prompt Rewrite**: ANALYSIS_PROMPT_TEMPLATE

**New Sections Added**:

1. **"Capital efficiency principle"**:
   ```
   This portfolio operates with LIMITED CAPITAL. Every dollar held in a
   mediocre position is a dollar NOT allocated to high-conviction opportunities.
   ```

2. **Conviction scale changes**:
   - **50-59**: "Prefer HOLD" → "If currently held, consider SELL to reallocate capital"
   - **40-49**: "Notable caution" → "SELL if held"

3. **Position-specific guidance**:
   - Held positions with conviction <60 → "Strong bias toward SELL"
   - Held positions 60-69 → "HOLD acceptable if no major deterioration"
   - New positions → "Only BUY if conviction 70+"

4. **Explicit reasoning requirement**:
   - SELL rationales must state "freeing capital for higher-conviction opportunities"

**Impact**: Should generate 15-25 SELL signals instead of just 4

---

#### 6. Order Generator: Support Pre-Set Allocations
**File**: `sentinel/order_generator.py:120-134`

**Problem**: Portfolio optimizer sets specific $ allocations, but order generator recalculated them

**Fix**: Check if signals have 'allocation' field:
```python
has_preset_allocations = any('allocation' in sig for sig in buy_signals)

if has_preset_allocations:
    allocations = {sig['symbol']: sig['allocation'] for sig in buy_signals}
else:
    # Calculate using conviction-weighted formula
    allocations, notes = self._calculate_allocations(...)
```

**Impact**: Portfolio optimizer's exact allocations are now respected

---

### Fixed

#### 1. Cosmetic Issues (Professional Output)
**Files Modified**:
- `sentinel_morning_workflow.py:621` - "SENTINEL EVENING WORKFLOW" → "SENTINEL MORNING WORKFLOW"
- `sentinel_morning_workflow.py:63` - Log filename `evening_workflow_*.log` → `morning_workflow_*.log`

**Rationale**: User feedback - "Cosmetic things matter. They are confusing and unprofessional."

---

### Known Issues

#### 1. Emergency Stop Database Errors (Unchanged from Week 3 Session 2)
- **Symptom**: CRITICAL messages about "FOREIGN KEY constraint failed"
- **Reality**: Emergency stops ARE created successfully in Alpaca
- **Issue**: Database write fails due to schema foreign key misalignment
- **Impact**: Stops protective, but database tracking fails
- **Status**: NOT FIXED (requires database schema investigation)

---

### Performance

#### Cost Per Run Analysis

**Previous** (75-stock test universe):
- Tier 1: $0
- Tier 2: $0.05
- Tier 3: 60 stocks × $0.01 = $0.60
- Optimizer: GPT-4-Turbo $0.03
- **Total**: ~$0.68/run

**Current** (600-stock production universe):
- Tier 1: $0
- Tier 2: $0.10
- Tier 3: ~100 stocks × $0.01 = $1.00
- Optimizer: GPT-5 $0.30
- **Total**: ~$1.40/run

**Monthly Cost** (20 trading days): $28/month

**ROI Calculation**:
If GPT-5 makes 0.3% better allocation decisions per month on $100k portfolio:
- Gain: $100,000 × 0.003 = $300
- Cost: $28
- **ROI**: 10.7x return on investment

---

### Testing Status 🧪

| Component | Status | Notes |
|-----------|--------|-------|
| GPT-5 optimizer | ⚠️ Untested | New model, may have API differences |
| 600-stock universe | ⚠️ Untested | Previous testing was 75 stocks |
| Aggressive Tier 1 | ⚠️ Untested | New parameters, need to verify ~100 output |
| Fractional shares | ⚠️ Untested | Need to verify Alpaca accepts fractional quantities |
| Zero-position cleanup | ⚠️ Untested | Should liquidate 5 known zero positions |
| Portfolio optimizer | ⚠️ Untested | Holistic decision-making untested with real portfolio |

**Recommendation**: Test tomorrow morning (9-11am PT) with real paper trading account. Observe:
1. Tier 1 output count (should be ~100)
2. GPT-5 optimizer decisions (sells, holds, buys)
3. No margin usage (cash should not go negative)
4. Fractional shares in new positions

---

### Migration Notes

**For Users Running Week 3 Session 2**:

1. **No database migration required** - Tables unchanged
2. **New dependency**: Ensure OpenAI API supports GPT-5 (or fallback to GPT-4-Turbo)
3. **Expected behavior changes**:
   - More SELL signals (15-25 instead of 4)
   - Fractional share quantities in positions
   - Zero-quantity positions auto-liquidated
   - No margin usage (optimizer respects constraint)
   - Longer Tier 1 processing (600 stocks vs 75)
4. **Configuration**: No changes to `config.py` or `.env` required

---

### User Feedback Integration

**Key Quote**: "I have questions: 1) Should I be considering using a different, more capable AI model for the all-important optimization step? It seems like a lot of intelligence and updated world knowledge would be real assets here..."

**Response**: ✅ Upgraded to GPT-5 for portfolio optimizer

**Key Quote**: "I am thinking we should simply use the S&P 500 + the Nasdaq 100 as the universe from now on... 600 stock universe... Tier 1 needs to filter down to approx 17% of the universe."

**Response**: ✅ Implemented S&P 500 + Nasdaq 100 universe with 83% rejection rate

**Key Quote**: "We are breeding a racehorse, here, not a pony for a little kid."

**Response**: ✅ Aggressive filtering parameters implemented

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
