---
from: TRADING
message_id: MSG_TRADING_20260505T161137Z_2a5adbdd
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-05T16:11:37.144011Z'
to: EXECUTIVE
---

# ORDER REJECTED: CLSK (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CLSK
- **Action:** BUY
- **Quantity:** 749

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,452.31 cash (6.5%), below 10% reserve (limit: 0.1, actual: 0.06530026465263065)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.