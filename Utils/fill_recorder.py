"""
Fill Recorder - Sync order fill data from Alpaca to database

This utility queries Alpaca for filled orders and records them in the
trading_fills table. It also updates the trading_orders table status.

Can be run:
1. After each trading session to capture fills
2. As part of the automated trading workflow
3. On-demand to backfill historical fills
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import logging
import sqlite3
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus

from config import APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('FillRecorder')


class FillRecorder:
    """Records order fills from Alpaca to the database."""

    def __init__(self, db_path: str = "sentinel.db"):
        """Initialize with database and Alpaca client."""
        self.db_path = db_path
        is_paper = 'paper' in APCA_API_BASE_URL.lower()
        self.trading_client = TradingClient(
            APCA_API_KEY_ID,
            APCA_API_SECRET_KEY,
            paper=is_paper
        )
        logger.info(f"FillRecorder initialized ({'paper' if is_paper else 'LIVE'} trading)")

    def get_recent_alpaca_orders(self, days: int = 7, status: str = 'all') -> List[Dict]:
        """
        Get recent orders from Alpaca.

        Args:
            days: Number of days to look back
            status: 'filled', 'all', 'open', or 'closed'
        """
        try:
            if status == 'filled':
                query_status = QueryOrderStatus.CLOSED
            elif status == 'open':
                query_status = QueryOrderStatus.OPEN
            elif status == 'closed':
                query_status = QueryOrderStatus.CLOSED
            else:
                query_status = QueryOrderStatus.ALL

            after = datetime.now() - timedelta(days=days)

            orders = self.trading_client.get_orders(
                GetOrdersRequest(
                    status=query_status,
                    after=after,
                    limit=500
                )
            )

            result = []
            for order in orders:
                result.append({
                    'alpaca_order_id': str(order.id),
                    'symbol': order.symbol,
                    'side': str(order.side),
                    'qty': float(order.qty) if order.qty else 0,
                    'filled_qty': float(order.filled_qty) if order.filled_qty else 0,
                    'filled_avg_price': float(order.filled_avg_price) if order.filled_avg_price else None,
                    'status': str(order.status),
                    'order_type': str(order.order_type),
                    'time_in_force': str(order.time_in_force),
                    'submitted_at': order.submitted_at.isoformat() if order.submitted_at else None,
                    'filled_at': order.filled_at.isoformat() if order.filled_at else None,
                    'created_at': order.created_at.isoformat() if order.created_at else None
                })

            return result

        except Exception as e:
            logger.error(f"Failed to get orders from Alpaca: {e}")
            return []

    def sync_fills_to_database(self, days: int = 7) -> Dict:
        """
        Sync filled orders from Alpaca to the database.

        Returns:
            Dictionary with sync results
        """
        results = {
            'orders_checked': 0,
            'fills_recorded': 0,
            'orders_updated': 0,
            'already_recorded': 0,
            'no_match_in_db': 0,
            'errors': []
        }

        # Get filled orders from Alpaca
        alpaca_orders = self.get_recent_alpaca_orders(days=days, status='closed')
        results['orders_checked'] = len(alpaca_orders)

        logger.info(f"Found {len(alpaca_orders)} closed orders in Alpaca (last {days} days)")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for order in alpaca_orders:
            # Skip orders that aren't actually filled
            if order['status'] != 'OrderStatus.FILLED' or order['filled_qty'] == 0:
                continue

            alpaca_id = order['alpaca_order_id']

            try:
                # Find the matching order in our database
                cursor.execute("""
                    SELECT id, order_id, ticker, action, quantity, status
                    FROM trading_orders
                    WHERE alpaca_order_id = ?
                """, (alpaca_id,))

                db_order = cursor.fetchone()

                if not db_order:
                    # Order not in our database (might be from Alpaca directly)
                    results['no_match_in_db'] += 1
                    continue

                db_id, order_id, ticker, action, quantity, current_status = db_order

                # Check if fill already recorded
                cursor.execute("""
                    SELECT id FROM trading_fills
                    WHERE order_id = ?
                """, (db_id,))

                if cursor.fetchone():
                    results['already_recorded'] += 1
                    continue

                # Record the fill
                fill_price = order['filled_avg_price']
                filled_qty = int(order['filled_qty'])
                fill_timestamp = order['filled_at']

                # Calculate slippage if we have expected price
                cursor.execute("""
                    SELECT limit_price FROM trading_orders WHERE id = ?
                """, (db_id,))
                expected_price_row = cursor.fetchone()
                expected_price = expected_price_row[0] if expected_price_row and expected_price_row[0] else None

                slippage_pct = None
                slippage_flag = False
                if expected_price and fill_price:
                    slippage_pct = ((fill_price - expected_price) / expected_price) * 100
                    # Flag significant slippage (> 0.5%)
                    slippage_flag = abs(slippage_pct) > 0.5

                # Insert fill record
                cursor.execute("""
                    INSERT INTO trading_fills (
                        order_id, fill_price, quantity_filled, commission,
                        fill_timestamp, expected_price, slippage_pct, slippage_flag,
                        alpaca_fill_id, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    db_id,
                    fill_price,
                    filled_qty,
                    0.0,  # Commission (Alpaca is commission-free)
                    fill_timestamp,
                    expected_price,
                    slippage_pct,
                    slippage_flag,
                    alpaca_id  # Using order ID as fill ID
                ))

                results['fills_recorded'] += 1
                logger.info(f"Recorded fill: {ticker} {action} {filled_qty} @ ${fill_price:.2f}")

                # Update order status to FILLED
                if current_status != 'FILLED':
                    cursor.execute("""
                        UPDATE trading_orders
                        SET status = 'FILLED', updated_at = datetime('now')
                        WHERE id = ?
                    """, (db_id,))
                    results['orders_updated'] += 1
                    logger.info(f"Updated order status to FILLED: {order_id}")

            except Exception as e:
                error_msg = f"Error processing order {alpaca_id}: {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)

        conn.commit()
        conn.close()

        logger.info(f"Sync complete: {results['fills_recorded']} fills recorded, "
                   f"{results['orders_updated']} orders updated")

        return results

    def get_fill_summary(self, days: int = 30) -> Dict:
        """Get summary of recorded fills."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total fills
        cursor.execute("SELECT COUNT(*) FROM trading_fills")
        total_fills = cursor.fetchone()[0]

        # Recent fills
        cursor.execute("""
            SELECT COUNT(*) FROM trading_fills
            WHERE fill_timestamp > datetime('now', ?)
        """, (f'-{days} days',))
        recent_fills = cursor.fetchone()[0]

        # Fills by action
        cursor.execute("""
            SELECT o.action, COUNT(f.id), SUM(f.quantity_filled), AVG(f.fill_price)
            FROM trading_fills f
            JOIN trading_orders o ON f.order_id = o.id
            GROUP BY o.action
        """)
        fills_by_action = {}
        for row in cursor.fetchall():
            fills_by_action[row[0]] = {
                'count': row[1],
                'total_shares': row[2],
                'avg_price': row[3]
            }

        # Orders without fills
        cursor.execute("""
            SELECT COUNT(*) FROM trading_orders
            WHERE status = 'SUBMITTED'
            AND submitted_timestamp > datetime('now', '-30 days')
        """)
        pending_orders = cursor.fetchone()[0]

        conn.close()

        return {
            'total_fills': total_fills,
            'recent_fills': recent_fills,
            'fills_by_action': fills_by_action,
            'pending_orders': pending_orders
        }

    def generate_report(self, days: int = 30) -> str:
        """Generate a human-readable fill summary report."""
        summary = self.get_fill_summary(days)

        lines = [
            "=" * 60,
            "FILL RECORDING SUMMARY",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            f"Total Fills Recorded: {summary['total_fills']}",
            f"Fills in Last {days} Days: {summary['recent_fills']}",
            f"Pending Orders (SUBMITTED): {summary['pending_orders']}",
            "",
        ]

        if summary['fills_by_action']:
            lines.append("Fills by Action:")
            for action, data in summary['fills_by_action'].items():
                lines.append(f"  {action}: {data['count']} fills, "
                           f"{data['total_shares']:.0f} shares, "
                           f"avg ${data['avg_price']:.2f}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """Run fill recorder from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Fill Recorder - Sync Alpaca fills to database')
    parser.add_argument('--sync', action='store_true', help='Sync fills from Alpaca')
    parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')
    parser.add_argument('--report', action='store_true', help='Show fill summary report')
    parser.add_argument('--list', action='store_true', help='List recent Alpaca orders')

    args = parser.parse_args()

    recorder = FillRecorder()

    if args.list:
        print("\nRecent Alpaca Orders:")
        print("-" * 80)
        orders = recorder.get_recent_alpaca_orders(days=args.days, status='all')
        for order in orders[:20]:
            status = order['status'].replace('OrderStatus.', '')
            print(f"{order['symbol']:<6} {order['side']:<15} {order['qty']:>6.0f} @ "
                  f"${order['filled_avg_price'] or 0:>8.2f} [{status}]")
        print(f"\nTotal: {len(orders)} orders")

    if args.sync:
        print(f"\nSyncing fills from Alpaca (last {args.days} days)...")
        results = recorder.sync_fills_to_database(days=args.days)
        print(f"\nSync Results:")
        print(f"  Orders checked: {results['orders_checked']}")
        print(f"  Fills recorded: {results['fills_recorded']}")
        print(f"  Orders updated: {results['orders_updated']}")
        print(f"  Already recorded: {results['already_recorded']}")
        print(f"  No DB match: {results['no_match_in_db']}")
        if results['errors']:
            print(f"  Errors: {len(results['errors'])}")

    if args.report or (not args.sync and not args.list):
        print(recorder.generate_report(days=args.days))


if __name__ == "__main__":
    main()
