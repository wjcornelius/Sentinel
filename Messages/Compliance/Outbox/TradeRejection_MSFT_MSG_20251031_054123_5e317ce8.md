---
from: Compliance
in_reply_to: MSG_20251031_054123_test01
message_id: MSG_20251031_054123_5e317ce8
message_type: TradeRejection
payload:
  check_results:
    duplicate_order_check: SKIP
    position_size_check: FAIL
    restricted_ticker_check: PASS
    risk_limit_check: SKIP
    sector_concentration_check: SKIP
  rejection_category: POSITION_SIZE
  rejection_reason: Position size 19.0% of portfolio exceeds maximum 10.0% ($19,000.00
    of $100,000.00)
  ticker: MSFT
  trade_proposal_message_id: MSG_20251031_054123_test01
  validation_status: REJECTED
timestamp: '2025-10-31T05:41:23.991221'
to: Portfolio
---

# TradeRejection

**Ticker:** MSFT
**Status:** REJECTED
**Trade Proposal:** MSG_20251031_054123_test01

## Rejection Details

**Category:** POSITION_SIZE
**Reason:** Position size 19.0% of portfolio exceeds maximum 10.0% ($19,000.00 of $100,000.00)

## Failed Checks

- ❌ position_size_check: FAIL
- ✅ sector_concentration_check: SKIP
- ✅ risk_limit_check: SKIP
- ✅ duplicate_order_check: SKIP
- ✅ restricted_ticker_check: PASS
