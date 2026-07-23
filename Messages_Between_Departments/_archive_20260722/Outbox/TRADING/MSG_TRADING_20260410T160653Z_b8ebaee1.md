---
from: TRADING
message_id: MSG_TRADING_20260410T160653Z_b8ebaee1
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-10T16:06:53.895764Z'
to: EXECUTIVE
---

# ORDER REJECTED: HSAI (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** HSAI
- **Action:** BUY
- **Quantity:** 339

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,660.31 cash (7.4%), below 10% reserve (limit: 0.1, actual: 0.07405971766485585)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.