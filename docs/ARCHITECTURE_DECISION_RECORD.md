# Architecture Decision Record (ADR)

## ADR-001: Database Choice - SQLite for MVP, Scalable to PostgreSQL

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team  

### Context
We need a database to store prediction history, audit trails, and bias metrics for compliance.

### Decision
Use SQLite for MVP development with a database abstraction layer that allows future migration to PostgreSQL.

### Rationale
- **Fast**: No external dependencies for local development
- **ACID**: Full ACID compliance for transaction integrity
- **Audit Trail**: Essential for regulatory compliance (one of 6 major requirements)
- **Scalable Architecture**: DB abstraction layer allows PostgreSQL migration for production

### Consequences
- ✅ Simplified local development
- ✅ File-based storage (no server infrastructure)
- ✅ Built-in transaction support
- ⚠️ Single-user concurrency limitation (mitigated by abstraction layer for future DB swap)
- ⚠️ Potential file locking in high-concurrency scenarios

---

## ADR-002: Gemini API Fallback to Local Risk Scorer

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
External AI APIs can experience outages (503), quota limits (429), or timeouts. Users need reliable loan decisions even when external services fail.

### Decision
Implement a local fallback risk assessment algorithm that calculates scores based on transparent business rules.

### Rationale
- **Resilience**: No single point of failure for critical lending decisions
- **Transparency**: Fallback uses explainable business rules (not a black box)
- **Cost**: Reduces API quota consumption
- **Auditability**: Can track when fallback is used vs. primary model

### Algorithm
```
Risk Score (0-100):
  - Repayment History: 0-45 points
  - Loan-to-Income: 0-30 points
  - Interest Rate: 0-15 points
  - Employment Stability: 0-8 points
  - Age Segment: 0-5 points
  
Decision: Reject if score >= 45, else Approve
```

### Consequences
- ✅ System availability during API outages
- ✅ Reduced API calls and costs
- ✅ Faster fallback decisions (local vs. remote)
- ⚠️ Fallback model may have different accuracy than Gemini
- ⚠️ Operational overhead to monitor when fallback is used

---

## ADR-003: Structured Logging with Request IDs

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
Compliance and debugging require detailed traceability of all predictions and overrides.

### Decision
- Every request gets a unique UUID (request_id)
- All related operations logged with this ID
- Structured JSON logging for machine parsing
- Separate audit log for compliance

### Rationale
- **Traceability**: Trace any decision from API call through prediction to override
- **Compliance**: Regulatory requirements for decision audit trail
- **Debugging**: Correlate distributed logs by request_id
- **Monitoring**: Enable alerts on patterns (e.g., too many overrides)

### Log Levels
- **INFO**: Normal operations, predictions, approvals
- **WARNING**: Fallback activation, validation failures, quota issues
- **ERROR**: System failures, unexpected exceptions

### Consequences
- ✅ Complete audit trail for compliance
- ✅ Simplified debugging of multi-step processes
- ⚠️ Increased logging volume
- ⚠️ Storage overhead for audit logs

---

## ADR-004: Role-Based Access Control (RBAC)

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
Different users (analysts, reviewers, admins) need different access levels.

### Decision
Implement RBAC via HTTP headers with four roles:

| Role | Permissions |
|------|------------|
| admin | View all, predict, approve, override, manage users, export data |
| analyst | View cases, predict, export own |
| reviewer | View cases, approve overrides, export own |
| viewer | View cases only |

### Rationale
- **Security**: Each role gets minimum necessary permissions
- **Compliance**: Audit trail shows who made each decision
- **Flexibility**: Easy to add new roles or permissions
- **Scalability**: Simple header-based auth (easily extended to JWT/OAuth)

### Consequences
- ✅ Clear permission boundaries
- ✅ Easy audit trail of approvals
- ⚠️ Requires user management system
- ⚠️ Risk of accidental role misconfiguration

---

## ADR-005: Decision Confidence & Risk Bands

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
Loan officers need to understand decision certainty and risk level at a glance.

### Decision
Every prediction returns:
- **Confidence Score** (0-100%): How certain the model is
- **Risk Band**: Low/Medium/High categorization
- **Risk Score** (0-100): Detailed numeric risk assessment

### Thresholds
```
Risk Bands:
  - Low Risk: 0-30
  - Medium Risk: 31-65
  - High Risk: 66-100

Confidence Algorithm:
  - Extreme scores (0-5, 95-100): 92% confidence
  - High risk extremes (20, 80): 85% confidence
  - Borderline (40-60): 55% confidence
```

### Rationale
- **User Experience**: Simplified decision making with bands
- **Precision**: Detailed scores for advanced review
- **Confidence**: Tells reviewer how much to trust the decision
- **Calibration**: Can track confidence vs. actual defaults

### Consequences
- ✅ Better UX for loan officers
- ✅ Confidence helps identify unreliable predictions
- ⚠️ Additional model tuning required
- ⚠️ Risk of over-relying on confidence scores

---

## ADR-006: Environment Variables for Secrets

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
API keys and sensitive config should NOT be in version control.

### Decision
- Use `.env` file locally (never commit)
- Use environment variables for secrets in production
- Provide `.env.example` template

### Required Variables
```
GEMINI_API_KEY
ADMIN_PASSWORD
DATABASE_URL
APP_SECRET_KEY
LOG_FILE_PATH
AUDIT_LOG_FILE
```

### Rationale
- **Security**: Keys not exposed in Git history
- **Flexibility**: Different config per environment (dev/prod)
- **Docker/Cloud**: Standard practice for containerized apps
- **Compliance**: Required audit controls

### Consequences
- ✅ Secure credential management
- ✅ Environment-specific config
- ⚠️ Developers must understand `.env` file setup
- ⚠️ Risk if `.env` accidentally committed

---

## ADR-007: PDF Export via ReportLab

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
Compliance requires archivable records of each decision.

### Decision
Use ReportLab to generate PDF reports containing:
- Applicant information
- Decision and confidence
- Risk factors analysis
- Explanation of prediction
- Audit timestamp

### Rationale
- **Compliance**: PDF is standard for official records
- **Portable**: Can email or archive independently
- **Professional**: Formatted reports for loan files
- **Programmable**: ReportLab allows custom branding

### Consequences
- ✅ Compliance-ready reports
- ✅ Professional presentation
- ⚠️ Additional library dependency
- ⚠️ PDF generation adds latency

---

## ADR-008: Feature Flags for Gradual Rollout

**Status**: Proposed  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
New features may need gradual testing with subsets of users.

### Decision
Implement feature flags in Config.py:
```python
FEATURES = {
    "enable_confidence_scores": True,
    "enable_risk_bands": True,
    "enable_bias_checks": True,
    # ...
}
```

### Rationale
- **Safety**: Test new features with subset of traffic
- **Rollback**: Disable problematic features instantly
- **A/B Testing**: Compare feature vs. no-feature outcomes

### Consequences
- ✅ Safe feature rollout
- ✅ Ability to disable broken features
- ⚠️ Code complexity increases
- ⚠️ Need to track flag status in audit trail

---

## ADR-009: Async/Await for AI API Calls

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
AI API calls are I/O bound and can timeout. We need efficient handling of multiple concurrent requests.

### Decision
Use FastAPI's async request handlers with aiohttp for non-blocking API calls.

### Rationale
- **Scalability**: Handle many concurrent requests with limited workers
- **Resource Efficiency**: Don't block threads on network I/O
- **TimeOut Management**: Can implement per-request timeouts
- **Retry Logic**: Easy to implement retry loops with async

### Consequences
- ✅ Better resource utilization
- ✅ Handles timeouts elegantly
- ⚠️ Requires async/await programming model
- ⚠️ Debugging async code is more complex

---

## ADR-010: SQLite Audit Trail (Normalization Decision)

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team

### Context
Audit trail must be immutable and queryable for compliance.

### Decision
Store complete audit trail in SQLite with separate tables:
- `predictions`: Full decision details
- `applicant_history`: Repayment outcomes
- `bias_metrics`: Demographic statistics
- `user_roles`: Access control

### Rationale
- **Integrity**: SQLite transactions ensure atomicity
- **Queryability**: SQL allows regulatory reporting
- **Compliance**: Immutable log of all decisions
- **Performance**: Indexed queries on prediction history

### Consequences
- ✅ Complete audit trail
- ✅ Compliance-ready queries
- ⚠️ File-based storage limits concurrency
- ⚠️ Must maintain referential integrity

---

## Future ADRs

- **ADR-011**: Migration strategy from SQLite to PostgreSQL
- **ADR-012**: Machine Learning model retraining pipeline
- **ADR-013**: Bias mitigation strategies
- **ADR-014**: Real-time fairness monitoring alerts
- **ADR-015**: Multi-currency support for international expansion

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-15  
**Maintained By**: Architecture Team
