---
from: TRADING
message_id: MSG_TRADING_20260525T160746Z_debecfa9
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-05-25T16:07:46.357224Z'
to: EXECUTIVE
---

# ORDER REJECTED: DLTR (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** DLTR
- **Action:** BUY
- **Quantity:** 73

**Violations:**
- **no_margin_trading:** Order would require margin (cash after: $-6,520.88) (limit: 0, actual: -6520.8802450561525)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.