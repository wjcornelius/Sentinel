---
from: PORTFOLIO
message_id: MSG_PORTFOLIO_20251031T104051Z_5ffceecf
message_type: CandidateRequest
priority: high
requires_response: true
timestamp: '2025-10-31T10:40:51.451973Z'
to: RESEARCH
---

# Candidate Request - Portfolio Under-Deployed

# Candidate Request

The Portfolio Department requires additional stock candidates to maintain target capital deployment.

## Current Portfolio Status
- **Current Deployment**: 29.2%
- **Target Deployment**: 100.0%
- **Deployed Capital**: $29,238
- **Available Capital**: $70,762
- **Open Positions**: 0/10
- **Pending Positions**: 3

## Request Parameters
- **Available Position Slots**: 7
- **Capital Available for New Positions**: $70,762
- **Minimum Composite Score**: 6.0

## Action Required
Please run daily screening and provide candidates that:
1. Meet minimum composite score threshold (6.0+)
2. Pass sector diversification requirements
3. Fit within available capital constraints

Priority: **High** - Portfolio is significantly under-deployed

```json
{
  "request_type": "CANDIDATE_REQUEST",
  "deployment_status": {
    "current_deployment_pct": 0.29238,
    "target_deployment_pct": 1.0,
    "available_capital": 70762.0,
    "available_positions": 7
  },
  "criteria": {
    "min_composite_score": 6.0,
    "max_candidates": 7,
    "require_sector_diversification": true
  }
}
```
