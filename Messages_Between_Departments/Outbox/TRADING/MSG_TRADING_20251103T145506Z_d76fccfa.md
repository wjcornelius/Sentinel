---
from: TRADING
message_id: MSG_TRADING_20251103T145506Z_d76fccfa
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-11-03T14:55:06.960399Z'
to: EXECUTIVE
---

# ORDER REJECTED: IBKR (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** IBKR
- **Action:** BUY
- **Quantity:** 213

**Violations:**
- **price_available:** Cannot determine current price (limit: valid price required, actual: 0)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.