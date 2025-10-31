"""
Sentinel Corporation - End-to-End Integration Test
Tests all departments and their integration
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# Test results
tests_passed = 0
tests_failed = 0
warnings = []

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_test(test_name, status, details=""):
    global tests_passed, tests_failed
    symbol = "[OK]" if status else "[FAIL]"
    print(f"{symbol} {test_name}")
    if details:
        print(f"     {details}")
    if status:
        tests_passed += 1
    else:
        tests_failed += 1

def print_warning(message):
    warnings.append(message)
    print(f"[WARN] {message}")

print_header("SENTINEL CORPORATION - END-TO-END INTEGRATION TEST")
print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Database: sentinel.db")

# Test 1: Database Existence
print_header("TEST 1: DATABASE AND TABLES")

db_path = Path(__file__).parent / "sentinel.db"
if db_path.exists():
    print_test("Database file exists", True, str(db_path))

    # Connect and check tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\nFound {len(tables)} tables:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  - {table}: {count} rows")

    # Check expected tables
    expected_tables = {
        'research_market_briefings': False,
        'risk_assessments': False,
        'portfolio_positions': False,
        'compliance_trade_validations': False,
        'trading_orders': False
    }

    for table in expected_tables:
        if table in tables:
            expected_tables[table] = True
            print_test(f"Table '{table}' exists", True)
        else:
            print_test(f"Table '{table}' exists", False, "Table not found - department may not be initialized")

    conn.close()
else:
    print_test("Database file exists", False, "sentinel.db not found!")

# Test 2: Executive Department
print_header("TEST 2: EXECUTIVE DEPARTMENT")

try:
    from Departments.Executive.executive_department import ExecutiveDepartment

    project_root = Path(__file__).parent
    executive = ExecutiveDepartment(
        db_path=project_root / 'sentinel.db',
        messages_dir=project_root / 'Messages',
        reports_dir=project_root / 'Reports'
    )

    print_test("ExecutiveDepartment import", True)
    print_test("ExecutiveDepartment initialization", True)

    # Test dashboard data
    try:
        data = executive.get_realtime_dashboard_data()
        print_test("get_realtime_dashboard_data()", True)

        # Check data structure
        required_keys = ['performance', 'open_positions', 'system_health']
        for key in required_keys:
            if key in data:
                print_test(f"Dashboard data has '{key}' key", True)
            else:
                print_test(f"Dashboard data has '{key}' key", False)

        # Display performance metrics
        if 'performance' in data:
            perf = data['performance']
            print("\nPerformance Metrics:")
            for key, value in perf.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value}")

        # Check positions
        if 'open_positions' in data:
            positions = data['open_positions']
            print(f"\nOpen Positions: {len(positions)}")
            for pos in positions[:3]:
                print(f"  {pos.get('ticker', 'N/A')}: {pos.get('shares', 0)} shares")

    except Exception as e:
        print_test("get_realtime_dashboard_data()", False, str(e))

except Exception as e:
    print_test("ExecutiveDepartment import", False, str(e))

# Test 3: Market Data Provider
print_header("TEST 3: MARKET DATA PROVIDER")

try:
    from Utils.market_data_provider import MarketDataProvider

    provider = MarketDataProvider(enable_cache=True)
    print_test("MarketDataProvider import", True)
    print_test("MarketDataProvider initialization", True)

    # Test price fetching
    try:
        price = provider.get_current_price('AAPL')
        if price and price > 0:
            print_test("Fetch current price (AAPL)", True, f"${price:.2f}")
        else:
            print_test("Fetch current price (AAPL)", False, "Price is None or invalid")
    except Exception as e:
        print_test("Fetch current price (AAPL)", False, str(e))

    # Test benchmark
    try:
        benchmark_return, details = provider.get_benchmark_return('SPY', period_days=30)
        print_test("Fetch benchmark return (SPY)", True, f"{benchmark_return:.2f}%")
    except Exception as e:
        print_test("Fetch benchmark return (SPY)", False, str(e))

except Exception as e:
    print_test("MarketDataProvider import", False, str(e))

# Test 4: Email Reporter
print_header("TEST 4: EMAIL REPORTER")

try:
    from Utils.email_reporter import EmailReporter

    reporter = EmailReporter(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender_email="test@example.com",
        sender_password="dummy"
    )
    print_test("EmailReporter import", True)
    print_test("EmailReporter initialization", True)

    # Test HTML generation (not sending)
    try:
        html = reporter.generate_html_report(data)
        if len(html) > 1000:  # Should be substantial HTML
            print_test("Generate HTML report", True, f"{len(html)} bytes")
        else:
            print_test("Generate HTML report", False, "HTML too short")
    except Exception as e:
        print_test("Generate HTML report", False, str(e))

except Exception as e:
    print_test("EmailReporter import", False, str(e))

# Test 5: Terminal Dashboard
print_header("TEST 5: TERMINAL DASHBOARD")

try:
    from Utils.terminal_dashboard import TerminalDashboard

    dashboard = TerminalDashboard(refresh_interval=5)
    print_test("TerminalDashboard import", True)
    print_test("TerminalDashboard initialization", True)

    # Test layout generation (not displaying)
    try:
        layout = dashboard.generate_layout()
        print_test("Generate dashboard layout", True)
    except Exception as e:
        print_test("Generate dashboard layout", False, str(e))

except Exception as e:
    print_test("TerminalDashboard import", False, str(e))

# Test 6: SMS Alerter
print_header("TEST 6: SMS ALERTER")

try:
    from Utils.sms_alerter import SMSAlerter
    import config

    alerter = SMSAlerter(
        account_sid=config.TWILIO_ACCOUNT_SID,
        auth_token=config.TWILIO_AUTH_TOKEN,
        from_phone=config.TWILIO_PHONE_NUMBER,
        to_phone=config.RECIPIENT_PHONE_NUMBER
    )
    print_test("SMSAlerter import", True)
    print_test("SMSAlerter initialization", True)

    # Test alert checking (not sending)
    try:
        alerts = alerter.check_and_alert(data)
        print_test("Check alert thresholds", True, f"{len(alerts)} alert(s) triggered")
        for alert in alerts:
            print(f"     - {alert}")
    except Exception as e:
        print_test("Check alert thresholds", False, str(e))

except Exception as e:
    print_test("SMSAlerter import", False, str(e))

# Test 7: File Structure
print_header("TEST 7: FILE STRUCTURE")

required_files = {
    'config.py': 'Configuration file',
    'sentinel.db': 'Database file',
    'Utils/market_data_provider.py': 'Market data provider',
    'Utils/email_reporter.py': 'Email reporter',
    'Utils/terminal_dashboard.py': 'Terminal dashboard',
    'Utils/sms_alerter.py': 'SMS alerter',
    'Departments/Executive/executive_department.py': 'Executive department',
    'Launch_Dashboard.bat': 'Dashboard launcher',
    'Send_Email_Report.bat': 'Email sender',
    'Sentinel_Control_Panel.bat': 'Control panel'
}

for file_path, description in required_files.items():
    full_path = Path(__file__).parent / file_path
    exists = full_path.exists()
    print_test(f"{description} exists", exists, file_path if exists else "Not found")

# Final Summary
print_header("TEST SUMMARY")

print(f"\nTests Passed:  {tests_passed}")
print(f"Tests Failed:  {tests_failed}")
print(f"Warnings:      {len(warnings)}")

if warnings:
    print("\nWarnings:")
    for warning in warnings:
        print(f"  - {warning}")

success_rate = (tests_passed / (tests_passed + tests_failed) * 100) if (tests_passed + tests_failed) > 0 else 0
print(f"\nSuccess Rate: {success_rate:.1f}%")

if tests_failed == 0:
    print("\n[OK] ALL TESTS PASSED!")
    print("Sentinel Corporation is operational and ready for use.")
else:
    print(f"\n[WARN] {tests_failed} test(s) failed.")
    print("Review failures above and address issues before production use.")

print("\n" + "=" * 80)
print("End-to-End Test Complete")
print("=" * 80 + "\n")
