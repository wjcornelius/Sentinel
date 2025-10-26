# -*- coding: utf-8 -*-
"""
Database operations for Sentinel.

Handles all SQLite database interactions for storing decisions,
trades, and system state.
"""

import logging
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

import config
from sentinel.utils.helpers import sanitize_conviction

DB_FILE = "sentinel.db"


def check_if_trades_executed_today() -> bool:
    """
    Check if trades have already been executed today to prevent duplicate runs.

    Queries the trades table for any entries from today with submitted/filled/failed status.
    Can be bypassed in dev mode via config.ALLOW_DEV_RERUNS.

    Returns:
        True if trades were already executed today, False otherwise
    """
    if getattr(config, "ALLOW_DEV_RERUNS", False):
        print("\n[DEV MODE] Bypassing single-run safeguard for today.")
        logging.warning("DEV MODE: Bypassing single-run safeguard")
        return False

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM trades
            WHERE DATE(timestamp) = DATE('now', 'localtime')
              AND status IN ('submitted', 'filled', 'execution_failed')
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()
        already_ran = result is not None
        logging.info(f"Checked for today's trades: already_ran={already_ran}")
        return already_ran
    except sqlite3.Error as e:
        logging.error(f"Database error checking for executed trades: {e}", exc_info=True)
        print(f"DB_ERROR checking for executed trades: {e}")
        return False


def get_prior_conviction(symbol: str) -> Optional[int]:
    """
    Retrieve the most recent conviction score for a symbol from the database.

    Args:
        symbol: Stock ticker symbol

    Returns:
        Prior conviction score (1-10), or None if no history exists
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT conviction_score
            FROM decisions
            WHERE symbol = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (symbol.upper(),))
        row = cursor.fetchone()
        conn.close()
        if row and row[0] is not None:
            return sanitize_conviction(row[0])
    except sqlite3.Error as e:
        logging.error(f"DB error fetching prior conviction for {symbol}: {e}")
        print(f"  - DB_ERROR fetching prior conviction for {symbol}: {e}")
    return None


def get_todays_decisions() -> List[Dict[str, Any]]:
    """
    Retrieve all AI decisions made for today.

    Used to check if a plan already exists before generating a new one.

    Returns:
        List of decision dictionaries with keys:
        - db_decision_id
        - symbol
        - decision
        - conviction_score
        - rationale
        - latest_price
        - market_context_summary
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, symbol, decision, conviction_score, rationale,
                   latest_price, market_context_summary
            FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        rows = cursor.fetchall()
        conn.close()

        decisions = []
        for row in rows:
            decisions.append({
                "db_decision_id": row["id"],
                "symbol": row["symbol"],
                "decision": row["decision"],
                "conviction_score": row["conviction_score"],
                "rationale": row["rationale"],
                "latest_price": row["latest_price"],
                "market_context_summary": row["market_context_summary"]
            })
        return decisions
    except sqlite3.Error as e:
        logging.error(f"DB error getting today's decisions: {e}", exc_info=True)
        print(f"DB_ERROR getting today's decisions: {e}")
        return []


def wipe_today_plan() -> bool:
    """
    Delete all decisions and trades from today (dev mode only).

    Used for testing to regenerate a fresh plan without waiting for tomorrow.

    Returns:
        True if successful, False otherwise
    """
    if not getattr(config, "ALLOW_DEV_RERUNS", False):
        return False

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        decisions_deleted = cursor.rowcount
        cursor.execute("""
            DELETE FROM trades
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        trades_deleted = cursor.rowcount
        conn.commit()
        conn.close()
        print(f"\n[DEV MODE] Cleared today's plan artifacts "
              f"(decisions deleted: {decisions_deleted}, trades deleted: {trades_deleted}).")
        logging.info(f"Wiped today's plan: {decisions_deleted} decisions, {trades_deleted} trades")
        return True
    except sqlite3.Error as e:
        logging.error(f"Failed to clear today's plan artifacts: {e}", exc_info=True)
        print(f"[DEV MODE] Failed to clear today's plan artifacts: {e}")
        return False


def log_decision_to_db(
    analysis: Dict[str, Any],
    latest_price: float,
    market_context: str
) -> Optional[int]:
    """
    Log an AI decision to the database.

    Args:
        analysis: Dictionary containing symbol, decision, conviction_score, rationale
        latest_price: Current stock price
        market_context: Market news summary

    Returns:
        Database row ID of inserted decision, or None if failed
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO decisions (
                timestamp,
                symbol,
                decision,
                conviction_score,
                rationale,
                latest_price,
                market_context_summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            analysis.get('symbol'),
            analysis.get('decision'),
            analysis.get('conviction_score'),
            analysis.get('rationale'),
            latest_price,
            market_context
        ))
        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logging.info(f"Logged decision for {analysis.get('symbol')} (ID: {decision_id})")
        print(f"    - Logged decision for {analysis.get('symbol')} (ID: {decision_id}).")
        return decision_id
    except sqlite3.Error as e:
        logging.error(f"Failed to log decision for {analysis.get('symbol')}: {e}", exc_info=True)
        print(f"    - DB_ERROR: Failed to log decision for {analysis.get('symbol')}: {e}")
        return None


def update_trade_log(trade_id: int, status: str, order_id: Optional[str] = None):
    """
    Update the status of a trade in the database.

    Args:
        trade_id: Database ID of the trade
        status: New status (e.g., 'submitted', 'filled', 'execution_failed')
        order_id: Optional Alpaca order ID
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE trades SET status = ?, alpaca_order_id = ? WHERE id = ?",
            (status, order_id, trade_id)
        )
        conn.commit()
        conn.close()
        logging.debug(f"Updated trade {trade_id} to status: {status}")
    except sqlite3.Error as e:
        logging.error(f"Failed to update trade log (ID {trade_id}): {e}", exc_info=True)
        print(f"  - DB_ERROR: Failed to update trade log (ID {trade_id}): {e}")
