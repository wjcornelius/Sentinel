"""
Poe LLM Portfolio Optimizer (Sentinel)

Cheap-model reranking of the top-N candidates before the deterministic
equal-weight sizer runs. Wraps the shared PoeCheapClient (Claude Haiku 4.5
via Poe, ~40-80 points/day).

Design:
- Deterministic path is authoritative. If the LLM is unavailable, fails,
  or returns unparseable output, we log and fall back to the caller's
  top-N-by-score selection unchanged.
- LLM is prompted to re-order the candidate list and optionally drop tickers
  for sector-diversification reasons. It never invents tickers; anything it
  emits that isn't in the input candidate set is dropped.
- Full response text is appended to Departments/Operations/data/llm_decisions.jsonl
  for later review.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Shared library
sys.path.insert(0, r'C:\Users\wjcor\OneDrive\Desktop\_shared_trading_lib')
try:
    from poe_cheap_client import PoeCheapClient, is_available  # noqa: E402
    _POE_IMPORTED = True
except Exception:
    _POE_IMPORTED = False

logger = logging.getLogger("PoePortfolioOptimizer")


_DECISIONS_LOG = (
    Path(__file__).parent / "data" / "llm_decisions.jsonl"
)


def _log_decision(entry: Dict) -> None:
    try:
        _DECISIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(_DECISIONS_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.warning(f"could not append llm_decisions.jsonl: {e}")


SYSTEM_PROMPT = (
    "You are a portfolio manager. Given a ranked list of candidate positions "
    "with their composite scores, technical indicators, fundamentals, and "
    "sentiment, select the top N (specified) for equal-weight allocation. "
    "Prefer diversification across sectors. Explain each pick in one sentence."
)


def _format_candidates(candidates: List[Dict]) -> str:
    lines = []
    for i, c in enumerate(candidates, 1):
        lines.append(
            f"{i}. {c.get('ticker')} | composite={c.get('composite_score', 0):.1f} "
            f"| tech={c.get('technical_score', 0):.0f} "
            f"| fund={c.get('fundamental_score', 0):.0f} "
            f"| sent={c.get('sentiment_score', 50):.0f} "
            f"| sector={c.get('sector', 'Unknown')} "
            f"| price=${c.get('current_price', 0):.2f}"
        )
    return "\n".join(lines)


def _parse_response(text: str, candidate_tickers: set) -> List[str]:
    """
    Extract picked tickers from LLM response. Accepts either:
      - a JSON block   { "picks": ["AAPL", ...] }
      - or a plain-text list where the first token per line matches a ticker
    Only tickers present in the input set are kept, first occurrence wins.
    """
    picked: List[str] = []
    # Try JSON first
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            obj = json.loads(text[start:end + 1])
            for t in obj.get("picks", []):
                t = str(t).strip().upper()
                if t in candidate_tickers and t not in picked:
                    picked.append(t)
            if picked:
                return picked
    except Exception:
        pass

    # Fall back to line-based extraction
    for line in text.splitlines():
        stripped = line.strip().lstrip("-*0123456789.) ").strip()
        if not stripped:
            continue
        first = stripped.split()[0].strip("*,.:;()[]").upper()
        if first in candidate_tickers and first not in picked:
            picked.append(first)
    return picked


def optimize_with_llm(
    selected_candidates: List[Dict],
    target_n: int,
    cash_available: float,
    current_holdings: Optional[List[Dict]] = None,
    model: Optional[str] = None,
) -> Tuple[List[Dict], str, bool]:
    """
    Try to have the cheap Poe LLM refine the top-N candidate list.

    Returns:
        (reordered_candidates, reasoning, used_llm)
        If the LLM is unavailable or its output cannot be parsed,
        returns (selected_candidates, "deterministic-fallback", False).
    """
    if not _POE_IMPORTED or not is_available():
        return selected_candidates, "deterministic (Poe unavailable)", False

    if not selected_candidates:
        return selected_candidates, "deterministic (no candidates)", False

    candidate_tickers = {c.get("ticker") for c in selected_candidates if c.get("ticker")}
    holdings_text = "(none)"
    if current_holdings:
        holdings_text = ", ".join(sorted({h.get("ticker") for h in current_holdings if h.get("ticker")}))

    user = (
        f"Cash available for new positions: ${cash_available:,.0f}\n"
        f"Target position count: {target_n}\n"
        f"Current holdings (do NOT rebuy): {holdings_text}\n\n"
        f"Candidates (already ranked by composite score, highest first):\n"
        f"{_format_candidates(selected_candidates)}\n\n"
        f"Return the top {target_n} tickers to buy. "
        f"Prefer sector diversification (no more than 40% of picks in any single sector). "
        f"Respond with a JSON object like {{\"picks\": [\"AAPL\", ...], \"rationale\": {{\"AAPL\": \"one-sentence reason\", ...}}}}."
    )

    try:
        client = PoeCheapClient(model=model) if model else PoeCheapClient()
        response = client.chat(system=SYSTEM_PROMPT, user=user, max_tokens=800)
    except Exception as e:
        logger.warning(f"Poe LLM call failed: {e}")
        _log_decision({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "status": "error",
            "error": str(e),
            "candidate_tickers": sorted(candidate_tickers),
            "target_n": target_n,
        })
        return selected_candidates, f"deterministic (Poe error: {e})", False

    picks = _parse_response(response, candidate_tickers)

    _log_decision({
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "ok" if picks else "unparseable",
        "target_n": target_n,
        "cash_available": cash_available,
        "candidate_tickers": sorted(candidate_tickers),
        "llm_response": response,
        "picks": picks,
    })

    if not picks:
        logger.warning("Poe LLM response could not be parsed — falling back to deterministic")
        return selected_candidates, "deterministic (unparseable LLM response)", False

    # Reorder selected_candidates according to picks; append any candidate the
    # LLM did NOT pick at the end so the caller still gets a full ordered list.
    by_ticker = {c["ticker"]: c for c in selected_candidates if c.get("ticker")}
    reordered = [by_ticker[t] for t in picks if t in by_ticker]
    already = set(picks)
    for c in selected_candidates:
        if c.get("ticker") not in already:
            reordered.append(c)

    truncated = reordered[:target_n] if target_n and target_n > 0 else reordered
    reasoning = f"Poe LLM ({client.model}) picked {len(picks)} tickers, {len(truncated)} used"
    return truncated, reasoning, True
