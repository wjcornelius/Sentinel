"""
Create protective stop orders for all unprotected positions
Uses 8% stop loss (92% of current price)
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
print('CREATING PROTECTIVE STOPS FOR UNPROTECTED POSITIONS')
print('=' * 70)
print()

# Get all positions
positions = api.list_positions()
print(f'Total positions: {len(positions)}')

# Get all open stop orders
stop_orders = [o for o in api.list_orders(status='open') if o.type == 'stop']

# Create a map of stops by symbol
stops_by_symbol = {}
for order in stop_orders:
    if order.symbol not in stops_by_symbol:
        stops_by_symbol[order.symbol] = []
    stops_by_symbol[order.symbol].append(order)

# Find unprotected positions
unprotected = []
for pos in positions:
    symbol = pos.symbol
    qty = int(float(pos.qty))

    if qty == 0:
        continue  # Skip zero quantity positions

    if symbol in stops_by_symbol:
        stop_qty = sum(int(float(o.qty)) for o in stops_by_symbol[symbol])
        if stop_qty < qty:
            unprotected.append((symbol, qty, float(pos.current_price)))
    else:
        unprotected.append((symbol, qty, float(pos.current_price)))

print(f'Found {len(unprotected)} unprotected positions')
print()

if not unprotected:
    print('[OK] All positions already have stops!')
    sys.exit(0)

# Ask for confirmation
print('Will create 8% stop loss orders for:')
for symbol, qty, price in unprotected[:10]:
    stop_price = round(price * 0.92, 2)
    print(f'  {symbol}: {qty} shares @ ${price:.2f}, stop @ ${stop_price}')
if len(unprotected) > 10:
    print(f'  ... and {len(unprotected)-10} more')

print()
response = input(f'Create {len(unprotected)} stop orders? (yes/no): ')

if response.lower() != 'yes':
    print('Aborted.')
    sys.exit(0)

# Create stops
print()
print('Creating stops...')
success_count = 0
fail_count = 0

for symbol, qty, price in unprotected:
    stop_price = round(price * 0.92, 2)

    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='stop',
            stop_price=stop_price,
            time_in_force='gtc'
        )
        print(f'  [OK] {symbol}: stop @ ${stop_price} (order {order.id[:8]}...)')
        success_count += 1
    except Exception as e:
        print(f'  [FAIL] {symbol}: {e}')
        fail_count += 1

print()
print('=' * 70)
print(f'COMPLETE: {success_count} stops created, {fail_count} failed')
print('=' * 70)
