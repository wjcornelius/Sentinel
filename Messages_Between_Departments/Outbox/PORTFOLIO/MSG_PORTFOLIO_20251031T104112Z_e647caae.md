---
from: PORTFOLIO
message_id: MSG_PORTFOLIO_20251031T104112Z_e647caae
message_type: TradeOrder
parent_message_id: POS_20251031_BAC_3b3bbc09
priority: urgent
requires_response: true
timestamp: '2025-10-31T10:41:12.990082Z'
to: TRADING
---

# Trade Order - SELL BAC

**Order Type**: SELL
**Position ID**: POS_20251031_BAC_3b3bbc09
**Exit Reason**: STOP_LOSS

## Order Details
- **Ticker**: BAC
- **Shares**: 95 (close full position)
- **Order Type**: MARKET
- **Current Price**: $53.03

## Exit Signal
- **Reason**: STOP_LOSS
- **Details**: Price $53.03 hit stop-loss $100.00. Protecting capital - closing position to limit loss.

## Performance
- **Entry**: $110.50
- **Exit**: $53.03 (estimated)
- **Gain**: $-57.47/share × 95 = $-5459.65
- **Return**: -52.01%
- **Days Held**: 0

```json
{
  "order_type": "SELL",
  "ticker": "BAC",
  "shares": 95,
  "execution_type": "MARKET",
  "position_id": "POS_20251031_BAC_3b3bbc09",
  "exit_reason": "STOP_LOSS",
  "exit_price": 53.029998779296875,
  "timeout_seconds": 60
}
```
