---
from: TRADING
message_id: MSG_TRADING_20260522T160642Z_a0ae6acc
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-22T16:06:42.251236Z'
to: EXECUTIVE
---

# ORDER REJECTED: CCI (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CCI
- **Action:** BUY
- **Quantity:** 98

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-5,884.44) (limit: 0, actual: -5884.440209350586)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.