# main_script.py
# Version 3.2 - SAFE / NO-TRADE VERSION
# Implements Nasdaq 100, cost-optimized news, and disables (but preserves) trade execution logic.

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

# --- Stage 0: System Initialization & State Review ---
def get_alpaca_api():
    """Initializes and returns an authenticated Alpaca API object."""
    return tradeapi.REST(
        config.APCA_API_KEY_ID,
        config.APCA_API_SECRET_KEY,
        config.APCA_API_BASE_URL,
        api_version='v2'
    )

def get_account_info(api):
    """Fetches and prints account status and current positions."""
    print("--- [Stage 0: Account & Position Review] ---")
    try:
        account = api.get_account()
        if account.status == 'ACTIVE':
            print(f"Account is ACTIVE. Portfolio Value: ${account.portfolio_value}")
        else:
            print(f"Account status: {account.status}")

        positions = api.list_positions()
        if positions:
            print(f"Current Positions ({len(positions)}):")
            for pos in positions:
                print(f"  - {pos.symbol}: {pos.qty} shares @ avg ${pos.avg_entry_price}")
        else:
            print("No open positions.")
        
        return {p.symbol: p for p in positions}, account

    except Exception as e:
        print(f"Error connecting to Alpaca: {e}")
        return {}, None

# --- Stage 1: Candidate Universe Generation ---
def get_nasdaq_100_symbols():
    """Fetches the list of Nasdaq 100 symbols from a reliable source."""
    print("  - Fetching Nasdaq 100 constituents...")
    try:
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        response = requests.get(url)
        tables = pd.read_html(response.text)
        nasdaq_100_df = tables[4]
        symbols = nasdaq_100_df['Ticker'].tolist()
        symbols = [s.replace('.', '-') for s in symbols]
        print(f"  - Successfully fetched {len(symbols)} symbols.")
        return symbols
    except Exception as e:
        print(f"  - ERROR: Could not fetch Nasdaq 100 list: {e}")
        print("  - Falling back to a smaller, static list for this run.")
        return ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL', 'AMZN', 'META']

def generate_candidate_universe(current_symbols):
    """Generates the universe of stocks to be analyzed, starting with the Nasdaq 100."""
    print("\n--- [Stage 1: Candidate Universe Generation] ---")
    base_universe = get_nasdaq_100_symbols()
    candidate_universe = sorted(list(set(base_universe + list(current_symbols))))
    print(f"Generated a universe of {len(candidate_universe)} candidates for analysis.")
    print(f"Sample candidates: {candidate_universe[:5]}...")
    return candidate_universe

# --- Stage 2: Data Dossier Aggregation ---
def get_market_context_from_perplexity():
    """
    Makes a single, cost-effective API call to Perplexity to get a summary
    of the day's most important market-moving news.
    """
    print("\n--- [Fetching General Market News Context via Perplexity] ---")
    try:
        client = OpenAI(api_key=config.PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
        prompt = """
        As a financial news analyst, please search the web for the top 15-20 most significant,
        market-moving news stories from the last 24 hours. Focus on topics like macroeconomic data releases
        (CPI, jobs reports), central bank policy changes (e.g., Fed announcements), major geopolitical events,
        or significant sector-wide trends. For each story, provide a concise one-sentence headline and a 2-3 sentence summary.
        Format the entire output as a single block of text.
        """
        response = client.chat.completions.create(
            model="llama-3-sonar-large-32k-online",
            messages=[{"role": "user", "content": prompt}],
        )
        market_news = response.choices[0].message.content
        print("Successfully fetched general market news from Perplexity.")
        return market_news
    except Exception as e:
        print(f"Error fetching news from Perplexity: {e}")
        return "Could not retrieve general market news from Perplexity."

def get_stock_specific_news_headlines(api, symbol):
    """Fetches only the headlines of recent news for a given stock from Alpaca (free)."""
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=3)
        news = api.get_news(symbol=symbol, start=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), end=end_time.strftime('%Y-%m-%dT%H:%M:%SZ'), limit=5)
        if not news: return "No recent stock-specific news headlines found."
        headlines = [article.headline for article in news]
        return " | ".join(headlines)
    except Exception:
        return "Error fetching stock-specific headlines."

def aggregate_data_dossiers(api, universe, market_news_summary):
    print("\n--- [Stage 2: Data Dossier Aggregation] ---")
    dossiers = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    universe_subset = universe[:10]
    print(f"*** NOTE: Analyzing a subset of {len(universe_subset)} stocks for this test run. ***")

    for i, symbol in enumerate(universe_subset):
        print(f"Aggregating data for {symbol} ({i+1}/{len(universe_subset)})...")
        try:
            bars = api.get_bars(symbol, '1Day', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), feed=config.APCA_API_DATA_FEED).df
            if bars.empty:
                print(f"  - No bar data found for {symbol}. Skipping.")
                continue
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            fundamentals = {"sector": info.get('sector', 'N/A'), "forward_pe": info.get('forwardPE', 'N/A')}
            
            stock_headlines = get_stock_specific_news_headlines(api, symbol)
            
            dossiers[symbol] = {
                "symbol": symbol,
                "fundamentals": fundamentals,
                "historical_data": bars.to_json(orient='split'),
                "stock_specific_headlines": stock_headlines,
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

    system_prompt = "You are a quantitative analyst..." # Abridged for brevity
    
    user_prompt = f"""
    Please analyze the stock {dossier['symbol']} and provide a recommendation.
    **1. Overall Market Context:** {market_context}
    **2. Stock-Specific Data for {dossier['symbol']}:**
    - **Fundamentals:** {json.dumps(dossier['fundamentals'], indent=2)}
    - **Recent News Headlines:** {dossier['stock_specific_headlines']}
    - **Technical Signal:** A {technical_signal} is present.
    **Your Task:** Synthesize all information. Return a JSON object with "symbol", "decision", "conviction_score", and "rationale".
    Output only the raw JSON object.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            response_format={"type": "json_object"}
        )
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    except Exception as e:
        print(f"    - ERROR: Failed to get AI analysis for {dossier['symbol']}: {e}")
        return None

# --- STAGE 4: ORDER EXECUTION (DISABLED FOR NOW) ---
# The following function is the complete trade execution logic. It is intentionally
# disabled until the SMS approval workflow is implemented and tested. This prevents
# accidental trades.
"""
def execute_trades(api, analyses, current_positions, account_info):
    print("\n--- [Stage 4: Trade Execution] ---")
    if not account_info:
        print("Could not retrieve account info. Halting trade execution.")
        return

    for analysis in analyses:
        symbol = analysis['symbol']
        decision = analysis['decision']
        conviction = analysis['conviction_score']
        rationale = analysis['rationale']
        
        print(f"Processing {symbol}: AI Decision is '{decision}' with conviction {conviction}.")
        print(f"  - Rationale: {rationale}")

        has_position = symbol in current_positions
        
        if decision == "Buy" and not has_position and conviction >= 7:
            try:
                target_position_value = float(account_info.portfolio_value) * 0.10
                latest_price = all_dossiers[symbol]['latest_price']
                quantity_to_buy = int(target_position_value / latest_price)

                if quantity_to_buy > 0:
                    print(f"  - ACTION: Placing BUY order for {quantity_to_buy} shares of {symbol}.")
                    api.submit_order(symbol=symbol, qty=quantity_to_buy, side='buy', type='market', time_in_force='day')
                else:
                    print(f"  - INFO: Target position value is too low to buy a single share.")
            except Exception as e:
                print(f"  - ERROR: Failed to place BUY order for {symbol}: {e}")

        elif decision == "Sell" and has_position and conviction >= 7:
            try:
                position = current_positions[symbol]
                print(f"  - ACTION: Placing SELL order for {position.qty} shares of {symbol}.")
                api.submit_order(symbol=symbol, qty=position.qty, side='sell', type='market', time_in_force='day')
            except Exception as e:
                print(f"  - ERROR: Failed to place SELL order for {symbol}: {e}")
        
        else:
            if decision == "Buy" and has_position:
                print(f"  - INFO: AI recommends 'Buy', but we already hold {symbol}. No action taken.")
            elif decision == "Sell" and not has_position:
                print(f"  - INFO: AI recommends 'Sell', but we do not hold {symbol}. No action taken.")
            elif decision == "Buy" or decision == "Sell" and conviction < 7:
                 print(f"  - INFO: AI decision is '{decision}', but conviction ({conviction}) is below our threshold of 7. No action taken.")
            else: # Hold
                print(f"  - INFO: AI recommends 'Hold'. No action taken.")
"""

# --- Main Execution Workflow ---
def main():
    """The main end-of-day execution function for the Sentinel system."""
    print("====== Sentinel Daily Run Initialized ======")
    
    alpaca_api = get_alpaca_api()
    
    current_positions, account_info = get_account_info(alpaca_api)
    candidate_universe = generate_candidate_universe(current_positions.keys())
    
    global all_dossiers
    market_context = get_market_context_from_perplexity()
    all_dossiers = aggregate_data_dossiers(alpaca_api, candidate_universe, market_context)
    
    print("\n--- [Stage 3: AI-Powered Analysis] ---")
    all_analyses = []
    if all_dossiers:
        for symbol, dossier in all_dossiers.items():
            analysis = get_ai_analysis(dossier, market_context)
            if analysis:
                all_analyses.append(analysis)
            time.sleep(2)
    else:
        print("No dossiers were created, skipping AI analysis.")
    
    # STAGE 4 & 5 ARE INTENTIONALLY OMITTED IN THIS SAFE VERSION
    # execute_trades(alpaca_api, all_analyses, current_positions, account_info)

    print("\n--- [Trade Plan Generation Complete] ---")
    print("The following decisions have been recommended by the AI. No trades will be executed.")
    
    for analysis in all_analyses:
        print("-" * 30)
        print(f"  Symbol:    {analysis['symbol']}")
        print(f"  Decision:  {analysis['decision']} (Conviction: {analysis['conviction_score']})")
        print(f"  Rationale: {analysis['rationale']}")
    
    print("\n====== Sentinel Daily Run Finished (SAFE MODE) ======")


if __name__ == "__main__":
    main()