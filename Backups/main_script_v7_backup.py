# main_script.py
# Version 7.0 - Portfolio Guardrails & Plan Transparency

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

# --- Global Constants ---
DB_FILE = "sentinel.db"

# --- Capital Allocation Rules from Charter ---
TARGET_INVESTED_RATIO = 0.90   # Invest 90% of total portfolio value
MAX_POSITION_PERCENTAGE = 0.10 # No single position may exceed 10% of the portfolio

# --- Position Count Guardrails ---
MIN_POSITIONS = 10
MAX_POSITIONS = 100
TARGET_POSITION_COUNT = 80     # Soft target, not a hard cap

# --- Trading Safeguards ---
MIN_TRADE_DOLLAR_THRESHOLD = 25.0  # Ignore miniscule trades
SAME_DAY_CONFLICT_ERROR = (
    "SAFEGUARD TRIGGERED: The trade plan attempted to both buy and sell the same symbol "
    "in a single run. No trades will be executed. Please share the log with the developer."
)

# --- Stage -1: Daily State Check ---
def check_if_trades_executed_today():
    """Checks the DB to see if any trades were already submitted today."""
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
        return result is not None
    except sqlite3.Error as e:
        print(f"DB_ERROR checking for executed trades: {e}")
        return False

def get_todays_decisions():
    """
    Returns all AI decisions stored for today (Buy, Sell, Hold).
    Each entry contains: id, symbol, decision, conviction_score, rationale, latest_price.
    """
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

# --- Stage 0: System Initialization & State Review ---
def get_alpaca_api():
    return tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

def get_account_info(api):
    print("--- [Stage 0: Account & Position Review] ---")
    try:
        account = api.get_account()
        portfolio_value = float(account.portfolio_value)
        print(f"Account is {'ACTIVE' if account.status == 'ACTIVE' else account.status}. "
              f"Portfolio Value: ${portfolio_value:,.2f}")
        positions = api.list_positions()
        if positions:
            print(f"Current Positions ({len(positions)}):")
            for pos in positions:
                qty = float(pos.qty)
                avg_price = float(pos.avg_entry_price)
                market_value = float(pos.market_value)
                print(f"  - {pos.symbol}: {qty:.6f} shares @ avg ${avg_price:,.2f} "
                      f"(Value: ${market_value:,.2f})")
        else:
            print("No open positions.")
        position_map = {p.symbol.upper(): p for p in positions}
        return position_map, account
    except Exception as e:
        print(f"Error connecting to Alpaca: {e}")
        return {}, None

def display_performance_report(api, current_value):
    """Fetches portfolio history and displays Daily and YTD performance."""
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

        today = datetime.now()
        start_of_year_str = f"{today.year}-01-01"
        ytd_hist = api.get_portfolio_history(date_start=start_of_year_str, timeframe='1D')

        if len(ytd_hist.equity) > 0:
            ytd_start_value = next((val for val in ytd_hist.equity if val is not None and val > 0), 0)

            if ytd_start_value > 0:
                ytd_pl = current_value - ytd_start_value
                ytd_pl_pct = (ytd_pl / ytd_start_value) * 100
                print(f"  - YTD P/L:      ${ytd_pl:,.2f} ({ytd_pl_pct:+.2f}%)")
            else:
                print("  - YTD P/L:      $0.00 (Not enough history for YTD %)")
        else:
            print("  - YTD P/L:      Not enough history to calculate.")

    except Exception as e:
        print(f"  - Could not generate performance report: {e}")
        print("  - This may be due to a new account with insufficient history.")

# --- Stage 1: Candidate Universe Generation ---
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

# --- Stage 2: Data Dossier Aggregation ---
def get_raw_search_results_from_perplexity():
    print("\n--- [News Gathering Step 1: Searching via Perplexity] ---")
    try:
        url = "https://api.perplexity.ai/search"
        payload = {"query": "Top 15-20 most significant, market-moving financial news stories last 24 hours"}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {config.PERPLEXITY_API_KEY}"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=20.0)
        response.raise_for_status()
        print("  - Successfully fetched raw search results from Perplexity.")
        return response.json()
    except Exception as e:
        print(f"  - ERROR fetching from Perplexity /search: {e}")
        return None

def summarize_market_context_with_openai(raw_results):
    print("--- [News Gathering Step 2: Summarizing via OpenAI] ---")
    if not raw_results:
        return "Could not retrieve general market news."
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        prompt = (
            "You are a financial news analyst. Summarize the key market-moving stories from the "
            "following dataset into a concise briefing (5 bullet points max). "
            "Highlight major risk factors and sentiment. Dataset:\n"
            f"{json.dumps(raw_results, indent=2)}"
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
        return " | ".join([article.headline for article in news]) if news else "No recent stock-specific news headlines found."
    except Exception:
        return "Error fetching stock-specific headlines."

def aggregate_data_dossiers(api, universe, market_news_summary):
    print("\n--- [Stage 2: Data Dossier Aggregation] ---")
    dossiers = {}
    print(f"*** Analyzing the full universe of {len(universe)} stocks. ***")
    for i, symbol in enumerate(universe):
        print(f"Aggregating data for {symbol} ({i+1}/{len(universe)})...")
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            bars = api.get_bars(
                symbol,
                '1Day',
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                feed=config.APCA_API_DATA_FEED
            ).df
            if bars.empty:
                print(f"  - No price data found for {symbol}; skipping.")
                continue
            info = yf.Ticker(symbol).info
            dossiers[symbol] = {
                "symbol": symbol,
                "fundamentals": {
                    "sector": info.get('sector', 'N/A'),
                    "forward_pe": info.get('forwardPE', 'N/A')
                },
                "historical_data": bars.to_json(orient='split'),
                "stock_specific_headlines": get_stock_specific_news_headlines(api, symbol),
                "latest_price": float(bars.iloc[-1]['close'])
            }
            print(f"  - Successfully created dossier for {symbol}.")
            time.sleep(1)
        except Exception as e:
            print(f"  - Failed to create dossier for {symbol}: {e}")
    print(f"\nSuccessfully aggregated {len(dossiers)} data dossiers.")
    return dossiers

# --- Stage 3: AI-Powered Analysis ---
def get_ai_analysis(dossier, market_context):
    print(f"  - Getting AI analysis for {dossier['symbol']}...")
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    try:
        df = pd.read_json(StringIO(dossier['historical_data']), orient='split')
        sma_50 = df['close'].rolling(window=50).mean().iloc[-1]
        sma_200 = df['close'].rolling(window=200).mean().iloc[-1]
        technical_signal = "Golden Cross (Bullish)" if sma_50 > sma_200 else "Death Cross (Bearish)"
    except Exception:
        technical_signal = "Could not calculate technical signal."

    system_prompt = (
        "You are a disciplined quantitative analyst. Use the provided data to issue a portfolio forecast."
        " Apply the following guidelines:\n"
        " - Return decisions only in JSON.\n"
        " - Use the full conviction scale: 1 (very weak) to 10 (very strong).\n"
        " - 'Hold' means maintain approximately the current stake.\n"
        " - 'Sell' means reduce to zero unless the human overrides you.\n"
        " - Be decisive; aim to differentiate across the universe."
    )

    user_prompt = f"""
    Evaluate {dossier['symbol']} using the dossier and market context below.

    MARKET CONTEXT SUMMARY:
    {market_context}

    STOCK DOSSIER:
    - Sector: {dossier['fundamentals'].get('sector')}
    - Forward P/E: {dossier['fundamentals'].get('forward_pe')}
    - Technical Signal: {technical_signal}
    - Stock-Specific Headlines: {dossier['stock_specific_headlines']}

    Expectations:
    - decision ? {{ "Buy", "Sell", "Hold" }}
    - conviction_score ? [1, 10], integer
    - Keep rationale to 2-3 sentences.

    Return ONLY the JSON object, e.g.:
    {{
        "symbol": "XYZ",
        "decision": "Buy",
        "conviction_score": 9,
        "rationale": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            timeout=30.0
        )
        analysis = json.loads(response.choices[0].message.content)

        required_keys = {'symbol', 'decision', 'conviction_score', 'rationale'}
        if not required_keys.issubset(analysis.keys()):
            print(f"    - ERROR: AI response for {dossier['symbol']} missing keys -> {analysis.keys()}")
            return None

        if isinstance(analysis['rationale'], list):
            analysis['rationale'] = ' '.join(map(str, analysis['rationale']))

        return analysis
    except Exception as e:
        print(f"    - ERROR: Failed to get or parse AI analysis for {dossier['symbol']}: {e}")
        return None

# --- Stage 4 Helpers: Portfolio Guardrails & Plan Construction ---
def normalize_decision(decision_raw):
    if not decision_raw:
        return "HOLD"
    decision = decision_raw.strip().upper()
    if decision not in {"BUY", "SELL", "HOLD"}:
        return "HOLD"
    return decision

def sanitize_conviction(raw_value):
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return 5
    value = max(1, min(10, value))
    return int(round(value))

def fetch_latest_price_from_alpaca(api, symbol):
    try:
        latest_trade = api.get_latest_trade(symbol)
        return float(latest_trade.price)
    except Exception:
        return None

def prepare_decision_book(decisions, current_positions, api):
    """
    Builds a dictionary keyed by symbol with standardized decision metadata.
    Ensures we have a usable latest_price for each symbol (fall back to Alpaca if needed).
    """
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
              "they were removed from today's plan:")
        print("  - " + ", ".join(sorted(set(skipped_symbols))))
    return decision_book

def ensure_minimum_positions(decision_book, current_positions):
    """
    Guarantees at least MIN_POSITIONS symbols remain in the target set.
    Returns (selected_symbols, notes)
    """
    notes = []
    selected_symbols = {sym for sym, data in decision_book.items()
                        if data["decision"] in {"BUY", "HOLD"}}

    if len(selected_symbols) >= MIN_POSITIONS:
        return selected_symbols, notes

    needed = MIN_POSITIONS - len(selected_symbols)
    print(f"\nEnforcing minimum position rule: need {MIN_POSITIONS}, "
          f"currently have {len(selected_symbols)}. Adding {needed} fallback holdings.")

    # Sort current positions by market value descending
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
    """
    Ensures we do not exceed MAX_POSITIONS.
    Returns (selected_symbols, notes)
    """
    notes = []
    if len(selected_symbols) <= MAX_POSITIONS:
        return selected_symbols, notes

    print(f"\nApplying max position cap: current target count {len(selected_symbols)} > {MAX_POSITIONS}.")
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
        decision_book[symbol]["rationale"] += " | Trimmed due to max position limit."
        decision_book[symbol]["source"] = "max_cap_forced"

    notes.append(f"Max position cap enforced: retained {len(selected_symbols)} highest-conviction holdings.")
    return selected_symbols, notes

def compute_target_allocations(decision_book, selected_symbols, portfolio_value):
    """
    Returns (allocations_dict, notes, invested_capital).
    allocations_dict maps symbol -> target dollar value (<= investable capital and <= max position cap).
    """
    investable_capital = portfolio_value * TARGET_INVESTED_RATIO
    max_position_value = portfolio_value * MAX_POSITION_PERCENTAGE
    notes = []

    # Collect convictions for allocation
    convictions = {}
    for symbol in selected_symbols:
        conviction = decision_book[symbol]["conviction_score"]
        convictions[symbol] = max(1, conviction)

    total_conviction = sum(convictions.values())
    if total_conviction == 0:
        # fallback: equal weight
        for symbol in selected_symbols:
            convictions[symbol] = 1
        total_conviction = len(selected_symbols)
        notes.append("Conviction scores were zero; defaulted to equal weighting.")

    # Initial allocation proportional to conviction
    allocations = {
        symbol: investable_capital * (convictions[symbol] / total_conviction)
        for symbol in selected_symbols
    }

    # Enforce max-position cap iteratively
    max_cap = max_position_value
    iteration_guard = 0
    while iteration_guard < 20:
        iteration_guard += 1
        over_allocated = [sym for sym, value in allocations.items() if value > max_cap + 1e-6]
        if not over_allocated:
            break

        surplus = sum(allocations[sym] - max_cap for sym in over_allocated)
        for sym in over_allocated:
            allocations[sym] = max_cap

        eligible = [sym for sym in allocations if sym not in over_allocated]
        if not eligible or surplus <= 1:
            notes.append("Unable to fully distribute capital due to max position caps; "
                         "excess kept as cash buffer.")
            break

        eligible_conv_sum = sum(convictions[sym] for sym in eligible)
        for sym in eligible:
            share = surplus * (convictions[sym] / eligible_conv_sum)
            allocations[sym] += share

    invested_capital = sum(allocations.values())
    if invested_capital < investable_capital * 0.985:
        notes.append("Investable capital not fully allocated (likely due to caps or rounding). "
                     "Cash buffer will be slightly above 10%.")

    return allocations, notes, invested_capital

def build_trade_plan(decision_book, selected_symbols, allocations, current_positions, portfolio_value):
    """
    Constructs the final trade plan (buys/sells) and post-trade state.
    Returns plan dictionary:
        - trades: list of trade instructions (order_type, notional/qty)
        - target_positions: map symbol -> target details
        - constraint_notes: list of text notes applied during planning
    """
    trades = []
    target_positions = {}
    constraint_notes = []

    invested_capital = sum(allocations.values())
    max_position_value = portfolio_value * MAX_POSITION_PERCENTAGE

    for symbol in selected_symbols:
        data = decision_book[symbol]
        latest_price = data["latest_price"]
        target_value = allocations.get(symbol, 0.0)
        target_value = min(target_value, max_position_value)
        target_qty = target_value / latest_price if latest_price > 0 else 0

        current_qty = float(current_positions[symbol].qty) if symbol in current_positions else 0.0
        current_value = current_qty * latest_price
        delta_value = target_value - current_value
        delta_qty = target_qty - current_qty

        # Determine action
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
        else:  # sell
            if target_value <= 0 and current_qty > 0:
                trade["order_type"] = "quantity"
                trade["quantity"] = str(round(current_qty, 6))
            else:
                trade["order_type"] = "notional"
                trade["notional"] = round(abs(delta_value), 2)
                if trade["notional"] < MIN_TRADE_DOLLAR_THRESHOLD:
                    continue

        trades.append(trade)

    # Ensure we liquidate any remaining positions not selected
    for symbol, position in current_positions.items():
        symbol = symbol.upper()
        if symbol in selected_symbols:
            continue
        latest_price = decision_book.get(symbol, {}).get("latest_price")
        if latest_price is None or latest_price <= 0:
            latest_price = float(position.current_price)

        current_qty = float(position.qty)
        current_value = current_qty * latest_price
        if current_value < MIN_TRADE_DOLLAR_THRESHOLD:
            continue

        note = "Position not in target portfolio; exiting."
        trades.append({
            "symbol": symbol,
            "side": "sell",
            "order_type": "quantity",
            "quantity": str(round(current_qty, 6)),
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

    # Safety check: ensure no buy/sell conflicts for a symbol
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
        "invested_capital": invested_capital
    }

def summarize_trade_plan(plan, current_positions_count, portfolio_value):
    allocations = plan["allocations"]
    trades = plan["trades"]

    buy_trades = [t for t in trades if t["side"] == "buy"]
    sell_trades = [t for t in trades if t["side"] == "sell"]

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
        "trades": trades,
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
        print("  - NOTE: Invested ratio deviates slightly from 90% due to caps/rounding.")

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

def request_user_approval():
    print("\n--- [Manual Approval Required] ---")
    print("Type 'APPROVE' to authorize this plan. Any other input cancels execution.")
    approval_input = input("Enter command: ")
    return approval_input.strip().upper() == 'APPROVE'

# --- Stage 4: Database Logging ---
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

# --- Stage 5: Execution ---
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
    mode = "LIVE PAPER TRADING" if config.LIVE_TRADING else "SAFE MODE"
    print(f"\n--- [Stage 5: Trade Execution & Logging ({mode})] ---")

    trades = plan.get("trades", [])
    if not trades:
        print("  - No trades to execute.")
        return

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
            order_details["qty"] = str(round(qty, 6))
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
                order = api.submit_order(
                    symbol=symbol,
                    side=side,
                    time_in_force='day',
                    **order_details
                )
                print(f"  - SUCCESS (LIVE): Order ID {order.id}")
                update_trade_log(trade_id, 'submitted', order.id)
            else:
                latest_price = trade["latest_price"]
                if order_type == "quantity":
                    sim_qty = float(trade["quantity"])
                else:
                    sim_qty = order_details["notional"] / latest_price if latest_price > 0 else 0
                fake_order_id = f"sim_{int(time.time())}_{symbol}"
                print(f"  - [SAFE MODE] {side.upper()} {symbol}: {displayed_amount} "
                      f"(~{sim_qty:,.4f} shares @ ${latest_price:,.2f}) -> Fake Order {fake_order_id}")
                update_trade_log(trade_id, 'submitted', fake_order_id)
        except Exception as e:
            print(f"  - FAILED to submit order for {symbol}: {e}")
            update_trade_log(trade_id, 'execution_failed')

# --- Stage 3 & 4 Orchestration ---
def generate_and_log_new_plan(api, current_positions):
    print("\n--- [Generating New Daily Plan] ---")
    candidate_universe = generate_candidate_universe(current_positions.keys())
    raw_news_data = get_raw_search_results_from_perplexity()
    market_context = summarize_market_context_with_openai(raw_news_data)
    dossiers = aggregate_data_dossiers(api, candidate_universe, market_context)

    print("\n--- [Stage 3: AI-Powered Analysis & Logging] ---")
    decisions = []

    if dossiers:
        for symbol, dossier in dossiers.items():
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

# --- Main Execution Workflow ---
def main():
    print("====== Sentinel Daily Run Initialized ======")

    if check_if_trades_executed_today():
        print("\nTrading has already been executed for today. See you tomorrow!")
        print("\n====== Sentinel Daily Run Finished ======")
        return

    alpaca_api = get_alpaca_api()
    current_positions, account = get_account_info(alpaca_api)

    if not account:
        print("\nCould not retrieve account info. Aborting run.")
        return

    portfolio_value = float(account.portfolio_value)
    display_performance_report(alpaca_api, portfolio_value)

    decisions = get_todays_decisions()
    dossiers = {}

    if decisions:
        print("\nFound a previously generated plan for today. Reusing stored decisions.")
    else:
        print("\nNo existing plan found for today. Generating a new one...")
        decisions, dossiers = generate_and_log_new_plan(alpaca_api, current_positions)

    if not decisions:
        print("\nNo actionable decisions were produced. Concluding run.")
        print("\n====== Sentinel Daily Run Finished ======")
        return

    decision_book = prepare_decision_book(decisions, current_positions, alpaca_api)
    if not decision_book:
        print("\nUnable to assemble decision book (missing prices). Aborting run.")
        print("\n====== Sentinel Daily Run Finished ======")
        return

    selected_symbols, notes_min = ensure_minimum_positions(decision_book, current_positions)
    selected_symbols, notes_max = enforce_position_limits(decision_book, selected_symbols)

    allocations, allocation_notes, invested_capital = compute_target_allocations(
        decision_book, selected_symbols, portfolio_value
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

    summary = summarize_trade_plan(
        plan,
        current_positions_count=len(current_positions),
        portfolio_value=portfolio_value
    )
    plan["summary"] = summary

    present_trade_plan(summary)

    approved = request_user_approval()
    if approved:
        execute_trades(alpaca_api, plan, current_positions)
    else:
        print("\n--- [Trade Execution Halted] ---")
        print("  - Plan not approved; no trades executed.")

    print("\n====== Sentinel Daily Run Finished ======")

if __name__ == "__main__":
    main()