# Compare order IDs in database vs Alpaca

import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi

# Get stops from Alpaca
api = tradeapi.REST(
    config.APCA_API_KEY_ID,
    config.APCA_API_SECRET_KEY,
    config.APCA_API_BASE_URL,
    api_version='v2'
)

alpaca_stops = {
    o.symbol: o.id
    for o in api.list_orders(status='open', limit=500)
    if o.type == 'stop' and o.side == 'sell'
}

# Get stops from database
conn = sqlite3.connect('sentinel.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

db_stops = {
    row['symbol']: row['order_id']
    for row in cursor.execute("""
        SELECT symbol, order_id
        FROM stop_loss_orders
        WHERE status = 'active'
          AND entry_order_id = -1
    """).fetchall()
}

print("\n" + "=" * 70)
print("ORDER ID COMPARISON (Legacy Stops)")
print("=" * 70)

for symbol in sorted(set(alpaca_stops.keys()) | set(db_stops.keys())):
    alpaca_id = alpaca_stops.get(symbol, 'MISSING')
    db_id = db_stops.get(symbol, 'MISSING')
    match = "✓" if alpaca_id == db_id else "✗"

    print(f"\n{symbol}:")
    print(f"  Alpaca: {alpaca_id}")
    print(f"  DB:     {db_id}")
    print(f"  Match:  {match}")

print("\n" + "=" * 70)
