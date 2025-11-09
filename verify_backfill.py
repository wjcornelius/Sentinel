#!/usr/bin/env python3
"""Verify backfilled positions"""

import sqlite3

conn = sqlite3.connect('sentinel.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT ticker, status, actual_shares, actual_entry_price,
           intended_stop_loss, intended_target, total_risk, actual_entry_date
    FROM portfolio_positions
    WHERE status = 'OPEN' AND DATE(created_at) = DATE('now')
    ORDER BY ticker
""")

positions = cursor.fetchall()

print(f"\nOPEN Positions Created Today: {len(positions)}")
print("=" * 80)

for p in positions:
    ticker, status, shares, price, stop, target, risk, entry_date = p
    print(f"{ticker}: {shares:.0f} shares @ ${price:.2f}")
    print(f"  Stop: ${stop:.2f} | Target: ${target:.2f} | Risk: ${risk:.2f}")
    print(f"  Entry Date: {entry_date}")
    print()

conn.close()
