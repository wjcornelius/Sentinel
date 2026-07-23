---
from: TRADING
message_id: MSG_TRADING_20260626T160721Z_aedbe1cd
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-06-26T16:07:21.260795Z'
to: EXECUTIVE
---

# ORDER REJECTED: EQT (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** EQT
- **Action:** BUY
- **Quantity:** 188

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $5,303.97 cash (4.8%), below 10% reserve (limit: 0.1, actual: 0.047523365569232714)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.