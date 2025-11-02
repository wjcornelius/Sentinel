# Week 2 Implementation Plan: Conviction Analysis + Order Generation

## Objective

Integrate three-tier conviction analysis system with v8 execution engine to enable automated order generation based on AI-driven stock analysis.

## Current State

**What We Have (Week 1):**
- ✅ OrderExecutionEngine with atomic entry+stop submission
- ✅ Trailing stop updates with staircase logic
- ✅ Profit-taking detection
- ✅ Orphaned stop cleanup
- ✅ Evening workflow orchestration (Steps 1-4, 7 complete)
- ✅ Database schema for order tracking
- ✅ Risk configuration system

**What's Missing:**
- ❌ Step 5: Conviction analysis (placeholder)
- ❌ Step 6: Order submission (placeholder)
- ❌ Integration with existing AI analysis code
- ❌ Three-tier filtering to reduce AI costs

## Target Architecture

### Three-Tier Filtering System

```
Russell 3000 Universe (~2500 liquid stocks)
            ↓
    Tier 1: Technical Filters
    - Liquidity: Volume > $1M/day
    - Price: $5 < price < $500
    - Momentum: ATR, RSI screens
    - Cost: ~$0 (cached data)
            ↓
    ~250 candidates
            ↓
    Tier 2: AI Screening (GPT-4o-mini)
    - Quick triage: "Worth deep analysis?"
    - Lightweight prompt (sector + headlines)
    - Score 1-10, keep top 70
    - Cost: ~$0.50
            ↓
    ~70 finalists
            ↓
    Tier 3: Deep Conviction Analysis (GPT-4 Turbo)
    - Full dossier analysis
    - Hierarchical context (market → sector → stock)
    - BUY/SELL/HOLD + conviction 1-10
    - Cost: ~$3.50
            ↓
    BUY signals with conviction scores
            ↓
    Capital Allocation (conviction-weighted)
            ↓
    Order Submission (entry + stop pairs)
```

**Total Daily Cost:** ~$4 (vs ~$125 for analyzing all 2500 stocks)

### Hierarchical Context System

```
Market Context (once per day)
    ↓
Sector Contexts (10-15 sectors)
    ↓
Stock Analysis (70 stocks with sector context)
```

**Benefits:**
- AI sees broader trends before individual stocks
- More coherent decisions within sectors
- Better understanding of relative opportunities

## Implementation Tasks

### Task 1: Create Tier 1 Technical Filter Module
**File:** `sentinel/tier1_technical_filter.py`

**Functions:**
- `fetch_universe_data()` - Get price/volume for Russell 3000
- `apply_liquidity_filter()` - Volume > $1M/day
- `apply_price_filter()` - $5 < price < $500
- `apply_momentum_filter()` - RSI, ATR, trend strength
- `filter_tier1_technical()` - Main entry point

**Output:** List of ~250 symbols

**Dependencies:**
- Alpaca market data API
- Pandas for calculations
- Existing RSI/ATR functions from main_script.py

### Task 2: Create Tier 2 AI Screening Module
**File:** `sentinel/tier2_ai_screening.py`

**Functions:**
- `build_screening_prompt()` - Lightweight prompt template
- `screen_stock_batch()` - Process 10-20 stocks at once
- `filter_tier2_ai_screening()` - Main entry point

**Output:** List of 70 stocks with screening scores

**Dependencies:**
- OpenAI API (GPT-4o-mini model)
- Alpaca news API
- Yahoo Finance for sector data

### Task 3: Create Hierarchical Context Builder
**File:** `sentinel/context_builder.py`

**Functions:**
- `fetch_market_context()` - Use existing Perplexity + GPT-4 logic
- `build_sector_contexts()` - Summarize trends per sector
- `build_hierarchical_context()` - Main orchestrator

**Output:** Dict of sector contexts

**Dependencies:**
- OpenAI API
- Tier 2 results for sector grouping

### Task 4: Adapt Existing Deep Analysis
**File:** `sentinel/tier3_conviction_analysis.py`

**Functions:**
- `build_stock_dossier()` - Extract from main_script.py
- `get_ai_conviction()` - Adapt get_ai_analysis() function
- `analyze_tier3_deep()` - Main entry point

**Output:** List of BUY/SELL/HOLD decisions with convictions

**Dependencies:**
- OpenAI API (GPT-4 Turbo)
- Existing ANALYSIS_PROMPT_TEMPLATE
- Alpaca API for price/volume/news
- Yahoo Finance for fundamentals

### Task 5: Create Order Generation Module
**File:** `sentinel/order_generator.py`

**Functions:**
- `conviction_to_weight()` - Extract from main_script.py
- `calculate_position_sizes()` - Conviction-weighted allocation
- `generate_entry_orders()` - Create order list with stops
- `apply_risk_limits()` - Enforce max position size, etc.

**Output:** List of {symbol, qty, entry_price, stop_price}

**Dependencies:**
- risk_config.py for limits
- Alpaca API for current portfolio value
- Existing conviction weighting logic

### Task 6: Integrate into Evening Workflow
**File:** `sentinel_evening_workflow.py`

**Changes:**
- Replace Step 5 placeholder with conviction analysis pipeline
- Replace Step 6 placeholder with order generation + submission
- Add error handling and logging
- Add dry-run mode for testing

**Output:** Complete end-to-end workflow

### Task 7: Create Test Suite
**File:** `tests/test_conviction_system.py`

**Tests:**
- test_tier1_filtering() - Verify technical filters work
- test_tier2_screening() - Mock AI responses
- test_tier3_analysis() - Mock full analysis
- test_order_generation() - Verify capital allocation
- test_integration() - End-to-end with mocked AI

## Timeline

**Session 1: Setup + Tier 1 (Technical Filters)**
- Create tier1_technical_filter.py
- Implement liquidity, price, momentum filters
- Test with real Russell 3000 data
- Verify ~250 output

**Session 2: Tier 2 (AI Screening)**
- Create tier2_ai_screening.py
- Implement GPT-4o-mini screening
- Test batching and scoring
- Verify ~70 output

**Session 3: Context + Tier 3 (Deep Analysis)**
- Create context_builder.py
- Create tier3_conviction_analysis.py
- Extract and adapt existing analysis logic
- Test hierarchical context flow

**Session 4: Order Generation + Integration**
- Create order_generator.py
- Extract capital allocation logic
- Integrate all tiers into workflow
- Add comprehensive logging

**Session 5: Testing + Validation**
- Create test suite
- Run dry-run end-to-end test
- Fix bugs and edge cases
- Document system

## Success Criteria

- [ ] Tier 1 filters reduce 2500 → 250 stocks reliably
- [ ] Tier 2 screens reduce 250 → 70 stocks with AI
- [ ] Tier 3 generates BUY/SELL/HOLD + conviction for 70 stocks
- [ ] Order generator creates valid entry+stop pairs
- [ ] Evening workflow executes all steps without errors
- [ ] Dry-run test completes successfully
- [ ] Total AI cost < $5/day
- [ ] All unit tests passing

## Risk Management

**AI API Failures:**
- Implement retry logic with exponential backoff
- Graceful degradation (skip tier if fails)
- Log failures for manual review

**Data Quality Issues:**
- Validate all inputs before AI calls
- Handle missing data gracefully
- Skip stocks with insufficient data

**Order Execution Risks:**
- Use dry-run mode extensively before live testing
- Verify risk limits enforced
- Check for duplicate orders
- Validate stop prices before submission

## Cost Optimization

**Tier 1:** $0 (local calculation)
**Tier 2:** ~$0.50 (250 stocks × GPT-4o-mini)
**Tier 3:** ~$3.50 (70 stocks × GPT-4 Turbo)
**Total:** ~$4/day

**Comparison:**
- Naive approach: 2500 stocks × $0.05 = $125/day
- Savings: 97% cost reduction
- Better quality: Focus AI on filtered candidates

---

**Status:** Ready to begin implementation
**Next Step:** Task 1 - Create Tier 1 Technical Filter Module
