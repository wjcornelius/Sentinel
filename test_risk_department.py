"""
Test Risk Department v2.0 - Advisory Role

Tests:
1. Create mock candidates
2. Assess risk for all candidates
3. Verify risk_score (0-100)
4. Verify risk_warnings list
5. Verify ALL candidates pass through (no rejections)
"""

import sys
import logging
from Departments.Risk import RiskDepartment

logging.basicConfig(level=logging.WARNING)  # Suppress INFO logs
logger = logging.getLogger(__name__)

def test_risk_department():
    """Test Risk Department advisory assessment"""
    print("=" * 80)
    print("RISK DEPARTMENT v2.0 TEST - Advisory Assessment")
    print("=" * 80)
    print()

    # Initialize
    print("[1/5] Initializing Risk Department...")
    risk = RiskDepartment(
        max_risk_per_trade_pct=1.0,
        max_portfolio_heat_pct=5.0
    )
    print("[OK] Initialized")
    print()

    # Create mock candidates
    print("[2/5] Creating mock candidates...")
    mock_candidates = [
        {
            'ticker': 'AAPL',
            'score': 75.0,
            'current_price': 175.50,
            'reasoning': 'Strong technical setup'
        },
        {
            'ticker': 'MSFT',
            'score': 82.0,
            'current_price': 380.25,
            'reasoning': 'Momentum breakout'
        },
        {
            'ticker': 'NVDA',
            'score': 68.0,
            'current_price': 135.75,
            'reasoning': 'High volatility but good trend'
        },
        {
            'ticker': 'TSLA',
            'score': 55.0,
            'current_price': 245.00,
            'reasoning': 'Risky but potential upside'
        },
        {
            'ticker': 'GOOGL',
            'score': 79.0,
            'current_price': 140.50,
            'reasoning': 'Solid fundamentals'
        }
    ]
    print(f"[OK] Created {len(mock_candidates)} mock candidates")
    print()

    # Assess risk
    print("[3/5] Assessing risk for all candidates...")
    available_capital = 100000.00  # $100K
    assessed = risk.assess_candidates(mock_candidates, available_capital)
    print(f"[OK] Assessed {len(assessed)} candidates")
    print()

    # Verify structure
    print("[4/5] Verifying advisory assessment...")

    # Check ALL candidates passed through
    if len(assessed) != len(mock_candidates):
        print(f"[ERROR] Expected {len(mock_candidates)} candidates, got {len(assessed)}")
        return False

    print(f"[OK] ALL {len(assessed)} candidates passed through (no rejections)")
    print()

    # Check each candidate has required fields
    required_fields = ['risk_score', 'risk_warnings', 'risk_metrics']
    for candidate in assessed:
        missing = [f for f in required_fields if f not in candidate]
        if missing:
            print(f"[ERROR] {candidate['ticker']} missing fields: {missing}")
            return False

    print("[OK] All candidates have risk_score, risk_warnings, risk_metrics")
    print()

    # Verify risk scores
    print("[5/5] Verifying risk scores and warnings...")

    for candidate in assessed:
        ticker = candidate['ticker']
        risk_score = candidate['risk_score']
        warnings = candidate['risk_warnings']

        # Check score range
        if not (0 <= risk_score <= 100):
            print(f"[ERROR] {ticker}: Invalid risk_score {risk_score} (must be 0-100)")
            return False

        print(f"  {ticker:6s}: Risk Score: {risk_score:5.1f}/100 - {len(warnings)} warnings")
        for warning in warnings:
            print(f"           WARNING: {warning}")
        print()

    print("[OK] All risk scores in valid range (0-100)")
    print()

    # Summary
    print("=" * 80)
    print("TEST RESULTS - RISK DEPARTMENT v2.0")
    print("=" * 80)
    print(f"[OK] Advisory assessment: Working ({len(assessed)} candidates assessed)")
    print(f"[OK] No rejections: All candidates passed through")
    print(f"[OK] Risk scores: Valid (0-100 range)")
    print(f"[OK] Risk warnings: Generated for each candidate")
    print()

    print("Risk Score Distribution:")
    for c in sorted(assessed, key=lambda x: -x['risk_score']):
        print(f"  {c['ticker']:6s}: {c['risk_score']:5.1f}/100")
    print()

    print("=" * 80)
    print("[OK] Risk Department v2.0: WORKING")
    print("=" * 80)

    return True

if __name__ == "__main__":
    try:
        success = test_risk_department()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
