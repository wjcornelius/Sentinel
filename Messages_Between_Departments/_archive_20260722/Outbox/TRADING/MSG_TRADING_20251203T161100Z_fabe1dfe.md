---
from: TRADING
message_id: MSG_TRADING_20251203T161100Z_fabe1dfe
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-12-03T16:11:00.106996Z'
to: EXECUTIVE
---

# ORDER REJECTED: DELL (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** DELL
- **Action:** BUY
- **Quantity:** 37

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-4,167.46) (limit: 0, actual: -4167.46)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.