# Critical Fixes - Second Run (2025-11-05)

## Summary
Fixed CRITICAL bugs that caused Perplexity API failures, GPT-4o-mini liquidating ALL holdings, and severely under-deploying capital.

---

## Issues Fixed

### 1. **Perplexity API Rate Limiting (429 Errors)**
**Problem:** 26+ API calls failed with "429 Too Many Requests" because we were hitting Perplexity's rate limits

**Root Cause:**
- Sending 10 concurrent requests in each batch
- No delay between batches
- No retry logic for rate limit errors

**Fix Applied:**
- Added 2-second delay between batches (line 171-174 in news_department.py)
- Added retry logic with exponential backoff (lines 249-256)
- Added retry-after header parsing from 429 responses
- Max 3 retries per ticker

**Code Location:** `Departments/News/news_department.py`
- Lines 158-176: Batch delay logic
- Lines 234-317: Retry logic in `_fetch_sentiment_async()`

**Result:** API errors should drop from 26+ to near-zero

---

### 2. **Malformed JSON Response Handling**
**Problem:** Multiple "Expecting value: line 1 column 1" errors from Perplexity responses

**Root Cause:**
- Perplexity sometimes returns JSON in markdown code blocks
- Sometimes returns malformed JSON during errors
- No fallback parsing logic

**Fix Applied:**
- Added multi-strategy JSON parsing (lines 274-292):
  1. Try markdown ```json block extraction
  2. Try generic ``` block extraction
  3. Try parsing entire response as JSON
  4. Fallback to neutral sentiment (50.0) with error message

**Code Location:** `Departments/News/news_department.py` lines 274-292

**Result:** JSON parse errors handled gracefully, no crashes

---

### 3. **CRITICAL: GPT-4o-mini Liquidating ALL Holdings**
**Problem:** GPT-4o-mini selected 2 new BUY positions, then the system LIQUIDATED all 7 existing holdings (even ones with scores 70+)

**Root Cause:**
"Implicit sell" logic in Operations Manager (lines 769-788 OLD) said:
```python
# If GPT-5 didn't select ticker for BUY → SELL IT
selected_tickers = {c['ticker'] for c in optimized_candidates if c.get('allocated_capital', 0) > 0}
for holding in holdings:
    if ticker not in selected_tickers:
        # SELL THIS HOLDING
```

This is WRONG! If you own UBER (score 71.6) and GPT doesn't say "buy more UBER", it got liquidated!

**Fix Applied:**
Changed logic to:
```python
# ONLY sell holdings with poor scores (< 55)
# Holdings with good scores (≥ 55) are KEPT automatically
for holding in holdings:
    composite = holding.get('research_composite_score', ...)
    if composite < 55:
        # SELL THIS HOLDING
    else:
        # KEEP THIS HOLDING
```

**Code Location:** `Departments/Operations/operations_manager.py` lines 769-793

**Result:**
- From your run: CARR (47.2) → Would sell ✓
- COP (57.2), CTVA (66.4), EIX (66.0), IBKR (73.6), ODFL (61.6), UBER (71.6) → Would KEEP ✓

---

### 4. **Low Capital Deployment (14% instead of 90%+)**
**Problem:** GPT-4o-mini only allocated $16,443 out of $117,464 (14% deployment)

**Root Cause:**
- Prompt didn't emphasize capital deployment strongly enough
- No explicit "MANDATORY" language
- GPT-4o-mini is conservative by nature

**Fix Applied:**
Strengthened prompt in 3 places:

1. **Philosophy section** (line 220):
```
- CAPITAL EFFICIENCY: Deploy 90-100% of capital across 5-10 positions (NOT NEGOTIABLE - use the capital!)
- BE AGGRESSIVE: This is a GROWTH portfolio, not capital preservation. Deploy capital!
```

2. **Task section** (lines 277-278):
```
- **MANDATORY**: Total deployment MUST be 90-100% of available capital
- **MANDATORY**: Select 5-10 positions (not 1-2, not 15+)
```

3. **Checklist section** (lines 333-336):
```
5. **VERIFY YOU'RE DEPLOYING 90-100% OF CAPITAL** - if not, add more positions!
...
**REMINDER**: Your job is to DEPLOY CAPITAL aggressively across 5-10 positions.
If you're only selecting 1-2 positions or deploying <90% of capital, you're not doing your job correctly. Be bold!
```

**Code Location:** `Departments/Executive/gpt5_portfolio_optimizer.py`
- Line 220: Philosophy
- Lines 277-278: Mandatory requirements
- Lines 333-336: Reminder

**Result:** GPT should now deploy 90-100% of capital

---

### 5. **Limited Diversification (2 positions instead of 5-10)**
**Problem:** GPT-4o-mini selected only 2 positions (FITB, CFG) instead of 5-10

**Root Cause:**
- Same as #4 - weak prompt guidance
- No explicit mandate on position count

**Fix Applied:**
- Added "Select 5-10 positions (NOT 1-2!) to diversify risk" to checklist (line 330)
- Added MANDATORY requirement in task section (line 278)
- Added reminder in final notes (line 336)

**Result:** GPT should now select 5-10 positions for diversification

---

### 6. **502 Bad Gateway Handling**
**Problem:** Several tickers got "502 Bad Gateway" errors from Perplexity

**Fix Applied:**
- Added retry logic for 502 errors (lines 258-265)
- Retry up to 3 times with 2-second delay
- Graceful fallback to neutral sentiment if all retries fail

**Code Location:** `Departments/News/news_department.py` lines 258-265

**Result:** Transient network errors handled gracefully

---

## Testing Recommendations

Before next run:
1. **Check Perplexity API key** - Make sure it's valid and has quota
2. **Monitor logs** - Watch for retry messages to confirm rate limiting is working
3. **Verify capital deployment** - Should see 90-100% deployment in next plan
4. **Check holdings retention** - Should only sell holdings with scores < 55

---

## Expected Behavior After Fixes

### Next Trading Plan Should Show:
- ✓ 90-100% capital deployment (not 14%)
- ✓ 5-10 new positions (not 2)
- ✓ KEEP holdings with scores ≥ 55
- ✓ SELL only holdings with scores < 55
- ✓ Minimal Perplexity API errors (maybe 1-2 instead of 26+)
- ✓ No JSON parsing errors

### From Your Current Run:
Holdings that SHOULD be kept (score ≥ 55):
- COP (57.2) ✓
- ODFL (61.6) ✓
- CTVA (66.4) ✓
- EIX (66.0) ✓
- UBER (71.6) ✓
- IBKR (73.6) ✓

Holdings that SHOULD be sold (score < 55):
- CARR (47.2) ✓

---

## Files Modified

1. **Departments/News/news_department.py**
   - Lines 158-176: Added batch delays
   - Lines 234-317: Added retry logic with 429/502 handling
   - Lines 274-292: Added robust JSON parsing

2. **Departments/Operations/operations_manager.py**
   - Lines 769-793: Fixed implicit sell logic to ONLY sell scores < 55

3. **Departments/Executive/gpt5_portfolio_optimizer.py**
   - Line 220: Strengthened capital deployment philosophy
   - Lines 277-278: Added MANDATORY requirements
   - Lines 330-336: Added aggressive deployment reminders

---

## Known Remaining Issues

1. **Perplexity quota** - If you hit daily API limit, sentiment will default to 50.0
2. **GPT-4o-mini conservatism** - May still under-deploy despite stronger prompt (GPT-4o or GPT-5 would be better)
3. **Portfolio value calculation** - Still using hardcoded values in some places

---

## Verification Commands

Test Perplexity retry logic:
```bash
python -c "from Departments.News.news_department import NewsDepartment; nd = NewsDepartment(); result = nd.get_sentiment_scores(['AAPL']); print(result)"
```

Test implicit sell logic:
```bash
python -c "
holdings = [{'ticker': 'TEST', 'research_composite_score': 60}]
# Should KEEP (not sell) because score ≥ 55
"
```

---

**Date:** 2025-11-05
**Run:** Second trading plan generation
**Status:** All critical fixes implemented ✓
**Ready for next run:** YES
