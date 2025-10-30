# MESSAGE PROTOCOL SPECIFICATION v1.0
**Date:** 2025-10-30
**Author:** C(P) + CC
**Status:** APPROVED FOR IMPLEMENTATION

## 1. MESSAGE FORMAT

### 1.1 File Structure
```yaml
---
message_id: "MSG_{department}_{timestamp}_{uuid4}"
from: "DEPARTMENT_NAME"
to: "DEPARTMENT_NAME"
timestamp: "2025-10-30T16:45:00Z"  # ISO 8601 UTC
message_type: "briefing|analysis|assessment|decision|log|escalation"
priority: "routine|elevated|critical"
requires_response: true|false
response_deadline: "2025-10-30T17:00:00Z"  # ISO 8601 UTC (if requires_response)
thread_id: "THREAD_{topic}_{date}"  # Groups related messages
parent_message_id: "MSG_..." # If replying to specific message
---

# Message Title (Human Readable)

## Summary
[One-sentence executive summary]

## Details
[Full message body in markdown]

### Data Payload (if applicable)
```json
{
  "structured_data": "goes_here",
  "ticker": "AAPL",
  "risk_score": 6.5,
  "components": {...}
}
```

## Action Required
[Specific request/question for recipient]

## Attachments
- reference_doc_1.yaml
- chart_volatility.png
```

### 1.2 Naming Convention
```
Messages_Between_Departments/
├── Inbox/
│   ├── RESEARCH/
│   ├── RISK/
│   ├── TRADING/
│   ├── PORTFOLIO/
│   ├── COMPLIANCE/
│   └── EXECUTIVE/
├── Outbox/
│   ├── RESEARCH/
│   ├── RISK/
│   ├── TRADING/
│   ├── PORTFOLIO/
│   ├── COMPLIANCE/
│   └── EXECUTIVE/
└── Archive/
    └── 2025-10-30/
        ├── RESEARCH/
        ├── RISK/
        └── ...
```

Filename format: `{message_id}.md`
Example: `MSG_RESEARCH_20251030T164500Z_a3f9c2d1.md`

### 1.3 Message Types

| Type | Sender | Recipients | Purpose | Response Required |
|------|--------|------------|---------|-------------------|
| `briefing` | Research | All | Daily market analysis | No |
| `analysis` | Research | Portfolio, Risk | Stock candidate deep-dive | Optional |
| `assessment` | Risk | Portfolio, Executive | Risk evaluation of proposal | Yes (decision) |
| `decision` | Executive | All | Approval/rejection of action | No (final) |
| `proposal` | Portfolio | Risk, Executive | Trade recommendation | Yes (assessment) |
| `execution` | Trading | Compliance | Order confirmation | No (log) |
| `log` | Compliance | Executive | Audit entry | No |
| `escalation` | Any | Executive or WJC | Issue requiring intervention | Yes (urgent) |

### 1.4 Priority Levels
- `routine`: Normal workflow, 2-hour SLA
- `elevated`: Time-sensitive, 30-min SLA
- `critical`: Market-moving event, 5-min SLA

## 2. STANDARD MESSAGE FLOWS

### 2.1 Daily Trading Cycle
```
09:30 MARKET_OPEN
  ↓
09:35 RESEARCH → ALL (briefing: "Market Open Analysis")
  ↓
10:00 RESEARCH → PORTFOLIO (analysis: 5-10 stock candidates)
  ↓
10:30 PORTFOLIO → RISK (proposal: "Trade Proposal - 3 new positions")
  ↓
11:00 RISK → PORTFOLIO (assessment: risk_scores for each)
  ↓
11:15 PORTFOLIO → EXECUTIVE (decision_request: "Approve 2 positions")
  ↓
11:30 EXECUTIVE → PORTFOLIO (decision: "APPROVED with modifications")
  ↓
11:45 PORTFOLIO → TRADING (execution_request: orders)
  ↓
12:00 TRADING → PORTFOLIO (execution: confirmations)
  ↓
12:05 TRADING → COMPLIANCE (log: trade_log)
  ↓
15:45 COMPLIANCE → EXECUTIVE (log: daily_reconciliation)
  ↓
16:00 MARKET_CLOSE
```

### 2.2 Emergency Escalation Flow
```
ANY_DEPARTMENT detects critical issue
  ↓
DEPARTMENT → EXECUTIVE (escalation: priority=critical)
  ↓
EXECUTIVE → WJC (escalation: formatted for human review)
  ↓
WJC responds via manual message injection
  ↓
EXECUTIVE → ALL (decision: broadcast WJC directive)
```

## 3. DATA SERIALIZATION STANDARDS

### 3.1 Embedded JSON (for structured data)
```yaml
---
from: RISK
to: PORTFOLIO
message_type: assessment
---

# Risk Assessment: AAPL Position

## Risk Score: 6.5/10

```json
{
  "ticker": "AAPL",
  "position_size": 50,
  "risk_score": 6.5,
  "components": {
    "volatility": 0.45,
    "concentration": 0.60,
    "liquidity": 0.20,
    "compliance": 0.00,
    "correlation": 0.40
  },
  "vix_adjustment": true,
  "violations": [],
  "recommendation": "APPROVE_WITH_CAUTION"
}
```
```

### 3.2 Large Datasets (separate files)
```yaml
---
from: RESEARCH
to: PORTFOLIO
---

# Candidate List: 2025-10-30

See attached: `Data/Research/candidates_20251030.json`

Summary: 25 candidates, avg sentiment +45, top 5:
1. AAPL (+78)
2. MSFT (+72)
3. GOOGL (+68)
...
```

## 4. ERROR HANDLING

### 4.1 Message Validation
```python
# Every department implements on message receipt:
def validate_message(msg):
    required_fields = ['message_id', 'from', 'to', 'timestamp', 'message_type']
    if not all(field in msg.metadata for field in required_fields):
        return ERROR_INVALID_FORMAT

    if msg.metadata['to'] != THIS_DEPARTMENT:
        return ERROR_WRONG_RECIPIENT

    if msg.metadata['requires_response'] and 'response_deadline' not in msg.metadata:
        return ERROR_MISSING_DEADLINE

    return VALID
```

### 4.2 Timeout Handling
- If `requires_response=true` and no response by deadline: sender escalates to EXECUTIVE
- If EXECUTIVE doesn't respond within SLA: escalate to WJC
- All timeouts logged in Compliance audit trail

### 4.3 Malformed Message Recovery
```
DEPARTMENT receives malformed message
  ↓
DEPARTMENT → SENDER (escalation: "Cannot parse message MSG_xyz")
  ↓
SENDER → DEPARTMENT (resends corrected message)
  ↓
DEPARTMENT → COMPLIANCE (log: "Malformed message incident")
```

## 5. DEPARTMENT-SPECIFIC PROTOCOLS

### 5.1 RESEARCH Output Format
```json
{
  "ticker": "AAPL",
  "analysis_date": "2025-10-30",
  "sentiment_score": 78.5,
  "sentiment_components": {
    "keyword_score": 35,
    "source_credibility": 0.85,
    "recency_weight": 1.2
  },
  "news_summary": "Apple reports strong Q3...",
  "technical_signals": {
    "rsi": 58,
    "macd": "bullish_crossover",
    "volume_trend": "increasing"
  },
  "fundamental_data": {
    "pe_ratio": 28.5,
    "revenue_growth_yoy": 0.12,
    "profit_margin": 0.26
  },
  "market_conditions": {
    "vix": 18.5,
    "spy_trend": "uptrend",
    "sector_performance": "tech outperforming"
  }
}
```

### 5.2 RISK Assessment Format
```json
{
  "ticker": "AAPL",
  "position_size": 50,
  "risk_score": 6.5,
  "components": {
    "volatility": 0.45,
    "concentration": 0.60,
    "liquidity": 0.20,
    "compliance": 0.00,
    "correlation": 0.40
  },
  "hard_constraint_violations": [],
  "soft_constraint_warnings": ["Position >10% of portfolio"],
  "vix_adjustment": true,
  "recommendation": "APPROVE_WITH_REDUCTION",
  "suggested_size_reduction": 0.30,
  "rationale": "Moderate risk due to concentration, reduce by 30%"
}
```

### 5.3 PORTFOLIO Proposal Format
```json
{
  "proposal_id": "PROP_20251030_001",
  "action": "BUY|SELL|HOLD",
  "ticker": "AAPL",
  "shares": 50,
  "rationale": "High sentiment (+78), strong fundamentals, portfolio conviction 85/100",
  "conviction_score": 85,
  "allocation_pct": 0.067,
  "expected_portfolio_heat_increase": 0.015,
  "post_trade_heat": 0.065,
  "requires_rebalancing": false
}
```

### 5.4 EXECUTIVE Decision Format
```json
{
  "decision_id": "DEC_20251030_001",
  "proposal_id": "PROP_20251030_001",
  "decision": "APPROVED|REJECTED|APPROVED_WITH_MODIFICATIONS|ESCALATE_TO_WJC",
  "modifications": {
    "original_shares": 50,
    "approved_shares": 35,
    "reduction_pct": 0.30,
    "reason": "Risk mitigation"
  },
  "rationale": "Approved with 30% reduction due to moderate risk score (6.5)",
  "approval_authority": "EXECUTIVE|WJC",
  "timestamp": "2025-10-30T11:30:00Z"
}
```

### 5.5 TRADING Execution Format
```json
{
  "order_id": "ORD_20251030_001",
  "proposal_id": "PROP_20251030_001",
  "decision_id": "DEC_20251030_001",
  "ticker": "AAPL",
  "action": "BUY",
  "shares": 35,
  "order_type": "LIMIT",
  "limit_price": 178.50,
  "status": "FILLED|PARTIAL|REJECTED|PENDING",
  "fill_price": 178.45,
  "fill_time": "2025-10-30T11:45:23Z",
  "slippage_pct": -0.028,
  "slippage_flag": false,
  "alpaca_order_id": "a3f9c2d1-...",
  "commission": 0.00
}
```

### 5.6 COMPLIANCE Log Format
```json
{
  "log_id": "LOG_20251030_001",
  "log_type": "TRADE|VIOLATION|RECONCILIATION|AUDIT",
  "timestamp": "2025-10-30T11:45:30Z",
  "related_messages": ["MSG_PORTFOLIO_...", "MSG_RISK_...", "MSG_TRADING_..."],
  "audit_trail": {
    "proposal": "PROP_20251030_001",
    "risk_assessment": "ASSESSMENT_20251030_001",
    "executive_decision": "DEC_20251030_001",
    "trade_execution": "ORD_20251030_001"
  },
  "compliance_checks": {
    "pdt_rule": "PASS",
    "buying_power": "PASS",
    "position_limits": "PASS",
    "hard_constraints": "PASS"
  },
  "flags": []
}
```

## 6. RATE LIMIT HANDLING

### 6.1 API Rate Limits (Phase 1)
```yaml
perplexity_api:
  rate_limit: 60  # queries per hour
  handling: "Queue requests, process batch every minute"

yfinance:
  rate_limit: null  # No official limit, but be respectful
  handling: "Cache aggressively, 5-min refresh"

alpha_vantage:
  rate_limit: 5  # queries per minute (free tier)
  handling: "Critical data only, cache 24h"

alpaca_api:
  rate_limit: 200  # requests per minute
  handling: "Batching orders, no throttling needed for Phase 1 volumes"
```

### 6.2 Backoff Strategy
```python
# Exponential backoff for rate limit errors
def api_call_with_retry(api_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api_func()
        except RateLimitError:
            if attempt == max_retries - 1:
                escalate_to_executive("API rate limit exceeded")
                raise
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
```

## 7. PHASE 1A vs 1B PROTOCOLS

### 7.1 Phase 1A (Human-Mediated)
- WJC manually copies messages between 6 Claude conversations
- Each department checks its Inbox/ folder every time WJC prompts
- WJC copies department's response from Outbox/ to recipient's Inbox/
- Estimated 20-40 total messages (proof of concept)

### 7.2 Phase 1B (Automated Router)
```python
# CC implements message router script
def message_router():
    while True:
        for dept in DEPARTMENTS:
            new_messages = scan_outbox(dept)
            for msg in new_messages:
                recipient = msg.metadata['to']
                move_to_inbox(msg, recipient)
                archive_message(msg)
                if msg.priority == 'critical':
                    notify_wjc(msg)
        time.sleep(10)  # Poll every 10 seconds
```

## 8. TESTING PROTOCOL

### 8.1 Message Validation Tests
- [ ] All departments validate incoming message format
- [ ] Reject malformed messages with clear error
- [ ] Handle missing required fields gracefully
- [ ] Timeout detection works (requires_response + no response)

### 8.2 Integration Tests
- [ ] Research → Portfolio flow (candidate delivery)
- [ ] Portfolio → Risk → Executive → Trading flow (trade approval)
- [ ] Trading → Compliance flow (audit trail)
- [ ] Any → Executive escalation flow

### 8.3 Load Tests (Phase 2)
- [ ] 100 messages/day throughput
- [ ] No message loss
- [ ] SLA compliance >95%

## 9. ALGORITHM SPECIFICATIONS (from C(P) blocker resolution)

### 9.1 Risk Score Calculation
```python
risk_score = (
    volatility_score * 0.30 +      # 30-day annualized volatility / 0.60
    concentration_score * 0.25 +   # position_pct / 0.15
    liquidity_score * 0.20 +       # shares / avg_volume / 0.05
    compliance_score * 0.15 +      # hard violations = 1.0, soft * 0.2
    correlation_score * 0.10       # max(0, avg_correlation)
) * 10

if vix > 30: risk_score *= 1.3
elif vix > 20: risk_score *= 1.15
risk_score = min(risk_score, 10.0)
```

### 9.2 Position Sizing (Portfolio)
```python
base_allocation = (portfolio_value * 0.85) / 15  # 85% invested, max 15 positions
conviction_multiplier = 0.8 + ((sentiment + 100) / 200) * 0.4  # 0.8 to 1.2
position_allocation = base_allocation * conviction_multiplier
position_allocation = clamp(position_allocation,
                            portfolio_value * 0.03,
                            portfolio_value * 0.15)
shares = int(position_allocation / current_price)
```

### 9.3 Executive Approval Logic (Risk Scores 6-7)
```python
if conviction >= 70 and heat < 0.06 and risk < 6.5 and vix < 25:
    return "APPROVED"
elif conviction >= 60 and heat < 0.07 and risk < 7.0:
    reduce_by = 0.25 + ((risk - 6.0) * 0.25)  # 25-50% reduction
    return "APPROVED_WITH_REDUCTION", reduce_by
elif conviction < 60 or heat >= 0.07 or vix >= 30:
    return "REJECTED"
else:
    return "ESCALATE_TO_WJC"
```

### 9.4 Sentiment Scoring (Research)
```python
# Keyword-based sentiment analysis
positive_keywords = {'strong': 2, 'beat': 3, 'growth': 2, ...}
negative_keywords = {'weak': -2, 'miss': -3, 'decline': -2, ...}

sentiment_sum = sum(count(keyword) * weight for all keywords in news_text)
sentiment_score = (sentiment_sum / 20) * 100  # Normalize to -100 to +100
sentiment_score = clamp(sentiment_score, -100, 100)
```

## 10. CRITICAL IMPLEMENTATION NOTES FOR CC

1. All departments MUST validate incoming messages (format, sender, recipient)
2. All departments MUST log every message (in/out) to Compliance
3. Timestamps MUST be UTC ISO 8601 (avoid timezone confusion)
4. JSON payloads MUST be in markdown code blocks (for Claude parsing)
5. UUIDs MUST be unique (use uuid4 in Python)
6. Thread IDs group related messages (e.g., all messages about AAPL trade proposal)
7. Hard constraint violations = immediate rejection (no scoring needed)
8. Risk scores ≥8 = auto-escalate to WJC (no Executive approval)
9. Phase 1A: WJC is the message router (manual copy/paste)
10. Phase 1B: Build Python router before paper trading (8-12 hours)

---

**PROTOCOL STATUS:** ✅ APPROVED FOR IMPLEMENTATION
**CC ACTION:** Implement message I/O in each department per this spec
**ESTIMATED EFFORT:** 6-8 hours per department for messaging infrastructure
