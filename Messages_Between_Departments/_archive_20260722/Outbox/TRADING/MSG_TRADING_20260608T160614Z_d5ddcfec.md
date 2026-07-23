---
from: TRADING
message_id: MSG_TRADING_20260608T160614Z_d5ddcfec
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-06-08T16:06:14.984867Z'
to: EXECUTIVE
---

# ORDER REJECTED: COLB (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** COLB
- **Action:** BUY
- **Quantity:** 336

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-18,985.77) (limit: 0, actual: -18985.770128173826)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.