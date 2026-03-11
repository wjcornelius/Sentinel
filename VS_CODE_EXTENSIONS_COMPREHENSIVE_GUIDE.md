# VS Code Extensions & AI Tools for Quantitative Trading Development

**Comprehensive Guide for QuantLab Project**
Research Date: November 2024
Focus: Python-based algorithmic trading systems with AI/ML integration

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Multi-AI Collaboration Setup](#multi-ai-collaboration-setup)
3. [Extension Categories](#extension-categories)
4. [Implementation Roadmap](#implementation-roadmap)
5. [Specific Q&A](#specific-qa)
6. [Cost Analysis](#cost-analysis)

---

## Executive Summary

### Key Findings

**Multi-AI Collaboration is Real and Accessible**
- GitHub Copilot now offers FREE tier with both GPT-4o AND Claude 3.5 Sonnet
- Continue.dev allows unlimited model switching (Claude, GPT-4, local models)
- Multi-AI code review workflows are production-ready

**Major 2024-2025 Updates**
- GitHub Copilot Free Tier (Dec 2024): 2,000 completions/month with GPT-4o + Claude
- Ruff: 150-200x faster than Flake8, replacing Black + isort + Flake8
- Data Wrangler GA (May 2024): Visual DataFrame exploration
- Native test coverage in Python extension

**Cost Comparison**
```
VS Code + Extensions:  $0-10/month  (better for quant work)
Cursor IDE:            $20-200/month (lacks Jupyter features)
```

**Recommended Minimal Setup (FREE)**
1. GitHub Copilot (free tier)
2. Continue.dev (multi-model)
3. Jupyter + Data Wrangler
4. Ruff + Mypy
5. DBCode
6. GitLens

---

## Multi-AI Collaboration Setup

### Method 1: GitHub Copilot (Easiest - FREE!)

**What Changed in December 2024:**
GitHub Copilot added FREE tier with:
- 2,000 code completions/month
- 50 chat messages/month
- **BOTH GPT-4o AND Claude 3.5 Sonnet**

**Setup:**
```bash
# Install extension
code --install-extension GitHub.copilot

# Sign in with GitHub account (free tier automatic)
# Settings → GitHub Copilot → Model → Choose between:
#   - gpt-4o (default)
#   - claude-3.5-sonnet
```

**Multi-AI Workflow:**
1. Use GPT-4o for initial code generation (faster)
2. Switch to Claude 3.5 Sonnet for code review
3. Toggle between models using chat interface

**Pros:**
- FREE with GitHub account
- Both frontier models included
- Native VS Code integration
- Context-aware suggestions

**Cons:**
- Limited to 2,000 completions/month (free tier)
- Can't run models simultaneously (must toggle)
- Requires internet connection

**Use Cases for QuantLab:**
- Strategy prototyping with GPT-4o
- Code review with Claude 3.5 Sonnet
- Documentation generation
- Test case creation

---

### Method 2: Continue.dev (Most Flexible - FREE!)

**What It Is:**
Open-source AI coding assistant that lets you configure unlimited models and switch between them in real-time.

**Supported Models:**
- Claude 3.5 Sonnet, Opus (via API)
- GPT-4, GPT-4 Turbo (via OpenAI API)
- Gemini Pro (via Google AI)
- Local models (Ollama, LM Studio)
- **Can configure ALL of them at once**

**Setup:**
```bash
# Install extension
code --install-extension Continue.continue

# Configure models in ~/.continue/config.json
{
  "models": [
    {
      "title": "Claude 3.5 Sonnet",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "apiKey": "YOUR_ANTHROPIC_API_KEY"
    },
    {
      "title": "GPT-4 Turbo",
      "provider": "openai",
      "model": "gpt-4-turbo-preview",
      "apiKey": "YOUR_OPENAI_API_KEY"
    },
    {
      "title": "Local Codestral",
      "provider": "ollama",
      "model": "codestral"
    }
  ]
}
```

**Multi-AI Code Review Workflow:**
1. Write code with Claude 3.5 Sonnet
2. Select code → Cmd+Shift+L → "Review this code"
3. Switch to GPT-4 Turbo → Get second opinion
4. Compare suggestions side-by-side
5. Iterate based on consensus

**Advanced: Automated Multi-AI Review Script**
```python
# continue_multi_review.py
# Run this to get automated reviews from all configured models

import subprocess
import json

models = ["Claude 3.5 Sonnet", "GPT-4 Turbo", "Gemini Pro"]

for model in models:
    print(f"\n{'='*80}")
    print(f"Review from {model}")
    print('='*80)

    # Continue CLI command (hypothetical - shows concept)
    cmd = f'continue chat --model "{model}" --prompt "Review this code for bugs and improvements"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
```

**Pros:**
- Unlimited model configurations
- Local models supported (privacy!)
- Free if using local models
- Context window up to 200k tokens (Claude)

**Cons:**
- Requires API keys (costs per token)
- Setup more complex than Copilot
- No autocomplete (chat-based only)

**Cost Estimates:**
```
Claude 3.5 Sonnet: $3/1M input tokens, $15/1M output tokens
GPT-4 Turbo:       $10/1M input tokens, $30/1M output tokens
Gemini Pro:        FREE (up to limits)
Local models:      $0 (hardware costs only)
```

**Use Cases for QuantLab:**
- Strategy brainstorming with multiple AIs
- Bug hunting (get 3 AI opinions)
- Architecture reviews before implementing
- Optimization suggestions

---

### Method 3: Cline (Autonomous Agent - FREE!)

**What It Is:**
Autonomous coding agent that can:
- Read/write files across your codebase
- Execute terminal commands
- Create multi-file implementations
- Debug and test code

**Setup:**
```bash
code --install-extension saoudrizwan.claude-dev

# Now called "Cline" (rebranded from Claude Dev)
```

**Multi-AI Autonomous Workflow:**
```
User: "Create a momentum strategy with RSI filter"

Cline (Claude 3.5):
1. Reads existing strategy files
2. Creates momentum_rsi_strategy.py
3. Writes unit tests
4. Runs tests
5. Asks: "Should I optimize parameters?"

User: "Yes, but get GPT-4's opinion first"

[Switch to Continue.dev with GPT-4]
GPT-4: "Suggests grid search with walk-forward validation"

Cline: Implements GPT-4's suggestion
```

**Pros:**
- Fully autonomous (multi-step tasks)
- Can execute code and fix errors
- Built-in file editing
- Shows diff before applying changes

**Cons:**
- Costs per token (uses Claude API)
- Can make mistakes (review changes!)
- Limited to Claude models only

**Use Cases for QuantLab:**
- "Build complete sentiment analysis module"
- "Add position sizing logic to all strategies"
- "Create backtesting comparison dashboard"
- "Implement Monte Carlo simulation"

**Cost Example:**
- 1 hour of active development: ~$0.50-2.00
- Creating complete feature: ~$2-5
- Still WAY cheaper than developer time!

---

### Method 4: Multi-Model Comparison (YouTube Video Setup)

**The Setup You Saw in the YouTube Video:**

This likely used **Continue.dev** with split terminal/chat windows:

**Layout:**
```
┌─────────────────┬─────────────────┐
│                 │                 │
│   Code Editor   │  Continue Chat  │
│                 │  (Claude)       │
│                 │                 │
├─────────────────┼─────────────────┤
│                 │                 │
│  Terminal       │  Continue Chat  │
│  (running code) │  (GPT-4)        │
│                 │                 │
└─────────────────┴─────────────────┘
```

**Workflow:**
1. Split VS Code window (View → Editor Layout → Split)
2. Left: Write code
3. Top-right: Continue with Claude reviewing
4. Bottom-right: Continue with GPT-4 reviewing
5. Both AIs comment on each other's suggestions!

**Setup Steps:**
```bash
# 1. Install Continue
code --install-extension Continue.continue

# 2. Configure two profiles in Continue settings
# ~/.continue/config.json

{
  "models": [
    {
      "title": "Claude (Primary)",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022"
    },
    {
      "title": "GPT-4 (Reviewer)",
      "provider": "openai",
      "model": "gpt-4-turbo-preview"
    }
  ],

  "experimental": {
    "multiChat": true  # Enable multiple chat panels
  }
}

# 3. Open two Continue chat panels
# Cmd+Shift+P → "Continue: Open Chat"
# Do this twice for two panels

# 4. In each panel, select different model
# Panel 1: Claude 3.5 Sonnet
# Panel 2: GPT-4 Turbo

# 5. Start conversation:
You: "Review this trading strategy implementation"
Claude Panel: [Provides review]
GPT-4 Panel: [Provides different perspective]

You: "GPT-4, what do you think of Claude's suggestion to add position limits?"
GPT-4: [Analyzes Claude's recommendation]

You: "Claude, GPT-4 thinks we should use Kelly Criterion instead. Thoughts?"
Claude: [Responds to GPT-4's idea]
```

**Real Example:**
```
You → Code:
def calculate_position_size(signal_strength, account_balance):
    return account_balance * 0.1  # 10% per trade

You → Claude: "Is this position sizing safe?"
Claude: "10% is aggressive. I recommend 2-5% per trade with Kelly Criterion"

You → GPT-4: "What do you think of Claude's Kelly Criterion suggestion?"
GPT-4: "Agree with caution. Kelly is optimal but can be volatile.
        Suggest Half-Kelly (Kelly/2) for more conservative sizing."

You → Claude: "GPT-4 suggests Half-Kelly. Implement this?"
Claude: "Good point. Here's implementation with Half-Kelly..."

[Both AIs just collaborated on a better solution!]
```

**Pros:**
- Best of both worlds (Claude's reasoning + GPT's knowledge)
- AIs catch each other's mistakes
- More thorough code review
- Learn different approaches

**Cons:**
- Costs 2x tokens (two models)
- More complex to manage
- Can get conflicting advice
- Requires strong judgment to mediate

---

## Extension Categories

### 1. AI/LLM Extensions

#### GitHub Copilot ⭐ MUST-HAVE (FREE!)
**Purpose:** AI pair programmer with inline suggestions

**Installation:**
```bash
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
```

**Key Features:**
- Autocomplete code as you type
- Chat interface for questions
- FREE tier: 2,000 completions/month
- Both GPT-4o AND Claude 3.5 Sonnet

**QuantLab Use Cases:**
- Auto-complete trading logic
- Generate test fixtures
- Document strategies
- Suggest optimizations

**Settings:**
```json
{
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "python": true
  },
  "github.copilot.advanced": {
    "model": "claude-3.5-sonnet"  // or "gpt-4o"
  }
}
```

**Cost:**
- Free: 2,000 completions/month
- Pro: $10/month (unlimited)
- Business: $19/user/month

**Priority:** MUST-HAVE

---

#### Continue.dev ⭐ RECOMMENDED (FREE!)
**Purpose:** Multi-model AI assistant with context awareness

**Installation:**
```bash
code --install-extension Continue.continue
```

**Key Features:**
- Switch between Claude, GPT-4, Gemini, local models
- Codebase-wide context (reads entire project)
- Custom prompts and workflows
- Local model support (privacy)

**QuantLab Use Cases:**
- "Explain how sentiment scoring works across all strategies"
- "Find all places where we calculate RSI"
- "Compare our MACD implementation to standard formula"
- "Generate backtest report from this data"

**Configuration:**
```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "Claude Sonnet (Strategy Dev)",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "apiKey": "YOUR_KEY",
      "context": ["strategies/", "backtesting/"]
    },
    {
      "title": "GPT-4 Turbo (Review)",
      "provider": "openai",
      "model": "gpt-4-turbo-preview",
      "apiKey": "YOUR_KEY"
    }
  ],
  "customCommands": [
    {
      "name": "Review Strategy",
      "prompt": "Review this trading strategy for:\n1. Risk management\n2. Edge validity\n3. Implementation bugs\n4. Performance optimization"
    }
  ]
}
```

**Cost:**
- Extension: FREE
- API usage: Pay-per-token to providers

**Priority:** RECOMMENDED

---

#### Cline (Claude Dev) - RECOMMENDED
**Purpose:** Autonomous AI coding agent

**Installation:**
```bash
code --install-extension saoudrizwan.claude-dev
```

**Key Features:**
- Executes multi-step tasks autonomously
- Reads/writes files across codebase
- Runs terminal commands
- Creates tests and documentation
- Shows diffs before applying

**QuantLab Use Cases:**
```
Task: "Add volatility-based position sizing to all strategies"

Cline will:
1. Read all strategy files
2. Identify where position sizing is calculated
3. Create volatility calculator module
4. Update each strategy to use it
5. Write unit tests
6. Run tests to verify
7. Create documentation
```

**Example Commands:**
- "Implement Sharpe ratio calculation for dashboard"
- "Add error handling to all Alpaca API calls"
- "Create Monte Carlo simulation for strategy backtests"
- "Refactor sentiment module to support multiple data sources"

**Cost:**
- Extension: FREE
- Claude API usage: ~$0.50-2/hour of active use

**Priority:** RECOMMENDED

---

### 2. Python Development Extensions

#### Ruff ⭐ MUST-HAVE (FREE!)
**Purpose:** Ultra-fast Python linter and formatter

**Why Ruff over Black/Flake8:**
- 150-200x faster than alternatives
- Replaces Black + isort + Flake8 + more
- Auto-fixes most issues
- Actively maintained (2023+)

**Installation:**
```bash
code --install-extension charliermarsh.ruff

# Also install in project
pip install ruff
```

**Configuration:**
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

ignore = [
    "E501",  # line too long (let formatter handle)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# Fix on save
[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports OK in __init__
"tests/*" = ["S101"]       # Assert OK in tests
```

**VS Code Settings:**
```json
{
  "ruff.enable": true,
  "ruff.organizeImports": true,
  "ruff.fixAll": true,

  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    }
  }
}
```

**Impact on QuantLab:**
- Auto-formats all Python files consistently
- Catches bugs before running code
- Organizes imports automatically
- Enforces style guide

**Priority:** MUST-HAVE

---

#### Pylance ⭐ MUST-HAVE (FREE!)
**Purpose:** Fast Python language server with IntelliSense

**Installation:**
```bash
code --install-extension ms-python.vscode-pylance
```

**Key Features:**
- Type checking (like mypy, but faster)
- Auto-imports
- Code navigation (Go to Definition)
- Rename refactoring
- Signature help

**Settings for QuantLab:**
```json
{
  "python.analysis.typeCheckingMode": "basic",  // or "strict"
  "python.analysis.autoImportCompletions": true,
  "python.analysis.diagnosticMode": "workspace",  // Check all files
  "python.analysis.extraPaths": [
    "./strategies",
    "./backtesting",
    "./Departments"
  ]
}
```

**Use Cases:**
- Jump to strategy implementation: Cmd+Click
- Rename variable across all files: F2
- See function signatures as you type
- Auto-import when using undefined names

**Priority:** MUST-HAVE

---

#### Mypy Type Checker - RECOMMENDED
**Purpose:** Static type checking for Python

**Installation:**
```bash
code --install-extension ms-python.mypy-type-checker

pip install mypy
```

**Why Use Type Hints:**
```python
# Without types (unclear what's expected)
def calculate_sharpe(returns, risk_free):
    return (returns.mean() - risk_free) / returns.std()

# With types (crystal clear)
import pandas as pd
from typing import float

def calculate_sharpe(
    returns: pd.Series,
    risk_free: float = 0.02
) -> float:
    """
    Calculate Sharpe ratio.

    Args:
        returns: Series of strategy returns
        risk_free: Annual risk-free rate (default 2%)

    Returns:
        Sharpe ratio (higher is better)
    """
    return (returns.mean() - risk_free) / returns.std()

# Now mypy catches errors:
sharpe = calculate_sharpe("AAPL", "invalid")  # ERROR: Wrong types!
```

**Configuration:**
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Start lenient, tighten later
check_untyped_defs = true

# Ignore third-party packages without stubs
[[tool.mypy.overrides]]
module = [
    "alpaca.*",
    "backtesting.*",
]
ignore_missing_imports = true
```

**Gradual Adoption:**
```python
# Start by typing public APIs
def get_signals(tickers: list[str]) -> pd.DataFrame:
    ...

# Then internal functions
def _calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    ...

# Finally, use strict mode per-file
# strategies/alpha_scout.py
# type: ignore  # TODO: Add types later
```

**Priority:** RECOMMENDED

---

#### autoDocstring - RECOMMENDED
**Purpose:** Auto-generate docstrings from function signatures

**Installation:**
```bash
code --install-extension njpwerner.autodocstring
```

**Usage:**
```python
def backtest_strategy(
    strategy_class: type,
    tickers: list[str],
    start_date: str,
    end_date: str,
    initial_capital: float = 100000
) -> dict:
    # Type """ and hit Enter
    """
    _summary_  # ← Cursor here, AI fills in

    Args:
        strategy_class (type): _description_
        tickers (list[str]): _description_
        start_date (str): _description_
        end_date (str): _description_
        initial_capital (float, optional): _description_. Defaults to 100000.

    Returns:
        dict: _description_
    """
```

**With AI Enhancement:**
Combine with Copilot/Continue to auto-fill descriptions:

```python
def backtest_strategy(...):
    """
    Run backtest for a trading strategy across multiple tickers.

    Executes walk-forward analysis with the specified strategy class,
    calculates performance metrics, and returns detailed results.

    Args:
        strategy_class: Strategy class inheriting from Strategy base
        tickers: List of ticker symbols to trade
        start_date: Backtest start date (YYYY-MM-DD)
        end_date: Backtest end date (YYYY-MM-DD)
        initial_capital: Starting portfolio value in USD

    Returns:
        Dictionary containing:
        - metrics: Performance metrics (Sharpe, drawdown, etc.)
        - trades: DataFrame of all executed trades
        - equity_curve: Time series of portfolio value

    Example:
        >>> results = backtest_strategy(
        ...     AlphaScoutV2,
        ...     ['AAPL', 'MSFT'],
        ...     '2020-01-01',
        ...     '2023-12-31'
        ... )
        >>> print(f"Sharpe: {results['metrics']['sharpe']:.2f}")
    """
```

**Settings:**
```json
{
  "autoDocstring.docstringFormat": "google",  // or "numpy", "sphinx"
  "autoDocstring.startOnNewLine": false,
  "autoDocstring.includeExtendedSummary": true,
  "autoDocstring.includeName": false
}
```

**Priority:** RECOMMENDED

---

### 3. Jupyter & Data Science Extensions

#### Jupyter ⭐ MUST-HAVE (FREE!)
**Purpose:** Run Jupyter notebooks natively in VS Code

**Installation:**
```bash
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.vscode-jupyter-cell-tags
code --install-extension ms-toolsai.vscode-jupyter-slideshow
```

**Why VS Code > Jupyter Lab for Trading:**
1. Better Git integration (diff notebooks easily)
2. Built-in debugger for notebook cells
3. Variable explorer with DataFrame preview
4. IntelliSense in cells
5. Export to Python script with one click

**Key Features:**
- Interactive window (like Jupyter, but in VS Code)
- Run cells, see output inline
- Debug notebook cells with breakpoints
- Variable explorer shows all DataFrames
- Plot viewer with zoom/pan
- Export to .py, .html, .pdf

**QuantLab Use Cases:**
```python
# strategy_research.ipynb

# Cell 1: Load data
import pandas as pd
from backtesting.data_loader import load_prices

prices = load_prices(['AAPL', 'MSFT', 'GOOGL'], '2020-01-01', '2023-12-31')
prices.head()  # ← Shows interactive DataFrame preview

# Cell 2: Calculate indicators
from strategies.indicators import calculate_rsi, calculate_macd

signals = pd.DataFrame()
signals['rsi'] = calculate_rsi(prices['close'])
signals['macd'] = calculate_macd(prices['close'])

# Cell 3: Visualize
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
ax1.plot(prices['close'])
ax1.set_title('Price')
ax2.plot(signals['rsi'])
ax2.axhline(30, color='g')
ax2.axhline(70, color='r')
ax2.set_title('RSI')
plt.show()  # ← Shows in VS Code plot viewer!

# Cell 4: Backtest
from backtesting import Backtest
from strategies.alpha_scout_v2 import AlphaScoutV2

bt = Backtest(prices, AlphaScoutV2, cash=100000)
stats = bt.run()
print(stats)  # ← Formatted output inline

# Cell 5: Export to production
# File → Export → Export as Python Script
# → Creates strategy_research.py with all cells as functions
```

**Settings:**
```json
{
  "jupyter.askForKernelRestart": false,  // Auto-restart
  "jupyter.interactiveWindow.textEditor.executeSelection": true,
  "notebook.output.textLineLimit": 500,  // More output lines
  "notebook.cellToolbarLocation": {
    "default": "right"
  }
}
```

**Priority:** MUST-HAVE

---

#### Data Wrangler ⭐ RECOMMENDED (FREE!)
**Purpose:** Visual DataFrame exploration and cleaning

**Installation:**
```bash
code --install-extension ms-toolsai.datawrangler
```

**What It Does:**
- Opens DataFrames in visual spreadsheet-like interface
- Sort, filter, search without writing code
- Generate cleaning code automatically
- Summary statistics with one click
- Export to CSV, Excel, SQL

**Example:**
```python
# In notebook or Python file
import pandas as pd
trades_df = pd.read_csv('trades.csv')

# Right-click on trades_df → "Open in Data Wrangler"
```

**Data Wrangler Opens:**
```
╔═══════════════════════════════════════════════════════════╗
║ trades_df (1,234 rows × 15 columns)                       ║
║                                                           ║
║ [Sort] [Filter] [Clean] [Summarize] [Export]             ║
╠════════╤═══════╤═══════════╤═══════════╤════════════════╣
║ ticker │ date  │ action    │ price     │ composite_score║
╠════════╪═══════╪═══════════╪═══════════╪════════════════╣
║ AAPL   │ 2024-01-05 │ BUY  │ 185.23    │ 0.752          ║
║ MSFT   │ 2024-01-05 │ BUY  │ 398.11    │ 0.681          ║
║ AAPL   │ 2024-01-12 │ SELL │ 192.45    │ 0.234          ║
║ ...                                                       ║
╚════════════════════════════════════════════════════════════╝

Actions:
✓ Filter: composite_score > 0.7
✓ Sort: date (descending)
✓ Group by: ticker
✓ Generate code: [Copy to Clipboard]
```

**Generated Code:**
```python
# Auto-generated by Data Wrangler
filtered_df = trades_df[trades_df['composite_score'] > 0.7]
sorted_df = filtered_df.sort_values('date', ascending=False)
summary = sorted_df.groupby('ticker').agg({
    'composite_score': ['mean', 'std'],
    'price': ['min', 'max']
})
```

**QuantLab Use Cases:**
- Explore trade history visually
- Find patterns in winning trades
- Clean sentiment data
- Debug DataFrame shape issues
- Quick summary statistics

**Priority:** RECOMMENDED

---

#### Python Debugger ⭐ MUST-HAVE (FREE!)
**Purpose:** Step-by-step code execution with breakpoints

**Installation:**
```bash
# Built into Python extension
code --install-extension ms-python.python
code --install-extension ms-python.debugpy
```

**Setup for QuantLab:**

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Trading Bot",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/run_daily_trading.py",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Debug Backtest",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/backtesting/portfolio_backtest.py",
      "args": [
        "--strategy", "AlphaScoutV2",
        "--start", "2020-01-01",
        "--end", "2023-12-31"
      ],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Attach to Running Bot",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      }
    }
  ]
}
```

**Usage:**
```python
# strategies/alpha_scout_v2.py

def calculate_composite_score(self, ticker: str) -> float:
    # Set breakpoint: Click left margin or F9
    sentiment = self.get_sentiment(ticker)  # ← Breakpoint here
    rsi = self.calculate_rsi(ticker)
    volume = self.calculate_volume_score(ticker)

    # Press F5 to run debugger
    # Execution pauses at breakpoint
    # Inspect variables in left panel:
    #   sentiment = 0.65
    #   rsi = 45.2
    #   volume = 1.3

    score = (0.4 * sentiment + 0.3 * rsi + 0.3 * volume)
    return score  # ← Step to here with F10
```

**Debug Console:**
```python
# While paused at breakpoint, type in debug console:
>>> sentiment
0.65
>>> rsi * 0.3
13.56
>>> self.get_sentiment('MSFT')  # Call methods!
0.72
>>> [s for s in self.tickers if self.calculate_rsi(s) < 30]
['F', 'INTC']  # Oversold stocks
```

**Debugging Strategies:**

**1. Breakpoints:**
- Regular: Pause on line
- Conditional: Pause only if condition true
- Logpoints: Print message without stopping

**2. Watch Expressions:**
Add variables to watch them change:
```
Watch:
  sentiment
  rsi
  score
  len(self.positions)  ← Updates in real-time!
```

**3. Call Stack:**
See how you got to current line:
```
Call Stack:
  calculate_composite_score() ← Current
  generate_signals()
  run_daily_trading()
  main()
```

**Priority:** MUST-HAVE

---

### 4. Database & Data Tools

#### SQLite Viewer ⭐ RECOMMENDED (FREE!)
**Purpose:** Browse and query SQLite databases visually

**Installation:**
```bash
code --install-extension alexcvzz.vscode-sqlite
```

**Usage:**
```
1. Open positions.db
2. Click SQLite Viewer icon
3. Browse tables visually
4. Run SQL queries inline
5. Export results to CSV
```

**Example:**
```sql
-- Right-click positions.db → "Open Database"

-- Trades table view:
┌──────────┬────────────┬────────┬────────┬───────┬──────────────┐
│ trade_id │ ticker     │ action │ shares │ price │ created_at   │
├──────────┼────────────┼────────┼────────┼───────┼──────────────┤
│ 1        │ AAPL       │ BUY    │ 50     │ 185.23│ 2024-01-05...│
│ 2        │ MSFT       │ BUY    │ 25     │ 398.11│ 2024-01-05...│
└──────────┴────────────┴────────┴────────┴───────┴──────────────┘

-- Run query inline:
SELECT ticker, COUNT(*) as trades, AVG(composite_score) as avg_score
FROM trades
WHERE action = 'BUY'
GROUP BY ticker
ORDER BY avg_score DESC;

-- Results appear in table below ↓
```

**QuantLab Use Cases:**
- Check today's trades without Python
- Debug database schema
- Quick analytics queries
- Export trade history to CSV for Excel analysis
- Verify sentiment cache hit rate

**Priority:** RECOMMENDED

---

#### DBCode - RECOMMENDED (FREE!)
**Purpose:** AI-powered SQL query generation and database management

**Installation:**
```bash
code --install-extension zjffun.dbcode
```

**AI Features:**
- Generate SQL from natural language
- Explain complex queries
- Optimize slow queries
- Suggest indexes
- Auto-complete table/column names

**Example:**
```
You: "Show me all winning trades from last month"

DBCode generates:
SELECT
    t1.ticker,
    t1.shares,
    t1.price as entry_price,
    t2.price as exit_price,
    (t2.price - t1.price) * t1.shares as profit,
    t1.created_at as entry_date,
    t2.created_at as exit_date
FROM trades t1
JOIN trades t2 ON t1.ticker = t2.ticker
WHERE t1.action = 'BUY'
  AND t2.action = 'SELL'
  AND t2.price > t1.price
  AND t1.created_at >= DATE('now', '-1 month')
ORDER BY profit DESC;

You: "Explain this query"

DBCode: "This self-joins the trades table to match BUY and SELL
         pairs for the same ticker, calculates profit, and filters
         for last month's winners sorted by profit."
```

**Optimization Suggestions:**
```sql
-- Your query:
SELECT * FROM trades WHERE ticker = 'AAPL';

-- DBCode suggests:
-- ⚠️ Query performance warning:
-- Consider adding index on ticker column
-- Estimated speedup: 10-100x for large tables

CREATE INDEX idx_trades_ticker ON trades(ticker);
```

**Priority:** RECOMMENDED

---

### 5. Trading/Finance Specific

#### Stocks Ticker - Nice-to-Have (FREE!)
**Purpose:** Live stock prices in VS Code status bar

**Installation:**
```bash
code --install-extension KavehAlias.vscode-stock-watcher
```

**What It Shows:**
```
Status Bar: AAPL ↑ $185.23 (+2.3%) | MSFT ↑ $398.11 (+1.8%) | SPY → $450.12 (0.0%)
                  ↑ Green if up      ↑ Red if down           ↑ Gray if flat
```

**Configuration:**
```json
{
  "stockWatcher.stocks": [
    "AAPL", "MSFT", "GOOGL", "AMZN",  // Your universe
    "SPY",   // Market benchmark
    "VIX"    // Volatility
  ],
  "stockWatcher.refreshInterval": 60000  // 1 minute
}
```

**QuantLab Use Cases:**
- Monitor positions while coding
- Quick check: "Is market moving today?"
- See VIX while developing risk models
- Track key stocks in your universe

**Priority:** Nice-to-have

---

#### TradingView Lightweight Charts - Nice-to-Have
**Purpose:** Embed interactive financial charts in notebooks/dashboards

**Not a VS Code extension, but a JavaScript library you can use in Jupyter notebooks or dashboards**

**Installation:**
```bash
pip install lightweight-charts
```

**Usage in Jupyter:**
```python
from lightweight_charts import Chart

# Create interactive chart
chart = Chart()

# Add candlestick data
df = load_prices('AAPL', '2024-01-01', '2024-11-21')
chart.set(df)

# Add indicators
rsi_line = chart.create_line()
rsi_line.set(calculate_rsi(df['close']))

# Show in notebook
chart.show()  # ← Interactive chart appears!
```

**Features:**
- Zoom, pan, crosshair
- Multiple indicators on same chart
- Sync multiple charts
- Export to PNG

**QuantLab Use Cases:**
- Visualize backtest results
- Debug indicator calculations
- Compare multiple strategies
- Present results in dashboards

**Priority:** Nice-to-have

---

### 6. Machine Learning / AI Extensions

#### PyTorch Snippets - RECOMMENDED
**Purpose:** Code snippets for PyTorch neural networks

**Installation:**
```bash
code --install-extension SBSnippets.pytorch-snippets
```

**What It Provides:**
```python
# Type: torch-model + Tab
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        # ← Cursor here

    def forward(self, x):
        # ← Implement forward pass
        return x

# Type: torch-train + Tab
def train(model, train_loader, optimizer, criterion):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
    return loss.item()
```

**QuantLab ML Use Cases:**

**1. Price Prediction Model:**
```python
# Type: torch-lstm + Tab
class PricePredictor(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        predictions = self.fc(lstm_out[:, -1, :])
        return predictions
```

**2. Sentiment Classifier:**
```python
# Type: torch-transformer + Tab
class SentimentTransformer(nn.Module):
    # Pre-filled transformer architecture
```

**Priority:** RECOMMENDED (if doing ML)

---

#### TensorBoard - RECOMMENDED
**Purpose:** Visualize ML training metrics

**Installation:**
```bash
code --install-extension ms-toolsai.tensorboard

pip install tensorboard
```

**Usage:**
```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/price_predictor')

for epoch in range(100):
    train_loss = train_epoch(model, train_loader)
    val_loss = validate_epoch(model, val_loader)

    # Log to TensorBoard
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Loss/val', val_loss, epoch)

    # Log model graph
    if epoch == 0:
        writer.add_graph(model, example_input)

writer.close()

# Open in VS Code: Cmd+Shift+P → "TensorBoard: Launch"
```

**TensorBoard Shows:**
- Loss curves over time
- Model architecture graph
- Hyperparameter comparison
- Confusion matrices
- Embedding visualizations

**QuantLab ML Use Cases:**
- Train price prediction models
- Optimize neural network hyperparameters
- Compare model architectures
- Debug vanishing/exploding gradients

**Priority:** RECOMMENDED (if doing ML)

---

#### Jupyter Notebook Renderers - RECOMMENDED
**Purpose:** Rich visualizations in notebooks

**Installation:**
```bash
code --install-extension ms-toolsai.jupyter-renderers
```

**Supports:**
- Plotly (interactive plots)
- Vega/Vega-Lite (declarative viz)
- Geo data visualizations
- 3D plots
- LaTeX math rendering

**Example:**
```python
import plotly.graph_objects as go

# Create interactive backtest chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=equity_curve.index,
    y=equity_curve.values,
    name='Strategy',
    line=dict(color='blue', width=2)
))

fig.add_trace(go.Scatter(
    x=benchmark.index,
    y=benchmark.values,
    name='S&P 500',
    line=dict(color='gray', width=1)
))

# Add drawdown regions
fig.add_vrect(
    x0='2020-03-01', x1='2020-04-01',
    fillcolor='red', opacity=0.2,
    annotation_text='COVID Crash'
)

fig.update_layout(
    title='Alpha Scout V2 Performance',
    xaxis_title='Date',
    yaxis_title='Portfolio Value ($)',
    hovermode='x unified'
)

fig.show()  # ← Shows interactive plot in VS Code!

# Zoom, pan, hover for details
# Export to PNG/HTML with buttons
```

**Priority:** RECOMMENDED

---

### 7. Testing & Quality

#### Python Test Explorer ⭐ MUST-HAVE (FREE!)
**Purpose:** Visual test runner with instant feedback

**Installation:**
```bash
# Built into Python extension
code --install-extension ms-python.python
```

**What It Provides:**
```
Test Explorer Panel:
├─ 📁 tests/
│  ├─ 📄 test_alpha_scout.py
│  │  ├─ ✅ test_calculate_rsi
│  │  ├─ ✅ test_calculate_macd
│  │  ├─ ❌ test_generate_signals  ← Click to see error
│  │  └─ ⏭️  test_backtest (skipped)
│  ├─ 📄 test_sentiment.py
│  │  ├─ ✅ test_fetch_sentiment
│  │  └─ ✅ test_cache_hit
```

**Click any test:**
- ✅ See assertion details
- ❌ Jump to failing line
- 🐛 Debug test with breakpoints
- 🔄 Re-run single test

**Example:**
```python
# tests/test_alpha_scout.py

def test_generate_signals():
    """Test signal generation returns expected tickers"""
    strategy = AlphaScoutV2(tickers=['AAPL', 'MSFT'])
    signals = strategy.generate_signals()

    assert len(signals) > 0, "Should generate at least one signal"
    assert 'ticker' in signals.columns
    assert 'composite_score' in signals.columns
    assert all(signals['composite_score'] >= 0.6)  # ← Fails!
```

**Test Explorer shows:**
```
❌ test_generate_signals
   AssertionError: assert all([0.55, 0.72, 0.68] >= 0.6)

   Expected: All scores >= 0.6
   Actual:   AAPL score = 0.55 (below threshold!)

   [Debug Test] [View Output] [Jump to Code]
```

**Settings:**
```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests",
    "-v",  // Verbose
    "--tb=short"  // Short tracebacks
  ],

  // Auto-discover tests
  "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

**QuantLab Test Structure:**
```
tests/
├── test_strategies.py       # Strategy logic tests
├── test_indicators.py       # RSI, MACD, etc.
├── test_sentiment.py        # Sentiment API tests
├── test_backtesting.py      # Backtest engine tests
├── test_paper_trader.py     # Alpaca integration tests
├── conftest.py              # pytest fixtures
└── fixtures/
    ├── sample_prices.csv
    └── sample_sentiment.json
```

**Priority:** MUST-HAVE

---

#### Coverage Gutters ⭐ RECOMMENDED (FREE!)
**Purpose:** See test coverage inline while editing

**Installation:**
```bash
code --install-extension ryanluker.vscode-coverage-gutters

pip install pytest-cov
```

**Setup:**
```bash
# Generate coverage report
pytest --cov=strategies --cov=backtesting --cov-report=xml

# Or add to pyproject.toml:
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=xml --cov-report=html"
```

**What It Shows:**
```python
# strategies/alpha_scout_v2.py

def calculate_composite_score(self, ticker: str) -> float:
    """Calculate composite score from indicators"""
    │ ← Green bar: Line covered by tests
    sentiment = self.get_sentiment(ticker)
    │ ← Green bar
    rsi = self.calculate_rsi(ticker)
    │ ← Red bar: Line NOT covered by tests!

    if rsi < 30:
    │ ← Yellow bar: Branch partially covered
        return 0.0  # Oversold, skip
    │ ← Red bar: This branch never tested!

    score = 0.4 * sentiment + 0.3 * rsi + 0.3 * volume
    │ ← Green bar
    return score
```

**Bottom Status Bar:**
```
Coverage: 73.2% | 142/194 lines | [Watch] [Report]
          ↑ Click to see detailed HTML report
```

**QuantLab Coverage Goals:**
- Strategies: 80%+ (critical path)
- Indicators: 95%+ (pure functions, easy to test)
- Backtesting: 70%+ (integration tests harder)
- Paper Trading: 60%+ (external API, harder)

**Priority:** RECOMMENDED

---

#### Snyk Security - RECOMMENDED (FREE tier)
**Purpose:** Find security vulnerabilities in dependencies

**Installation:**
```bash
code --install-extension snyk-security.snyk-vulnerability-scanner
```

**What It Does:**
```
Scanning dependencies...

⚠️ 3 vulnerabilities found:

1. CRITICAL: SQL Injection in alpaca-py 0.5.2
   Fix: Upgrade to alpaca-py >= 0.6.0

2. HIGH: Arbitrary Code Execution in pandas 1.5.0
   Fix: Upgrade to pandas >= 1.5.3

3. MEDIUM: Denial of Service in requests 2.28.0
   Fix: Upgrade to requests >= 2.31.0

[Fix All] [Ignore] [Learn More]
```

**Auto-Fix:**
Click "Fix All" → Snyk updates `requirements.txt`:
```diff
- alpaca-py==0.5.2
+ alpaca-py==0.6.0
- pandas==1.5.0
+ pandas==1.5.3
- requests==2.28.0
+ requests==2.31.0
```

**Continuous Monitoring:**
- Checks on every `pip install`
- Weekly scans in background
- GitHub PR checks (if connected)

**Cost:**
- Free: Unlimited scans for open source
- Pro: $0-25/month for private repos

**Priority:** RECOMMENDED

---

### 8. Workflow & Productivity

#### GitLens ⭐ MUST-HAVE (FREE!)
**Purpose:** Supercharge Git with blame, history, and visualization

**Installation:**
```bash
code --install-extension eamodio.gitlens
```

**Key Features:**

**1. Inline Blame:**
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    # ← Shows: "John Smith, 3 months ago: Optimized RSI calculation"
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    # ← Shows: "Claude AI, 2 weeks ago: Fixed division by zero bug"
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

**2. File History:**
```
Right-click file → "Open File History"

Shows timeline:
├─ 2024-11-21: Fix: Handle missing sentiment data
├─ 2024-11-15: Feat: Add composite score caching
├─ 2024-11-10: Refactor: Extract indicator calculations
├─ 2024-11-01: Initial commit: Alpha Scout V2
```

**3. Compare Commits:**
```
View → Command Palette → "GitLens: Compare..."

Compare:
  Before: 2024-11-01 (Initial)
  After:  2024-11-21 (Current)

Shows diff of entire file/folder
```

**4. Visualize Repo:**
```
Click "Graph" in GitLens panel

Shows commit graph:
    * 23f5e8b (HEAD -> main) Feat: Paper trading automation
    |
    * 21d2509 Fix: Compliance position limits
    |\
    | * 393595c Feature: Realism simulator
    |/
    * a917b02 Feat: Pre-flight checks
```

**QuantLab Use Cases:**
- "When did we change the RSI period from 14 to 20?"
- "Who added sentiment weighting and why?"
- "Show me all changes to AlphaScoutV2 since last month"
- "What did this function look like before the bug fix?"

**Settings:**
```json
{
  "gitlens.currentLine.enabled": true,
  "gitlens.codeLens.enabled": true,
  "gitlens.hovers.currentLine.over": "line",
  "gitlens.blame.format": "${author}, ${agoOrDate}",
  "gitlens.defaultDateFormat": "YYYY-MM-DD",
  "gitlens.advanced.messages": {
    "suppressCommitHasNoPreviousCommitWarning": true
  }
}
```

**Priority:** MUST-HAVE

---

#### Todo Tree ⭐ RECOMMENDED (FREE!)
**Purpose:** Highlight and organize TODOs/FIXMEs across codebase

**Installation:**
```bash
code --install-extension Gruntfuggly.todo-tree
```

**What It Finds:**
```python
# strategies/alpha_scout_v2.py

def calculate_composite_score(self, ticker: str) -> float:
    # TODO: Add machine learning model for sentiment
    # FIXME: RSI sometimes returns NaN for new tickers
    # HACK: Temporary workaround for missing data
    # NOTE: Weights optimized on 2020-2023 data

    sentiment = self.get_sentiment(ticker)

    # BUG: This fails when sentiment is None
    # OPTIMIZE: Cache RSI calculations (called multiple times)
```

**Todo Tree Panel:**
```
TODO TREE
├─ 📁 strategies/
│  ├─ ⚠️  TODO: Add ML model (alpha_scout_v2.py:45)
│  ├─ 🔴 FIXME: RSI NaN issue (alpha_scout_v2.py:46)
│  ├─ 🔧 HACK: Missing data workaround (alpha_scout_v2.py:47)
│  └─ 🐛 BUG: Sentiment None check (alpha_scout_v2.py:52)
├─ 📁 backtesting/
│  ├─ ⚡ OPTIMIZE: Vectorize calculations (portfolio_backtest.py:123)
│  └─ 📝 NOTE: Walk-forward window = 252 days (portfolio_backtest.py:89)
```

**Click any item → Jumps to that line**

**Custom Tags:**
```json
{
  "todo-tree.general.tags": [
    "TODO",
    "FIXME",
    "BUG",
    "HACK",
    "OPTIMIZE",
    "NOTE",
    "IDEA",
    "QUESTION",
    "RESEARCH",
    "ML"  // Custom tag for ML tasks
  ],

  "todo-tree.highlights.customHighlight": {
    "BUG": {
      "icon": "bug",
      "iconColour": "#FF0000",
      "foreground": "#FF0000"
    },
    "OPTIMIZE": {
      "icon": "zap",
      "iconColour": "#FFD700"
    },
    "ML": {
      "icon": "beaker",
      "iconColour": "#00FF00"
    }
  }
}
```

**QuantLab Workflow:**
```python
# After code review with AI:

# TODO: Implement Kelly Criterion position sizing
# RESEARCH: Compare RSI vs. Stochastic for entry signals
# ML: Train sentiment classifier on historical news
# OPTIMIZE: Parallelize sentiment API calls (currently sequential)
# BUG: Bracket orders fail when stop == entry (divide by zero)
# FIXME: Dashboard doesn't update after manual trades
```

**Priority:** RECOMMENDED

---

#### Project Manager - RECOMMENDED (FREE!)
**Purpose:** Manage multiple projects and switch quickly

**Installation:**
```bash
code --install-extension alefragnani.project-manager
```

**Setup:**
```json
{
  "projectManager.any.baseFolders": [
    "C:\\Users\\wjcor\\OneDrive\\Desktop"
  ],

  "projectManager.git.baseFolders": [
    "C:\\Users\\wjcor\\OneDrive\\Desktop"
  ]
}
```

**Projects Panel:**
```
PROJECT MANAGER
├─ 📊 QuantLab          (C:\Users\wjcor\OneDrive\Desktop\QuantLab)
├─ 🤖 Sentinel          (C:\Users\wjcor\OneDrive\Desktop\Sentinel)
├─ 📈 Backtest Research (C:\Users\wjcor\Documents\Research)
├─ 🧪 ML Experiments    (C:\Users\wjcor\Documents\ML)

[New Project] [Edit] [Open in New Window]
```

**Click any project → Instantly switch**
- Closes current workspace
- Opens selected project
- Restores previous state (open files, terminal, etc.)

**QuantLab Use Case:**
- Develop in QuantLab
- Quick switch to Sentinel for reference
- Open ML Experiments for strategy research
- Back to QuantLab without losing context

**Priority:** RECOMMENDED

---

#### Code Spell Checker - RECOMMENDED (FREE!)
**Purpose:** Catch typos in code, comments, strings

**Installation:**
```bash
code --install-extension streetsidesoftware.code-spell-checker
```

**What It Catches:**
```python
# Before:
def calcualte_sharpe_ration(returns):  # ← Wavy red underlines
    """Calulate Sharpe ratio"""  # ← Underlined
    # Caculate mean and std  # ← Underlined

# After:
def calculate_sharpe_ratio(returns):
    """Calculate Sharpe ratio"""
    # Calculate mean and std
```

**Custom Dictionary:**
```json
{
  "cSpell.words": [
    "alpaca",
    "backtesting",
    "macd",
    "rsi",
    "quantlab",
    "perplexity",
    "vectorbt",
    "sharpe",
    "sortino",
    "calmar"
  ]
}
```

**Priority:** RECOMMENDED

---

#### Bookmarks - Nice-to-Have (FREE!)
**Purpose:** Mark important lines and navigate between them

**Installation:**
```bash
code --install-extension alefragnani.Bookmarks
```

**Usage:**
```python
# strategies/alpha_scout_v2.py

def generate_signals(self):  # ← Bookmark: "Entry point"
    """Main signal generation logic"""

def calculate_composite_score(self):  # ← Bookmark: "Core scoring"
    """Where the magic happens"""

def apply_filters(self):  # ← Bookmark: "Risk filters"
    """Final safety checks"""
```

**Bookmarks Panel:**
```
BOOKMARKS
├─ alpha_scout_v2.py
│  ├─ 🔖 Entry point (line 45)
│  ├─ 🔖 Core scoring (line 89)
│  └─ 🔖 Risk filters (line 156)
```

**Keyboard Shortcuts:**
- `Cmd+Alt+K`: Toggle bookmark on current line
- `Cmd+Alt+L`: Jump to next bookmark
- `Cmd+Alt+J`: Jump to previous bookmark

**Priority:** Nice-to-have

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Priority: MUST-HAVE tools first**

**Day 1-2: AI & Code Quality**
```bash
# Install core AI extensions
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension Continue.continue

# Install code quality tools
code --install-extension charliermarsh.ruff
code --install-extension ms-python.vscode-pylance

# Configure Ruff
cat > pyproject.toml <<EOF
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
EOF

# Install in project
pip install ruff

# Test: Open any .py file, make a change, save
# → Should auto-format and organize imports
```

**Day 3-4: Testing & Git**
```bash
# Install testing tools
code --install-extension ms-python.python  # Includes test explorer

# Install Git tools
code --install-extension eamodio.gitlens

# Setup pytest
pip install pytest pytest-cov

# Create basic test structure
mkdir -p tests
cat > tests/test_alpha_scout.py <<EOF
import pytest
from strategies.alpha_scout_v2 import AlphaScoutV2

def test_calculate_rsi():
    """Test RSI calculation"""
    strategy = AlphaScoutV2(tickers=['AAPL'])
    # Add test logic
    pass

def test_generate_signals():
    """Test signal generation"""
    # Add test logic
    pass
EOF

# Configure test discovery
cat > .vscode/settings.json <<EOF
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests", "-v"]
}
EOF

# Run tests: View → Testing → Run All
```

**Day 5-7: Jupyter & Data Tools**
```bash
# Install Jupyter
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.datawrangler

# Install database tools
code --install-extension alexcvzz.vscode-sqlite

# Create research notebook
cat > research/strategy_analysis.ipynb <<EOF
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from backtesting.data_loader import load_prices\n",
    "\n",
    "# Load data\n",
    "prices = load_prices(['AAPL', 'MSFT'], '2020-01-01', '2023-12-31')\n",
    "prices.head()"
   ]
  }
 ]
}
EOF

# Test: Open notebook, run cell, see output
```

**Week 1 Checklist:**
- ✅ Copilot installed and working
- ✅ Continue.dev configured with API keys
- ✅ Ruff auto-formatting on save
- ✅ Pylance providing type hints
- ✅ Test Explorer showing all tests
- ✅ GitLens showing inline blame
- ✅ Jupyter notebooks running
- ✅ SQLite viewer showing positions.db

---

### Phase 2: Enhancement (Week 2)

**Priority: RECOMMENDED tools**

**Day 1-2: Type Checking & Documentation**
```bash
# Install type checker
code --install-extension ms-python.mypy-type-checker
pip install mypy

# Install docstring generator
code --install-extension njpwerner.autodocstring

# Configure mypy
cat >> pyproject.toml <<EOF

[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = false
check_untyped_defs = true

[[tool.mypy.overrides]]
module = ["alpaca.*", "backtesting.*"]
ignore_missing_imports = true
EOF

# Add type hints to key functions
# Use Copilot to help: Select function, ask "Add type hints"
```

**Day 3-4: Code Quality & Security**
```bash
# Install coverage
code --install-extension ryanluker.vscode-coverage-gutters
pip install pytest-cov

# Install security scanner
code --install-extension snyk-security.snyk-vulnerability-scanner

# Generate coverage report
pytest --cov=strategies --cov=backtesting --cov-report=xml

# View coverage: Cmd+Shift+P → "Coverage Gutters: Watch"

# Run security scan
# Snyk will prompt for authentication
```

**Day 5-7: Productivity Tools**
```bash
# Install workflow tools
code --install-extension Gruntfuggly.todo-tree
code --install-extension alefragnani.project-manager
code --install-extension streetsidesoftware.code-spell-checker

# Configure custom TODO tags
# Add QuantLab project to Project Manager
# Add trading terms to spell checker dictionary
```

**Week 2 Checklist:**
- ✅ Mypy checking types in background
- ✅ Docstrings auto-generating
- ✅ Coverage showing green/red bars inline
- ✅ Snyk scanning for vulnerabilities
- ✅ Todo Tree showing all TODOs
- ✅ Project Manager with QuantLab + Sentinel
- ✅ Spell checker not flagging trading terms

---

### Phase 3: Specialization (Week 3)

**Priority: ML/Trading specific tools**

**Day 1-3: Machine Learning Setup**
```bash
# Install ML tools
code --install-extension SBSnippets.pytorch-snippets
code --install-extension ms-toolsai.tensorboard
pip install torch tensorboard

# Create ML experiment structure
mkdir -p ml_experiments/
cat > ml_experiments/price_predictor.py <<EOF
import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

class LSTMPredictor(nn.Module):
    # Use snippet: torch-lstm + Tab
    pass

# Training loop with TensorBoard logging
writer = SummaryWriter('runs/lstm_v1')
# ... training code ...
EOF

# Test TensorBoard
# Cmd+Shift+P → "TensorBoard: Launch"
```

**Day 4-5: Trading Tools**
```bash
# Install market data tools
code --install-extension KavehAlias.vscode-stock-watcher

# Configure watchlist
cat >> .vscode/settings.json <<EOF
{
  "stockWatcher.stocks": [
    "AAPL", "MSFT", "GOOGL", "AMZN",
    "SPY", "VIX"
  ],
  "stockWatcher.refreshInterval": 60000
}
EOF

# Install charting library
pip install lightweight-charts

# Create interactive chart notebook
# See examples in notebook section
```

**Day 6-7: Database Enhancement**
```bash
# Install advanced DB tools
code --install-extension zjffun.dbcode

# Test AI SQL generation
# Open DBCode panel
# Type: "Show winning trades from last month"
# → Generates SQL query
```

**Week 3 Checklist:**
- ✅ PyTorch snippets working
- ✅ TensorBoard showing training curves
- ✅ Stock prices in status bar
- ✅ Interactive charts in notebooks
- ✅ DBCode generating SQL from natural language

---

### Phase 4: Advanced Workflows (Week 4)

**Priority: Multi-AI collaboration**

**Day 1-3: Multi-AI Setup**
```bash
# Already have Copilot and Continue.dev from Week 1

# Configure Continue with multiple models
cat > ~/.continue/config.json <<EOF
{
  "models": [
    {
      "title": "Claude Sonnet (Strategy)",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "apiKey": "${ANTHROPIC_API_KEY}"
    },
    {
      "title": "GPT-4 Turbo (Review)",
      "provider": "openai",
      "model": "gpt-4-turbo-preview",
      "apiKey": "${OPENAI_API_KEY}"
    },
    {
      "title": "Gemini Pro (Free)",
      "provider": "google",
      "model": "gemini-pro",
      "apiKey": "${GOOGLE_API_KEY}"
    }
  ],

  "customCommands": [
    {
      "name": "Multi-AI Review",
      "prompt": "Review this code from three perspectives:\n1. Correctness\n2. Performance\n3. Trading edge validity"
    }
  ]
}
EOF

# Test multi-model workflow:
# 1. Write code with Copilot (GPT-4o)
# 2. Review with Continue (Claude)
# 3. Get second opinion with Continue (GPT-4 Turbo)
```

**Day 4-5: Autonomous Agent Setup**
```bash
# Install Cline (autonomous coding)
code --install-extension saoudrizwan.claude-dev

# Test autonomous task:
# Open Cline chat
# Type: "Create a new momentum strategy with:
#        - 20-day moving average crossover
#        - Volume filter (1.5x average)
#        - RSI confirmation (30-70 range)
#        - Unit tests for all functions"
#
# Cline will:
# - Create strategies/momentum_v1.py
# - Implement the strategy
# - Create tests/test_momentum.py
# - Run tests
# - Ask for approval before saving
```

**Day 6-7: Custom Workflows**
```bash
# Create custom VS Code tasks for common operations
cat > .vscode/tasks.json <<EOF
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Trading Bot",
      "type": "shell",
      "command": "venv/Scripts/python.exe run_daily_trading.py",
      "problemMatcher": []
    },
    {
      "label": "Backtest All Strategies",
      "type": "shell",
      "command": "venv/Scripts/python.exe backtesting/compare_all.py",
      "problemMatcher": []
    },
    {
      "label": "Update Sentiment DB",
      "type": "shell",
      "command": "venv/Scripts/python.exe update_sentiment.py",
      "problemMatcher": []
    },
    {
      "label": "Generate Performance Report",
      "type": "shell",
      "command": "venv/Scripts/python.exe dashboard.py && venv/Scripts/python.exe send_daily_email.py",
      "problemMatcher": []
    }
  ]
}
EOF

# Run tasks: Cmd+Shift+P → "Tasks: Run Task"

# Create keyboard shortcuts for common tasks
cat > .vscode/keybindings.json <<EOF
[
  {
    "key": "cmd+shift+t",
    "command": "workbench.action.tasks.runTask",
    "args": "Run Trading Bot"
  },
  {
    "key": "cmd+shift+b",
    "command": "workbench.action.tasks.runTask",
    "args": "Backtest All Strategies"
  }
]
EOF
```

**Week 4 Checklist:**
- ✅ Continue.dev with 3+ models configured
- ✅ Multi-AI code review workflow tested
- ✅ Cline autonomous agent working
- ✅ Custom tasks for common operations
- ✅ Keyboard shortcuts for trading workflows

---

## Specific Q&A

### Q1: How exactly can you run Claude + GPT-4 simultaneously in VS Code?

**Answer: Yes, using Continue.dev with split chat panels**

**Method 1: Continue.dev Split Panels (Recommended)**

1. Install Continue.dev
2. Configure multiple models in `~/.continue/config.json`
3. Open two Continue chat panels (View → split editor)
4. Select different model in each panel
5. Ask same question to both, compare answers

**Method 2: GitHub Copilot + Continue.dev**

1. Use Copilot for inline autocomplete (GPT-4o)
2. Use Continue for chat/review (Claude)
3. Both running simultaneously, different purposes

**Method 3: Cursor IDE Alternative**

- Cursor has built-in multi-model chat
- But costs $20-200/month
- VS Code + Continue is FREE and more flexible

**Real Workflow Example:**

```
Window Layout:
┌─────────────────┬─────────────────┐
│                 │                 │
│   Editor        │  Continue       │
│   (your code)   │  (Claude)       │
│                 │                 │
├─────────────────┼─────────────────┤
│                 │                 │
│   Terminal      │  Continue       │
│   (tests)       │  (GPT-4)        │
│                 │                 │
└─────────────────┴─────────────────┘

You type code → Copilot suggests completions
You select code → Ask Claude to review
Claude suggests changes → Ask GPT-4 for second opinion
GPT-4 agrees/disagrees → You decide which advice to take
```

**Cost:**
- Continue.dev extension: FREE
- API usage: ~$2-5/month for moderate use
- GitHub Copilot free tier: 2,000 completions/month
- Total: $0-10/month

---

### Q2: What's the best setup for multi-AI code review workflows?

**Answer: Continue.dev with custom review prompts**

**Recommended Setup:**

```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "Claude 3.5 Sonnet",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "apiKey": "YOUR_KEY"
    },
    {
      "title": "GPT-4 Turbo",
      "provider": "openai",
      "model": "gpt-4-turbo-preview",
      "apiKey": "YOUR_KEY"
    }
  ],

  "customCommands": [
    {
      "name": "Trading Strategy Review",
      "prompt": "Review this trading strategy code for:\n\n1. **Edge Validity**: Does the logic make financial sense? Are there any logical flaws in the trading edge?\n2. **Risk Management**: Are position sizing, stops, and limits appropriate?\n3. **Implementation Bugs**: Any off-by-one errors, lookahead bias, or calculation mistakes?\n4. **Performance**: Any obvious optimizations (vectorization, caching, etc.)?\n5. **Robustness**: Will this work across different market conditions?\n\nProvide specific line-by-line feedback."
    },
    {
      "name": "Backtest Validation",
      "prompt": "Review this backtest code for common pitfalls:\n\n1. **Lookahead Bias**: Does it use future data to make past decisions?\n2. **Survivorship Bias**: Does it only test on stocks that still exist today?\n3. **Overfitting**: Are there too many parameters optimized on too little data?\n4. **Transaction Costs**: Are slippage and commissions realistic?\n5. **Market Impact**: Does it assume infinite liquidity?\n\nExplain any issues clearly."
    }
  ]
}
```

**Workflow:**

**Step 1: Initial Implementation with Claude**
```
You: "Create a mean reversion strategy using Bollinger Bands"
Claude: [Writes code]
```

**Step 2: Self-Review with Claude**
```
You: /Trading Strategy Review
Claude:
"Line 45: The entry condition uses close < lower_band, but should
         wait for confirmation (e.g., RSI < 30) to avoid catching
         falling knives.

Line 67: Position sizing uses fixed $10k per trade, but should
         scale based on volatility (use ATR-based sizing).

Line 89: No maximum holding period. Mean reversion trades should
         exit after N days if target not hit (time stop)."
```

**Step 3: Second Opinion from GPT-4**
```
You: [Paste code] "GPT-4, Claude suggested these changes. What do you think?"
GPT-4:
"Claude's suggestions are solid. I'd add:

1. Line 45: Also check volume - mean reversion works better on
   low-volume selloffs (indicates overreaction vs. fundamental change)

2. Line 67: Claude's right about ATR sizing. Use 1-2 ATR position size.

3. Line 89: Agree on time stop. I suggest 5 days max for mean reversion.

Additional point Claude missed:
Line 102: The backtest doesn't account for overnight gaps. Mean reversion
          can gap against you - add max gap filter (e.g., skip if gap > 3%)."
```

**Step 4: Consensus Implementation**
```
You implement:
✅ Claude's RSI confirmation
✅ Claude's ATR-based sizing
✅ Claude's time stop
✅ GPT-4's volume filter
✅ GPT-4's gap filter
```

**Step 5: Final Validation with Gemini (Free)**
```
You: [Paste updated code] "Final review?"
Gemini:
"Code looks good now. All major issues addressed.

Minor suggestions:
- Add logging for why trades are skipped (helps debugging)
- Use constants for magic numbers (30, 70, 5 days, etc.)
- Add docstrings to main functions

Otherwise ready for backtesting!"
```

**Result: 3 AIs collaborated to catch issues you might have missed!**

---

### Q3: Best tools for backtesting strategy visualization?

**Answer: Combination of Plotly in Jupyter + TensorBoard for comparisons**

**For Individual Strategy Analysis: Plotly in Jupyter**

```python
# research/backtest_visualization.ipynb

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def visualize_backtest(results):
    """Create interactive backtest dashboard"""

    # Create subplot layout
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=(
            'Equity Curve vs Benchmark',
            'Drawdown',
            'Monthly Returns Heatmap',
            'Win/Loss Distribution',
            'Trade Duration',
            'Entry/Exit Timing',
            'Rolling Sharpe (252-day)',
            'Position Sizing'
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}]
        ],
        vertical_spacing=0.08,
        horizontal_spacing=0.1
    )

    # 1. Equity Curve
    fig.add_trace(
        go.Scatter(
            x=results['equity_curve'].index,
            y=results['equity_curve'],
            name='Strategy',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=results['benchmark'].index,
            y=results['benchmark'],
            name='S&P 500',
            line=dict(color='gray', width=1, dash='dash')
        ),
        row=1, col=1
    )

    # 2. Drawdown
    drawdown = (results['equity_curve'] / results['equity_curve'].cummax() - 1) * 100
    fig.add_trace(
        go.Scatter(
            x=drawdown.index,
            y=drawdown,
            fill='tozeroy',
            name='Drawdown',
            line=dict(color='red')
        ),
        row=1, col=2
    )

    # 3. Monthly Returns Heatmap
    monthly_returns = results['returns'].resample('M').sum() * 100
    monthly_pivot = monthly_returns.to_frame().pivot_table(
        index=monthly_returns.index.month,
        columns=monthly_returns.index.year,
        values='returns'
    )

    fig.add_trace(
        go.Heatmap(
            z=monthly_pivot.values,
            x=monthly_pivot.columns,
            y=['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec'],
            colorscale='RdYlGn',
            zmid=0,
            text=monthly_pivot.values,
            texttemplate='%{text:.1f}%',
            textfont={"size": 10}
        ),
        row=2, col=1
    )

    # 4. Win/Loss Distribution
    trades = results['trades']
    wins = trades[trades['pnl'] > 0]['pnl']
    losses = trades[trades['pnl'] <= 0]['pnl']

    fig.add_trace(
        go.Histogram(
            x=wins,
            name='Wins',
            marker_color='green',
            opacity=0.7,
            nbinsx=30
        ),
        row=2, col=2
    )

    fig.add_trace(
        go.Histogram(
            x=losses,
            name='Losses',
            marker_color='red',
            opacity=0.7,
            nbinsx=30
        ),
        row=2, col=2
    )

    # 5. Trade Duration
    fig.add_trace(
        go.Box(
            y=trades['duration_days'],
            name='Duration',
            marker_color='blue'
        ),
        row=3, col=1
    )

    # 6. Entry/Exit Timing (hour of day)
    fig.add_trace(
        go.Histogram(
            x=trades['entry_time'].dt.hour,
            name='Entry Hour',
            marker_color='green',
            opacity=0.7
        ),
        row=3, col=2
    )

    # 7. Rolling Sharpe
    rolling_sharpe = results['returns'].rolling(252).apply(
        lambda x: x.mean() / x.std() * np.sqrt(252)
    )

    fig.add_trace(
        go.Scatter(
            x=rolling_sharpe.index,
            y=rolling_sharpe,
            name='Rolling Sharpe',
            line=dict(color='purple')
        ),
        row=4, col=1
    )

    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=4, col=1)

    # 8. Position Sizing Over Time
    fig.add_trace(
        go.Scatter(
            x=trades['entry_date'],
            y=trades['position_size'],
            mode='markers',
            name='Position Size',
            marker=dict(
                color=trades['pnl'],
                colorscale='RdYlGn',
                size=10,
                showscale=True
            )
        ),
        row=4, col=2
    )

    # Update layout
    fig.update_layout(
        height=1600,
        width=1400,
        title_text=f"Backtest Dashboard: {results['strategy_name']}",
        showlegend=True,
        hovermode='x unified'
    )

    # Add metrics annotation
    metrics_text = f"""
    Sharpe: {results['sharpe']:.2f} | Sortino: {results['sortino']:.2f}
    Max DD: {results['max_drawdown']:.1f}% | Calmar: {results['calmar']:.2f}
    Win Rate: {results['win_rate']*100:.1f}% | Profit Factor: {results['profit_factor']:.2f}
    Total Trades: {len(trades)} | Avg Duration: {trades['duration_days'].mean():.1f} days
    """

    fig.add_annotation(
        text=metrics_text,
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=12),
        align="center"
    )

    return fig

# Usage:
results = backtest_strategy(AlphaScoutV2, tickers, start, end)
fig = visualize_backtest(results)
fig.show()  # Interactive in VS Code!

# Export
fig.write_html('backtest_report.html')
fig.write_image('backtest_report.png')
```

**For Multi-Strategy Comparison: Custom Dashboard**

```python
# dashboard/strategy_comparison.py

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Strategy Comparison")

# Load all strategy results
strategies = {
    'Alpha Scout V1': load_backtest('alpha_scout_v1.pkl'),
    'Alpha Scout V2': load_backtest('alpha_scout_v2.pkl'),
    'Alpha Scout V3': load_backtest('alpha_scout_v3.pkl'),
    'Momentum Only': load_backtest('momentum_only.pkl'),
    'Mean Reversion': load_backtest('mean_reversion.pkl')
}

# Sidebar: Strategy selection
selected = st.sidebar.multiselect(
    'Select strategies to compare:',
    list(strategies.keys()),
    default=list(strategies.keys())
)

# Main area: Comparison charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Equity Curves")
    fig = go.Figure()

    for name in selected:
        fig.add_trace(go.Scatter(
            x=strategies[name]['equity'].index,
            y=strategies[name]['equity'],
            name=name,
            mode='lines'
        ))

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Risk Metrics")

    metrics_df = pd.DataFrame({
        name: {
            'Sharpe': strategies[name]['sharpe'],
            'Sortino': strategies[name]['sortino'],
            'Max DD': strategies[name]['max_dd'],
            'Calmar': strategies[name]['calmar']
        }
        for name in selected
    }).T

    st.dataframe(metrics_df.style.highlight_max(axis=0, color='lightgreen'))

# Run: streamlit run dashboard/strategy_comparison.py
```

**For ML Model Training: TensorBoard**

```python
# ml_experiments/train_predictor.py

from torch.utils.tensorboard import SummaryWriter
import torch
import torch.nn as nn

writer = SummaryWriter('runs/lstm_v1')

for epoch in range(100):
    # Train
    model.train()
    train_loss = 0
    for batch in train_loader:
        loss = train_step(model, batch, optimizer)
        train_loss += loss

    train_loss /= len(train_loader)

    # Validate
    model.eval()
    val_loss = validate(model, val_loader)
    val_sharpe = backtest_predictions(model, val_data)

    # Log to TensorBoard
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Loss/val', val_loss, epoch)
    writer.add_scalar('Metrics/sharpe', val_sharpe, epoch)

    # Log model weights histogram
    for name, param in model.named_parameters():
        writer.add_histogram(f'weights/{name}', param, epoch)

    # Log sample predictions
    if epoch % 10 == 0:
        fig = plot_predictions(model, val_data[:100])
        writer.add_figure('predictions', fig, epoch)

writer.close()

# View in VS Code: Cmd+Shift+P → "TensorBoard: Launch"
```

**Best Combo for QuantLab:**

1. **Development/Research**: Plotly in Jupyter notebooks
   - Interactive exploration
   - Drill down into specific trades
   - Export static images for reports

2. **Strategy Comparison**: Custom Streamlit dashboard
   - Compare multiple strategies side-by-side
   - Filter by date ranges
   - Calculate correlation between strategies

3. **ML Training**: TensorBoard
   - Track model training progress
   - Compare different architectures
   - Debug training issues

---

### Q4: ML/AI tools that could enhance trading strategy development?

**Answer: PyTorch for prediction models + Optuna for hyperparameter optimization + SHAP for explainability**

**Tool 1: PyTorch for Neural Network Strategies**

**Use Case: Price/Return Prediction**

```python
# ml_experiments/price_predictor.py

import torch
import torch.nn as nn
import pandas as pd
import numpy as np

class LSTMPredictor(nn.Module):
    """Predict next-day returns using LSTM"""

    def __init__(self, input_size=10, hidden_size=64, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x shape: (batch, sequence_length, features)
        lstm_out, _ = self.lstm(x)
        # Take last timestep
        last_hidden = lstm_out[:, -1, :]
        prediction = self.fc(last_hidden)
        return prediction

# Features: OHLCV + indicators
def create_features(df):
    """Create feature matrix for ML model"""
    features = pd.DataFrame(index=df.index)

    # Price features (normalized)
    features['returns'] = df['close'].pct_change()
    features['high_low_ratio'] = df['high'] / df['low']
    features['close_open_ratio'] = df['close'] / df['open']

    # Volume features
    features['volume_ratio'] = df['volume'] / df['volume'].rolling(20).mean()

    # Technical indicators
    features['rsi'] = calculate_rsi(df['close'])
    features['macd'] = calculate_macd(df['close'])['macd']
    features['bb_position'] = (df['close'] - df['close'].rolling(20).mean()) / (2 * df['close'].rolling(20).std())

    # Lagged features
    for lag in [1, 2, 3, 5]:
        features[f'return_lag_{lag}'] = features['returns'].shift(lag)

    return features.dropna()

# Training loop
def train_model(model, train_loader, val_loader, epochs=100):
    """Train LSTM predictor"""
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

    best_val_loss = float('inf')

    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            predictions = model(X_batch)
            loss = criterion(predictions, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # Validate
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                predictions = model(X_batch)
                loss = criterion(predictions, y_batch)
                val_loss += loss.item()

        val_loss /= len(val_loader)
        scheduler.step(val_loss)

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'models/lstm_best.pth')

        print(f'Epoch {epoch}: Train Loss={train_loss/len(train_loader):.4f}, Val Loss={val_loss:.4f}')

    return model

# Use predictions in strategy
class MLEnhancedStrategy:
    """Trading strategy that uses ML predictions"""

    def __init__(self, model_path='models/lstm_best.pth'):
        self.model = LSTMPredictor()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def generate_signals(self, data):
        """Generate trading signals using ML predictions"""
        features = create_features(data)

        # Get ML prediction for next day
        X = torch.FloatTensor(features.values[-20:]).unsqueeze(0)  # Last 20 days
        with torch.no_grad():
            predicted_return = self.model(X).item()

        # Combine with traditional signals
        rsi = features['rsi'].iloc[-1]
        macd = features['macd'].iloc[-1]

        # Buy signal: ML predicts positive return AND traditional indicators confirm
        if predicted_return > 0.005 and rsi < 70 and macd > 0:
            return 'BUY'

        # Sell signal: ML predicts negative return OR traditional indicators warn
        elif predicted_return < -0.005 or rsi > 80 or macd < 0:
            return 'SELL'

        return 'HOLD'
```

**Tool 2: Optuna for Hyperparameter Optimization**

```python
# ml_experiments/optimize_strategy.py

import optuna
from backtesting import Backtest

def objective(trial):
    """Optimization objective for strategy parameters"""

    # Suggest hyperparameters
    params = {
        'rsi_lower': trial.suggest_int('rsi_lower', 20, 40),
        'rsi_upper': trial.suggest_int('rsi_upper', 60, 80),
        'rsi_exit': trial.suggest_int('rsi_exit', 30, 50),
        'sentiment_weight': trial.suggest_float('sentiment_weight', 0.2, 0.6),
        'volume_threshold': trial.suggest_float('volume_threshold', 1.0, 2.0),
        'stop_loss_pct': trial.suggest_float('stop_loss_pct', 0.05, 0.15),
        'take_profit_pct': trial.suggest_float('take_profit_pct', 0.10, 0.30),
    }

    # Create strategy with these params
    class ParameterizedStrategy(AlphaScoutV2):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.params = params

    # Backtest
    bt = Backtest(data, ParameterizedStrategy, cash=100000)
    stats = bt.run()

    # Optimize for Sharpe ratio (or custom metric)
    sharpe = stats['Sharpe Ratio']

    # Add constraints (penalize if violated)
    max_dd = abs(stats['Max. Drawdown [%]'])
    if max_dd > 30:  # Don't allow >30% drawdown
        sharpe -= (max_dd - 30) * 0.1  # Penalty

    win_rate = stats['Win Rate [%]']
    if win_rate < 45:  # Want at least 45% win rate
        sharpe -= (45 - win_rate) * 0.05

    return sharpe

# Run optimization
study = optuna.create_study(
    direction='maximize',
    sampler=optuna.samplers.TPESampler(seed=42)
)

study.optimize(objective, n_trials=200, show_progress_bar=True)

# Best parameters
print("Best parameters:", study.best_params)
print("Best Sharpe:", study.best_value)

# Visualize optimization
from optuna.visualization import plot_optimization_history, plot_param_importances

plot_optimization_history(study).show()
plot_param_importances(study).show()

# VS Code extension for Optuna:
# Install: code --install-extension optuna.optuna-dashboard
# Launch: optuna-dashboard sqlite:///optuna_study.db
```

**Tool 3: SHAP for Model Explainability**

```python
# ml_experiments/explain_model.py

import shap
import matplotlib.pyplot as plt

# Load trained model
model = LSTMPredictor()
model.load_state_dict(torch.load('models/lstm_best.pth'))
model.eval()

# Create SHAP explainer
# For PyTorch, use DeepExplainer
background = torch.FloatTensor(X_train[:100])  # Background dataset
explainer = shap.DeepExplainer(model, background)

# Explain predictions
test_sample = torch.FloatTensor(X_test[:10])
shap_values = explainer.shap_values(test_sample)

# Visualize feature importance
feature_names = ['returns', 'rsi', 'macd', 'volume_ratio', 'bb_position',
                 'return_lag_1', 'return_lag_2', 'return_lag_3']

shap.summary_plot(shap_values, test_sample.numpy(), feature_names=feature_names)

# Shows which features drive predictions:
# - Red: High feature value
# - Blue: Low feature value
# - X-axis: Impact on prediction
#
# Example output:
# rsi             ●●●●●●●●○○○○○○ (high RSI → bearish prediction)
# macd            ●●●●○○○○○○○○○○ (high MACD → bullish prediction)
# volume_ratio    ●●○○○○○○○○○○○○ (moderate impact)
# ...
```

**Tool 4: AutoML with AutoGluon**

```python
# ml_experiments/autogluon_strategy.py

from autogluon.tabular import TabularPredictor

# Prepare data
features = create_features(price_data)
features['target'] = features['returns'].shift(-1)  # Next day return
features = features.dropna()

# Split
train = features.iloc[:int(len(features)*0.8)]
test = features.iloc[int(len(features)*0.8):]

# AutoML - automatically tries different models
predictor = TabularPredictor(label='target').fit(
    train_data=train,
    time_limit=3600,  # 1 hour
    presets='best_quality'
)

# AutoGluon tries:
# - LightGBM
# - XGBoost
# - CatBoost
# - Neural networks
# - Ensemble combinations

# Best model automatically selected
leaderboard = predictor.leaderboard(test)
print(leaderboard)

# Use in strategy
def generate_signals_autogluon(data):
    features = create_features(data)
    prediction = predictor.predict(features.iloc[[-1]])

    if prediction[0] > 0.01:  # Predict >1% gain
        return 'BUY'
    elif prediction[0] < -0.01:
        return 'SELL'
    return 'HOLD'
```

**Best ML Workflow for QuantLab:**

1. **Feature Engineering**: Create rich feature set from price data
2. **Model Training**: Use PyTorch for complex models (LSTM, Transformer)
3. **Hyperparameter Tuning**: Use Optuna to find best params
4. **Explainability**: Use SHAP to understand what drives predictions
5. **Validation**: Walk-forward backtest with ML predictions
6. **Deployment**: Integrate ML predictions into existing Alpha Scout framework

**VS Code Setup for ML:**
```bash
code --install-extension ms-toolsai.jupyter
code --install-extension SBSnippets.pytorch-snippets
code --install-extension ms-toolsai.tensorboard

pip install torch optuna shap autogluon
```

---

### Q5: Tools for comparing strategy performance metrics?

**Answer: Custom analytics with pandas + Plotly + Streamlit dashboard**

**Create Comprehensive Strategy Comparison System:**

```python
# analytics/strategy_comparison.py

import pandas as pd
import numpy as np
from typing import Dict, List
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class StrategyComparison:
    """Compare multiple strategies across various metrics"""

    def __init__(self, strategies: Dict[str, pd.DataFrame]):
        """
        Args:
            strategies: Dict mapping strategy name to equity curve DataFrame
        """
        self.strategies = strategies
        self.metrics = {}
        self.calculate_all_metrics()

    def calculate_all_metrics(self):
        """Calculate comprehensive metrics for all strategies"""
        for name, equity in self.strategies.items():
            returns = equity.pct_change().dropna()

            self.metrics[name] = {
                # Return metrics
                'Total Return': (equity.iloc[-1] / equity.iloc[0] - 1) * 100,
                'CAGR': self._calculate_cagr(equity),
                'Ann. Volatility': returns.std() * np.sqrt(252) * 100,

                # Risk-adjusted returns
                'Sharpe Ratio': self._calculate_sharpe(returns),
                'Sortino Ratio': self._calculate_sortino(returns),
                'Calmar Ratio': self._calculate_calmar(equity),

                # Drawdown metrics
                'Max Drawdown': self._calculate_max_dd(equity),
                'Avg Drawdown': self._calculate_avg_dd(equity),
                'Max DD Duration': self._calculate_max_dd_duration(equity),

                # Trade metrics (if available)
                'Win Rate': self._calculate_win_rate(name),
                'Profit Factor': self._calculate_profit_factor(name),
                'Avg Win / Avg Loss': self._calculate_win_loss_ratio(name),

                # Consistency metrics
                'Monthly Win Rate': self._calculate_monthly_win_rate(returns),
                'Best Month': returns.resample('M').sum().max() * 100,
                'Worst Month': returns.resample('M').sum().min() * 100,

                # Tail risk
                'VaR (95%)': np.percentile(returns, 5) * 100,
                'CVaR (95%)': returns[returns <= np.percentile(returns, 5)].mean() * 100,

                # Statistical
                'Skewness': returns.skew(),
                'Kurtosis': returns.kurtosis(),
                'Daily Sharpe': returns.mean() / returns.std() * np.sqrt(252)
            }

    def compare_table(self) -> pd.DataFrame:
        """Create comparison table"""
        df = pd.DataFrame(self.metrics).T

        # Round for readability
        df = df.round(2)

        # Add ranking columns
        for col in ['Sharpe Ratio', 'CAGR', 'Sortino Ratio']:
            df[f'{col} Rank'] = df[col].rank(ascending=False).astype(int)

        return df

    def visualize_comparison(self) -> go.Figure:
        """Create comprehensive comparison dashboard"""

        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=(
                'Equity Curves',
                'Risk-Adjusted Returns',
                'Drawdown Comparison',
                'Monthly Return Distribution',
                'Win Rate vs Sharpe',
                'Return vs Volatility',
                'Rolling Sharpe (6M)',
                'Correlation Matrix',
                'Underwater Plot'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "bar"}, {"type": "scatter"}],
                [{"type": "box"}, {"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "heatmap"}, {"type": "scatter"}]
            ]
        )

        # 1. Equity curves (normalized to 100)
        for name, equity in self.strategies.items():
            normalized = (equity / equity.iloc[0]) * 100
            fig.add_trace(
                go.Scatter(x=equity.index, y=normalized, name=name, mode='lines'),
                row=1, col=1
            )

        # 2. Risk-adjusted returns (bar chart)
        metrics_df = pd.DataFrame(self.metrics).T
        fig.add_trace(
            go.Bar(x=metrics_df.index, y=metrics_df['Sharpe Ratio'], name='Sharpe'),
            row=1, col=2
        )

        # 3. Drawdown comparison
        for name, equity in self.strategies.items():
            dd = (equity / equity.cummax() - 1) * 100
            fig.add_trace(
                go.Scatter(x=equity.index, y=dd, name=name, fill='tozeroy'),
                row=1, col=3
            )

        # 4. Monthly return distribution (box plot)
        for name, equity in self.strategies.items():
            returns = equity.pct_change().dropna()
            monthly = returns.resample('M').sum() * 100
            fig.add_trace(
                go.Box(y=monthly, name=name),
                row=2, col=1
            )

        # 5. Win Rate vs Sharpe (scatter)
        fig.add_trace(
            go.Scatter(
                x=metrics_df['Win Rate'],
                y=metrics_df['Sharpe Ratio'],
                mode='markers+text',
                text=metrics_df.index,
                textposition='top center',
                marker=dict(size=15)
            ),
            row=2, col=2
        )

        # 6. Return vs Volatility (efficient frontier)
        fig.add_trace(
            go.Scatter(
                x=metrics_df['Ann. Volatility'],
                y=metrics_df['CAGR'],
                mode='markers+text',
                text=metrics_df.index,
                textposition='top center',
                marker=dict(size=15, color=metrics_df['Sharpe Ratio'], colorscale='Viridis', showscale=True)
            ),
            row=2, col=3
        )

        # 7. Rolling Sharpe
        for name, equity in self.strategies.items():
            returns = equity.pct_change().dropna()
            rolling = returns.rolling(126).apply(lambda x: x.mean() / x.std() * np.sqrt(252))
            fig.add_trace(
                go.Scatter(x=returns.index, y=rolling, name=name),
                row=3, col=1
            )

        # 8. Correlation matrix
        all_returns = pd.DataFrame({
            name: equity.pct_change().dropna()
            for name, equity in self.strategies.items()
        })
        corr = all_returns.corr()

        fig.add_trace(
            go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                colorscale='RdBu',
                zmid=0,
                text=corr.values,
                texttemplate='%{text:.2f}'
            ),
            row=3, col=2
        )

        # 9. Underwater plot (time in drawdown)
        for name, equity in self.strategies.items():
            underwater = (equity / equity.cummax() - 1) * 100
            fig.add_trace(
                go.Scatter(x=equity.index, y=underwater, name=name, fill='tozeroy'),
                row=3, col=3
            )

        fig.update_layout(height=1200, width=1800, showlegend=True)
        return fig

    def statistical_tests(self) -> pd.DataFrame:
        """Run statistical tests to compare strategies"""
        from scipy import stats

        results = []

        # Pairwise t-tests
        strategies_list = list(self.strategies.keys())
        for i, name1 in enumerate(strategies_list):
            for name2 in strategies_list[i+1:]:
                returns1 = self.strategies[name1].pct_change().dropna()
                returns2 = self.strategies[name2].pct_change().dropna()

                # Paired t-test
                t_stat, p_value = stats.ttest_rel(returns1, returns2)

                results.append({
                    'Strategy 1': name1,
                    'Strategy 2': name2,
                    't-statistic': t_stat,
                    'p-value': p_value,
                    'Significant (5%)': 'Yes' if p_value < 0.05 else 'No',
                    'Winner': name1 if t_stat > 0 else name2
                })

        return pd.DataFrame(results)

# Usage:
strategies = {
    'Alpha Scout V1': load_equity_curve('v1.csv'),
    'Alpha Scout V2': load_equity_curve('v2.csv'),
    'Alpha Scout V3': load_equity_curve('v3.csv'),
    'Momentum Only': load_equity_curve('momentum.csv'),
}

comparison = StrategyComparison(strategies)

# Get metrics table
print(comparison.compare_table())

# Visualize
fig = comparison.visualize_comparison()
fig.show()

# Statistical significance
print(comparison.statistical_tests())
```

**Interactive Streamlit Dashboard:**

```python
# dashboard/strategy_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Strategy Comparison Dashboard")

# Load strategies
@st.cache_data
def load_all_strategies():
    return {
        'Alpha Scout V1': pd.read_csv('results/v1_equity.csv', index_col=0, parse_dates=True),
        'Alpha Scout V2': pd.read_csv('results/v2_equity.csv', index_col=0, parse_dates=True),
        'Alpha Scout V3': pd.read_csv('results/v3_equity.csv', index_col=0, parse_dates=True),
        'Momentum': pd.read_csv('results/momentum_equity.csv', index_col=0, parse_dates=True),
    }

strategies = load_all_strategies()
comparison = StrategyComparison(strategies)

# Sidebar: Filters
st.sidebar.header("Filters")
selected = st.sidebar.multiselect(
    'Select Strategies',
    list(strategies.keys()),
    default=list(strategies.keys())
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(strategies[selected[0]].index[0], strategies[selected[0]].index[-1])
)

# Main area
st.title("🎯 Strategy Performance Dashboard")

# Metrics cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    best_sharpe = comparison.metrics_df['Sharpe Ratio'].idxmax()
    st.metric(
        "Best Sharpe",
        f"{comparison.metrics_df.loc[best_sharpe, 'Sharpe Ratio']:.2f}",
        best_sharpe
    )

with col2:
    best_return = comparison.metrics_df['Total Return'].idxmax()
    st.metric(
        "Best Return",
        f"{comparison.metrics_df.loc[best_return, 'Total Return']:.1f}%",
        best_return
    )

with col3:
    lowest_dd = comparison.metrics_df['Max Drawdown'].idxmax()  # Least negative
    st.metric(
        "Lowest Max DD",
        f"{comparison.metrics_df.loc[lowest_dd, 'Max Drawdown']:.1f}%",
        lowest_dd
    )

with col4:
    best_calmar = comparison.metrics_df['Calmar Ratio'].idxmax()
    st.metric(
        "Best Calmar",
        f"{comparison.metrics_df.loc[best_calmar, 'Calmar Ratio']:.2f}",
        best_calmar
    )

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Performance", "⚖️ Risk", "🔬 Analysis"])

with tab1:
    st.subheader("Performance Metrics")
    st.dataframe(
        comparison.compare_table().style.highlight_max(axis=0, color='lightgreen')
    )

with tab2:
    st.plotly_chart(comparison.visualize_comparison(), use_container_width=True)

with tab3:
    # Risk analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Drawdown Analysis")
        # Drawdown plot

    with col2:
        st.subheader("VaR/CVaR")
        # VaR plot

with tab4:
    st.subheader("Statistical Significance Tests")
    st.dataframe(comparison.statistical_tests())

# Run: streamlit run dashboard/strategy_dashboard.py
```

**Priority for QuantLab:**
1. Create `analytics/strategy_comparison.py` module
2. Run comparisons in Jupyter for exploration
3. Build Streamlit dashboard for sharing results
4. Use VS Code extensions (Data Wrangler, Plotly renderer) for interactivity

---

## Cost Analysis

### Free Setup (Fully Functional)

```
GitHub Copilot Free Tier:        $0/month
  - 2,000 completions/month
  - 50 chat messages/month
  - Both GPT-4o + Claude 3.5

Continue.dev:                     $0/month (extension)
  + Claude API usage:             ~$2-5/month
  + GPT-4 API usage:              ~$2-5/month

Ruff:                             $0
Pylance:                          $0
Jupyter:                          $0
Data Wrangler:                    $0
GitLens:                          $0
Python Test Explorer:             $0
Todo Tree:                        $0
SQLite Viewer:                    $0
DBCode:                           $0
Coverage Gutters:                 $0
Snyk (free tier):                 $0

Total: $4-10/month
```

### Recommended Setup (Best Value)

```
GitHub Copilot Pro:               $10/month
  - Unlimited completions
  - Unlimited chat
  - Priority access
  - Faster responses

Continue.dev:                     $0/month (extension)
  + API usage (moderate):         ~$5/month

Cline (Claude Dev):               $0/month (extension)
  + API usage:                    ~$3/month

All free extensions:              $0

Total: $18/month
```

### Premium Setup (If Budget Allows)

```
GitHub Copilot Pro:               $10/month
Cursor IDE (alternative):         $20/month (not recommended over VS Code for quant)
Continue.dev + Heavy API:         ~$15/month
Snyk Pro:                         $25/month
PyCharm Professional:             $9/month (not needed with VS Code setup)

Total: $35-55/month
```

**Recommendation for QuantLab: Start with Free Setup**
- Test GitHub Copilot free tier
- Use Continue with pay-as-you-go APIs
- Upgrade to Copilot Pro ($10) if you hit limits
- Total cost: $0-10/month is plenty for serious development

---

## Summary & Next Steps

### What We Found

**1. Multi-AI Collaboration is Real**
- GitHub Copilot FREE tier has both GPT-4o AND Claude 3.5
- Continue.dev lets you run unlimited models simultaneously
- You CAN have AIs review each other's code (as seen in YouTube)

**2. Major 2024-2025 Improvements**
- Ruff is 150-200x faster than old tools
- Native test coverage visualization
- GitHub Copilot now has free tier
- Data Wrangler for visual DataFrame editing

**3. VS Code Beats Cursor for Quant Trading**
- Better Jupyter integration
- More customizable
- Costs $0-10 vs $20-200/month
- Larger extension ecosystem

### Recommended Installation Order

**Week 1: Core Tools**
1. GitHub Copilot (free)
2. Continue.dev
3. Ruff + Pylance
4. Jupyter + Data Wrangler
5. GitLens
6. Test Explorer

**Week 2: Quality & Productivity**
7. Mypy
8. Coverage Gutters
9. autoDocstring
10. Todo Tree
11. SQLite Viewer

**Week 3: Specialization**
12. PyTorch snippets (if doing ML)
13. TensorBoard
14. DBCode
15. Stocks Ticker

**Week 4: Advanced**
16. Cline (autonomous agent)
17. Multi-AI workflow setup
18. Custom tasks/shortcuts
19. Streamlit dashboard

### Try This First

**Immediate Action (5 minutes):**
```bash
# Install GitHub Copilot (free tier)
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat

# Restart VS Code
# Sign in with GitHub account
# Try it: Open any Python file, start typing a function
# Copilot will suggest completions!
```

**Then (15 minutes):**
```bash
# Install Continue.dev
code --install-extension Continue.continue

# Configure with your API keys
# Try multi-AI review on existing QuantLab code
```

**This Weekend:**
- Read full guide (saved to Sentinel folder)
- Follow Week 1 setup
- Test Copilot + Continue on Alpha Scout V2 code
- Report back what works best!

All documentation saved to:
`C:\Users\wjcor\OneDrive\Desktop\Sentinel\VS_CODE_EXTENSIONS_COMPREHENSIVE_GUIDE.md`
