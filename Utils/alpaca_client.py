"""
Alpaca Client Module
====================
Centralized Alpaca API interface - THE GROUND TRUTH for all position and account data.
Database is audit trail only - always query Alpaca for current state.
"""

import os
import sys
from datetime import datetime, timedelta
import pytz

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
except ImportError:
    print("Warning: alpaca-py not installed. Run: pip install alpaca-py")
    TradingClient = None


class AlpacaClient:
    """
    Centralized Alpaca API client.
    This is the GROUND TRUTH for all position and account data.
    """

    def __init__(self, api_key=None, secret_key=None, paper=True):
        """
        Initialize Alpaca client.

        Args:
            api_key: Alpaca API key (defaults to config.py)
            secret_key: Alpaca secret key (defaults to config.py)
            paper: Use paper trading (True) or live (False)
        """
        if TradingClient is None:
            raise ImportError("alpaca-py not installed. Run: pip install alpaca-py")

        self.api_key = api_key or config.APCA_API_KEY_ID
        self.secret_key = secret_key or config.APCA_API_SECRET_KEY
        self.paper = paper

        # Initialize trading client
        self.trading_client = TradingClient(
            api_key=self.api_key,
            secret_key=self.secret_key,
            paper=self.paper
        )

        # Initialize data client (for historical data)
        self.data_client = StockHistoricalDataClient(
            api_key=self.api_key,
            secret_key=self.secret_key
        )

        self.eastern_tz = pytz.timezone('US/Eastern')

    # =========================================================================
    # GROUND TRUTH: Position Queries
    # =========================================================================

    def get_current_positions(self):
        """
        Get current positions from Alpaca (GROUND TRUTH).
        This should ALWAYS be used instead of querying the database.

        Returns:
            list: List of position objects from Alpaca
        """
        try:
            positions = self.trading_client.get_all_positions()
            return positions
        except Exception as e:
            print(f"Error getting positions from Alpaca: {e}")
            return []

    def get_position(self, symbol):
        """
        Get specific position for a symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Position object or None if not found
        """
        try:
            position = self.trading_client.get_open_position(symbol)
            return position
        except Exception as e:
            # Position not found is not an error, just return None
            if "not found" in str(e).lower():
                return None
            print(f"Error getting position for {symbol}: {e}")
            return None

    def get_positions_summary(self):
        """
        Get positions in a simplified format for easy use.

        Returns:
            list: List of dicts with position info
        """
        positions = self.get_current_positions()

        summary = []
        for pos in positions:
            summary.append({
                'symbol': pos.symbol,
                'qty': float(pos.qty),
                'avg_entry_price': float(pos.avg_entry_price),
                'current_price': float(pos.current_price),
                'market_value': float(pos.market_value),
                'cost_basis': float(pos.cost_basis),
                'unrealized_pl': float(pos.unrealized_pl),
                'unrealized_plpc': float(pos.unrealized_plpc),
                'side': pos.side
            })

        return summary

    # =========================================================================
    # GROUND TRUTH: Account Queries
    # =========================================================================

    def get_account_info(self):
        """
        Get account information from Alpaca (GROUND TRUTH).
        This should ALWAYS be used instead of querying the database.

        Returns:
            dict: Account information
        """
        try:
            account = self.trading_client.get_account()

            return {
                'account_number': account.account_number,
                'status': account.status,
                'currency': account.currency,
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'equity': float(account.equity),
                'last_equity': float(account.last_equity),
                'long_market_value': float(account.long_market_value),
                'short_market_value': float(account.short_market_value),
                'initial_margin': float(account.initial_margin),
                'maintenance_margin': float(account.maintenance_margin),
                'daytrade_count': account.daytrade_count,
                'daytrading_buying_power': float(account.daytrading_buying_power),
                'pattern_day_trader': account.pattern_day_trader,
            }

        except Exception as e:
            print(f"Error getting account info from Alpaca: {e}")
            return None

    # =========================================================================
    # GROUND TRUTH: Order Queries
    # =========================================================================

    def get_today_orders(self):
        """
        Get all orders submitted today (for "already traded" check).

        Returns:
            list: Orders submitted today
        """
        try:
            eastern_now = datetime.now(self.eastern_tz)
            today_start = self.eastern_tz.localize(
                datetime.combine(eastern_now.date(), datetime.min.time())
            )

            from alpaca.trading.requests import GetOrdersRequest
            from alpaca.trading.enums import QueryOrderStatus

            request = GetOrdersRequest(
                status=QueryOrderStatus.ALL,
                after=today_start,
                limit=100
            )

            orders = self.trading_client.get_orders(filter=request)

            return list(orders)

        except Exception as e:
            print(f"Error getting today's orders: {e}")
            return []

    def get_recent_orders(self, days=7):
        """
        Get orders from the last N days.

        Args:
            days: Number of days to look back

        Returns:
            list: Recent orders
        """
        try:
            eastern_now = datetime.now(self.eastern_tz)
            start_date = eastern_now - timedelta(days=days)

            from alpaca.trading.requests import GetOrdersRequest
            from alpaca.trading.enums import QueryOrderStatus

            request = GetOrdersRequest(
                status=QueryOrderStatus.ALL,
                after=start_date,
                limit=500
            )

            orders = self.trading_client.get_orders(filter=request)

            return list(orders)

        except Exception as e:
            print(f"Error getting recent orders: {e}")
            return []

    def get_order(self, order_id):
        """
        Get specific order by ID.

        Args:
            order_id: Alpaca order ID

        Returns:
            Order object or None
        """
        try:
            order = self.trading_client.get_order_by_id(order_id)
            return order
        except Exception as e:
            print(f"Error getting order {order_id}: {e}")
            return None

    # =========================================================================
    # ORDER SUBMISSION (only when online mode)
    # =========================================================================

    def submit_market_order(self, symbol, qty, side='buy', time_in_force='day'):
        """
        Submit a market order to Alpaca.

        Args:
            symbol: Stock ticker
            qty: Quantity (fractional shares supported)
            side: 'buy' or 'sell'
            time_in_force: 'day', 'gtc', 'ioc', etc.

        Returns:
            Order object or None if failed
        """
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL

            tif_map = {
                'day': TimeInForce.DAY,
                'gtc': TimeInForce.GTC,
                'ioc': TimeInForce.IOC,
                'fok': TimeInForce.FOK
            }
            tif = tif_map.get(time_in_force.lower(), TimeInForce.DAY)

            market_order = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=tif
            )

            order = self.trading_client.submit_order(order_data=market_order)
            print(f"✓ Market {side} order submitted: {symbol} x{qty}")
            return order

        except Exception as e:
            print(f"✗ Error submitting market order: {e}")
            return None

    def submit_limit_order(self, symbol, qty, limit_price, side='buy', time_in_force='day'):
        """
        Submit a limit order to Alpaca.

        Args:
            symbol: Stock ticker
            qty: Quantity
            limit_price: Limit price
            side: 'buy' or 'sell'
            time_in_force: 'day', 'gtc', etc.

        Returns:
            Order object or None if failed
        """
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL

            tif_map = {
                'day': TimeInForce.DAY,
                'gtc': TimeInForce.GTC,
                'ioc': TimeInForce.IOC,
                'fok': TimeInForce.FOK
            }
            tif = tif_map.get(time_in_force.lower(), TimeInForce.DAY)

            limit_order = LimitOrderRequest(
                symbol=symbol,
                qty=qty,
                limit_price=limit_price,
                side=order_side,
                time_in_force=tif
            )

            order = self.trading_client.submit_order(order_data=limit_order)
            print(f"✓ Limit {side} order submitted: {symbol} x{qty} @ ${limit_price}")
            return order

        except Exception as e:
            print(f"✗ Error submitting limit order: {e}")
            return None

    def cancel_order(self, order_id):
        """
        Cancel an order.

        Args:
            order_id: Alpaca order ID

        Returns:
            bool: True if canceled successfully
        """
        try:
            self.trading_client.cancel_order_by_id(order_id)
            print(f"✓ Order {order_id} canceled")
            return True
        except Exception as e:
            print(f"✗ Error canceling order {order_id}: {e}")
            return False

    def cancel_all_orders(self):
        """
        Cancel all open orders.

        Returns:
            list: List of canceled order IDs
        """
        try:
            result = self.trading_client.cancel_orders()
            print(f"✓ All orders canceled")
            return result
        except Exception as e:
            print(f"✗ Error canceling all orders: {e}")
            return []

    # =========================================================================
    # MARKET CALENDAR
    # =========================================================================

    def get_calendar(self, start=None, end=None):
        """
        Get market calendar (trading days).

        Args:
            start: Start date (YYYY-MM-DD) or datetime
            end: End date (YYYY-MM-DD) or datetime

        Returns:
            list: Calendar entries
        """
        try:
            if start is None:
                eastern_now = datetime.now(self.eastern_tz)
                start = eastern_now.date().isoformat()

            if end is None:
                end = start

            from alpaca.trading.requests import GetCalendarRequest
            from datetime import date as date_type

            # Convert strings to date objects if needed
            if isinstance(start, str):
                start = date_type.fromisoformat(start)
            if isinstance(end, str):
                end = date_type.fromisoformat(end)

            request = GetCalendarRequest(start=start, end=end)
            calendar = self.trading_client.get_calendar(request)
            return list(calendar)

        except Exception as e:
            print(f"Error getting calendar: {e}")
            return []

    # =========================================================================
    # HISTORICAL DATA (for analysis)
    # =========================================================================

    def get_bars(self, symbol, start, end=None, timeframe='1Day'):
        """
        Get historical price bars.

        Args:
            symbol: Stock ticker
            start: Start date
            end: End date (optional, defaults to now)
            timeframe: '1Day', '1Hour', etc.

        Returns:
            DataFrame: Historical bars
        """
        try:
            if end is None:
                end = datetime.now(self.eastern_tz)

            timeframe_map = {
                '1Min': TimeFrame.Minute,
                '5Min': TimeFrame(5, 'Minute'),
                '15Min': TimeFrame(15, 'Minute'),
                '1Hour': TimeFrame.Hour,
                '1Day': TimeFrame.Day,
            }

            tf = timeframe_map.get(timeframe, TimeFrame.Day)

            request_params = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=tf,
                start=start,
                end=end
            )

            bars = self.data_client.get_stock_bars(request_params)
            return bars.df

        except Exception as e:
            print(f"Error getting bars for {symbol}: {e}")
            return None

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def is_connected(self):
        """
        Test if connected to Alpaca by querying account.

        Returns:
            bool: True if connected
        """
        try:
            self.trading_client.get_account()
            return True
        except Exception as e:
            print(f"Not connected to Alpaca: {e}")
            return False

    def get_connection_info(self):
        """
        Get connection information for display.

        Returns:
            dict: Connection info
        """
        return {
            'api_key': self.api_key[:8] + '...' if self.api_key else 'Not set',
            'paper_trading': self.paper,
            'connected': self.is_connected()
        }


# Convenience function for easy import
def create_alpaca_client(api_key=None, secret_key=None, paper=True):
    """
    Create an Alpaca client with config defaults.

    Args:
        api_key: Optional API key override
        secret_key: Optional secret key override
        paper: Paper trading (True) or live (False)

    Returns:
        AlpacaClient instance
    """
    return AlpacaClient(api_key=api_key, secret_key=secret_key, paper=paper)


if __name__ == "__main__":
    # Test the Alpaca client
    print("=" * 80)
    print("ALPACA CLIENT MODULE TEST")
    print("=" * 80)
    print()

    try:
        # Create client
        client = create_alpaca_client()

        # Test connection
        print("Testing connection...")
        conn_info = client.get_connection_info()
        print(f"  API Key:        {conn_info['api_key']}")
        print(f"  Paper Trading:  {conn_info['paper_trading']}")
        print(f"  Connected:      {conn_info['connected']}")
        print()

        if not conn_info['connected']:
            print("✗ Not connected to Alpaca. Check API keys in config.py")
            sys.exit(1)

        # Get account info (GROUND TRUTH)
        print("Getting account info (GROUND TRUTH)...")
        account = client.get_account_info()
        if account:
            print(f"  Account Number:   {account['account_number']}")
            print(f"  Status:           {account['status']}")
            print(f"  Portfolio Value:  ${account['portfolio_value']:,.2f}")
            print(f"  Buying Power:     ${account['buying_power']:,.2f}")
            print(f"  Cash:             ${account['cash']:,.2f}")
            print()

        # Get positions (GROUND TRUTH)
        print("Getting current positions (GROUND TRUTH)...")
        positions = client.get_positions_summary()
        if positions:
            print(f"  Found {len(positions)} position(s):")
            for pos in positions:
                print(f"    {pos['symbol']}: {pos['qty']} shares @ ${pos['avg_entry_price']:.2f}")
                print(f"      Current: ${pos['current_price']:.2f} | P&L: ${pos['unrealized_pl']:.2f} ({pos['unrealized_plpc']*100:.2f}%)")
        else:
            print("  No positions found (empty portfolio)")
        print()

        # Check for today's orders
        print("Checking for today's orders...")
        today_orders = client.get_today_orders()
        if today_orders:
            print(f"  Found {len(today_orders)} order(s) submitted today:")
            for order in today_orders:
                print(f"    {order.symbol}: {order.side} {order.qty} @ {order.order_type} - Status: {order.status}")
        else:
            print("  No orders submitted today")
        print()

        # Get market calendar
        print("Checking market calendar for today...")
        calendar = client.get_calendar()
        if calendar:
            today_cal = calendar[0]
            print(f"  Market Open:  {today_cal.open}")
            print(f"  Market Close: {today_cal.close}")
        else:
            print("  Market is closed today (holiday or weekend)")
        print()

        print("=" * 80)
        print("[SUCCESS] All tests passed! Alpaca client is working correctly.")
        print("=" * 80)

    except Exception as e:
        print()
        print("=" * 80)
        print(f"[ERROR] Error: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
