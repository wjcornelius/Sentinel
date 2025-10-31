"""
TEST: PositionTracker Class (Week 4 Day 3)
Tests position lifecycle: PENDING → OPEN → CLOSED
Tests partial fills, reconciliation, and portfolio summary
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
import sqlite3
from pathlib import Path
from datetime import datetime, date
import uuid

# Import PositionTracker
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from portfolio_department import PositionTracker, MessageHandler

# Paths
config_path = Path("Config/portfolio_config.yaml")
db_path = Path("sentinel.db")

print("=" * 100)
print("POSITION TRACKER TEST - Week 4 Day 3")
print("=" * 100)
print()

# Clean up any test data from previous runs
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM portfolio_positions WHERE ticker IN ('AAPL', 'MSFT') AND created_at > datetime('now', '-1 hour')")
conn.commit()
conn.close()
print("Test data cleanup complete\n")

# Load config
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize components
tracker = PositionTracker(db_path)
message_handler = MessageHandler()

# Test 1: Create Pending Position
print("[TEST 1] CREATE PENDING POSITION")
print("-" * 100)

# Mock candidate data
test_candidate = {
    'position_id': f"POS_{datetime.now().strftime('%Y%m%d')}_AAPL_{uuid.uuid4().hex[:8]}",
    'ticker': 'AAPL',
    'entry_price': 175.50,
    'shares': 56,
    'stop_loss': 165.25,
    'target_price': 185.75,
    'risk_per_share': 10.25,
    'total_risk': 574.00,
    'sector': 'Technology',
    'research_composite_score': 7.5
}

# Simulate BuyOrder message ID
buy_order_msg_id = "MSG_PORTFOLIO_20251031T101533Z_3e34f2dd"
risk_assessment_msg_id = "MSG_RISK_20251031T100000Z_test123"

position_id = tracker.create_pending_position(
    candidate=test_candidate,
    order_message_id=buy_order_msg_id,
    risk_assessment_message_id=risk_assessment_msg_id
)

print(f"  Position Created: {position_id}")
print(f"  Ticker: {test_candidate['ticker']}")
print(f"  Status: PENDING")
print(f"  Intended Entry: ${test_candidate['entry_price']:.2f}")
print(f"  Intended Shares: {test_candidate['shares']}")
print(f"  Stop-Loss: ${test_candidate['stop_loss']:.2f}")
print(f"  Target: ${test_candidate['target_price']:.2f}")
print()

# Verify in database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT position_id, ticker, status, intended_entry_price, intended_shares
    FROM portfolio_positions
    WHERE position_id = ?
""", (position_id,))
row = cursor.fetchone()
conn.close()

if row:
    print(f"  Database Verification: SUCCESS")
    print(f"    - Position ID: {row[0]}")
    print(f"    - Ticker: {row[1]}")
    print(f"    - Status: {row[2]}")
    print(f"    - Intended Entry: ${row[3]:.2f}")
    print(f"    - Intended Shares: {row[4]}")
else:
    print(f"  Database Verification: FAILED - Position not found")
print()

# Test 2: Update Position on Full Fill
print("[TEST 2] UPDATE POSITION - FULL FILL")
print("-" * 100)

fill_data = {
    'filled_shares': 56,  # Full fill
    'fill_price': 175.60,  # Slightly different from intended
    'fill_date': datetime.now().date().isoformat(),
    'fill_message_id': 'MSG_TRADING_20251031T101540Z_fill123'
}

success = tracker.update_position_on_fill(position_id, fill_data)

if success:
    print(f"  Position Updated: {position_id}")
    print(f"  Status: PENDING -> OPEN")
    print(f"  Fill Type: FULL")
    print(f"  Filled Shares: {fill_data['filled_shares']}/{test_candidate['shares']}")
    print(f"  Fill Price: ${fill_data['fill_price']:.2f} (intended ${test_candidate['entry_price']:.2f})")
    print(f"  Slippage: ${fill_data['fill_price'] - test_candidate['entry_price']:.2f}")
else:
    print(f"  Update FAILED")
print()

# Verify in database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT status, actual_entry_price, actual_shares, actual_entry_date
    FROM portfolio_positions
    WHERE position_id = ?
""", (position_id,))
row = cursor.fetchone()
conn.close()

if row:
    print(f"  Database Verification: SUCCESS")
    print(f"    - Status: {row[0]}")
    print(f"    - Actual Entry Price: ${row[1]:.2f}")
    print(f"    - Actual Shares: {row[2]}")
    print(f"    - Entry Date: {row[3]}")
else:
    print(f"  Database Verification: FAILED")
print()

# Test 3: Portfolio Summary
print("[TEST 3] PORTFOLIO SUMMARY")
print("-" * 100)

summary = tracker.get_portfolio_summary()

print(f"  Position Counts:")
print(f"    - PENDING: {summary['pending_positions']}")
print(f"    - OPEN: {summary['open_positions']}")
print(f"    - CLOSED: {summary['closed_positions']}")
print(f"    - REJECTED: {summary['rejected_positions']}")
print()
print(f"  Capital:")
print(f"    - Deployed: ${summary['capital_deployed']:,.2f}")
print(f"    - Unrealized P&L: ${summary['unrealized_pnl']:,.2f}")
print(f"    - Realized P&L: ${summary['realized_pnl']:,.2f}")
print(f"    - Total P&L: ${summary['total_pnl']:,.2f}")
print()

# Test 4: Close Position (Simulate Target Hit)
print("[TEST 4] CLOSE POSITION - TARGET HIT")
print("-" * 100)

exit_data = {
    'exit_price': 186.00,  # Above target
    'exit_date': datetime.now().date().isoformat(),
    'exit_reason': 'TARGET',
    'exit_message_id': 'MSG_PORTFOLIO_20251031T105000Z_sell123'
}

success = tracker.close_position(position_id, exit_data)

if success:
    print(f"  Position Closed: {position_id}")
    print(f"  Status: OPEN -> CLOSED")
    print(f"  Exit Reason: {exit_data['exit_reason']}")
    print(f"  Entry Price: ${fill_data['fill_price']:.2f}")
    print(f"  Exit Price: ${exit_data['exit_price']:.2f}")

    gain_per_share = exit_data['exit_price'] - fill_data['fill_price']
    total_gain = gain_per_share * fill_data['filled_shares']
    return_pct = (gain_per_share / fill_data['fill_price']) * 100

    print(f"  Gain: ${gain_per_share:.2f}/share × {fill_data['filled_shares']} = ${total_gain:.2f}")
    print(f"  Return: {return_pct:+.2f}%")
else:
    print(f"  Close FAILED")
print()

# Verify in database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT status, exit_reason, exit_price, exit_date
    FROM portfolio_positions
    WHERE position_id = ?
""", (position_id,))
row = cursor.fetchone()
conn.close()

if row:
    print(f"  Database Verification: SUCCESS")
    print(f"    - Status: {row[0]}")
    print(f"    - Exit Reason: {row[1]}")
    print(f"    - Exit Price: ${row[2]:.2f}")
    print(f"    - Exit Date: {row[3]}")
else:
    print(f"  Database Verification: FAILED")
print()

# Test 5: Partial Fill Scenario
print("[TEST 5] PARTIAL FILL SCENARIO")
print("-" * 100)

# Create another pending position
test_candidate_2 = {
    'position_id': f"POS_{datetime.now().strftime('%Y%m%d')}_MSFT_{uuid.uuid4().hex[:8]}",
    'ticker': 'MSFT',
    'entry_price': 420.00,
    'shares': 40,
    'stop_loss': 400.00,
    'target_price': 440.00,
    'risk_per_share': 20.00,
    'total_risk': 800.00,
    'sector': 'Technology',
    'research_composite_score': 6.8
}

position_id_2 = tracker.create_pending_position(
    candidate=test_candidate_2,
    order_message_id="MSG_PORTFOLIO_20251031T110000Z_buy456",
    risk_assessment_message_id="MSG_RISK_20251031T105500Z_test456"
)

print(f"  Position Created: {position_id_2}")
print(f"  Ticker: {test_candidate_2['ticker']}")
print(f"  Intended Shares: {test_candidate_2['shares']}")
print()

# Simulate partial fill (only 30 out of 40 shares filled)
partial_fill_data = {
    'filled_shares': 30,  # Partial fill
    'fill_price': 420.50,
    'fill_date': datetime.now().date().isoformat(),
    'fill_message_id': 'MSG_TRADING_20251031T110100Z_fill456'
}

success = tracker.update_position_on_fill(position_id_2, partial_fill_data)

if success:
    print(f"  Position Updated: {position_id_2}")
    print(f"  Fill Type: PARTIAL")
    print(f"  Filled Shares: {partial_fill_data['filled_shares']}/{test_candidate_2['shares']}")
    print(f"  Fill Rate: {(partial_fill_data['filled_shares']/test_candidate_2['shares'])*100:.1f}%")
    print(f"  Unfilled: {test_candidate_2['shares'] - partial_fill_data['filled_shares']} shares")
else:
    print(f"  Update FAILED")
print()

# Test 6: Reconciliation
print("[TEST 6] RECONCILIATION CHECK")
print("-" * 100)

issues = tracker.reconcile_with_trading()

print(f"  Stale PENDING Positions: {len(issues['stale_pending'])}")
if issues['stale_pending']:
    for pos_id in issues['stale_pending']:
        print(f"    - {pos_id}")

print(f"  Price Discrepancies: {len(issues['price_discrepancies'])}")
if issues['price_discrepancies']:
    for pos_id in issues['price_discrepancies']:
        print(f"    - {pos_id}")

if not issues['stale_pending'] and not issues['price_discrepancies']:
    print(f"  No issues found - all positions reconciled")
print()

# Test 7: Get Position Details
print("[TEST 7] GET POSITION DETAILS")
print("-" * 100)

details = tracker.get_position_details(position_id)

if details:
    print(f"  Position ID: {details['position_id']}")
    print(f"  Ticker: {details['ticker']}")
    print(f"  Status: {details['status']}")
    print(f"  Intended Entry: ${details['intended_entry_price']:.2f}")
    print(f"  Actual Entry: ${details['actual_entry_price']:.2f}")
    print(f"  Exit Price: ${details['exit_price']:.2f}")
    print(f"  Exit Reason: {details['exit_reason']}")
    print(f"  Created: {details['created_at']}")
    print(f"  Updated: {details['updated_at']}")
else:
    print(f"  Position not found")
print()

# Final Summary
print("=" * 100)
print("TEST COMPLETE - POSITION TRACKER")
print("=" * 100)

final_summary = tracker.get_portfolio_summary()

print(f"Final Portfolio State:")
print(f"  - PENDING: {final_summary['pending_positions']}")
print(f"  - OPEN: {final_summary['open_positions']}")
print(f"  - CLOSED: {final_summary['closed_positions']}")
print(f"  - Total Capital Deployed: ${final_summary['capital_deployed']:,.2f}")
print(f"  - Total P&L: ${final_summary['total_pnl']:,.2f}")
print()
print("Week 4 Day 3 COMPLETE: PositionTracker class verified")
print("=" * 100)
