---
from: TRADING
message_id: MSG_TRADING_20260518T160710Z_a32ebbdb
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-18T16:07:10.264172Z'
to: EXECUTIVE
---

# ORDER REJECTED: EQT (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** EQT
- **Action:** BUY
- **Quantity:** 173

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $2,508.09 cash (2.3%), below 10% reserve (limit: 0.1, actual: 0.023024201800735576)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.