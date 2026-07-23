---
from: PORTFOLIO
message_id: MSG_PORTFOLIO_20251031T104144Z_b4d4dfc7
message_type: TradeOrder
parent_message_id: POS_20251031_C_5390a1b7
priority: urgent
requires_response: true
timestamp: '2025-10-31T10:41:44.320506Z'
to: TRADING
---

# Trade Order - SELL C

**Order Type**: SELL
**Position ID**: POS_20251031_C_5390a1b7
**Exit Reason**: STOP_LOSS

## Order Details
- **Ticker**: C
- **Shares**: 85 (close full position)
- **Order Type**: MARKET
- **Current Price**: $100.22

## Exit Signal
- **Reason**: STOP_LOSS
- **Details**: Price $100.22 hit stop-loss $120.00. Protecting capital - closing position to limit loss.

## Performance
- **Entry**: $130.50
- **Exit**: $100.22 (estimated)
- **Gain**: $-30.28/share × 85 = $-2573.80
- **Return**: -23.20%
- **Days Held**: 0

```json
{
  "order_type": "SELL",
  "ticker": "C",
  "shares": 85,
  "execution_type": "MARKET",
  "position_id": "POS_20251031_C_5390a1b7",
  "exit_reason": "STOP_LOSS",
  "exit_price": 100.22000122070312,
  "timeout_seconds": 60
}
```
