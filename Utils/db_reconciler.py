"""
Database Reconciler - Sync portfolio_positions with Alpaca reality

This utility prevents stale database records from accumulating by:
1. Comparing database OPEN/PENDING positions against Alpaca's actual positions
2. Closing any database records for positions that no longer exist in Alpaca
3. Logging discrepancies for investigation

Should be run:
1. At the start of each automated trading session (BEFORE compliance checks)
2. On-demand when investigating sync issues
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import logging
import sqlite3
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from alpaca.trading.client import TradingClient
from config import APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DBReconciler')


class DBReconciler:
    """Reconciles database records with Alpaca reality."""

    def __init__(self, db_path: str = "sentinel.db"):
        """Initialize with database and Alpaca client."""
        self.db_path = db_path
        is_paper = 'paper' in APCA_API_BASE_URL.lower()
        self.trading_client = TradingClient(
            APCA_API_KEY_ID,
            APCA_API_SECRET_KEY,
            paper=is_paper
        )
        logger.info(f"DBReconciler initialized ({'paper' if is_paper else 'LIVE'} trading)")

    def get_alpaca_positions(self) -> Dict[str, Dict]:
        """Get all current positions from Alpaca."""
        try:
            positions = self.trading_client.get_all_positions()
            result = {}
            for pos in positions:
                result[pos.symbol] = {
                    'symbol': pos.symbol,
                    'qty': float(pos.qty),
                    'avg_entry_price': float(pos.avg_entry_price),
                    'current_price': float(pos.current_price),
                    'market_value': float(pos.market_value),
                    'unrealized_pl': float(pos.unrealized_pl),
                    'side': str(pos.side)
                }
            return result
        except Exception as e:
            logger.error(f"Failed to get positions from Alpaca: {e}")
            return {}

    def get_database_open_positions(self) -> List[Dict]:
        """Get all OPEN/PENDING positions from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, ticker, status, actual_shares, actual_entry_price, total_risk, created_at
            FROM portfolio_positions
            WHERE status IN ('OPEN', 'PENDING')
            ORDER BY ticker
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'id': row[0],
                'ticker': row[1],
                'status': row[2],
                'shares': row[3],
                'entry_price': row[4],
                'total_risk': row[5],
                'created_at': row[6]
            }
            for row in rows
        ]

    def reconcile(self, dry_run: bool = False) -> Dict:
        """
        Reconcile database with Alpaca positions.

        Args:
            dry_run: If True, report what would be done without making changes

        Returns:
            Dictionary with reconciliation results
        """
        results = {
            'alpaca_positions': 0,
            'db_open_positions': 0,
            'stale_closed': 0,
            'in_sync': 0,
            'orphan_alpaca': [],  # Alpaca positions not in database
            'stale_records': [],  # DB records not in Alpaca
            'errors': []
        }

        # Get both sides
        alpaca_positions = self.get_alpaca_positions()
        db_positions = self.get_database_open_positions()

        results['alpaca_positions'] = len(alpaca_positions)
        results['db_open_positions'] = len(db_positions)

        logger.info(f"Alpaca positions: {len(alpaca_positions)}")
        logger.info(f"Database OPEN/PENDING: {len(db_positions)}")

        alpaca_tickers = set(alpaca_positions.keys())
        db_tickers = set(pos['ticker'] for pos in db_positions)

        # Find stale records (in DB but not in Alpaca)
        stale_tickers = db_tickers - alpaca_tickers
        for pos in db_positions:
            if pos['ticker'] in stale_tickers:
                results['stale_records'].append(pos)

        # Find orphan Alpaca positions (in Alpaca but not in DB)
        orphan_tickers = alpaca_tickers - db_tickers
        for ticker in orphan_tickers:
            results['orphan_alpaca'].append(alpaca_positions[ticker])

        # Count in-sync positions
        results['in_sync'] = len(alpaca_tickers & db_tickers)

        if results['stale_records']:
            logger.warning(f"Found {len(results['stale_records'])} stale DB records to close")
            for pos in results['stale_records']:
                logger.warning(f"  - {pos['ticker']}: {pos['status']} (created {pos['created_at']})")

        if results['orphan_alpaca']:
            logger.info(f"Found {len(results['orphan_alpaca'])} Alpaca positions not in DB")
            for pos in results['orphan_alpaca']:
                logger.info(f"  - {pos['symbol']}: {pos['qty']} shares @ ${pos['avg_entry_price']:.2f}")

        # Close stale records (unless dry run)
        if not dry_run and results['stale_records']:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for pos in results['stale_records']:
                try:
                    cursor.execute("""
                        UPDATE portfolio_positions
                        SET status = 'CLOSED',
                            exit_reason = 'RECONCILIATION_CLEANUP',
                            updated_at = datetime('now')
                        WHERE id = ?
                    """, (pos['id'],))
                    results['stale_closed'] += 1
                    logger.info(f"Closed stale record: {pos['ticker']} (ID: {pos['id']})")
                except Exception as e:
                    error_msg = f"Error closing {pos['ticker']}: {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)

            conn.commit()
            conn.close()

        return results

    def get_risk_summary(self) -> Dict:
        """Get current portfolio risk from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as count,
                COALESCE(SUM(total_risk), 0) as total_risk
            FROM portfolio_positions
            WHERE status IN ('OPEN', 'PENDING')
        """)

        row = cursor.fetchone()
        conn.close()

        return {
            'open_positions': row[0],
            'total_risk': row[1]
        }

    def generate_report(self, results: Dict = None) -> str:
        """Generate a human-readable reconciliation report."""
        if results is None:
            results = self.reconcile(dry_run=True)

        risk = self.get_risk_summary()

        lines = [
            "=" * 60,
            "DATABASE RECONCILIATION REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            "POSITION COUNTS:",
            f"  Alpaca (actual):     {results['alpaca_positions']}",
            f"  Database (tracked):  {results['db_open_positions']}",
            f"  In Sync:             {results['in_sync']}",
            "",
            f"STALE RECORDS (DB only): {len(results['stale_records'])}",
        ]

        if results['stale_records']:
            for pos in results['stale_records']:
                lines.append(f"  - {pos['ticker']}: risk=${pos['total_risk']:.2f}")

        lines.extend([
            "",
            f"ORPHAN POSITIONS (Alpaca only): {len(results['orphan_alpaca'])}",
        ])

        if results['orphan_alpaca']:
            for pos in results['orphan_alpaca']:
                lines.append(f"  - {pos['symbol']}: {pos['qty']:.0f} shares")

        lines.extend([
            "",
            "PORTFOLIO RISK (from DB):",
            f"  Open Positions:  {risk['open_positions']}",
            f"  Total Risk:      ${risk['total_risk']:.2f}",
            "",
        ])

        # Sync status
        if len(results['stale_records']) == 0 and len(results['orphan_alpaca']) == 0:
            lines.append("STATUS: DATABASE IN SYNC WITH ALPACA")
        else:
            lines.append("STATUS: RECONCILIATION NEEDED")
            if results.get('stale_closed', 0) > 0:
                lines.append(f"  Stale records closed: {results['stale_closed']}")

        lines.extend(["", "=" * 60])

        return "\n".join(lines)


def main():
    """Run reconciler from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Database Reconciler - Sync with Alpaca')
    parser.add_argument('--check', action='store_true', help='Check status (dry run)')
    parser.add_argument('--fix', action='store_true', help='Fix stale records')
    parser.add_argument('--report', action='store_true', help='Show detailed report')

    args = parser.parse_args()

    reconciler = DBReconciler()

    if args.fix:
        print("\nReconciling database with Alpaca...")
        results = reconciler.reconcile(dry_run=False)
        print(reconciler.generate_report(results))
    elif args.check or args.report:
        print(reconciler.generate_report())
    else:
        # Default: show report
        print(reconciler.generate_report())


if __name__ == "__main__":
    main()
