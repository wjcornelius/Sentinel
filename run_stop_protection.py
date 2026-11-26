#!/usr/bin/env python
"""
run_stop_protection.py — the daily job the two-stage stop design always assumed.

Added 2026-08-10.

WHY THIS EXISTS
Departments/Trading/trading_department.py describes a deliberate two-stage stop,
specified 2026-07-22:

    "For the first 5 trading days after entry, park the stop at the 15% ceiling
     to give the swing thesis room to develop. A daily job (trailing_stop_monitor)
     swaps the stop to the tighter target_trail_percent on day 6."

That daily job was never scheduled. Neither stage ever ran. On 2026-08-10 the
account held ten positions and the measured protection rate was 0.0% — across
2,129 orders in nine months, Sentinel had never submitted a single stop order of
any kind. Every position it has ever held has been naked.

The cost, from 225 reconstructed round trips:
  * median give-back from peak 6.89%
  * trades that reached +16.49% closed at +7.27%
  * 15 losses — 19% of measured trades — were once up 5% or more
  * a 10% stop would have cut ZERO winners and saved $2,723 on the measured
    third of the book, against a nine-month total profit of $1,012

TWO PASSES, EVERY DAY
  1. protect_all_positions  — any position without a stop gets one, sized from
     its own ATR (8%-14% in practice, by volatility).
  2. tighten_stops_after_delay(5) — positions past day five step down from the
     wide entry stop to their ATR target.

Safe: adding a protective stop can only reduce loss. It never opens a position,
never increases size, and never sells anything at market. Runs against whatever
account config.py points at — paper today.

USAGE
  python run_stop_protection.py            # do it
  python run_stop_protection.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / f"stop_protection_{datetime.now():%Y-%m-%d}.log",
            encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("StopProtection")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    from Utils.trailing_stop_monitor import TrailingStopMonitor

    monitor = TrailingStopMonitor()

    before = monitor.check_protection_status()
    logger.info("Protection before: %.0f%% (%d protected, %d naked)",
                before.get("protection_rate", 0),
                len(before.get("protected", [])),
                len(before.get("unprotected", [])))
    if before.get("unprotected"):
        logger.info("  Naked: %s", ", ".join(before["unprotected"]))

    # Pass 1 — cover anything with no stop at all.
    added = monitor.protect_all_positions(dry_run=args.dry_run)
    for f in added.get("failed", []):
        # Worth surfacing rather than swallowing: an asset that cannot take a
        # stop order is usually halted or delisted, which is a position problem
        # in its own right, not just a protection gap.
        logger.warning("Could not protect %s: %s", f.get("ticker"), f.get("error"))

    # Pass 2 — step the five-day-old entry stops down to their ATR target.
    tightened = monitor.tighten_stops_after_delay(delay_days=5,
                                                  dry_run=args.dry_run)
    for t in tightened.get("tightened", []):
        logger.info("Tightened %s -> %s%%", t.get("ticker"),
                    t.get("new_trail_percent", t.get("target_pct")))

    after = monitor.check_protection_status()
    logger.info("Protection after: %.0f%% (%d protected, %d naked)",
                after.get("protection_rate", 0),
                len(after.get("protected", [])),
                len(after.get("unprotected", [])))

    # Record it where a performance analysis can find it later, alongside the
    # other daily audit rows.
    try:
        import sqlite3
        conn = sqlite3.connect(PROJECT_ROOT / "sentinel.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stop_protection_log (
                run_date         TEXT PRIMARY KEY,
                protection_rate  REAL,
                positions_total  INTEGER,
                newly_protected  INTEGER,
                tightened        INTEGER,
                failures         TEXT,
                recorded_at      TEXT
            )""")
        conn.execute(
            "INSERT OR REPLACE INTO stop_protection_log VALUES (?,?,?,?,?,?,?)",
            (datetime.now().strftime("%Y-%m-%d"),
             after.get("protection_rate"),
             after.get("total_positions"),
             len(added.get("protected", [])),
             len(tightened.get("tightened", [])),
             json.dumps(added.get("failed", []), default=str)[:2000],
             datetime.now(timezone.utc).isoformat(timespec="seconds")))
        conn.commit()
        conn.close()
    except Exception as exc:
        logger.warning("Could not log protection run: %s", exc)

    # Separate genuinely-naked positions from ones that simply cannot take an
    # order. IPG is INACTIVE at Alpaca after the Omnicom merger, so it will be
    # reported unprotected every morning forever — and a warning that fires
    # every day is a warning nobody reads on the day it matters.
    naked = list(after.get("unprotected", []))
    frozen = []
    try:
        from Utils.tradability import is_tradable
        frozen = [t for t in naked if not is_tradable(monitor.trading_client, t)]
        naked = [t for t in naked if t not in frozen]
    except Exception as exc:
        logger.debug("Tradability check unavailable: %s", exc)

    if frozen:
        logger.info("Untradeable, cannot be protected (expected): %s",
                    ", ".join(frozen))
    if naked:
        # 2026-11-25: with daily ranking sells off, the trailing stop is the
        # only exit, so a tradeable position still naked after this run has NO
        # exit at all. Say so loudly and make the scheduled task show a
        # non-zero result.
        logger.error("!" * 70)
        logger.error("STILL NAKED - NO EXIT FOR: %s", ", ".join(naked))
        logger.error("!" * 70)
        return 0 if args.dry_run else 2
    logger.info("Every tradeable position is protected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
