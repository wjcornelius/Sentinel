---
from: TRADING
message_id: MSG_TRADING_20260602T160835Z_0f5ffcaa
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-06-02T16:08:35.397807Z'
to: EXECUTIVE
---

# ORDER REJECTED: DG (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** DG
- **Action:** BUY
- **Quantity:** 61

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $9,759.27 cash (8.6%), below 10% reserve (limit: 0.1, actual: 0.08591398747955756)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.