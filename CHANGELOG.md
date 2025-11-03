# Sentinel Corporation - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Phase 2] - 2025-11-02

### Added
- **CEO Orchestration Layer**: New daily cycle orchestrator (`run_daily_cycle.py`)
  - `SentinelCEO` class coordinates all departments
  - Linear pipeline execution: Research → News → Compliance → Portfolio
  - Mesh network architecture: All departments accessible to each other
  - Graceful error handling and comprehensive logging
  - Daily report generation with summary statistics

### Architecture
- **New Pipeline Flow**:
  ```
  Stage 1: Research (v3.0) → Generate ~50 swing-suitable candidates
  Stage 2: News → Add sentiment scores + news summaries
  Stage 3: Compliance → Validate candidates (simplified)
  Stage 4: Portfolio → Optimization ready
  ```
- **Mesh Network**: All departments initialized upfront, can communicate as needed
- **Risk Department Retired**: Functionality absorbed into Research Stage 1 (swing suitability scoring)
- **Entry Point**: `python run_daily_cycle.py` - single command to run full pipeline

### Changed
- **Department Initialization**: Standardized across all departments
  - Research: `db_path`, `alpaca_client`
  - News: `db_path`
  - Compliance: `config_path` (Path), `db_path` (Path)
  - Portfolio: `config_path` (Path), `db_path` (Path)
- **News Integration**: Batch sentiment scoring via `get_sentiment_scores(tickers)`
  - Returns dict with `sentiment_score`, `news_summary`, `sentiment_reasoning`
  - Graceful fallback to neutral (50.0) on API errors
- **Compliance Integration**: Simplified pre-validation (full validation at trade execution)

### Fixed
- Missing `__init__.py` files for Compliance and Portfolio departments
- Department initialization parameter mismatches
- News API method name (singular → plural)

### Testing
- Full end-to-end pipeline tested and passing
- Successfully processes 50 candidates through all 4 stages
- ~30s execution time (including Research Stage 1 scoring)
- Handles API failures gracefully (Perplexity 401 → neutral sentiment)

### Files Created
- `run_daily_cycle.py` - Main orchestrator and entry point
- `Departments/Compliance/__init__.py`
- `Departments/Portfolio/__init__.py`

### Output Example
```
Research: 50 candidates, 0 holdings
News: 50 tickers scored
Compliance: 50 approved, 0 flagged
Portfolio: 50 ready for optimization
```

---

## [Phase 1.5] - 2025-11-02

### Fixed
- **Risk Department Scoring Philosophy**: Corrected risk_score calculation to align with Sentinel Corporation's swing trading philosophy
  - Changed from traditional finance scoring (100 = safest) to swing trading scoring (100 = excellent swing trade)
  - Now correctly rewards high volatility (20-40%), wide stops (5-10%), and good R:R ratios (≥2:1)
  - Low volatility stocks (<15%) now score lower (stagnation risk)
  - Updated scoring: AAPL 85.0, NVDA 80.0 vs. old AAPL/NVDA 100.0

### Added
- **SENTINEL_RISK_PHILOSOPHY.md**: Comprehensive philosophy document (400+ lines)
  - Defines SC's unique risk philosophy: "breeding a racehorse, not a carnival pony"
  - Documents swing trading requirements and scoring rubric
  - Provides context block for AI departments (GPT-5, CEO)
  - Establishes scoring consistency across all departments (higher = better)
- **Warning Categories**: Added three advisory categories
  - "Too Boring" - low volatility, tight stops, stagnation risk
  - "Excessive Risk" - over-leveraged, too volatile
  - "Poor Setup" - bad R:R ratio, invalid data

### Changed
- **Risk Department**: v2.0 → v2.1
  - Updated `_calculate_risk_score()` method with swing trading logic
  - Updated `_generate_warnings()` to include "too boring" warnings
  - Updated docstrings to clarify swing trading philosophy
- **test_risk_department.py**: Updated expectations for swing trading scoring
- **Departments/Risk/__init__.py**: Updated docstring (still says "higher = safer" - needs fix)

### Documentation
- **PHASE1_SUMMARY.md**: Added Phase 1.5 section documenting risk scoring fix
- **README.md**: (pending update)

---

## [Phase 1] - 2025-11-02

### Added
- **News Department**: Separated sentiment analysis from Research
  - Perplexity AI batch fetching (10 concurrent requests)
  - 16-hour cache TTL for sentiment scores
  - Async/await pattern for performance
  - Fallback to neutral (50.0) on API errors
  - Database table: `news_sentiment_cache`

### Changed
- **Research Department**: Major refactor (backed up as `.bak`)
  - Removed all Perplexity API calls (moved to News Department)
  - Added adaptive filtering (5 presets: VERY_STRICT → VERY_RELAXED)
  - Added Alpaca integration for current holdings
  - Added 16-hour cache for price/volume data
  - Changed sentiment score to 50.0 placeholder (filled by News Dept)
  - Output: ~50 buy candidates (adaptive) + current holdings (~60)

- **Risk Department**: Changed from gatekeeper to advisor (v2.0)
  - Removed approval/rejection authority
  - Changed role from gatekeeper to advisor
  - Added `risk_score` (0-100, initially traditional finance scoring)
  - Added `risk_warnings` list (concerns, not blockers)
  - All candidates now pass through with risk assessment
  - Calculates ATR-based stop-loss, position sizing, R:R ratio, volatility

### Architecture
- **New Workflow**:
  ```
  Research (programmatic) ──┐
  News (sentiment) ─────────┼─→ Risk (advisory) → Portfolio Optimizer (GPT-5)
  Alpaca (holdings) ────────┘
  ```
- **Key Principles Established**:
  1. Separation of Concerns: Sentiment in News, technicals in Research
  2. Ground Truth: Alpaca is source of truth for positions
  3. Advisory, Not Authoritative: Risk recommends, doesn't reject
  4. Data Freshness: All data < 16 hours old
  5. Adaptive Filtering: Research adjusts to find ~50 candidates

### Testing
- All departments tested and passing
- News: 25 tickers in 1.0s, cache 125x faster
- Research: Adaptive filtering works, 30.7s for 25 tickers
- Risk: All candidates pass, risk scores 0-100 valid

### Files Created
- `Departments/News/__init__.py`
- `Departments/News/news_department.py`
- `Departments/Research/__init__.py`
- `Departments/Risk/__init__.py`
- `test_news_department.py`
- `test_research_department.py`
- `test_research_quick.py`
- `test_risk_department.py`
- `PHASE1_SUMMARY.md`

### Database
- Added table: `news_sentiment_cache` (ticker, sentiment_score, news_summary, reasoning, timestamps)

---

## [Week 7] - 2025-11-01

### Completed
- System Integration & Live Trading Preparation
- All tests passing (100%)
- Ready for live trading environment

---

## [Week 5] - 2025-10-30

### Added
- PreTradeValidator: Validates trades before execution
- PostTradeAuditor: Audits trades after execution
- Main Orchestrator: Coordinates all departments
- Integration testing suite

---

## [Week 4] - 2025-10-28

### Completed
- Main orchestrator implementation
- Integration testing
- All core functionality working

---

## Format Notes

### Change Types
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

### Version Format
- **Phase X**: Major architectural changes
- **Week X**: Sprint-based development milestones
- **vX.Y.Z**: Semantic versioning (when released)
