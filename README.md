# Sentinel Corporation

**Inter-day swing trading system powered by AI-driven portfolio optimization**

> "We are breeding a racehorse, not a pony that gives rides at a carnival."

---

## Overview

Sentinel Corporation is an **AI-powered swing trading system** designed to profit from market momentum over 1-4 week hold periods. The system maintains approximately **60 positions** that constantly rotate to capture the best-performing stocks in the current market environment.

### Key Features

- **GPT-5 Portfolio Optimizer**: Holistic decision-making for both buys AND sells
- **Multi-Department Architecture**: Research, News, Risk, Portfolio, Compliance, Trading
- **Swing Trading Philosophy**: High volatility (20-40%) = opportunity, not danger
- **Adaptive Filtering**: Automatically adjusts technical filters to find ~50 candidates daily
- **Ground Truth Principle**: Alpaca API as source of truth for position data
- **16-Hour Data Freshness**: All cached data expires within 16 hours

---

## Architecture

### Current State: Phase 1.5 Complete

```
Research Department (Technical Analysis)
    ├─> Adaptive filtering (RSI, Volume, Price)
    ├─> yfinance for price/volume data
    └─> Output: ~50 buy candidates

News Department (Sentiment Analysis)
    ├─> Perplexity AI batch fetching (10 concurrent)
    ├─> 16-hour sentiment cache
    └─> Output: Sentiment scores (0-100)

Risk Department (Advisory)
    ├─> Calculate risk metrics (ATR, volatility, R:R)
    ├─> Assign risk_score (0-100, HIGHER = BETTER SWING TRADE)
    ├─> Generate warnings (not rejections)
    └─> Output: All candidates with risk assessment

                        ↓

Portfolio Optimizer (GPT-5) [Phase 2+]
    ├─> Receives ~110 stocks (50 candidates + 60 holdings)
    ├─> Decides BOTH sells and buys
    └─> Output: Executable trading plan

                        ↓

Compliance Department [Phase 2+]
    ├─> Reviews trading plan
    ├─> Sends feedback to Portfolio Optimizer
    └─> Iterates until plan passes

                        ↓

Trading Department [Phase 2+]
    ├─> Executes approved trades via Alpaca
    └─> Logs all transactions
```

---

## Sentinel Corporation's Risk Philosophy

**Traditional finance says**: High volatility = danger, wide stops = over-exposed

**Sentinel Corporation says**:
- ✓ **High volatility (20-40%)** = Motion of the ocean (GOOD)
- ✓ **Wide stops (5-10%)** = Room to run (GOOD)
- ✓ **Momentum stocks** = Trending moves (GOOD)
- ✗ **Low volatility (<15%)** = Stagnation risk (BAD)
- ✗ **Tight stops (<3%)** = Death by 1000 cuts (BAD)

### What "Risk" Means at SC

1. **Stagnation Risk**: Stock doesn't move → capital eroded by inflation
2. **Opportunity Cost Risk**: Boring stock clogs slot → missing better movers
3. **Time Risk**: Takes >1 month to profit → wasted position
4. **Illiquidity Risk**: Can't exit when needed → trapped capital
5. **Excessive Leverage Risk**: Over-positioned → account destruction

**See [SENTINEL_RISK_PHILOSOPHY.md](SENTINEL_RISK_PHILOSOPHY.md) for complete philosophy**

---

## Risk Score Interpretation

All departments use **0-100 scoring** where **HIGHER = BETTER**:

| Score | Grade | Meaning |
|-------|-------|---------|
| **90-100** | A+ | EXCELLENT swing trade - strong buy |
| **80-89** | A | VERY GOOD swing trade - good buy |
| **70-79** | B | GOOD swing trade - buy |
| **60-69** | C | ACCEPTABLE - consider if limited alternatives |
| **50-59** | D | MARGINAL - either too boring OR borderline risky |
| **0-49** | F | POOR/REJECT - not suitable for swing trading |

### Department Scores

- **Research** (Technical): 100 = excellent setup, 0 = poor technicals
- **News** (Sentiment): 100 = very bullish, 50 = neutral, 0 = very bearish
- **Risk** (Swing Suitability): 100 = excellent swing trade, 0 = unsuitable
- **Portfolio** (Overall): Weighted combination of all scores

---

## Installation

### Prerequisites

```bash
Python 3.10+
Windows (current deployment environment)
```

### Setup

```bash
# Clone repository
git clone <repo-url>
cd Sentinel

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **API Keys**: Set environment variables
   ```bash
   ALPACA_API_KEY=<your-alpaca-key>
   ALPACA_SECRET_KEY=<your-alpaca-secret>
   PERPLEXITY_API_KEY=<your-perplexity-key>  # Optional
   ```

2. **Config Files**:
   - `Config/portfolio_config.yaml` - Portfolio settings
   - `Config/research_config.yaml` - Research parameters
   - `Config/risk_config.yaml` - Risk limits

---

## Usage

### Run Individual Departments

```bash
# Test News Department (sentiment analysis)
python test_news_department.py

# Test Research Department (technical analysis)
python test_research_quick.py  # 25 tickers (fast)
python test_research_department.py  # Full universe (~600 tickers)

# Test Risk Department (risk assessment)
python test_risk_department.py
```

### Run Full System (Phase 2+)

```bash
# Not yet implemented - awaiting CEO Orchestration Layer
python main_script.py
```

---

## Testing

All Phase 1 departments tested and passing:

| Department | Status | Test File | Key Metrics |
|------------|--------|-----------|-------------|
| News | ✓ PASSING | `test_news_department.py` | 25 tickers in 1.0s |
| Research | ✓ PASSING | `test_research_quick.py` | Adaptive filtering works |
| Risk v2.1 | ✓ PASSING | `test_risk_department.py` | Swing scoring correct |

```bash
# Run all tests
python test_news_department.py
python test_research_quick.py
python test_risk_department.py
```

---

## Project Structure

```
Sentinel/
├── Departments/
│   ├── News/
│   │   ├── __init__.py
│   │   └── news_department.py
│   ├── Research/
│   │   ├── __init__.py
│   │   └── research_department.py
│   ├── Risk/
│   │   ├── __init__.py
│   │   └── risk_department.py
│   ├── Portfolio/
│   ├── Compliance/
│   └── Trading/
├── Config/
│   ├── portfolio_config.yaml
│   ├── research_config.yaml
│   └── risk_config.yaml
├── Messages_Between_Departments/
│   ├── Inbox/
│   └── Outbox/
├── test_news_department.py
├── test_research_quick.py
├── test_risk_department.py
├── sentinel.db
├── SENTINEL_RISK_PHILOSOPHY.md
├── PHASE1_SUMMARY.md
├── CHANGELOG.md
└── README.md
```

---

## Database Schema

### `news_sentiment_cache`
```sql
CREATE TABLE news_sentiment_cache (
    ticker TEXT PRIMARY KEY,
    sentiment_score REAL NOT NULL,      -- 0-100 (higher = more bullish)
    news_summary TEXT,
    sentiment_reasoning TEXT,
    fetched_at TEXT NOT NULL,
    expires_at TEXT NOT NULL            -- 16-hour TTL
)
```

### `research_table` (existing)
- Price/volume data
- Technical indicators (RSI, SMA, etc.)
- 16-hour cache

---

## Development Roadmap

### ✓ Phase 1: Department Refactoring (COMPLETE)
- [x] News Department (sentiment analysis)
- [x] Research Department (technical analysis)
- [x] Risk Department v2.0 (advisory mode)

### ✓ Phase 1.5: Risk Scoring Fix (COMPLETE)
- [x] Fix risk_score to align with swing trading philosophy
- [x] Create SENTINEL_RISK_PHILOSOPHY.md
- [x] Update Risk Department v2.0 → v2.1
- [x] Test swing trading scoring

### Phase 2: CEO Orchestration (NEXT)
- [ ] Main control loop
- [ ] Department coordination
- [ ] Workflow management

### Phase 3: GPT-5 Portfolio Optimizer
- [ ] Receives ~110 stocks (candidates + holdings)
- [ ] Decides BOTH sells and buys
- [ ] Outputs executable trading plan

### Phase 4: Compliance Feedback Loop
- [ ] Reviews trading plan
- [ ] Sends feedback to Portfolio Optimizer
- [ ] Iterates until plan passes

### Phase 5: Integration Testing
- [ ] End-to-end workflow
- [ ] Live trading simulation
- [ ] Performance validation

---

## Configuration

### Risk Limits
- **Max risk per trade**: 1.0% of capital
- **Max portfolio heat**: 5.0% of capital
- **ATR multiplier**: 2.0x for stop-loss
- **Target positions**: ~60 (variable size)
- **Max positions**: 70 (hard limit)

### Data Freshness
- **All cached data**: 16-hour TTL
- **News sentiment**: 16 hours
- **Price/volume data**: 16 hours
- **Market fundamentals**: 16 hours (when implemented)

### Batch Processing
- **Perplexity sentiment**: 10 concurrent requests
- **Research filtering**: Adaptive (5 presets)

---

## Known Issues

1. **yfinance Warnings**: FutureWarning about `auto_adjust` - cosmetic, no impact
2. **Perplexity 401**: Expected when API key not set - graceful fallback to neutral 50.0
3. **BRK.B / BF.B**: Yahoo Finance data issues - stocks skipped correctly
4. **Weekend Testing**: Market closed, may return 0 candidates - correct behavior
5. **Risk __init__.py**: Docstring still says "higher = safer" - needs update

---

## Contributing

This is a private trading system. Contributions are not currently accepted.

---

## License

Proprietary - All rights reserved

---

## Documentation

- **[SENTINEL_RISK_PHILOSOPHY.md](SENTINEL_RISK_PHILOSOPHY.md)** - Complete risk philosophy and scoring rubric
- **[PHASE1_SUMMARY.md](PHASE1_SUMMARY.md)** - Phase 1 & 1.5 implementation details
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

---

## Contact

For questions or issues, contact the Sentinel Corporation development team.

---

**Version**: Phase 1.5 (Risk v2.1, News/Research v1.0)
**Last Updated**: November 2, 2025
**Status**: Phase 1 Complete, Phase 2 Development Starting
