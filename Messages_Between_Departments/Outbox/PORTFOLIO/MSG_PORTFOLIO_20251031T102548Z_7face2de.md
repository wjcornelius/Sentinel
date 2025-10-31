---
from: PORTFOLIO
message_id: MSG_PORTFOLIO_20251031T102548Z_7face2de
message_type: CandidateRequest
priority: high
requires_response: true
timestamp: '2025-10-31T10:25:48.579889Z'
to: RESEARCH
---

# Candidate Request - Portfolio Under-Deployed

# Candidate Request

The Portfolio Department requires additional stock candidates to maintain target capital deployment.

## Current Portfolio Status
- **Current Deployment**: 12.6%
- **Target Deployment**: 100.0%
- **Deployed Capital**: $12,615
- **Available Capital**: $87,385
- **Open Positions**: 1/10
- **Pending Positions**: 0

## Request Parameters
- **Available Position Slots**: 9
- **Capital Available for New Positions**: $87,385
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
    "current_deployment_pct": 0.12615,
    "target_deployment_pct": 1.0,
    "available_capital": 87385.0,
    "available_positions": 9
  },
  "criteria": {
    "min_composite_score": 6.0,
    "max_candidates": 9,
    "require_sector_diversification": true
  }
}
```
