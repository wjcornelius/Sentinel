"""
Fetch S&P 500 and Nasdaq 100 Constituent Lists
================================================
Downloads the actual 600-stock universe from Wikipedia tables.
Saves to a file for use by Research Department.
"""

import pandas as pd
from pathlib import Path

def fetch_sp500_tickers():
    """Fetch S&P 500 tickers from Wikipedia"""
    print("Fetching S&P 500 constituents...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    try:
        # Read the first table (current constituents)
        tables = pd.read_html(url)
        sp500_table = tables[0]

        # Extract ticker symbols
        tickers = sp500_table['Symbol'].tolist()

        # Clean up tickers (some have periods instead of hyphens)
        tickers = [ticker.replace('.', '-') for ticker in tickers]

        print(f"  Found {len(tickers)} S&P 500 stocks")
        return tickers
    except Exception as e:
        print(f"  ERROR fetching S&P 500: {e}")
        return []

def fetch_nasdaq100_tickers():
    """Fetch Nasdaq 100 tickers from Wikipedia"""
    print("Fetching Nasdaq 100 constituents...")
    url = 'https://en.wikipedia.org/wiki/Nasdaq-100'

    try:
        # Read tables from the page
        tables = pd.read_html(url)

        # The constituent table is usually table index 4
        nasdaq_table = tables[4]

        # Extract ticker symbols
        tickers = nasdaq_table['Ticker'].tolist()

        print(f"  Found {len(tickers)} Nasdaq 100 stocks")
        return tickers
    except Exception as e:
        print(f"  ERROR fetching Nasdaq 100: {e}")
        return []

def save_universe(tickers, filename="ticker_universe.txt"):
    """Save ticker universe to file"""
    output_path = Path(__file__).parent / filename

    with open(output_path, 'w') as f:
        for ticker in sorted(set(tickers)):
            f.write(f"{ticker}\n")

    print(f"\nSaved {len(set(tickers))} unique tickers to {filename}")
    return output_path

if __name__ == "__main__":
    print("=" * 70)
    print("FETCHING STOCK UNIVERSE (S&P 500 + Nasdaq 100)")
    print("=" * 70)

    # Fetch both lists
    sp500 = fetch_sp500_tickers()
    nasdaq100 = fetch_nasdaq100_tickers()

    # Combine (will have some overlap like AAPL, MSFT, etc.)
    combined = sp500 + nasdaq100
    unique_tickers = sorted(set(combined))

    print("\n" + "=" * 70)
    print(f"TOTAL UNIVERSE: {len(unique_tickers)} unique stocks")
    print(f"  S&P 500: {len(sp500)} stocks")
    print(f"  Nasdaq 100: {len(nasdaq100)} stocks")
    print(f"  Overlap: {len(sp500) + len(nasdaq100) - len(unique_tickers)} stocks")
    print("=" * 70)

    # Save to file
    save_universe(unique_tickers)

    print("\nDone! Research Department can now use this universe.")
