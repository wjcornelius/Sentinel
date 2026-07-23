---
from: TRADING
message_id: MSG_TRADING_20260416T160841Z_dab1fd7d
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-16T16:08:41.774575Z'
to: EXECUTIVE
---

# ORDER REJECTED: CNM (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CNM
- **Action:** BUY
- **Quantity:** 127

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-1,144.29) (limit: 0, actual: -1144.2901937866209)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.