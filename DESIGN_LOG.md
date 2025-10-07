# Project Sentinel - Design & Decision Log (Comprehensive History)

This document tracks the key architectural decisions, bug fixes, and strategic pivots made during the development of Sentinel. It serves as a condensed and detailed version of the full conversation history, intended to bring any developer (including a future version of myself or a new AI) up to speed on the project's entire lifecycle.

---

### **v1.0: The Conceptual Phase & The Project Charter**

*   **Decision:** Formalized the project's mission, rules, and philosophy in a "Project Charter."
*   **Reasoning:** To establish a clear source of truth for the bot's strategic goals before writing any code. This prevents "feature creep" and ensures all development aligns with the core mission.
*   **Key Principles Established:**
    *   **Philosophy:** "AI-Maximalist, Code-Minimalist." Use AI for complex, subjective analysis (strategy) and use simple, auditable Python code for deterministic tasks (math, data handling).
    *   **Capital Rules:**
        1.  **90% Invested Rule:** The bot should aim to keep 90% of the portfolio's total value invested in equities.
        2.  **10% Max Position Rule:** No single stock position should exceed 10% of the portfolio's total value to ensure diversification.
    *   **Risk Management:**
        1.  **Human-in-the-Loop:** The bot must present a trade plan for manual `APPROVE`/`DENY` confirmation before execution.
        2.  **"Dead Man's Switch":** The bot must be run manually each day and is not fully automated, ensuring human oversight.

---

### **v2.0: The First Functional Prototype (Offline)**

*   **Decision:** Created the first `main_script.py` as a single, monolithic file.
*   **Reasoning:** To quickly prototype and test the core capital allocation and rebalancing logic in a simple, self-contained script.
*   **Functionality:**
    *   Used **hardcoded, static data** for portfolio value, current positions, and AI decisions.
    *   Successfully implemented the `calculate_trade_plan` function, which contained the pure Python math for the 90% and 10% rules.
    *   The script's output was simply a series of `print()` statements showing the proposed trades. No external APIs were called.

---

### **v3.0: Integrating with the Real World (API Layer 1)**

*   **Decision:** Replaced hardcoded data with live data from the Alpaca API. Created `config.py` and `.gitignore`.
*   **Reasoning:** To make the bot operate on real-time, accurate account information instead of static test data.
*   **Key Changes:**
    *   **Alpaca Integration:** Added code to fetch the current portfolio value and a list of all open positions directly from the paper trading account.
    *   **`config.py`:** Created this separate, private file to store API keys.
    *   **`.gitignore`:** Created this file to explicitly tell Git to **never** track `config.py`, preventing accidental leakage of secret keys.
    *   **Stock Universe:** Formalized the decision to use the **Nasdaq 100** as the primary candidate universe for the bot's analysis.

---

### **v4.0: The "Brain" - AI-Powered Decision Making**

*   **Decision:** Integrated OpenAI's GPT-4 model to replace the hardcoded "Buy/Sell" decisions.
*   **Reasoning:** This was the core implementation of the "AI-Maximalist" philosophy. The AI was tasked with performing the strategic analysis for each stock.
*   **Key Architecture:**
    *   **Data Dossier:** For each stock in the Nasdaq 100, the script would assemble a "dossier" of information.
    *   **News Source:** Used the Alpaca News API to pull recent headlines for each specific stock.
    *   **AI Prompting:** A detailed prompt was engineered to instruct the AI to act as a quantitative analyst and evaluate the stock based on the provided dossier.
    *   **Structured Output:** The AI was required to return its analysis in a strict **JSON format**: `{"decision": "Buy/Sell/Hold", "conviction_score": 1-10}`. This made the AI's output machine-readable and easy to parse by the Python script.

---

### **v5.0: State Management & Enhanced Intelligence**

*   **Decision:** Integrated a SQLite database and upgraded the market intelligence gathering with Perplexity.
*   **Reasoning:** The bot was "stateless," meaning it would try to run again if executed twice, and its market view was too narrow.
*   **Key Upgrades:**
    *   **SQLite Database (`sentinel.db`):**
        1.  Created `database_setup.py` to initialize the database with `decisions` and `trades` tables.
        2.  The main script was modified to **check the database first**. If trades for the current day already existed, the script would exit immediately, preventing duplicate orders.
        3.  All AI decisions and executed trades were now logged for future performance analysis.
    *   **Perplexity API Integration:**
        1.  The Alpaca News API was found to be too limited (just headlines).
        2.  Perplexity was added to perform a broad search for "major market news" and provide a comprehensive summary. This summary was then fed to OpenAI to give the main AI a high-level **market context** before it analyzed individual stocks, dramatically improving its analytical context.

---

### **v6.x: Live Trading, Hardening, and Documentation**

*   **v6.0 - The Safety Switch:**
    *   **Decision:** Implemented a `LIVE_TRADING = False` boolean flag in `config.py`.
    *   **Reasoning:** To create a single, clear, and robust safety switch to toggle between "simulation mode" (printing trades) and "live mode" (executing trades via the API). This is much safer than commenting/uncommenting code.

*   **v6.1 - First Live Bug Fix:**
    *   **Bug:** The first live paper trading attempt failed. All orders were rejected by the Alpaca API.
    *   **Diagnosis:** The calculated dollar values for trades had more than two decimal places (e.g., $50.12345).
    *   **Fix:** Implemented `round(value, 2)` on all notional order amounts within the `calculate_trade_plan` function to ensure API compliance.

*   **v6.2 - Security & Documentation:**
    *   **Bug:** A `git push` command was rejected by GitHub.
    *   **Diagnosis:** GitHub's "Push Protection" feature correctly identified API keys located in backup files (`.bak`, `_archive/`) that were accidentally added to the commit.
    *   **Fix:** The bad commit was undone (`git reset`), the offending backup files were deleted, and the `.gitignore` file was significantly enhanced to ignore common backup file types and folders, preventing the issue from reoccurring.
    *   **Documentation:** Created the `README.md` (user manual) and this `DESIGN_LOG.md` (developer history) to ensure the project's long-term maintainability. Created the `START_HERE_WHEN_YOU_RETURN.txt` file as a "time capsule" for future recovery.

---
*This log is a living document. Future changes and decisions should be appended here.*