# PHASE 1 IMPLEMENTATION PLAN v1.0
**Date:** 2025-10-30
**Prepared By:** C(P)
**Reviewed By:** CC
**Approved By:** WJC
**Status:** READY TO EXECUTE

## 1. EFFORT SUMMARY

| Department | Hours | Weeks (40h) | Dependencies |
|------------|-------|-------------|--------------|
| Trading | 40-55 | 1.0-1.4 | None (start here) |
| Research | 38-55 | 0.95-1.4 | Trading (for testing) |
| Risk | 50-70 | 1.25-1.75 | Research, hard_constraints.yaml |
| Portfolio | 55-75 | 1.4-1.9 | Research, Risk |
| Compliance | 45-65 | 1.1-1.6 | Trading, Risk, Portfolio |
| Executive | 65-90 | 1.6-2.25 | All above |
| **Total** | **293-410** | **7.3-10.25** | Sequential + integration |

**Adjusted Timeline (with integration testing):** 9-12 weeks at 40 hrs/week

## 2. BUILD ORDER & RATIONALE

### Phase 1.1: Trading Department (Week 1)
**Effort:** 40-55 hours
**Rationale:** Validates Alpaca connection, no dependencies
**Deliverables:**
- Alpaca API connection (paper trading account)
- Hard constraint validation (max position size, market hours, etc.)
- Order execution (market/limit orders)
- Slippage monitoring
- Message I/O (reads from Inbox, writes to Outbox)
- Database schema (trading_orders, executions)

**Checkpoint:** Successfully execute 5 manual test trades via message interface

### Phase 1.2: Research Department (Week 2)
**Effort:** 38-55 hours
**Rationale:** Provides data to all departments
**Deliverables:**
- Perplexity API integration (news sentiment)
- yfinance integration (price, volume, technicals)
- Alpha Vantage integration (fundamentals)
- Sentiment scoring (keyword-based)
- Market conditions monitor (VIX, SPY, sector indices)
- Message I/O (daily briefings, candidate analysis)
- Database schema (market_conditions, stock_analysis)

**Checkpoint:** Generate 10 stock candidates with sentiment scores, verify data accuracy

### Phase 1.3: Risk Management Department (Week 3-4)
**Effort:** 50-70 hours
**Rationale:** Critical gatekeeper, needs Research data
**Deliverables:**
- Hard constraint checker (reads hard_constraints.yaml)
- Risk score calculator (implements 5-component formula)
- CVaR calculator (deferred to Phase 2, use simple VaR)
- Correlation matrix (tracks inter-position correlations)
- Trading_Wisdom compliance (manual coding of 15 key rules)
- Message I/O (risk assessments)
- Database schema (risk_assessments, violations)

**Checkpoint:** Assess 20 test proposals, verify risk scores match manual calculations

### Phase 1.4: Portfolio Management Department (Week 5-6)
**Effort:** 55-75 hours
**Rationale:** Orchestrates trades, needs Research + Risk
**Deliverables:**
- Position tracking (current holdings, P&L)
- Candidate selection (top N by sentiment)
- Position sizing (equal-weight + conviction overlay)
- Trade proposal generator (buy/sell/rebalance decisions)
- Reconciliation (Alpaca vs internal state)
- Message I/O (proposals to Risk/Executive)
- Database schema (positions, portfolio_state, proposals)

**Checkpoint:** Generate 5 trade proposals, verify allocation logic matches spec

### Phase 1.5: Compliance Department (Week 7)
**Effort:** 45-65 hours
**Rationale:** Audit trail for all activity
**Deliverables:**
- Message archive indexer (timestamp-based)
- Trade logging (complete audit trail)
- Reconciliation (daily position reconciliation)
- Compliance checker (PDT rule, buying power via Alpaca API)
- Audit trail cross-referencer (links related messages)
- Message I/O (logs to Executive)
- Database schema (audit_trail, compliance_checks)

**Checkpoint:** Audit 10 trades end-to-end, verify complete paper trail

### Phase 1.6: Executive Department (Week 8-9)
**Effort:** 65-90 hours
**Rationale:** Orchestrates all departments
**Deliverables:**
- Workflow orchestration (daily trading cycle)
- Department coordination (tracks states: idle/working/waiting/failed)
- Trade approval framework (risk score 6-7 decision logic)
- WJC escalation formatter (human-readable summaries)
- Market condition adapter (VIX-based risk adjustments)
- Error handling (timeout detection, escalation)
- Message I/O (decisions to all departments)
- Database schema (decisions, escalations, department_states)

**Checkpoint:** Execute 3 full daily trading cycles, verify all workflows

### Phase 1.7: Integration Testing (Week 10-11)
**Effort:** 40-60 hours
**Focus:** End-to-end system validation

**Test Scenarios:**
1. **Routine Day:** 10 candidates → 5 proposals → 3 approved → 3 executed
2. **High Risk Day:** Proposals with risk scores 7-8 → Executive review → WJC escalation
3. **Market Stress:** VIX >30 → reduced position sizes → defensive posture
4. **Constraint Violation:** Proposal violates hard constraint → auto-reject
5. **Reconciliation:** Verify Alpaca positions match internal state
6. **Audit Trail:** Verify complete message chain for all trades
7. **Error Recovery:** Simulate department failure → Executive escalation → WJC intervention

**Checkpoint:** 90% of Phase 1 validation checkboxes passing

### Phase 1.8: Phase 1A Proof of Concept (Week 12)
**Effort:** 20-30 hours
**Focus:** Live paper trading with human message routing

**Scope:**
- 5-10 real trades (spread over 1-2 weeks)
- WJC manually routes messages between 6 Claude sessions
- Verify architecture works in production
- Identify bugs/edge cases

**Success Criteria:**
- All 5-10 trades execute successfully
- No message loss
- Complete audit trail
- WJC time <2 hours total (manageable)

**Checkpoint:** Phase 1A complete → proceed to Phase 1B (automated routing)

## 3. PHASE 1B: AUTOMATED MESSAGE ROUTER

**Timing:** Build during Phase 1A if WJC unavailable for manual routing
**Effort:** 8-12 hours
**Deliverable:** Python script replaces WJC as message router

```python
# Pseudo-code for message router
while True:
    for dept in DEPARTMENTS:
        messages = scan_folder(f"Messages_Between_Departments/Outbox/{dept}/")
        for msg in messages:
            recipient = parse_yaml(msg)['to']
            move_file(msg, f"Inbox/{recipient}/")
            archive_file(msg, f"Archive/{today}/{dept}/")
            if msg['priority'] == 'critical':
                email_wjc(msg)  # Escalation notification
    sleep(10)  # Poll every 10 seconds
```

**Decision Point:** WJC decides during Phase 1A whether Phase 1B router needed before full paper trading

## 4. PHASE 2 READINESS CRITERIA

Phase 1 → Phase 2 transition requires:

- ✅ All 6 departments operational
- ✅ Message protocol stable (no format changes in 1 week)
- ✅ 90% of validation checkboxes passing
- ✅ 20+ successful paper trades (Phase 1A)
- ✅ Zero critical bugs in 1 week
- ✅ Complete audit trail for all trades
- ✅ WJC approval to proceed

**Estimated Timeline:** 9-12 weeks from CC start date

## 5. RISK MITIGATION

### 5.1 Schedule Risks
- **Risk:** Department build takes longer than estimated
- **Mitigation:** 30% time buffer built into estimates (conservative)
- **Trigger:** If any department exceeds estimate by >20%, escalate to WJC

### 5.2 Technical Risks
- **Risk:** Message protocol doesn't scale to 100 msg/day
- **Mitigation:** Phase 1A tests with low volume, Phase 1B adds automation
- **Trigger:** If message loss >5%, halt and redesign

### 5.3 Integration Risks
- **Risk:** Departments don't communicate correctly
- **Mitigation:** Checkpoint after each department validates messages
- **Trigger:** If integration test failures >10%, review protocol spec

### 5.4 API Risks
- **Risk:** Perplexity/Alpha Vantage rate limits or API changes
- **Mitigation:** Aggressive caching, fallback to yfinance for some data
- **Trigger:** If API failures >5%, add redundant data sources

## 6. DEPENDENCIES & PREREQUISITES

### Before CC Starts:
- ✅ hard_constraints.yaml delivered (C(P) - completed)
- ✅ MESSAGE_PROTOCOL_SPECIFICATION.md delivered (C(P) - completed)
- ✅ PHASE_1_IMPLEMENTATION_PLAN.md delivered (C(P) - completed)
- ⏳ WJC approval to proceed (pending)
- ⏳ Alpaca paper trading account active (WJC - verify)
- ⏳ API keys: Perplexity, Alpha Vantage, Alpaca (WJC - provide to CC)

### During Build:
- WJC available for Phase 1A manual message routing (1-2 hours over 2 weeks)
- WJC available for escalation testing (simulate critical decisions)
- WJC reviews weekly progress reports from CC

## 7. WEEKLY PROGRESS MILESTONES

| Week | Department | Milestone | CC Deliverable |
|------|------------|-----------|----------------|
| 1 | Trading | Alpaca integration complete | 5 test trades executed |
| 2 | Research | Data pipeline operational | 10 candidates with sentiment |
| 3 | Risk | Hard constraints coded | 20 risk assessments |
| 4 | Risk | Risk scoring complete | Correlation matrix working |
| 5 | Portfolio | Position tracking done | Current positions tracked |
| 6 | Portfolio | Allocation logic complete | 5 trade proposals generated |
| 7 | Compliance | Audit trail working | 10 trades fully audited |
| 8 | Executive | Workflow orchestration | Daily cycle executes |
| 9 | Executive | Approval logic complete | 3 full cycles end-to-end |
| 10 | Integration | Test scenarios 1-4 passing | Bug report |
| 11 | Integration | Test scenarios 5-7 passing | Final validation |
| 12 | Phase 1A | Proof of concept | 5-10 live paper trades |

**CC submits weekly status report:** progress, blockers, hours spent, next week plan

## 8. ACCEPTANCE CRITERIA (Phase 1 Complete)

### 8.1 Functional Requirements
- [ ] All 6 departments operational and message-enabled
- [ ] Complete daily trading cycle (Research → Portfolio → Risk → Executive → Trading → Compliance)
- [ ] Hard constraints enforced (100% compliance)
- [ ] Risk scoring accurate (manual validation of 20 scores)
- [ ] Position sizing matches spec (equal-weight + conviction)
- [ ] Executive approval logic correct (test 10 decisions)
- [ ] Audit trail complete (no missing message links)
- [ ] Alpaca integration working (paper trades execute)

### 8.2 Performance Requirements
- [ ] Message latency <5 minutes (Phase 1A manual routing)
- [ ] Data refresh rate: VIX/indices every 5 min, stock data every hour
- [ ] Database queries <1 second (for Phase 1 volumes)
- [ ] No message loss (100% delivery)

### 8.3 Quality Requirements
- [ ] Zero critical bugs (trading halts, incorrect risk scores, violated constraints)
- [ ] <5 minor bugs (cosmetic issues, non-critical message delays)
- [ ] Code documented (docstrings for all functions)
- [ ] Database schema matches DEPARTMENTAL_SPECIFICATIONS

### 8.4 Business Requirements
- [ ] 20+ successful paper trades (no losses >5% per trade)
- [ ] WJC can understand all escalations (clear formatting)
- [ ] Complete audit trail (Compliance can reconstruct any trade)
- [ ] Risk management effective (no hard constraint violations in production)

**Phase 1 Sign-Off:** WJC + CC + C(P) all approve → Proceed to Phase 2

## 9. PHASE 2 PREVIEW (Not in Scope for Current Plan)

Phase 2 Enhancements (Future):
- Economic indicators (FRED API)
- Advanced sentiment (FinBERT, GPT-based)
- CVaR risk measurement (replace VaR)
- Kelly criterion position sizing
- Risk-parity allocation
- Full Trading_Wisdom.txt parser (NLP-based)
- Settlement tracking
- Extended hours trading
- Multi-timeframe analysis
- ML-based conviction scoring
- Automated message router (if not built in Phase 1B)

**Phase 2 Trigger:** Phase 1 complete + WJC approval + 1 month live paper trading success

---

**PLAN STATUS:** ✅ APPROVED FOR EXECUTION
**CC START DATE:** Upon receipt of this document + WJC confirmation
**ESTIMATED COMPLETION:** 9-12 weeks from start
**NEXT REVIEW:** End of Week 1 (Trading Department checkpoint)
