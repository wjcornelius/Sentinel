# Sentinel Trading Bot - Dry-Run Test Plan

**Purpose**: Comprehensive testing before live paper trading deployment
**Status**: 🔴 MUST COMPLETE BEFORE GOING LIVE
**Created**: 2025-10-27 (Week 3, Session 2)

---

## ⚠️ CRITICAL: Why We Can't Go Live Tomorrow

You mentioned concern about PDT rules - that's the right instinct. Here's why we need testing first:

1. **Untested Bug Fixes**: We fixed critical bugs today but haven't validated the fixes work correctly
2. **New Features Never Run**: SELL execution, Perplexity integration, BUY filtering - zero test coverage
3. **Cash Management Unknown**: Does SELL-then-BUY sequencing actually work? Will we get cash constraint errors?
4. **PDT Compliance Unclear**: I don't see explicit day trade counting logic - need to verify this exists
5. **Real-World Edge Cases**: What happens if Perplexity is down? What if conviction returns NaN? What if all 70 finalists are SELL signals?

**PDT Risk**: Even paper trading accounts get 90-day suspensions for PDT violations. We must validate the system counts day trades correctly before letting it trade.

---

## Testing Philosophy

### Dry-Run Mode vs Live Mode
**Dry-Run**: Execute entire workflow but SKIP order submission. Log what WOULD have been executed.
- Validates logic flow
- Catches crashes and errors
- Verifies data transformations
- Zero risk of bad orders

**Live Mode**: Submit real orders to Alpaca paper trading API
- Only use after dry-run testing passes
- Start with small position sizes
- Monitor first week closely

### Test Pyramid
```
           Manual Review (You spot-check results)
          ↗
     Integration Tests (Full workflow end-to-end)
    ↗
   Unit Tests (Individual functions)
  ↗
System Tests (Database, API connections)
```

We'll focus on **Integration Tests** (full workflow) and **Manual Review** since unit tests would take days to write.

---

## Pre-Flight Checklist

Before running ANY tests, verify these basics:

### System Health
- [ ] Python environment active (`venv` or system Python)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Database exists and is accessible (`sqlite3 sentinel.db ".tables"`)
- [ ] Config file has all API keys (Alpaca, OpenAI, Perplexity)

### Database Migrations
- [ ] Run migration 004 to create `conviction_sells` table
  ```bash
  sqlite3 sentinel.db < database_migrations/004_add_conviction_sells.sql
  ```
- [ ] Verify table exists:
  ```bash
  sqlite3 sentinel.db ".schema conviction_sells"
  ```

### API Credentials Validation
- [ ] Alpaca paper trading account accessible (check account endpoint)
- [ ] OpenAI API key valid (test with simple completion)
- [ ] Perplexity API key valid (test with `python sentinel/perplexity_news.py`)

### Baseline Checks
- [ ] Can fetch current positions from Alpaca
- [ ] Can fetch account cash balance
- [ ] Can query database without errors
- [ ] Logs directory exists and is writable

---

## Test Suite 1: Component Tests

Test individual components before full workflow.

### Test 1.1: Perplexity Integration
**File**: `sentinel/perplexity_news.py`
**Command**: `python sentinel/perplexity_news.py`

**What to verify**:
- ✅ NVDA news fetched successfully
- ✅ Market overview fetched successfully
- ✅ Sentiment analysis returns valid values (positive/negative/neutral)
- ✅ Citations/sources returned
- ⚠️ **NEW**: Test error handling by temporarily breaking API key

**Expected Output**:
```
Testing Perplexity News Integration...
1. Testing single ticker news (NVDA):
   Symbol: NVDA
   Sentiment: positive
   Summary: [Recent news about Nvidia...]
   Key Events: [List of events]
   Sources: [List of URLs]

2. Testing market overview:
   Market Summary: [Overall market conditions...]
   Sources: 6 citations
```

**Pass Criteria**:
- No exceptions raised
- News summary > 100 characters
- Sentiment is one of: positive/negative/neutral
- At least 1 source citation returned

---

### Test 1.2: Conviction Scoring Fix Validation
**What to test**: Verify bug fixes actually work

**Manual Test** (Python REPL):
```python
import sys
sys.path.insert(0, '.')
from sentinel.order_generator import OrderGenerator

# Create mock generator
gen = OrderGenerator(account_value=100000, logger=None)

# Test conviction weighting with various scores
test_scores = [100, 95, 85, 75, 65, 50, 25, 10, 1]

print("Conviction Score → Normalized Weight → Final Weight")
print("-" * 60)

for score in test_scores:
    weight = gen._conviction_to_weight(score)
    normalized = score / 100.0
    print(f"{score:3d} → {normalized:.2f} → {weight:.4f}")
```

**Expected Output** (approximate, depends on `CONVICTION_WEIGHT_EXP`):
```
Conviction Score → Normalized Weight → Final Weight
------------------------------------------------------------
100 → 1.00 → 1.0000
 95 → 0.95 → 0.9025
 85 → 0.85 → 0.7225
 75 → 0.75 → 0.5625
 65 → 0.65 → 0.4225
 50 → 0.50 → 0.2500
 25 → 0.25 → 0.0625
 10 → 0.10 → 0.0500 (or MIN_WEIGHT_FLOOR)
  1 → 0.01 → 0.0500 (MIN_WEIGHT_FLOOR)
```

**Pass Criteria**:
- Higher scores get HIGHER weights (monotonic increase)
- Score 100 gets weight close to 1.0
- Score 50 gets weight around 0.25 (exponential weighting)
- Low scores hit `MIN_WEIGHT_FLOOR` (prevent zero allocation)

**CRITICAL**: If scores 95, 75, 50 all get SAME weight → BUG STILL EXISTS

---

### Test 1.3: Database Operations
**What to test**: Verify `conviction_sells` table works

**Manual Test** (bash):
```bash
sqlite3 sentinel.db <<EOF
-- Test insert
INSERT INTO conviction_sells (symbol, order_id, client_order_id, qty, conviction_score, reasoning, tier3_decision)
VALUES ('TEST', 'test_order_123', 'test_client_123', 100, 85, 'Test reasoning', 'SELL');

-- Verify insert
SELECT * FROM conviction_sells WHERE symbol = 'TEST';

-- Clean up
DELETE FROM conviction_sells WHERE symbol = 'TEST';
EOF
```

**Pass Criteria**:
- Insert succeeds without errors
- SELECT returns the inserted row
- All columns populated correctly
- DELETE cleans up test data

---

## Test Suite 2: Integration Tests (Dry-Run)

Test full workflow end-to-end WITHOUT submitting orders.

### Test 2.1: Morning Workflow Dry-Run (Basic)
**File**: `sentinel_morning_workflow.py`
**Goal**: Verify workflow executes without crashing

**Preparation**:
1. Temporarily modify workflow to skip order submission:
   ```python
   # Around line 608-618, comment out actual order submission
   if len(sell_results) > 0:
       logger.info(f"[DRY-RUN] Would execute {len(sell_results)} SELL orders")
       # sell_results = engine.submit_conviction_sells(...)  # COMMENTED FOR DRY-RUN

   if len(filtered_buy_signals) > 0:
       logger.info(f"[DRY-RUN] Would execute {len(filtered_buy_signals)} BUY orders")
       # buy_results = engine.generate_and_submit_orders(...)  # COMMENTED FOR DRY-RUN
   ```

2. Run workflow:
   ```bash
   python sentinel_morning_workflow.py
   ```

**What to verify**:
- ✅ Workflow starts and initializes
- ✅ Alpaca connection successful
- ✅ Account balance fetched
- ✅ Tier 1 runs without errors (produces candidate list)
- ✅ Perplexity market overview fetched
- ✅ Tier 2 runs without errors (produces finalist list)
- ✅ Tier 3 runs without errors (produces BUY/SELL/HOLD decisions)
- ✅ BUY filtering logic executes (logs filtered signals)
- ✅ Would-execute logs show reasonable order counts
- ✅ No Python exceptions or crashes

**Expected Log Output** (approximate):
```
[INFO] Sentinel Morning Workflow Starting (9 AM PT / Noon ET)
[INFO] Connected to Alpaca API successfully
[INFO] Account balance: $100,000.00
[INFO] Step 4: Tier 1 Technical Filtering
[INFO]   Processed 40 candidates → 15 passed filters
[INFO] Step 5: Tier 2 AI Screening
[INFO]   Gathering real-time market overview...
[INFO]   Market overview gathered: 1513 chars
[INFO]   Tier 2 complete: 15 candidates → 8 finalists
[INFO] Step 6: Tier 3 Deep Conviction Analysis
[INFO]   Gathering batch news for 8 tickers...
[INFO]   Tier 3 complete: 3 BUY, 2 SELL, 3 HOLD
[INFO] BUY signal filtering: 2/3 above 70 threshold
[INFO]   Filtered out: XYZ (conviction: 65)
[INFO] [DRY-RUN] Would execute 2 SELL orders
[INFO] [DRY-RUN] Would execute 2 BUY orders
```

**Pass Criteria**:
- No exceptions/crashes
- Tier 1 produces candidates (>0 results)
- Tier 2 produces finalists (>0 results)
- Tier 3 produces mix of BUY/SELL/HOLD
- BUY filtering logs make sense
- Dry-run logs show would-execute counts

**FAIL Criteria** (require investigation):
- Python exception/crash
- Zero candidates from Tier 1 (too aggressive filtering?)
- Zero finalists from Tier 2 (AI rejecting everything?)
- All Tier 3 decisions are HOLD (no actionable signals?)
- BUY filtering removes ALL signals (threshold too high?)

---

### Test 2.2: Conviction Weighting in Practice
**Goal**: Verify high-conviction trades get more capital than low-conviction

**Setup**:
Create mock scenario with known conviction scores:
- Signal A: conviction 95 (very high)
- Signal B: conviction 75 (medium)
- Signal C: conviction 50 (low)

**Manual Test** (modify workflow temporarily or use Python REPL):
```python
from sentinel.order_generator import OrderGenerator

# Mock scenario
account_value = 100000
available_cash = 100000
logger = None

gen = OrderGenerator(account_value=account_value, logger=logger)

# Mock signals
signals = [
    {'symbol': 'SIGNAL_A', 'conviction_score': 95, 'entry': 100.0, 'stop': 95.0, 'decision': 'BUY'},
    {'symbol': 'SIGNAL_B', 'conviction_score': 75, 'entry': 50.0, 'stop': 47.5, 'decision': 'BUY'},
    {'symbol': 'SIGNAL_C', 'conviction_score': 50, 'entry': 25.0, 'stop': 23.75, 'decision': 'BUY'},
]

# Generate orders
orders = gen.generate_buy_orders(
    signals=signals,
    available_cash=available_cash
)

# Analyze allocation
print("Conviction Weighting Test Results")
print("-" * 70)
print(f"{'Symbol':<10} {'Conviction':<12} {'Qty':<8} {'Value':<12} {'% of Cash':<12}")
print("-" * 70)

total_value = 0
for order in orders:
    value = order['qty'] * order['entry']
    pct = (value / available_cash) * 100
    total_value += value
    print(f"{order['symbol']:<10} {order['conviction']:<12} {order['qty']:<8} ${value:<11,.2f} {pct:<11.1f}%")

print("-" * 70)
print(f"Total allocated: ${total_value:,.2f} ({(total_value/available_cash)*100:.1f}% of cash)")
```

**Expected Output** (approximate):
```
Symbol     Conviction   Qty      Value        % of Cash
----------------------------------------------------------------------
SIGNAL_A   95           500      $50,000.00   50.0%
SIGNAL_B   75           300      $15,000.00   15.0%
SIGNAL_C   50           100      $2,500.00    2.5%
----------------------------------------------------------------------
Total allocated: $67,500.00 (67.5% of cash)
```

**Pass Criteria**:
- SIGNAL_A gets MOST capital (highest conviction)
- SIGNAL_B gets MEDIUM capital
- SIGNAL_C gets LEAST capital (lowest conviction)
- Ratio of allocations makes sense (not equal distribution)
- Total allocation ≤100% of available cash

**FAIL Criteria**:
- Equal allocation to all three (bug still exists!)
- Inverted allocation (low conviction gets more than high)
- Total allocation >100% (cash constraint violation)

---

### Test 2.3: BUY Filtering Threshold
**Goal**: Verify signals below 70 conviction are filtered out

**Test Data** (create mock Tier 3 output):
```python
mock_tier3_results = [
    {'symbol': 'HIGH_A', 'decision': 'BUY', 'conviction_score': 95},
    {'symbol': 'HIGH_B', 'decision': 'BUY', 'conviction_score': 78},
    {'symbol': 'THRESHOLD', 'decision': 'BUY', 'conviction_score': 70},  # Edge case
    {'symbol': 'LOW_A', 'decision': 'BUY', 'conviction_score': 65},  # Should filter
    {'symbol': 'LOW_B', 'decision': 'BUY', 'conviction_score': 50},  # Should filter
    {'symbol': 'SELL_X', 'decision': 'SELL', 'conviction_score': 20},  # Should execute anyway
]
```

**Expected Behavior**:
- HIGH_A: ✅ Executed (95 ≥ 70)
- HIGH_B: ✅ Executed (78 ≥ 70)
- THRESHOLD: ✅ Executed (70 ≥ 70, edge case)
- LOW_A: ❌ Filtered (65 < 70)
- LOW_B: ❌ Filtered (50 < 70)
- SELL_X: ✅ Executed (SELL ignores threshold)

**How to Test**:
1. Add temporary logging to workflow showing filtering decisions
2. Run dry-run with mock data
3. Verify logs show correct filtering

**Expected Log Output**:
```
[INFO] BUY signal filtering: 3/5 above 70 threshold
[INFO]   Filtered out: LOW_A (conviction: 65)
[INFO]   Filtered out: LOW_B (conviction: 50)
[INFO] [DRY-RUN] Would execute 1 SELL orders (no filtering)
[INFO] [DRY-RUN] Would execute 3 BUY orders (after filtering)
```

**Pass Criteria**:
- Signals ≥70 pass filter
- Signals <70 are filtered out
- SELL signals ignore threshold (all execute)
- Logs clearly show what was filtered and why

---

### Test 2.4: SELL-then-BUY Cash Sequencing
**Goal**: Verify SELL orders execute first, freeing cash for BUY orders

**Scenario**:
- Account has $10,000 cash
- Current position: 100 shares of XYZ @ $200 = $20,000 value
- Tier 3 says: SELL XYZ (free up $20,000), BUY ABC for $25,000

**Expected Behavior**:
1. Execute SELL XYZ first → cash becomes $30,000
2. Execute BUY ABC for $25,000 → cash becomes $5,000
3. Final state: No XYZ position, 125 shares ABC, $5,000 cash

**How to Test** (requires real account state or sophisticated mocking):
Option A: Run workflow with real paper account that has a position
Option B: Mock scenario with manual calculation:

```python
# Starting state
cash = 10000
positions = {'XYZ': {'qty': 100, 'avg_entry': 200}}

# Tier 3 decisions
sell_signals = [{'symbol': 'XYZ', 'qty': 100, 'conviction': 85}]
buy_signals = [{'symbol': 'ABC', 'conviction': 90, 'entry': 200, 'stop': 190}]

# Step 6A: Execute SELLs first
for sell in sell_signals:
    sell_value = sell['qty'] * positions[sell['symbol']]['avg_entry']
    cash += sell_value
    del positions[sell['symbol']]
    print(f"SELL {sell['symbol']}: +${sell_value:,.2f} → Cash now ${cash:,.2f}")

# Step 6B: Execute BUYs second (with updated cash)
print(f"\nAvailable cash for BUYs: ${cash:,.2f}")

for buy in buy_signals:
    # Simplified allocation (25% of cash per buy)
    allocation = cash * 0.25
    qty = int(allocation / buy['entry'])
    cost = qty * buy['entry']

    if cost <= cash:
        positions[buy['symbol']] = {'qty': qty, 'avg_entry': buy['entry']}
        cash -= cost
        print(f"BUY {buy['symbol']}: {qty} shares @ ${buy['entry']} = ${cost:,.2f} → Cash now ${cash:,.2f}")
    else:
        print(f"BUY {buy['symbol']}: INSUFFICIENT CASH (need ${cost:,.2f}, have ${cash:,.2f})")
```

**Expected Output**:
```
SELL XYZ: +$20,000.00 → Cash now $30,000.00

Available cash for BUYs: $30,000.00
BUY ABC: 37 shares @ $200 = $7,400.00 → Cash now $22,600.00
```

**Pass Criteria**:
- SELL executes first
- Cash increases after SELL
- BUY executes second with updated cash amount
- No "insufficient cash" errors
- Final cash balance makes sense

**FAIL Criteria**:
- BUY attempts before SELL completes
- "Insufficient cash" error despite SELL freeing capital
- Final cash balance goes negative
- Cash calculation doesn't reflect SELL proceeds

---

### Test 2.5: Perplexity Error Handling
**Goal**: Verify graceful degradation if Perplexity API fails

**How to Test**:
1. Temporarily break Perplexity API key in config
2. Run workflow dry-run
3. Verify system falls back to generic context

**Expected Behavior**:
- Perplexity fetch fails with error
- System logs warning
- Falls back to: "Market conditions vary - see detailed analysis"
- Workflow continues (doesn't crash)
- Tier 2/3 still execute (with generic context)

**Expected Log Output**:
```
[INFO] Step 5: Tier 2 AI Screening
[INFO]   Gathering real-time market overview...
[WARNING]   Could not fetch market overview: 401 Unauthorized. Using fallback.
[INFO]   Tier 2 complete: 15 candidates → 8 finalists
```

**Pass Criteria**:
- Warning logged (not fatal error)
- Workflow continues
- Generic context used as fallback
- Tier 2/3 still execute

**FAIL Criteria**:
- Workflow crashes
- Exception propagates and kills execution
- Tier 2/3 skip execution

---

## Test Suite 3: PDT Compliance Validation

### Test 3.1: Day Trade Detection
**Goal**: Verify system correctly identifies day trades

**Definition**: Day trade = BUY and SELL of same stock on same day

**Test Scenarios**:
1. Buy AAPL Monday 9am, Sell AAPL Monday 3pm → DAY TRADE ✓
2. Buy AAPL Monday 9am, Sell AAPL Tuesday 9am → NOT day trade
3. Sell AAPL Monday 9am (existing position), Buy AAPL Monday 3pm → DAY TRADE ✓
4. Buy AAPL Monday, Sell 50% Tuesday, Sell 50% Wednesday → NOT day trades

**How to Test**:
Need to find or implement day trade counting logic. Search codebase:

```bash
grep -r "day.trade" sentinel/ --ignore-case
grep -r "pdt" sentinel/ --ignore-case
grep -r "pattern.day" sentinel/ --ignore-case
```

**Expected**: Should find logic that:
- Tracks trades by symbol and date
- Counts round-trips (buy→sell or sell→buy on same day)
- Warns or blocks 4th day trade in 5-day window

**⚠️ CRITICAL**: If search returns NOTHING → we have a gap!
- System may be submitting orders without PDT checks
- Paper account could get suspended

**Action if Missing**:
1. DO NOT go live until implemented
2. Add day trade counting to execution engine
3. Add pre-flight check before order submission

---

### Test 3.2: 5-Day Rolling Window
**Goal**: Verify 5-day window calculation is correct

**Example**:
```
Mon Oct 23: Day trade #1
Tue Oct 24: Day trade #2
Wed Oct 25: Day trade #3
Thu Oct 26: (none)
Fri Oct 27: (none)
Mon Oct 30: Can now do 1 more (day trade #1 aged out)
```

**Pass Criteria**:
- Window is 5 BUSINESS days (excludes weekends)
- Oldest day trade drops off after 5 business days
- Count resets correctly

**How to Test**: Manual calculation with mock trade history

---

## Test Suite 4: Edge Cases & Error Scenarios

### Test 4.1: Empty Candidate Lists
**Scenario**: What if Tier 1 returns zero candidates?

**How to Test**: Run workflow on a day with extreme market conditions (or mock empty list)

**Expected Behavior**:
- Tier 1 logs: "0 candidates passed filters"
- Tier 2 skipped (nothing to screen)
- Tier 3 skipped (nothing to analyze)
- Workflow completes cleanly
- No orders submitted

---

### Test 4.2: All HOLD Decisions
**Scenario**: Tier 3 says HOLD for all 70 finalists

**Expected Behavior**:
- No BUY signals to execute
- No SELL signals to execute
- Logs: "No actionable signals today"
- Workflow completes cleanly
- Existing positions maintained with stops

---

### Test 4.3: API Rate Limiting
**Scenario**: Perplexity or OpenAI rate limit hit

**Expected Behavior**:
- Graceful backoff/retry
- Or skip affected tickers with warning
- Workflow continues for unaffected tickers
- Doesn't crash entire system

---

### Test 4.4: Conviction Score Edge Cases
**Test Data**:
- Conviction = 0 (invalid, should reject or default)
- Conviction = 101 (invalid, should clamp to 100)
- Conviction = NaN (error, should catch)
- Conviction = "high" (type error, should catch)

**Expected Behavior**:
- Invalid scores rejected or defaulted to safe value (50)
- Error logged
- Signal skipped rather than crashing

---

## Test Suite 5: Real-World Validation

### Test 5.1: Historical Backtest (Optional)
**Goal**: Run workflow on historical data to validate logic

**How**:
1. Pick a past date (e.g., Oct 20, 2025)
2. Mock market data for that date
3. Run workflow and record decisions
4. Compare to what actually happened

**Value**: Can validate if signals made sense historically

---

### Test 5.2: Paper Trading Observation Week
**Goal**: Run live in paper trading but don't risk real money

**Plan**:
- Week 1: Run workflow, observe, don't modify
- Monitor for:
  - Unexpected behavior
  - Orders rejected by broker
  - Position sizing issues
  - PDT violations
  - Cash constraint errors

- Daily review:
  - Check logs for errors
  - Verify orders submitted correctly
  - Validate conviction weighting working
  - Ensure stops placed properly

---

## Test Results Checklist

Before considering going live, verify ALL of these pass:

### Component Tests
- [ ] Perplexity integration works (news + market overview)
- [ ] Conviction weighting formula correct (high scores get more capital)
- [ ] Database operations work (`conviction_sells` table functional)

### Integration Tests
- [ ] Morning workflow dry-run completes without crashes
- [ ] BUY filtering threshold works (signals <70 filtered)
- [ ] SELL-then-BUY sequencing correct (cash frees before BUY)
- [ ] Perplexity error handling graceful (fallback works)

### PDT Compliance
- [ ] Day trade counting logic exists and is correct
- [ ] 5-day rolling window calculation correct
- [ ] System prevents 4th day trade in 5-day window

### Edge Cases
- [ ] Empty candidate lists handled gracefully
- [ ] All HOLD decisions handled gracefully
- [ ] Invalid conviction scores caught and handled
- [ ] API rate limiting doesn't crash system

### Manual Review
- [ ] Log files reviewed and make sense
- [ ] Order quantities reasonable (not oversized)
- [ ] Stop-loss prices calculated correctly
- [ ] Cash calculations correct (no overdraft)

---

## Go/No-Go Decision Criteria

### ✅ SAFE TO GO LIVE (Paper Trading)
- All component tests pass
- All integration tests pass
- PDT compliance verified
- Edge cases handled gracefully
- Manual review shows reasonable behavior
- You feel confident in the system

### ⚠️ PROCEED WITH EXTREME CAUTION
- Most tests pass but some edge cases uncertain
- PDT compliance exists but not thoroughly tested
- Minor bugs found but not critical

### 🛑 DO NOT GO LIVE
- Any component test fails
- PDT compliance missing or broken
- Cash constraint violations observed
- Frequent crashes or errors
- Conviction weighting still broken
- You feel uncertain or rushed

---

## Post-Deployment Monitoring (After Going Live)

Even after testing passes, monitor closely for first week:

### Daily Checklist
- [ ] Review morning workflow logs (any errors?)
- [ ] Check Alpaca account (orders submitted correctly?)
- [ ] Verify positions match expected (no surprises?)
- [ ] Validate stops are in place (every position has stop?)
- [ ] Check day trade count (staying under limit?)
- [ ] Review conviction scores (reasonable distribution?)

### Weekly Checklist
- [ ] Analyze filled orders (conviction weighting working?)
- [ ] Compare SELL vs stop-loss exits (which performs better?)
- [ ] Review win rate and P&L (system profitable?)
- [ ] Check API costs (within budget?)
- [ ] Evaluate Perplexity value (is news helpful?)

---

## Appendix A: Testing Commands Quick Reference

### Run Perplexity Test
```bash
python sentinel/perplexity_news.py
```

### Check Database Schema
```bash
sqlite3 sentinel.db ".schema conviction_sells"
```

### Run Migration
```bash
sqlite3 sentinel.db < database_migrations/004_add_conviction_sells.sql
```

### Check Git Status
```bash
git status
git log --oneline -5
```

### Search for PDT Logic
```bash
grep -r "day.trade" sentinel/ --ignore-case
grep -r "pdt" sentinel/ --ignore-case
```

### View Recent Logs
```bash
ls -lt logs/ | head -10
tail -100 logs/sentinel_morning_YYYYMMDD.log
```

---

## Appendix B: Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'config'"
**Solution**: Ensure you're running from project root, not subdirectory

### Issue: "Database locked"
**Solution**: Close all SQLite connections, restart terminal

### Issue: Perplexity 401 Unauthorized
**Solution**: Check `config.py` has correct `PERPLEXITY_API_KEY`

### Issue: OpenAI 429 Rate Limit
**Solution**: Wait 60 seconds, or reduce batch size (70 → 50 finalists)

### Issue: Alpaca "buying power insufficient"
**Solution**: SELL signals need to execute BEFORE BUY signals

### Issue: All conviction scores = 50
**Solution**: Bug in Tier 3 prompt or parsing logic

---

## Summary

This test plan is comprehensive but not exhaustive. The goal is to catch the most likely bugs before they cost you real money (even in paper trading, PDT violations hurt).

**Estimated Testing Time**: 4-6 hours for thorough testing

**Priority Order**:
1. Component tests (1 hour)
2. Integration dry-run (1 hour)
3. PDT compliance validation (1 hour)
4. Edge case testing (1 hour)
5. Manual log review (1 hour)

**Bottom Line**: Investing 4-6 hours in testing now could save you from a 90-day PDT suspension, capital loss from bugs, or embarrassing order errors.

**Tomorrow Morning Decision**: Based on test results, decide whether to:
- ✅ Go live with paper trading (if all tests pass)
- ⚠️ Go live but with tiny position sizes (if mostly passing)
- 🛑 Continue testing (if major issues found)

Good luck! 🚀
