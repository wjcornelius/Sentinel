---
from: TRADING
message_id: MSG_TRADING_20260409T160635Z_b5bfc3ad
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-09T16:06:35.758656Z'
to: EXECUTIVE
---

# ORDER REJECTED: BMRN (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** BMRN
- **Action:** BUY
- **Quantity:** 113

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $8,989.22 cash (8.7%), below 10% reserve (limit: 0.1, actual: 0.08730116159997982)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.