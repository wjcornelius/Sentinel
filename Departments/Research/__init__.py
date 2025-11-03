"""
Research Department - Programmatic Technical Analysis & Adaptive Filtering

Responsibilities:
- Load ticker universe (S&P 500 + Nasdaq 100 = ~515 stocks)
- Adaptive filtering to find ~50 buy candidates
- Programmatic technical analysis (NO AI)
- Alpaca integration for current holdings
- 16-hour cache for price/volume data
- Output: ~110 stocks (50 candidates + 60 holdings)
"""

from .research_department import ResearchDepartment

__all__ = ['ResearchDepartment']
