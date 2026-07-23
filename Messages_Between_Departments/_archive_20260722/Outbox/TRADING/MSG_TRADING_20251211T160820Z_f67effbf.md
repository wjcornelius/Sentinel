---
from: TRADING
message_id: MSG_TRADING_20251211T160820Z_f67effbf
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-12-11T16:08:20.384577Z'
to: EXECUTIVE
---

# ORDER REJECTED: CSGP (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CSGP
- **Action:** BUY
- **Quantity:** 73

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $487.97 cash (0.5%), below 10% reserve (limit: 0.1, actual: 0.004804030398273811)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.