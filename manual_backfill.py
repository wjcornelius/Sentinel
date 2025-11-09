#!/usr/bin/env python3
"""Manual backfill with retry logic"""

import sqlite3
import time
from datetime import datetime

def backfill_with_retry(max_retries=10):
    """Backfill positions with retry logic for database locks"""

    # Position data from Alpaca
    positions = [
        {'ticker': 'QCOM', 'shares': 74, 'price': 172.30},
        {'ticker': 'NVDA', 'shares': 37, 'price': 190.75},
        {'ticker': 'ACGL', 'shares': 101, 'price': 88.62},
        {'ticker': 'HST', 'shares': 432, 'price': 17.11},
        {'ticker': 'DVN', 'shares': 225, 'price': 32.61},
    ]

    print("\n" + "=" * 80)
    print("MANUAL BACKFILL WITH RETRY LOGIC")
    print("=" * 80)

    for pos in positions:
        ticker = pos['ticker']
        shares = pos['shares']
        price = pos['price']

        # Calculate stop/target
        stop = round(price * 0.92, 2)
        target = round(price * 1.16, 2)
        risk_per_share = round(price - stop, 2)
        total_risk = round(risk_per_share * shares, 2)

        # Generate IDs
        position_id = f"POS_20251106_080000_{ticker}"
        order_id = f"ORD_20251106_080000_{ticker}"

        # Try to insert with retries
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect('sentinel.db', timeout=60.0)
                cursor = conn.cursor()

                # Check if already exists
                cursor.execute(
                    "SELECT position_id FROM portfolio_positions WHERE ticker = ? AND status = 'OPEN'",
                    (ticker,)
                )
                if cursor.fetchone():
                    print(f"  {ticker}: Already exists, skipping")
                    conn.close()
                    break

                # Insert
                cursor.execute("""
                    INSERT INTO portfolio_positions (
                        position_id, ticker, status,
                        intended_entry_price, intended_shares,
                        intended_stop_loss, intended_target,
                        actual_entry_price, actual_shares, actual_entry_date,
                        risk_per_share, total_risk,
                        entry_order_message_id,
                        created_at, updated_at
                    ) VALUES (?, ?, 'OPEN', ?, ?, ?, ?, ?, ?, date('now'), ?, ?, ?, datetime('now'), datetime('now'))
                """, (
                    position_id, ticker, price, shares, stop, target,
                    price, shares, risk_per_share, total_risk, order_id
                ))

                conn.commit()
                conn.close()

                print(f"  {ticker}: OK Created ({shares} shares @ ${price:.2f}, risk: ${total_risk:.2f})")
                break

            except sqlite3.OperationalError as e:
                if 'locked' in str(e) and attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"  {ticker}: Database locked, retry {attempt+1}/{max_retries} in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"  {ticker}: FAILED after {attempt+1} attempts: {e}")
                    break
            except Exception as e:
                print(f"  {ticker}: ERROR: {e}")
                break

    print("=" * 80)
    print("Backfill complete")
    print("=" * 80)

if __name__ == "__main__":
    backfill_with_retry()
