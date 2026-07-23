---
from: TRADING
message_id: MSG_TRADING_20260626T160720Z_bdb7de9c
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-06-26T16:07:20.706293Z'
to: EXECUTIVE
---

# ORDER REJECTED: LYFT (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** LYFT
- **Action:** BUY
- **Quantity:** 690

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $5,299.33 cash (4.7%), below 10% reserve (limit: 0.1, actual: 0.047481792381550744)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.