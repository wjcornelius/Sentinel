---
message_id: MSG_EXECUTIVE_20251031_REJECT001
from: EXECUTIVE
to: TRADING
timestamp: 2025-10-31T15:05:00Z
message_type: ExecutiveApproval
priority: routine
---

# Executive Approval: BUY NVDA 50 shares

## Decision

Approved trade proposal PROP_20251031_R003 after Risk and Portfolio review.

**Risk Score:** 5.2/10 (Moderate Risk)

**Rationale:** AI leader with strong momentum, but this is a POSITION LIMIT TEST. Approx $5700 shares x ~$140 = $19,600 (19.4% of portfolio - EXCEEDS 15% LIMIT).

## Order Details

Please execute the following trade:

```json
{
  "decision_id": "DEC_20251031_R003",
  "proposal_id": "PROP_20251031_R003",
  "ticker": "NVDA",
  "action": "BUY",
  "shares": 50,
  "order_type": "MARKET",
  "risk_score": 5.2,
  "approval_status": "APPROVED",
  "expected_value": 19600.00,
  "portfolio_impact": "19.4% position size",
  "approved_by": "EXECUTIVE",
  "approved_timestamp": "2025-10-31T15:05:00Z"
}
```

## Instructions

- Execute at market open or current market hours
- Report execution status to Portfolio and Compliance
- Flag any slippage >1%

## Note

This is a TEST for max_single_position_pct constraint (>15% should trigger auto-rejection).
