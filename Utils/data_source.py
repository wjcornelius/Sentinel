"""
Data Source Module
==================
Unified data access layer for Portfolio and Executive Departments.

This module decides where to get position/account data from:
- If ALPACA_PAPER_TRADING_ENABLED = True → Query Alpaca (GROUND TRUTH)
- If ALPACA_PAPER_TRADING_ENABLED = False → Query database (simulation mode)

This allows departments to work in both modes without code changes.

Pattern:
- Departments call this module instead of direct database queries
- This module routes to either Alpaca or database
- Database is still used for audit trail (writes continue)
"""

import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
import sqlite3

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from Utils.alpaca_client import create_alpaca_client
from Utils.position_provider import create_position_provider


class DataSource:
    """
    Unified data source that routes queries to either Alpaca or database.
    """

    def __init__(self, db_path: str = "sentinel.db"):
        """
        Initialize data source.

        Args:
            db_path: Path to SQLite database (used for simulation mode and audit trail)
        """
        self.db_path = db_path
        self.alpaca_enabled = getattr(config, 'ALPACA_PAPER_TRADING_ENABLED', False)

        # Initialize Alpaca client if enabled
        self.alpaca_client = None
        self.position_provider = None

        if self.alpaca_enabled:
            try:
                self.alpaca_client = create_alpaca_client()
                if self.alpaca_client.is_connected():
                    self.position_provider = create_position_provider(self.alpaca_client)
                    print(f"[DataSource] Connected to Alpaca - using as GROUND TRUTH")
                else:
                    print(f"[DataSource] WARNING: Alpaca enabled but not connected - falling back to database")
                    self.alpaca_enabled = False
            except Exception as e:
                print(f"[DataSource] WARNING: Failed to connect to Alpaca: {e}")
                print(f"[DataSource] Falling back to database mode")
                self.alpaca_enabled = False
        else:
            print(f"[DataSource] Alpaca disabled - using database (simulation mode)")

    # =========================================================================
    # POSITION QUERIES (route to Alpaca or database)
    # =========================================================================

    def get_open_positions(self) -> List[Dict]:
        """
        Get all open positions.

        Returns same structure as database query:
            SELECT * FROM portfolio_positions WHERE status='OPEN'

        Returns:
            list: List of position dicts
        """
        if self.alpaca_enabled and self.position_provider:
            # Query Alpaca (GROUND TRUTH)
            return self.position_provider.get_open_positions()
        else:
            # Query database (simulation mode)
            return self._get_open_positions_from_db()

    def get_position_count(self) -> int:
        """
        Get count of open/pending positions.

        Returns same result as:
            SELECT COUNT(*) FROM portfolio_positions WHERE status IN ('OPEN', 'PENDING')

        Returns:
            int: Number of positions
        """
        if self.alpaca_enabled and self.position_provider:
            # Query Alpaca (GROUND TRUTH)
            return self.position_provider.get_position_count()
        else:
            # Query database (simulation mode)
            return self._get_position_count_from_db()

    def get_open_tickers(self) -> List[str]:
        """
        Get list of tickers for open/pending positions.

        Returns same result as:
            SELECT ticker FROM portfolio_positions WHERE status IN ('OPEN', 'PENDING')

        Returns:
            list: List of ticker symbols
        """
        if self.alpaca_enabled and self.position_provider:
            # Query Alpaca (GROUND TRUTH)
            return self.position_provider.get_open_position_tickers()
        else:
            # Query database (simulation mode)
            return self._get_open_tickers_from_db()

    def get_deployed_capital(self) -> float:
        """
        Get total capital deployed in open positions.

        Returns:
            float: Total market value of positions
        """
        if self.alpaca_enabled and self.position_provider:
            # Query Alpaca (GROUND TRUTH)
            return self.position_provider.get_total_market_value()
        else:
            # Query database (simulation mode)
            return self._get_deployed_capital_from_db()

    def has_position(self, ticker: str) -> bool:
        """
        Check if position exists for ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            bool: True if position exists
        """
        if self.alpaca_enabled and self.position_provider:
            # Query Alpaca (GROUND TRUTH)
            return self.position_provider.has_position(ticker)
        else:
            # Query database (simulation mode)
            return self._has_position_in_db(ticker)

    def get_position_by_ticker(self, ticker: str) -> Optional[Dict]:
        """
        Get specific position by ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            dict: Position dict or None
        """
        if self.alpaca_enabled and self.position_provider:
            # Query Alpaca (GROUND TRUTH)
            return self.position_provider.get_position_by_ticker(ticker)
        else:
            # Query database (simulation mode)
            return self._get_position_by_ticker_from_db(ticker)

    # =========================================================================
    # ACCOUNT QUERIES (route to Alpaca or database)
    # =========================================================================

    def get_account_balance(self) -> float:
        """
        Get current account cash balance.

        Returns:
            float: Available cash
        """
        if self.alpaca_enabled and self.alpaca_client:
            # Query Alpaca (GROUND TRUTH)
            account = self.alpaca_client.get_account_info()
            return account['cash'] if account else 0.0
        else:
            # Query database (simulation mode)
            return self._get_account_balance_from_db()

    def get_buying_power(self) -> float:
        """
        Get current buying power (includes margin).

        Returns:
            float: Total buying power
        """
        if self.alpaca_enabled and self.alpaca_client:
            # Query Alpaca (GROUND TRUTH)
            account = self.alpaca_client.get_account_info()
            return account['buying_power'] if account else 0.0
        else:
            # Query database (simulation mode - assume no margin)
            return self._get_account_balance_from_db()

    def get_portfolio_value(self) -> float:
        """
        Get total portfolio value (cash + positions).

        Returns:
            float: Total portfolio value
        """
        if self.alpaca_enabled and self.alpaca_client:
            # Query Alpaca (GROUND TRUTH)
            account = self.alpaca_client.get_account_info()
            return account['portfolio_value'] if account else 0.0
        else:
            # Query database (simulation mode)
            cash = self._get_account_balance_from_db()
            positions_value = self._get_deployed_capital_from_db()
            return cash + positions_value

    # =========================================================================
    # DATABASE FALLBACK METHODS (used when Alpaca disabled)
    # =========================================================================

    def _get_open_positions_from_db(self) -> List[Dict]:
        """Get open positions from database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM portfolio_positions
                WHERE status = 'OPEN'
                ORDER BY created_at DESC
            """)

            positions = [dict(row) for row in cursor.fetchall()]
            conn.close()

            return positions

        except Exception as e:
            print(f"[DataSource] Error getting positions from database: {e}")
            return []

    def _get_position_count_from_db(self) -> int:
        """Get position count from database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) FROM portfolio_positions
                WHERE status IN ('PENDING', 'OPEN')
            """)

            count = cursor.fetchone()[0]
            conn.close()

            return count

        except Exception as e:
            print(f"[DataSource] Error getting position count from database: {e}")
            return 0

    def _get_open_tickers_from_db(self) -> List[str]:
        """Get open tickers from database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT ticker FROM portfolio_positions
                WHERE status IN ('PENDING', 'OPEN')
                ORDER BY ticker
            """)

            tickers = [row[0] for row in cursor.fetchall()]
            conn.close()

            return tickers

        except Exception as e:
            print(f"[DataSource] Error getting tickers from database: {e}")
            return []

    def _get_deployed_capital_from_db(self) -> float:
        """Get deployed capital from database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT SUM(intended_shares * intended_entry_price) as deployed
                FROM portfolio_positions
                WHERE status IN ('PENDING', 'OPEN')
            """)

            result = cursor.fetchone()[0]
            conn.close()

            return result if result else 0.0

        except Exception as e:
            print(f"[DataSource] Error getting deployed capital from database: {e}")
            return 0.0

    def _has_position_in_db(self, ticker: str) -> bool:
        """Check if position exists in database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) FROM portfolio_positions
                WHERE ticker = ? AND status IN ('PENDING', 'OPEN')
            """, (ticker.upper(),))

            count = cursor.fetchone()[0]
            conn.close()

            return count > 0

        except Exception as e:
            print(f"[DataSource] Error checking position in database: {e}")
            return False

    def _get_position_by_ticker_from_db(self, ticker: str) -> Optional[Dict]:
        """Get position by ticker from database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM portfolio_positions
                WHERE ticker = ? AND status IN ('PENDING', 'OPEN')
                ORDER BY created_at DESC
                LIMIT 1
            """, (ticker.upper(),))

            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else None

        except Exception as e:
            print(f"[DataSource] Error getting position from database: {e}")
            return None

    def _get_account_balance_from_db(self) -> float:
        """Get account balance from database (simulation mode)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT cash_balance FROM account_snapshots
                ORDER BY created_at DESC
                LIMIT 1
            """)

            result = cursor.fetchone()
            conn.close()

            return result[0] if result else 100000.0  # Default $100K if no snapshot

        except Exception as e:
            print(f"[DataSource] Error getting account balance from database: {e}")
            return 100000.0  # Default

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def is_using_alpaca(self) -> bool:
        """Check if currently using Alpaca as data source."""
        return self.alpaca_enabled and self.position_provider is not None

    def get_data_source_info(self) -> Dict:
        """
        Get information about current data source.

        Returns:
            dict: Data source information
        """
        return {
            'alpaca_enabled': self.alpaca_enabled,
            'using_alpaca': self.is_using_alpaca(),
            'data_source': 'Alpaca (GROUND TRUTH)' if self.is_using_alpaca() else 'Database (simulation)',
            'alpaca_connected': self.alpaca_client.is_connected() if self.alpaca_client else False,
        }


# Convenience function
def create_data_source(db_path: str = "sentinel.db") -> DataSource:
    """
    Create a data source instance.

    Args:
        db_path: Path to SQLite database

    Returns:
        DataSource instance
    """
    return DataSource(db_path=db_path)


if __name__ == "__main__":
    # Test the data source
    print("=" * 80)
    print("DATA SOURCE MODULE TEST")
    print("=" * 80)
    print()

    try:
        # Create data source
        ds = create_data_source()

        # Show data source info
        info = ds.get_data_source_info()
        print("Data Source Information:")
        print(f"  Alpaca Enabled:  {info['alpaca_enabled']}")
        print(f"  Using Alpaca:    {info['using_alpaca']}")
        print(f"  Data Source:     {info['data_source']}")
        print(f"  Alpaca Connected: {info['alpaca_connected']}")
        print()

        # Test position queries
        print("Testing position queries...")
        position_count = ds.get_position_count()
        open_tickers = ds.get_open_tickers()
        deployed_capital = ds.get_deployed_capital()

        print(f"  Position Count:   {position_count}")
        print(f"  Open Tickers:     {open_tickers}")
        print(f"  Deployed Capital: ${deployed_capital:,.2f}")
        print()

        # Test account queries
        print("Testing account queries...")
        cash = ds.get_account_balance()
        buying_power = ds.get_buying_power()
        portfolio_value = ds.get_portfolio_value()

        print(f"  Cash Balance:     ${cash:,.2f}")
        print(f"  Buying Power:     ${buying_power:,.2f}")
        print(f"  Portfolio Value:  ${portfolio_value:,.2f}")
        print()

        print("=" * 80)
        print("[SUCCESS] Data Source test completed successfully")
        print("=" * 80)

    except Exception as e:
        print()
        print("=" * 80)
        print(f"[ERROR] Error: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
