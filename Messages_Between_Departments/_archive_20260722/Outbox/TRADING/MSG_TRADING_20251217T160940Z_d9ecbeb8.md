---
from: TRADING
message_id: MSG_TRADING_20251217T160940Z_d9ecbeb8
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-12-17T16:09:40.140123Z'
to: EXECUTIVE
---

# ORDER REJECTED: CG (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CG
- **Action:** BUY
- **Quantity:** 86

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,026.81 cash (7.1%), below 10% reserve (limit: 0.1, actual: 0.07089633951068411)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.