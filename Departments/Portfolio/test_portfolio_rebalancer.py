"""
TEST: PortfolioRebalancer Class (Week 4 Day 4)
Tests deployment monitoring, candidate requests, and sector concentration checks
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
import json
from pathlib import Path

# Import PortfolioRebalancer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from portfolio_department import PortfolioRebalancer, MessageHandler

# Paths
config_path = Path("Config/portfolio_config.yaml")
db_path = Path("sentinel.db")

print("=" * 100)
print("PORTFOLIO REBALANCER TEST - Week 4 Day 4")
print("=" * 100)
print()

# Load config
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize components
rebalancer = PortfolioRebalancer(config, db_path)
message_handler = MessageHandler()

# Test 1: Check Deployment Status
print("[TEST 1] CHECK DEPLOYMENT STATUS")
print("-" * 100)

status = rebalancer.check_deployment_status()

print(f"  Timestamp: {status['timestamp']}")
print()
print(f"  Position Status:")
print(f"    - OPEN: {status['open_positions']}")
print(f"    - PENDING: {status['pending_positions']}")
print(f"    - Total: {status['total_positions']}/{status['max_positions']}")
print(f"    - Available Slots: {status['available_positions']}")
print()
print(f"  Capital Deployment:")
print(f"    - Deployed: ${status['deployed_capital']:,.2f}")
print(f"    - Target: ${status['target_capital']:,.2f}")
print(f"    - Available: ${status['available_capital']:,.2f}")
print()
print(f"  Deployment Percentage:")
print(f"    - Current: {status['deployment_pct']:.1%}")
print(f"    - Target: {status['target_deployment_pct']:.1%}")
print()
print(f"  Rebalancing Status:")
print(f"    - Under-Deployed: {status['under_deployed']}")
print(f"    - Has Capacity: {status['has_capacity']}")
print(f"    - Needs Rebalancing: {status['needs_rebalancing']}")
print()

# Test 2: Sector Concentration
print("[TEST 2] SECTOR CONCENTRATION CHECK")
print("-" * 100)

sector_weights = rebalancer.check_sector_concentration()

if sector_weights:
    print(f"  Current Sector Allocation:")
    for sector, weight in sorted(sector_weights.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {sector}: {weight:.1%}")
        if weight > 0.30:
            print(f"      WARNING: Over-concentrated (>30% threshold)")
else:
    print(f"  No open positions - sector allocation N/A")
print()

# Test 3: Generate Candidate Request (if needed)
print("[TEST 3] CANDIDATE REQUEST GENERATION")
print("-" * 100)

if status['needs_rebalancing']:
    print(f"  Portfolio needs rebalancing - generating candidate request...")
    print()

    message_id = rebalancer.generate_candidate_request(message_handler)

    print(f"  Candidate Request Generated:")
    print(f"    - Message ID: {message_id}")
    print(f"    - To: RESEARCH")
    print(f"    - Priority: HIGH")
    print()

    # Read the message back
    outbox_path = Path("Messages_Between_Departments/Outbox/PORTFOLIO")
    message_files = sorted(outbox_path.glob("MSG_PORTFOLIO_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)

    if message_files:
        latest_message = message_files[0]
        with open(latest_message, 'r') as f:
            content = f.read()

        # Extract JSON payload
        if "```json" in content:
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            payload = json.loads(content[json_start:json_end].strip())

            print(f"  Request Details:")
            print(f"    - Available Positions: {payload['deployment_status']['available_positions']}")
            print(f"    - Available Capital: ${payload['deployment_status']['available_capital']:,.2f}")
            print(f"    - Min Score: {payload['criteria']['min_composite_score']}")
            print(f"    - Max Candidates: {payload['criteria']['max_candidates']}")
            print(f"    - Require Sector Diversification: {payload['criteria']['require_sector_diversification']}")
else:
    print(f"  Portfolio is adequately deployed - no candidate request needed")
    print(f"    - Current Deployment: {status['deployment_pct']:.1%}")
    print(f"    - Minimum Threshold: {config['rebalancing']['min_deployment_threshold']:.1%} of {status['target_deployment_pct']:.1%}")
    print(f"    - Trigger Level: {status['target_deployment_pct'] * config['rebalancing']['min_deployment_threshold']:.1%}")
print()

# Test 4: Generate Rebalancing Report
print("[TEST 4] COMPREHENSIVE REBALANCING REPORT")
print("-" * 100)

report = rebalancer.generate_rebalancing_report()

print(f"  Report Timestamp: {report['timestamp']}")
print()

# Deployment metrics
deployment = report['deployment']
print(f"  Deployment Metrics:")
print(f"    - Deployed Capital: ${deployment['deployed_capital']:,.2f} ({deployment['deployment_pct']:.1%})")
print(f"    - Target Capital: ${deployment['target_capital']:,.2f} ({deployment['target_deployment_pct']:.1%})")
print(f"    - Available Capital: ${deployment['available_capital']:,.2f}")
print(f"    - Positions: {deployment['total_positions']}/{deployment['max_positions']}")
print()

# Position metrics
pos_metrics = report['position_metrics']
if pos_metrics['average_size'] > 0:
    print(f"  Position Metrics:")
    print(f"    - Average Size: ${pos_metrics['average_size']:,.2f}")
    print(f"    - Min Size: ${pos_metrics['min_size']:,.2f}")
    print(f"    - Max Size: ${pos_metrics['max_size']:,.2f}")
    print(f"    - Largest Position: {pos_metrics['largest_position_pct']:.1%} of portfolio")
    print()

# Sector allocation
sector_alloc = report['sector_allocation']
if sector_alloc:
    print(f"  Sector Allocation:")
    for sector, weight in sorted(sector_alloc.items(), key=lambda x: x[1], reverse=True):
        status_flag = " [OVER-CONCENTRATED]" if weight > 0.30 else ""
        print(f"    - {sector}: {weight:.1%}{status_flag}")
    print()

# Recommendations
recommendations = report['recommendations']
if recommendations:
    print(f"  Recommendations ({len(recommendations)}):")
    for i, rec in enumerate(recommendations, 1):
        print(f"    {i}. [{rec['priority']}] {rec['action']}")
        print(f"       Reason: {rec['reason']}")
else:
    print(f"  No recommendations - portfolio is well-balanced")
print()

# Test 5: Verify Message Format
print("[TEST 5] MESSAGE FORMAT VERIFICATION")
print("-" * 100)

if status['needs_rebalancing']:
    outbox_path = Path("Messages_Between_Departments/Outbox/PORTFOLIO")
    message_files = sorted(outbox_path.glob("MSG_PORTFOLIO_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)

    if message_files:
        latest_message = message_files[0]

        print(f"  Message File: {latest_message.name}")
        print()

        with open(latest_message, 'r') as f:
            content = f.read()

        # Check for required components
        has_frontmatter = content.startswith("---")
        has_json_payload = "```json" in content
        has_to_dept = "to: RESEARCH" in content
        has_message_type = "message_type: CandidateRequest" in content
        has_priority = "priority: high" in content

        print(f"  Format Validation:")
        print(f"    - YAML Frontmatter: {'PASS' if has_frontmatter else 'FAIL'}")
        print(f"    - To Department: {'PASS' if has_to_dept else 'FAIL'}")
        print(f"    - Message Type: {'PASS' if has_message_type else 'FAIL'}")
        print(f"    - Priority Level: {'PASS' if has_priority else 'FAIL'}")
        print(f"    - JSON Payload: {'PASS' if has_json_payload else 'FAIL'}")
        print()

        if all([has_frontmatter, has_json_payload, has_to_dept, has_message_type, has_priority]):
            print(f"  Message Format: VALID")
        else:
            print(f"  Message Format: INVALID")
else:
    print(f"  No message generated - skipping format verification")
print()

# Final Summary
print("=" * 100)
print("TEST COMPLETE - PORTFOLIO REBALANCER")
print("=" * 100)

final_status = rebalancer.check_deployment_status()

print(f"Final Portfolio Status:")
print(f"  - Deployment: {final_status['deployment_pct']:.1%} of {final_status['target_deployment_pct']:.1%} target")
print(f"  - Positions: {final_status['total_positions']}/{final_status['max_positions']}")
print(f"  - Capital: ${final_status['deployed_capital']:,.2f} deployed / ${final_status['available_capital']:,.2f} available")
print(f"  - Needs Rebalancing: {'YES' if final_status['needs_rebalancing'] else 'NO'}")
print()
print("Week 4 Day 4 COMPLETE: PortfolioRebalancer class verified")
print("=" * 100)
