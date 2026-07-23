---
from: TRADING
message_id: MSG_TRADING_20260220T160811Z_7bbefbb8
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-02-20T16:08:11.586357Z'
to: EXECUTIVE
---

# ORDER REJECTED: MTCH (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** MTCH
- **Action:** BUY
- **Quantity:** 319

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-6,271.10) (limit: 0, actual: -6271.099902648926)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.