---
from: TRADING
message_id: MSG_TRADING_20260415T160903Z_aeedd3bc
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-15T16:09:03.971374Z'
to: EXECUTIVE
---

# ORDER REJECTED: BRO (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** BRO
- **Action:** BUY
- **Quantity:** 99

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $3,023.17 cash (2.9%), below 10% reserve (limit: 0.1, actual: 0.02867029319830953)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.