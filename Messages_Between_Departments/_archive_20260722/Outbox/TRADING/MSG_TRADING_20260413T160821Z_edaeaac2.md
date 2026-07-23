---
from: TRADING
message_id: MSG_TRADING_20260413T160821Z_edaeaac2
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-13T16:08:21.912227Z'
to: EXECUTIVE
---

# ORDER REJECTED: CDE (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CDE
- **Action:** BUY
- **Quantity:** 323

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $8,921.46 cash (8.6%), below 10% reserve (limit: 0.1, actual: 0.08586196190375327)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.