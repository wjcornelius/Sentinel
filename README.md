# Sentinel Corporation

**AI-Powered Swing Trading System with Intelligent Portfolio Optimization**

> "We are breeding a racehorse, not a pony that gives rides at a carnival."

[![Status](https://img.shields.io/badge/Status-Live%20Paper%20Trading-success)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![License](https://img.shields.io/badge/License-Private-red)]()

---

## 🎯 Overview

Sentinel Corporation is an **AI-powered swing trading system** that executes 1-5 day momentum trades using GPT-5 for portfolio optimization. The system maintains **8-10 positions** with bracket orders (stop-loss + take-profit) for disciplined risk management.

### Current Status (November 3, 2025)

- ✅ **Live Trading**: 8 positions with bracket orders active
- ✅ **GPT-5 Optimization**: Intelligent stock selection and capital allocation
- ✅ **Bracket Orders**: 8% stop-loss, 16% take-profit (2:1 R/R ratio)
- ✅ **Wide Brackets Philosophy**: "Room to run" for volatile swing candidates
- ✅ **Duplicate Prevention**: UUID handling and retry logic fixed
- ✅ **Real-Time Execution**: Orders submitted to Alpaca paper trading

---

## 🏗️ Architecture

### Departmental Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER (Control Panel)                        │
│                   sentinel_control_panel.py                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      CEO (Orchestrator)                          │
│         ceo.py - Workflow Coordination & User Interface          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   OPERATIONS MANAGER                             │
│           operations_manager.py - 3-Stage Workflow               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────┬───────────────┬────────────────┐
        ↓             ↓               ↓                ↓
┌──────────────┐ ┌──────────┐ ┌────────────┐ ┌──────────────┐
│   RESEARCH   │ │   NEWS   │ │   GPT-5    │ │  COMPLIANCE  │
│              │ │          │ │ OPTIMIZER  │ │   ADVISORY   │
│ Stage 1      │ │ Stage 2  │ │  Stage 3   │ │   Stage 4    │
│ ~50 stocks   │ │ Sentiment│ │ 8-10 picks │ │ Pre-check    │
│ Swing-suited │ │ Perplexity│ │ OpenAI    │ │ Position size│
└──────────────┘ └──────────┘ └────────────┘ └──────────────┘
                              ↓
                    ┌─────────────────┐
                    │      CEO        │
                    │   Approval &    │
                    │   Execution     │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │    TRADING      │
                    │   Department    │
                    │ Bracket Orders  │
                    │  to Alpaca API  │
                    └─────────────────┘
```

### Three-Stage Workflow

**Stage 1: Research Department (v3.0)**
- Two-stage filtering: Swing scoring → Technical filters
- Universe: S&P 500 + Nasdaq 100 (~600 stocks)
- Output: ~50 swing-suitable candidates
- Metrics: Technical score, fundamental score, composite score
- Data source: yfinance (60-day lookback)

**Stage 2: News Department**
- Batch sentiment analysis via Perplexity AI
- 16-hour cache for cost optimization
- Output: Sentiment scores (0-100) + news summaries
- Concurrent processing (10 tickers at a time)

**Stage 3: GPT-5 Portfolio Optimizer**
- Analyzes all 50 candidates holistically
- Considers market conditions (VIX, SPY trend)
- Decides which to buy and capital allocation
- Target: 8-10 positions, 90-100% capital deployment
- Output: Executable trading plan with reasoning

**Stage 4: Compliance Advisory**
- Reviews proposed trades for constraint violations
- Flags (but doesn't block) oversized positions
- Max position: 10% of portfolio
- Max sector: 30% of portfolio
- Advisory mode: CEO sees flags but makes final call

---

## 🎲 Trading Philosophy

### Swing Trading Principles

- **Holding Period**: 1-5 days (not day trading, not long-term)
- **Position Count**: 8-10 concurrent positions
- **Capital Deployment**: 90-100% invested
- **Volatility = Opportunity**: We WANT volatile stocks (creates swing moves)
- **Room to Run**: Wide brackets allow normal volatility without stopping out

### Risk Management

**Bracket Orders (Every Position)**
- **Stop-Loss**: 8% below entry
  - Protects against large losses
  - Wide enough for intraday volatility
  - Automated execution (no emotions)

- **Take-Profit**: 16% above entry
  - Captures meaningful swing moves
  - 2:1 reward-to-risk ratio
  - Automatic profit-taking

**Position Sizing**
- Hard constraint: 10% max per position
- Sector constraint: 30% max per sector
- Compliance flags violations (advisory mode)

**Portfolio Heat**
- Total capital at risk: 8-10 positions × 8% stop = 64-80% max exposure
- Conservative for swing trading volatility

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.11+
Alpaca Paper Trading Account
OpenAI API Key (GPT-5 access)
Perplexity API Key
```

### Installation

```bash
# Clone repository
git clone [repository-url]
cd Sentinel

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp config.py.example config.py
# Edit config.py with your API keys
```

### Configuration

Edit `config.py`:

```python
# Alpaca Paper Trading
APCA_API_KEY_ID = "your_alpaca_key"
APCA_API_SECRET_KEY = "your_alpaca_secret"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

# OpenAI (GPT-5)
OPENAI_API_KEY = "your_openai_key"

# Perplexity (News Sentiment)
PERPLEXITY_API_KEY = "your_perplexity_key"
```

### Daily Execution

```bash
# Run the control panel (interactive UI)
python sentinel_control_panel.py

# Main menu options:
# [1] Request Trading Plan  - Generate new plan
# [2] Execute Approved Plan - Execute previously approved plan
# [3] View Plan Status      - See current plan details
# [4] Exit                  - Quit system
```

---

## 📊 System Components

### Research Department (v3.0)
**Location**: `Departments/Research/research_department.py`

**Features**:
- Two-stage filtering (swing suitability → technical filters)
- Adaptive thresholds (auto-adjusts to find ~50 candidates)
- 16-hour data cache (market close to next run)
- yfinance integration for price/volume data

**Outputs**:
- Composite score (0-100)
- Technical score (RSI, MACD, moving averages)
- Fundamental score (profitability, valuation, growth)
- Swing suitability score (volatility, liquidity, momentum)

### News Department
**Location**: `Departments/News/news_department.py`

**Features**:
- Perplexity AI sentiment analysis
- Batch processing (10 concurrent requests)
- 16-hour cache per ticker
- Graceful fallback to neutral (50.0) on errors

**Outputs**:
- Sentiment score (0-100)
- News summary (key headlines)
- Sentiment reasoning (why bullish/bearish/neutral)

### GPT-5 Portfolio Optimizer
**Location**: `Departments/Executive/gpt5_portfolio_optimizer.py`

**Features**:
- OpenAI GPT-5 API integration
- Holistic portfolio analysis (all candidates at once)
- Market condition awareness (VIX, SPY trend)
- Conviction-weighted allocation
- Strategic reasoning output

**Outputs**:
- Selected tickers (8-10 stocks)
- Capital allocation per ticker
- Reasoning for each selection
- Portfolio-level strategy explanation

### Trading Department
**Location**: `Departments/Trading/trading_department.py`

**Features**:
- Bracket order execution (stop-loss + take-profit)
- Real-time price query from Alpaca
- Duplicate order prevention
- UUID to string conversion (database compatibility)
- Retry logic (database only, not Alpaca submission)
- Hard constraint validation before submission

**Order Flow**:
1. Receive order from CEO
2. Validate hard constraints (position size, portfolio value)
3. Query current market price from Alpaca
4. Calculate bracket prices (8% stop, 16% target)
5. Submit market order with bracket orders to Alpaca
6. Store in database (with retry on failure)
7. Send confirmation to Portfolio & Compliance

---

## 🎮 Control Panel Features

### Main Menu

```
1. Request Trading Plan
   - Runs 3-stage workflow
   - GPT-5 optimization
   - Displays proposed trades with scores
   - Shows compliance advisory notes

2. Execute Approved Plan
   - Submits orders to Trading Department
   - Bracket orders automatically attached
   - Real-time execution logging
   - Confirmation messages

3. View Plan Status
   - Current plan details
   - Stage quality scores
   - Trade breakdown
   - Compliance notes

4. Exit
   - Clean shutdown
```

### Plan Display

```
TRADING PLAN SUMMARY
────────────────────
Total Trades: 8
Research Candidates: 50
GPT-5 Selected: 8
Compliance Flagged: 0
Overall Quality: 96/100

WORKFLOW STAGES
────────────────
✓ Research: 50 candidates (avg score: 48.0)
✓ News: 50/50 sentiment coverage (100%)
✓ GPT-5: 8 positions, $91,000 allocated
✓ Compliance: Advisory review (0 violations)

PROPOSED TRADES
────────────────
1. CARR - 168 shares @ $59.49 = $10,000
   Composite: 60.2/100
   Sector: Industrials

2. CCL - 485 shares @ $28.83 = $14,000
   Composite: 69.2/100
   Sector: Consumer Cyclical
   [COMPLIANCE FLAG: 14% position > 10% limit]

...
```

---

## 📈 Performance Monitoring

### Current Positions (Live)

```
Portfolio Value: $100,200
Daily P/L: +$174 (+0.17%)
Cash: $11,052
Buying Power: $111,226

Active Positions: 8
- IBKR: $15,372 (+$206)
- CCL: $13,803 (-$19)
- FITB: $11,904 (-$13)
- GLW: $9,905 (+$19)
- CARR: $9,738 (-$13)
- HPQ: $9,736 (+$36)
- ODFL: $9,668 (-$9)
- COP: $8,953 (+$10)

Bracket Orders: 16 active
- 8 stop-loss orders (held)
- 8 take-profit orders (pending)
```

---

## 🔧 Configuration Files

### `config.py`
API keys and environment settings (not in Git)

### `Config/hard_constraints.yaml`
Trading rules enforced by Trading Department

```yaml
max_position_size_pct: 10.0    # Max 10% per position
max_sector_exposure_pct: 30.0  # Max 30% per sector
max_daily_loss_pct: 3.0        # Stop trading if down 3% today
min_account_value: 1000        # Emergency brake
```

### `Config/compliance_config.yaml`
Compliance Department advisory thresholds

### `Config/risk_config.yaml`
Risk scoring parameters (deprecated - absorbed into Research v3.0)

---

## 🗄️ Database Schema

### `sentinel.db` (SQLite)

**Tables**:
- `trading_orders`: Order execution history
- `research_cache`: 16-hour data cache
- `news_sentiment_cache`: Sentiment analysis cache
- `daily_reports`: Performance tracking
- `compliance_logs`: Advisory notes

**Key Fields** (`trading_orders`):
- `order_id`: Internal tracking ID
- `alpaca_order_id`: Alpaca's UUID (converted to string)
- `ticker`, `action`, `quantity`, `limit_price`
- `status`: SUBMITTED, FILLED, CANCELLED, FAILED
- `submitted_timestamp`, `filled_timestamp`
- `executive_approval_msg_id`: Message chain tracking

---

## 🧪 Testing

### Unit Tests
```bash
# Test bracket order calculations
python test_bracket_orders.py

# Test workflow execution
python test_workflow_execution.py

# Test CEO trading plan generation
python test_ceo_trading_plan.py
```

### Integration Tests
```bash
# Test full pipeline (no actual orders)
python sentinel_control_panel.py
# Select option 1 (Request Trading Plan)
# Review plan but DON'T execute
```

---

## 📚 Documentation

- **FUTURE_DIRECTIONS.md**: Roadmap and improvement priorities
- **CHANGELOG.md**: Version history and recent changes
- **Documentation_Dev/**: Detailed technical documentation
  - Architecture diagrams
  - Department specifications
  - API integration guides
  - Phase completion summaries

---

## 🛡️ Safety Features

### Duplicate Order Prevention
- UUID-based order tracking
- Retry logic separated (Alpaca once, database can retry)
- Duplicate detection before submission
- Message archiving after execution

### Risk Constraints
- Hard constraints enforced before execution
- Position size limits (10% max)
- Sector concentration limits (30% max)
- Portfolio value minimums

### Mode Management (Planned)
- Auto-detect market hours
- Prevent trading twice in one day
- Simulation mode after hours
- Manual override controls

---

## 🐛 Known Issues

1. **Real-Time Price API**: Method name incorrect (`get_latest_trade` → needs correct Alpaca SDK method)
   - Impact: Falls back to 16-hour-old prices for bracket calculation
   - Workaround: Using estimated prices (works fine in normal market conditions)
   - Fix: Update to correct Alpaca SDK method (TBD)

2. **Mode Manager Not Integrated**: Can trade multiple times per day
   - Impact: Risk of duplicate trading on same day
   - Mitigation: Duplicate detector prevents duplicate orders
   - Fix: Integrate mode_manager.py into control panel (Priority 1)

3. **No Position Monitoring**: Manual Alpaca dashboard checking required
   - Impact: No real-time P&L visibility during trading day
   - Fix: Build position monitor dashboard (Priority 2)

---

## 📝 Recent Changes

### November 3, 2025 - Bracket Orders & Duplicate Prevention

**Added**:
- Bracket orders with 8% stop-loss, 16% take-profit
- Real-time price query from Alpaca (with fallback)
- Wide brackets philosophy for volatile swing stocks
- GPT-5 prompt updated to reflect bracket strategy

**Fixed**:
- UUID to string conversion for database compatibility
- Retry logic separated (Alpaca submission once only)
- Duplicate order prevention (tested and working)
- Database storage with proper UUID handling

**Live Trading Results**:
- 8 positions executed successfully
- All bracket orders active (stop + target)
- No duplicate orders (verified)
- Portfolio: $100,200 (+$200 first day)

### November 2, 2025 - CEO Orchestration Complete

**Added**:
- CEO orchestration layer (3-stage workflow)
- Operations Manager (workflow execution)
- Advisory compliance (non-blocking reviews)
- Message-based inter-department communication

---

## 🚧 Future Roadmap

See [FUTURE_DIRECTIONS.md](Documentation_Dev/FUTURE_DIRECTIONS.md) for detailed improvement plans.

**Immediate Priorities**:
1. Integrate Mode Manager (prevent duplicate trading days)
2. Build Position Monitor (real-time P&L tracking)
3. Fix real-time price API (correct Alpaca SDK method)

**Short-Term**:
4. Trade outcome tracker (win rates, hold times)
5. Daily performance reports (automated summaries)
6. Market regime detector (VIX-based adaptation)

**Long-Term**:
7. Universe expansion (add Russell 2000)
8. Bracket optimization (data-driven percentages)
9. Advanced position management (trailing stops)

---

## 📞 Contact & Support

**Repository**: [GitHub URL]
**Author**: WJC
**Version**: Phase 1 Complete - Live Paper Trading
**Last Updated**: November 3, 2025

---

## ⚖️ License

Private - All Rights Reserved

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 🙏 Acknowledgments

- **OpenAI GPT-5**: Portfolio optimization intelligence
- **Perplexity AI**: News sentiment analysis
- **Alpaca Markets**: Paper trading platform
- **yfinance**: Market data
- **Claude (Anthropic)**: Development assistance

---

**Remember**: "We are breeding a racehorse, not a pony that gives rides at a carnival."
