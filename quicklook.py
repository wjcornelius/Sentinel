# -*- coding: utf-8 -*-
"""
QuickLook - Standalone stock analysis tool
Analyzes stocks using yfinance data and OpenAI for AI insights.
Usage: python quicklook.py AAPL MSFT NVDA
"""

import argparse
import sys
from datetime import datetime, timedelta

import yfinance as yf
from openai import OpenAI

# Import API key from config
try:
    from config import OPENAI_API_KEY
except ImportError:
    import os
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        print("ERROR: Could not find OPENAI_API_KEY in config.py or environment")
        sys.exit(1)


def calculate_rsi(prices, period=14):
    """Calculate RSI from price series."""
    if len(prices) < period + 1:
        return None
    deltas = prices.diff()
    gains = deltas.where(deltas > 0, 0)
    losses = (-deltas).where(deltas < 0, 0)
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else None


def get_stock_data(ticker: str) -> dict:
    """Fetch comprehensive stock data using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get historical data for technicals
        hist = stock.history(period="1y")
        if hist.empty:
            return {"error": f"No historical data for {ticker}"}

        latest_close = hist['Close'].iloc[-1]

        # Price changes
        one_day_ago = hist['Close'].iloc[-2] if len(hist) >= 2 else latest_close
        twenty_days_ago = hist['Close'].iloc[-20] if len(hist) >= 20 else latest_close
        sixty_days_ago = hist['Close'].iloc[-60] if len(hist) >= 60 else latest_close

        one_day_change = ((latest_close - one_day_ago) / one_day_ago) * 100
        twenty_day_change = ((latest_close - twenty_days_ago) / twenty_days_ago) * 100
        sixty_day_change = ((latest_close - sixty_days_ago) / sixty_days_ago) * 100

        # Moving averages
        sma_20 = hist['Close'].tail(20).mean() if len(hist) >= 20 else None
        sma_50 = hist['Close'].tail(50).mean() if len(hist) >= 50 else None
        sma_200 = hist['Close'].tail(200).mean() if len(hist) >= 200 else None

        # RSI
        rsi = calculate_rsi(hist['Close'])

        # 52-week range
        fifty_two_week_high = hist['Close'].max()
        fifty_two_week_low = hist['Close'].min()

        # Average volume
        avg_volume = hist['Volume'].tail(20).mean()

        # ATR for volatility context
        high_low = hist['High'] - hist['Low']
        high_close = abs(hist['High'] - hist['Close'].shift())
        low_close = abs(hist['Low'] - hist['Close'].shift())
        tr = high_low.combine(high_close, max).combine(low_close, max)
        atr = tr.tail(14).mean()
        atr_percent = (atr / latest_close) * 100

        return {
            "ticker": ticker.upper(),
            "company_name": info.get('longName', ticker),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "latest_close": latest_close,
            "one_day_change_pct": one_day_change,
            "twenty_day_change_pct": twenty_day_change,
            "sixty_day_change_pct": sixty_day_change,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "rsi_14": rsi,
            "fifty_two_week_high": fifty_two_week_high,
            "fifty_two_week_low": fifty_two_week_low,
            "avg_volume_20d": avg_volume,
            "atr_percent": atr_percent,
            "market_cap": info.get('marketCap'),
            "forward_pe": info.get('forwardPE'),
            "trailing_pe": info.get('trailingPE'),
            "price_to_book": info.get('priceToBook'),
            "profit_margins": info.get('profitMargins'),
            "revenue_growth": info.get('revenueGrowth'),
            "earnings_growth": info.get('earningsGrowth'),
            "dividend_yield": info.get('dividendYield'),
            "beta": info.get('beta'),
            "short_ratio": info.get('shortRatio'),
            "analyst_target": info.get('targetMeanPrice'),
            "recommendation": info.get('recommendationKey'),
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def format_value(value, fmt="{:.2f}", fallback="N/A"):
    """Format a value with fallback for None."""
    if value is None:
        return fallback
    try:
        return fmt.format(value)
    except:
        return str(value)


def format_large_number(value):
    """Format large numbers (market cap, volume) in readable form."""
    if value is None:
        return "N/A"
    if value >= 1e12:
        return f"${value/1e12:.2f}T"
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    if value >= 1e6:
        return f"${value/1e6:.2f}M"
    return f"${value:,.0f}"


def print_stock_summary(data: dict):
    """Print formatted stock summary to console."""
    if "error" in data:
        print(f"  ERROR: {data['error']}")
        return

    print(f"  Company: {data['company_name']}")
    print(f"  Sector: {data['sector']} | Industry: {data['industry']}")
    print(f"  Market Cap: {format_large_number(data.get('market_cap'))}")
    print()

    print(f"  Latest Close: ${format_value(data['latest_close'])}")
    print(f"  Price Change: 1D {format_value(data['one_day_change_pct'], '{:+.2f}')}% | "
          f"20D {format_value(data['twenty_day_change_pct'], '{:+.2f}')}% | "
          f"60D {format_value(data['sixty_day_change_pct'], '{:+.2f}')}%")
    print(f"  52-Week Range: ${format_value(data['fifty_two_week_low'])} - ${format_value(data['fifty_two_week_high'])}")
    print()

    print(f"  SMA 20: ${format_value(data['sma_20'])} | "
          f"SMA 50: ${format_value(data['sma_50'])} | "
          f"SMA 200: ${format_value(data['sma_200'])}")
    print(f"  RSI(14): {format_value(data['rsi_14'])}")
    print(f"  ATR Volatility: {format_value(data['atr_percent'])}%")
    print(f"  Beta: {format_value(data.get('beta'))}")
    print()

    print(f"  Forward P/E: {format_value(data.get('forward_pe'))} | "
          f"Trailing P/E: {format_value(data.get('trailing_pe'))} | "
          f"P/B: {format_value(data.get('price_to_book'))}")
    print(f"  Profit Margin: {format_value(data.get('profit_margins'), '{:.1%}') if data.get('profit_margins') else 'N/A'}")
    print(f"  Revenue Growth: {format_value(data.get('revenue_growth'), '{:.1%}') if data.get('revenue_growth') else 'N/A'} | "
          f"Earnings Growth: {format_value(data.get('earnings_growth'), '{:.1%}') if data.get('earnings_growth') else 'N/A'}")
    div_yield = data.get('dividend_yield')
    print(f"  Dividend Yield: {format_value(div_yield, '{:.2%}') if div_yield else 'None'}")
    print()

    print(f"  Analyst Target: ${format_value(data.get('analyst_target'))} | "
          f"Recommendation: {data.get('recommendation', 'N/A').upper() if data.get('recommendation') else 'N/A'}")
    print(f"  Short Ratio: {format_value(data.get('short_ratio'))} days")


def get_ai_analysis(data: dict) -> str:
    """Get AI analysis of the stock using OpenAI."""
    if "error" in data:
        return "Cannot provide AI analysis due to data error."

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Build context for AI
    prompt = f"""Analyze this stock for a swing trading perspective (holding period: days to weeks).

Stock: {data['ticker']} - {data['company_name']}
Sector: {data['sector']} | Industry: {data['industry']}

PRICE DATA:
- Current Price: ${data['latest_close']:.2f}
- 1-Day Change: {data['one_day_change_pct']:+.2f}%
- 20-Day Change: {data['twenty_day_change_pct']:+.2f}%
- 60-Day Change: {data['sixty_day_change_pct']:+.2f}%
- 52-Week Range: ${data['fifty_two_week_low']:.2f} - ${data['fifty_two_week_high']:.2f}

TECHNICALS:
- SMA 20: {f"${data['sma_20']:.2f}" if data['sma_20'] else 'N/A'}
- SMA 50: {f"${data['sma_50']:.2f}" if data['sma_50'] else 'N/A'}
- SMA 200: {f"${data['sma_200']:.2f}" if data['sma_200'] else 'N/A'}
- RSI(14): {f"{data['rsi_14']:.1f}" if data['rsi_14'] else 'N/A'}
- ATR Volatility: {f"{data['atr_percent']:.2f}" if data['atr_percent'] else 'N/A'}%
- Beta: {data.get('beta', 'N/A')}

FUNDAMENTALS:
- Market Cap: {format_large_number(data.get('market_cap'))}
- Forward P/E: {data.get('forward_pe', 'N/A')}
- Trailing P/E: {data.get('trailing_pe', 'N/A')}
- Profit Margin: {f"{data['profit_margins']:.1%}" if data.get('profit_margins') else 'N/A'}
- Revenue Growth: {f"{data['revenue_growth']:.1%}" if data.get('revenue_growth') else 'N/A'}

ANALYST DATA:
- Target Price: ${data.get('analyst_target', 'N/A')}
- Recommendation: {data.get('recommendation', 'N/A')}
- Short Ratio: {data.get('short_ratio', 'N/A')} days

Provide a concise analysis covering:
1. OVERALL ASSESSMENT: Bullish/Bearish/Neutral and why (1-2 sentences)
2. KEY STRENGTHS: Top 2-3 positives
3. KEY RISKS: Top 2-3 concerns
4. SWING TRADE OUTLOOK: Is this a good swing trade candidate right now? Entry considerations?

Keep the response under 200 words. Be direct and actionable."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional stock analyst providing concise, actionable insights for swing traders. Be direct and avoid fluff."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis error: {str(e)}"


def run_quicklook(tickers: list, skip_ai: bool = False):
    """Run QuickLook analysis on provided tickers."""
    print(f"\n{'='*72}")
    print(f"  QUICKLOOK STOCK ANALYSIS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*72}\n")

    for ticker in tickers:
        ticker = ticker.upper().strip()
        print(f"{'='*72}")
        print(f"  {ticker}")
        print(f"{'='*72}")

        # Get stock data
        print("\n  Fetching data...\n")
        data = get_stock_data(ticker)
        print_stock_summary(data)

        # Get AI analysis
        if not skip_ai and "error" not in data:
            print(f"\n{'-'*72}")
            print("  AI ANALYSIS")
            print(f"{'-'*72}\n")
            analysis = get_ai_analysis(data)
            # Indent the analysis
            for line in analysis.split('\n'):
                print(f"  {line}")

        print(f"\n{'='*72}\n")


def main():
    parser = argparse.ArgumentParser(
        description="QuickLook - Fast stock analysis with AI insights",
        epilog="Example: python quicklook.py AAPL NVDA TSLA"
    )
    parser.add_argument(
        "tickers",
        nargs="*",
        help="Ticker symbols to analyze (e.g., AAPL MSFT NVDA)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip AI analysis (faster, just show data)"
    )
    args = parser.parse_args()

    # If no tickers provided, prompt for input
    if not args.tickers:
        print("\nQuickLook - Stock Analysis Tool")
        print("-" * 40)
        ticker_input = input("Enter ticker(s) separated by spaces: ").strip()
        if not ticker_input:
            print("No tickers provided. Exiting.")
            sys.exit(0)
        tickers = ticker_input.split()
    else:
        tickers = args.tickers

    run_quicklook(tickers, skip_ai=args.no_ai)

    # Only prompt if running interactively
    try:
        import sys
        if sys.stdin.isatty():
            input("\nPress Enter to exit...")
    except:
        pass


if __name__ == "__main__":
    main()
