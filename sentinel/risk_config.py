# -*- coding: utf-8 -*-
# sentinel/risk_config.py
# Risk Management Configuration - Week 1 Implementation
# Stop-Loss Only Architecture for Paper Trading Phase

"""
Risk tolerance parameters confirmed by user:
- Max Drawdown: 18% (moderate-aggressive)
- Target Annual Return: 25% (2.5× market average)
- Sharpe Floor: 0.9 (pause system if below this)
"""

# ============================================================================
# STOP LOSS PARAMETERS
# ============================================================================

# Initial stop loss distance from entry price
INITIAL_STOP_LOSS_PCT = 0.92  # -8% stop loss
# Example: Entry at $100 → Stop at $92

# Stop loss as percentage points (for display/logging)
STOP_LOSS_DISTANCE = 8.0  # 8% below entry


# ============================================================================
# TRAILING STOP PARAMETERS
# ============================================================================

# Activate trailing stops when position reaches this gain
TRAILING_STOP_TRIGGER_PCT = 0.08  # Activate at +8% unrealized gain
# Example: Entry $100, current $108 → start trailing

# Minimum profit to lock in (conservative level)
TRAILING_STOP_LOCK_IN_PCT = 0.02  # Lock in at least +2%
# Example: Position at +10% → raise stop to $102 (entry was $100)

# Staircase levels for progressive profit protection
TRAILING_STOP_LEVELS = [
    # (min_gain_pct, lock_in_pct, stop_type_label)
    (0.08, 0.02, 'trailing_conservative'),   # +8% gain → lock in +2%
    (0.15, 0.08, 'trailing_moderate'),       # +15% gain → lock in +8%
    (0.25, 0.15, 'trailing_aggressive'),     # +25% gain → lock in +15%
]


# ============================================================================
# PROFIT TAKING PARAMETERS
# ============================================================================

# Hard profit target (triggers market sell during evening review)
PROFIT_TARGET_PCT = 0.16  # Take profit at +16% gain
# Example: Entry $100, current $116 → flag for profit taking

# Require manual approval before submitting profit-taking sell orders
REQUIRE_MANUAL_APPROVAL_FOR_PROFIT_TAKING = True


# ============================================================================
# POSITION SIZING (PAPER TRADING)
# ============================================================================

# Dollar amount per position during paper trading phase
PAPER_TRADING_POSITION_SIZE = 750  # $750 per stock
# Rationale: $10K account / 13-14 initial positions ≈ $750 each
# Allows building to 60-80 positions over 2-3 weeks

# Maximum position size as percentage of portfolio
MAX_POSITION_SIZE_PCT = 0.10  # 10% max per stock

# Target invested ratio (amount of capital to keep deployed)
TARGET_INVESTED_RATIO = 0.875  # 87.5% invested, 12.5% cash buffer


# ============================================================================
# RISK LIMITS (USER-CONFIRMED)
# ============================================================================

# Maximum acceptable portfolio drawdown before system pause
MAX_DRAWDOWN_LIMIT = 0.18  # 18% (moderate-aggressive risk tolerance)

# Target annual return
TARGET_ANNUAL_RETURN = 0.25  # 25% (2.5× market average)

# Minimum Sharpe ratio before system pause and investigation
SHARPE_RATIO_FLOOR = 0.9  # Below this, pause and investigate

# Maximum consecutive losing trades before investigation
MAX_CONSECUTIVE_LOSSES = 8


# ============================================================================
# ORDER EXECUTION PARAMETERS
# ============================================================================

# Maximum retries for API calls
MAX_API_RETRIES = 3

# Exponential backoff delays (seconds)
API_RETRY_DELAYS = [1, 2, 4]  # 1s, 2s, 4s

# Timeout for API calls (seconds)
API_CALL_TIMEOUT = 30

# Grace period before canceling orphaned stops (minutes)
ORPHANED_STOP_GRACE_PERIOD = 5  # Allow 5 minutes for settlement


# ============================================================================
# EVENING WORKFLOW TIMING
# ============================================================================

# Preferred start time for evening workflow (24-hour format)
EVENING_WORKFLOW_START_TIME = "19:00"  # 7:00 PM local time

# Maximum runtime for evening workflow before timeout (minutes)
EVENING_WORKFLOW_TIMEOUT = 30  # Must complete in 30 minutes

# Workflow steps (for progress tracking)
EVENING_WORKFLOW_STEPS = [
    "reconcile_fills",
    "update_trailing_stops",
    "check_profit_taking",
    "cleanup_orphaned_stops",
    "run_conviction_analysis",
    "submit_new_entries",
    "generate_summary_report"
]


# ============================================================================
# NOTIFICATION PREFERENCES
# ============================================================================

# Email notifications
SEND_EMAIL_ON_FILLS = True
SEND_EMAIL_ON_STOP_TRIGGERS = True
SEND_EMAIL_ON_PROFIT_TARGETS = True
SEND_DAILY_SUMMARY_EMAIL = True
SEND_EMAIL_ON_ERRORS = True       # Email on system errors

# SMS notifications (high priority only)
SEND_SMS_ON_STOP_TRIGGERS = True  # Stop losses are critical
SEND_SMS_ON_ERRORS = True         # System errors need immediate attention


# ============================================================================
# DATABASE MIGRATION SETTINGS
# ============================================================================

# Archive v7 data for historical analysis
ARCHIVE_V7_DATA = True

# Database file paths
DB_FILE = "sentinel.db"
ARCHIVED_DB_SUFFIX = "_archived_v7"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_stop_price(entry_price: float) -> float:
    """Calculate stop loss price from entry price."""
    return round(entry_price * INITIAL_STOP_LOSS_PCT, 2)


def calculate_trailing_stop_price(entry_price: float, current_unrealized_pnl_pct: float) -> float:
    """
    Calculate trailing stop price based on current gain.

    Uses staircase approach: higher gains = more protection.
    """
    # Find applicable staircase level
    for min_gain, lock_in, stop_type in reversed(TRAILING_STOP_LEVELS):
        if current_unrealized_pnl_pct >= min_gain:
            return round(entry_price * (1 + lock_in), 2)

    # Below minimum trailing threshold, use initial stop
    return calculate_stop_price(entry_price)


def get_stop_type_label(entry_price: float, current_unrealized_pnl_pct: float) -> str:
    """Get descriptive label for stop type based on gain level."""
    for min_gain, _, stop_type in reversed(TRAILING_STOP_LEVELS):
        if current_unrealized_pnl_pct >= min_gain:
            return stop_type
    return 'initial_stop'


def should_take_profit(current_unrealized_pnl_pct: float) -> bool:
    """Check if position has hit profit target."""
    return current_unrealized_pnl_pct >= PROFIT_TARGET_PCT


def calculate_position_quantity(stock_price: float, position_size_dollars: float = None) -> int:
    """
    Calculate share quantity for position based on dollar size.

    Args:
        stock_price: Current price per share
        position_size_dollars: Target position size (defaults to PAPER_TRADING_POSITION_SIZE)

    Returns:
        Integer number of shares to buy
    """
    if position_size_dollars is None:
        position_size_dollars = PAPER_TRADING_POSITION_SIZE

    qty = int(position_size_dollars / stock_price)
    return max(1, qty)  # Minimum 1 share


# ============================================================================
# VALIDATION
# ============================================================================

def validate_risk_config():
    """Validate risk configuration parameters."""
    errors = []

    # Stop loss validation
    if not (0.80 <= INITIAL_STOP_LOSS_PCT <= 0.98):
        errors.append(f"INITIAL_STOP_LOSS_PCT ({INITIAL_STOP_LOSS_PCT}) must be between 0.80 and 0.98")

    # Trailing stop validation
    if TRAILING_STOP_TRIGGER_PCT <= 0:
        errors.append(f"TRAILING_STOP_TRIGGER_PCT ({TRAILING_STOP_TRIGGER_PCT}) must be positive")

    if TRAILING_STOP_LOCK_IN_PCT < 0:
        errors.append(f"TRAILING_STOP_LOCK_IN_PCT ({TRAILING_STOP_LOCK_IN_PCT}) must be non-negative")

    # Profit target validation
    if PROFIT_TARGET_PCT <= TRAILING_STOP_TRIGGER_PCT:
        errors.append(f"PROFIT_TARGET_PCT ({PROFIT_TARGET_PCT}) should be greater than TRAILING_STOP_TRIGGER_PCT ({TRAILING_STOP_TRIGGER_PCT})")

    # Risk limits validation
    if not (0.05 <= MAX_DRAWDOWN_LIMIT <= 0.30):
        errors.append(f"MAX_DRAWDOWN_LIMIT ({MAX_DRAWDOWN_LIMIT}) should be between 5% and 30%")

    if TARGET_ANNUAL_RETURN <= 0:
        errors.append(f"TARGET_ANNUAL_RETURN ({TARGET_ANNUAL_RETURN}) must be positive")

    if SHARPE_RATIO_FLOOR < 0:
        errors.append(f"SHARPE_RATIO_FLOOR ({SHARPE_RATIO_FLOOR}) must be non-negative")

    # Position sizing validation
    if PAPER_TRADING_POSITION_SIZE <= 0:
        errors.append(f"PAPER_TRADING_POSITION_SIZE ({PAPER_TRADING_POSITION_SIZE}) must be positive")

    if not (0.50 <= TARGET_INVESTED_RATIO <= 0.95):
        errors.append(f"TARGET_INVESTED_RATIO ({TARGET_INVESTED_RATIO}) should be between 50% and 95%")

    if errors:
        raise ValueError("Risk configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    return True


# Run validation on import
validate_risk_config()
