#!/usr/bin/env python3
"""Quick script to check current Alpaca positions"""

from alpaca.trading.client import TradingClient
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

def main():
    client = TradingClient(
        ALPACA_API_KEY,
        ALPACA_SECRET_KEY,
        paper=True
    )

    positions = client.get_all_positions()
    print(f"\nCurrent Alpaca Positions: {len(positions)}")
    print("=" * 80)

    if not positions:
        print("No positions found in Alpaca")
        return

    for p in sorted(positions, key=lambda x: x.symbol):
        print(f"{p.symbol}: {p.qty} shares @ ${float(p.avg_entry_price):.2f}")
        print(f"  Current: ${float(p.current_price):.2f}")
        print(f"  P/L: ${float(p.unrealized_pl):.2f} ({float(p.unrealized_plpc)*100:.2f}%)")
        print()

if __name__ == "__main__":
    main()
