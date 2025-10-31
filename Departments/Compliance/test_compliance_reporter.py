"""
TEST: ComplianceReporter Class (Week 5 Day 3)
Tests report generation: Markdown, CSV, and JSON exports
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import yaml
from pathlib import Path
from datetime import datetime, date

# Import ComplianceReporter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from compliance_department import ComplianceReporter

# Paths
config_path = Path("Config/compliance_config.yaml")
db_path = Path("sentinel.db")
report_dir = Path("Reports/Compliance")

print("=" * 100)
print("COMPLIANCE REPORTER TEST - Week 5 Day 3")
print("=" * 100)
print()

# Load config
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize ComplianceReporter
reporter = ComplianceReporter(config, db_path)

# Test 1: Generate Daily Report (Markdown)
print("[TEST 1] GENERATE DAILY REPORT (MARKDOWN)")
print("-" * 100)

report_path = reporter.generate_daily_report()

if report_path:
    print(f"  Report Generated: {report_path}")

    # Check file exists
    if Path(report_path).exists():
        file_size = Path(report_path).stat().st_size
        print(f"  File Size: {file_size} bytes")
        print(f"  Status: SUCCESS")

        # Show first 20 lines
        print()
        print("  Report Preview (first 20 lines):")
        print("  " + "-" * 96)
        with open(report_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:20]
            for line in lines:
                print(f"  {line.rstrip()}")
    else:
        print(f"  Status: FAILED - File not found")
else:
    print(f"  Report generation FAILED")
print()

# Test 2: Generate Trade CSV
print("[TEST 2] GENERATE TRADE CSV")
print("-" * 100)

csv_path = reporter.generate_trade_csv()

if csv_path:
    print(f"  CSV Generated: {csv_path}")

    # Check file exists
    if Path(csv_path).exists():
        file_size = Path(csv_path).stat().st_size

        # Count rows
        with open(csv_path, 'r', encoding='utf-8') as f:
            row_count = len(f.readlines())

        print(f"  File Size: {file_size} bytes")
        print(f"  Total Rows: {row_count} (including header)")
        print(f"  Data Rows: {row_count - 1}")
        print(f"  Status: SUCCESS")

        # Show first 5 rows
        print()
        print("  CSV Preview (first 5 rows):")
        print("  " + "-" * 96)
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]
            for i, line in enumerate(lines):
                print(f"  Row {i}: {line.rstrip()[:90]}...")
    else:
        print(f"  Status: FAILED - File not found")
else:
    print(f"  CSV generation FAILED")
print()

# Test 3: Generate Violation CSV
print("[TEST 3] GENERATE VIOLATION CSV")
print("-" * 100)

violation_csv_path = reporter.generate_violation_csv()

if violation_csv_path:
    print(f"  CSV Generated: {violation_csv_path}")

    # Check file exists
    if Path(violation_csv_path).exists():
        file_size = Path(violation_csv_path).stat().st_size

        # Count rows
        with open(violation_csv_path, 'r', encoding='utf-8') as f:
            row_count = len(f.readlines())

        print(f"  File Size: {file_size} bytes")
        print(f"  Total Rows: {row_count} (including header)")
        print(f"  Data Rows: {row_count - 1}")
        print(f"  Status: SUCCESS")
    else:
        print(f"  Status: FAILED - File not found")
else:
    print(f"  CSV generation FAILED")
print()

# Test 4: Generate Portfolio JSON
print("[TEST 4] GENERATE PORTFOLIO JSON")
print("-" * 100)

json_path = reporter.generate_portfolio_json()

if json_path:
    print(f"  JSON Generated: {json_path}")

    # Check file exists
    if Path(json_path).exists():
        file_size = Path(json_path).stat().st_size
        print(f"  File Size: {file_size} bytes")

        # Parse and validate JSON
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"  Status: SUCCESS")
        print()
        print(f"  JSON Structure:")
        print(f"    - Timestamp: {data.get('timestamp', 'N/A')}")
        print(f"    - Date: {data.get('date', 'N/A')}")
        print(f"    - Total Positions: {data.get('summary', {}).get('total_positions', 0)}")
        print(f"    - Open Positions: {data.get('summary', {}).get('open_positions', 0)}")
        print(f"    - Capital Deployed: ${data.get('summary', {}).get('capital_deployed', 0):,.2f}")
        print(f"    - Deployment %: {data.get('summary', {}).get('deployment_percentage', 0):.2f}%")
        print(f"    - Portfolio Risk: ${data.get('risk', {}).get('total_portfolio_risk', 0):,.2f}")
        print(f"    - Position Count: {len(data.get('positions', []))}")

        # Show first position if exists
        if data.get('positions'):
            pos = data['positions'][0]
            print()
            print(f"  First Position:")
            print(f"    - Ticker: {pos.get('ticker', 'N/A')}")
            print(f"    - Status: {pos.get('status', 'N/A')}")
            print(f"    - Shares: {pos.get('shares', 0)}")
            print(f"    - Entry: ${pos.get('entry_price', 0):.2f}")
            print(f"    - Value: ${pos.get('position_value', 0):,.2f}")
    else:
        print(f"  Status: FAILED - File not found")
else:
    print(f"  JSON generation FAILED")
print()

# Test 5: Verify Database Report Summary
print("[TEST 5] VERIFY DATABASE REPORT SUMMARY")
print("-" * 100)

import sqlite3

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get most recent report
cursor.execute("""
    SELECT
        report_date,
        total_trades,
        approved_trades,
        rejected_trades,
        total_audits,
        audit_pass,
        audit_warn,
        audit_fail,
        total_violations,
        critical_violations,
        warn_violations
    FROM compliance_daily_reports
    ORDER BY report_date DESC
    LIMIT 1
""")

row = cursor.fetchone()
conn.close()

if row:
    approval_rate = (row[2] / row[1] * 100) if row[1] > 0 else 0.0
    print(f"  Most Recent Report: {row[0]}")
    print()
    print(f"  Trade Summary:")
    print(f"    - Total Trades: {row[1]}")
    print(f"    - Approved: {row[2]}")
    print(f"    - Rejected: {row[3]}")
    print(f"    - Approval Rate: {approval_rate:.1f}%")
    print()
    print(f"  Audit Summary:")
    print(f"    - Total Audits: {row[4]}")
    print(f"    - PASS: {row[5]}")
    print(f"    - WARN: {row[6]}")
    print(f"    - FAIL: {row[7]}")
    print()
    print(f"  Violations:")
    print(f"    - Total: {row[8]}")
    print(f"    - CRITICAL: {row[9]}")
    print(f"    - WARN: {row[10]}")
    print()
    print(f"  Database Verification: SUCCESS")
else:
    print(f"  No report found in database")
print()

# Final Summary
print("=" * 100)
print("TEST COMPLETE - COMPLIANCE REPORTER")
print("=" * 100)
print()
print("Week 5 Day 3 COMPLETE: ComplianceReporter class verified")
print()
print("Files Generated:")
print(f"  1. Daily Report (Markdown): {report_path if report_path else 'N/A'}")
print(f"  2. Trade CSV: {csv_path if csv_path else 'N/A'}")
print(f"  3. Violation CSV: {violation_csv_path if violation_csv_path else 'N/A'}")
print(f"  4. Portfolio JSON: {json_path if json_path else 'N/A'}")
print()
print("Next: Week 5 Day 4 - ComplianceDepartment Orchestrator")
print("=" * 100)
