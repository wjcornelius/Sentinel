---
from: TRADING
message_id: MSG_TRADING_20260529T160723Z_fbc6edbd
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-29T16:07:23.145380Z'
to: EXECUTIVE
---

# ORDER REJECTED: FOXA (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** FOXA
- **Action:** BUY
- **Quantity:** 120

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-181.50) (limit: 0, actual: -181.50010986328107)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.