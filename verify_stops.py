"""
Verify all positions have stop loss protection
"""
import alpaca_trade_api as tradeapi
import sys
from pathlib import Path

# Add sentinel directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import config
import config

api = tradeapi.REST(
    config.APCA_API_KEY_ID,
    config.APCA_API_SECRET_KEY,
    base_url=config.APCA_API_BASE_URL
)

print('=' * 70)
print('VERIFYING ALL POSITIONS HAVE STOP PROTECTION')
print('=' * 70)
print()

# Get all positions
positions = api.list_positions()
print(f'Total positions: {len(positions)}')

# Get all stop orders (open or new status)
all_orders = api.list_orders(status='all', limit=500)
stop_orders = [o for o in all_orders if o.type == 'stop' and o.status in ['open', 'new']]
print(f'Total active stop orders: {len(stop_orders)}')
print()

# Create a map of stops by symbol
stops_by_symbol = {}
for order in stop_orders:
    if order.symbol not in stops_by_symbol:
        stops_by_symbol[order.symbol] = []
    stops_by_symbol[order.symbol].append(order)

# Check each position
unprotected = []
protected_count = 0

for pos in positions:
    symbol = pos.symbol
    qty = int(float(pos.qty))

    if symbol in stops_by_symbol:
        stop_qty = sum(int(float(o.qty)) for o in stops_by_symbol[symbol])
        if stop_qty >= qty:
            protected_count += 1
        else:
            unprotected.append(f'{symbol}: {qty} shares but only {stop_qty} shares protected')
    else:
        unprotected.append(f'{symbol}: {qty} shares with NO STOP ORDER')

print(f'PROTECTED: {protected_count}/{len(positions)} positions have adequate stop coverage')

if unprotected:
    print()
    print(f'WARNING: {len(unprotected)} positions need attention:')
    print()
    for u in unprotected:
        print(f'  - {u}')
else:
    print()
    print('[OK] ALL POSITIONS ARE FULLY PROTECTED!')

print()
print('=' * 70)
