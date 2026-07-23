---
from: TRADING
message_id: MSG_TRADING_20260323T160941Z_cb4bcad5
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-03-23T16:09:41.009579Z'
to: EXECUTIVE
---

# ORDER REJECTED: OKE (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** OKE
- **Action:** BUY
- **Quantity:** 112

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,890.16 cash (7.8%), below 10% reserve (limit: 0.1, actual: 0.07782202583043242)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.