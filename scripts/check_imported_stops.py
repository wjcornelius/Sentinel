# Check imported stop details

import sys
import sqlite3
from pathlib import Path

conn = sqlite3.connect('sentinel.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "=" * 70)
print("IMPORTED STOP DETAILS")
print("=" * 70)

rows = cursor.execute("""
    SELECT symbol, qty, stop_price, stop_type
    FROM stop_loss_orders
    WHERE entry_order_id = -1
    ORDER BY symbol
""").fetchall()

for row in rows:
    print(f"{row['symbol']}: {row['qty']} shares @ ${row['stop_price']} ({row['stop_type']})")

print("\n" + "=" * 70)
