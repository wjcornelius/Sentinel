"""
Position Drift Monitor
======================
Monitors positions for drift beyond configured limits.
Generates SELL recommendations when positions grow too large.

Usage:
    python -m Utils.position_drift_monitor [--dry-run]
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class PositionDriftMonitor:
    """
    Monitor positions for size drift beyond limits.

    When a position appreciates beyond max_position_pct, generates
    a recommendation to trim it back to target_position_pct.
    """

    def __init__(self):
        import yaml
        from alpaca.trading.client import TradingClient
        import config

        self.trading_client = TradingClient(
            config.APCA_API_KEY_ID,
            config.APCA_API_SECRET_KEY,
            paper=True
        )

        # Load constraints
        hard_constraints_path = project_root / "Config" / "hard_constraints.yaml"
        with open(hard_constraints_path) as f:
            self.hard_constraints = yaml.safe_load(f)

        # Position limits from hard_constraints.yaml
        self.max_position_pct = self.hard_constraints['position_limits']['max_single_position_pct']  # 0.25 (25%)
        self.target_position_pct = 0.20  # Trim back to 20% when exceeded
        self.alert_threshold_pct = 0.22  # Alert at 22% (before hitting 25% limit)

    def check_position_drift(self) -> Dict:
        """
        Check all positions for drift beyond limits.

        Returns:
            Dict with drift analysis and recommendations
        """
        account = self.trading_client.get_account()
        positions = self.trading_client.get_all_positions()

        portfolio_value = float(account.portfolio_value)

        results = {
            'timestamp': datetime.now().isoformat(),
            'portfolio_value': portfolio_value,
            'max_position_pct': self.max_position_pct,
            'positions_checked': len(positions),
            'oversized_positions': [],
            'alert_positions': [],
            'trim_recommendations': [],
            'all_positions': []
        }

        for pos in positions:
            ticker = pos.symbol
            market_value = float(pos.market_value)
            shares = float(pos.qty)
            current_price = float(pos.current_price)
            position_pct = market_value / portfolio_value

            position_info = {
                'ticker': ticker,
                'shares': shares,
                'market_value': market_value,
                'current_price': current_price,
                'position_pct': position_pct,
                'position_pct_display': f"{position_pct:.1%}"
            }
            results['all_positions'].append(position_info)

            # Check if position exceeds maximum
            if position_pct > self.max_position_pct:
                results['oversized_positions'].append(position_info)

                # Calculate trim amount
                target_value = portfolio_value * self.target_position_pct
                excess_value = market_value - target_value
                shares_to_sell = int(excess_value / current_price)

                if shares_to_sell > 0:
                    results['trim_recommendations'].append({
                        'ticker': ticker,
                        'action': 'SELL',
                        'shares_to_sell': shares_to_sell,
                        'current_pct': f"{position_pct:.1%}",
                        'target_pct': f"{self.target_position_pct:.1%}",
                        'excess_value': excess_value,
                        'reason': f"Position at {position_pct:.1%} exceeds {self.max_position_pct:.0%} limit"
                    })

            # Check if approaching limit (alert zone)
            elif position_pct > self.alert_threshold_pct:
                results['alert_positions'].append(position_info)

        # Sort all positions by size (largest first)
        results['all_positions'].sort(key=lambda x: -x['position_pct'])

        return results

    def generate_trim_orders(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Generate order specifications from trim recommendations.

        Args:
            recommendations: List of trim recommendations

        Returns:
            List of order specs ready for execution
        """
        orders = []
        for rec in recommendations:
            orders.append({
                'ticker': rec['ticker'],
                'action': 'SELL',
                'quantity': rec['shares_to_sell'],
                'order_type': 'MARKET',
                'reason': rec['reason'],
                'source': 'position_drift_monitor'
            })
        return orders

    def print_report(self, results: Dict):
        """Print a formatted drift report."""
        print("\n" + "=" * 70)
        print("POSITION DRIFT MONITOR REPORT")
        print(f"Timestamp: {results['timestamp']}")
        print("=" * 70)

        print(f"\nPortfolio Value: ${results['portfolio_value']:,.2f}")
        print(f"Max Position Limit: {results['max_position_pct']:.0%}")
        print(f"Positions Checked: {results['positions_checked']}")

        # All positions summary
        print("\n--- ALL POSITIONS (by size) ---")
        for pos in results['all_positions']:
            status = ""
            if pos['position_pct'] > self.max_position_pct:
                status = " *** OVERSIZED ***"
            elif pos['position_pct'] > self.alert_threshold_pct:
                status = " (approaching limit)"
            print(f"  {pos['ticker']}: {pos['position_pct_display']} (${pos['market_value']:,.2f}){status}")

        # Oversized positions
        if results['oversized_positions']:
            print("\n--- OVERSIZED POSITIONS ---")
            for pos in results['oversized_positions']:
                print(f"  {pos['ticker']}: {pos['position_pct_display']} - EXCEEDS {self.max_position_pct:.0%} LIMIT")
        else:
            print("\n--- No oversized positions ---")

        # Alert positions
        if results['alert_positions']:
            print("\n--- ALERT POSITIONS (approaching limit) ---")
            for pos in results['alert_positions']:
                print(f"  {pos['ticker']}: {pos['position_pct_display']} - approaching {self.max_position_pct:.0%} limit")

        # Trim recommendations
        if results['trim_recommendations']:
            print("\n--- TRIM RECOMMENDATIONS ---")
            for rec in results['trim_recommendations']:
                print(f"  SELL {rec['shares_to_sell']} shares of {rec['ticker']}")
                print(f"    Current: {rec['current_pct']} -> Target: {rec['target_pct']}")
                print(f"    Excess value: ${rec['excess_value']:,.2f}")
        else:
            print("\n--- No trim actions required ---")

        print("\n" + "=" * 70)


def main():
    """Run the position drift monitor."""
    import argparse

    parser = argparse.ArgumentParser(description="Monitor positions for size drift")
    parser.add_argument('--dry-run', action='store_true', help="Check only, don't execute")
    parser.add_argument('--json', action='store_true', help="Output as JSON")
    args = parser.parse_args()

    monitor = PositionDriftMonitor()
    results = monitor.check_position_drift()

    if args.json:
        import json
        print(json.dumps(results, indent=2, default=str))
    else:
        monitor.print_report(results)

        if results['trim_recommendations']:
            print("\nTo execute trim orders, integrate with Trading Department")
            print("or run manually via Alpaca dashboard.")


if __name__ == "__main__":
    main()
