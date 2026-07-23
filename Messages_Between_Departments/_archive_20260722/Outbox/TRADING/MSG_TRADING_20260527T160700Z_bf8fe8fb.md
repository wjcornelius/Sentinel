---
from: TRADING
message_id: MSG_TRADING_20260527T160700Z_bf8fe8fb
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-27T16:07:00.167164Z'
to: EXECUTIVE
---

# ORDER REJECTED: MGNI (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** MGNI
- **Action:** BUY
- **Quantity:** 514

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $3,055.93 cash (2.7%), below 10% reserve (limit: 0.1, actual: 0.027121949388941326)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.