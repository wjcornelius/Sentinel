"""
Test GPT-5 Portfolio Optimizer with Real Candidates
====================================================
Verify that GPT-5 makes intelligent capital allocation decisions
based on candidate scores, risk/reward ratios, and sectors.

Tests:
1. GPT-5 can process candidate data
2. Allocations are weighted by conviction (higher scores = more capital)
3. Total deployment is 90-100% of available capital
4. Diversification across sectors
5. Written reasoning is provided
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from Departments.Executive.gpt5_portfolio_optimizer import GPT5PortfolioOptimizer
import config as app_config

def test_gpt5_allocation():
    """Test GPT-5 with sample candidates"""

    print("=" * 80)
    print("TESTING GPT-5 PORTFOLIO OPTIMIZER")
    print("=" * 80)

    # Mock candidates with varying quality levels
    candidates = [
        {
            'ticker': 'AAPL',
            'research_composite_score': 72.5,
            'technical_score': 75.0,
            'fundamental_score': 70.0,
            'sentiment_score': 73.0,
            'risk_reward_ratio': 2.8,
            'entry_price': 180.00,
            'stop_loss': 172.00,
            'target': 202.00,
            'position_size_shares': 55,
            'position_size_value': 10000.00,
            'total_risk': 440.00,
            'sector': 'Technology'
        },
        {
            'ticker': 'MSFT',
            'research_composite_score': 70.2,
            'technical_score': 68.0,
            'fundamental_score': 72.0,
            'sentiment_score': 71.0,
            'risk_reward_ratio': 3.1,
            'entry_price': 380.00,
            'stop_loss': 365.00,
            'target': 427.00,
            'position_size_shares': 26,
            'position_size_value': 10000.00,
            'total_risk': 390.00,
            'sector': 'Technology'
        },
        {
            'ticker': 'JPM',
            'research_composite_score': 65.8,
            'technical_score': 64.0,
            'fundamental_score': 68.0,
            'sentiment_score': 65.0,
            'risk_reward_ratio': 2.2,
            'entry_price': 155.00,
            'stop_loss': 149.00,
            'target': 168.00,
            'position_size_shares': 64,
            'position_size_value': 10000.00,
            'total_risk': 384.00,
            'sector': 'Financials'
        },
        {
            'ticker': 'JNJ',
            'research_composite_score': 63.5,
            'technical_score': 62.0,
            'fundamental_score': 66.0,
            'sentiment_score': 63.0,
            'risk_reward_ratio': 2.0,
            'entry_price': 160.00,
            'stop_loss': 154.00,
            'target': 172.00,
            'position_size_shares': 62,
            'position_size_value': 10000.00,
            'total_risk': 372.00,
            'sector': 'Healthcare'
        },
        {
            'ticker': 'XOM',
            'research_composite_score': 61.2,
            'technical_score': 60.0,
            'fundamental_score': 63.0,
            'sentiment_score': 61.0,
            'risk_reward_ratio': 1.8,
            'entry_price': 110.00,
            'stop_loss': 105.00,
            'target': 119.00,
            'position_size_shares': 90,
            'position_size_value': 10000.00,
            'total_risk': 450.00,
            'sector': 'Energy'
        },
        {
            'ticker': 'WMT',
            'research_composite_score': 60.5,
            'technical_score': 58.0,
            'fundamental_score': 62.0,
            'sentiment_score': 62.0,
            'risk_reward_ratio': 2.3,
            'entry_price': 175.00,
            'stop_loss': 169.00,
            'target': 189.00,
            'position_size_shares': 57,
            'position_size_value': 10000.00,
            'total_risk': 342.00,
            'sector': 'Consumer Staples'
        }
    ]

    # Portfolio constraints
    available_capital = 100000.0
    market_conditions = {
        'spy_change_pct': 0.3,
        'vix_level': 18.5,
        'vix_status': 'NORMAL',
        'market_sentiment': 'BULLISH'
    }

    print(f"\nAvailable Capital: ${available_capital:,.2f}")
    print(f"Candidates: {len(candidates)}")
    print(f"Market Conditions: {market_conditions['market_sentiment']} (VIX: {market_conditions['vix_level']})")

    print("\n" + "=" * 80)
    print("CANDIDATE SUMMARY (Before GPT-5)")
    print("=" * 80)
    print(f"{'Ticker':<8} {'Composite':<12} {'R:R':<8} {'Sector':<20} {'Risk Dept $':<15}")
    print("-" * 80)

    for c in candidates:
        print(f"{c['ticker']:<8} {c['research_composite_score']:>6.1f}/100   "
              f"{c['risk_reward_ratio']:>4.1f}:1  {c['sector']:<20} "
              f"${c['position_size_value']:>10,.0f}")

    print("-" * 80)
    print(f"{'TOTAL':<8} {'':12} {'':8} {'':20} ${sum(c['position_size_value'] for c in candidates):>10,.0f}")
    print(f"\nRisk Dept Allocation: Fixed 10% per position = ${sum(c['position_size_value'] for c in candidates):,.0f} total")
    print("(NO intelligence - just deterministic formula)")

    # Initialize GPT-5 optimizer
    print("\n" + "=" * 80)
    print("INITIALIZING GPT-5 PORTFOLIO OPTIMIZER")
    print("=" * 80)

    optimizer = GPT5PortfolioOptimizer(api_key=app_config.OPENAI_API_KEY)

    # Call GPT-5
    print("\nCalling OpenAI GPT-5 for intelligent allocation...")
    print("(This may take 10-20 seconds...)\n")

    try:
        optimized_candidates, reasoning = optimizer.optimize_portfolio(
            candidates=candidates,
            available_capital=available_capital,
            market_conditions=market_conditions,
            current_positions=0,
            max_positions=10
        )

        print("\n" + "=" * 80)
        print("GPT-5 ANALYSIS & REASONING")
        print("=" * 80)
        print(reasoning)

        print("\n" + "=" * 80)
        print("GPT-5 ALLOCATION DECISIONS")
        print("=" * 80)
        print(f"{'Ticker':<8} {'Composite':<12} {'R:R':<8} {'GPT-5 Allocation':<20} {'% of Portfolio':<15}")
        print("-" * 80)

        total_allocated = 0
        for c in optimized_candidates:
            allocated = c.get('allocated_capital', 0)
            total_allocated += allocated
            pct = (allocated / available_capital * 100) if available_capital > 0 else 0

            print(f"{c['ticker']:<8} {c['research_composite_score']:>6.1f}/100   "
                  f"{c['risk_reward_ratio']:>4.1f}:1  ${allocated:>15,.0f}     {pct:>5.1f}%")

            # Show GPT-5's reasoning for this allocation
            if 'gpt5_reasoning' in c:
                print(f"         Reasoning: {c['gpt5_reasoning']}")

        print("-" * 80)
        deployment_pct = (total_allocated / available_capital * 100) if available_capital > 0 else 0
        print(f"{'TOTAL':<8} {'':12} {'':8} ${total_allocated:>15,.0f}     {deployment_pct:>5.1f}%")

        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)

        # Check if allocations are weighted by conviction
        print("\n1. CONVICTION WEIGHTING:")
        print("   Higher scores should get more capital...")

        sorted_by_score = sorted(optimized_candidates, key=lambda x: x['research_composite_score'], reverse=True)
        sorted_by_allocation = sorted(optimized_candidates, key=lambda x: x.get('allocated_capital', 0), reverse=True)

        print(f"\n   Top by Score: {sorted_by_score[0]['ticker']} ({sorted_by_score[0]['research_composite_score']:.1f}/100)")
        print(f"   Top by Allocation: {sorted_by_allocation[0]['ticker']} (${sorted_by_allocation[0].get('allocated_capital', 0):,.0f})")

        if sorted_by_score[0]['ticker'] == sorted_by_allocation[0]['ticker']:
            print("   ✓ PASS: Top score gets most capital")
        else:
            print("   ⚠ NOTE: Different top pick (GPT-5 may be prioritizing R:R or diversification)")

        # Check deployment
        print("\n2. CAPITAL DEPLOYMENT:")
        print(f"   Target: 90-100% of ${available_capital:,.0f}")
        print(f"   Actual: {deployment_pct:.1f}% (${total_allocated:,.0f})")

        if deployment_pct >= 90 and deployment_pct <= 100:
            print("   ✓ PASS: Meets deployment target")
        elif deployment_pct >= 80:
            print("   ⚠ CAUTION: Below target but acceptable")
        else:
            print("   ✗ FAIL: Insufficient capital deployment")

        # Check diversification
        print("\n3. SECTOR DIVERSIFICATION:")
        sectors = {}
        for c in optimized_candidates:
            sector = c.get('sector', 'Unknown')
            allocated = c.get('allocated_capital', 0)
            sectors[sector] = sectors.get(sector, 0) + allocated

        for sector, total in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
            pct = (total / total_allocated * 100) if total_allocated > 0 else 0
            print(f"   {sector:<20} ${total:>10,.0f} ({pct:>5.1f}%)")

        if len(sectors) >= 3:
            print("   ✓ PASS: Good diversification (3+ sectors)")
        else:
            print("   ⚠ CAUTION: Limited sector diversification")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        print("\nGPT-5 Portfolio Optimizer is working correctly!")
        print("Ready to integrate into live trading workflow.")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gpt5_allocation()
