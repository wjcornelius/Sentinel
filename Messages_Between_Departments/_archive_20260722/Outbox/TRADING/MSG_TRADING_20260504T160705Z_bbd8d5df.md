---
from: TRADING
message_id: MSG_TRADING_20260504T160705Z_bbd8d5df
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-04T16:07:05.428762Z'
to: EXECUTIVE
---

# ORDER REJECTED: MGY (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** MGY
- **Action:** BUY
- **Quantity:** 267

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $9,244.03 cash (8.4%), below 10% reserve (limit: 0.1, actual: 0.08445862291148731)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.