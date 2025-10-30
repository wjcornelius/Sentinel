DEPARTMENTAL_SPECIFICATIONS v1.0
Sentinel Corporation Transformation
Strategic Architecture for Autonomous Trading System
Document Version: 1.0 DRAFT
Date: October 30, 2025
Authors: C(P) (Claude PoE)
Status: Awaiting CC Technical Review
Database: sentinel.db (clean build)
Trading Status: Build & Test Phase (No Trading)

EXECUTIVE SUMMARY
This document specifies the architecture for Sentinel Corporation: a six-department autonomous trading system built from clean slate (v6.2 retired). Each department operates as a specialized Claude instance, communicating via file-based message-passing, coordinated by WJC.

Core Principles:

Component-based architecture (not monolithic)
Message-passing communication (auditable, transparent)
Human-in-the-loop decision making (WJC approves critical decisions)
Trading_Wisdom.txt as operational doctrine (Risk Department enforces)
Build right, not fast (quality over speed)
Development Phases:

Phase 1: Build & Test (No trading) - Comprehensive integration testing
Phase 2: Paper Trading (When WJC/C(P)/CC agree system is ready)
Phase 3: Real Money (If/when WJC explicitly authorizes)
ARCHITECTURE OVERVIEW
Six Departments

+-------------------------------------------------------------+
¦                    EXECUTIVE DEPARTMENT                      ¦
¦              (Coordination & Decision Making)                ¦
+-------------------------------------------------------------+
                            ?
                            ¦ Escalations & Approvals
                            ¦
        +-------------------+-------------------+
        ¦                   ¦                   ¦
        ?                   ?                   ?
+--------------+    +--------------+    +--------------+
¦   RESEARCH   ¦---?¦     RISK     ¦---?¦  PORTFOLIO   ¦
¦  DEPARTMENT  ¦    ¦ MANAGEMENT   ¦    ¦ MANAGEMENT   ¦
+--------------+    +--------------+    +--------------+
                            ¦                   ¦
                            ?                   ?
                    +--------------+    +--------------+
                    ¦   TRADING    ¦---?¦  COMPLIANCE  ¦
                    ¦  DEPARTMENT  ¦    ¦  DEPARTMENT  ¦
                    +--------------+    +--------------+
Communication Architecture
Message Format: Markdown files with YAML frontmatter

Message Directory Structure:

apache

Messages_Between_Departments/
  From_Research/
    2025-10-30_10-00_to-Risk_market-briefing.md
    2025-10-30_10-15_to-Executive_ticker-analysis-AAPL.md
  From_Risk/
    2025-10-30_10-20_to-Portfolio_risk-assessment-AAPL.md
    2025-10-30_10-25_to-Executive_risk-warning-portfolio-heat.md
  From_Portfolio/
    2025-10-30_10-30_to-Trading_allocation-decision-AAPL.md
  From_Trading/
    2025-10-30_10-35_to-Compliance_execution-log-AAPL.md
  From_Compliance/
    2025-10-30_10-40_to-Executive_audit-trail-daily.md
  From_Executive/
    2025-10-30_09-00_to-Research_daily-briefing-request.md
    2025-10-30_10-45_to-WJC_approval-request-high-risk-trade.md
Standard Message Template:

markdown

---
from: [Department Name]
to: [Department Name]
timestamp: [ISO 8601 timestamp]
message_type: [briefing|analysis|assessment|decision|log|escalation]
priority: [routine|elevated|critical]
requires_response: [true|false]
---

# [Message Title]

[Message content in markdown]

## Action Required
[What the receiving department should do]

## Deadline
[When response/action is needed]
DEPARTMENT 1: RESEARCH DEPARTMENT
Role & Responsibilities
The Research Department is Sentinel Corporation's intelligence arm. It monitors markets, analyzes news/sentiment, evaluates individual securities, and provides the foundational data that all other departments rely on.

Primary Responsibilities:

Monitor overall market conditions (indices, VIX, sector performance)
Conduct news/sentiment analysis via Perplexity API
Perform fundamental analysis on candidate tickers
Generate daily market briefings
Respond to ad-hoc research requests from other departments
Maintain research database of historical analyses
NOT Responsible For:

Risk assessment (that's Risk Management's job)
Position sizing decisions (that's Portfolio Management's job)
Trade execution (that's Trading Department's job)
Inputs
Daily Trigger Inputs:

From_Executive/[timestamp]_to-Research_daily-briefing-request.md (9:00 AM daily)
Market open signal (9:30 AM ET automated trigger)
Ad-hoc Request Inputs:

From_Risk/[timestamp]_to-Research_deep-dive-request-[TICKER].md
From_Portfolio/[timestamp]_to-Research_sector-analysis-request-[SECTOR].md
From_Executive/[timestamp]_to-Research_urgent-analysis-[TOPIC].md
Data Source Inputs (APIs):

Perplexity API: News articles, sentiment data
yfinance: Price data, volume, technical indicators
Alpha Vantage: Fundamental data (P/E, revenue, margins)
FRED API: Economic indicators (GDP, unemployment, inflation)
Outputs
Daily Outputs:

Market Briefing (10:00 AM daily)

File: From_Research/[date]_to-Risk_market-briefing.md
Content: Market condition summary, VIX level, sector performance, major news
Format: Structured markdown with JSON data block
Candidate Ticker List (10:15 AM daily)

File: From_Research/[date]_to-Portfolio_candidate-tickers.md
Content: 10-20 tickers worth considering, with preliminary analysis
Format: Table with ticker, sector, catalyst, sentiment score
Ad-hoc Outputs:

Deep Ticker Analysis (on request, <1 hour turnaround)

File: From_Research/[timestamp]_to-[RequestingDept]_analysis-[TICKER].md
Content: Comprehensive fundamental, technical, and sentiment analysis
Format: Multi-section report with data tables
Sector Analysis (on request, <2 hour turnaround)

File: From_Research/[timestamp]_to-[RequestingDept]_sector-[SECTOR].md
Content: Sector trends, leading/lagging stocks, rotation signals
Format: Comparative analysis with charts (ASCII/markdown tables)
Emergency Outputs:

Breaking News Alert (immediate, as events occur)
File: From_Research/[timestamp]_to-Executive_ALERT-[TOPIC].md
Content: Market-moving news requiring immediate attention
Format: Brief summary with recommended actions
Triggers: >2% market moves, geopolitical events, Fed announcements
Tools/APIs
Market Data:

yfinance library (primary): Real-time quotes, historical data, volume
Alpha Vantage API (secondary): Fundamentals, earnings, analyst ratings
Alpaca Market Data API (tertiary): Real-time bars for live trading hours
News & Sentiment:

Perplexity API (primary): News aggregation, sentiment analysis, context
Alternative: NewsAPI if Perplexity unavailable
Economic Data:

FRED API: GDP, unemployment, CPI, treasury yields
Alternative: Manual scraping from federalreserve.gov if API down
Technical Analysis:

pandas_ta library: RSI, MACD, Bollinger Bands, volume indicators
Custom calculations: Support/resistance, trend lines
Database Access:

Read/Write: sentinel.db tables:
research_analyses (historical ticker analyses)
market_briefings (daily briefing archive)
news_events (major market events log)
Decision Authority
Autonomous Decisions (No Approval Needed):

Which tickers to research daily
Which news sources to prioritize
Technical indicator calculations
Data refresh frequency
Research report formatting
Requires Escalation to Executive:

? NONE - Research is purely informational
Requires WJC Approval:

? NONE - Research never makes trading decisions
Collaboration with Other Departments:

Responds to ad-hoc requests within SLA (1-2 hours)
Provides data to Risk, Portfolio, Executive as requested
Does NOT provide recommendations (only data and analysis)
Failure Modes
Failure Mode 1: Perplexity API Outage

Detection: API returns error or timeout (>30 seconds)
Impact: Cannot perform news/sentiment analysis
Recovery:
Fallback to cached news from last 24 hours
Flag in market briefing: "Sentiment data stale (last updated [timestamp])"
Continue with fundamental/technical analysis only
Escalate to Executive if outage >4 hours
Failure Mode 2: Market Data API Failures

Detection: yfinance returns empty data or stale quotes
Impact: Cannot provide current prices or technical indicators
Recovery:
Attempt Alpha Vantage as backup
If both fail, attempt Alpaca Market Data API
Use last known good data with staleness warning
Escalate to Executive immediately (cannot trade on stale data)
Failure Mode 3: Incomplete Fundamental Data

Detection: Alpha Vantage missing P/E, revenue, or key metrics
Impact: Incomplete ticker analysis
Recovery:
Note missing data in analysis report
Attempt manual scraping from Yahoo Finance or company SEC filings
Provide partial analysis with clear disclaimers
Do NOT fabricate or estimate missing data
Failure Mode 4: Research Backlog (Too Many Requests)

Detection: >5 pending analysis requests in queue
Impact: SLA violations (>2 hour response time)
Recovery:
Prioritize by requester: Executive > Risk > Portfolio
Notify requesters of delay with ETA
Provide preliminary analysis (partial data) to unblock decisions
Suggest limiting concurrent research requests
Failure Mode 5: Database Write Failure

Detection: SQLite insert/update fails
Impact: Historical data not persisted
Recovery:
Continue operation (real-time analysis still works)
Log error to file: logs/research_db_errors.log
Attempt retry every 15 minutes
Escalate to CC if failure persists >1 hour (database corruption risk)
Success Metrics
Timeliness:

? Daily Market Briefing delivered by 10:00 AM (100% on-time target)
? Ad-hoc ticker analysis <1 hour response time (90% target)
? Breaking news alerts <5 minutes from event (95% target)
Accuracy:

? News sentiment correlation with subsequent price moves (>60% directional accuracy)
? Zero factual errors in fundamental data (100% target - verify all numbers)
? Technical indicator calculations match external validators (100% target)
Completeness:

? All requested data fields populated (or explicitly marked "unavailable")
? Market briefing includes all major indices, VIX, sector performance
? Ticker analyses include fundamentals, technicals, news, sentiment
Usefulness:

? Risk Department finds data sufficient for risk assessment (qualitative feedback)
? Portfolio Department successfully uses candidate lists (>50% of candidates become positions)
? Executive Department rarely needs to request additional research (research is proactive)
Reliability:

? API failure recovery works (system continues operating with degraded data)
? No missed market briefings due to technical issues (100% uptime target)
? Database maintains historical record (zero data loss)
v6.2 Component Mapping
Components to Migrate from v6.2 ? Research Department:

perplexity_news.py ? Research Department (news/sentiment analysis)

Current function: Queries Perplexity for news
New role: Core research capability
Refactoring needed: Wrap in message-based interface
context_builder.py ? Research Department (market context assembly)

Current function: Builds context from multiple sources
New role: Assembles daily market briefing
Refactoring needed: Output to markdown message instead of dict
Market data fetching (currently in sentinel_morning_workflow.py) ? Research

Current function: Gets prices via yfinance
New role: Centralized market data service
Refactoring needed: Separate into standalone module
Tier 1/2/3 stock analysis (currently in stock_selection.py) ? Research

Current function: Filters stocks by market cap tiers
New role: Initial candidate screening
Refactoring needed: More sophisticated screening based on market conditions
Components to BUILD NEW for Research Department:

Message interface module

Reads requests from Messages_Between_Departments/
Writes responses in standard format
Manages request queue and prioritization
Sentiment scoring system

Quantifies Perplexity news sentiment (-100 to +100 scale)
Aggregates multiple news sources
Historical sentiment tracking
Economic indicator monitor

FRED API integration
Tracks GDP, unemployment, CPI, yields
Flags significant changes
Research database schema

sql

CREATE TABLE research_analyses (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    analysis_date DATE NOT NULL,
    fundamentals JSON,
    technicals JSON,
    sentiment_score REAL,
    news_summary TEXT,
    analyst_rating TEXT,
    full_report_path TEXT
);

CREATE TABLE market_briefings (
    id INTEGER PRIMARY KEY,
    briefing_date DATE NOT NULL,
    market_condition TEXT,
    vix_level REAL,
    sector_performance JSON,
    major_news TEXT,
    full_briefing_path TEXT
);
Effort Estimate for Research Department:

Migration of existing components: 8-12 hours (CC estimate needed)
New message interface: 4-6 hours
New sentiment system: 6-8 hours
New economic monitor: 4-6 hours
Database schema + integration: 4-6 hours
Testing & validation: 8-12 hours
Total: 34-50 hours
DEPARTMENT 2: RISK MANAGEMENT DEPARTMENT
Role & Responsibilities
The Risk Management Department is Sentinel Corporation's guardian of Trading_Wisdom.txt doctrine. It evaluates all proposed trades and portfolio changes against established risk parameters, producing risk assessments that inform decision-making.

Primary Responsibilities:

Enforce Trading_Wisdom.txt doctrine (all rules and principles)
Calculate portfolio risk metrics (heat, CVaR, correlation, concentration)
Assess individual trade risk (position sizing, volatility, liquidity)
Monitor real-time risk during market hours
Produce daily risk reports
Escalate risk warnings to Executive Department
Maintain risk assessment database
NOT Responsible For:

Making final trade decisions (that's Executive's job)
Executing trades (that's Trading Department's job)
Selecting tickers (that's Research's job)
Portfolio allocation (that's Portfolio Management's job)
Philosophy: Risk acts as advisor, not gatekeeper. It produces risk assessments with recommendations, but Executive Department makes final decisions. WJC always has veto power.

Inputs
Daily Inputs:

From_Research/[date]_to-Risk_market-briefing.md (market conditions)
From_Portfolio/[date]_to-Risk_current-positions.md (existing portfolio state)
Trade Proposal Inputs:

From_Portfolio/[timestamp]_to-Risk_trade-proposal-[TICKER].md
Contains: ticker, proposed action (BUY/SELL), quantity, rationale
From_Executive/[timestamp]_to-Risk_emergency-assessment-[TOPIC].md
Contains: urgent risk assessment request (e.g., market crash scenario)
Continuous Monitoring Inputs:

Market data (VIX, volatility, correlations) via Research Department
Position P&L updates via Portfolio Department
Real-time heat calculations (updated every 15 minutes during market hours)
Outputs
Daily Outputs:

Daily Risk Report (4:30 PM daily, after market close)
File: From_Risk/[date]_to-Executive_daily-risk-report.md
Content: Portfolio heat, CVaR, concentration, correlation matrix, warnings
Format: Structured report with metrics table
Trade Assessment Outputs:

Trade Risk Assessment (on request, <30 minutes turnaround)
File: From_Risk/[timestamp]_to-Portfolio_assessment-[TICKER].md
Also CC: From_Risk/[timestamp]_to-Executive_assessment-[TICKER].md
Content: Risk score (0-10), Trading_Wisdom.txt compliance analysis, recommendation
Format: Structured assessment with PASS/WARNING/FAIL flags
Alert Outputs:

Risk Warning (immediate, when thresholds exceeded)
File: From_Risk/[timestamp]_to-Executive_WARNING-[ISSUE].md
Content: What threshold was exceeded, current value, recommended action
Format: Brief alert with severity level (WARNING/CRITICAL)
Examples:
Portfolio heat >7% (WARNING)
Portfolio heat >8% (CRITICAL - hard limit)
Single position >15% (CRITICAL - hard limit)
Sector concentration >40% (WARNING)
Analysis Outputs:

Scenario Analysis (on request, <1 hour)
File: From_Risk/[timestamp]_to-[Requester]_scenario-[SCENARIO].md
Content: "What if" analysis (e.g., "what if market drops 10%?")
Format: Impact table showing portfolio changes under scenario
Tools/APIs
Risk Calculation Tools:

pandas/numpy: Portfolio math, correlation matrices, CVaR calculations
scipy.stats: Statistical distributions for risk modeling
Custom risk models: Heat calculation, liquidity risk, concentration risk
Data Sources:

Market data via Research Department messages (no direct API calls)
Position data via Portfolio Department messages
Historical volatility: Calculate from price data in sentinel.db
Trading_Wisdom.txt Parser:

Custom Python module: trading_wisdom_parser.py
Parses all rules from Trading_Wisdom.txt
Categorizes rules as:
Hard constraints (never violate - coded limits)
Soft constraints (prefer to follow - Risk evaluates)
Heuristics (guidance - Risk considers)
Database Access:

Read/Write: sentinel.db tables:
risk_assessments (all trade assessments)
daily_risk_reports (historical risk metrics)
risk_warnings (alert history)
trading_wisdom_violations (doctrine violation log)
Decision Authority
Autonomous Decisions:

Which risk metrics to calculate
How to weight different risk factors
Risk score methodology (0-10 scale)
When to issue warnings vs alerts
Requires Escalation to Executive:

? Risk score =7 (elevated risk) ? Executive must review before proceeding
? Hard constraint violation detected ? Executive must override or reject
? Portfolio heat >7% ? Executive must approve continued trading
? Unusual correlation shifts ? Executive should be aware
Requires WJC Approval:

? Risk score =9 (critical risk) ? WJC must explicitly approve
? Hard constraint override ? WJC must authorize exception to Trading_Wisdom.txt
? Portfolio heat >8% ? WJC must approve (doctrine violation)
Cannot Do (No Authority):

? Block trades directly (can only recommend against)
? Modify position sizes (can only suggest adjustments)
? Alter Trading_Wisdom.txt (doctrine is immutable without WJC approval)
Failure Modes
Failure Mode 1: Missing Position Data

Detection: Portfolio Department doesn't provide current positions
Impact: Cannot calculate portfolio-level risk metrics
Recovery:
Use last known positions from database
Flag risk report as "based on stale data (last updated [timestamp])"
Issue WARNING to Executive: cannot assess current risk accurately
Recommend halting new trades until position data available
Failure Mode 2: Market Data Unavailable

Detection: Research Department doesn't provide VIX or volatility data
Impact: Cannot assess market-relative risk
Recovery:
Use historical average volatility (30-day rolling)
Flag assessment as "using historical volatility estimates"
Conservative bias: Increase risk scores by 1 point when data unavailable
Recommend reducing position sizes until live data restored
Failure Mode 3: Trading_Wisdom.txt Interpretation Ambiguity

Detection: Trade scenario not clearly covered by doctrine
Impact: Cannot definitively assess compliance
Recovery:
Document the ambiguity in assessment
Provide two scenarios: "if we interpret conservatively..." and "if liberally..."
Escalate to Executive with recommendation
Suggest WJC clarify Trading_Wisdom.txt for future cases
Failure Mode 4: Calculation Error (Bug in Risk Model)

Detection: Risk metric produces impossible value (e.g., negative heat)
Impact: Invalid risk assessment
Recovery:
HALT: Do not produce assessment
Immediately escalate to CC: "Bug in risk calculation module"
Provide raw data to CC for debugging
Manual calculation by WJC/C(P) if urgent
Fix bug before resuming automated assessments
Failure Mode 5: Contradictory Risk Signals

Detection: Low volatility but high heat, or similar contradictions
Impact: Unclear risk recommendation
Recovery:
Document the contradiction explicitly
Explain which metric is more concerning in current context
Provide recommendation based on worst-case metric
Flag for Executive review (not routine approval)
Success Metrics
Accuracy:

? Risk scores correlate with actual drawdowns (higher risk ? larger drawdowns)
? Trading_Wisdom.txt violation detection: Zero false negatives (catch all violations)
? Risk warnings actionable: >80% of warnings prevent subsequent issues
Timeliness:

? Trade assessments <30 minutes (95% target)
? Risk warnings <5 minutes from threshold breach (100% target)
? Daily risk report by 4:30 PM (100% target)
Completeness:

? All Trading_Wisdom.txt rules evaluated for each trade
? All relevant risk metrics calculated (heat, CVaR, concentration, correlation)
? Clear recommendation provided (APPROVE/CONDITIONAL/REJECT)
Usefulness:

? Executive Department follows recommendations >90% of time
? WJC overrides <10% of assessments (high trust in Risk's judgment)
? Portfolio performance aligns with doctrine (staying within heat limits correlates with avoiding disasters)
Conservatism:

? False alarms acceptable (better safe than sorry)
? When uncertain, Risk errs on conservative side
? Zero instances of Risk approving a trade that later violated doctrine
v6.2 Component Mapping
Components to Migrate from v6.2 ? Risk Department:

Heat calculation (currently in position_manager.py) ? Risk Department

Current function: Calculates portfolio heat
New role: Core risk metric
Refactoring needed: Separate from position management, make standalone
Position sizing logic (currently in position_manager.py) ? Risk Department

Current function: Determines share count based on risk
New role: Risk validates proposed sizes, suggests adjustments
Refactoring needed: Risk advises, doesn't decide (Portfolio decides)
Risk_tolerance checking (scattered across v6.2) ? Risk Department

Current function: Ad-hoc risk checks
New role: Centralized, comprehensive risk assessment
Refactoring needed: Consolidate all risk logic into Risk Department
Components to BUILD NEW for Risk Department:

Trading_Wisdom.txt parser and rule engine

Parses all rules from Trading_Wisdom.txt
Categorizes rules (hard/soft/heuristics)
Evaluates trades against each rule
Produces compliance report
CVaR calculator

Conditional Value at Risk calculation
Uses historical return distributions
Estimates tail risk
Correlation matrix generator

Calculates inter-position correlations
Identifies concentration risk
Flags correlated positions
Risk scoring model

Combines multiple risk metrics into 0-10 score
Weighted by current market conditions
Produces actionable recommendations
Risk database schema

sql

CREATE TABLE risk_assessments (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    assessment_date TIMESTAMP NOT NULL,
    risk_score REAL NOT NULL,
    recommendation TEXT NOT NULL,
    trading_wisdom_compliance JSON,
    metrics JSON,
    full_assessment_path TEXT
);

CREATE TABLE daily_risk_reports (
    id INTEGER PRIMARY KEY,
    report_date DATE NOT NULL,
    portfolio_heat REAL,
    cvar REAL,
    concentration JSON,
    warnings TEXT,
    full_report_path TEXT
);

CREATE TABLE risk_warnings (
    id INTEGER PRIMARY KEY,
    warning_timestamp TIMESTAMP NOT NULL,
    severity TEXT NOT NULL,
    issue TEXT NOT NULL,
    threshold_value REAL,
    current_value REAL,
    resolution TEXT
);
Effort Estimate for Risk Department:

Migration of heat/sizing logic: 6-8 hours
Trading_Wisdom.txt parser: 12-16 hours (complex rule engine)
CVaR calculator: 6-8 hours
Correlation matrix: 4-6 hours
Risk scoring model: 8-12 hours
Database schema + integration: 4-6 hours
Testing & validation: 12-16 hours
Total: 52-72 hours
DEPARTMENT 3: TRADING DEPARTMENT
Role & Responsibilities
The Trading Department is Sentinel Corporation's execution arm. It interfaces directly with Alpaca API to execute approved trades, monitors order fills, handles execution issues, and maintains execution logs.

Primary Responsibilities:

Execute approved trades via Alpaca API
Monitor order status (pending, filled, rejected, cancelled)
Handle partial fills and execution issues
Implement hard constraint guards (coded risk limits)
Log all execution activity
Provide execution reports to Compliance Department
Maintain connection to Alpaca (authentication, heartbeat)
NOT Responsible For:

Deciding what to trade (that's Portfolio Management's job)
Risk assessment (that's Risk Management's job)
Compliance review (that's Compliance Department's job)
Strategic decisions (that's Executive's job)
Philosophy: Trading is a pure execution layer. It receives orders from Portfolio Department (via Executive approval), validates they don't violate hard constraints, and executes. It does NOT make trading decisions.

Inputs
Order Inputs:

From_Portfolio/[timestamp]_to-Trading_order-[TICKER].md
Contains: ticker, action (BUY/SELL), quantity, order_type (MARKET/LIMIT), limit_price (if applicable)
Must include: executive_approval: true field (proof of Executive sign-off)
Monitoring Inputs:

Alpaca order status webhooks (or polling every 10 seconds for pending orders)
Alpaca account status (buying power, positions, cash)
Manual Intervention Inputs:

From_Executive/[timestamp]_to-Trading_cancel-order-[ORDER_ID].md (cancel pending order)
From_Executive/[timestamp]_to-Trading_modify-order-[ORDER_ID].md (change limit price)
Outputs
Execution Confirmation Outputs:

Order Submitted Confirmation (immediate, <10 seconds after order placed)

File: From_Trading/[timestamp]_to-Portfolio_order-submitted-[TICKER].md
Also CC: From_Trading/[timestamp]_to-Compliance_order-submitted-[TICKER].md
Content: Order ID, ticker, quantity, order type, timestamp
Format: Structured confirmation with Alpaca order ID
Order Filled Confirmation (immediate, when Alpaca confirms fill)

File: From_Trading/[timestamp]_to-Portfolio_order-filled-[TICKER].md
Also CC: From_Trading/[timestamp]_to-Compliance_order-filled-[TICKER].md
Content: Fill price, quantity filled, commission, fill timestamp
Format: Structured confirmation with execution details
Exception Outputs:

Order Rejected Alert (immediate, if Alpaca rejects order)

File: From_Trading/[timestamp]_to-Executive_REJECTED-[TICKER].md
Also CC: From_Trading/[timestamp]_to-Compliance_order-rejected-[TICKER].md
Content: Rejection reason, what to do next
Format: Alert with recommended remediation
Examples: Insufficient buying power, invalid ticker, market closed
Partial Fill Report (if order partially filled after 5 minutes)

File: From_Trading/[timestamp]_to-Portfolio_partial-fill-[TICKER].md
Content: Quantity filled vs requested, decision needed (cancel remainder or wait)
Format: Status report with options
Daily Outputs:

Daily Execution Log (4:30 PM daily)
File: From_Trading/[date]_to-Compliance_daily-execution-log.md
Content: All orders executed today, fills, rejections, commissions
Format: Table of all trading activity
Tools/APIs
Alpaca API:

alpaca-trade-api Python library (primary interface)
Endpoints used:
/v2/orders (submit, cancel, get order status)
/v2/account (get buying power, positions)
/v2/positions (current holdings)
/v2/positions/{symbol} (close position)
Authentication:

API Key and Secret (stored in environment variables or secure config)
Paper trading endpoint: https://paper-api.alpaca.markets
Real money endpoint: https://api.alpaca.markets (Phase 3 only)
Hard Constraint Guards (Coded Limits):

python

Run

# These are Trading Department's AUTOMATED blocks (no human approval needed)

MAX_POSITION_HEAT = 0.08  # Never allow portfolio heat >8%
MAX_SINGLE_POSITION = 0.15  # Never allow single position >15% of portfolio
MIN_LIQUIDITY = 500000  # Never trade stocks with <500K daily volume
MAX_ORDER_SIZE_PERCENT = 0.10  # Never trade >10% of daily volume (slippage risk)
MARKET_HOURS_ONLY = True  # Never submit orders outside 9:30 AM - 4:00 PM ET
NO_PENNY_STOCKS = 5.00  # Never trade stocks <$5 per share

# If ANY of these violated, order is REJECTED immediately (no escalation needed)
Database Access:

Read/Write: sentinel.db tables:
orders (all orders submitted)
fills (all order fills)
rejections (all rejected orders with reasons)
daily_execution_logs (daily summary)
Decision Authority
Autonomous Decisions:

? Execute orders that pass hard constraint checks
? Cancel orders if Alpaca reports "order would violate day trade rule"
? Retry orders if temporary network issue
? Choose market vs limit order type (based on Portfolio's specification)
Requires Escalation to Executive:

?? Partial fill after 5 minutes (should we cancel remainder or wait?)
?? Repeated rejections for same order (>3 retries failed)
?? Alpaca account issue (e.g., "pattern day trader restriction")
?? Execution price significantly worse than expected (>2% slippage on market order)
Requires WJC Approval:

? NONE - Trading never overrides hard constraints
(If WJC wants to override hard constraint, he must change the code itself)
Cannot Do (No Authority):

? Submit orders without Executive approval field
? Modify order quantity or ticker (only Portfolio can change these)
? Trade outside market hours (unless explicitly coded exception)
? Violate any hard constraint (even if Executive requests it)
Failure Modes
Failure Mode 1: Alpaca API Outage

Detection: API returns 500 error or timeouts
Impact: Cannot execute trades
Recovery:
Retry with exponential backoff (1s, 2s, 4s, 8s, 16s)
After 5 retries, escalate to Executive: "Alpaca API unavailable"
Provide manual execution instructions to WJC (if urgent)
Queue orders for automatic submission when API restored
Monitor Alpaca status page for outage notifications
Failure Mode 2: Order Rejected (Insufficient Buying Power)

Detection: Alpaca returns "insufficient buying power" error
Impact: Cannot execute buy order
Recovery:
Check if Portfolio's calculation was outdated (maybe a recent fill consumed cash)
Report actual available buying power to Portfolio
Suggest reduced order size that fits available cash
Escalate to Executive for decision: reduce size or cancel
Failure Mode 3: Partial Fill (Illiquid Stock)

Detection: Order submitted, only partial quantity filled after 5 minutes
Impact: Position smaller than intended
Recovery:
Report partial fill to Portfolio
Options:
Wait longer (if stock is moderately liquid)
Cancel remainder (if stock is very illiquid)
Submit additional order (if still want full position)
Escalate to Executive with recommendation based on liquidity data
Failure Mode 4: Execution Price Slippage (>2%)

Detection: Fill price differs from expected price by >2%
Impact: Worse execution than anticipated
Recovery:
Document slippage in execution log
Report to Compliance (potential issue)
Analyze: Was this due to market volatility or illiquidity?
Recommend using limit orders instead of market orders for this ticker
If slippage >5%, escalate to Executive (may indicate problem)
Failure Mode 5: Hard Constraint Violated (Code Bug)

Detection: Order passed validation but shouldn't have (e.g., heat calculation wrong)
Impact: Doctrine violation
Recovery:
HALT all trading immediately
Cancel pending orders
Escalate to CC: "Bug in hard constraint validation"
Manual review by WJC before resuming trading
Fix bug and add regression test
Failure Mode 6: Duplicate Order Submission

Detection: Same ticker, quantity, action submitted twice within 1 minute
Impact: Accidentally double position size
Recovery:
Reject second order automatically
Alert Executive: "Duplicate order detected and blocked"
Investigate: Was this a retry (expected) or a bug (unexpected)?
Log incident for review
Success Metrics
Execution Quality:

? Fill price within 0.5% of expected (for liquid stocks, >1M daily volume)
? Fill price within 1.0% of expected (for less liquid stocks, 100K-1M volume)
? Zero executions of orders that violate hard constraints (perfect validation)
Timeliness:

? Order submitted to Alpaca within 10 seconds of receiving Portfolio order
? Order confirmations sent within 10 seconds of Alpaca confirmation
? Rejected orders reported within 10 seconds of Alpaca rejection
Reliability:

? 100% of approved orders executed (or rejection reason documented)
? Zero duplicate orders (duplicate detection works)
? Zero manual intervention needed for routine orders
Auditability:

? Every order has complete audit trail (submitted ? filled/rejected ? logged)
? Daily execution log matches Alpaca's records (100% reconciliation)
? Compliance Department can reconstruct all trades from logs
Uptime:

? Trading Department available during market hours (9:30 AM - 4:00 PM ET, 100% uptime)
? Alpaca API connection maintained (heartbeat every 60 seconds)
v6.2 Component Mapping
Components to Migrate from v6.2 ? Trading Department:

Alpaca order submission (currently in trading_executor.py) ? Trading Department

Current function: Submits orders via Alpaca API
New role: Core execution capability
Refactoring needed: Add hard constraint validation before submission
Order monitoring (currently in trading_executor.py) ? Trading Department

Current function: Checks order status
New role: Tracks fills, partial fills, rejections
Refactoring needed: More sophisticated partial fill handling
Position closing logic (currently in position_manager.py) ? Trading Department

Current function: Closes positions via Alpaca
New role: Executes sell orders
Refactoring needed: Same as buy orders (validation, logging)
Components to BUILD NEW for Trading Department:

Hard constraint validation module

python

Run

def validate_order_hard_constraints(order, current_portfolio, market_data):
    """
    Returns (is_valid: bool, violation_reason: str)
    """
    # Check all hard constraints
    # If ANY fail, reject order (no exceptions)
Duplicate order detection

Maintains cache of recent orders (last 5 minutes)
Rejects exact duplicates
Allows retries with different parameters
Slippage analyzer

Compares expected vs actual fill price
Flags excessive slippage (>2%)
Recommends limit orders for problematic tickers
Trading database schema

sql

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    alpaca_order_id TEXT UNIQUE NOT NULL,
    ticker TEXT NOT NULL,
    action TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    order_type TEXT NOT NULL,
    limit_price REAL,
    submitted_timestamp TIMESTAMP NOT NULL,
    executive_approval_path TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE fills (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    fill_price REAL NOT NULL,
    quantity_filled INTEGER NOT NULL,
    commission REAL,
    fill_timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE rejections (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    rejection_reason TEXT NOT NULL,
    rejection_timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
Effort Estimate for Trading Department:

Migration of Alpaca execution logic: 6-8 hours
Hard constraint validation module: 8-12 hours (critical to get right)
Duplicate detection: 3-4 hours
Slippage analyzer: 4-6 hours
Order monitoring enhancements: 6-8 hours
Database schema + integration: 4-6 hours
Testing & validation: 12-16 hours (extensive testing needed for execution)
Total: 43-60 hours
DEPARTMENT 4: PORTFOLIO MANAGEMENT DEPARTMENT
Role & Responsibilities
The Portfolio Management Department is Sentinel Corporation's strategic allocation brain. It decides which positions to hold, how much capital to allocate to each, when to enter/exit, and maintains the overall portfolio composition.

Primary Responsibilities:

Maintain current portfolio state (positions, cash, buying power)
Decide position entry/exit based on Research analysis + Risk assessment
Determine position sizes (within Risk Department's constraints)
Manage portfolio rebalancing
Track P&L (realized and unrealized)
Propose trades to Executive Department for approval
Respond to margin calls or portfolio issues
NOT Responsible For:

Ticker research (that's Research Department's job)
Risk assessment (that's Risk Management's job)
Trade execution (that's Trading Department's job)
Final trade approval (that's Executive's job)
Philosophy: Portfolio Management is the strategic allocation layer. It translates Research insights and Risk constraints into concrete position sizing decisions.

Inputs
Daily Inputs:

From_Research/[date]_to-Portfolio_candidate-tickers.md (potential investments)
From_Research/[date]_to-Portfolio_market-briefing.md (market context)
From_Risk/[date]_to-Portfolio_daily-risk-report.md (current risk state)
Current State Inputs:

Alpaca API: Current positions, cash balance, buying power
Note: Portfolio reads directly from Alpaca for real-time position data
This is exception to "all data via messages" rule (Alpaca is source of truth for positions)
Trade Assessment Inputs:

From_Risk/[timestamp]_to-Portfolio_assessment-[TICKER].md (risk assessment for proposed trade)
Executive Directive Inputs:

From_Executive/[timestamp]_to-Portfolio_directive-[ACTION].md
Examples: "Reduce exposure to Tech sector", "Raise cash to 20%", "Close position in AAPL"
Outputs
Trade Proposal Outputs:

Buy Order Proposal (when Portfolio wants to enter new position)

File: From_Portfolio/[timestamp]_to-Risk_trade-proposal-BUY-[TICKER].md
Content: Ticker, quantity, entry rationale, target allocation %
Next step: Wait for Risk assessment before submitting to Executive
Sell Order Proposal (when Portfolio wants to exit position)

File: From_Portfolio/[timestamp]_to-Risk_trade-proposal-SELL-[TICKER].md
Content: Ticker, quantity (or % of position), exit rationale
Next step: Wait for Risk assessment before submitting to Executive
Final Trade Order (after Risk approves and Executive authorizes)

File: From_Portfolio/[timestamp]_to-Trading_order-[TICKER].md
Content: Ticker, action, quantity, order_type, limit_price (if applicable), executive_approval: true
This is what Trading Department executes
Portfolio State Outputs:

Daily Portfolio Summary (4:00 PM daily)

File: From_Portfolio/[date]_to-Executive_daily-summary.md
Also CC: From_Portfolio/[date]_to-Compliance_daily-summary.md
Content: All positions, cash, total value, daily P&L, sector allocation
Format: Structured report with tables
Current Positions Report (on request, or daily at 9:45 AM for Risk)

File: From_Portfolio/[timestamp]_to-Risk_current-positions.md
Content: Each position's ticker, quantity, cost basis, current price, unrealized P&L
Format: JSON + markdown table
Alert Outputs:

Portfolio Issue Alert (immediate, when issues detected)
File: From_Portfolio/[timestamp]_to-Executive_ALERT-[ISSUE].md
Examples:
Margin call imminent
Position dropped >10% today
Buying power exhausted
Unexpected position discrepancy (Alpaca shows position we didn't order)
Tools/APIs
Alpaca API (Direct Access):

Portfolio Department is only department with direct Alpaca API access (besides Trading)
Endpoints used:
/v2/account (cash, buying power, portfolio value)
/v2/positions (all current holdings)
/v2/positions/{symbol} (specific position details)
Read-only access (no order submission - that's Trading's job)
Position Tracking:

pandas DataFrame: In-memory representation of portfolio
Synchronized with Alpaca every 15 minutes during market hours
Updated immediately after Trading Department reports fills
Allocation Models:

Equal weight: Each position gets equal allocation (simple)
Risk-parity: Allocate based on volatility (lower vol ? larger position)
Conviction-weighted: Allocate based on Research sentiment scores
Custom: WJC can specify allocation strategy via Trading_Wisdom.txt
Database Access:

Read/Write: sentinel.db tables:
portfolio_snapshots (daily portfolio state)
position_history (all position entries/exits)
pnl_tracking (realized and unrealized P&L)
Decision Authority
Autonomous Decisions:

? Which candidate tickers from Research to pursue (based on risk/reward)
? Position sizing (within Risk Department's limits)
? When to rebalance (if positions drift from target allocation)
? Profit-taking levels (can sell partial positions to lock in gains)
? Stop-loss triggers (can propose exits if position down >X%)
Requires Risk Department Review:

? ALL new position entries (must get risk assessment first)
? ALL position increases (must verify doesn't violate concentration limits)
? Portfolio rebalancing (must verify doesn't increase overall heat)
Requires Executive Approval:

? ALL trades (after Risk assessment, Executive gives final authorization)
? Allocation strategy changes (e.g., switching from equal-weight to risk-parity)
? Deviation from Trading_Wisdom.txt allocation guidance
Requires WJC Approval:

? Allocation strategy overhaul (e.g., moving from long-only to long/short)
? Raising cash above 30% (defensive positioning)
? Concentrating >50% in single sector (aggressive bet)
Cannot Do (No Authority):

? Execute trades directly (must go through Trading Department)
? Override Risk Department's hard constraint violations
? Trade outside Alpaca account (no external brokers)
Failure Modes
Failure Mode 1: Position Discrepancy (Alpaca vs Internal Records)

Detection: Alpaca shows position we don't have in database (or vice versa)
Impact: Portfolio state out of sync, incorrect allocation decisions
Recovery:
HALT all trading immediately
Escalate to Executive: "Position discrepancy detected"
Reconcile: Which is correct - Alpaca or our records?
Likely cause: Missed fill confirmation from Trading Department
Manual reconciliation by WJC
Update database to match Alpaca (Alpaca is always source of truth)
Resume trading only after full reconciliation
Failure Mode 2: Insufficient Buying Power for Proposed Trade

Detection: Portfolio proposes trade, but Alpaca buying power insufficient
Impact: Cannot execute trade
Recovery:
Recalculate available cash (maybe recent fill consumed more than expected)
Reduce position size to fit available buying power
Re-submit proposal to Risk with smaller size
If multiple positions competing for limited cash, prioritize by conviction/risk-adjusted return
Failure Mode 3: Research Provides No Candidate Tickers

Detection: Research's daily candidate list is empty
Impact: No new investment opportunities
Recovery:
NOT a failure - sometimes markets offer nothing attractive
Focus on managing existing positions
Consider trimming losers or rebalancing
Request specific sector analysis from Research if needed
Escalate to Executive if this persists >5 days (may indicate Research issue)
Failure Mode 4: Risk Department Rejects All Proposals

Detection: Portfolio proposes 5+ trades, Risk rejects all
Impact: Cannot deploy capital
Recovery:
Review Risk's rejection reasons (are they valid?)
If rejections due to high portfolio heat: Trim existing positions first to create headroom
If rejections due to poor quality candidates: Request better research from Research Department
If rejections seem overly conservative: Escalate to Executive for review of Risk's methodology
Possible: Trading_Wisdom.txt too restrictive for current market ? WJC may need to adjust doctrine
Failure Mode 5: Unrealized Loss Exceeds Stop-Loss Threshold

Detection: Position down >15% from entry (or whatever threshold in Trading_Wisdom.txt)
Impact: Discipline requires exiting losing position
Recovery:
Automatically propose SELL order to Risk
Document reason: "Stop-loss triggered"
If Risk/Executive want to hold position despite loss, they must explicitly override
This is NOT a failure - it's doctrine enforcement
Track: How often do we stop out vs hold through drawdowns? (measure discipline)
Failure Mode 6: Alpaca API Unavailable (Cannot Get Position Data)

Detection: Alpaca API returns errors when requesting /v2/positions
Impact: Cannot determine current portfolio state
Recovery:
Use last known positions from database (cached state)
Flag all calculations as "based on stale data (last updated [timestamp])"
Do NOT propose new trades until live data restored
Escalate to Executive: "Operating on stale position data"
If outage >1 hour, consider manual position check via Alpaca web dashboard
Success Metrics
Allocation Quality:

? Actual allocation matches intended allocation (within 2% per position)
? No unintended concentration (no position >15%, no sector >40% unless explicitly approved)
? Cash balance maintained within target range (10-20% unless market conditions dictate otherwise)
Decision Quality:

? Winning trades >losing trades (>55% win rate target)
? Average winner > average loser (risk/reward >1.5:1 target)
? Stop-loss discipline (actually exit when threshold hit, no "hope trades")
Execution:

? Trade proposals to Risk within 30 minutes of Research providing candidates
? Final orders to Trading within 15 minutes of Executive approval
? Daily portfolio summary delivered by 4:00 PM (100% on-time)
Risk Management Integration:

? Zero trades executed without Risk assessment
? Zero hard constraint violations (perfect coordination with Risk)
? Portfolio heat stays within doctrine limits (100% compliance)
Reconciliation:

? Portfolio records match Alpaca 100% (daily reconciliation, zero discrepancies)
? P&L calculations match Alpaca's performance page (within $0.01)
v6.2 Component Mapping
Components to Migrate from v6.2 ? Portfolio Department:

Position tracking (currently in position_manager.py) ? Portfolio Department

Current function: Tracks open positions
New role: Centralized position state management
Refactoring needed: Separate tracking from sizing/risk (those go to Risk)
Stock selection (currently in stock_selection.py) ? Portfolio Department

Current function: Chooses which stocks to trade
New role: Evaluates Research candidates, decides which to pursue
Refactoring needed: Move research to Research Dept, move risk to Risk Dept, Portfolio decides allocation
Rebalancing logic (currently in rebalance.py) ? Portfolio Department

Current function: Adjusts position sizes
New role: Identifies when rebalancing needed, proposes adjustments
Refactoring needed: Portfolio proposes, Risk validates, Executive approves
P&L tracking (currently in position_manager.py) ? Portfolio Department

Current function: Calculates gains/losses
New role: Comprehensive P&L reporting
Refactoring needed: Separate realized vs unrealized, track by position and portfolio-wide
Components to BUILD NEW for Portfolio Department:

Allocation strategy engine

Implements equal-weight, risk-parity, or custom allocation
Configurable via Trading_Wisdom.txt or Executive directive
Produces target weights for each position
Trade proposal generator

Formats proposals in standard message format
Includes rationale, target allocation, alternatives considered
Auto-populated with Research data and current portfolio state
Position reconciliation module

Compares internal records to Alpaca positions
Flags discrepancies
Suggests corrections
Portfolio database schema

sql

CREATE TABLE portfolio_snapshots (
    id INTEGER PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    total_value REAL NOT NULL,
    cash_balance REAL NOT NULL,
    positions JSON NOT NULL,
    sector_allocation JSON,
    daily_pnl REAL
);

CREATE TABLE position_history (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    entry_date DATE NOT NULL,
    entry_price REAL NOT NULL,
    entry_quantity INTEGER NOT NULL,
    exit_date DATE,
    exit_price REAL,
    exit_quantity INTEGER,
    realized_pnl REAL
);

CREATE TABLE pnl_tracking (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    realized_pnl REAL NOT NULL,
    unrealized_pnl REAL NOT NULL,
    total_pnl REAL NOT NULL,
    cumulative_pnl REAL NOT NULL
);
Effort Estimate for Portfolio Department:

Migration of position tracking: 8-12 hours
Migration of stock selection logic: 6-8 hours
Allocation strategy engine: 10-14 hours
Trade proposal generator: 6-8 hours
Position reconciliation: 6-8 hours
P&L tracking enhancements: 8-12 hours
Database schema + integration: 6-8 hours
Testing & validation: 12-16 hours
Total: 62-86 hours
DEPARTMENT 5: COMPLIANCE DEPARTMENT
Role & Responsibilities
The Compliance Department is Sentinel Corporation's record-keeper and auditor. It maintains complete audit trails of all trading activity, ensures regulatory compliance (even for paper trading), and produces reports for WJC review.

Primary Responsibilities:

Log all trading activity (orders, fills, rejections, modifications)
Maintain complete audit trail (who decided what, when, why)
Track regulatory compliance (pattern day trading rules, settlement violations, etc.)
Produce daily compliance reports
Archive all inter-departmental messages
Flag suspicious activity or policy violations
Respond to audit requests from WJC
NOT Responsible For:

Making trading decisions (that's Portfolio/Executive's job)
Blocking trades (that's Risk/Trading's job via hard constraints)
Risk assessment (that's Risk Management's job)
Philosophy: Compliance is a watchdog and historian. It ensures complete transparency and accountability, but does not interfere with operations unless critical compliance issue detected.

Inputs
Trading Activity Inputs:

From_Trading/[timestamp]_to-Compliance_order-submitted-[TICKER].md
From_Trading/[timestamp]_to-Compliance_order-filled-[TICKER].md
From_Trading/[timestamp]_to-Compliance_order-rejected-[TICKER].md
From_Trading/[date]_to-Compliance_daily-execution-log.md
Portfolio State Inputs:

From_Portfolio/[date]_to-Compliance_daily-summary.md
Decision Trail Inputs:

ALL messages in Messages_Between_Departments/ (Compliance reads everything for audit trail)
Regulatory Data Inputs:

Alpaca API: Account restrictions, day trade count, pattern day trader status
FINRA rules database: Updated regulations (for future real money compliance)
Outputs
Daily Outputs:

Daily Compliance Report (5:00 PM daily, after market close)
File: From_Compliance/[date]_to-WJC_daily-compliance-report.md
Content:
All trades executed today
Any compliance warnings (e.g., approaching day trade limit)
Reconciliation: Trading's logs vs Alpaca's records
Policy violations (if any)
Audit trail completeness check
Format: Structured report with pass/fail checklist
Alert Outputs:

Compliance Warning (immediate, when threshold approached)

File: From_Compliance/[timestamp]_to-Executive_WARNING-[ISSUE].md
Examples:
2 day trades used (out of 3 allowed in 5 days)
Approaching pattern day trader designation
Settlement violation risk (selling stock before purchase settled)
Unusual trading pattern (e.g., 10 trades in 1 hour)
Compliance Violation Alert (immediate, when violation detected)

File: From_Compliance/[timestamp]_to-WJC_VIOLATION-[ISSUE].md
Also CC: From_Compliance/[timestamp]_to-Executive_VIOLATION-[ISSUE].md
Examples:
Pattern day trader rule violated
Trade executed without proper approval trail
Position exceeded allowed concentration
Any discrepancy between logs and actual trades
Archive Outputs:

Weekly Audit Trail Archive (Sunday midnight)
File: From_Compliance/[week]_audit-trail-archive.md
Content: All messages from past week, indexed and cross-referenced
Format: Markdown with hyperlinks to all original messages
Purpose: Easy review of decision history
On-Demand Outputs:

Audit Response (when WJC requests specific audit)
File: From_Compliance/[timestamp]_to-WJC_audit-response-[TOPIC].md
Content: Complete trail for specific trade, decision, or time period
Examples:
"Show me all decisions related to AAPL position"
"Why did we exit MSFT on Oct 25?"
"What was Risk's assessment before TSLA trade?"
Tools/APIs
Audit Trail Tools:

File system scanner: Reads all messages in Messages_Between_Departments/
Message parser: Extracts metadata (from, to, timestamp, type)
Cross-reference engine: Links related messages (proposal ? assessment ? approval ? execution)
Compliance Rule Engine:

Pattern day trader detector
Settlement violation checker
Position limit validator
Trading_Wisdom.txt compliance cross-check (compared to Risk's assessments)
Alpaca API (Compliance Checks):

/v2/account (day trade count, restrictions, flags)
/v2/account/activities (all account activity for reconciliation)
Database Access:

Read/Write: sentinel.db tables:
compliance_logs (all compliance events)
audit_trails (indexed message archive)
violations (any policy violations)
reconciliations (daily reconciliation results)
Decision Authority
Autonomous Decisions:

? Which compliance rules to check
? When to issue warnings (before violations occur)
? How to format compliance reports
? Archive retention policy (how long to keep logs)
Requires Escalation to Executive:

?? Approaching compliance limits (e.g., 2 day trades used)
?? Reconciliation discrepancies (logs don't match Alpaca)
?? Unusual activity patterns (may indicate bug or issue)
Requires WJC Alert:

? Actual violations (not warnings)
? Audit trail gaps (missing messages in decision chain)
? Regulatory changes affecting Sentinel (for future real money trading)
Cannot Do (No Authority):

? Block trades (only Trading Department can reject based on hard constraints)
? Override decisions (Compliance observes and reports, doesn't decide)
? Modify logs (audit trail is immutable)
Failure Modes
Failure Mode 1: Missing Message in Decision Chain

Detection: Trade executed, but no Risk assessment found in messages
Impact: Incomplete audit trail
Recovery:
Flag as VIOLATION: "Trade executed without documented risk assessment"
Escalate to WJC immediately
Investigate: Was assessment lost, or was process bypassed?
Require manual justification from WJC for this trade
Implement check to prevent future occurrence
Failure Mode 2: Reconciliation Failure (Logs ? Alpaca)

Detection: Trading Department logged 5 fills, Alpaca shows 4 fills
Impact: Cannot verify all trades
Recovery:
HALT trading until reconciled
Escalate to Executive and CC
Manual investigation: Which fill is missing or extra?
Likely causes:
Trading Department missed logging a fill
Alpaca had delay in reporting fill
Duplicate order (one got cancelled)
Resolve discrepancy before resuming trading
Update logs to match Alpaca (Alpaca is source of truth)
Failure Mode 3: Compliance Warning Ignored

Detection: Compliance issued "2 day trades used" warning, Executive approved 3rd day trade anyway
Impact: Pattern day trader rule violated
Recovery:
Flag as VIOLATION: "Day trade limit exceeded"
Escalate to WJC: "Account now restricted by pattern day trader rule"
Document: Was this intentional or oversight?
If intentional: WJC accepts consequences (Alpaca may restrict account)
If oversight: Implement stronger warning system (require explicit override acknowledgment)
Failure Mode 4: Audit Trail Archive Corruption

Detection: Weekly archive file corrupted or missing
Impact: Cannot retrieve historical decision trail
Recovery:
Attempt recovery from git history (all messages in Messages_Between_Departments/ are git-tracked)
Reconstruct archive from individual message files
If unrecoverable: Document gap in audit trail
Escalate to CC: "Data integrity issue"
Implement backup strategy (multiple archive locations)
Failure Mode 5: New Regulation Not Implemented

Detection: FINRA/SEC announces new rule affecting trading
Impact: Sentinel may unknowingly violate new rule
Recovery:
Compliance monitors regulatory news (manual for Phase 1)
Escalate to WJC: "New regulation requires review"
WJC/C(P) update Trading_Wisdom.txt to incorporate new rule
Compliance updates rule engine to check new constraint
If retroactive violation: Report to WJC, assess if Alpaca account affected
Success Metrics
Audit Trail Completeness:

? 100% of trades have complete decision trail (proposal ? assessment ? approval ? execution ? log)
? Zero gaps in message archive (all messages indexed and retrievable)
? Daily reconciliation: 100% match between logs and Alpaca records
Compliance Accuracy:

? Zero false positives (warnings about non-existent violations)
? Zero missed violations (if violation occurs, Compliance catches it)
? Warnings issued before violations (proactive, not reactive)
Timeliness:

? Daily compliance report delivered by 5:00 PM (100% on-time)
? Violations escalated within 5 minutes of detection
? Audit responses to WJC within 1 hour
Usefulness:

? WJC can reconstruct any decision from audit trail
? Compliance reports actionable (clear what to do about warnings)
? No violations slip through to Alpaca enforcement (Compliance catches first)
Integrity:

? Audit trail immutable (no message modifications after creation)
? All timestamps accurate (UTC, no timezone issues)
? Archive backups successful (weekly backup to external location)
v6.2 Component Mapping
Components to Migrate from v6.2 ? Compliance Department:

Trade logging (currently in trading_executor.py) ? Compliance Department

Current function: Logs each trade to file
New role: Comprehensive audit trail with cross-references
Refactoring needed: More structured, indexed, queryable
Position reconciliation (currently ad-hoc manual process) ? Compliance Department

Current function: Occasionally check if positions match Alpaca
New role: Daily automated reconciliation with alerts
Refactoring needed: Build from scratch (no existing code)
Components to BUILD NEW for Compliance Department:

Message archive indexer

Scans all messages in Messages_Between_Departments/
Builds index: audit_index.json with links between related messages
Allows queries like "show all messages about AAPL" or "show decision chain for order #12345"
Compliance rule engine

python

Run

class ComplianceRuleEngine:
    def check_day_trade_limit(account_activity):
        """Returns (is_compliant, day_trade_count, warning_message)"""
    
    def check_settlement_violation(trade, account_history):
        """Returns (is_compliant, violation_type, explanation)"""
    
    def check_position_limits(position, portfolio):
        """Returns (is_compliant, limit_type, current_vs_max)"""
Reconciliation module

Compares Trading Department logs to Alpaca /v2/account/activities
Identifies discrepancies
Suggests resolutions
Compliance database schema

sql

CREATE TABLE compliance_logs (
    id INTEGER PRIMARY KEY,
    log_timestamp TIMESTAMP NOT NULL,
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    resolution TEXT
);

CREATE TABLE audit_trails (
    id INTEGER PRIMARY KEY,
    trade_id TEXT NOT NULL,
    decision_chain JSON NOT NULL,
    all_messages JSON NOT NULL,
    audit_complete BOOLEAN NOT NULL
);

CREATE TABLE violations (
    id INTEGER PRIMARY KEY,
    violation_timestamp TIMESTAMP NOT NULL,
    violation_type TEXT NOT NULL,
    description TEXT NOT NULL,
    responsible_dept TEXT,
    resolution TEXT,
    resolved_timestamp TIMESTAMP
);

CREATE TABLE reconciliations (
    id INTEGER PRIMARY KEY,
    reconciliation_date DATE NOT NULL,
    sentinel_trade_count INTEGER NOT NULL,
    alpaca_trade_count INTEGER NOT NULL,
    discrepancies JSON,
    reconciliation_status TEXT NOT NULL
);
Effort Estimate for Compliance Department:

Migration of trade logging: 4-6 hours
Message archive indexer: 8-12 hours
Compliance rule engine: 10-14 hours
Reconciliation module: 8-12 hours
Audit trail cross-referencer: 6-8 hours
Database schema + integration: 6-8 hours
Testing & validation: 10-14 hours
Total: 52-74 hours
DEPARTMENT 6: EXECUTIVE DEPARTMENT
Role & Responsibilities
The Executive Department is Sentinel Corporation's coordination and decision-making center. It orchestrates the workflow between departments, makes final approvals on trades, handles escalations, and interfaces directly with WJC.

Primary Responsibilities:

Coordinate daily workflow (trigger departments in correct sequence)
Review and approve/reject trade proposals
Handle escalations from all departments
Make strategic decisions when departments disagree
Interface with WJC (escalate critical decisions, receive directives)
Monitor overall system health
Adapt to changing market conditions (shift risk tolerance, pause trading, etc.)
NOT Responsible For:

Detailed research (that's Research Department's job)
Risk calculations (that's Risk Management's job)
Position sizing (that's Portfolio Management's job)
Trade execution (that's Trading Department's job)
Audit logging (that's Compliance Department's job)
Philosophy: Executive is the strategic coordinator. It sees the big picture, makes high-level decisions, and ensures all departments work together harmoniously toward Sentinel's goals.

Inputs
Daily Workflow Inputs:

Time triggers (9:00 AM: start daily process, 4:00 PM: end of day review)
Market condition inputs from Research Department
Risk status from Risk Management Department
Trade proposals from Portfolio Department
Escalation Inputs:

From_Risk/[timestamp]_to-Executive_WARNING-[ISSUE].md (risk concerns)
From_Trading/[timestamp]_to-Executive_REJECTED-[TICKER].md (execution issues)
From_Portfolio/[timestamp]_to-Executive_ALERT-[ISSUE].md (portfolio issues)
From_Compliance/[timestamp]_to-Executive_WARNING-[ISSUE].md (compliance concerns)
From_Research/[timestamp]_to-Executive_ALERT-[TOPIC].md (breaking news)
Trade Approval Inputs:

From_Risk/[timestamp]_to-Executive_assessment-[TICKER].md (Risk's verdict on proposed trade)
From_Portfolio/[timestamp]_to-Executive_trade-proposal-[TICKER].md (Portfolio's request)
WJC Directive Inputs:

From_WJC/[timestamp]_to-Executive_directive-[ACTION].md
Examples:
"Pause all trading until I review"
"Shift to defensive positioning"
"Close all positions in Tech sector"
"Override Risk's rejection of AAPL trade"
Outputs
Daily Coordination Outputs:

Daily Briefing Request (9:00 AM daily)

File: From_Executive/[date]_to-Research_daily-briefing-request.md
Content: Request for market briefing and candidate tickers
Triggers Research Department's daily workflow
End of Day Summary (5:00 PM daily)

File: From_Executive/[date]_to-WJC_end-of-day-summary.md
Content:
What happened today (trades, market moves, issues)
Current portfolio state
Risk status
Compliance status
Plan for tomorrow
Format: Executive summary (1-2 pages, high-level overview)
Trade Approval Outputs:

Trade Approved (after reviewing Risk assessment)

File: From_Executive/[timestamp]_to-Portfolio_trade-APPROVED-[TICKER].md
Content: Authorization to proceed, any conditions (e.g., "reduce size by 25%")
Next step: Portfolio sends order to Trading Department
Trade Rejected (if risk too high or other concerns)

File: From_Executive/[timestamp]_to-Portfolio_trade-REJECTED-[TICKER].md
Content: Reason for rejection, what would need to change for approval
Portfolio must revise proposal or abandon trade
WJC Escalation Outputs:

Approval Request (when Executive needs WJC input)

File: From_Executive/[timestamp]_to-WJC_approval-request-[ISSUE].md
Examples:
Risk score =9 (critical risk trade)
Departments disagree (Risk says no, Portfolio insists)
Unusual market event (VIX spike, circuit breaker)
Compliance violation occurred (need WJC decision on response)
Status Report (on-demand when WJC requests)

File: From_Executive/[timestamp]_to-WJC_status-report-[TOPIC].md
Content: Current state of whatever WJC asked about
Examples:
"What's our current Tech exposure?"
"Why did we sell MSFT?"
"Are we ready for Phase 2 (paper trading)?"
Department Directive Outputs:

Directive to Department (when Executive needs to adjust operations)
File: From_Executive/[timestamp]_to-[Dept]_directive-[ACTION].md
Examples:
To Research: "Focus on defensive sectors today"
To Risk: "Temporarily lower heat threshold to 6%"
To Portfolio: "Raise cash to 30%"
To Trading: "Halt all trading until further notice"
Tools/APIs
Coordination Tools:

Workflow scheduler: Manages daily triggers (9:00 AM start, 4:00 PM EOD, etc.)
Message queue monitor: Tracks which departments have pending responses
Escalation prioritizer: Sorts incoming alerts by severity
Decision Support:

Risk/reward calculator: Weighs Risk's assessment against Portfolio's conviction
Market condition interpreter: Translates Research's briefing into action items
Conflict resolver: Framework for deciding when departments disagree
Communication:

Message templates: Pre-formatted messages for common coordination tasks
WJC interface: Special message format for human escalations
Database Access:

Read: All tables (Executive has visibility into entire system)
Write: sentinel.db tables:
executive_decisions (all approvals/rejections with rationale)
system_directives (strategic decisions affecting operations)
wjc_escalations (all requests to WJC with responses)
Decision Authority
Autonomous Decisions:

? Approve trades with Risk score =5 (low risk)
? Coordinate daily workflow (when to trigger each department)
? Prioritize among multiple trade proposals (if limited capital)
? Adjust position sizes within Risk's approved range
? Request additional analysis from Research or Risk
Requires Internal Review (Executive thinks harder):

?? Trades with Risk score 6-7 (moderate risk)
Executive must document why benefits outweigh risks
?? Trades violating soft constraints in Trading_Wisdom.txt
Executive must justify deviation from doctrine
?? Conflicting recommendations from departments
Executive must decide which to follow, document rationale
Requires WJC Approval:

? Trades with Risk score =8 (high risk)
? Trades with Risk score =9 (critical risk)
? Hard constraint overrides (violating coded limits)
? Strategic shifts (changing allocation strategy, raising cash >30%, etc.)
? Doctrine changes (modifying Trading_Wisdom.txt)
? Compliance violations (how to respond)
Cannot Do (No Authority):

? Override hard constraints without WJC approval (coded limits are absolute)
? Execute trades directly (must go through Trading Department)
? Modify other departments' logic (can only request, not command)
Failure Modes
Failure Mode 1: Department Not Responding

Detection: Research hasn't delivered market briefing by 10:30 AM (30 min late)
Impact: Workflow stalled
Recovery:
Send reminder to department: "Still waiting for [output], please respond"
If no response after 1 hour, escalate to WJC: "Research Department unresponsive"
WJC must manually intervene (check if Research is stuck or if there's a bug)
Possible workaround: Use yesterday's market briefing as fallback (stale but better than nothing)
Failure Mode 2: Conflicting Recommendations

Detection: Risk says "REJECT trade", Portfolio insists "We must do this trade"
Impact: Executive must arbitrate
Recovery:
Request additional information from both:
To Risk: "What would reduce risk enough to approve?"
To Portfolio: "What's the opportunity cost of not doing this trade?"
If still conflicting, escalate to WJC with both perspectives
WJC makes final call
Document: This was escalated conflict, not routine decision
Failure Mode 3: WJC Directive Contradicts Doctrine

Detection: WJC says "Buy 1000 shares of TSLA", but this violates 15% position limit
Impact: Conflict between human authority and Trading_Wisdom.txt
Recovery:
Clarify with WJC: "This would violate [specific rule in Trading_Wisdom.txt], confirm override?"
If WJC confirms: Document exception, proceed with trade
If WJC reconsiders: Adjust directive to comply with doctrine
Important: WJC always has override authority, but must be explicit about exceptions
Failure Mode 4: Multiple Simultaneous Escalations

Detection: Risk, Trading, and Compliance all escalate issues within 5 minutes
Impact: Executive overwhelmed, cannot process all simultaneously
Recovery:
Triage by severity:
CRITICAL (system-breaking): Handle immediately
WARNING (need attention): Queue for processing
INFO (nice to know): Defer until CRITICAL/WARNING resolved
If truly cannot handle: Escalate to WJC: "Multiple urgent issues, need human prioritization"
Process one at a time, document resolution order
Failure Mode 5: Market Condition Change Mid-Day

Detection: Research issues ALERT: "VIX spiked 30%, market down 3%"
Impact: Morning's trade approvals may no longer be appropriate
Recovery:
Immediately pause pending orders (if not yet executed by Trading)
Request emergency risk re-assessment from Risk Department
Evaluate: Should we:
Cancel pending trades?
Reduce position sizes?
Go defensive (raise cash)?
Escalate to WJC if situation extreme (>5% market drop)
Document: Market condition changed, prior approvals invalidated
Failure Mode 6: Executive Makes Wrong Decision (In Hindsight)

Detection: Executive approved trade, it lost money (or rejected trade, it would have won)
Impact: Confidence in Executive's judgment questioned
Recovery:
NOT a failure mode - investing involves uncertainty
Document: What information was available at decision time?
Was decision process sound, even if outcome bad?
Learn: Would different framework have led to better decision?
Track: Decision quality metrics (separate process quality from outcome luck)
Important: Good process + bad outcome ? bad decision
Only if pattern of bad decisions, escalate to C(P)/WJC for framework review
Success Metrics
Coordination Efficiency:

? Daily workflow completes on schedule (market briefing ? risk assessment ? trade approvals ? execution all by 11:00 AM)
? Zero department bottlenecks (no department waiting >1 hour for another)
? All escalations resolved (nothing left in "pending" state at EOD)
Decision Quality:

? Approved trades align with Trading_Wisdom.txt (>90% compliance with soft constraints)
? Escalations to WJC are legitimate (WJC agrees Executive couldn't decide alone >80% of time)
? Rejected trades later prove to have been bad ideas (validation of Executive's judgment)
Risk Management:

? Zero hard constraint violations approved (100% enforcement of coded limits)
? High-risk trades (score =8) escalated to WJC (100% escalation rate)
? Portfolio heat stays within limits (thanks to Executive's oversight)
Communication:

? End of day summary delivered by 5:00 PM (100% on-time)
? WJC escalations include all necessary context (WJC can decide without requesting more info)
? Department directives clear and actionable (departments understand what to do)
Adaptability:

? Executive adjusts to changing market conditions (shifts defensive when appropriate)
? Workflow continues despite department failures (graceful degradation)
? Learns from mistakes (pattern recognition improves over time)
v6.2 Component Mapping
Components to Migrate from v6.2 ? Executive Department:

Workflow orchestration (currently in sentinel_morning_workflow.py) ? Executive Department

Current function: Runs the daily trading process
New role: Coordinates all six departments
Refactoring needed: Much more sophisticated - now coordinating distributed system, not monolithic script
Final trade decision (currently implicit in workflow) ? Executive Department

Current function: Workflow executes trades if conditions met
New role: Explicit approval/rejection with documented rationale
Refactoring needed: Build approval framework (risk/reward balancing)
Error handling (currently scattered throughout v6.2) ? Executive Department

Current function: Try/catch blocks, retry logic
New role: Centralized error escalation and recovery
Refactoring needed: Systematic escalation framework
Components to BUILD NEW for Executive Department:

Department coordination engine

Tracks department states (idle, working, waiting, failed)
Manages message flows (who's waiting for whom)
Detects bottlenecks and stalls
Trade approval framework

python

Run

def approve_trade(portfolio_proposal, risk_assessment, market_conditions):
    """
    Returns (APPROVED|REJECTED|ESCALATE_TO_WJC, rationale)
    
    Logic:
    - If risk_score <= 5: APPROVED (routine)
    - If 6 <= risk_score <= 7: Review benefits vs risks, document decision
    - If risk_score >= 8: ESCALATE_TO_WJC (too risky for autonomous approval)
    - If hard_constraint_violated: REJECTED (or ESCALATE if WJC override needed)
    - If departments_disagree: ESCALATE_TO_WJC
    """
WJC escalation formatter

Takes complex situation
Produces clear, concise summary for WJC
Includes: What decision is needed, what options exist, what Executive recommends, why
Market condition adapter

Interprets Research's market briefing
Adjusts decision-making (more conservative when VIX high, etc.)
Implements adaptive risk tolerance
Executive database schema

sql

CREATE TABLE executive_decisions (
    id INTEGER PRIMARY KEY,
    decision_timestamp TIMESTAMP NOT NULL,
    decision_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    risk_score REAL,
    outcome TEXT
);

CREATE TABLE system_directives (
    id INTEGER PRIMARY KEY,
    directive_timestamp TIMESTAMP NOT NULL,
    target_department TEXT NOT NULL,
    directive TEXT NOT NULL,
    reason TEXT NOT NULL,
    expires_at TIMESTAMP
);

CREATE TABLE wjc_escalations (
    id INTEGER PRIMARY KEY,
    escalation_timestamp TIMESTAMP NOT NULL,
    issue TEXT NOT NULL,
    executive_recommendation TEXT,
    wjc_response TEXT,
    response_timestamp TIMESTAMP
);
Effort Estimate for Executive Department:

Migration of workflow orchestration: 12-16 hours (complex refactoring)
Department coordination engine: 10-14 hours
Trade approval framework: 8-12 hours
WJC escalation formatter: 6-8 hours
Market condition adapter: 6-8 hours
Error handling & recovery: 8-12 hours
Database schema + integration: 6-8 hours
Testing & validation: 14-18 hours (most complex department)
Total: 70-96 hours
APPENDIX A: MESSAGE FLOW DIAGRAMS
Daily Workflow - Normal Market Day
mipsasm

9:00 AM - Executive triggers daily workflow
   ?
   Executive ? Research: "Provide daily market briefing"
   ?
10:00 AM - Research delivers briefing
   ?
   Research ? Risk: market-briefing.md
   Research ? Portfolio: market-briefing.md
   Research ? Portfolio: candidate-tickers.md
   ?
10:15 AM - Portfolio evaluates candidates
   ?
   Portfolio ? Risk: "Assess trade proposal for AAPL (BUY 50 shares)"
   ?
10:20 AM - Risk assesses proposal
   ?
   Risk ? Portfolio: risk-assessment-AAPL.md (Risk Score: 6, CONDITIONAL APPROVAL)
   Risk ? Executive: risk-assessment-AAPL.md (CC for awareness)
   ?
10:25 AM - Executive reviews and approves
   ?
   Executive ? Portfolio: "Trade APPROVED (reduce to 40 shares per Risk's recommendation)"
   ?
10:30 AM - Portfolio sends order to Trading
   ?
   Portfolio ? Trading: order-AAPL.md (BUY 40 shares, executive_approval: true)
   ?
10:31 AM - Trading validates and executes
   ?
   Trading ? Alpaca API: Submit order
   Alpaca ? Trading: Order confirmed, ID #12345
   ?
   Trading ? Portfolio: order-submitted-AAPL.md
   Trading ? Compliance: order-submitted-AAPL.md
   ?
10:32 AM - Order fills
   ?
   Alpaca ? Trading: Fill notification (40 shares @ $178.50)
   ?
   Trading ? Portfolio: order-filled-AAPL.md
   Trading ? Compliance: order-filled-AAPL.md
   ?
[Repeat for other tickers throughout day]
   ?
4:00 PM - Market close, end of day reporting
   ?
   Portfolio ? Risk: current-positions.md
   Portfolio ? Executive: daily-summary.md
   Portfolio ? Compliance: daily-summary.md
   ?
4:30 PM - Risk produces daily risk report
   ?
   Risk ? Executive: daily-risk-report.md
   ?
   Trading ? Compliance: daily-execution-log.md
   ?
5:00 PM - Compliance produces daily compliance report
   ?
   Compliance ? WJC: daily-compliance-report.md
   ?
   Executive ? WJC: end-of-day-summary.md
   ?
END OF DAY
Escalation Workflow - High Risk Trade
sql_more

Portfolio proposes trade with potential risk issues
   ?
   Portfolio ? Risk: trade-proposal-TSLA.md (BUY 100 shares)
   ?
Risk analyzes, identifies concerns
   ?
   Risk ? Portfolio: risk-assessment-TSLA.md (Risk Score: 8, WARNING: High volatility)
   Risk ? Executive: risk-assessment-TSLA.md (CC for escalation)
   ?
Executive sees Risk Score =8, must escalate to WJC
   ?
   Executive ? WJC: approval-request-TSLA.md
   
   Contents:
   - Portfolio wants to buy 100 shares TSLA (~$25K position)
   - Risk score: 8 (high risk due to volatility)
   - Concerns: TSLA daily volatility 3.5%, single position would be 12% of portfolio
   - Opportunities: Strong momentum, positive sentiment
   - Executive recommendation: Approve with reduced size (50 shares)
   ?
WJC reviews, makes decision
   ?
   WJC ? Executive: directive-TSLA-approval.md
   
   Contents: "Approved at 50 shares. I accept elevated risk given momentum."
   ?
Executive authorizes Portfolio
   ?
   Executive ? Portfolio: trade-APPROVED-TSLA.md (50 shares, per WJC)
   ?
[Normal execution workflow continues with Trading Department]
Exception Workflow - Order Rejection
ebnf

Trading Department receives order
   ?
   Trading: Validates hard constraints
   ?
   ERROR: Insufficient buying power ($10K needed, $8K available)
   ?
Trading rejects order, escalates
   ?
   Trading ? Executive: order-REJECTED-NVDA.md (Reason: Insufficient buying power)
   Trading ? Compliance: order-rejected-NVDA.md (For audit trail)
   ?
Executive investigates
   ?
   Executive ? Portfolio: "NVDA order rejected, only $8K available. Adjust?"
   ?
Portfolio recalculates
   ?
   Portfolio ? Risk: "Re-assess NVDA with reduced size (20 shares instead of 30)"
   ?
Risk re-assesses
   ?
   Risk ? Portfolio: risk-assessment-NVDA-revised.md (Risk Score: 5, APPROVED)
   Risk ? Executive: risk-assessment-NVDA-revised.md
   ?
Executive approves revised proposal
   ?
   Executive ? Portfolio: trade-APPROVED-NVDA-revised.md
   ?
   Portfolio ? Trading: order-NVDA-revised.md (BUY 20 shares)
   ?
[Trading executes successfully this time]
APPENDIX B: DECISION ESCALATION MATRIX
Situation	Research	Risk	Trading	Portfolio	Compliance	Executive	WJC
Daily market briefing	Decides	-	-	-	-	Requests	-
Ticker to research	Decides	-	-	Requests	-	-	-
Risk score 0-5	-	Decides	-	-	-	Approves	-
Risk score 6-7	-	Decides	-	-	-	Approves + Documents	-
Risk score 8-9	-	Decides	-	-	-	Escalates	Approves
Risk score 10	-	Decides	-	-	-	Escalates	Approves
Position size	-	Validates	-	Decides	-	-	-
Order type (market/limit)	-	-	-	Decides	-	-	-
Execute order	-	-	Decides	-	-	-	-
Hard constraint violation	-	-	Blocks	-	-	-	Can override
Soft constraint violation	-	Warns	-	-	-	Decides	-
Partial fill	-	-	Escalates	-	-	Decides	-
Reconciliation discrepancy	-	-	-	-	Escalates	Escalates	Resolves
Compliance violation	-	-	-	-	Escalates	Escalates	Resolves
Market crash (>5% drop)	Alerts	Alerts	-	Alerts	-	Escalates	Decides
Trading halt request	-	-	-	-	-	Decides	Can override
Change Trading_Wisdom.txt	-	-	-	-	-	-	Decides
Allocation strategy change	-	-	-	Recommends	-	Escalates	Approves
Department disagreement	-	-	-	-	-	Arbitrates or Escalates	Resolves
Legend:

Decides: Department has autonomous authority
Approves: Department reviews and authorizes
Escalates: Department passes to higher authority
Validates: Department checks compliance
Recommends: Department provides input
Blocks: Department prevents action
Alerts: Department notifies others
Requests: Department asks for service
Resolves: Final decision maker
APPENDIX C: PHASE 1 VALIDATION CRITERIA
Before Paper Trading Can Begin
All three parties (WJC, C(P), CC) must agree that ALL criteria below are met:

Department-Level Validation
Research Department:

 Can retrieve market data from yfinance, Alpaca, Alpha Vantage
 Perplexity API integration works (news/sentiment analysis)
 Daily market briefing delivered on-time for 5 consecutive days
 Ad-hoc ticker analysis responds within SLA (<1 hour)
 Database logging works (historical analyses retrievable)
 Failure recovery tested (API outage gracefully handled)
Risk Management Department:

 Trading_Wisdom.txt parser correctly identifies all rules
 Heat calculation matches manual verification
 CVaR calculation produces reasonable results
 Hard constraints correctly enforced (test cases pass)
 Risk scores correlate with actual volatility
 Assessments delivered within SLA (<30 minutes)
 Escalation thresholds work (score =8 escalates to Executive)
Trading Department:

 Alpaca API connection established (paper trading endpoint)
 Hard constraint validation blocks violating orders
 Market orders submit successfully
 Limit orders submit successfully
 Order status tracking works (pending ? filled)
 Partial fill handling tested
 Rejection handling tested (insufficient buying power, etc.)
 Duplicate order detection works
 Execution logs complete and accurate
Portfolio Management Department:

 Can read Alpaca positions accurately
 Position reconciliation works (database matches Alpaca)
 Trade proposals formatted correctly
 Allocation logic produces reasonable sizes
 P&L tracking matches Alpaca's calculations
 Daily summary delivered on-time for 5 consecutive days
 Handles edge cases (zero positions, all cash, etc.)
Compliance Department:

 Message archive indexer works (all messages indexed)
 Audit trail completeness verified (can trace any decision)
 Reconciliation module works (logs match Alpaca)
 Pattern day trader detection works
 Daily compliance report delivered on-time for 5 consecutive days
 Violation alerts trigger correctly (test cases pass)
Executive Department:

 Daily workflow coordination works (triggers departments in sequence)
 Trade approval logic works (correct escalations)
 WJC escalation messages formatted clearly
 End of day summary delivered on-time for 5 consecutive days
 Handles department failures gracefully
 Conflict resolution tested (departments disagree)
Integration Testing
Inter-Departmental Communication:

 Research ? Risk message flow works
 Risk ? Portfolio message flow works
 Portfolio ? Trading message flow works
 Trading ? Compliance message flow works
 All ? Executive message flow works
 Executive ? WJC message flow works
 Messages arrive within expected timeframes
 Message format parsing works (YAML frontmatter + markdown)
Complete Workflow Testing:

 Full daily workflow tested 5 times (end-to-end)
 Normal trade workflow tested (proposal ? assessment ? approval ? execution ? log)
 High-risk trade workflow tested (escalation to WJC)
 Trade rejection workflow tested (insufficient buying power)
 Partial fill workflow tested
 Market condition change workflow tested (VIX spike)
 Department failure workflow tested (Research doesn't respond)
Data Integrity:

 All departments write to database successfully
 Database queries work (historical data retrievable)
 No data loss during failures
 Reconciliation between departments (everyone sees same portfolio state)
 Git commits work (all messages version-controlled)
External Integrations:

 Perplexity API: Successful news queries, sentiment analysis
 yfinance: Successful price data retrieval
 Alpha Vantage: Successful fundamental data retrieval
 Alpaca Market Data API: Successful real-time quotes
 Alpaca Trading API: Successful order submission/cancellation (paper trading)
 All APIs handle failures gracefully (timeouts, rate limits, etc.)
Human Interfaces:

 WJC can read all messages (markdown formatting clear)
 WJC can respond to escalations (directive format works)
 WJC can trigger workflows manually (if needed)
 WJC can inspect database (queries documented)
 C(P) ? Sentinel communication tested (strategic guidance flows)
 CC ? Sentinel communication tested (technical issues reported/resolved)
Performance & Reliability
Timeliness:

 Daily workflow completes by 11:00 AM (95% of time)
 All SLAs met for 5 consecutive days:
Research: Market briefing by 10:00 AM
Risk: Trade assessment <30 minutes
Trading: Order submission <10 seconds
Portfolio: Daily summary by 4:00 PM
Compliance: Daily report by 5:00 PM
Executive: EOD summary by 5:00 PM
Reliability:

 Zero unhandled exceptions in any department for 5 consecutive days
 All failure modes have documented recovery procedures
 System continues operating despite single department failure
 Database backups working (daily backups to external location)
 Git history complete (can rollback to any previous state)
Accuracy:

 Zero math errors (heat, CVaR, P&L all manually verified)
 Zero rule interpretation errors (Trading_Wisdom.txt correctly applied)
 Zero data mismatches (all departments see consistent portfolio state)
Final Approval Checklist
CC (Claude Code) Certification:

 All code reviewed and tested
 No known bugs
 All failure modes handled
 Performance acceptable
 Database schema finalized
 API integrations robust
 Ready for paper trading: YES / NO
C(P) (Claude PoE) Certification:

 All departments fulfill intended roles
 Trading_Wisdom.txt correctly implemented
 Decision escalation matrix works as designed
 Message flows align with architecture
 Risk management philosophy sound
 Ready for paper trading: YES / NO
WJC (William J. Cornelius) Certification:

 Understand how every department works
 Trust the decision-making processes
 Comfortable with risk management
 Escalation workflows clear
 Confident in system's judgment
 Ready to entrust capital (paper money) to Sentinel: YES / NO
If all three certify YES, Phase 2 (Paper Trading) begins.

If any certify NO, continue testing and refinement until concerns addressed.

APPENDIX D: DATABASE SCHEMA SUMMARY
All tables in sentinel.db:

Research Department Tables
sql

CREATE TABLE research_analyses (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    analysis_date DATE NOT NULL,
    fundamentals JSON,
    technicals JSON,
    sentiment_score REAL,
    news_summary TEXT,
    analyst_rating TEXT,
    full_report_path TEXT
);

CREATE TABLE market_briefings (
    id INTEGER PRIMARY KEY,
    briefing_date DATE NOT NULL,
    market_condition TEXT,
    vix_level REAL,
    sector_performance JSON,
    major_news TEXT,
    full_briefing_path TEXT
);
Risk Management Tables
sql

CREATE TABLE risk_assessments (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    assessment_date TIMESTAMP NOT NULL,
    risk_score REAL NOT NULL,
    recommendation TEXT NOT NULL,
    trading_wisdom_compliance JSON,
    metrics JSON,
    full_assessment_path TEXT
);

CREATE TABLE daily_risk_reports (
    id INTEGER PRIMARY KEY,
    report_date DATE NOT NULL,
    portfolio_heat REAL,
    cvar REAL,
    concentration JSON,
    warnings TEXT,
    full_report_path TEXT
);

CREATE TABLE risk_warnings (
    id INTEGER PRIMARY KEY,
    warning_timestamp TIMESTAMP NOT NULL,
    severity TEXT NOT NULL,
    issue TEXT NOT NULL,
    threshold_value REAL,
    current_value REAL,
    resolution TEXT
);
Trading Department Tables
sql

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    alpaca_order_id TEXT UNIQUE NOT NULL,
    ticker TEXT NOT NULL,
    action TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    order_type TEXT NOT NULL,
    limit_price REAL,
    submitted_timestamp TIMESTAMP NOT NULL,
    executive_approval_path TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE fills (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    fill_price REAL NOT NULL,
    quantity_filled INTEGER NOT NULL,
    commission REAL,
    fill_timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE rejections (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    rejection_reason TEXT NOT NULL,
    rejection_timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
Portfolio Management Tables
sql

CREATE TABLE portfolio_snapshots (
    id INTEGER PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    total_value REAL NOT NULL,
    cash_balance REAL NOT NULL,
    positions JSON NOT NULL,
    sector_allocation JSON,
    daily_pnl REAL
);

CREATE TABLE position_history (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    entry_date DATE NOT NULL,
    entry_price REAL NOT NULL,
    entry_quantity INTEGER NOT NULL,
    exit_date DATE,
    exit_price REAL,
    exit_quantity INTEGER,
    realized_pnl REAL
);

CREATE TABLE pnl_tracking (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    realized_pnl REAL NOT NULL,
    unrealized_pnl REAL NOT NULL,
    total_pnl REAL NOT NULL,
    cumulative_pnl REAL NOT NULL
);
Compliance Department Tables
sql

CREATE TABLE compliance_logs (
    id INTEGER PRIMARY KEY,
    log_timestamp TIMESTAMP NOT NULL,
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    resolution TEXT
);

CREATE TABLE audit_trails (
    id INTEGER PRIMARY KEY,
    trade_id TEXT NOT NULL,
    decision_chain JSON NOT NULL,
    all_messages JSON NOT NULL,
    audit_complete BOOLEAN NOT NULL
);

CREATE TABLE violations (
    id INTEGER PRIMARY KEY,
    violation_timestamp TIMESTAMP NOT NULL,
    violation_type TEXT NOT NULL,
    description TEXT NOT NULL,
    responsible_dept TEXT,
    resolution TEXT,
    resolved_timestamp TIMESTAMP
);

CREATE TABLE reconciliations (
    id INTEGER PRIMARY KEY,
    reconciliation_date DATE NOT NULL,
    sentinel_trade_count INTEGER NOT NULL,
    alpaca_trade_count INTEGER NOT NULL,
    discrepancies JSON,
    reconciliation_status TEXT NOT NULL
);
Executive Department Tables
sql

CREATE TABLE executive_decisions (
    id INTEGER PRIMARY KEY,
    decision_timestamp TIMESTAMP NOT NULL,
    decision_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    risk_score REAL,
    outcome TEXT
);

CREATE TABLE system_directives (
    id INTEGER PRIMARY KEY,
    directive_timestamp TIMESTAMP NOT NULL,
    target_department TEXT NOT NULL,
    directive TEXT NOT NULL,
    reason TEXT NOT NULL,
    expires_at TIMESTAMP
);

CREATE TABLE wjc_escalations (
    id INTEGER PRIMARY KEY,
    escalation_timestamp TIMESTAMP NOT NULL,
    issue TEXT NOT NULL,
    executive_recommendation TEXT,
    wjc_response TEXT,
    response_timestamp TIMESTAMP
);
TOTAL EFFORT ESTIMATE SUMMARY
Per Department Implementation Estimates (CC to refine):

Department	Effort (Hours)	Priority
Research	34-50	High (needed first for data)
Risk Management	52-72	High (needed for approvals)
Trading	43-60	High (needed to execute)
Portfolio Management	62-86	High (needed for decisions)
Compliance	52-74	Medium (needed for audit, not blocking)
Executive	70-96	High (needed for coordination)
TOTAL	313-438 hours	
Assumptions:

CC working alone (single developer)
Includes migration of existing v6.2 components
Includes building new components
Includes comprehensive testing
Does NOT include C(P) strategic review time
Does NOT include WJC approval time
Realistic Timeline (CC to adjust):

If working 20 hours/week: 16-22 weeks (4-5.5 months)
If working 40 hours/week: 8-11 weeks (2-2.75 months)
These are serial estimates (one department at a time)
Some parallelization possible, but integration testing is serial
Recommendation:
Build departments in this order (dependencies):

Research (provides data to everyone)
Risk (validates proposals)
Portfolio (makes decisions)
Trading (executes decisions)
Compliance (audits everything)
Executive (coordinates everyone)
After each department, test integration with previously built departments.

NEXT STEPS
This draft is complete.

CC: Please review within 24 hours and provide:

Technical feasibility assessment for each department
Effort estimate refinements (are my hour estimates realistic?)
v6.2 component mapping validation (did I correctly identify what to migrate?)
Implementation complexity rankings (which departments are hardest?)
Any technical concerns or architectural issues
Approval or requested modifications
After CC's review and revisions, we proceed to:

MESSAGE_PROTOCOL_SPECIFICATION.md
PHASE_1_IMPLEMENTATION_PLAN.md
END OF DEPARTMENTAL_SPECIFICATIONS v1.0 DRAFT