---
from: TRADING
message_id: MSG_TRADING_20260430T160710Z_aafda15e
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-30T16:07:10.569659Z'
to: EXECUTIVE
---

# ORDER REJECTED: CPRT (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CPRT
- **Action:** BUY
- **Quantity:** 212

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $7,826.61 cash (7.2%), below 10% reserve (limit: 0.1, actual: 0.07162322883460812)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.