# -*- coding: utf-8 -*-
# scripts/import_legacy_stops.py
# Import existing stop orders from Alpaca into database

"""
Import existing stop orders from Alpaca into v8 database.
Useful for tracking legacy positions from pre-v8 migration.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import alpaca_trade_api as tradeapi


def main():
    """Import existing stop orders from Alpaca into database."""

    print("\n" + "=" * 70)
    print("IMPORT LEGACY STOP ORDERS")
    print("=" * 70)

    # Connect to Alpaca
    api = tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

    # Get all open stop orders
    orders = api.list_orders(status='open', limit=500)
    stop_orders = [o for o in orders if o.type == 'stop' and o.side == 'sell']

    print(f"\nFound {len(stop_orders)} open stop orders on Alpaca")

    # Connect to database
    conn = sqlite3.connect('sentinel.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    imported = 0
    skipped = 0

    for order in stop_orders:
        # Check if already in database
        existing = cursor.execute(
            "SELECT id FROM stop_loss_orders WHERE order_id = ?",
            (order.id,)
        ).fetchone()

        if existing:
            skipped += 1
            continue

        # Import as legacy stop (entry_order_id = -1, stop_type = 'initial')
        try:
            # Convert Alpaca Timestamp to ISO format string
            submitted_at = order.submitted_at.isoformat() if hasattr(order.submitted_at, 'isoformat') else str(order.submitted_at)

            cursor.execute("""
                INSERT INTO stop_loss_orders (
                    entry_order_id, symbol, order_id, client_order_id,
                    qty, stop_price, stop_type, time_in_force, status, submitted_at
                ) VALUES (
                    -1, ?, ?, ?, ?, ?, 'initial', ?, 'active', ?
                )
            """, (
                order.symbol,
                order.id,
                order.client_order_id,
                int(float(order.qty)),
                float(order.stop_price),
                order.time_in_force,
                submitted_at
            ))

            imported += 1
            print(f"  [IMPORTED] {order.symbol}: {order.qty} shares @ ${order.stop_price}")

        except Exception as e:
            print(f"  [ERROR] Failed to import {order.symbol}: {e}")

    conn.commit()
    conn.close()

    print("\n" + "=" * 70)
    print(f"IMPORT COMPLETE: {imported} imported, {skipped} already tracked")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
