# Project Sentinel: An AI-Driven Portfolio Manager

**Version: 6.2**
**Status: Live Paper Trading**

This document serves as a high-level technical and logical guide for the Sentinel Portfolio Manager. It describes the system's architecture, workflow, and core principles as of the version listed above.

---

### Core Philosophy & Guiding Principles

The system is built on an "AI-Maximalist, Code-Minimalist" philosophy. It leverages powerful AI models for complex, subjective analysis (e.g., strategy, ranking) while using simple, auditable Python code for structured, mathematical tasks (e.g., data handling, capital allocation).

-   **Local-Only Operation:** The entire system runs on a single, user-monitored machine.
-   **Human-in-the-Loop:** The system proposes a plan, but the user gives final `APPROVE`/`DENY` confirmation before any trades are executed.
-   **Portfolio-Centric Logic:** The system thinks in terms of an "ideal portfolio" and generates rebalancing trades to move from the current state to the ideal state.
-   **State-Aware & Resilient:** Using a local SQLite database (`sentinel.db`), the system knows what it has already done each day and can recover from crashes or restarts.

---

### System File Structure

-   `main_script.py`: The monolithic core logic file that runs the entire daily process.
-   `config.py`: Stores all API keys and the master `LIVE_TRADING` switch. **This file is ignored by Git and should never be shared.**
-   `database_setup.py`: A one-time script to create the SQLite database and tables.
-   `sentinel.db`: The SQLite database file where all decisions and trades are logged.
-   `.gitignore`: Instructs Git to ignore sensitive or transient files like `config.py`, `sentinel.db`, and Python cache folders.
-   `README.md`: This file.

---

### The Daily End-of-Day Workflow

The `main_script.py` is executed once per day after market close.

#### **Stage 0: State & Performance Review**
1.  **State Check:** The script first queries `sentinel.db` to see if trades have already been executed for the current day. If so, it exits immediately to prevent duplicate orders.
2.  **Account & Position Sync:** It connects to the Alpaca API to get the current portfolio value and a list of all open positions.
3.  **Performance Reporting:** It calculates and displays the daily and Year-to-Date portfolio performance.

#### **Stage 1: Candidate Universe Generation**
1.  The script fetches the current list of all stocks in the **Nasdaq 100**.
2.  It adds any stocks that are currently held in the portfolio to this list (to ensure they are re-evaluated).
3.  This combined, de-duplicated list forms the "candidate universe" for the day's analysis.

#### **Stage 2: Data Dossier Aggregation**
For each stock in the universe, the script assembles a data "dossier":
1.  **Market Context:** It makes a single API call to Perplexity to search for major market news, then uses OpenAI's GPT-4 to summarize this into a market context report.
2.  **Stock Data:** It pulls historical price/volume data from Alpaca and fundamental data (e.g., sector) from `yfinance`.
3.  **Stock News:** It pulls recent stock-specific news headlines from the Alpaca API.

#### **Stage 3: AI-Powered Strategic Analysis**
1.  The complete dossier for each stock is sent to **OpenAI's GPT-4 Turbo model**.
2.  The AI is prompted to act as a quantitative analyst and return a simple JSON object containing a `decision` ("Buy", "Sell", or "Hold") and a `conviction_score` (integer 1-10).
3.  This strategic decision is logged to the `decisions` table in `sentinel.db`.

#### **Stage 4: Trade Plan Formulation & Rebalancing**
This stage uses pure Python code to translate the AI's strategic vision into an actionable plan.
1.  **Approval:** The user is shown the list of "Buy" and "Sell" decisions and must type `APPROVE`.
2.  **Capital Allocation:** Upon approval, the `calculate_trade_plan` function applies the following rules from the Project Charter:
    -   **90% Invested Rule:** It calculates the total target capital to be invested as 90% of the total portfolio value.
    -   **Conviction Weighting:** It allocates this capital across all "Buy" recommendations, giving more capital to stocks with a higher `conviction_score`.
    -   **10% Max Position Rule:** It caps any single position's target value at 10% of the total portfolio value to ensure diversification.
3.  **Rebalancing:** It compares the calculated ideal portfolio against the current positions and generates the final list of trades (Buys, Sells, and Trims) needed to rebalance. Dollar amounts are rounded to 2 decimal places for API compliance.

#### **Stage 5: Trade Execution**
1.  The script checks the `LIVE_TRADING` flag in `config.py`.
2.  **If `False` (Safe Mode):** It prints the simulated trades to the console without contacting the broker.
3.  **If `True` (Live Mode):** It connects to the Alpaca API and submits the "notional" (dollar-value) buy orders and "quantity" sell orders to close positions.
4.  The status of each submitted order (`submitted` or `execution_failed`) is logged to the `trades` table in `sentinel.db`.
