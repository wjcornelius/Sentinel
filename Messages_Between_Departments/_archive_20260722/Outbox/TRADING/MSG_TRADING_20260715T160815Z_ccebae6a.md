---
from: TRADING
message_id: MSG_TRADING_20260715T160815Z_ccebae6a
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-07-15T16:08:15.033087Z'
to: EXECUTIVE
---

# ORDER REJECTED: SBRA (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** SBRA
- **Action:** BUY
- **Quantity:** 508

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $8,395.26 cash (7.9%), below 10% reserve (limit: 0.1, actual: 0.07856449267628755)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.