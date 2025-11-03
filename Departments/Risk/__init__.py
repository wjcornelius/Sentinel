"""
Risk Department v2.1 - Advisory Risk Assessment (Swing Trading)

Responsibilities:
- Calculate risk metrics for each candidate
- Assign risk_score (0-100, HIGHER = BETTER SWING TRADE)
- Generate risk_warnings list for each candidate
- Pass ALL candidates to downstream departments
- NO approval/rejection authority

See SENTINEL_RISK_PHILOSOPHY.md for complete philosophy
"""

from .risk_department import RiskDepartment

__all__ = ['RiskDepartment']
