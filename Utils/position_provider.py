"""
Position Provider Module
=========================
Provides position data from Alpaca in database-compatible format.

This is a compatibility layer that allows existing code to work with Alpaca as ground truth
without requiring complete refactoring of Portfolio and Executive Departments.

Pattern:
- Query Alpaca for current positions (GROUND TRUTH)
- Return data in same format as database queries
- Database is still used for audit trail (writes continue)
"""

import os
import sys
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.alpaca_client import AlpacaClient
import config


class PositionProvider:
    """
    Provides position data from Alpaca (ground truth) in database-compatible format.
    """

    def __init__(self, alpaca_client: AlpacaClient):
        """
        Initialize Position Provider.

        Args:
            alpaca_client: AlpacaClient instance
        """
        self.alpaca = alpaca_client

    def get_open_positions(self) -> List[Dict]:
        """
        Get open positions from Alpaca in database-compatible format.

        Returns same structure as:
            SELECT ticker, actual_shares, actual_entry_price, ... FROM portfolio_positions WHERE status='OPEN'

        Returns:
            list: List of position dicts with database-compatible keys
        """
        try:
            # Query Alpaca (GROUND TRUTH)
            alpaca_positions = self.alpaca.get_current_positions()

            # Convert to database-compatible format
            positions = []
            for pos in alpaca_positions:
                positions.append({
                    'ticker': pos.symbol,
                    'actual_shares': float(pos.qty),
                    'actual_entry_price': float(pos.avg_entry_price),
                    'current_price': float(pos.current_price),
                    'market_value': float(pos.market_value),
                    'cost_basis': float(pos.cost_basis),
                    'unrealized_pl': float(pos.unrealized_pl),
                    'unrealized_plpc': float(pos.unrealized_plpc),
                    'status': 'OPEN',  # All Alpaca positions are open by definition
                    'side': pos.side,  # 'long' or 'short'
                })

            return positions

        except Exception as e:
            print(f"Error getting positions from Alpaca: {e}")
            return []

    def get_open_position_tickers(self) -> List[str]:
        """
        Get list of tickers for open positions.

        Returns same structure as:
            SELECT ticker FROM portfolio_positions WHERE status='OPEN'

        Returns:
            list: List of ticker symbols
        """
        positions = self.get_open_positions()
        return [pos['ticker'] for pos in positions]

    def get_position_count(self) -> int:
        """
        Get count of open positions.

        Returns same structure as:
            SELECT COUNT(*) FROM portfolio_positions WHERE status='OPEN'

        Returns:
            int: Number of open positions
        """
        positions = self.get_open_positions()
        return len(positions)

    def get_position_by_ticker(self, ticker: str) -> Optional[Dict]:
        """
        Get specific position by ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            dict: Position dict or None if not found
        """
        positions = self.get_open_positions()
        for pos in positions:
            if pos['ticker'].upper() == ticker.upper():
                return pos
        return None

    def has_position(self, ticker: str) -> bool:
        """
        Check if position exists for ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            bool: True if position exists
        """
        return self.get_position_by_ticker(ticker) is not None

    def get_total_market_value(self) -> float:
        """
        Get total market value of all positions.

        Returns:
            float: Total market value
        """
        positions = self.get_open_positions()
        return sum(pos['market_value'] for pos in positions)

    def get_total_cost_basis(self) -> float:
        """
        Get total cost basis of all positions.

        Returns:
            float: Total cost basis
        """
        positions = self.get_open_positions()
        return sum(pos['cost_basis'] for pos in positions)

    def get_total_unrealized_pl(self) -> float:
        """
        Get total unrealized P&L across all positions.

        Returns:
            float: Total unrealized P&L
        """
        positions = self.get_open_positions()
        return sum(pos['unrealized_pl'] for pos in positions)

    def get_account_summary(self) -> Dict:
        """
        Get account summary from Alpaca (GROUND TRUTH).

        Returns same structure as database account queries.

        Returns:
            dict: Account summary
        """
        try:
            # Query Alpaca (GROUND TRUTH)
            account = self.alpaca.get_account_info()

            return {
                'portfolio_value': account['portfolio_value'],
                'equity': account['equity'],
                'cash': account['cash'],
                'buying_power': account['buying_power'],
                'long_market_value': account['long_market_value'],
                'short_market_value': account['short_market_value'],
                'initial_margin': account['initial_margin'],
                'maintenance_margin': account['maintenance_margin'],
                'daytrade_count': account['daytrade_count'],
                'pattern_day_trader': account['pattern_day_trader'],
            }

        except Exception as e:
            print(f"Error getting account info from Alpaca: {e}")
            return None


# Convenience functions for easy import
def create_position_provider(alpaca_client: AlpacaClient) -> PositionProvider:
    """
    Create a PositionProvider instance.

    Args:
        alpaca_client: AlpacaClient instance

    Returns:
        PositionProvider instance
    """
    return PositionProvider(alpaca_client)


if __name__ == "__main__":
    # Test the position provider
    print("=" * 80)
    print("POSITION PROVIDER MODULE TEST")
    print("=" * 80)
    print()

    try:
        from Utils.alpaca_client import create_alpaca_client

        # Create Alpaca client
        print("Connecting to Alpaca...")
        alpaca = create_alpaca_client()

        if not alpaca.is_connected():
            print("[ERROR] Not connected to Alpaca. Check API keys in config.py")
            sys.exit(1)

        print("[OK] Connected to Alpaca")
        print()

        # Create position provider
        provider = create_position_provider(alpaca)

        # Test getting open positions
        print("Getting open positions (from Alpaca)...")
        positions = provider.get_open_positions()

        if positions:
            print(f"  Found {len(positions)} position(s):")
            for pos in positions:
                print(f"    {pos['ticker']}: {pos['actual_shares']} shares @ ${pos['actual_entry_price']:.2f}")
                print(f"      Current: ${pos['current_price']:.2f} | P&L: ${pos['unrealized_pl']:.2f} ({pos['unrealized_plpc']*100:.2f}%)")
        else:
            print("  No positions found (empty portfolio)")
        print()

        # Test getting position count
        count = provider.get_position_count()
        print(f"Position Count: {count}")
        print()

        # Test getting tickers
        tickers = provider.get_open_position_tickers()
        print(f"Open Tickers: {tickers}")
        print()

        # Test getting account summary
        print("Getting account summary (from Alpaca)...")
        account = provider.get_account_summary()
        if account:
            print(f"  Portfolio Value:  ${account['portfolio_value']:,.2f}")
            print(f"  Cash:             ${account['cash']:,.2f}")
            print(f"  Buying Power:     ${account['buying_power']:,.2f}")
            print(f"  Total Market Val: ${provider.get_total_market_value():,.2f}")
            print(f"  Total Cost Basis: ${provider.get_total_cost_basis():,.2f}")
            print(f"  Total Unrealized: ${provider.get_total_unrealized_pl():,.2f}")
        print()

        # Test specific position lookup
        if tickers:
            test_ticker = tickers[0]
            print(f"Testing position lookup for {test_ticker}...")
            pos = provider.get_position_by_ticker(test_ticker)
            if pos:
                print(f"  [OK] Found: {pos['ticker']} - {pos['actual_shares']} shares")
            print()

            print(f"Testing has_position for {test_ticker}...")
            has_pos = provider.has_position(test_ticker)
            print(f"  Result: {has_pos}")
            print()

        print("=" * 80)
        print("[SUCCESS] All tests passed! Position Provider working correctly")
        print("=" * 80)

    except Exception as e:
        print()
        print("=" * 80)
        print(f"[ERROR] Error: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
