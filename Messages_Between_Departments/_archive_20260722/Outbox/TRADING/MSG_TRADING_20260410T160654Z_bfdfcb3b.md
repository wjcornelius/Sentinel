---
from: TRADING
message_id: MSG_TRADING_20260410T160654Z_bfdfcb3b
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-10T16:06:54.525363Z'
to: EXECUTIVE
---

# ORDER REJECTED: CF (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CF
- **Action:** BUY
- **Quantity:** 63

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,742.18 cash (7.5%), below 10% reserve (limit: 0.1, actual: 0.07485065894802363)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.