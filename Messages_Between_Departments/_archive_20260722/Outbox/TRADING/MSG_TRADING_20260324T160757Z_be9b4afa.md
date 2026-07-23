---
from: TRADING
message_id: MSG_TRADING_20260324T160757Z_be9b4afa
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-03-24T16:07:57.966220Z'
to: EXECUTIVE
---

# ORDER REJECTED: GLW (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** GLW
- **Action:** BUY
- **Quantity:** 51

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $9,261.98 cash (8.9%), below 10% reserve (limit: 0.1, actual: 0.0894347743116388)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.