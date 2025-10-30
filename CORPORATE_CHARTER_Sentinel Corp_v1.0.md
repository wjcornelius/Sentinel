SENTINEL CORPORATION - CORPORATE CHARTER v1.0
Document Status: Foundation Document - All departments, workflows, and code must align with this charter
Last Updated: October 30, 2025
Authority: William J. Cornelius (Chairman & CEO)
Version Control: /CORPORATE_CHARTER.md in main Sentinel repository

EXECUTIVE SUMMARY
Sentinel Corporation is an algorithmic trading operation structured as a business organization with clearly defined departments, each having specific responsibilities, interfaces, and performance metrics. This charter defines the organizational structure, departmental boundaries, communication protocols, and operational standards.

Mission: Execute momentum-based equity trading strategies with institutional discipline, retail agility, and quantifiable edge.

Core Principle: Every component is either a strategic decision-maker (AI/human) or a mechanical executor (deterministic code). No component does both.

ORGANIZATIONAL STRUCTURE

+-----------------------------------------------------+
¦           BOARD OF DIRECTORS (You)                  ¦
¦  - Strategic direction                              ¦
¦  - Performance review                               ¦
¦  - Hire/fire departments                            ¦
¦  - Approve architecture changes                     ¦
¦  - Live trading authorization (SIM ? LIVE switch)  ¦
+-----------------------------------------------------+
                          ¦
                          ?
+-----------------------------------------------------+
¦              CHIEF EXECUTIVE OFFICER                ¦
¦           (GPT-5 Portfolio Optimizer)               ¦
¦  - Capital allocation decisions                     ¦
¦  - Position sizing across portfolio                 ¦
¦  - Rebalancing strategy                             ¦
¦  - Sell vs. hold vs. buy decisions                  ¦
¦  INPUT: Executive summaries (not raw data)          ¦
¦  OUTPUT: Trade plan (what to buy/sell, how much)    ¦
+-----------------------------------------------------+
          ¦                    ¦                    ¦
          ?                    ?                    ?
+------------------+  +------------------+  +------------------+
¦    RESEARCH      ¦  ¦  TRADING DESK    ¦  ¦   COMPLIANCE     ¦
¦   DEPARTMENT     ¦  ¦                  ¦  ¦   DEPARTMENT     ¦
+------------------+  +------------------+  +------------------+
          ¦                    ¦                    ¦
          ?                    ?                    ?
+------------------+  +------------------+  +------------------+
¦   ACCOUNTING     ¦  ¦   OPERATIONS     ¦  ¦   RISK MGMT      ¦
¦   DEPARTMENT     ¦  ¦   DEPARTMENT     ¦  ¦   DEPARTMENT     ¦
+------------------+  +------------------+  +------------------+
DEPARTMENT SPECIFICATIONS
1. BOARD OF DIRECTORS (You - William J. Cornelius)
Role: Strategic oversight and final authority

Responsibilities:

Define strategic goals (target returns, risk tolerance, market focus)
Review quarterly and annual performance
Approve major architectural changes
Hire/fire departments (decide which components to build/remove)
Authorize transition from paper trading to live trading
Intervene in crisis situations (manual override authority)
Does NOT:

Write code (delegates to Engineering via Claude Code)
Debug Python errors (delegates to Engineering)
Monitor minute-by-minute operations (delegates to Operations)
Make individual trade decisions (delegates to CEO)
Success Metrics:

Annual portfolio return vs. benchmark (SPY)
Risk-adjusted return (Sharpe, Sortino)
Maximum drawdown vs. target
Operational uptime and reliability
Cost efficiency (total trading costs as % of edge)
2. CHIEF EXECUTIVE OFFICER (GPT-5 Portfolio Optimizer)
Role: Strategic capital allocation and portfolio management

Responsibilities:

Receive executive summaries from Research Department
Decide portfolio composition:
Which positions to close (sell candidates)
Which positions to add (buy candidates)
Position sizing for each (% of portfolio)
Output: Trade Plan = structured list of actions with rationale
Maintain portfolio-level risk targets (heat, concentration, correlation)
Input Format (Executive Summary from Research):

json

{
  "market_context": {
    "regime": "trend|chop|bear|high_vol|crisis",
    "spy_above_200dma": true|false,
    "vix": 18.5,
    "breadth_zscore": 0.3,
    "date": "2025-10-30"
  },
  "portfolio_state": {
    "total_value": 102410.51,
    "cash_available": 5766.94,
    "buying_power": 5766.94,
    "position_count": 92,
    "total_heat": 7.2,
    "unrealized_pnl": 3499.37
  },
  "current_positions": [
    {
      "symbol": "KLAC",
      "conviction_score": 62,
      "profit_pct": 16.3,
      "profit_usd": 278.27,
      "days_held": 18,
      "current_value": 1850.00,
      "reasoning": "Profit target hit, momentum weakening"
    },
    // ... up to 92 positions (all current holdings)
  ],
  "buy_candidates": [
    {
      "symbol": "TER",
      "conviction_score": 84,
      "reasoning": "Strong semicon momentum + positive earnings surprise",
      "tier1_score": 78,
      "sector": "Technology"
    },
    // ... top 30 candidates only
  ],
  "sell_candidates": [
    {
      "symbol": "IDXX",
      "conviction_score": 55,
      "reasoning": "Weakening fundamentals, sector headwinds",
      "current_value": 1200.00,
      "unrealized_pnl": -50.00
    },
    // ... bottom 15 holdings only
  ]
}
Output Format (Trade Plan):

json

{
  "plan_date": "2025-10-30",
  "decisions": [
    {
      "action": "SELL",
      "symbol": "IDXX",
      "reason": "Conviction dropped to 55, replace with higher conviction",
      "current_shares": 10,
      "target_shares": 0,
      "priority": "high"
    },
    {
      "action": "BUY",
      "symbol": "TER",
      "reason": "Top conviction (84), strong semicon momentum",
      "target_allocation_pct": 1.8,
      "priority": "high"
    },
    {
      "action": "HOLD",
      "symbol": "NVDA",
      "reason": "Conviction 68, still profitable, no better alternative",
      "current_shares": 12.5
    }
  ],
  "rationale": "Rotating from low conviction (IDXX, MS) to high conviction (TER, TMO). Maintaining 85-95 position target. Current heat 7.2% acceptable given VIX=18.5."
}
Does NOT:

Analyze individual stocks (Research does this)
Execute trades (Trading Desk does this)
Validate order feasibility (Compliance does this)
Monitor real-time prices (Operations does this)
Success Metrics:

Portfolio Sharpe Ratio > 1.2
MAR (CAGR/MaxDD) > 0.7
Turnover < 250% annually
Alpha vs. SPY (tracking error > 10%)
Decisions completed within 2 minutes (no timeouts)
Constraints:

Max 2-minute response time (timeout protection)
Input limited to ~150 stocks (92 current + 30 buy + 15 sell + context)
Must provide rationale for every decision
Cannot access raw market data (only summaries)
3. RESEARCH DEPARTMENT
Role: Intelligence gathering and candidate identification

Sub-Departments:

3A. TIER 1 SCREENING (Technical Filter)
Input: Universe of ~600 stocks (updated weekly)
Process: Apply mechanical filters (price, volume, momentum, liquidity)
Output: ~80-100 candidates passing technical criteria
Success Metric: Top 100 includes 70%+ of eventual profitable trades
3B. TIER 2 ENRICHMENT (Context Gathering)
Input: Tier 1 candidates
Process: Add sector data, recent news, fundamental context
Output: Enriched candidate data for Tier 3
Success Metric: News relevance score > 0.7 (human validation sample)
3C. TIER 3 CONVICTION ANALYSIS (Deep Analysis)
Input: Enriched candidates
Process: AI-driven conviction scoring (0-100) with BUY/HOLD/SELL recommendation
Output: Conviction scores + reasoning for each candidate
Success Metric: Conviction score correlates with 30-day forward returns (r > 0.3)
3D. EXECUTIVE SUMMARY GENERATOR
Input: All Tier 3 outputs + current positions + market context
Process:
Rank current positions by conviction (identify bottom 15 as sell candidates)
Rank new candidates by conviction (identify top 30 as buy candidates)
Format for CEO consumption (structure defined above)
Output: Executive summary JSON (CEO input)
Success Metric: CEO never requests additional data
Department-Level Success Metrics:

Processing time: Full pipeline < 30 minutes
Coverage: Analyze 100% of universe weekly
Error rate: < 5% failures (missing data, API errors)
Conviction accuracy: Top quartile scores outperform bottom quartile by >10% annualized
4. TRADING DESK
Role: Flawless order execution following broker rules

Responsibilities:

Receive validated trade plan from Compliance
Execute orders using appropriate order types
Handle retries, cancellations, timeouts
Report fill status to Accounting
Manage stops (creation, adjustment, cancellation)
Order Types (Alpaca-specific):

Entry orders: Market (during market hours only) OR Marketable Limit
Stop orders:
Whole shares: GTC stop
Fractional shares: DAY stop (must recreate daily)
Bracket orders: Entry + stop combined (preferred when possible)
Execution Rules:

Order validation: Already done by Compliance (Trading Desk trusts validated orders)
Timing: Only execute 9:35-15:55 ET (avoid open/close volatility)
Retry logic: 3 attempts with exponential backoff (100ms, 300ms, 900ms)
Timeout: Cancel unfilled orders after 5 minutes (adverse selection protection)
Stop creation: Immediately after entry fill (never leave position unprotected)
Error handling: Log all errors, report to Operations for alerting
Does NOT:

Decide which orders to submit (CEO decides this)
Validate order feasibility (Compliance does this)
Calculate position sizes (CEO does this)
Analyze market conditions (Research does this)
Success Metrics:

Fill rate: >95% of submitted orders filled
Slippage: Average < 0.15% per trade (large-cap), < 0.30% (mid-cap)
Unprotected positions: Zero tolerance (every position has stop)
Order errors: < 1% rejection rate
Stop creation: 100% within 30 seconds of fill
Failure Protocols:

Order rejected: Log error, notify Operations, do NOT retry (Compliance should have prevented)
Stop creation fails: CRITICAL alert to Operations + Board (manual intervention required)
API timeout: Retry 3x, then escalate to Operations
Broker outage: Halt all operations, use backup broker if positions at risk
5. COMPLIANCE DEPARTMENT
Role: Pre-flight validation of all trade decisions

Responsibilities:

Receive trade plan from CEO
Validate every order against broker rules and constraints
Check available cash/buying power
Verify order types are compatible with account/security
Enforce trading hours, PDT rules, wash sale exclusions
Output: Validated Trade Plan (pass to Trading Desk) OR Rejection Report (back to CEO)
Validation Checks:

Buying Power Check:

For BUY orders: sum(order_values) <= available_buying_power * 0.95 (5% buffer)
For margin accounts: Check maintenance margin requirements
Order Type Compatibility:

Fractional shares: Only DAY orders for stops
Whole shares: GTC allowed for stops
Market orders: Only during market hours (9:30-16:00 ET)
PDT Rule (if account < $25K):

Count day trades in rolling 5-day window
Block if would exceed 3 day trades
Recommend swing strategy (hold overnight)
Earnings Blackout:

Check earnings calendar for next 5 days
Block entry if earnings within window
Allow exits anytime
Wash Sale Tracking:

Check if security sold at loss within last 30 days
Block repurchase if wash sale would trigger
Maintain 31-day exclusion list
SSR (Short Sale Restriction):

If implementing shorts: check if stock down >10% from prior close
Adjust order tactics or skip short entry
Liquidity Check:

Order size < 5% of average daily volume
Spread < configured threshold (20bps large-cap, 25bps mid-cap)
Output Format (Validated Plan):

json

{
  "validation_timestamp": "2025-10-30T09:35:00",
  "original_plan": { /* CEO's trade plan */ },
  "validated_orders": [
    {
      "symbol": "TER",
      "action": "BUY",
      "shares": 10,  // Converted from allocation % to whole shares
      "order_type": "market",
      "stop_price": 154.92,
      "stop_type": "gtc",  // Whole shares
      "estimated_cost": 1685.60,
      "validation_status": "APPROVED"
    }
  ],
  "rejected_orders": [
    {
      "symbol": "INTU",
      "action": "BUY",
      "rejection_reason": "Insufficient buying power ($5766 available, $6500 required)",
      "recommendation": "Reduce position size or sell another position first"
    }
  ],
  "warnings": [
    "Total allocation would use 98% of buying power - reduced to 90% for safety buffer"
  ]
}
Does NOT:

Execute orders (Trading Desk does this)
Make strategic decisions (CEO does this)
Analyze securities (Research does this)
Success Metrics:

False negatives: Zero (never approve invalid order)
False positives: < 5% (don't reject valid orders unnecessarily)
Processing time: < 30 seconds for typical trade plan
Documentation: 100% of rejections have clear explanation
Failure Protocols:

Validation timeout: Reject entire trade plan (safety first)
Uncertain check: Reject order (err on side of caution)
Broker rule change: Halt operations, update validation logic, test, resume
6. ACCOUNTING DEPARTMENT
Role: Perfect record-keeping and performance tracking

Responsibilities:

Record every trade (order submission, fill, cancellation)
Track position history (entries, exits, adjustments)
Calculate P&L (realized, unrealized)
Maintain audit trail for compliance and analysis
Generate performance reports
Database Schema (primary tables):

trades:

trade_id (unique)
timestamp (ISO-8601 datetime string)
symbol
action (BUY/SELL)
shares (decimal)
price (decimal)
commission (decimal)
status (submitted|filled|canceled|rejected)
order_id (Alpaca order ID)
conviction_score (from Research)
rationale (from CEO)
positions:

position_id (unique)
symbol
shares (current)
avg_entry_price
current_price
unrealized_pnl
stop_price
stop_order_id
entry_date
last_updated
daily_snapshots:

snapshot_date
portfolio_value
cash
position_count
total_pnl
daily_return_pct
Data Integrity Rules:

All timestamps stored as ISO-8601 strings (not pandas Timestamp objects)
All monetary values stored as DECIMAL (not float)
Immutable logs: append-only for trades (never update/delete)
Position reconciliation: Daily comparison against broker account
Backup: Daily export to CSV + git commit
Does NOT:

Make trading decisions (CEO does this)
Validate data quality (Operations does this)
Generate strategic insights (Research does this)
Success Metrics:

Data accuracy: 100% match with broker records (daily reconciliation)
Completeness: Zero missing trades or positions
Audit trail: Can reconstruct any historical portfolio state
Performance reporting: Daily, weekly, monthly reports available
Query speed: Any performance metric retrievable < 5 seconds
7. OPERATIONS DEPARTMENT
Role: Mechanical processes and infrastructure

Responsibilities:

Data fetching (market data, corporate actions, earnings calendar)
Universe management (weekly refresh of stock list)
Workflow orchestration (schedule daily/weekly tasks)
Health monitoring (API status, data quality, system uptime)
Alerting (critical errors, performance thresholds)
Daily Tasks:

6:00 AM ET: Fetch overnight news, check for corporate actions
9:30 AM ET: Market open check (verify API connectivity)
9:35 AM ET: Trigger morning workflow (Research ? CEO ? Compliance ? Trading Desk ? Accounting)
4:00 PM ET: Market close reconciliation (verify all positions have stops)
6:00 PM ET: Daily snapshot and reporting
Weekly Tasks:

Friday 5:00 PM: Universe refresh (apply filters to ~600 stock list)
Saturday: Backup databases, export to CSV, git commit
Sunday: Performance review reports (week/month/quarter)
Monitoring:

API Health: Ping Alpaca, check quote freshness, detect outages
Data Quality: Missing bars, stale prices, volume anomalies
Position State: Verify all positions have stops, check for orphaned orders
Performance: Track slippage, fill rates, error rates
Alerts: SMS/email for critical failures (unprotected position, API outage, >5% drawdown)
Does NOT:

Make trading decisions (CEO does this)
Execute orders (Trading Desk does this)
Analyze market conditions (Research does this)
Success Metrics:

Uptime: >99% (scheduled maintenance excluded)
Data completeness: <1% missing bars
Alert accuracy: <5% false positives
Workflow reliability: Daily workflow completes successfully >95% of days
8. RISK MANAGEMENT DEPARTMENT
Role: Portfolio-level risk monitoring and intervention

Responsibilities:

Calculate portfolio heat (position risk × count)
Monitor concentration (sector, factor, single-stock limits)
Track drawdown and intervene at thresholds
Detect correlation regime shifts
Enforce risk limits (halt trading if exceeded)
Risk Metrics (calculated daily):

Portfolio Heat:

heat = S(position_risk) where position_risk = equity × r × position_count
Dynamic cap: heat_cap = min(tier_max, 4% × 20/VIX, floor 3%)
Action: If heat > cap, block new entries until reduced
Concentration:

Sector limit: Max 40% heat per GICS sector
Factor clusters: Tech+CommSvc+Semis =60%, Financials+RealEstate =60%, Energy+Materials =60%
Single stock: Max 5% of portfolio
Action: If exceeded, force sell of excess concentration
Drawdown:

10% DD: Reduce new position sizing 50%, tighten stops 20%
15% DD: Close highest-risk 30% of positions, halt new entries
20% DD: Close all positions, cease trading
Action: Automatic intervention at thresholds
Correlation Regime:

Rolling 60-day correlation matrix
Avg pairwise correlation: <0.3 low, 0.3-0.6 moderate, >0.6 high
Action: High correlation ? reduce position count, increase quality threshold
Does NOT:

Make individual position decisions (CEO does this)
Execute trades (Trading Desk does this)
Set strategic risk targets (Board does this)
Success Metrics:

MaxDD: Never exceed 20% (hard stop)
Heat violations: Zero (prevent before occurrence)
Drawdown response time: Intervention within 1 trading day
Correlation detection: Shift detected within 5 days
COMMUNICATION PROTOCOLS
Information Flow
Strategic Direction:


Board ? CEO: Strategic goals, risk tolerance, performance targets
Daily Trading Workflow:


1. Research ? Executive Summary ? CEO
2. CEO ? Trade Plan ? Compliance
3. Compliance ? Validated Plan ? Trading Desk
4. Trading Desk ? Fill Reports ? Accounting
5. Accounting ? Daily Snapshot ? Board + Risk Management
6. Risk Management ? Risk Alerts ? Board + CEO
Error Escalation:


Any Department ? Critical Error ? Operations ? Alert ? Board
Data Formats
All inter-department communication uses structured JSON with versioned schemas.

Why JSON:

Human-readable (Board can inspect)
Machine-parseable (deterministic processing)
Versioned (schema evolution without breaking changes)
Language-agnostic (works across Python, AI prompts, databases)
Schema Versioning:

Include schema_version field in every message
Backward compatibility required for 2 versions
Breaking changes require new schema version + migration plan
OPERATIONAL STANDARDS
Code Quality
All departments must:

Have unit tests (pytest) with >80% coverage
Include docstrings (Google style) for all public functions
Use type hints (mypy strict mode)
Log all significant actions (INFO level minimum)
Handle errors gracefully (no silent failures)
Follow PEP 8 style (enforced by black + flake8)
Version Control:

Git required for all code
Commit messages follow conventional commits format
Tag releases (v1.0.0, v1.1.0, etc.)
Never commit secrets (use environment variables)
Testing Standards
Before Any Code Goes Live:

Unit tests pass (department-level)
Integration tests pass (workflow-level)
Paper trading validation (minimum 50 trades)
Code review by Board (you review changes)
Git tag release version
Shadow Mode:

New departments run in parallel with old system for 2 weeks
Compare outputs, identify discrepancies
Only promote to production after validation
Monitoring and Alerting
Real-Time Alerts (immediate SMS/email):

Unprotected position detected
API outage >5 minutes
Order rejection rate >5%
Portfolio loss >5% in single day
Daily Review (email summary):

Trades executed
Performance vs. benchmark
Risk metrics (heat, concentration, drawdown)
Error log summary
Weekly Review (email report):

Sharpe ratio, MAR, win rate, profit factor
Slippage analysis
Sector/factor exposure
Top/bottom performers
SCALING PATH
Tier 1: $5K-$15K (Current)
5-8 positions
Risk per trade: 1%
Large-cap only (market cap >$5B)
Max heat: 5%
Conservative execution
Tier 2: $15K-$50K
8-15 positions
Risk per trade: 1-1.5%
Allow selective mid-caps
Max heat: 6%
Standard execution
Tier 3: $50K-$100K
12-25 positions
Risk per trade: 1.5-2%
Allow small-caps (if liquid)
Max heat: 8%
Aggressive execution
Promotion Criteria:

Minimum 200 successful trades at current tier
Sharpe ratio >1.2 over last 100 trades
MaxDD <15% at current tier
Board approval required
FAILURE AND RECOVERY
Kill Switch Criteria (Immediate Trading Halt)
Performance Failure:

Sharpe ratio <0 over last 50 trades (DSR <0)
Drawdown >1.5× historical max
Three consecutive months underperforming expectation
Risk Failure:

Unprotected position exists >1 hour
Correlation to SPY >0.85 (no alpha, just beta)
Portfolio heat exceeds cap by >50%
Operational Failure:

API outage >30 minutes with open positions
Database corruption detected
Broker rule violation detected
Recovery Protocol:

Halt all trading (close-only mode)
Close any unprotected positions immediately
Diagnostic: Identify root cause
Fix: Code change + testing
Validation: Paper trading for 50 trades
Board approval to resume
SUCCESS METRICS (Corporate Level)
Financial:

Net CAGR: 15-25% (target range)
Sharpe Ratio: 1.2-1.8
MAR: =0.7
Max Drawdown: <20%
Profit Factor: 1.5-2.2
Operational:

Uptime: >99%
Order fill rate: >95%
Unprotected positions: Zero
Data quality: <1% missing bars
Error rate: <2% of trades
Strategic:

Alpha vs. SPY: Tracking error >10%
Cost efficiency: Total costs <40bps per trade
Edge preservation: No significant decay over 12 months
REVISION HISTORY
v1.0 (2025-10-30): Initial charter

Defined 8 core departments
Established communication protocols
Set operational standards and success metrics
APPENDICES
A. Trading Wisdom Integration
The complete trading wisdom document (TRADING_WISDOM.md) is incorporated by reference and defines:

Position sizing methodology
Execution framework
Risk management protocols
Backtesting standards
All quantitative parameters
Hierarchy: If conflict between Charter and Trading Wisdom, Charter governs organizational structure, Trading Wisdom governs trading parameters.

B. Technology Stack
Core:

Python 3.11+
Alpaca API (broker)
SQLite (database)
Git (version control)

AI/ML:

GPT-5 (CEO - portfolio optimization)
Claude Code (Engineering department)
Claude Sonnet 4.5 (Strategic advisory to Board)

Infrastructure:

Sentinel (main project folder) + department subfolders
MCP Server (Sentinel state access - conversational UI to local files and tools)
GitHub (repository + CI/CD)
pytest (testing)

C. Glossary
Board: William J. Cornelius (strategic oversight)
CEO: GPT-5 Portfolio Optimizer (capital allocation)
Heat: Portfolio risk = S(position_risk)
Conviction Score: 0-100 scale from Research, higher = stronger buy
Executive Summary: Condensed input to CEO (~150 stocks max)
Trade Plan: CEO output = what to buy/sell/hold
Validated Plan: Compliance-approved trade plan
Fill: Executed order confirmation from broker
SIM Mode: Paper trading (no real money)
LIVE Mode: Real money trading (requires Board authorization)

END OF CORPORATE CHARTER