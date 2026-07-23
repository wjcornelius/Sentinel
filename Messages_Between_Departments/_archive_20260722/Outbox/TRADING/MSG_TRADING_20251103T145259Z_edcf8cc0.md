---
from: TRADING
message_id: MSG_TRADING_20251103T145259Z_edcf8cc0
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-11-03T14:52:59.579250Z'
to: EXECUTIVE
---

# ORDER REJECTED: IVZ (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** IVZ
- **Action:** BUY
- **Quantity:** 632

**Violations:**
- **price_available:** Cannot determine current price (limit: valid price required, actual: 0)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.