"""
Test Ticker Universe Loading
=============================
Verify that ResearchDepartment loads the full 515-stock universe.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from Departments.Research.research_department import ResearchDepartment
import yaml
import config as app_config

def test_universe():
    print("=" * 80)
    print("TESTING TICKER UNIVERSE LOADING")
    print("=" * 80)

    # Load config
    config_path = Path(__file__).parent / "Config" / "research_config.yaml"
    with open(config_path, 'r') as f:
        research_config = yaml.safe_load(f)

    # Get API key
    perplexity_api_key = app_config.PERPLEXITY_API_KEY

    # Database path
    db_path = Path(__file__).parent / "sentinel.db"

    # Initialize Research Department
    print("\nInitializing Research Department...")
    research = ResearchDepartment(research_config, perplexity_api_key, db_path)

    # Get ticker universe
    print("\nCalling get_ticker_universe()...")
    universe = research.get_ticker_universe()

    print(f"\nUniverse size: {len(universe)} stocks")
    print(f"\nFirst 20 tickers: {', '.join(universe[:20])}")
    print(f"Last 20 tickers: {', '.join(universe[-20:])}")

    # Check for expected overlap stocks
    expected_stocks = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'JPM', 'BAC']
    found = [s for s in expected_stocks if s in universe]
    print(f"\nExpected stocks found: {len(found)}/{len(expected_stocks)}")
    print(f"  Found: {', '.join(found)}")

    if len(universe) >= 500:
        print("\n" + "=" * 80)
        print("SUCCESS: Full 515-stock universe loaded!")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print(f"WARNING: Only {len(universe)} stocks loaded (expected ~515)")
        print("=" * 80)

if __name__ == "__main__":
    test_universe()
