---
from: TRADING
message_id: MSG_TRADING_20260604T160639Z_e87cdecc
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-06-04T16:06:39.865262Z'
to: EXECUTIVE
---

# ORDER REJECTED: IREN (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** IREN
- **Action:** BUY
- **Quantity:** 164

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-5,084.18) (limit: 0, actual: -5084.179774780274)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.