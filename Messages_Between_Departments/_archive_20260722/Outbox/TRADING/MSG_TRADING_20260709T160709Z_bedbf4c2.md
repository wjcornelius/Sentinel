---
from: TRADING
message_id: MSG_TRADING_20260709T160709Z_bedbf4c2
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-07-09T16:07:09.050487Z'
to: EXECUTIVE
---

# ORDER REJECTED: FTI (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** FTI
- **Action:** BUY
- **Quantity:** 142

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $398.77 cash (0.4%), below 10% reserve (limit: 0.1, actual: 0.0037039998920711205)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.