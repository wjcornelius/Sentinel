"""
Risk Department v2.0 - Advisory Risk Assessment

Responsibilities:
- Calculate risk metrics for each candidate
- Assign risk_score (0-100, higher = safer)
- Generate risk_warnings list for each candidate
- Pass ALL candidates to downstream departments
- NO approval/rejection authority
"""

from .risk_department import RiskDepartment

__all__ = ['RiskDepartment']
