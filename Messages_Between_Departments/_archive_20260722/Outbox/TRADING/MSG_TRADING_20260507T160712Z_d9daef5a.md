---
from: TRADING
message_id: MSG_TRADING_20260507T160712Z_d9daef5a
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-07T16:07:12.045097Z'
to: EXECUTIVE
---

# ORDER REJECTED: CG (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CG
- **Action:** BUY
- **Quantity:** 148

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $1,114.86 cash (1.0%), below 10% reserve (limit: 0.1, actual: 0.010004699427488002)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.