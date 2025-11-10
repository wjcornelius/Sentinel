"""
Weekly Universe Refresh Script
================================

Purpose: Generate optimized swing trading universe for upcoming week

Run Schedule: Weekends only (Saturday/Sunday)
Output: ticker_universe.txt with ~800 swing-suitable stocks

Filters Applied:
- Market cap: $2B - $200B
- Average daily volume: >2M shares
- ATR% (14-day): >2.5% (volatility requirement)
- Price range: $10 - $500
- Excludes: Utilities, REITs, Preferred stocks

Usage:
  python refresh_universe.py              # Interactive mode (asks confirmation)
  python refresh_universe.py --force      # Force run (skip weekend check)
  python refresh_universe.py --auto       # Auto mode (no confirmation)
"""

import sys
import json
import sqlite3
import yfinance as yf
import pandas as pd
import yaml
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Dict, Tuple


class UniverseRefresher:
    """Generate optimized swing trading universe"""

    def __init__(self, db_path: str = "sentinel.db"):
        self.db_path = db_path

        # Load Alpaca credentials from config
        self._load_alpaca_config()

        # Swing trading criteria
        self.MIN_MARKET_CAP = 2_000_000_000  # $2B
        self.MAX_MARKET_CAP = 200_000_000_000  # $200B
        self.MIN_AVG_VOLUME = 2_000_000  # 2M shares/day
        self.MIN_PRICE = 10.0
        self.MAX_PRICE = 500.0
        self.MIN_ATR_PERCENT = 2.5  # Minimum 2.5% daily volatility

        # Excluded sectors/categories
        self.EXCLUDED_KEYWORDS = ['PREFERRED', 'WARRANT', 'UNIT', 'RIGHT', 'NOTE']

        self._init_database()

    def _load_alpaca_config(self):
        """Load Alpaca API credentials from config file"""
        try:
            config_path = Path(__file__).parent / "Config" / "alpaca_config.yaml"
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            self.api_key = config['api_key']
            self.secret_key = config['secret_key']
            self.base_url = config['base_url']

        except Exception as e:
            raise RuntimeError(f"Failed to load Alpaca config: {e}")

    def _init_database(self):
        """Create table for universe history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS universe_history (
                refresh_date TEXT PRIMARY KEY,
                ticker_count INTEGER,
                tickers_json TEXT,
                criteria_json TEXT,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def check_weekend(self) -> Tuple[bool, str]:
        """
        Check if today is weekend

        Returns:
            (is_weekend, message)
        """
        today = date.today()
        day_name = today.strftime('%A')

        if today.weekday() >= 5:  # Saturday=5, Sunday=6
            return True, f"Today is {day_name} - weekend check PASSED"
        else:
            return False, f"Today is {day_name} - NOT a weekend. Universe refresh should run on weekends only."

    def get_all_tradeable_stocks(self) -> List[Dict]:
        """
        Get all tradeable stocks from Alpaca

        Returns:
            List of stock info dicts
        """
        print("\nFetching all tradeable stocks from Alpaca...")

        try:
            # Get all active stocks from Alpaca
            api = tradeapi.REST(
                key_id=self.api_key,
                secret_key=self.secret_key,
                base_url=self.base_url
            )

            assets = api.list_assets(status='active', asset_class='us_equity')

            # Filter to stocks only (exclude crypto, etc)
            stocks = []
            for asset in assets:
                # Skip non-tradeable
                if not asset.tradable:
                    continue

                # Skip fractionable=False (usually weird securities)
                if not asset.fractionable:
                    continue

                # Skip excluded keywords in name
                if any(kw in asset.name.upper() for kw in self.EXCLUDED_KEYWORDS):
                    continue

                stocks.append({
                    'ticker': asset.symbol,
                    'name': asset.name,
                    'exchange': asset.exchange
                })

            print(f"  Found {len(stocks):,} tradeable stocks")
            return stocks

        except Exception as e:
            print(f"  ERROR: Failed to fetch stocks from Alpaca: {e}")
            return []

    def apply_swing_filters(self, stocks: List[Dict]) -> List[str]:
        """
        Apply swing trading filters to stock list

        Args:
            stocks: List of stock info dicts

        Returns:
            List of tickers meeting swing criteria
        """
        print(f"\nApplying swing trading filters to {len(stocks):,} stocks...")
        print(f"  Criteria:")
        print(f"    - Market cap: ${self.MIN_MARKET_CAP/1e9:.1f}B - ${self.MAX_MARKET_CAP/1e9:.0f}B")
        print(f"    - Avg volume: >{self.MIN_AVG_VOLUME/1e6:.1f}M shares/day")
        print(f"    - Price: ${self.MIN_PRICE} - ${self.MAX_PRICE}")
        print(f"    - ATR%: >{self.MIN_ATR_PERCENT}%")
        print()

        qualified = []
        tickers = [s['ticker'] for s in stocks]

        # Process in batches to avoid rate limits
        batch_size = 100
        total_batches = (len(tickers) + batch_size - 1) // batch_size

        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i+batch_size]
            batch_num = i // batch_size + 1

            print(f"  Processing batch {batch_num}/{total_batches} ({len(batch)} tickers)...", end='', flush=True)

            for ticker in batch:
                try:
                    stock = yf.Ticker(ticker)

                    # Get info (contains market cap)
                    info = stock.info

                    # Check market cap
                    market_cap = info.get('marketCap', 0)
                    if market_cap < self.MIN_MARKET_CAP or market_cap > self.MAX_MARKET_CAP:
                        continue

                    # Get price data (last 30 days for ATR calculation)
                    hist = stock.history(period='1mo', interval='1d')

                    if hist.empty or len(hist) < 14:
                        continue

                    # Check current price
                    current_price = hist['Close'].iloc[-1]
                    if current_price < self.MIN_PRICE or current_price > self.MAX_PRICE:
                        continue

                    # Check average volume
                    avg_volume = hist['Volume'].mean()
                    if avg_volume < self.MIN_AVG_VOLUME:
                        continue

                    # Calculate ATR% (14-day)
                    high_low = hist['High'] - hist['Low']
                    high_close = abs(hist['High'] - hist['Close'].shift())
                    low_close = abs(hist['Low'] - hist['Close'].shift())

                    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                    atr = true_range.rolling(window=14).mean().iloc[-1]
                    atr_percent = (atr / current_price) * 100

                    if atr_percent < self.MIN_ATR_PERCENT:
                        continue

                    # Passed all filters!
                    qualified.append(ticker)

                except Exception as e:
                    # Skip stocks with data issues
                    continue

            print(f" {len(qualified)} qualified so far")

        print(f"\n  RESULT: {len(qualified)} stocks meet swing trading criteria")
        return qualified

    def save_to_database(self, tickers: List[str]) -> bool:
        """
        Save universe to database for audit trail

        Args:
            tickers: List of qualified tickers

        Returns:
            Success boolean
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            refresh_date = date.today().isoformat()
            created_at = datetime.now().isoformat()

            criteria = {
                'min_market_cap': self.MIN_MARKET_CAP,
                'max_market_cap': self.MAX_MARKET_CAP,
                'min_avg_volume': self.MIN_AVG_VOLUME,
                'min_price': self.MIN_PRICE,
                'max_price': self.MAX_PRICE,
                'min_atr_percent': self.MIN_ATR_PERCENT
            }

            cursor.execute("""
                INSERT OR REPLACE INTO universe_history
                (refresh_date, ticker_count, tickers_json, criteria_json, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                refresh_date,
                len(tickers),
                json.dumps(tickers),
                json.dumps(criteria),
                created_at
            ))

            conn.commit()
            conn.close()

            print(f"\n  Saved to database: {len(tickers)} tickers archived")
            return True

        except Exception as e:
            print(f"\n  ERROR saving to database: {e}")
            return False

    def write_universe_file(self, tickers: List[str]) -> bool:
        """
        Write new ticker_universe.txt

        Args:
            tickers: List of qualified tickers

        Returns:
            Success boolean
        """
        try:
            # Sort alphabetically for consistency
            tickers_sorted = sorted(tickers)

            with open('ticker_universe.txt', 'w') as f:
                f.write("# Optimized Swing Trading Universe\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total stocks: {len(tickers_sorted)}\n")
                f.write("#\n")
                f.write("# Criteria:\n")
                f.write(f"#   - Market cap: ${self.MIN_MARKET_CAP/1e9:.1f}B - ${self.MAX_MARKET_CAP/1e9:.0f}B\n")
                f.write(f"#   - Avg volume: >{self.MIN_AVG_VOLUME/1e6:.1f}M shares/day\n")
                f.write(f"#   - Price: ${self.MIN_PRICE} - ${self.MAX_PRICE}\n")
                f.write(f"#   - ATR%: >{self.MIN_ATR_PERCENT}%\n")
                f.write("#\n")

                for ticker in tickers_sorted:
                    f.write(f"{ticker}\n")

            print(f"\n  ticker_universe.txt updated successfully")
            return True

        except Exception as e:
            print(f"\n  ERROR writing ticker_universe.txt: {e}")
            return False

    def run(self, force: bool = False, auto: bool = False) -> bool:
        """
        Run universe refresh

        Args:
            force: Skip weekend check
            auto: Skip confirmation prompt

        Returns:
            Success boolean
        """
        print("=" * 80)
        print("WEEKLY UNIVERSE REFRESH")
        print("=" * 80)
        print()

        # Check if weekend (unless forced)
        if not force:
            is_weekend, message = self.check_weekend()
            print(message)

            if not is_weekend:
                print("\nUse --force flag to run anyway")
                return False
            print()

        # Get all stocks
        stocks = self.get_all_tradeable_stocks()
        if not stocks:
            print("\nERROR: Could not fetch stock list from Alpaca")
            return False

        # Apply filters
        qualified_tickers = self.apply_swing_filters(stocks)

        if not qualified_tickers:
            print("\nERROR: No stocks qualified (criteria may be too strict)")
            return False

        # Show results
        print()
        print("=" * 80)
        print("UNIVERSE REFRESH COMPLETE")
        print("=" * 80)
        print(f"  Starting universe: {len(stocks):,} tradeable stocks")
        print(f"  Qualified stocks: {len(qualified_tickers)} swing-suitable stocks")
        print(f"  Rejection rate: {((len(stocks) - len(qualified_tickers)) / len(stocks) * 100):.1f}%")
        print()

        # Ask for confirmation (unless auto mode)
        if not auto:
            print("This will overwrite ticker_universe.txt with the new universe.")
            print(f"Current file will be backed up as ticker_universe_backup_{date.today().isoformat()}.txt")
            print()
            response = input("Proceed with update? (yes/no): ").strip().lower()

            if response not in ['yes', 'y']:
                print("\nCancelled by user")
                return False

        # Backup old file
        try:
            import shutil
            if Path('ticker_universe.txt').exists():
                backup_name = f"ticker_universe_backup_{date.today().isoformat()}.txt"
                shutil.copy('ticker_universe.txt', backup_name)
                print(f"\n  Old universe backed up to: {backup_name}")
        except Exception as e:
            print(f"\n  WARNING: Could not backup old file: {e}")

        # Save to database
        self.save_to_database(qualified_tickers)

        # Write new file
        success = self.write_universe_file(qualified_tickers)

        if success:
            print()
            print("=" * 80)
            print("SUCCESS!")
            print("=" * 80)
            print(f"  New universe: {len(qualified_tickers)} stocks")
            print(f"  File: ticker_universe.txt")
            print(f"  Ready for Monday's trading plan generation")
            print()
            print("  Next steps:")
            print("    1. Run 'Propose Daily Trading Plan' on Monday morning")
            print("    2. System will automatically use new universe")
            print("    3. Monitor results over the week")
            print("=" * 80)

        return success


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Refresh swing trading universe')
    parser.add_argument('--force', action='store_true', help='Skip weekend check')
    parser.add_argument('--auto', action='store_true', help='Auto mode (no confirmation)')

    args = parser.parse_args()

    refresher = UniverseRefresher()
    success = refresher.run(force=args.force, auto=args.auto)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
