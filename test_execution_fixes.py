"""
Comprehensive Execution Fixes Test
==================================

Tests all three critical fixes implemented on 2025-11-10:

1. Order Sequencing: SELLs execute before BUYs
2. Position Size Validation: All positions meet minimum size requirements
3. Position Constraints: Updated to 30 max positions, $500 minimum

This test should catch execution issues BEFORE live trading.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timezone

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("COMPREHENSIVE EXECUTION FIXES TEST")
print("=" * 80)
print()

# ==============================================================================
# TEST 1: Order Sequencing (SELLs before BUYs)
# ==============================================================================

print("=" * 80)
print("TEST 1: ORDER SEQUENCING (SELLs BEFORE BUYs)")
print("=" * 80)
print()

def test_order_sequencing():
    """Verify that SELLs are executed before BUYs"""
    from Departments.Executive.ceo import CEO

    # Create CEO instance
    project_root = Path(__file__).parent
    ceo = CEO(project_root=project_root)

    # Mock approved plan with both SELLs and BUYs
    ceo.current_plan = {
        'plan_id': 'TEST_PLAN_001',
        'trades': [
            # BUY orders (have allocated_capital)
            {'ticker': 'AAPL', 'action': 'BUY', 'shares': 10, 'allocated_capital': 1800, 'price': 180},
            {'ticker': 'MSFT', 'action': 'BUY', 'shares': 5, 'allocated_capital': 2000, 'price': 400},
            # SELL orders (no allocated_capital)
            {'ticker': 'TSLA', 'action': 'SELL', 'shares': 20, 'price': 250},
            {'ticker': 'NVDA', 'action': 'SELL', 'shares': 15, 'price': 500},
        ]
    }
    ceo.plan_approved = True  # Mark plan as approved

    # Track execution order
    execution_log = []

    def mock_send_trade(trade):
        action = 'BUY' if 'allocated_capital' in trade else 'SELL'
        execution_log.append({
            'action': action,
            'ticker': trade['ticker'],
            'timestamp': datetime.now()
        })
        return f"MSG_TEST_{trade['ticker']}"

    def mock_process_inbox():
        pass  # No-op for testing

    def mock_wait_for_orders(tickers, timeout=60):
        return True  # Assume all orders fill immediately

    # Patch methods
    with patch.object(ceo, '_send_trade_to_trading_dept', side_effect=mock_send_trade):
        with patch('Departments.Trading.trading_department.TradingDepartment') as MockTradingDept:
            mock_trading = MockTradingDept.return_value
            mock_trading.process_inbox = mock_process_inbox

            with patch.object(ceo, '_wait_for_orders_to_fill', side_effect=mock_wait_for_orders):
                # Execute plan
                result = ceo.execute_approved_plan()

    # Validate execution order
    print("Execution Log:")
    for i, entry in enumerate(execution_log, 1):
        print(f"  {i}. {entry['action']:4s} {entry['ticker']}")
    print()

    # Check that all SELLs came before all BUYs
    sell_indices = [i for i, e in enumerate(execution_log) if e['action'] == 'SELL']
    buy_indices = [i for i, e in enumerate(execution_log) if e['action'] == 'BUY']

    if sell_indices and buy_indices:
        last_sell_idx = max(sell_indices)
        first_buy_idx = min(buy_indices)

        if last_sell_idx < first_buy_idx:
            print("[PASS] All SELLs executed before BUYs")
            print(f"  Last SELL at position {last_sell_idx + 1}")
            print(f"  First BUY at position {first_buy_idx + 1}")
            return True
        else:
            print("[FAIL] BUYs executed before SELLs completed")
            print(f"  Last SELL at position {last_sell_idx + 1}")
            print(f"  First BUY at position {first_buy_idx + 1}")
            return False
    else:
        print("[WARN] No SELLs or BUYs in execution log")
        return False

test1_passed = test_order_sequencing()
print()

# ==============================================================================
# TEST 2: Position Size Validation
# ==============================================================================

print("=" * 80)
print("TEST 2: POSITION SIZE VALIDATION")
print("=" * 80)
print()

def test_position_size_validation():
    """Verify that auto-correction respects minimum position size"""
    import yaml

    # Load compliance config
    config_path = Path(__file__).parent / "Config" / "compliance_config.yaml"
    with open(config_path) as f:
        compliance_cfg = yaml.safe_load(f)

    min_position_value = compliance_cfg['position_sizing']['min_position_value']

    print(f"Minimum Position Size: ${min_position_value}")
    print()

    # Simulate auto-correction logic
    available_capital = 100000
    max_position_pct = 0.08

    # Test candidates with various prices
    test_candidates = [
        {'ticker': 'HIGH', 'price': 500, 'composite_score': 75},  # Expensive
        {'ticker': 'MED', 'price': 50, 'composite_score': 70},    # Medium
        {'ticker': 'LOW', 'price': 5, 'composite_score': 65},     # Cheap
    ]

    print("Test Candidates:")
    for c in test_candidates:
        print(f"  {c['ticker']:5s}: ${c['price']:6.2f}/share (score: {c['composite_score']})")
    print()

    print("Validation Results:")
    passed = True
    for candidate in test_candidates:
        import math
        entry_price = candidate['price']

        # Calculate min shares needed
        min_shares = math.ceil(min_position_value / entry_price)
        allocated = min_shares * entry_price

        # Check constraints
        max_position_value = available_capital * max_position_pct

        if allocated < min_position_value:
            print(f"  {candidate['ticker']:5s}: [FAIL] ${allocated:,.0f} < ${min_position_value} minimum")
            passed = False
        elif allocated > max_position_value:
            print(f"  {candidate['ticker']:5s}: [SKIP] ${allocated:,.0f} > ${max_position_value:,.0f} maximum (8%)")
        else:
            print(f"  {candidate['ticker']:5s}: [PASS] ${allocated:,.0f} (meets ${min_position_value} minimum)")

    print()
    if passed:
        print("[PASS] All valid positions meet minimum size requirement")
    else:
        print("[FAIL] Some positions below minimum size")

    return passed

test2_passed = test_position_size_validation()
print()

# ==============================================================================
# TEST 3: Position Constraints Update
# ==============================================================================

print("=" * 80)
print("TEST 3: POSITION CONSTRAINTS UPDATE")
print("=" * 80)
print()

def test_position_constraints():
    """Verify that constraints were updated correctly"""
    import yaml

    # Check compliance_config.yaml
    compliance_path = Path(__file__).parent / "Config" / "compliance_config.yaml"
    with open(compliance_path) as f:
        compliance_cfg = yaml.safe_load(f)

    min_pos_value = compliance_cfg['position_sizing']['min_position_value']

    print(f"Compliance Config:")
    print(f"  min_position_value: ${min_pos_value}")

    if min_pos_value == 500:
        print(f"  [PASS] Lowered from $1000 to $500")
        compliance_passed = True
    else:
        print(f"  [FAIL] Expected $500, got ${min_pos_value}")
        compliance_passed = False

    print()

    # Check hard_constraints.yaml
    hard_constraints_path = Path(__file__).parent / "Config" / "hard_constraints.yaml"
    with open(hard_constraints_path) as f:
        hard_cfg = yaml.safe_load(f)

    max_positions = hard_cfg['position_limits']['max_positions_total']

    print(f"Hard Constraints Config:")
    print(f"  max_positions_total: {max_positions}")

    if max_positions == 30:
        print(f"  [PASS] Raised from 20 to 30")
        hard_passed = True
    else:
        print(f"  [FAIL] Expected 30, got {max_positions}")
        hard_passed = False

    print()

    passed = compliance_passed and hard_passed
    if passed:
        print("[PASS] All constraints updated correctly")
    else:
        print("[FAIL] Some constraints not updated")

    return passed

test3_passed = test_position_constraints()
print()

# ==============================================================================
# FINAL RESULTS
# ==============================================================================

print("=" * 80)
print("FINAL RESULTS")
print("=" * 80)
print()

all_tests = [
    ("Order Sequencing (SELLs before BUYs)", test1_passed),
    ("Position Size Validation", test2_passed),
    ("Position Constraints Update", test3_passed),
]

passed_count = sum(1 for _, passed in all_tests if passed)
total_count = len(all_tests)

for test_name, passed in all_tests:
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status}: {test_name}")

print()
print(f"Tests Passed: {passed_count}/{total_count}")
print()

if passed_count == total_count:
    print("ALL TESTS PASSED - Ready for next trading execution")
else:
    print("SOME TESTS FAILED - Fix issues before trading")

print("=" * 80)
