---
from: TRADING
message_id: MSG_TRADING_20260407T160722Z_b1bdbbe3
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-07T16:07:22.430551Z'
to: EXECUTIVE
---

# ORDER REJECTED: ARM (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** ARM
- **Action:** BUY
- **Quantity:** 42

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $9,567.20 cash (9.3%), below 10% reserve (limit: 0.1, actual: 0.09312849371796889)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.