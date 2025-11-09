"""
TEST: Portfolio Department End-to-End Integration (Week 4 Day 5)
Tests complete workflow with 4 scenarios:
A. Fresh portfolio -> First trades
B. Full portfolio -> Capacity rejections
C. Exit signal -> Rebalancing triggered
D. Partial fill handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
import json
import sqlite3
from pathlib import Path
from datetime import datetime, date
import uuid

# Import Portfolio Department
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from portfolio_department import (
    PortfolioDepartment,
    MessageHandler,
    PositionTracker
)

# Paths
config_path = Path("Config/portfolio_config.yaml")
db_path = Path("sentinel.db")
inbox_path = Path("Messages_Between_Departments/Inbox/PORTFOLIO")
outbox_path = Path("Messages_Between_Departments/Outbox/PORTFOLIO")

print("=" * 100)
print("PORTFOLIO DEPARTMENT - END-TO-END INTEGRATION TESTS")
print("=" * 100)
print()

# Clean up test data and messages
print("[SETUP] Cleaning test environment...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clean positions from previous tests
cursor.execute("DELETE FROM portfolio_positions WHERE created_at > datetime('now', '-1 day')")
cursor.execute("DELETE FROM portfolio_decisions WHERE created_at > datetime('now', '-1 day')")
cursor.execute("DELETE FROM portfolio_rejections WHERE created_at > datetime('now', '-1 day')")
conn.commit()
conn.close()

# Clean test messages
for msg_file in inbox_path.glob("MSG_RISK_TEST_*.md"):
    msg_file.unlink()

print("  Test environment clean")
print()

# Initialize Portfolio Department
portfolio = PortfolioDepartment(config_path, db_path)
tracker = PositionTracker(db_path)

# ============================================================================
# SCENARIO A: Fresh Portfolio -> First Trades
# ============================================================================
print("=" * 100)
print("SCENARIO A: FRESH PORTFOLIO -> FIRST TRADES")
print("=" * 100)
print()

print("[A.1] SETUP: Create mock RiskAssessment with 3 candidates")
print("-" * 100)

# Create RiskAssessment message with 3 approved candidates
risk_msg_a = {
    'metadata': {
        'from': 'RISK',
        'to': 'PORTFOLIO',
        'message_id': f'MSG_RISK_TEST_A_{uuid.uuid4().hex[:8]}',
        'message_type': 'RiskAssessment',
        'priority': 'high',
        'created_at': datetime.now().isoformat()
    },
    'data': {
        'approved_candidates': [
            {
                'ticker': 'AAPL',
                'entry_price': 175.50,
                'stop_loss': 165.25,
                'target_price': 185.75,
                'shares': 56,
                'position_size_shares': 56,
                'position_size_value': 9828.00,
                'risk_per_share': 10.25,
                'total_risk': 574.00,
                'risk_percentage': 0.00574,
                'risk_reward_ratio': 2.0,
                'sector': 'Technology',
                'research_composite_score': 7.5
            },
            {
                'ticker': 'MSFT',
                'entry_price': 420.00,
                'stop_loss': 400.00,
                'target_price': 440.00,
                'shares': 23,
                'position_size_shares': 23,
                'position_size_value': 9660.00,
                'risk_per_share': 20.00,
                'total_risk': 460.00,
                'risk_percentage': 0.00460,
                'risk_reward_ratio': 2.0,
                'sector': 'Technology',
                'research_composite_score': 6.8
            },
            {
                'ticker': 'JPM',
                'entry_price': 195.00,
                'stop_loss': 185.00,
                'target_price': 205.00,
                'shares': 50,
                'position_size_shares': 50,
                'position_size_value': 9750.00,
                'risk_per_share': 10.00,
                'total_risk': 500.00,
                'risk_percentage': 0.00500,
                'risk_reward_ratio': 2.0,
                'sector': 'Financials',
                'research_composite_score': 6.2
            }
        ]
    }
}

# Write RiskAssessment message to inbox
msg_handler = MessageHandler()
risk_msg_path = inbox_path / f"{risk_msg_a['metadata']['message_id']}.md"

with open(risk_msg_path, 'w') as f:
    # Write YAML frontmatter
    f.write("---\n")
    for key, value in risk_msg_a['metadata'].items():
        f.write(f"{key}: {value}\n")
    f.write("---\n\n")

    # Write body
    f.write("# Risk Assessment - 3 Candidates Approved\n\n")
    f.write("Portfolio Department: Please review these approved candidates.\n\n")

    # Write JSON payload
    f.write("```json\n")
    f.write(json.dumps(risk_msg_a['data'], indent=2))
    f.write("\n```\n")

print(f"  RiskAssessment created: {risk_msg_a['metadata']['message_id']}")
print(f"  Candidates: 3 (AAPL, MSFT, JPM)")
print()

print("[A.2] EXECUTION: Run Portfolio daily cycle")
print("-" * 100)

# Run daily cycle
portfolio.run_daily_cycle()

print()
print("[A.3] VERIFICATION: Check results")
print("-" * 100)

# Check portfolio summary
summary_a = tracker.get_portfolio_summary()

print(f"  Portfolio Summary:")
print(f"    - PENDING: {summary_a['pending_positions']}")
print(f"    - OPEN: {summary_a['open_positions']}")
print(f"    - Deployed Capital: ${summary_a['capital_deployed']:,.2f}")
print()

# Check database for PENDING positions
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT position_id, ticker, intended_shares, intended_entry_price
    FROM portfolio_positions
    WHERE status = 'PENDING'
    ORDER BY created_at DESC
    LIMIT 3
""")
pending_positions_a = cursor.fetchall()
conn.close()

print(f"  PENDING Positions Created: {len(pending_positions_a)}")
for pos_id, ticker, shares, price in pending_positions_a:
    print(f"    - {ticker}: {shares} shares @ ${price:.2f} (Position: {pos_id})")
print()

# Check BuyOrder messages generated
buy_orders_a = sorted(outbox_path.glob("MSG_PORTFOLIO_*_BUY_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:3]

print(f"  BuyOrder Messages Generated: {len(buy_orders_a)}")
for msg_file in buy_orders_a:
    print(f"    - {msg_file.name}")
print()

print(f"SCENARIO A RESULT: {'PASS' if len(pending_positions_a) == 3 else 'FAIL'}")
print(f"  Expected: 3 BuyOrders, 3 PENDING positions")
print(f"  Actual: {len(buy_orders_a)} BuyOrders, {len(pending_positions_a)} PENDING positions")
print()

# ============================================================================
# SCENARIO B: Full Portfolio -> Capacity Rejections
# ============================================================================
print("=" * 100)
print("SCENARIO B: FULL PORTFOLIO -> CAPACITY REJECTIONS")
print("=" * 100)
print()

print("[B.1] SETUP: Fill portfolio to max capacity (20 positions)")
print("-" * 100)

# Create 7 more OPEN positions (already have 3 PENDING from Scenario A)
tickers_b = ['GS', 'BAC', 'WFC', 'C', 'V', 'MA', 'AXP']

for i, ticker in enumerate(tickers_b):
    pos_id_b = f"POS_{datetime.now().strftime('%Y%m%d')}_{ticker}_{uuid.uuid4().hex[:8]}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO portfolio_positions (
            position_id, ticker, status,
            intended_entry_price, intended_shares,
            intended_stop_loss, intended_target,
            actual_entry_price, actual_entry_date, actual_shares,
            risk_per_share, total_risk, sector,
            entry_order_message_id, risk_assessment_message_id,
            created_at, updated_at
        ) VALUES (?, ?, 'OPEN', ?, ?, ?, ?, ?, date('now'), ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (
        pos_id_b, ticker,
        100.00 + i * 10, 100 - i * 5,  # Varying prices and shares
        90.00 + i * 10, 110.00 + i * 10,
        100.50 + i * 10, 100 - i * 5,
        5.00, 500.00, 'Financials',
        f'MSG_PORTFOLIO_TEST_B_{i}', f'MSG_RISK_TEST_B_{i}'
    ))
    conn.commit()
    conn.close()

# Convert PENDING to OPEN for the 3 from Scenario A (simulate fills)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    UPDATE portfolio_positions
    SET status = 'OPEN',
        actual_entry_price = intended_entry_price,
        actual_entry_date = date('now'),
        actual_shares = intended_shares,
        updated_at = datetime('now')
    WHERE status = 'PENDING'
""")
conn.commit()
conn.close()

summary_b = tracker.get_portfolio_summary()
print(f"  Portfolio filled: {summary_b['open_positions']} OPEN positions")
print()

print("[B.2] SETUP: Create RiskAssessment with 2 new candidates")
print("-" * 100)

risk_msg_b = {
    'metadata': {
        'from': 'RISK',
        'to': 'PORTFOLIO',
        'message_id': f'MSG_RISK_TEST_B_{uuid.uuid4().hex[:8]}',
        'message_type': 'RiskAssessment',
        'priority': 'high',
        'created_at': datetime.now().isoformat()
    },
    'data': {
        'approved_candidates': [
            {
                'ticker': 'NVDA',
                'entry_price': 880.00,
                'stop_loss': 850.00,
                'target_price': 920.00,
                'shares': 11,
                'position_size_shares': 11,
                'position_size_value': 9680.00,
                'risk_per_share': 30.00,
                'total_risk': 330.00,
                'risk_percentage': 0.00330,
                'risk_reward_ratio': 2.0,
                'sector': 'Technology',
                'research_composite_score': 8.2
            },
            {
                'ticker': 'GOOGL',
                'entry_price': 145.00,
                'stop_loss': 135.00,
                'target_price': 155.00,
                'shares': 68,
                'position_size_shares': 68,
                'position_size_value': 9860.00,
                'risk_per_share': 10.00,
                'total_risk': 680.00,
                'risk_percentage': 0.00680,
                'risk_reward_ratio': 2.0,
                'sector': 'Technology',
                'research_composite_score': 7.8
            }
        ]
    }
}

# Write RiskAssessment to inbox
risk_msg_path_b = inbox_path / f"{risk_msg_b['metadata']['message_id']}.md"

with open(risk_msg_path_b, 'w') as f:
    f.write("---\n")
    for key, value in risk_msg_b['metadata'].items():
        f.write(f"{key}: {value}\n")
    f.write("---\n\n")
    f.write("# Risk Assessment - 2 Candidates Approved\n\n")
    f.write("```json\n")
    f.write(json.dumps(risk_msg_b['data'], indent=2))
    f.write("\n```\n")

print(f"  RiskAssessment created: {risk_msg_b['metadata']['message_id']}")
print(f"  Candidates: 2 (NVDA, GOOGL)")
print()

print("[B.3] EXECUTION: Run Portfolio daily cycle (should reject both)")
print("-" * 100)

portfolio.run_daily_cycle()

print()
print("[B.4] VERIFICATION: Check rejections")
print("-" * 100)

# Check for rejections in database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT ticker, rejection_reason, rejection_category
    FROM portfolio_rejections
    WHERE decision_timestamp > datetime('now', '-1 minute')
    ORDER BY decision_timestamp DESC
""")
rejections_b = cursor.fetchall()
conn.close()

print(f"  Rejections Logged: {len(rejections_b)}")
for ticker, reason, category in rejections_b:
    print(f"    - {ticker}: {reason} ({category})")
print()

# Check no new PENDING positions created
summary_b2 = tracker.get_portfolio_summary()
print(f"  Portfolio Status After:")
print(f"    - OPEN: {summary_b2['open_positions']}")
print(f"    - PENDING: {summary_b2['pending_positions']}")
print()

print(f"SCENARIO B RESULT: {'PASS' if len(rejections_b) == 2 else 'FAIL'}")
print(f"  Expected: 2 rejections (MAX_POSITIONS_REACHED), 0 new positions")
print(f"  Actual: {len(rejections_b)} rejections, {summary_b2['pending_positions']} new PENDING")
print()

# ============================================================================
# SCENARIO C: Exit Signal -> Rebalancing Triggered
# ============================================================================
print("=" * 100)
print("SCENARIO C: EXIT SIGNAL -> REBALANCING TRIGGERED")
print("=" * 100)
print()

print("[C.1] SETUP: Close 5 positions to free capacity")
print("-" * 100)

# Close 5 positions (simulate exits)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get 5 position IDs to close
cursor.execute("""
    SELECT position_id FROM portfolio_positions
    WHERE status = 'OPEN'
    LIMIT 5
""")
positions_to_close = [row[0] for row in cursor.fetchall()]

# Close them
for pos_id in positions_to_close:
    cursor.execute("""
        UPDATE portfolio_positions
        SET status = 'CLOSED',
            exit_reason = 'TARGET',
            exit_price = actual_entry_price * 1.10,
            exit_date = date('now'),
            updated_at = datetime('now')
        WHERE position_id = ?
    """, (pos_id,))

conn.commit()
conn.close()

summary_c = tracker.get_portfolio_summary()
print(f"  Closed 5 positions")
print(f"  Portfolio Status:")
print(f"    - OPEN: {summary_c['open_positions']}")
print(f"    - CLOSED: {summary_c['closed_positions']}")
print(f"    - Deployment: ${summary_c['capital_deployed']:,.2f}")
print()

print("[C.2] EXECUTION: Run Portfolio daily cycle (should trigger rebalancing)")
print("-" * 100)

# Count messages before
messages_before_c = len(list(outbox_path.glob("MSG_PORTFOLIO_*_CandidateRequest_*.md")))

portfolio.run_daily_cycle()

# Count messages after
messages_after_c = len(list(outbox_path.glob("MSG_PORTFOLIO_*_CandidateRequest_*.md")))

print()
print("[C.3] VERIFICATION: Check CandidateRequest sent")
print("-" * 100)

candidate_requests_c = messages_after_c - messages_before_c

print(f"  CandidateRequest Messages: {candidate_requests_c}")

if candidate_requests_c > 0:
    latest_request = sorted(
        outbox_path.glob("MSG_PORTFOLIO_*CandidateRequest*.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )[0]

    with open(latest_request, 'r') as f:
        content = f.read()

    print(f"    - Message: {latest_request.name}")
    print(f"    - To: RESEARCH")

    if "```json" in content:
        json_start = content.find("```json") + 7
        json_end = content.find("```", json_start)
        payload = json.loads(content[json_start:json_end].strip())

        print(f"    - Available Positions: {payload['deployment_status']['available_positions']}")
        print(f"    - Available Capital: ${payload['deployment_status']['available_capital']:,.2f}")

print()

print(f"SCENARIO C RESULT: {'PASS' if candidate_requests_c > 0 else 'FAIL'}")
print(f"  Expected: 1 CandidateRequest sent to Research")
print(f"  Actual: {candidate_requests_c} CandidateRequest(s) sent")
print()

# ============================================================================
# SCENARIO D: Partial Fill Handling
# ============================================================================
print("=" * 100)
print("SCENARIO D: PARTIAL FILL HANDLING")
print("=" * 100)
print()

print("[D.1] SETUP: Create PENDING position")
print("-" * 100)

# Create a PENDING position
pos_id_d = f"POS_{datetime.now().strftime('%Y%m%d')}_TSLA_{uuid.uuid4().hex[:8]}"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO portfolio_positions (
        position_id, ticker, status,
        intended_entry_price, intended_shares,
        intended_stop_loss, intended_target,
        risk_per_share, total_risk, sector,
        entry_order_message_id, risk_assessment_message_id,
        created_at, updated_at
    ) VALUES (?, 'TSLA', 'PENDING', ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
""", (
    pos_id_d,
    250.00, 40,  # Intended: 40 shares
    230.00, 270.00,
    20.00, 800.00, 'Consumer Cyclical',
    f'MSG_PORTFOLIO_TEST_D', f'MSG_RISK_TEST_D'
))
conn.commit()
conn.close()

print(f"  PENDING Position Created: {pos_id_d}")
print(f"  Ticker: TSLA")
print(f"  Intended Shares: 40")
print()

print("[D.2] EXECUTION: Simulate partial fill (30/40 shares)")
print("-" * 100)

# Simulate partial fill (75% filled)
fill_data_d = {
    'filled_shares': 30,  # Only 30 out of 40 filled
    'fill_price': 251.50,
    'fill_date': datetime.now().date().isoformat(),
    'fill_message_id': 'MSG_TRADING_TEST_D_FILL'
}

success_d = tracker.update_position_on_fill(pos_id_d, fill_data_d)

print(f"  Fill Update: {'SUCCESS' if success_d else 'FAILED'}")
print(f"  Filled Shares: {fill_data_d['filled_shares']}/40 (75.0%)")
print(f"  Fill Price: ${fill_data_d['fill_price']:.2f}")
print()

print("[D.3] VERIFICATION: Check position updated correctly")
print("-" * 100)

# Verify position in database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    SELECT status, intended_shares, actual_shares, actual_entry_price
    FROM portfolio_positions
    WHERE position_id = ?
""", (pos_id_d,))
row_d = cursor.fetchone()
conn.close()

if row_d:
    status_d, intended_d, actual_d, price_d = row_d

    print(f"  Position Status:")
    print(f"    - Status: {status_d}")
    print(f"    - Intended Shares: {intended_d}")
    print(f"    - Actual Shares: {actual_d}")
    print(f"    - Actual Entry Price: ${price_d:.2f}")
    print(f"    - Fill Rate: {(actual_d/intended_d)*100:.1f}%")
    print()

    # Recalculated risk
    actual_risk_d = actual_d * 20.00  # risk_per_share = $20
    print(f"  Risk Recalculation:")
    print(f"    - Intended Risk: $800.00 (40 shares × $20)")
    print(f"    - Actual Risk: ${actual_risk_d:.2f} ({actual_d} shares × $20)")
    print(f"    - Risk Reduction: ${800.00 - actual_risk_d:.2f}")
    print()

print(f"SCENARIO D RESULT: {'PASS' if row_d and row_d[0] == 'OPEN' and row_d[2] == 30 else 'FAIL'}")
print(f"  Expected: Position status = OPEN, actual_shares = 30")
print(f"  Actual: Position status = {row_d[0] if row_d else 'N/A'}, actual_shares = {row_d[2] if row_d else 'N/A'}")
print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("=" * 100)
print("INTEGRATION TESTS COMPLETE - FINAL SUMMARY")
print("=" * 100)
print()

final_summary = tracker.get_portfolio_summary()

print("Final Portfolio State:")
print(f"  - PENDING: {final_summary['pending_positions']}")
print(f"  - OPEN: {final_summary['open_positions']}")
print(f"  - CLOSED: {final_summary['closed_positions']}")
print(f"  - Deployed Capital: ${final_summary['capital_deployed']:,.2f}")
print(f"  - Total P&L: ${final_summary['total_pnl']:,.2f}")
print()

# Test results summary
scenarios_passed = 0
scenarios_total = 4

if len(pending_positions_a) == 3:
    scenarios_passed += 1
if len(rejections_b) == 2:
    scenarios_passed += 1
if candidate_requests_c > 0:
    scenarios_passed += 1
if row_d and row_d[0] == 'OPEN' and row_d[2] == 30:
    scenarios_passed += 1

print("Test Results:")
print(f"  Scenario A (Fresh Portfolio): {'PASS' if len(pending_positions_a) == 3 else 'FAIL'}")
print(f"  Scenario B (Full Portfolio): {'PASS' if len(rejections_b) == 2 else 'FAIL'}")
print(f"  Scenario C (Exit -> Rebalance): {'PASS' if candidate_requests_c > 0 else 'FAIL'}")
print(f"  Scenario D (Partial Fill): {'PASS' if row_d and row_d[0] == 'OPEN' and row_d[2] == 30 else 'FAIL'}")
print()
print(f"  Overall: {scenarios_passed}/{scenarios_total} scenarios passed")
print()

if scenarios_passed == scenarios_total:
    print("Week 4 Day 5 COMPLETE: All integration tests passed!")
    print("Portfolio Department is PRODUCTION READY!")
else:
    print(f"WARNING: {scenarios_total - scenarios_passed} scenario(s) failed")
    print("Review test output above for details")

print("=" * 100)
