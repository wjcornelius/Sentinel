---
from: TRADING
message_id: MSG_TRADING_20260401T160708Z_f8cedf1b
message_type: escalation
priority: elevated
requires_response: false
timestamp: '2026-04-01T16:07:08.543573Z'
to: EXECUTIVE
---

# ORDER REJECTED: CDE (Hard Constraint Violations)

## Hard Constraint Violations

Order was automatically rejected due to hard constraint violations:

**Order Details:**
- **Ticker:** CDE
- **Action:** BUY
- **Quantity:** 498

**Violations:**
- **min_cash_reserve_pct:** Order would leave only $211.13 cash (0.2%), below 10% reserve (limit: 0.1, actual: 0.0020531631652019214)

**Action Required:** Review portfolio allocation or adjust constraints in hard_constraints.yaml.