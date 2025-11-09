#!/usr/bin/env python3
"""Backfill positions that were submitted to Alpaca but not recorded in database"""

import sqlite3
from datetime import datetime
import uuid
from alpaca.trading.client import TradingClient
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

def main():
    # Connect to database
    conn = sqlite3.connect('sentinel.db', timeout=30.0)
    cursor = conn.cursor()

    # Get Alpaca positions
    client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    alpaca_positions = client.get_all_positions()
    alpaca_tickers = {pos.symbol: pos for pos in alpaca_positions}

    # Today's expected trades from the execution
    expected_buys = {
        'QCOM': {'shares': 74, 'order_id': '11170fcd-1521-488a-9db0-de9e2d72c75c'},
        'NVDA': {'shares': 37, 'order_id': 'a92de20c-7be0-46d2-91d1-393648771196'},
        'ACGL': {'shares': 101, 'order_id': 'f342c69b-65c5-40d7-8af7-3d99f01b845a'},
        'HST': {'shares': 432, 'order_id': '9cbae1c0-f25f-486f-a6aa-ab01226a7234'},
        'DVN': {'shares': 225, 'order_id': '6cc6134f-a20f-453c-b925-aa56d9db4087'},
    }

    print("\n" + "=" * 80)
    print("BACKFILLING POSITIONS FROM TODAY'S EXECUTION (Nov 6, 2025)")
    print("=" * 80)

    created_count = 0

    for ticker, info in expected_buys.items():
        # Check if position already exists
        cursor.execute(
            "SELECT position_id FROM portfolio_positions WHERE ticker = ? AND status = 'OPEN'",
            (ticker,)
        )
        existing = cursor.fetchone()

        if existing:
            print(f"  {ticker}: Already exists as OPEN, skipping")
            continue

        # Check if position exists in Alpaca
        if ticker not in alpaca_tickers:
            print(f"  {ticker}: NOT FOUND in Alpaca positions, skipping")
            continue

        alpaca_pos = alpaca_tickers[ticker]
        actual_shares = float(alpaca_pos.qty)
        actual_entry_price = float(alpaca_pos.avg_entry_price)

        # Create position entry
        position_id = f"POS_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        internal_order_id = f"ORD_20251106_080000_{uuid.uuid4().hex[:8]}"  # Approximate time

        # Calculate stop-loss and target (8% stop, 16% target)
        stop_loss = actual_entry_price * 0.92
        target = actual_entry_price * 1.16
        risk_per_share = actual_entry_price - stop_loss
        total_risk = risk_per_share * actual_shares

        cursor.execute("""
            INSERT INTO portfolio_positions (
                position_id,
                ticker,
                status,
                intended_entry_price,
                intended_shares,
                intended_stop_loss,
                intended_target,
                actual_entry_price,
                actual_shares,
                actual_entry_date,
                risk_per_share,
                total_risk,
                entry_order_message_id,
                created_at,
                updated_at
            ) VALUES (?, ?, 'OPEN', ?, ?, ?, ?, ?, ?, date('now'), ?, ?, ?, datetime('now'), datetime('now'))
        """, (
            position_id,
            ticker,
            actual_entry_price,  # Use actual as intended since we're backfilling
            actual_shares,
            stop_loss,
            target,
            actual_entry_price,
            actual_shares,
            risk_per_share,
            total_risk,
            internal_order_id
        ))

        print(f"  {ticker}: Created OPEN position - {actual_shares} shares @ ${actual_entry_price:.2f}")
        print(f"    Stop: ${stop_loss:.2f} | Target: ${target:.2f} | Risk: ${total_risk:.2f}")
        created_count += 1

    conn.commit()
    conn.close()

    print("=" * 80)
    print(f"Backfill complete: {created_count} positions created")
    print("=" * 80)

if __name__ == "__main__":
    main()
