# -*- coding: utf-8 -*-
# main_script.py
# Version 7.8 - Desktop Dashboard with Web UI (Flask-based control panel)

import config
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import time
from io import StringIO
from openai import OpenAI
import requests
from twilio.rest import Client
import sqlite3
import math
import logging
import os
from pathlib import Path
import backup_database
from functools import wraps
from sentinel import ui_bridge

DB_FILE = "sentinel.db"
LOG_DIR = "logs"
BACKUP_DIR = "backups"

# API retry configuration
MAX_API_RETRIES = 3
API_RETRY_DELAY = 2  # seconds

TARGET_INVESTED_RATIO = 0.90
MAX_POSITION_PERCENTAGE = 0.10

MIN_POSITIONS = 10
MAX_POSITIONS = 100
TARGET_POSITION_COUNT = 80

MIN_TRADE_DOLLAR_THRESHOLD = 25.0
CONVICTION_WEIGHT_EXP = 1.6  # Exponential weight for conviction scoring (higher = more aggressive weighting)
MIN_WEIGHT_FLOOR = 0.05  # Minimum allocation weight to prevent zero-weight positions

# Setup logging
def setup_logging():
    """Configure logging to both file and console with appropriate levels."""
    Path(LOG_DIR).mkdir(exist_ok=True)

    log_filename = os.path.join(LOG_DIR, f"sentinel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler - detailed logging
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler - info and above (keeps console clean)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("="*80)
    logging.info("Sentinel logging initialized")
    logging.info(f"Log file: {log_filename}")
    logging.info(f"Config: LIVE_TRADING={config.LIVE_TRADING}, ALLOW_DEV_RERUNS={getattr(config, 'ALLOW_DEV_RERUNS', False)}")
    logging.info("="*80)

    return log_filename


def retry_on_failure(max_retries=MAX_API_RETRIES, delay=API_RETRY_DELAY, exceptions=(Exception,)):
    """
    Decorator to retry a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Base delay in seconds between retries (doubles with each retry)
        exceptions: Tuple of exception types to catch and retry on

    Returns:
        Decorated function that retries on failure
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logging.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= 2  # Exponential backoff
                    else:
                        logging.error(
                            f"{func.__name__} failed after {max_retries} attempts: {e}",
                            exc_info=True
                        )

            # If we get here, all retries failed
            raise last_exception

        return wrapper
    return decorator


SAME_DAY_CONFLICT_ERROR = (
    "SAFEGUARD TRIGGERED: The trade plan attempted to both buy and sell the same symbol "
    "in a single run. No trades will be executed. Please share the log with the developer."
)

ANALYSIS_PROMPT_TEMPLATE = """
You are Sentinel, a disciplined equity analyst tasked with evaluating a single stock for a daily trading system. You will receive the following JSON payload:

Payload:
<<PAYLOAD>>

Your job is to decide whether the trading system should BUY, SELL, or HOLD this ticker tomorrow and to assign a conviction score between 1 and 10. Follow these instructions exactly:

1. Decision categories
   � BUY � add or increase exposure.
   � SELL � exit or reduce exposure.
   � HOLD � maintain the current position size.

2. Conviction scale (use the full range)
   � 10 � Exceptional edge. Multiple independent, high-quality signals align in a compelling way. Very rare; reserve for best-in-class setups.
   � 8�9 � Strong, actionable idea with clear catalysts and supportive data across most dimensions.
   � 6�7 � Mild positive or negative bias. Evidence is mixed or moderate; fine for tactical adjustments but avoid clustering here unless warranted.
   � 5 � Neutral stance. Signals conflict or lack sufficient edge. Prefer HOLD unless portfolio constraints require action.
   � 3�4 � Notable caution. Signals lean bearish or thesis is deteriorating.
   � 1�2 � Acute risk/urgency to exit. Severe red flags, broken thesis, or imminent negative catalysts. Use sparingly.

   Important: If you find yourself defaulting to 6�7, reassess. Only sit in the mid-range when evidence is truly mixed. Push scores toward the tails when data justifies it.

3. Rationale
   � Provide 2�3 concise bullet points (no more than ~40 words each) covering the strongest drivers of your decision.
   � Mention concrete evidence: earnings momentum, valuation shifts, technical breaks, macro tailwinds/headwinds, regulatory news, etc.
   � If data conflicts, call it out.

4. Output format
   � Return a single JSON object on one line with the keys: symbol, decision, conviction, rationale (array of bullet strings).
   � Ensure valid JSON (double quotes, no trailing commas).

5. Tone & discipline
   � Be analytical, impartial, and data-driven.
   � Do not reference this prompt or the fact you are an AI.
   � If critical data is missing, mention it in the rationale and adjust conviction downward.

Take a moment to weigh all inputs carefully before responding. The trading engine relies on your conviction spread to size positions�make each score count.
"""

def check_if_trades_executed_today():
    """Check if trades have already been executed today to prevent duplicate runs."""
    if getattr(config, "ALLOW_DEV_RERUNS", False):
        print("\n[DEV MODE] Bypassing single-run safeguard for today.")
        logging.warning("DEV MODE: Bypassing single-run safeguard")
        return False
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM trades
            WHERE DATE(timestamp) = DATE('now', 'localtime')
              AND status IN ('submitted', 'filled', 'execution_failed')
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()
        already_ran = result is not None
        logging.info(f"Checked for today's trades: already_ran={already_ran}")
        return already_ran
    except sqlite3.Error as e:
        logging.error(f"Database error checking for executed trades: {e}", exc_info=True)
        print(f"DB_ERROR checking for executed trades: {e}")
        return False

def get_prior_conviction(symbol):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT conviction_score
            FROM decisions
            WHERE symbol = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (symbol.upper(),))
        row = cursor.fetchone()
        conn.close()
        if row and row[0] is not None:
            return sanitize_conviction(row[0])
    except sqlite3.Error as e:
        print(f"  - DB_ERROR fetching prior conviction for {symbol}: {e}")
    return None

def floor_to_precision(value, decimals=6):
    if value <= 0:
        return 0.0
    factor = 10 ** decimals
    floored = math.floor(value * factor) / factor
    epsilon = 1 / factor
    if floored > 0:
        floored = max(0.0, floored - epsilon)
    return max(0.0, floored)

def conviction_to_weight(conviction):
    normalized = max(1, min(10, conviction)) / 10.0
    weight = normalized ** CONVICTION_WEIGHT_EXP
    return max(MIN_WEIGHT_FLOOR, weight)

def calculate_rsi(series, period=14):
    if series is None or len(series) < period + 1:
        return None
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    if avg_loss.iloc[-1] == 0:
        return 100.0
    rs = avg_gain.iloc[-1] / avg_loss.iloc[-1]
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)

def compute_pct_change(series, periods):
    if len(series) <= periods:
        return None
    start = series.iloc[-periods - 1]
    end = series.iloc[-1]
    if start == 0:
        return None
    return float((end - start) / start * 100)

def get_todays_decisions():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, symbol, decision, conviction_score, rationale, latest_price, market_context_summary
            FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        rows = cursor.fetchall()
        conn.close()
        decisions = []
        for row in rows:
            decisions.append({
                "db_decision_id": row["id"],
                "symbol": row["symbol"],
                "decision": row["decision"],
                "conviction_score": row["conviction_score"],
                "rationale": row["rationale"],
                "latest_price": row["latest_price"],
                "market_context_summary": row["market_context_summary"]
            })
        return decisions
    except sqlite3.Error as e:
        print(f"DB_ERROR getting today's decisions: {e}")
        return []

def wipe_today_plan():
    if not getattr(config, "ALLOW_DEV_RERUNS", False):
        return False
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        decisions_deleted = cursor.rowcount
        cursor.execute("""
            DELETE FROM trades
            WHERE DATE(timestamp) = DATE('now', 'localtime')
        """)
        trades_deleted = cursor.rowcount
        conn.commit()
        conn.close()
        print(f"\n[DEV MODE] Cleared today's plan artifacts "
              f"(decisions deleted: {decisions_deleted}, trades deleted: {trades_deleted}).")
        return True
    except sqlite3.Error as e:
        print(f"[DEV MODE] Failed to clear today's plan artifacts: {e}")
        return False

def maybe_regenerate_plan(decisions):
    # Only prompt in DEV_RERUNS mode
    if not getattr(config, "ALLOW_DEV_RERUNS", False):
        return decisions

    # If no decisions found, nothing to regenerate
    if not decisions:
        return decisions

    # Get info about existing plan
    unique_symbols = len({d["symbol"].upper() for d in decisions})
    plan_info = {
        "symbol_count": unique_symbols,
        "decision_count": len(decisions),
        "message": f"Existing plan covers {unique_symbols} symbols with {len(decisions)} decisions"
    }

    print(f"\n[DEV MODE] Existing plan detected for today ({unique_symbols} symbols, {len(decisions)} decisions).", flush=True)
    logging.info(f"[DEV MODE] Existing plan detected - requesting user decision")

    # Ask user via UI or console
    should_regenerate = ui_bridge.wait_for_plan_decision(plan_info)

    if should_regenerate:
        if wipe_today_plan():
            return []
    return decisions

def get_alpaca_api():
    """Initialize and return Alpaca API client."""
    logging.debug(f"Connecting to Alpaca API at {config.APCA_API_BASE_URL}")
    try:
        api = tradeapi.REST(
            config.APCA_API_KEY_ID,
            config.APCA_API_SECRET_KEY,
            config.APCA_API_BASE_URL,
            api_version='v2'
        )
        logging.info("Successfully connected to Alpaca API")
        return api
    except Exception as e:
        logging.error(f"Failed to connect to Alpaca API: {e}", exc_info=True)
        raise

def get_account_info(api):
    """Retrieve account status and current positions from Alpaca."""
    print("--- [Stage 0: Account & Position Review] ---")
    logging.info("Stage 0: Fetching account info and positions")
    try:
        account = api.get_account()
        portfolio_value = float(account.portfolio_value)
        logging.info(f"Account status: {account.status}, Portfolio value: ${portfolio_value:,.2f}")
        print(f"Account is {'ACTIVE' if account.status == 'ACTIVE' else account.status}. "
              f"Portfolio Value: ${portfolio_value:,.2f}")

        positions = api.list_positions()
        logging.info(f"Retrieved {len(positions)} open positions")

        if positions:
            print(f"Current Positions ({len(positions)}):")
            for pos in positions:
                qty = float(pos.qty)
                avg_price = float(pos.avg_entry_price)
                market_value = float(pos.market_value)
                logging.debug(f"Position: {pos.symbol} - {qty:.6f} shares @ ${avg_price:,.2f} = ${market_value:,.2f}")
                print(f"  - {pos.symbol}: {qty:.6f} shares @ avg ${avg_price:,.2f} "
                      f"(Value: ${market_value:,.2f})")
        else:
            print("No open positions.")
            logging.info("No open positions")

        position_map = {p.symbol.upper(): p for p in positions}
        return position_map, account
    except Exception as e:
        logging.error(f"Error retrieving account info from Alpaca: {e}", exc_info=True)
        print(f"Error connecting to Alpaca: {e}")
        return {}, None

def display_performance_report(api, current_value):
    print("\n--- [Stage 0.1: Performance Report] ---")
    try:
        hist = api.get_portfolio_history(period='7D', timeframe='1D')

        if len(hist.equity) > 1:
            prev_close = hist.equity[-2]
            daily_pl = current_value - prev_close
            daily_pl_pct = (daily_pl / prev_close) * 100 if prev_close != 0 else 0
            print(f"  - Daily P/L:    ${daily_pl:,.2f} ({daily_pl_pct:+.2f}%)")
        else:
            print("  - Daily P/L:    Not enough history to calculate.")

        # YTD P/L calculation
        today = datetime.now()
        start_of_year_str = f"{today.year}-01-01"

        logging.debug(f"Fetching YTD history from {start_of_year_str}")
        ytd_hist = api.get_portfolio_history(date_start=start_of_year_str, timeframe='1D')

        if len(ytd_hist.equity) > 0 and len(ytd_hist.timestamp) > 0:
            # Filter out None values and create list of valid (timestamp, equity) pairs
            valid_data = [(ts, eq) for ts, eq in zip(ytd_hist.timestamp, ytd_hist.equity)
                         if eq is not None and eq > 0]

            logging.debug(f"YTD history: {len(ytd_hist.equity)} total points, {len(valid_data)} valid points")

            if valid_data:
                # Get the first valid equity value (earliest trading day)
                ytd_start_value = valid_data[0][1]
                ytd_start_date = pd.to_datetime(valid_data[0][0]).strftime('%Y-%m-%d')

                ytd_pl = current_value - ytd_start_value
                ytd_pl_pct = (ytd_pl / ytd_start_value) * 100
                logging.info(f"YTD P/L: ${ytd_pl:,.2f} ({ytd_pl_pct:+.2f}%) from {ytd_start_date}")
                print(f"  - YTD P/L:      ${ytd_pl:,.2f} ({ytd_pl_pct:+.2f}%) since {ytd_start_date}")
            else:
                logging.warning("No valid YTD equity data found")
                print("  - YTD P/L:      No valid data (account may be new)")
        else:
            logging.warning("YTD history returned empty")
            print("  - YTD P/L:      Not enough history to calculate.")

        # Enhanced Analytics (Phase 3)
        print("\n  [Advanced Metrics]")
        try:
            from sentinel.analytics import generate_performance_summary
            metrics = generate_performance_summary(api, current_value)

            if metrics['days_tracked'] >= 10:
                print(f"  - Sharpe Ratio:   {metrics['sharpe_ratio']:.2f}")
                print(f"  - Max Drawdown:   {metrics['max_drawdown']:.2f}%")
                if metrics['max_dd_start'] and metrics['max_dd_end']:
                    print(f"    (from {metrics['max_dd_start']} to {metrics['max_dd_end']})")
                print(f"  - Volatility:     {metrics['volatility_annual']:.1f}% (annualized)")
                logging.info(f"Advanced metrics: Sharpe={metrics['sharpe_ratio']:.2f}, MaxDD={metrics['max_drawdown']:.2f}%")
            else:
                print(f"  - Need {10 - metrics['days_tracked']} more days of data for advanced metrics")
        except ImportError:
            logging.debug("Analytics module not available, skipping advanced metrics")
        except Exception as e:
            logging.warning(f"Could not calculate advanced metrics: {e}")
            print(f"  - Advanced metrics unavailable: {e}")

    except Exception as e:
        print(f"  - Could not generate performance report: {e}")
        print("  - This may be due to a new account with insufficient history.")
        logging.error(f"Performance report error: {e}", exc_info=True)

def get_nasdaq_100_symbols():
    print("  - Fetching Nasdaq 100 constituents...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        response = requests.get(url, headers=headers, timeout=20.0)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        nasdaq_100_df = next(table for table in tables if 'Ticker' in table.columns)
        symbols = [s.replace('.', '-').upper() for s in nasdaq_100_df['Ticker'].tolist()]
        print(f"  - Successfully fetched {len(symbols)} symbols.")
        return symbols
    except Exception as e:
        print(f"  - ERROR: Could not fetch Nasdaq 100 list: {e}")
        fallback = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL', 'AMZN', 'META']
        print(f"  - Using fallback list: {fallback}")
        return fallback

def generate_candidate_universe(current_symbols):
    print("\n--- [Stage 1: Candidate Universe Generation] ---")
    base_universe = get_nasdaq_100_symbols()
    candidate_universe = sorted(list(set(base_universe + list(current_symbols))))
    print(f"Generated a universe of {len(candidate_universe)} candidates for analysis.")
    return candidate_universe

@retry_on_failure(max_retries=2, delay=3, exceptions=(requests.RequestException,))
def get_raw_search_results_from_perplexity():
    """Fetch market news from Perplexity API with retry logic."""
    print("\n--- [News Gathering Step 1: Searching via Perplexity] ---")
    logging.info("Fetching market news from Perplexity")

    url = "https://api.perplexity.ai/search"
    payload = {"query": "Top 15-20 most significant, market-moving financial news stories last 24 hours"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {config.PERPLEXITY_API_KEY}"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=20.0)
    response.raise_for_status()
    logging.info("Successfully fetched market news from Perplexity")
    print("  - Successfully fetched raw search results from Perplexity.")
    return response.json()

def summarize_market_context_with_openAI(raw_results):
    print("--- [News Gathering Step 2: Summarizing via OpenAI] ---")
    if not raw_results:
        return "Could not retrieve general market news."
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        prompt = (
            "You are a financial news analyst. Summarize the key market-moving stories from the "
            "following dataset into a concise briefing (5 bullet points max). Highlight major risk factors and sentiment.\n"
            f"Dataset:\n{json.dumps(raw_results, indent=2)}"
        )
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            timeout=45.0
        )
        print("  - Successfully summarized market news using OpenAI.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"  - ERROR summarizing news with OpenAI: {e}")
        return "Could not summarize general market news."

def get_stock_specific_news_headlines(api, symbol):
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=3)
        news = api.get_news(
            symbol=symbol,
            start=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            end=end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            limit=5
        )
        return [article.headline for article in news] if news else []
    except Exception:
        return []

def aggregate_data_dossiers(api, universe, market_news_summary, current_positions, portfolio_value):
    print("\n--- [Stage 2: Data Dossier Aggregation] ---")
    dossiers = {}
    print(f"*** Analyzing the full universe of {len(universe)} stocks. ***")

    from threading import Thread
    import queue

    for i, symbol in enumerate(universe):
        print(f"Aggregating data for {symbol} ({i+1}/{len(universe)})...")

        # Use threading to add timeout for entire dossier creation
        result_queue = queue.Queue()

        def create_dossier_with_timeout():
            try:
                dossier = _create_single_dossier(api, symbol, market_news_summary, current_positions, portfolio_value)
                result_queue.put(('success', dossier))
            except Exception as e:
                result_queue.put(('error', str(e)))

        thread = Thread(target=create_dossier_with_timeout)
        thread.daemon = True
        thread.start()
        thread.join(timeout=30)  # 30 second timeout per stock

        if thread.is_alive():
            print(f"  - Timeout fetching data for {symbol}; skipping.")
            logging.warning(f"Timeout during dossier creation for {symbol}")
            continue

        try:
            status, result = result_queue.get_nowait()
            if status == 'success' and result:
                dossiers[symbol] = result
                print(f"  - Successfully created dossier for {symbol}.")
            elif status == 'error':
                print(f"  - Failed to create dossier for {symbol}: {result}")
        except queue.Empty:
            print(f"  - No result returned for {symbol}; skipping.")

        time.sleep(1)

    print(f"\nSuccessfully aggregated {len(dossiers)} data dossiers.")
    return dossiers


def _create_single_dossier(api, symbol, market_news_summary, current_positions, portfolio_value):
    """Create dossier for a single stock (extracted for timeout wrapper)."""
    try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            bars_obj = api.get_bars(
                symbol,
                '1Day',
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                feed=config.APCA_API_DATA_FEED
            )
            bars = bars_obj.df
            if bars.empty:
                print(f"  - No price data found for {symbol}; skipping.")
                return None

            closes = bars['close']
            highs = bars['high']
            lows = bars['low']
            latest_close = float(closes.iloc[-1])
            prev_close = float(closes.iloc[-2]) if len(closes) > 1 else latest_close
            change_1d = ((latest_close - prev_close) / prev_close * 100) if prev_close else 0.0
            change_20d = compute_pct_change(closes, 20)
            change_60d = compute_pct_change(closes, 60)

            sma_20 = float(closes.rolling(window=20).mean().iloc[-1]) if len(closes) >= 20 else None
            sma_50 = float(closes.rolling(window=50).mean().iloc[-1]) if len(closes) >= 50 else None
            sma_200 = float(closes.rolling(window=200).mean().iloc[-1]) if len(closes) >= 200 else None
            rsi_14 = calculate_rsi(closes, period=14)
            year_high = float(highs.rolling(window=min(len(highs), 252)).max().iloc[-1])
            year_low = float(lows.rolling(window=min(len(lows), 252)).min().iloc[-1])

            info = {}
            try:
                # Fetch yfinance info with a timeout using threading
                from threading import Thread
                result_container = [{}]

                def fetch_info():
                    try:
                        ticker = yf.Ticker(symbol)
                        result_container[0] = ticker.info
                    except Exception:
                        result_container[0] = {}

                thread = Thread(target=fetch_info)
                thread.daemon = True
                thread.start()
                thread.join(timeout=10)  # 10 second timeout

                if thread.is_alive():
                    print(f"  - Warning: yfinance timeout for {symbol}, using empty info")
                    info = {}
                else:
                    info = result_container[0]
            except Exception as e:
                print(f"  - Warning: Could not fetch yfinance info for {symbol}: {e}")
                info = {}

            headlines = get_stock_specific_news_headlines(api, symbol)
            if not headlines:
                headlines = ["No material stock-specific headlines in the last 72 hours."]

            position = current_positions.get(symbol.upper())
            currently_held = position is not None
            current_qty = float(position.qty) if currently_held else 0.0
            current_value = float(position.market_value) if currently_held else 0.0
            current_weight = (current_value / portfolio_value) if (currently_held and portfolio_value) else 0.0
            prior_conviction = get_prior_conviction(symbol)

            return {
                "symbol": symbol,
                "company_name": info.get('shortName') or info.get('longName') or symbol,
                "fundamentals": {
                    "sector": info.get('sector', 'N/A'),
                    "industry": info.get('industry', 'N/A'),
                    "forward_pe": info.get('forwardPE', 'N/A'),
                    "trailing_pe": info.get('trailingPE', 'N/A'),
                    "market_cap": info.get('marketCap', 'N/A'),
                    "profit_margins": info.get('profitMargins', 'N/A')
                },
                "technicals": {
                    "latest_close": latest_close,
                    "one_day_change_pct": change_1d,
                    "twenty_day_change_pct": change_20d,
                    "sixty_day_change_pct": change_60d,
                    "sma_20": sma_20,
                    "sma_50": sma_50,
                    "sma_200": sma_200,
                    "rsi_14": rsi_14,
                    "fifty_two_week_high": year_high,
                    "fifty_two_week_low": year_low
                },
                "news_headlines": headlines,
                "stock_specific_headlines": " | ".join(headlines),
                "latest_price": latest_close,
                "historical_data": bars.to_json(orient='split'),
                "position_context": {
                    "currently_held": currently_held,
                    "current_shares": current_qty,
                    "current_value": current_value,
                    "current_weight": current_weight,
                    "prior_conviction": prior_conviction
                },
                "macro_context": {
                    "market_briefing": market_news_summary
                },
                "alt_data": {}
            }
    except Exception as e:
        logging.error(f"Error creating dossier for {symbol}: {e}")
        return None

def sanitize_conviction(raw_value):
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return 5
    value = max(1, min(10, value))
    return int(round(value))

def get_ai_analysis(dossier, market_context):
    """Get AI-powered buy/sell/hold decision for a stock using OpenAI GPT-4."""
    symbol = dossier['symbol']
    print(f"  - Getting AI analysis for {symbol}...")
    logging.debug(f"Requesting AI analysis for {symbol}")
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    analysis_payload = {
        "symbol": dossier.get("symbol"),
        "company_name": dossier.get("company_name"),
        "sector": dossier.get("fundamentals", {}).get("sector"),
        "industry": dossier.get("fundamentals", {}).get("industry"),
        "price": dossier.get("latest_price"),
        "market_cap": dossier.get("fundamentals", {}).get("market_cap"),
        "technicals": dossier.get("technicals", {}),
        "fundamentals": dossier.get("fundamentals", {}),
        "news_headlines": dossier.get("news_headlines", []),
        "alt_datas": dossier.get("alt_data", {}),
        "position_context": dossier.get("position_context", {}),
        "macro_context": {"market_briefing": market_context}
    }

    prompt = ANALYSIS_PROMPT_TEMPLATE.replace("<<PAYLOAD>>", json.dumps(analysis_payload, indent=2))

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            timeout=45.0
        )
        analysis = json.loads(response.choices[0].message.content)

        required_keys = {'symbol', 'decision', 'conviction', 'rationale'}
        if not required_keys.issubset(analysis.keys()):
            print(f"    - ERROR: AI response for {dossier['symbol']} missing keys -> {analysis.keys()}")
            return None

        decision = normalize_decision(analysis.get("decision"))
        conviction = sanitize_conviction(analysis.get("conviction"))

        rationale = analysis.get("rationale", [])
        if isinstance(rationale, list):
            rationale_text = " | ".join(str(item).strip() for item in rationale if item)
        else:
            rationale_text = str(rationale).strip()
        if not rationale_text:
            rationale_text = "No rationale provided."

        analysis["decision"] = decision
        analysis["conviction_score"] = conviction
        analysis["rationale"] = rationale_text

        logging.info(f"AI analysis for {symbol}: {decision} (conviction: {conviction})")
        logging.debug(f"AI rationale for {symbol}: {rationale_text}")
        return analysis
    except Exception as e:
        logging.error(f"Failed to get AI analysis for {dossier['symbol']}: {e}", exc_info=True)
        print(f"    - ERROR: Failed to get or parse AI analysis for {dossier['symbol']}: {e}")
        return None

def normalize_decision(decision_raw):
    if not decision_raw:
        return "HOLD"
    decision = decision_raw.strip().upper()
    if decision not in {"BUY", "SELL", "HOLD"}:
        return "HOLD"
    return decision

def fetch_latest_price_from_alpaca(api, symbol):
    try:
        latest_trade = api.get_latest_trade(symbol)
        return float(latest_trade.price)
    except Exception:
        return None

def prepare_decision_book(decisions, current_positions, api):
    decision_book = {}
    skipped_symbols = []

    for entry in decisions:
        symbol = entry.get("symbol", "").upper().strip()
        if not symbol:
            continue
        decision = normalize_decision(entry.get("decision"))
        conviction = sanitize_conviction(entry.get("conviction_score"))
        latest_price = entry.get("latest_price")

        if latest_price is None or latest_price == 0:
            if symbol in current_positions:
                latest_price = float(current_positions[symbol].current_price)
            if (latest_price is None or latest_price == 0) and api is not None:
                latest_price = fetch_latest_price_from_alpaca(api, symbol)

        if latest_price is None or latest_price <= 0:
            skipped_symbols.append(symbol)
            continue

        decision_book[symbol] = {
            "symbol": symbol,
            "decision": decision,
            "conviction_score": conviction,
            "rationale": entry.get("rationale", ""),
            "db_decision_id": entry.get("db_decision_id"),
            "latest_price": float(latest_price),
            "source": "ai"
        }

    if skipped_symbols:
        print("\nWARNING: Missing reliable price data for the following symbols; "
              "removed from today's plan:")
        print("  - " + ", ".join(sorted(set(skipped_symbols))))
    return decision_book

def display_decision_mix(decision_book):
    counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
    convictions = []
    for data in decision_book.values():
        counts[data["decision"]] += 1
        convictions.append(data["conviction_score"])
    print(f"\nAI Decision Mix -> BUY: {counts['BUY']} | SELL: {counts['SELL']} | HOLD: {counts['HOLD']}")
    if convictions:
        avg = sum(convictions) / len(convictions)
        hi = max(convictions)
        lo = min(convictions)
        print(f"Conviction stats -> avg: {avg:.2f} | range: {lo}-{hi}")

def ensure_minimum_positions(decision_book, current_positions):
    notes = []
    current_position_symbols = {sym.upper() for sym in current_positions.keys()}
    selected_symbols = set()

    for sym, data in decision_book.items():
        decision = data["decision"]
        if decision == "BUY":
            selected_symbols.add(sym)
        elif decision == "HOLD" and sym in current_position_symbols:
            selected_symbols.add(sym)

    if len(selected_symbols) >= MIN_POSITIONS:
        return selected_symbols, notes

    needed = MIN_POSITIONS - len(selected_symbols)
    print(f"\nEnforcing minimum position rule: need {MIN_POSITIONS}, "
          f"currently have {len(selected_symbols)}. Adding {needed} fallback holdings.")

    existing_sorted = sorted(
        current_positions.items(),
        key=lambda kv: float(kv[1].market_value),
        reverse=True
    )

    for symbol, position in existing_sorted:
        symbol = symbol.upper()
        if symbol in selected_symbols:
            continue

        latest_price = float(position.current_price)
        if symbol not in decision_book:
            decision_book[symbol] = {
                "symbol": symbol,
                "decision": "HOLD",
                "conviction_score": 4,
                "rationale": "Maintained to satisfy minimum position threshold.",
                "db_decision_id": None,
                "latest_price": latest_price,
                "source": "fallback"
            }
        else:
            decision_book[symbol]["decision"] = "HOLD"
            decision_book[symbol]["conviction_score"] = max(3, decision_book[symbol]["conviction_score"])
            decision_book[symbol]["rationale"] += " | Maintained to satisfy minimum position threshold."
            decision_book[symbol]["source"] = "fallback"

        selected_symbols.add(symbol)
        needed -= 1
        if needed == 0:
            break

    notes.append("Minimum position threshold applied; portfolio will retain at least "
                 f"{len(selected_symbols)} holdings.")
    return selected_symbols, notes

def enforce_position_limits(decision_book, selected_symbols):
    notes = []
    if len(selected_symbols) <= MAX_POSITIONS:
        return selected_symbols, notes

    print(f"\nApplying max position cap: target count {len(selected_symbols)} > {MAX_POSITIONS}.")
    ordered = sorted(
        [decision_book[sym] for sym in selected_symbols],
        key=lambda d: (d["conviction_score"], d["symbol"]),
        reverse=True
    )
    kept = ordered[:MAX_POSITIONS]
    dropped = ordered[MAX_POSITIONS:]

    selected_symbols = {entry["symbol"] for entry in kept}
    for entry in dropped:
        symbol = entry["symbol"]
        decision_book[symbol]["decision"] = "SELL"
        decision_book[symbol]["rationale"] += " | Set to SELL due to max position limit."
        decision_book[symbol]["source"] = "max_cap_forced"

    notes.append(f"Max position cap enforced: retained {len(selected_symbols)} highest-conviction holdings.")
    return selected_symbols, notes

def compute_target_allocations(decision_book, selected_symbols, portfolio_value, current_positions):
    investable_capital = portfolio_value * TARGET_INVESTED_RATIO
    max_position_value = portfolio_value * MAX_POSITION_PERCENTAGE
    notes = []

    allocations = {}
    base_total = 0.0

    for symbol in selected_symbols:
        data = decision_book[symbol]
        latest_price = data["latest_price"]
        current_qty = float(current_positions[symbol].qty) if symbol in current_positions else 0.0
        current_value = current_qty * latest_price
        capped_value = min(current_value, max_position_value)
        allocations[symbol] = capped_value
        base_total += capped_value
        if current_value > max_position_value + 1e-6:
            notes.append(
                f"{symbol} exceeds max position cap; trimming toward ${max_position_value:,.2f} target."
            )

    additional_capital = investable_capital - base_total
    buy_candidates = [
        sym for sym in selected_symbols
        if decision_book[sym]["decision"] == "BUY"
    ]

    if additional_capital > 1.0 and buy_candidates:
        active_buys = [
            sym for sym in buy_candidates
            if allocations.get(sym, 0.0) < max_position_value - 1e-6
        ]
        if not active_buys:
            notes.append("All BUY targets already at maximum cap; surplus retained as cash.")
        else:
            weights = {
                sym: conviction_to_weight(decision_book[sym]["conviction_score"])
                for sym in active_buys
            }
            total_weight = sum(weights.values())
            if total_weight == 0:
                for sym in active_buys:
                    weights[sym] = 1.0
                total_weight = len(active_buys)
                notes.append("Conviction scores for BUY targets summed to zero; defaulted to equal weighting.")

            remaining = additional_capital
            iteration_guard = 0
            while remaining > 1.0 and active_buys and iteration_guard < 20:
                iteration_guard += 1
                weight_total = sum(weights[sym] for sym in active_buys)
                if weight_total <= 0:
                    share_map = {sym: remaining / len(active_buys) for sym in active_buys}
                else:
                    share_map = {sym: remaining * (weights[sym] / weight_total) for sym in active_buys}

                overflow = 0.0
                for sym in list(active_buys):
                    proposed = allocations.get(sym, 0.0) + share_map[sym]
                    if proposed > max_position_value + 1e-6:
                        overflow += proposed - max_position_value
                        allocations[sym] = max_position_value
                        active_buys.remove(sym)
                    else:
                        allocations[sym] = proposed
                remaining = overflow

            if remaining > 1.0:
                notes.append("Unable to fully deploy BUY capital due to max position caps; residual left in cash.")
    elif additional_capital > 1.0 and not buy_candidates:
        notes.append("Hold-only plan detected; unused capital remains in cash due to lack of BUY signals.")
    elif additional_capital < -1.0:
        notes.append("Existing exposure exceeds 90% target; retaining surplus until SELL signals emerge.")

    invested_capital = sum(allocations.values())
    return allocations, notes, invested_capital

def build_trade_plan(decision_book, selected_symbols, allocations, current_positions, portfolio_value):
    trades = []
    target_positions = {}
    constraint_notes = []

    max_position_value = portfolio_value * MAX_POSITION_PERCENTAGE

    for symbol in selected_symbols:
        data = decision_book[symbol]
        latest_price = data["latest_price"]
        target_value = allocations.get(symbol, 0.0)
        target_value = min(target_value, max_position_value)

        current_qty = float(current_positions[symbol].qty) if symbol in current_positions else 0.0
        current_value = current_qty * latest_price

        if data["decision"] == "HOLD" and symbol in current_positions:
            target_qty = current_qty
            target_value = current_value
        else:
            target_qty = target_value / latest_price if latest_price > 0 else 0.0

        delta_value = target_value - current_value
        delta_qty = target_qty - current_qty

        if abs(delta_value) < MIN_TRADE_DOLLAR_THRESHOLD:
            action = "hold"
        elif delta_qty > 0:
            action = "buy"
        else:
            action = "sell"

        note = []
        if data.get("source") == "fallback":
            note.append("Maintained per minimum position constraint.")
        if data.get("source") == "max_cap_forced":
            note.append("Set to Sell due to max position limit.")
        if action == "buy" and current_qty == 0:
            note.append("Initiating new position.")
        elif action == "buy":
            note.append("Topping up to target weight.")
        elif action == "sell" and target_value <= 0:
            note.append("Full liquidation.")
        elif action == "sell":
            note.append("Trimming to target weight.")
        elif action == "hold":
            if current_qty > 0:
                note.append("Maintaining current weight.")
            else:
                note.append("No action required.")

        target_positions[symbol] = {
            "decision": data["decision"],
            "conviction_score": data["conviction_score"],
            "target_value": target_value,
            "target_shares": target_qty,
            "latest_price": latest_price,
            "note": " ".join(note).strip(),
            "db_decision_id": data.get("db_decision_id")
        }

        if action == "hold":
            continue

        trade = {
            "symbol": symbol,
            "side": action,
            "decision_id": data.get("db_decision_id"),
            "note": " ".join(note).strip(),
            "target_value": target_value,
            "target_shares": target_qty,
            "current_shares": current_qty,
            "latest_price": latest_price
        }

        if action == "buy":
            trade["order_type"] = "notional"
            trade["notional"] = round(abs(delta_value), 2)
            if trade["notional"] < MIN_TRADE_DOLLAR_THRESHOLD:
                continue
        else:
            # Handle sell orders
            if target_value <= 0 and current_qty > 0:
                # Full liquidation - use EXACT quantity from position to avoid remnants
                # Do NOT use floor_to_precision as it can leave tiny amounts unsold
                logging.debug(f"Full liquidation: {symbol} - selling exact qty {current_qty}")
                trade["order_type"] = "quantity"
                trade["quantity"] = f"{current_qty:.6f}"  # Exact quantity, no epsilon adjustment
            else:
                trade["order_type"] = "notional"
                trade["notional"] = round(abs(delta_value), 2)
                if trade["notional"] < MIN_TRADE_DOLLAR_THRESHOLD:
                    continue

        trades.append(trade)

    for symbol, position in current_positions.items():
        symbol = symbol.upper()
        if symbol in selected_symbols:
            continue
        latest_price = decision_book.get(symbol, {}).get("latest_price")
        if latest_price is None or latest_price <= 0:
            latest_price = float(position.current_price)

        current_qty = float(position.qty)
        current_value = current_qty * latest_price

        # Full liquidation for position not in target portfolio
        # Use EXACT quantity to ensure complete exit (no remnants)
        logging.debug(f"Liquidating {symbol} (not in target portfolio): exact qty {current_qty}")

        note = "Position not in target portfolio; exiting."
        trades.append({
            "symbol": symbol,
            "side": "sell",
            "order_type": "quantity",
            "quantity": f"{current_qty:.6f}",  # Exact quantity from position
            "notional": round(current_value, 2),
            "decision_id": decision_book.get(symbol, {}).get("db_decision_id"),
            "note": note,
            "target_value": 0.0,
            "target_shares": 0.0,
            "current_shares": current_qty,
            "latest_price": latest_price
        })
        target_positions[symbol] = {
            "decision": "SELL",
            "conviction_score": decision_book.get(symbol, {}).get("conviction_score", 5),
            "target_value": 0.0,
            "target_shares": 0.0,
            "latest_price": latest_price,
            "note": note,
            "db_decision_id": decision_book.get(symbol, {}).get("db_decision_id")
        }

    buy_symbols = {trade["symbol"] for trade in trades if trade["side"] == "buy"}
    sell_symbols = {trade["symbol"] for trade in trades if trade["side"] == "sell"}
    conflicts = buy_symbols & sell_symbols
    if conflicts:
        print("\n" + "*" * 72)
        print(SAME_DAY_CONFLICT_ERROR)
        print("Conflicting symbols:", ", ".join(sorted(conflicts)))
        print("*" * 72 + "\n")
        return None

    return {
        "trades": trades,
        "target_positions": target_positions,
        "constraint_notes": constraint_notes,
        "selected_symbols": selected_symbols,
        "allocations": allocations,
        "invested_capital": sum(allocations.values())
    }

def trade_sort_key(trade):
    return (
        0 if trade["side"] == "sell" else 1,
        0 if trade.get("order_type") == "quantity" else 1,
        trade["symbol"]
    )

def summarize_trade_plan(plan, current_positions_count, portfolio_value):
    allocations = plan["allocations"]
    trades = plan["trades"]
    sorted_trades = sorted(trades, key=trade_sort_key)

    buy_trades = [t for t in sorted_trades if t["side"] == "buy"]
    sell_trades = [t for t in sorted_trades if t["side"] == "sell"]

    buy_total = sum(t.get("notional", 0.0) for t in buy_trades)
    sell_total = sum(
        (t.get("notional") if t["order_type"] == "notional"
         else float(t["quantity"]) * t["latest_price"])
        for t in sell_trades
    )

    target_position_count = len(plan["selected_symbols"])
    target_invested = sum(allocations.values())
    projected_cash = portfolio_value - target_invested
    invested_ratio = (target_invested / portfolio_value * 100) if portfolio_value else 0

    return {
        "current_position_count": current_positions_count,
        "target_position_count": target_position_count,
        "buy_count": len(buy_trades),
        "sell_count": len(sell_trades),
        "buy_total": buy_total,
        "sell_total": sell_total,
        "projected_invested": target_invested,
        "projected_cash": projected_cash,
        "invested_ratio": invested_ratio,
        "constraint_notes": plan["constraint_notes"],
        "trades": sorted_trades,
        "target_positions": plan["target_positions"]
    }

def present_trade_plan(summary):
    print("\n--- [Stage 4: Trade Plan Summary] ---")
    print(f"Current positions: {summary['current_position_count']}")
    print(f"Target positions:  {summary['target_position_count']} (min {MIN_POSITIONS}, max {MAX_POSITIONS})")
    print(f"Planned BUY orders:  {summary['buy_count']} totaling ${summary['buy_total']:,.2f}")
    print(f"Planned SELL orders: {summary['sell_count']} totaling ${summary['sell_total']:,.2f}")
    print(f"Projected invested capital: ${summary['projected_invested']:,.2f} "
          f"({summary['invested_ratio']:.2f}% of portfolio)")
    print(f"Projected cash buffer:      ${summary['projected_cash']:,.2f}")

    if summary["invested_ratio"] > 90.5 or summary["invested_ratio"] < 89.0:
        print("  - NOTE: Invested ratio deviates slightly from 90% due to caps/rounding or HOLD preservation.")

    if summary["target_position_count"] > TARGET_POSITION_COUNT + 5:
        print(f"  - NOTE: Target holdings exceed soft goal of {TARGET_POSITION_COUNT}; "
              "convictions warranted additional positions.")
    elif summary["target_position_count"] < TARGET_POSITION_COUNT - 5:
        print(f"  - NOTE: Target holdings below soft goal of {TARGET_POSITION_COUNT}; "
              "market conditions produced fewer high conviction candidates.")

    if summary["constraint_notes"]:
        print("\nConstraint adjustments applied:")
        for note in summary["constraint_notes"]:
            print(f"  * {note}")

    if summary["trades"]:
        print("\nProposed Trades (per symbol):")
        for trade in summary["trades"]:
            side = trade["side"].upper()
            symbol = trade["symbol"]
            if trade["order_type"] == "notional":
                amount = f"${trade['notional']:,.2f}"
            else:
                amount = f"{float(trade['quantity']):,.6f} shares"
            note = f" | {trade['note']}" if trade.get("note") else ""
            print(f"  - {side} {symbol}: {amount}{note}")
    else:
        print("\nNo trades required. Portfolio already aligns with target configuration.")

def request_user_approval(plan_summary):
    """Request approval from UI or console, depending on mode."""
    print("\n--- [Manual Approval Required] ---")

    # If running in UI mode, delegate to UI bridge
    if ui_bridge.is_ui_mode():
        print("Waiting for approval from dashboard...")
        logging.info("Requesting approval via dashboard UI")
        return ui_bridge.wait_for_approval(plan_summary)

    # Otherwise, use console input
    print("Type 'APPROVE' to authorize this plan. Any other input cancels execution.")
    approval_input = input("Enter command: ")
    return approval_input.strip().upper() == 'APPROVE'

def log_decision_to_db(analysis, latest_price, market_context):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO decisions (
                timestamp,
                symbol,
                decision,
                conviction_score,
                rationale,
                latest_price,
                market_context_summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            analysis.get('symbol'),
            analysis.get('decision'),
            analysis.get('conviction_score'),
            analysis.get('rationale'),
            latest_price,
            market_context
        ))
        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"    - Logged decision for {analysis.get('symbol')} (ID: {decision_id}).")
        return decision_id
    except sqlite3.Error as e:
        print(f"    - DB_ERROR: Failed to log decision for {analysis.get('symbol')}: {e}")
        return None

def update_trade_log(trade_id, status, order_id=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE trades SET status = ?, alpaca_order_id = ? WHERE id = ?",
            (status, order_id, trade_id)
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"  - DB_ERROR: Failed to update trade log (ID {trade_id}): {e}")

def execute_trades(api, plan, current_positions):
    """Execute approved trades via Alpaca API or simulate in safe mode."""
    mode = "LIVE PAPER TRADING" if config.LIVE_TRADING else "SAFE MODE"
    print(f"\n--- [Stage 5: Trade Execution & Logging ({mode})] ---")
    logging.info(f"Stage 5: Beginning trade execution in {mode}")

    trades = plan.get("trades", [])
    if not trades:
        print("  - No trades to execute.")
        logging.info("No trades to execute")
        return

    logging.info(f"Executing {len(trades)} trades")
    trades = sorted(trades, key=trade_sort_key)

    for trade in trades:
        symbol = trade["symbol"]
        side = trade["side"].lower()
        order_type = trade["order_type"]
        decision_id = trade.get("decision_id")
        note = trade.get("note", "")

        order_details = {}
        displayed_amount = ""

        if order_type == "quantity":
            qty = float(trade["quantity"])
            order_details["qty"] = f"{qty:.6f}"
            displayed_amount = f"{qty:,.6f} shares"
        else:
            notional = float(trade["notional"])
            order_details["notional"] = round(notional, 2)
            displayed_amount = f"${order_details['notional']:,.2f}"

        trade_id = None
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            logged_amount = order_details.get('qty', order_details.get('notional', 0))
            cursor.execute("""
                INSERT INTO trades (decision_id, timestamp, symbol, side, quantity, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (decision_id, datetime.now(), symbol, side, logged_amount, 'approved'))
            trade_id = cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"  - Logged trade #{trade_id}: {side.upper()} {symbol} {displayed_amount} ({note})")
        except sqlite3.Error as e:
            print(f"  - DB_ERROR: Failed to log trade for {symbol}: {e}")
            continue

        try:
            if config.LIVE_TRADING:
                print(f"  - Submitting {side.upper()} order for {symbol} ({displayed_amount})...")
                logging.info(f"Submitting LIVE order: {side.upper()} {symbol} {displayed_amount}")
                order = api.submit_order(
                    symbol=symbol,
                    side=side,
                    time_in_force='day',
                    **order_details
                )
                print(f"  - SUCCESS (LIVE): Order ID {order.id}")
                logging.info(f"Order submitted successfully: {order.id} for {symbol}")
                update_trade_log(trade_id, 'submitted', order.id)
            else:
                latest_price = trade["latest_price"]
                if order_type == "quantity":
                    sim_qty = float(trade["quantity"])
                else:
                    sim_qty = order_details["notional"] / latest_price if latest_price > 0 else 0
                fake_order_id = f"sim_{int(time.time())}_{symbol}"
                logging.info(f"SAFE MODE simulation: {side.upper()} {symbol} {displayed_amount} ({sim_qty:.4f} shares)")
                print(f"  - [SAFE MODE] {side.upper()} {symbol}: {displayed_amount} "
                      f"(~{sim_qty:,.4f} shares @ ${latest_price:,.2f}) -> Fake Order {fake_order_id}")
                update_trade_log(trade_id, 'submitted', fake_order_id)
        except Exception as e:
            logging.error(f"Failed to submit order for {symbol}: {e}", exc_info=True)
            print(f"  - FAILED to submit order for {symbol}: {e}")
            update_trade_log(trade_id, 'execution_failed')

def generate_and_log_new_plan(api, current_positions, portfolio_value):
    """Generate a complete daily trading plan with AI analysis."""
    print("\n--- [Generating New Daily Plan] ---")
    logging.info("Beginning daily plan generation")

    candidate_universe = generate_candidate_universe(current_positions.keys())

    # Graceful degradation: If news fetching fails, continue with generic context
    try:
        raw_news_data = get_raw_search_results_from_perplexity()
        market_context = summarize_market_context_with_openAI(raw_news_data)
    except Exception as e:
        logging.error(f"News gathering failed, using fallback context: {e}")
        print(f"  - WARNING: News gathering failed. Continuing with generic market context.")
        market_context = (
            "Market news unavailable for this analysis. "
            "Proceeding with technical and fundamental data only. "
            f"Analysis date: {datetime.now().strftime('%Y-%m-%d')}"
        )

    dossiers = aggregate_data_dossiers(api, candidate_universe, market_context, current_positions, portfolio_value)

    print("\n--- [Stage 3: AI-Powered Analysis & Logging] ---")
    decisions = []

    if dossiers:
        for symbol in sorted(dossiers.keys()):
            dossier = dossiers[symbol]
            analysis = get_ai_analysis(dossier, market_context)
            if analysis:
                analysis["latest_price"] = dossier.get("latest_price")
                decision_id = log_decision_to_db(analysis, dossier.get("latest_price"), market_context)
                analysis["db_decision_id"] = decision_id
                decisions.append(analysis)
            time.sleep(2)
    else:
        print("No dossiers were created; skipping AI analysis.")

    return decisions, dossiers

def main():
    # Initialize logging first
    log_file = setup_logging()

    print("====== Sentinel Daily Run Initialized ======")
    print(f"[CONFIG] LIVE_TRADING={config.LIVE_TRADING} | "
          f"ALLOW_DEV_RERUNS={getattr(config, 'ALLOW_DEV_RERUNS', False)} | "
          f"TARGET_INVESTED_RATIO={TARGET_INVESTED_RATIO:.2f}")
    print(f"[LOG] Session log: {log_file}")

    logging.info("="*80)
    logging.info("SENTINEL DAILY RUN STARTED")
    logging.info(f"Version: 7.8")
    logging.info(f"Live Trading: {config.LIVE_TRADING}")
    logging.info(f"UI Mode: {ui_bridge.is_ui_mode()}")
    logging.info(f"Target Invested Ratio: {TARGET_INVESTED_RATIO:.2%}")
    logging.info("="*80)

    # Create database backup before proceeding
    print("\n--- [Backing up database] ---")
    backup_success = backup_database.run_backup_maintenance()
    if not backup_success:
        logging.warning("Database backup failed, but continuing with run")
        print("WARNING: Database backup failed. Continuing anyway...")

    if check_if_trades_executed_today():
        print("\nTrading has already been executed for today. See you tomorrow!")
        logging.info("Run terminated: Trades already executed today")
        print("\n====== Sentinel Daily Run Finished ======")
        logging.info("="*80)
        logging.info("SENTINEL DAILY RUN FINISHED")
        logging.info("="*80)
        return

    alpaca_api = get_alpaca_api()
    current_positions, account = get_account_info(alpaca_api)

    if not account:
        print("\nCould not retrieve account info. Aborting run.")
        return

    # Abort checkpoint: After account info retrieval
    if ui_bridge.check_abort_safe_point("Account Info"):
        print("\n[ABORTED] User requested stop.")
        logging.warning("Run aborted by user at Account Info stage")
        return

    portfolio_value = float(account.portfolio_value)
    display_performance_report(alpaca_api, portfolio_value)

    decisions = get_todays_decisions()
    decisions = maybe_regenerate_plan(decisions)
    dossiers = {}

    if decisions:
        unique_symbols = len({d["symbol"].upper() for d in decisions})
        print(f"\n[INFO] Reusing stored plan for today covering {unique_symbols} symbols.")
    else:
        print("\nNo existing plan found for today. Generating a new one...")
        decisions, dossiers = generate_and_log_new_plan(alpaca_api, current_positions, portfolio_value)

    # Abort checkpoint: After plan generation
    if ui_bridge.check_abort_safe_point("Plan Generation"):
        print("\n[ABORTED] User requested stop.")
        logging.warning("Run aborted by user after Plan Generation")
        return

    if not decisions:
        print("\nNo actionable decisions were produced. Concluding run.")
        print("\n====== Sentinel Daily Run Finished ======")
        return

    decision_book = prepare_decision_book(decisions, current_positions, alpaca_api)
    if not decision_book:
        print("\nUnable to assemble decision book (missing prices). Aborting run.")
        print("\n====== Sentinel Daily Run Finished ======")
        return

    display_decision_mix(decision_book)

    selected_symbols, notes_min = ensure_minimum_positions(decision_book, current_positions)
    selected_symbols, notes_max = enforce_position_limits(decision_book, selected_symbols)

    allocations, allocation_notes, invested_capital = compute_target_allocations(
        decision_book, selected_symbols, portfolio_value, current_positions
    )

    plan = build_trade_plan(
        decision_book,
        selected_symbols,
        allocations,
        current_positions,
        portfolio_value
    )

    if plan is None:
        print("\nPlan aborted due to safeguard trigger. No trades executed.")
        print("\n====== Sentinel Daily Run Finished ======")
        return

    plan["constraint_notes"].extend(notes_min + notes_max + allocation_notes)

    # Abort checkpoint: Before trade approval
    if ui_bridge.check_abort_safe_point("Trade Plan Review"):
        print("\n[ABORTED] User requested stop.")
        logging.warning("Run aborted by user before Trade Plan Review")
        return

    summary = summarize_trade_plan(
        plan,
        current_positions_count=len(current_positions),
        portfolio_value=portfolio_value
    )
    plan["summary"] = summary

    present_trade_plan(summary)

    approved = request_user_approval(summary)
    if approved:
        logging.info("User approved trade plan - proceeding with execution")
        execute_trades(alpaca_api, plan, current_positions)
    else:
        print("\n--- [Trade Execution Halted] ---")
        print("  - Plan not approved; no trades executed.")
        logging.warning("User rejected trade plan - no trades executed")

    print("\n====== Sentinel Daily Run Finished ======")
    logging.info("="*80)
    logging.info("SENTINEL DAILY RUN FINISHED")
    logging.info("="*80)

if __name__ == "__main__":
    main()