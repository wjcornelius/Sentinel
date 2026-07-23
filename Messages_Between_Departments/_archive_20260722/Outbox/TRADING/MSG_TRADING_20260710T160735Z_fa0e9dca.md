---
from: TRADING
message_id: MSG_TRADING_20260710T160735Z_fa0e9dca
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-07-10T16:07:35.860662Z'
to: EXECUTIVE
---

# ORDER REJECTED: EBC (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** EBC
- **Action:** BUY
- **Quantity:** 449

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $4,335.45 cash (4.0%), below 10% reserve (limit: 0.1, actual: 0.04025185675056696)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.