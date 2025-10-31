---
from: PORTFOLIO
message_id: MSG_PORTFOLIO_20251031T104144Z_d98caeca
message_type: TradeOrder
parent_message_id: POS_20251031_MA_d4596cb7
priority: urgent
requires_response: true
timestamp: '2025-10-31T10:41:44.323608Z'
to: TRADING
---

# Trade Order - SELL MA

**Order Type**: SELL
**Position ID**: POS_20251031_MA_d4596cb7
**Exit Reason**: TARGET

## Order Details
- **Ticker**: MA
- **Shares**: 75 (close full position)
- **Order Type**: MARKET
- **Current Price**: $553.68

## Exit Signal
- **Reason**: TARGET
- **Details**: Price $553.68 hit target $160.00. Taking profit at target price.

## Performance
- **Entry**: $150.50
- **Exit**: $553.68 (estimated)
- **Gain**: $403.18/share × 75 = $30238.50
- **Return**: +267.89%
- **Days Held**: 0

```json
{
  "order_type": "SELL",
  "ticker": "MA",
  "shares": 75,
  "execution_type": "MARKET",
  "position_id": "POS_20251031_MA_d4596cb7",
  "exit_reason": "TARGET",
  "exit_price": 553.6799926757812,
  "timeout_seconds": 60
}
```
