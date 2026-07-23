"""
One-shot: backfill Sentinel's shared closed_trades table from historical
trading_fills + trading_orders using FIFO reconstruction.

Added 2026-07-22. Reason: the canonical closed_trades table is empty because
the shared ClosedTradesTable wiring was added the same day. Reconstruct
history from trading_fills so the review harness has a real time series to
compute win-rate / hold-period / MAE from day 1.

Method:
  1. Join trading_fills -> trading_orders to get BUY/SELL rows with prices.
  2. Sort per ticker by fill_timestamp.
  3. FIFO-match SELL fills against open BUY lots.
  4. Compute realized P&L per round-trip, emit one row per SELL to
     closed_trades via the shared library.
  5. Best-effort exit_reason inference — if the SELL order came from a
     stop_order_id linkage or the order note mentions 'stop', tag it
     'trailing_stop'; otherwise 'strategy_exit'.
"""

from __future__ import annotations

import sqlite3
import sys
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

# Shared library
sys.path.insert(0, r'C:\Users\wjcor\OneDrive\Desktop\_shared_trading_lib')
from closed_trades import ClosedTradesTable

PROJECT_ROOT = Path(__file__).parent
SENTINEL_DB = PROJECT_ROOT / "sentinel.db"
OUT_DB = PROJECT_ROOT / "Departments" / "Trading" / "data" / "closed_trades.db"


def load_fills_with_orders() -> List[Dict]:
    """Return every fill joined against its parent order, sorted by ticker/ts."""
    conn = sqlite3.connect(str(SENTINEL_DB))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT
                f.id            AS fill_id,
                f.order_id      AS order_pk,
                f.fill_price    AS price,
                f.quantity_filled AS qty,
                f.fill_timestamp AS ts,
                f.alpaca_fill_id AS alpaca_fill_id,
                o.order_id      AS order_id,
                o.alpaca_order_id AS alpaca_order_id,
                o.ticker        AS ticker,
                o.action        AS action,
                o.status        AS status
            FROM trading_fills f
            JOIN trading_orders o ON f.order_id = o.id
            WHERE f.fill_price IS NOT NULL
              AND f.quantity_filled IS NOT NULL
              AND o.ticker IS NOT NULL
              AND o.action IS NOT NULL
            ORDER BY o.ticker, f.fill_timestamp, f.id
            """
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def load_sector_map() -> Dict[str, str]:
    """Prefer the populated Config/ticker_sectors.json, else return {}."""
    import json
    path = PROJECT_ROOT / "Config" / "ticker_sectors.json"
    if not path.exists():
        return {}
    try:
        return (json.loads(path.read_text(encoding="utf-8")) or {}).get("sectors", {}) or {}
    except Exception:
        return {}


def infer_exit_reason(order_row: Dict) -> str:
    """Best-effort exit reason."""
    status = (order_row.get("status") or "").upper()
    if "STOP" in status or "TRAIL" in status:
        return "trailing_stop"
    return "strategy_exit"


def backfill() -> Tuple[int, int, int]:
    fills = load_fills_with_orders()
    print(f"Loaded {len(fills)} fills across {len({f['ticker'] for f in fills})} tickers")

    sector_map = load_sector_map()
    if sector_map:
        print(f"  Loaded sector map ({len(sector_map)} tickers) — populate_ticker_sectors.py output")
    else:
        print("  No Config/ticker_sectors.json yet — sectors will be 'Unknown'")

    table = ClosedTradesTable(db_path=OUT_DB, bot_name="Sentinel")

    # FIFO queue of open BUY lots per ticker: deque of dicts with qty/price/ts/order_id
    open_lots: Dict[str, deque] = defaultdict(deque)

    round_trips = 0
    skipped_no_lot = 0
    already = 0

    for f in fills:
        ticker = f["ticker"]
        action = f["action"].upper()
        qty = int(f["qty"] or 0)
        price = float(f["price"] or 0)
        ts = f["ts"] or datetime.now(timezone.utc).isoformat()
        alpaca_id = f["alpaca_fill_id"] or f["alpaca_order_id"] or f["order_id"]

        if qty <= 0 or price <= 0:
            continue

        if action == "BUY":
            open_lots[ticker].append({
                "qty": qty,
                "price": price,
                "ts": ts,
                "alpaca_entry_order_id": f["alpaca_order_id"] or f["order_id"],
            })
            continue

        if action != "SELL":
            continue

        # FIFO-match against open lots
        remaining = qty
        while remaining > 0 and open_lots[ticker]:
            lot = open_lots[ticker][0]
            take = min(lot["qty"], remaining)
            try:
                row_id = table.record_close(
                    strategy="SentinelDept",
                    ticker=ticker,
                    entry_ts=lot["ts"],
                    exit_ts=ts,
                    entry_price=lot["price"],
                    exit_price=price,
                    qty=take,
                    exit_reason=infer_exit_reason(f),
                    sector=sector_map.get(ticker, "Unknown"),
                    alpaca_entry_order_id=str(lot.get("alpaca_entry_order_id") or ""),
                    # Ensure UNIQUE per split-lot by combining exit id with lot qty
                    alpaca_exit_order_id=f"{alpaca_id}::lot={take}::ts={lot['ts']}",
                )
                if row_id:
                    round_trips += 1
                else:
                    already += 1
            except Exception as e:
                print(f"  record_close failed for {ticker}: {e}")

            lot["qty"] -= take
            remaining -= take
            if lot["qty"] <= 0:
                open_lots[ticker].popleft()

        if remaining > 0:
            skipped_no_lot += remaining  # SELL without a matching BUY (short? bad data)

    return round_trips, already, skipped_no_lot


def main() -> int:
    print("Sentinel closed_trades backfill")
    print(f"  Source: {SENTINEL_DB}")
    print(f"  Target: {OUT_DB}")
    print()

    OUT_DB.parent.mkdir(parents=True, exist_ok=True)

    round_trips, already, skipped = backfill()
    print()
    print(f"Backfill complete:")
    print(f"  Round trips recorded: {round_trips}")
    print(f"  Already-present (idempotent): {already}")
    print(f"  SELLs with no matching BUY lot: {skipped}")

    # Print a quick summary from the table
    table = ClosedTradesTable(db_path=OUT_DB, bot_name="Sentinel")
    summary = table.query_summary()
    print()
    print("Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
