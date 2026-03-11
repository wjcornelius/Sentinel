---
from: TRADING
message_id: MSG_TRADING_20251218T161012Z_5aabc8cb
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-12-18T16:10:12.094555Z'
to: EXECUTIVE
---

# ORDER REJECTED: GSK (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** GSK
- **Action:** BUY
- **Quantity:** 103

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $6,983.54 cash (7.0%), below 10% reserve (limit: 0.1, actual: 0.06996394396842555)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.