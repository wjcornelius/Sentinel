---
from: TRADING
message_id: MSG_TRADING_20260310T160936Z_dcb79abc
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-03-10T16:09:36.366352Z'
to: EXECUTIVE
---

# ORDER REJECTED: SLM (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** SLM
- **Action:** BUY
- **Quantity:** 497

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-5,384.05) (limit: 0, actual: -5384.054772491455)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.