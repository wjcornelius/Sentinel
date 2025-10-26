# -*- coding: utf-8 -*-
"""
UI Bridge Module - Communication between main_script.py and Dashboard

Handles:
- User approval (APPROVE/DENY buttons in UI)
- Safe abort checking
- Terminal output streaming
- Status updates
"""

import os
import time
import logging
from typing import Optional
import queue
import threading

# Global state (shared between dashboard and main script)
_ui_mode = os.getenv('SENTINEL_UI_MODE') == '1'
_abort_requested = False
_approval_response = None
_terminal_queue = queue.Queue()
_status_callbacks = []


def is_ui_mode() -> bool:
    """Check if running in UI mode (from dashboard)."""
    return _ui_mode


def set_ui_mode(enabled: bool):
    """Enable/disable UI mode."""
    global _ui_mode
    _ui_mode = enabled
    if enabled:
        logging.info("UI mode enabled - dashboard integration active")


def request_abort():
    """Request graceful abort of current run."""
    global _abort_requested
    _abort_requested = True
    logging.warning("Abort requested by user")
    send_terminal_output("\n[ABORT REQUESTED] Stopping safely after current operation...\n")


def is_abort_requested() -> bool:
    """Check if user requested abort."""
    return _abort_requested


def reset_abort():
    """Clear abort flag (called at start of new run)."""
    global _abort_requested
    _abort_requested = False


def set_approval_response(approved: bool):
    """Set user's approval decision from dashboard."""
    global _approval_response
    _approval_response = approved
    logging.info(f"User approval received: {'APPROVED' if approved else 'DENIED'}")


def wait_for_approval(plan_summary: dict) -> bool:
    """
    Wait for user approval from dashboard (or console if not in UI mode).

    Args:
        plan_summary: Dictionary with trade plan details

    Returns:
        True if approved, False if denied
    """
    global _approval_response

    if not is_ui_mode():
        # Console mode - traditional approval
        print("\n--- [Manual Approval Required] ---")
        print("Type 'APPROVE' to authorize this plan. Any other input cancels execution.")
        approval_input = input("Enter command: ")
        approved = approval_input.strip().upper() == 'APPROVE'
        logging.info(f"Console approval: {'APPROVED' if approved else 'DENIED'}")
        return approved

    # UI mode - wait for dashboard response
    _approval_response = None
    send_terminal_output("\n--- [Manual Approval Required] ---\n")
    send_terminal_output("Waiting for approval from dashboard...\n")
    send_status_update("waiting_approval", plan_summary)

    logging.info("Waiting for UI approval response...")

    # Wait up to 5 minutes for response
    timeout = 300  # 5 minutes
    start = time.time()

    while _approval_response is None:
        if time.time() - start > timeout:
            logging.error("Approval timeout - defaulting to DENY")
            send_terminal_output("\n[TIMEOUT] No response received - denying plan\n")
            return False

        if is_abort_requested():
            logging.info("Abort requested during approval wait")
            return False

        time.sleep(0.1)  # Check every 100ms

    approved = _approval_response
    _approval_response = None  # Reset for next time

    if approved:
        send_terminal_output("\n[APPROVED] Executing trade plan...\n")
    else:
        send_terminal_output("\n[DENIED] Trade plan rejected by user\n")

    return approved


def send_terminal_output(message: str):
    """Send terminal output to dashboard."""
    if is_ui_mode():
        _terminal_queue.put({'type': 'terminal', 'data': message})
    # Always print to console as well
    print(message, end='')


def send_status_update(status: str, data: dict = None):
    """Send status update to dashboard."""
    if is_ui_mode():
        _terminal_queue.put({
            'type': 'status',
            'status': status,
            'data': data or {}
        })


def get_terminal_messages():
    """Get all pending terminal messages (for dashboard)."""
    messages = []
    while not _terminal_queue.empty():
        try:
            messages.append(_terminal_queue.get_nowait())
        except queue.Empty:
            break
    return messages


def check_abort_safe_point(stage_name: str) -> bool:
    """
    Check for abort request at a safe point.

    Args:
        stage_name: Name of current stage (for logging)

    Returns:
        True if should abort, False if should continue

    Safe points:
    - After Stage 0 (Account review)
    - After Stage 1 (Universe generation)
    - Between stocks in Stage 2 (Data aggregation)
    - After Stage 3 (AI analysis)
    - Before Stage 5 (Trade execution)
    """
    if is_abort_requested():
        logging.info(f"Abort check at {stage_name}: ABORTING")
        send_terminal_output(f"\n[ABORTED] Stopped safely at {stage_name}\n")
        send_status_update("aborted", {"stage": stage_name})
        return True
    return False
