---
from: TRADING
message_id: MSG_TRADING_20260414T160831Z_dcb3cdec
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-14T16:08:31.339580Z'
to: EXECUTIVE
---

# ORDER REJECTED: GILD (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** GILD
- **Action:** BUY
- **Quantity:** 48

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,032.36 cash (6.6%), below 10% reserve (limit: 0.1, actual: 0.06610360395209788)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.