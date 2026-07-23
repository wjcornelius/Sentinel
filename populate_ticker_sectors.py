"""
One-shot: populate Config/ticker_sectors.json with the GICS sector for every
ticker in Sentinel's universe (ticker_universe.txt).

Added 2026-07-22. Reason: analysis showed 368 of 407 trades had sector="Unknown",
so the 40% sector-concentration hard constraint could not bind. Run once (or
whenever the universe file changes) and Research/Ops read the mapping at plan time.

yfinance sometimes has no `sector` field (ETFs, some ADRs, delisted). Those get
saved as "Unknown" — the downstream code already handles that string.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import yfinance as yf


PROJECT_ROOT = Path(__file__).parent
UNIVERSE = PROJECT_ROOT / "ticker_universe.txt"
OUTPUT = PROJECT_ROOT / "Config" / "ticker_sectors.json"


def load_universe() -> List[str]:
    tickers: List[str] = []
    for raw in UNIVERSE.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        # Some lines may have inline comments
        tk = raw.split()[0].split("#")[0].strip().upper()
        if tk and tk not in tickers:
            tickers.append(tk)
    return tickers


def fetch_sector(ticker: str) -> str:
    try:
        info = yf.Ticker(ticker).info or {}
        sector = info.get("sector") or ""
        sector = sector.strip() or "Unknown"
        return sector
    except Exception:
        return "Unknown"


def load_existing() -> Dict[str, str]:
    if OUTPUT.exists():
        try:
            data = json.loads(OUTPUT.read_text(encoding="utf-8"))
            return data.get("sectors", {})
        except Exception:
            return {}
    return {}


def main() -> int:
    tickers = load_universe()
    print(f"Loaded {len(tickers)} tickers from {UNIVERSE.name}")

    existing = load_existing()
    result: Dict[str, str] = dict(existing)

    # Only fetch tickers we haven't tagged yet (idempotent)
    to_fetch = [t for t in tickers if t not in result or result.get(t) == "Unknown"]
    print(f"Will fetch {len(to_fetch)} tickers (already have {len(tickers) - len(to_fetch)})")

    for i, ticker in enumerate(to_fetch, 1):
        sector = fetch_sector(ticker)
        result[ticker] = sector
        if i % 25 == 0 or i == len(to_fetch):
            print(f"  {i}/{len(to_fetch)}  {ticker} -> {sector}")
        # be gentle with yfinance
        time.sleep(0.1)

    unknown_count = sum(1 for v in result.values() if v == "Unknown")
    print(f"\nDone. {len(result)} total, {unknown_count} still Unknown.")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "universe_file": str(UNIVERSE.name),
        "sectors": result,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
