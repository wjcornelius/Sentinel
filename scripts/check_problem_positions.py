# Quick script to check P&L for problem positions

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
print("CHECKING P&L FOR PROBLEM POSITIONS")
print("=" * 70)

positions = api.list_positions()

for pos in positions:
    if pos.symbol in symbols_to_check:
        entry_price = float(pos.avg_entry_price)
        current_price = float(pos.current_price)
        pnl_pct = (current_price - entry_price) / entry_price

        print(f"{pos.symbol}: Entry=${entry_price:.2f}, Current=${current_price:.2f}, P&L={pnl_pct:+.1%}")

print("\n" + "=" * 70)
