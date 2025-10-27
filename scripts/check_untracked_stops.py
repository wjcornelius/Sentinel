# Quick script to check existing orders for positions without database stops

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi

api = tradeapi.REST(
    config.APCA_API_KEY_ID,
    config.APCA_API_SECRET_KEY,
    config.APCA_API_BASE_URL,
    api_version='v2'
)

symbols_to_check = ['GOOG', 'GOOGL', 'KLAC', 'MU', 'PEP', 'QCOM', 'WBD']

print("\n" + "=" * 70)
print("CHECKING EXISTING ORDERS FOR UNTRACKED POSITIONS")
print("=" * 70)

orders = api.list_orders(status='open', limit=500)
relevant_orders = [o for o in orders if o.symbol in symbols_to_check]

print(f"\nFound {len(relevant_orders)} open orders for these symbols:")

for order in relevant_orders:
    stop_price = order.stop_price if hasattr(order, 'stop_price') and order.stop_price else 'N/A'
    print(f"  {order.symbol}: {order.type} {order.side} {order.qty} shares @ ${stop_price}")

print("\n" + "=" * 70)
