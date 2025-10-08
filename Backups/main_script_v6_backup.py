# main_script.py
# Version 6.2 - API COMPLIANCE FIX
# Rounds notional trade values to 2 decimal places to meet Alpaca API requirements.

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
TARGET_INVESTED_RATIO = 0.90  # Invest 90% of total portfolio value
MAX_POSITION_PERCENTAGE = 0.10 # No single position should exceed 10% of the portfolio

# --- STAGE -1: DAILY STATE CHECK ---
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

def get_todays_proposed_plan():
    """
    Checks the DB for a plan that was proposed but not executed today.
    Now also fetches the price at the time of decision to avoid re-aggregation.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, symbol, decision, conviction_score, rationale, latest_price FROM decisions
            WHERE DATE(timestamp) = DATE('now', 'localtime')
            AND decision IN ('Buy', 'Sell')
        """)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows: return []

        proposed_trades = [{'db_decision_id': r['id'], 'symbol': r['symbol'], 'decision': r['decision'],
                            'conviction_score': r['conviction_score'], 'rationale': r['rationale'],
                            'latest_price': r['latest_price']} for r in rows]
        return proposed_trades
    except sqlite3.Error as e:
        print(f"DB_ERROR getting today's proposed plan: {e}")
        return []

# --- Stage 0: System Initialization & State Review ---
def get_alpaca_api():
    return tradeapi.REST(config.APCA_API_KEY_ID, config.APCA_API_SECRET_KEY, config.APCA_API_BASE_URL, api_version='v2')

def get_account_info(api):
    print("--- [Stage 0: Account & Position Review] ---")
    try:
        account = api.get_account()
        print(f"Account is {'ACTIVE' if account.status == 'ACTIVE' else account.status}. Portfolio Value: ${float(account.portfolio_value):,.2f}")
        positions = api.list_positions()
        if positions:
            print(f"Current Positions ({len(positions)}):")
            for pos in positions:
                print(f"  - {pos.symbol}: {pos.qty} shares @ avg ${float(pos.avg_entry_price):,.2f} (Value: ${float(pos.market_value):,.2f})")
        else:
            print("No open positions.")
        return {p.symbol: p for p in positions}, account
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
                print(f"  - YTD P/L:      $0.00 (Not enough history for YTD %)")
        else:
            print("  - YTD P/L:      Not enough history to calculate.")

    except Exception as e:
        print(f"  - Could not generate performance report: {e}")
        print("  - This may be due to a new account with insufficient history.")

# --- Stage 1: Candidate Universe Generation ---
def generate_and_log_new_plan(api, current_positions):
    print("\n--- [Generating New Daily Plan] ---")
    candidate_universe = generate_candidate_universe(current_positions.keys())
    raw_news_data = get_raw_search_results_from_perplexity()
    market_context = summarize_market_context_with_openai(raw_news_data)
    all_dossiers = aggregate_data_dossiers(api, candidate_universe, market_context)
    
    print("\n--- [Stage 3: AI-Powered Analysis & Logging] ---")
    all_analyses = []
    if all_dossiers:
        for symbol, dossier in all_dossiers.items():
            analysis = get_ai_analysis(dossier, market_context)
            if analysis:
                decision_id = log_decision_to_db(analysis, dossier.get('latest_price'), market_context)
                if decision_id:
                    analysis['db_decision_id'] = decision_id
                all_analyses.append(analysis)
            time.sleep(2)
    else:
        print("No dossiers were created, skipping AI analysis.")
    
    proposed_trades = [an for an in all_analyses if an.get('decision', 'N/A').lower() in ['buy', 'sell']]
    return proposed_trades, all_dossiers

def get_nasdaq_100_symbols():
    print("  - Fetching Nasdaq 100 constituents...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        nasdaq_100_df = next(table for table in tables if 'Ticker' in table.columns)
        symbols = [s.replace('.', '-') for s in nasdaq_100_df['Ticker'].tolist()]
        print(f"  - Successfully fetched {len(symbols)} symbols.")
        return symbols
    except Exception as e:
        print(f"  - ERROR: Could not fetch Nasdaq 100 list: {e}")
        return ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL', 'AMZN', 'META']

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
        headers = { "accept": "application/json", "content-type": "application/json", "authorization": f"Bearer {config.PERPLEXITY_API_KEY}" }
        response = requests.post(url, json=payload, headers=headers, timeout=20.0)
        response.raise_for_status()
        print("  - Successfully fetched raw search results from Perplexity.")
        return response.json()
    except Exception as e:
        print(f"  - ERROR fetching from Perplexity /search: {e}")
        return None

def summarize_market_context_with_openai(raw_results):
    print("--- [News Gathering Step 2: Summarizing via OpenAI] ---")
    if not raw_results: return "Could not retrieve general market news."
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        prompt = f"""You are a financial news analyst... RAW SEARCH DATA: {json.dumps(raw_results, indent=2)}"""
        response = client.chat.completions.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}], timeout=45.0)
        print("  - Successfully summarized market news using OpenAI.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"  - ERROR summarizing news with OpenAI: {e}")
        return "Could not summarize general market news."

def get_stock_specific_news_headlines(api, symbol):
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=3)
        news = api.get_news(symbol=symbol, start=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), end=end_time.strftime('%Y-%m-%dT%H:%M:%SZ'), limit=5)
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
            bars = api.get_bars(symbol, '1Day', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), feed=config.APCA_API_DATA_FEED).df
            if bars.empty: continue
            info = yf.Ticker(symbol).info
            dossiers[symbol] = {
                "symbol": symbol, "fundamentals": {"sector": info.get('sector', 'N/A'), "forward_pe": info.get('forwardPE', 'N/A')},
                "historical_data": bars.to_json(orient='split'), "stock_specific_headlines": get_stock_specific_news_headlines(api, symbol),
                "latest_price": bars.iloc[-1]['close']
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
    
    system_prompt = "You are a quantitative analyst providing a trade recommendation."
    user_prompt = f"""
    Please analyze the stock {dossier['symbol']}... Return a JSON object with four specific keys:
    1. "symbol": A string, which must be exactly "{dossier['symbol']}".
    2. "decision": A string, which must be one of "Buy", "Sell", or "Hold".
    3. "conviction_score": An integer from 1 to 10.
    4. "rationale": A single string explaining your reasoning in 2-3 sentences.
    Output only the raw JSON object and nothing else.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            response_format={"type": "json_object"}, timeout=30.0
        )
        analysis = json.loads(response.choices[0].message.content)

        if not all(k in analysis for k in ['symbol', 'decision', 'conviction_score', 'rationale']):
            print(f"    - ERROR: AI response for {dossier['symbol']} was missing required keys.")
            return None
        
        if isinstance(analysis['rationale'], list):
            analysis['rationale'] = ' '.join(map(str, analysis['rationale']))

        return analysis
    except Exception as e:
        print(f"    - ERROR: Failed to get or parse AI analysis for {dossier['symbol']}: {e}")
        return None

# --- STAGE 4: DATABASE, APPROVAL & EXECUTION ---
def log_decision_to_db(analysis, latest_price, market_context):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO decisions (timestamp, symbol, decision, conviction_score, rationale, latest_price, market_context_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (datetime.now(), analysis.get('symbol'), analysis.get('decision'), analysis.get('conviction_score'), 
              analysis.get('rationale'), latest_price, market_context))
        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"    - Successfully logged decision for {analysis.get('symbol')} to DB (ID: {decision_id}).")
        return decision_id
    except sqlite3.Error as e:
        print(f"    - DB_ERROR: Failed to log decision for {analysis.get('symbol')}: {e}")
        return None

def handle_approval_process(proposed_trades):
    print("\n--- [Stage 4: Trade Approval] ---")
    if not proposed_trades:
        print("  - No actionable trades proposed. Skipping approval.")
        return False
    
    print("\n--- [Manual Approval Required] ---")
    print("The following trade plan is proposed:")
    print("-" * 35)
    for trade in proposed_trades:
        print(f"  - {trade['decision'].upper()} {trade['symbol']} (Conviction: {trade['conviction_score']})")
    print("-" * 35)
    
    approval_input = input("Enter 'APPROVE' to confirm trades: ")

    if approval_input.strip().upper() == 'APPROVE':
        print("  - Approval received.")
        return True
    else:
        print("  - Approval denied. No trades will be executed.")
        return False

# --- MODIFIED (v6.2): Rounds dollar amounts for API compliance ---
def calculate_trade_plan(ai_proposals, current_positions, portfolio_value):
    """
    Calculates the final trade list based on conviction scores and portfolio rules.
    This is the core "portfolio manager" logic from the Charter.
    """
    print("\n--- [Stage 4.1: Formulating Trade Plan] ---")
    
    investable_capital = portfolio_value * TARGET_INVESTED_RATIO
    max_position_value = portfolio_value * MAX_POSITION_PERCENTAGE
    print(f"  - Portfolio Value: ${portfolio_value:,.2f}")
    print(f"  - Target Invested Capital (90%): ${investable_capital:,.2f}")
    print(f"  - Max Position Size (10%): ${max_position_value:,.2f}")

    target_portfolio = {p['symbol']: p for p in ai_proposals if p['decision'].lower() == 'buy'}
    if not target_portfolio:
        print("  - AI recommends no new 'Buy' positions.")
    else:
        print(f"  - AI has identified {len(target_portfolio)} stocks for the target portfolio.")

    total_conviction = sum(p['conviction_score'] for p in target_portfolio.values())
    target_allocations = {}
    if total_conviction > 0:
        for symbol, proposal in target_portfolio.items():
            weight = proposal['conviction_score'] / total_conviction
            target_value = min(investable_capital * weight, max_position_value)
            target_allocations[symbol] = target_value

    final_trades = []
    
    for symbol, target_value in target_allocations.items():
        current_value = float(current_positions[symbol].market_value) if symbol in current_positions else 0.0
        trade_dollar_amount = target_value - current_value
        
        if abs(trade_dollar_amount) > 25.0: 
            side = 'buy' if trade_dollar_amount > 0 else 'sell'
            final_trades.append({
                'symbol': symbol, 'side': side, 
                'dollar_amount': round(abs(trade_dollar_amount), 2), # <-- FIX IS HERE
                'decision_id': target_portfolio[symbol]['db_decision_id']
            })

    for symbol, position in current_positions.items():
        if symbol not in target_portfolio:
            print(f"  - Position {symbol} is not in the AI's target portfolio. Marking for liquidation.")
            ai_sell_decision = next((p for p in ai_proposals if p['symbol'] == symbol and p['decision'].lower() == 'sell'), None)
            decision_id = ai_sell_decision['db_decision_id'] if ai_sell_decision else None
            
            final_trades.append({
                'symbol': symbol, 'side': 'sell', 
                'dollar_amount': round(float(position.market_value), 2), # <-- FIX IS HERE
                'decision_id': decision_id
            })
    
    for proposal in ai_proposals:
        if proposal['decision'].lower() == 'sell' and proposal['symbol'] not in current_positions:
            print(f"  - AI recommends 'Sell' for {proposal['symbol']}, but no position is held. No action needed.")

    if not final_trades:
        print("  - No rebalancing trades are necessary to match the AI's target portfolio.")
    else:
        print("\n--- [Final Rebalancing Plan] ---")
        for trade in final_trades:
            print(f"  - {trade['side'].upper()} {trade['symbol']} for approx. ${trade['dollar_amount']:,.2f}")
            
    return final_trades

def update_trade_log(trade_id, status, order_id=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE trades SET status = ?, alpaca_order_id = ? WHERE id = ?", (status, order_id, trade_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"  - DB_ERROR: Failed to update trade log for trade ID {trade_id}: {e}")

def execute_trades(api, trade_plan, current_positions):
    """Executes or simulates trades based on the LIVE_TRADING flag in config.py."""
    
    mode = "LIVE PAPER TRADING" if config.LIVE_TRADING else "SAFE MODE"
    print(f"\n--- [Stage 5: Trade Execution & Logging ({mode})] ---")

    if not trade_plan:
        print("  - No trades to execute.")
        return

    for trade in trade_plan:
        symbol = trade.get('symbol')
        side = trade.get('side').lower()
        decision_id = trade.get('decision_id')
        dollar_amount = trade.get('dollar_amount')
        
        # For full liquidations, we use quantity to ensure the position is closed.
        if side == 'sell' and symbol in current_positions and symbol not in [p['symbol'] for p in trade_plan if p['side'] == 'buy']:
             quantity = current_positions[symbol].qty
             order_details = {'qty': quantity}
        else:
             order_details = {'notional': dollar_amount}

        trade_id = None
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            # Note: Storing dollar_amount instead of quantity for notional orders
            cursor.execute("INSERT INTO trades (decision_id, timestamp, symbol, side, quantity, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (decision_id, datetime.now(), symbol, side, order_details.get('qty', 0) or order_details.get('notional', 0), 'approved'))
            trade_id = cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"  - Logged trade as 'approved' in DB (Trade ID: {trade_id}).")
        except sqlite3.Error as e:
            print(f"  - DB_ERROR: Failed to insert approved trade for {symbol}: {e}")
            continue

        try:
            order = None
            if config.LIVE_TRADING:
                print(f"  - Submitting {side.upper()} order for {symbol}...")
                order = api.submit_order(
                    symbol=symbol,
                    side=side,
                    time_in_force='day',
                    **order_details
                )
                print(f"  - SUCCESS (LIVE): Order for {symbol} submitted. Order ID: {order.id}")
                update_trade_log(trade_id, 'submitted', order.id)
            else: # SAFE MODE
                # We calculate the simulated quantity here just for the log message
                latest_price = api.get_latest_trade(symbol).price
                sim_qty = dollar_amount / latest_price if 'notional' in order_details else quantity
                print(f"  - [SAFE MODE] Simulating {side.upper()} order for {sim_qty:.4f} shares of {symbol}...")
                fake_order_id = f"fake_order_{int(time.time())}_{symbol}"
                print(f"  - SUCCESS (SIMULATED): Order for {symbol}. Fake Order ID: {fake_order_id}")
                update_trade_log(trade_id, 'submitted', fake_order_id)

        except Exception as e:
            print(f"  - FAILED to submit order for {symbol}: {e}")
            update_trade_log(trade_id, 'execution_failed')


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
    
    all_dossiers = {}
    proposed_trades = get_todays_proposed_plan()
    
    if proposed_trades:
        print("\nFound a previously proposed plan for today. Proceeding to approval.")
        all_dossiers = {trade['symbol']: {'latest_price': trade['latest_price']} for trade in proposed_trades}
        print("  - Dossier information loaded from database. Skipping aggregation.")
    else:
        print("\nNo existing plan found for today. Generating a new one...")
        proposed_trades, all_dossiers = generate_and_log_new_plan(alpaca_api, current_positions)

    if not proposed_trades:
        print("\nNo actionable trades were proposed. Concluding run.")
    else:
        # Note: The approval step is now just for the AI's high-level plan
        is_approved = handle_approval_process(proposed_trades)
        if is_approved:
            final_trade_plan = calculate_trade_plan(proposed_trades, current_positions, portfolio_value)
            # We pass current_positions to execute_trades for liquidation logic
            execute_trades(alpaca_api, final_trade_plan, current_positions)
        else:
            print("\n--- [Trade Execution Halted] ---")
            print("  - Run concluded without executing trades.")

    print("\n====== Sentinel Daily Run Finished ======")

if __name__ == "__main__":
    main()