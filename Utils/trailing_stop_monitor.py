"""
Trailing Stop Monitor

Ensures all positions have active GTC trailing stop orders for 24/7 protection.
Can be run daily or on-demand to:
1. Check which positions have active trailing stops
2. Add trailing stops to unprotected positions
3. Report on current protection status

This addresses the gap where existing positions (bought before this enhancement)
may not have trailing stop orders in place.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest, TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus

from config import APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL
from Utils.atr_calculator import calculate_trailing_stop_percent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TrailingStopMonitor')


class TrailingStopMonitor:
    """Monitor and manage trailing stop orders for all positions."""

    def __init__(self):
        """Initialize with Alpaca trading client."""
        is_paper = 'paper' in APCA_API_BASE_URL.lower()
        self.trading_client = TradingClient(
            APCA_API_KEY_ID,
            APCA_API_SECRET_KEY,
            paper=is_paper
        )
        logger.info(f"TrailingStopMonitor initialized ({'paper' if is_paper else 'LIVE'} trading)")

    def get_all_positions(self) -> List[Dict]:
        """Get all current positions from Alpaca."""
        try:
            positions = self.trading_client.get_all_positions()
            return [{
                'ticker': pos.symbol,
                'shares': float(pos.qty),
                'current_price': float(pos.current_price),
                'market_value': float(pos.market_value),
                'unrealized_pl': float(pos.unrealized_pl),
                'unrealized_pl_pct': float(pos.unrealized_plpc) * 100
            } for pos in positions]
        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            return []

    def get_open_trailing_stops(self) -> Dict[str, Dict]:
        """Get all open trailing stop orders, keyed by ticker."""
        try:
            orders_request = GetOrdersRequest(status=QueryOrderStatus.OPEN)
            all_orders = self.trading_client.get_orders(filter=orders_request)

            trailing_stops = {}
            for order in all_orders:
                if order.order_type == 'trailing_stop':
                    trailing_stops[order.symbol] = {
                        'order_id': str(order.id),
                        'qty': float(order.qty),
                        'trail_percent': float(order.trail_percent) if order.trail_percent else None,
                        'trail_price': float(order.trail_price) if order.trail_price else None,
                        'created_at': order.created_at.isoformat() if order.created_at else None
                    }

            return trailing_stops

        except Exception as e:
            logger.error(f"Failed to get trailing stop orders: {e}")
            return {}

    def check_protection_status(self) -> Dict:
        """
        Check which positions are protected by trailing stops.

        Returns:
            Dictionary with:
            - protected: List of tickers with active trailing stops
            - unprotected: List of tickers without trailing stops
            - details: Full details for each position
        """
        positions = self.get_all_positions()
        trailing_stops = self.get_open_trailing_stops()

        protected = []
        unprotected = []
        details = {}

        for pos in positions:
            ticker = pos['ticker']
            has_stop = ticker in trailing_stops

            if has_stop:
                protected.append(ticker)
                pos['trailing_stop'] = trailing_stops[ticker]
            else:
                unprotected.append(ticker)
                pos['trailing_stop'] = None

            details[ticker] = pos

        logger.info(f"Protection status: {len(protected)} protected, {len(unprotected)} unprotected")

        return {
            'protected': protected,
            'unprotected': unprotected,
            'details': details,
            'total_positions': len(positions),
            'protection_rate': len(protected) / len(positions) * 100 if positions else 0
        }

    def add_trailing_stop(self, ticker: str, shares: float, current_price: float = None) -> Tuple[bool, str]:
        """
        Add a GTC trailing stop order for a position.

        Args:
            ticker: Stock symbol
            shares: Number of shares to protect
            current_price: Current price (fetched if not provided)

        Returns:
            Tuple of (success, message)
        """
        try:
            # Calculate ATR-based trailing stop percentage
            atr_result = calculate_trailing_stop_percent(ticker, current_price)
            trail_percent = atr_result['trail_percent']

            # Submit trailing stop order
            trailing_stop_request = TrailingStopOrderRequest(
                symbol=ticker,
                qty=shares,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.GTC,
                trail_percent=trail_percent
            )

            order = self.trading_client.submit_order(trailing_stop_request)

            logger.info(f"Added trailing stop for {ticker}: {trail_percent}% (Order ID: {order.id})")
            return True, f"Added {trail_percent}% trailing stop"

        except Exception as e:
            logger.error(f"Failed to add trailing stop for {ticker}: {e}")
            return False, str(e)

    def protect_all_positions(self, dry_run: bool = True) -> Dict:
        """
        Add trailing stops to all unprotected positions.

        Args:
            dry_run: If True, only report what would be done without actually submitting orders

        Returns:
            Dictionary with results for each ticker
        """
        status = self.check_protection_status()
        results = {
            'dry_run': dry_run,
            'positions_checked': status['total_positions'],
            'already_protected': len(status['protected']),
            'newly_protected': [],
            'failed': []
        }

        if not status['unprotected']:
            logger.info("All positions already have trailing stops!")
            return results

        logger.info(f"Found {len(status['unprotected'])} unprotected positions")

        for ticker in status['unprotected']:
            pos = status['details'][ticker]
            shares = pos['shares']
            current_price = pos['current_price']

            # Calculate what trailing stop would be used
            atr_result = calculate_trailing_stop_percent(ticker, current_price)

            if dry_run:
                logger.info(
                    f"[DRY RUN] Would add {atr_result['trail_percent']}% trailing stop for "
                    f"{ticker} ({shares} shares @ ${current_price:.2f})"
                )
                results['newly_protected'].append({
                    'ticker': ticker,
                    'shares': shares,
                    'trail_percent': atr_result['trail_percent'],
                    'status': 'would_add'
                })
            else:
                success, message = self.add_trailing_stop(ticker, shares, current_price)
                if success:
                    results['newly_protected'].append({
                        'ticker': ticker,
                        'shares': shares,
                        'trail_percent': atr_result['trail_percent'],
                        'status': 'added'
                    })
                else:
                    results['failed'].append({
                        'ticker': ticker,
                        'error': message
                    })

        return results

    def tighten_stops_after_delay(self, delay_days: int = 5, dry_run: bool = True) -> Dict:
        """
        Swap the initial wide 15% stop for the tighter target ATR-based stop
        once a position has been held for `delay_days` trading days.

        This implements the "delayed-stop rule" added 2026-07-22 to fix the
        <=7 day hold-period problem where ATR stops were cutting winners into
        losers on normal intraday noise.

        Args:
            delay_days: Calendar days after entry before tightening (default 5)
            dry_run: If True, only report what would happen

        Returns:
            Dict of results per ticker
        """
        import sqlite3
        from pathlib import Path

        db_path = Path(__file__).parent.parent / "sentinel.db"
        results = {'dry_run': dry_run, 'tightened': [], 'still_in_delay': [], 'errors': []}

        # Get all open positions with entry dates
        try:
            conn = sqlite3.connect(str(db_path), timeout=30.0)
            cur = conn.cursor()
            cur.execute(
                """
                SELECT ticker, actual_shares, actual_entry_price, actual_entry_date
                FROM portfolio_positions
                WHERE status = 'OPEN' AND actual_entry_date IS NOT NULL
                """
            )
            open_positions = cur.fetchall()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to read open positions: {e}")
            return results

        trailing_stops = self.get_open_trailing_stops()

        for ticker, shares, entry_price, entry_date_str in open_positions:
            try:
                entry_date = datetime.fromisoformat(entry_date_str).date()
                age_days = (datetime.now().date() - entry_date).days

                if age_days < delay_days:
                    results['still_in_delay'].append({
                        'ticker': ticker,
                        'age_days': age_days,
                        'delay_days': delay_days,
                    })
                    continue

                # Find the current trailing stop
                stop_info = trailing_stops.get(ticker)
                if not stop_info:
                    logger.info(f"{ticker}: no active trailing stop found (skipping)")
                    continue

                current_trail_pct = stop_info.get('trail_percent') or 0
                # Get current price to compute target ATR
                pos = next((p for p in self.get_all_positions() if p['ticker'] == ticker), None)
                if pos is None:
                    continue
                atr_result = calculate_trailing_stop_percent(ticker, pos['current_price'])
                target_pct = atr_result['trail_percent']

                # Only tighten if the current stop is still the wide 15% initial
                # (allow a small tolerance for float noise)
                if current_trail_pct < 14.5:
                    logger.debug(f"{ticker}: stop already tightened to {current_trail_pct}% — skipping")
                    continue
                # And only if the target is materially tighter
                if target_pct >= current_trail_pct - 0.5:
                    continue

                if dry_run:
                    logger.info(
                        f"[DRY RUN] Would tighten {ticker}: {current_trail_pct}% -> {target_pct}% "
                        f"(age {age_days} days)"
                    )
                    results['tightened'].append({
                        'ticker': ticker, 'from_pct': current_trail_pct,
                        'to_pct': target_pct, 'status': 'would_tighten'
                    })
                    continue

                # Cancel old stop
                try:
                    self.trading_client.cancel_order_by_id(stop_info['order_id'])
                except Exception as e:
                    logger.warning(f"{ticker}: could not cancel old stop: {e}")

                # Submit new tighter trailing stop
                new_req = TrailingStopOrderRequest(
                    symbol=ticker,
                    qty=shares,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC,
                    trail_percent=target_pct,
                )
                new_order = self.trading_client.submit_order(new_req)
                logger.info(
                    f"{ticker}: tightened stop {current_trail_pct}% -> {target_pct}% "
                    f"(new order {new_order.id}, age {age_days} days)"
                )
                results['tightened'].append({
                    'ticker': ticker, 'from_pct': current_trail_pct,
                    'to_pct': target_pct, 'status': 'tightened',
                    'new_order_id': str(new_order.id),
                })
            except Exception as e:
                logger.error(f"{ticker}: tighten failed - {e}")
                results['errors'].append({'ticker': ticker, 'error': str(e)})

        return results

    def generate_report(self) -> str:
        """Generate a human-readable protection status report."""
        status = self.check_protection_status()

        lines = [
            "=" * 70,
            "TRAILING STOP PROTECTION REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 70,
            "",
            f"Total Positions: {status['total_positions']}",
            f"Protected: {len(status['protected'])} ({status['protection_rate']:.1f}%)",
            f"Unprotected: {len(status['unprotected'])}",
            "",
        ]

        if status['protected']:
            lines.append("PROTECTED POSITIONS:")
            lines.append("-" * 70)
            lines.append(f"{'Ticker':<8} {'Shares':>10} {'Price':>10} {'Trail%':>8} {'P&L':>10}")
            lines.append("-" * 70)

            for ticker in status['protected']:
                pos = status['details'][ticker]
                stop = pos['trailing_stop']
                trail_pct = f"{stop['trail_percent']:.1f}%" if stop['trail_percent'] else "N/A"
                pl = f"{pos['unrealized_pl_pct']:+.1f}%"

                lines.append(
                    f"{ticker:<8} {pos['shares']:>10.0f} ${pos['current_price']:>8.2f} "
                    f"{trail_pct:>8} {pl:>10}"
                )
            lines.append("")

        if status['unprotected']:
            lines.append("UNPROTECTED POSITIONS (Need Trailing Stops):")
            lines.append("-" * 70)
            lines.append(f"{'Ticker':<8} {'Shares':>10} {'Price':>10} {'Suggested':>10} {'P&L':>10}")
            lines.append("-" * 70)

            for ticker in status['unprotected']:
                pos = status['details'][ticker]
                # Calculate what trailing stop would be
                atr_result = calculate_trailing_stop_percent(ticker, pos['current_price'])
                suggested = f"{atr_result['trail_percent']:.1f}%"
                pl = f"{pos['unrealized_pl_pct']:+.1f}%"

                lines.append(
                    f"{ticker:<8} {pos['shares']:>10.0f} ${pos['current_price']:>8.2f} "
                    f"{suggested:>10} {pl:>10}"
                )
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)


def main():
    """Run trailing stop monitor from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Trailing Stop Monitor')
    parser.add_argument('--protect', action='store_true', help='Add trailing stops to unprotected positions')
    parser.add_argument('--tighten', action='store_true', help='Swap wide 15%% stops for tight ATR stops after delay')
    parser.add_argument('--delay-days', type=int, default=5, help='Days before tightening (default 5)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--report', action='store_true', help='Generate protection status report')

    args = parser.parse_args()

    monitor = TrailingStopMonitor()

    if args.report or (not args.protect and not args.tighten):
        print(monitor.generate_report())

    if args.tighten:
        dry_run = args.dry_run
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Tightening stops after {args.delay_days} day delay...\n")
        tighten_results = monitor.tighten_stops_after_delay(
            delay_days=args.delay_days, dry_run=dry_run
        )
        print(f"Tightened: {len(tighten_results['tightened'])}")
        print(f"Still in delay window: {len(tighten_results['still_in_delay'])}")
        print(f"Errors: {len(tighten_results['errors'])}")

    if args.protect:
        dry_run = args.dry_run
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Protecting unprotected positions...\n")
        results = monitor.protect_all_positions(dry_run=dry_run)

        print(f"Positions checked: {results['positions_checked']}")
        print(f"Already protected: {results['already_protected']}")
        print(f"Newly protected: {len(results['newly_protected'])}")
        print(f"Failed: {len(results['failed'])}")

        if results['failed']:
            print("\nFailed positions:")
            for fail in results['failed']:
                print(f"  {fail['ticker']}: {fail['error']}")


if __name__ == "__main__":
    main()
