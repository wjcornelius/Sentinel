---
from: TRADING
message_id: MSG_TRADING_20260422T160637Z_b24deddc
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-22T16:06:37.451568Z'
to: EXECUTIVE
---

# ORDER REJECTED: FOXA (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** FOXA
- **Action:** BUY
- **Quantity:** 107

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,532.59 cash (6.9%), below 10% reserve (limit: 0.1, actual: 0.06913557472869622)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.