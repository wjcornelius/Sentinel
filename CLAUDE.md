# Sentinel Corporation - Claude Context File

> Read this file at the start of every session to understand the project.

## Project Overview

**Sentinel Corporation** is an AI-powered swing trading system for paper trading on Alpaca. It uses a corporate departmental structure where AI agents collaborate to research, analyze, and execute trades.

**Philosophy:** "We are breeding a racehorse, not a pony that gives rides at a carnival."

**Current Status:** Live paper trading with ~$100K portfolio, 15-20 concurrent positions, ATR-based GTC trailing stops (3-15% based on volatility).

---

## Architecture

```
USER (Control Panel: sentinel_control_panel.py)
         ↓
    CEO (ceo.py) - Orchestrator & User Interface
         ↓
    OPERATIONS MANAGER (operations_manager.py) - Workflow Coordination
         ↓
    ┌─────────────┬──────────────┬────────────────┬──────────────┐
    ↓             ↓              ↓                ↓              ↓
 RESEARCH      NEWS         GPT-5/4o        COMPLIANCE      TRADING
 ~50 stocks   Sentiment    Portfolio        Pre-check       Bracket
 Swing-suited Perplexity   Optimization     Position size   Orders
```

### Key Departments

| Department | File | Purpose |
|------------|------|---------|
| CEO | `Departments/Executive/ceo.py` | User interface, approval flow |
| Operations | `Departments/Operations/operations_manager.py` | Workflow coordination |
| Research | `Departments/Research/research_department.py` | Stock screening, ~50 candidates |
| News | `Departments/News/news_department.py` | Perplexity sentiment analysis |
| GPT Optimizer | `Departments/Executive/gpt5_portfolio_optimizer.py` | AI portfolio selection |
| Compliance | `Departments/Compliance/compliance_department.py` | Position limits enforcement |
| Trading | `Departments/Trading/trading_department.py` | ATR-based GTC trailing stop execution |
| Risk | `Departments/Risk/risk_department.py` | Risk scoring (legacy) |
| Portfolio | `Departments/Portfolio/portfolio_department.py` | Position tracking |

### Supporting Components

- `Departments/Operations/mode_manager.py` - Trading session control & safety gates
- `Departments/Operations/realism_simulator.py` - Paper trading realism constraints
- `Departments/Research/market_regime.py` - VIX-based market regime detection
- `Utils/atr_calculator.py` - ATR-based trailing stop percentage calculation
- `Utils/trailing_stop_monitor.py` - Monitor and manage trailing stop protection
- `Utils/fill_recorder.py` - Sync order fills from Alpaca to database

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config.py` | API keys (Alpaca, OpenAI, Perplexity) - NOT in git |
| `Config/hard_constraints.yaml` | Trading rules (position limits, risk gates) |
| `Config/compliance_config.yaml` | Compliance thresholds |
| `ticker_universe.txt` | S&P 500 + Nasdaq 100 stock universe |

### Current Hard Constraints (from hard_constraints.yaml)
- Max single position: 25% of portfolio
- Min position: 2.5% of portfolio
- Max positions: 30 total
- Max sector concentration: 40%
- Min cash reserve: 10%
- Max portfolio heat: 8%
- VIX panic halt: >40

---

## Daily Workflow

1. **Run:** `python sentinel_control_panel.py`
2. **Menu Options:**
   - [1] Request Trading Plan - Runs full pipeline
   - [2] Execute Approved Plan - Submits orders to Alpaca
   - [3] View Plan Status - Current plan details
   - [4] Exit

### Pipeline Stages
1. Research: Screens ~600 stocks → ~50 swing candidates
2. News: Perplexity sentiment analysis (16-hour cache)
3. GPT Optimizer: Selects 15-20 positions, allocates capital
4. Compliance: Enforces position limits
5. Trading: Executes with ATR-based GTC trailing stops

---

## Recent Development History

### December 2025 (Latest)
- **ATR-based GTC trailing stops** - Replaced fixed 8% DAY brackets with volatility-adjusted GTC trailing stops (3-15%)
- **Fill recording** - Order fills now synced from Alpaca to database for tracking
- **Trailing stop monitor** - Utility to check/add protection for all positions
- **SELL constraint fix** - min_position_pct no longer blocks sell orders
- Compliance enforcement (not just advisory)
- Portfolio allocator respects position limits
- Realism simulator for paper trading constraints

### November 2025
- Automated pre-flight checks
- Position monitoring integration
- Database consolidation (single unified DB)
- Mode manager (trading session control)
- Real-time price API fixes
- Universe optimization & dynamic messaging

### October-November 2025
- Major architectural transformation from single main_script.py to departmental structure
- Corporate hierarchy: CEO → Operations Manager → Departments
- Message-based inter-department communication

---

## Project History

Originally started as a simple prototype (v1-v6) with a single `main_script.py`. Transformed in November 2025 to the current departmental architecture. Historical documentation was in `CONVERSATION_INDEX.md` and `DESIGN_LOG.md` (deleted during transformation but recoverable from git commit `def847e`).

**Original Philosophy (still applies):**
- "AI-Maximalist, Code-Minimalist" - AI for strategy, simple code for execution
- 90% capital invested, 10% max per position (later expanded)
- Human-in-the-loop approval before execution
- Local-only operation on monitored machine

---

## Key Files for Understanding the System

1. `sentinel_control_panel.py` - Main entry point
2. `Departments/Executive/ceo.py` - Core orchestration logic
3. `Departments/Operations/operations_manager.py` - Workflow coordination
4. `README.md` - Comprehensive system documentation
5. `Config/hard_constraints.yaml` - Trading rules

---

## Database

SQLite database: `sentinel.db`

Key Tables:
- `trading_orders` - All order submissions with Alpaca IDs
- `trading_fills` - Fill data synced from Alpaca (price, qty, slippage)
- `trading_rejections` - Orders rejected for constraint violations
- `portfolio_positions` - Position tracking with entry/stop/target
- `research_cache` - Stock screening data cache
- `news_sentiment_cache` - Perplexity sentiment data

---

## APIs Used

- **Alpaca** - Paper trading execution, account data
- **OpenAI** - GPT-4o/GPT-5 for portfolio optimization
- **Perplexity** - News sentiment analysis
- **yfinance** - Historical price/volume data

---

## Inter-Claude Communication

The project involves collaboration between:
- **Claude Code** (this instance) - Development, code changes
- **Claude (Poe)** - Strategic guidance, vision documents

Messages between Claudes are stored in:
- `Messages_From_Claude_Poe/` - Directives from Claude Poe
- `Messages_For_Claude_Poe/` - Responses to Claude Poe
- `Messages_Between_Departments/` - Inter-department messages

---

## Notes for Future Sessions

- This file (`CLAUDE.md`) is read automatically at session start
- The conversation history does NOT persist between Claude Code sessions
- If context is lost, this file provides the essential project knowledge
- For deep history, check git log and the deleted docs at commit `def847e`

---

*Last updated: December 19, 2025*
