---
from: TRADING
message_id: MSG_TRADING_20260617T160730Z_d2eebf3a
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-06-17T16:07:30.095582Z'
to: EXECUTIVE
---

# ORDER REJECTED: BEAM (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** BEAM
- **Action:** BUY
- **Quantity:** 294

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,392.98 cash (6.7%), below 10% reserve (limit: 0.1, actual: 0.06673393694781048)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.