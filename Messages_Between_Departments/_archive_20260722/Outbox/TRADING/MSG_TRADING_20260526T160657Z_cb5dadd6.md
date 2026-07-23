---
from: TRADING
message_id: MSG_TRADING_20260526T160657Z_cb5dadd6
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-26T16:06:57.901424Z'
to: EXECUTIVE
---

# ORDER REJECTED: BWA (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** BWA
- **Action:** BUY
- **Quantity:** 111

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $2,657.03 cash (2.4%), below 10% reserve (limit: 0.1, actual: 0.023598184814318256)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.