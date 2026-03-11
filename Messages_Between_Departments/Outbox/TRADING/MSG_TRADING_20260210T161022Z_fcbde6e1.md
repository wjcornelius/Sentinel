---
from: TRADING
message_id: MSG_TRADING_20260210T161022Z_fcbde6e1
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-02-10T16:10:22.970482Z'
to: EXECUTIVE
---

# ORDER REJECTED: APO (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** APO
- **Action:** BUY
- **Quantity:** 47

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $2,502.37 cash (2.4%), below 10% reserve (limit: 0.1, actual: 0.02377412595502694)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.