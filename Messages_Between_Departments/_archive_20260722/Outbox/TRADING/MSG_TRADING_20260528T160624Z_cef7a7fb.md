---
from: TRADING
message_id: MSG_TRADING_20260528T160624Z_cef7a7fb
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-28T16:06:24.092709Z'
to: EXECUTIVE
---

# ORDER REJECTED: KLAR (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** KLAR
- **Action:** BUY
- **Quantity:** 560

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-2,010.28) (limit: 0, actual: -2010.279965820312)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.