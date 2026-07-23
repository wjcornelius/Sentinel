---
from: TRADING
message_id: MSG_TRADING_20260417T160659Z_caff6c3b
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-17T16:06:59.018702Z'
to: EXECUTIVE
---

# ORDER REJECTED: CNM (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CNM
- **Action:** BUY
- **Quantity:** 132

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-1,369.26) (limit: 0, actual: -1369.260080566406)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.