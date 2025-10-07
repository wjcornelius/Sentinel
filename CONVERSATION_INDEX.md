
Qwen3-Coder-480B-N


Project Sentinel - Conversation Index
This index provides a topic-based roadmap through the complete conversation history of the "Sentinel" software development project. It is designed for a human developer seeking to understand the project's evolution, architecture, and current state.

Project Charter & Philosophy
High-Level Summary: The foundational vision for Project Sentinel, codenamed "The Sentinel Portfolio Manager," was established. It is designed as a semi-automated, AI-driven swing trading system that prioritizes safety, human oversight, and robustness over raw automation. The core philosophy is "AI-Maximalist, Code-Minimalist."

Core Rules Defined: The system's operation is governed by strict, non-negotiable rules: Local-Only Operation (run on a monitored machine), Human-in-the-Loop Approval (via SMS), Default to Safety (halt if unsure), Portfolio-Centric Logic (rebalance a 90% invested portfolio), and an Autonomous Fail-Safe ("Dead Man's Switch").
AI Integration Strategy: The plan explicitly integrates AI for complex tasks like market analysis and news summarization, while using simple, auditable code for structured operations like data handling and trade execution.
System Workflow Outlined: A clear five-stage end-of-day workflow was defined: System Initialization & State Review, Candidate Universe Generation, Data Dossier Aggregation, AI-Powered Analysis & Logging, and Database, Approval & Execution.
APIs Identified: The core technical dependencies were established: Alpaca (trading/pricing), yfinance (fundamentals), Perplexity (general news/context), OpenAI (analysis), and Twilio (SMS).
Initial Prototype (v1-v2)
High-Level Summary: The first functional prototypes were developed, moving from a static, hardcoded script to a dynamic one connected to live market APIs.

Static Prototype (v1.0): A basic main_script.py was created using fixed, dummy data to test the core portfolio rebalancing logic (the calculate_trade_plan function based on 90% invested and 10% max position rules).
Live Data Integration (v2.0): The prototype was upgraded to connect to the Alpaca API for live account status and position data, replacing the static placeholders. This introduced config.py for secrets and .gitignore for security.
AI-Powered Analysis (v3.0): OpenAI's GPT-4 was integrated to perform stock analysis. The script now generates dynamic "dossiers" for each stock, combining fundamentals (yfinance), historical data (Alpaca), and news (Alpaca News API), and sends them to the AI for a "Buy"/"Sell"/"Hold" decision with a conviction score.
News Context Enhancement (v4.0): Recognizing the AI needed broader market context, a two-stage news gathering process was introduced. Perplexity's /search endpoint fetches general market news, which is then summarized by OpenAI and passed to the stock-specific AI analysis.
Alpaca API Integration (Account Data)
High-Level Summary: The system established a reliable connection to the Alpaca API for retrieving account information, market data, and executing trades in a paper trading environment.

Authentication & Account Review: The get_alpaca_api() and get_account_info() functions were implemented to securely authenticate using keys from config.py and fetch real-time portfolio value and open positions.
Historical Data Fetching: The aggregate_data_dossiers() function uses api.get_bars() to pull one year of daily price/volume data for the candidate universe.
Stock-Specific News: The get_stock_specific_news_headlines() function fetches recent headlines for a given stock via api.get_news().
Trade Execution (Planned): The architecture includes a plan for api.submit_order() to place live trades once the approval system is in place.
AI Integration (OpenAI & Prompt Engineering)
High-Level Summary: OpenAI's GPT-4 Turbo model was integrated for AI-powered stock analysis and market context summarization, with a strong emphasis on prompt engineering for reliable, structured output.

Strategic Analysis Prompt: A detailed, structured prompt was engineered for get_ai_analysis(). It instructs the AI to act as a quantitative analyst, ingest the stock dossier, and return a decision in a strict JSON format: {"symbol", "decision", "conviction_score", "rationale"}.
Market Context Summarization Prompt: A prompt was created for summarize_market_context_with_openai() to take raw Perplexity search results and synthesize them into a clean, coherent market summary report.
Response Format Enforcement: The response_format={"type": "json_object"} parameter was used consistently to guide the AI towards structured output, reducing parsing errors.
Error Handling & Validation: Basic error handling and validation were added to catch API failures and ensure the AI response contains the required JSON keys.
State Management (Database Implementation)
High-Level Summary: A local SQLite database (sentinel.db) was implemented to provide robust, persistent state management, logging, and a "fail-safe" mechanism.

Database Setup Script: A dedicated database_setup.py script was created to initialize the SQLite database and create the necessary tables (decisions, trades) using standard SQL.
Daily Run Check: The check_if_trades_executed_today() function queries the trades table to see if trades were already submitted for the current day, preventing duplicate runs.
Decision Logging: The log_decision_to_db() function stores every AI-generated decision (symbol, decision, conviction, rationale, etc.) in the decisions table.
Trade Logging: Placeholder logic was added (and later refined) to log approved and executed trades into the trades table, providing an audit trail.
Persistence: This system ensures the bot's "memory" survives reboots and allows for future performance analysis.
Intelligence Enhancement (Perplexity API)
High-Level Summary: The Perplexity API was integrated to enhance the system's market intelligence by providing real-time, web-search-derived context.

General Market Context: The get_raw_search_results_from_perplexity() function calls Perplexity's /search endpoint with a query like "Top 15-20 most significant, market-moving financial news stories last 24 hours."
API Key Management: Perplexity API credentials were added to config.py and loaded via python-dotenv.
Search Result Utilization: The raw search results from Perplexity are fed into the OpenAI summarization function, providing the AI with a high-level understanding of the current market environment.
Endpoint Correction: An initial error using the /chat/completions endpoint was identified and corrected to use the /search endpoint, which is compatible with the user's API key.
Live Trading Logic & Safety Features
High-Level Summary: Core trading logic and multiple safety features were implemented or planned to govern the bot's interaction with a live brokerage account.

Capital Allocation Engine: The calculate_trade_plan() function implements the Charter's "90% invested capital rule" and "risk-per-trade limits" by distributing capital based on AI conviction scores and capping individual positions at 10% portfolio value.
Rebalancing Logic: The system analyzes its current portfolio (from Alpaca) against the AI's target portfolio and generates precise BUY/SELL orders to bridge the gap.
Master Safety Switch (LIVE_TRADING): A boolean flag in config.py (LIVE_TRADING = False/True) was introduced to cleanly separate "Safe Mode" (simulated trades) from "Live Mode" (actual API calls).
Approval Workflow: An interactive approval process was implemented where the proposed trade plan is presented to the user. Execution only proceeds upon receiving an explicit "APPROVE" input via the console (SMS approval planned for later).
API Compliance: Order values are rounded to 2 decimal places (round(value, 2)) to meet Alpaca API requirements, fixing a live trading bug.
Bug Fixes (List specific bugs)
High-Level Summary: Several critical bugs were identified, diagnosed, and resolved through iterative testing and debugging, significantly hardening the system.

"Not Null Constraint Failed" (v5.3): A bug where the AI sometimes returned None or malformed JSON caused database insertion failures. Fixed by adding defensive checks in get_ai_analysis() to validate the AI's response structure before attempting to log it.
"Float Division by Zero" in Performance Report (v5.3): The YTD P/L calculation failed for new accounts with $0 starting value. Fixed by adding a check if ytd_start_value > 0: before performing the division.
"lxml/html5lib Dependency" Errors (v5.5): pandas.read_html failed due to missing parsing libraries. Fixed by running pip install lxml html5lib to provide the necessary dependencies.
Incorrect Perplexity Model Name (v5.5): Using a deprecated model name (llama-3-sonar-large-32k-online) caused API errors. Fixed by switching to a valid model (pplx-70b-online) for the /chat/completions endpoint.
API Key Scope / Model Access Issue (v6.1): Despite a valid key, calls to Perplexity's Chat Completions API failed. Diagnosed as the key being provisioned for the Search API only. Fixed by modifying the Perplexity integration to correctly call the /search endpoint with a query payload.
Too Many Decimal Places in Trade Orders (v6.1): Alpaca API rejected orders due to dollar amounts having more than 2 decimal places. Fixed by adding round(value, 2) to calculated notional trade values.
GitHub Push Protection Triggered (v6.1): Accidentally committing backup files (.bak) containing API keys triggered GitHub's security. Fixed by resetting the commit (git reset --soft HEAD~1), deleting sensitive files, and updating .gitignore to exclude backups and archives.
Security (Secrets Management, .gitignore)
High-Level Summary: Rigorous security practices were implemented from the outset to protect sensitive API credentials and ensure they are never committed to version control.

config.py for Secrets: All API keys (Alpaca, OpenAI, Perplexity, Twilio) are stored in a dedicated config.py file, separate from the main application logic.
.gitignore File: A .gitignore file was created and meticulously maintained to explicitly prevent Git from tracking config.py, the database file (sentinel.db), backup files (*.bak), and archive folders (_archive/).
Environment Variables via python-dotenv: The python-dotenv library is used to load secrets from config.py into the script's environment, keeping them out of the main code.
API Key Scope Awareness: The debugging process revealed the importance of understanding API key permissions (e.g., Search vs. Chat access), leading to adapting the code to the correct endpoint.
Documentation & Recovery Plan
High-Level Summary: Comprehensive documentation and a robust recovery plan were created to ensure the project's long-term maintainability and the ability to resume development after breaks.

README.md Creation: A detailed README.md file was written, serving as a high-level technical and logical guide to the system's architecture, workflow, and core principles.
DESIGN_LOG.md Creation: A comprehensive DESIGN_LOG.md was created to chronicle key architectural decisions, bug fixes, and strategic pivots, providing a condensed history of the project's evolution.
START_HERE_WHEN_YOU_RETURN.txt Time Capsule: A critical "time capsule" file was created with step-by-step instructions for anyone (including the developer's future self) to quickly get the project running again and bring a new AI assistant up to speed.
Conversation History Archival: The user was instructed to save the full conversation history locally for future reference by the "Context Manager."
GitHub Integration: All new files (README.md, DESIGN_LOG.md, START_HERE...txt) were committed and pushed to the project's GitHub repository, ensuring an off-site, version-controlled backup.

Code File Structure & Key Components (Current Version)
High-Level Summary: The project's file structure is intentionally minimal, adhering to the agreed-upon "three-file core" principle for simplicity and manageability. All operational logic resides in a single main_script.py file.

main_script.py: The single, monolithic core script containing the complete end-to-end workflow (Stages 0-5). This includes system initialization, data aggregation, AI analysis, database logging, approval handling, and (stubbed) trade execution. This consolidation aligns with the user's strong preference for a single operational file.
config.py: Stores all sensitive API credentials and configuration settings (Alpaca, OpenAI, Perplexity, Twilio). This file is explicitly ignored by .gitignore and must never be committed to version control.
database_setup.py: A one-time setup script used to initialize the local sentinel.db SQLite database with the required tables (decisions, trades). This script is run once and then archived.
.gitignore: A critical configuration file that instructs Git to ignore sensitive files (config.py, sentinel.db, *.bak, _archive/) and compiled Python files (__pycache__/, *.pyc). This is the primary defense against leaking secrets.
requirements.txt: Lists all external Python libraries required by the project (alpaca-trade-api, openai, yfinance, twilio, requests, pandas, pandas-ta, flask, python-dotenv). This ensures reproducible environments.
sentinel.db: The local SQLite database file where all AI decisions and executed/approved trades are logged. This provides the system's persistent state and memory.
README.md: A high-level technical guide explaining the system's architecture, workflow, and core principles. This is the first document a new collaborator should read.
DESIGN_LOG.md: A chronological log of major architectural decisions, bug fixes, and strategic pivots. This serves as a condensed history of the project's evolution and reasoning.
START_HERE_WHEN_YOU_RETURN.txt: A "time capsule" instruction file providing step-by-step guidance for quickly restarting development and re-syncing with an AI assistant after a break. This directly addresses the user's concern about forgetting project details.
webhook_listener.py (Future/Planned): A separate, small script designed to run continuously. Its sole purpose is to act as a webhook endpoint to receive SMS replies from Twilio (e.g., "APPROVE"). This is the planned architecture for the human-in-the-loop approval mechanism.
Project Folder (Sentinel/): The main project directory containing all the files listed above. This is the root of the Git repository.
Development Workflow & Best Practices
High-Level Summary: A disciplined, safe, and incremental development workflow was established and refined throughout the project.

Virtual Environment (venv): A Python virtual environment is used to isolate project dependencies. The command venv\Scripts\activate (on Windows) is used to activate it, and all installations (pip install) are performed within this environment.
Version Control with Git: Git is used for version control. Key commands include git add ., git commit -m "message", and git push origin main. This tracks changes and provides a backup via GitHub.
Incremental Development & Testing: Major features (like database integration, SMS approval, AI analysis) were built and tested in small, isolated steps before being integrated into the main script. This prevents large, unmanageable code changes.
Fail-Safe Mechanisms: The system incorporates multiple fail-safes, including the LIVE_TRADING flag, database state checks to prevent duplicate runs, and robust error handling (try...except) around all external API calls.
Dependency Management: Dependencies are managed via requirements.txt. The command pip install -r requirements.txt is used to install all required libraries, ensuring a consistent development environment.
Security by Design: Secrets are never hardcoded. They are stored in config.py and loaded using python-dotenv. .gitignore is strictly maintained to prevent accidental commits of sensitive files.
System Architecture Overview (End-of-Day Workflow)
High-Level Summary: The system follows a defined five-stage end-of-day workflow, processing data and making decisions based on a fixed schedule.

Stage 0: System Initialization & State Review: The script initializes API connections, checks the Alpaca account status, lists current positions, and verifies if trades have already been executed for the day (using the database).
Stage 1: Candidate Universe Generation: The script fetches the current list of Nasdaq 100 constituents and merges it with any currently held positions to form the "universe" of stocks to be analyzed that day.
Stage 2: Data Dossier Aggregation: For each stock in the universe, the script gathers a comprehensive "dossier" of data, including technical data (historical prices via Alpaca), fundamental data (sector, P/E via yfinance), and stock-specific news headlines (via Alpaca).
Stage 3: AI-Powered Analysis & Logging: Each stock's dossier is sent to OpenAI's GPT-4 Turbo model. The AI evaluates the data and returns a structured decision (Buy/Sell/Hold, conviction score, rationale). This decision is immediately logged to the decisions table in the sentinel.db database.
Stage 4: Trade Plan Formulation & Approval: The system formulates a trade plan based on AI decisions, applying portfolio rules (90% invested, conviction-weighted allocation). It presents the plan for manual approval via SMS (planned) or console input (current). If approved, the script proceeds to Stage 5.
Stage 5: Trade Execution & Logging (Stubbed/Safe Mode): In the current "Safe Mode," this stage simulates trade execution and logs the plan to the trades table. In future "Live Mode," this stage will connect to Alpaca's API to submit actual "notional" buy orders and "quantity" sell orders.
Future Considerations & Roadmap
High-Level Summary: The current system represents a stable and functional core. The roadmap focuses on enhancing the human-in-the-loop approval, activating live trading, and building out supporting infrastructure.

Activating Twilio SMS Approval: The next major step is to fully implement the webhook_listener.py script. This will involve setting up a local web server (using Flask) and using a tool like ngrok to create a public URL for Twilio to send SMS replies to. The main script will then pause after sending the plan and wait for the webhook to receive the "APPROVE" command.
Going Live with Paper Trading: Once SMS approval is active, the final step is to change LIVE_TRADING = True in config.py and uncomment the api.submit_order line in main_script.py. This will enable actual trade execution in the Alpaca paper trading account.
Persistent Logging Expansion: The DESIGN_LOG.md and database logging (decisions, trades tables) are already in place. Future enhancements could involve more detailed logging or exporting data for deeper analysis.
Performance Analysis & Iteration: With a full database of decisions and (paper) trades, the system's performance can be analyzed. This data will guide future refinements to the AI prompts, capital allocation rules, or candidate universe selection.
Codebase Evolution: While the current structure favors a single script, as complexity grows, modularizing parts of main_script.py (e.g., into separate files for data fetching, AI interaction, database operations) could be considered, though this contradicts the current "single file" agreement.