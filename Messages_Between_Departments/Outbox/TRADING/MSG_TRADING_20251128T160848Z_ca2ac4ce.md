---
from: TRADING
message_id: MSG_TRADING_20251128T160848Z_ca2ac4ce
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2025-11-28T16:08:48.482348Z'
to: EXECUTIVE
---

# ORDER REJECTED: GPN (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** GPN
- **Action:** BUY
- **Quantity:** 40

**Violations:**
- **min_position_pct:** Position would be 3.0% of portfolio (too small) (limit: 0.03, actual: 0.02996079296573409)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.