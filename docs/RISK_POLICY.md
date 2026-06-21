# Risk Policy & Approval Rules

## Credit Risk Intelligence Platform v1.0.0

---

## 1. Risk Assessment Framework

### Risk Score Calculation (0-100)

The platform calculates risk scores based on five weighted factors:

| Factor | Max Points | Description |
|--------|-----------|-------------|
| **Repayment History** | 45 | Past payment behavior |
| **Loan-to-Income Ratio** | 30 | Debt capacity relative to income |
| **Interest Rate** | 15 | Cost of borrowing |
| **Employment Stability** | 8 | Employment history |
| **Age Segment** | 5 | Borrower age demographics |
| **TOTAL** | **103** | Normalized to 0-100 |

### Risk Bands

```
Low Risk:      0-30 points   → Recommended for Approval
Medium Risk:  31-65 points  → Review recommended
High Risk:   66-100 points  → Escalation required
```

### Confidence Scoring

Confidence indicates prediction reliability:

```
95-100% Confidence: Extreme scores (0-5, 95-100 points)
85-94% Confidence:  Strong signals (20-34, 66-80 points)
65-84% Confidence:  Clear direction (35-65 points)
55-64% Confidence:  Borderline (45-55 points - near threshold)
```

---

## 2. Approval Authority by Role

### Administrator
- **Authority**: All approval levels
- **Max Exposure**: Unlimited
- **Restrictions**: None
- **Oversight**: Board of Directors

### Analyst (Credit Analyst)
- **Authority**: Low Risk (0-30) automatically
- **Max Exposure**: Up to $50,000 per applicant
- **Restrictions**: Cannot override High Risk
- **Escalation**: Medium+ Risk to Reviewer

### Reviewer (Credit Officer / Manager)
- **Authority**: Up to Medium Risk (31-65)
- **Max Exposure**: Up to $100,000 per applicant
- **Restrictions**: Cannot approve High Risk alone
- **Escalation**: High Risk to Administrator

### Viewer (Operations / Reporting)
- **Authority**: View decisions only
- **Max Exposure**: No approval authority
- **Restrictions**: Reporting only

---

## 3. Decision Rules

### Automatic Approval (NO manual review needed)

**Applicants with:**
- Risk Score < 25 (Upper Low Risk)
- Confidence > 85%
- Loan Amount < $10,000
- Repayment History = "Excellent" or "Good"
- LTI Ratio < 0.30

**Process**: Approve immediately, log to audit trail

---

### Manual Review Required

**Applicants with:**
- Risk Score 25-65 (Medium Risk)
- OR Confidence 55-75%
- OR LTI Ratio 0.30-0.50
- OR Repayment History = "Fair" or "Average"

**Process**: 
1. Assign to Credit Analyst
2. Review all decision factors
3. Approve/Reject/Escalate within 24 hours
4. Document reason in override field

---

### Mandatory Escalation

**Applicants with:**
- Risk Score > 65 (High Risk)
- AND Loan Amount > $50,000
- OR Repayment History = "Poor" or "Defaulted"
- OR LTI Ratio > 0.60

**Process**:
1. Automatically escalate to Credit Officer
2. Require management approval
3. Document business justification
4. Notify compliance team
5. Update bias metrics

---

## 4. Override Guidelines

### When Overrides Are Permitted

Override decisions must document reasons in this format:

```
"reason": "special_circumstance | relationship_manager_recommendation | 
           business_development_priority | portfolio_balancing | 
           seasonal_adjustment | collateral_provided | guarantor_available | other"
```

### Acceptable Override Reasons

1. **Special Circumstance**
   - Recent job change (with offer letter)
   - Temporary income dip (show LOE)
   - Recent debt payoff proving capacity

2. **Relationship Manager Recommendation**
   - Long-standing customer
   - Customer lifetime value > $100K
   - Existing account in good standing

3. **Portfolio Balancing**
   - Geographic expansion
   - Loan intent diversification
   - Seasonal business pattern

4. **Collateral Provided**
   - Real estate pledge
   - Savings/CD pledge
   - Third-party guarantee

5. **Guarantor Available**
   - Co-signer with strong profile
   - Employer guarantee
   - Family member guarantee

6. **Business Development Priority**
   - Strategic customer acquisition
   - Market expansion
   - Relationship deepening

7. **Other** (must be documented in detail)

### Override Restrictions

- **Analysts** cannot override
- **Reviewers** can override Low/Medium Risk only
- **Admins** can override any risk level
- **Max Overrides Per Month**: 5% of total decisions
- **Max Override Delta**: Cannot reverse decision + 2 risk bands

---

## 5. Bias & Fairness Controls

### Protected Characteristics (NOT used in scoring)

The model does NOT directly use:
- Race/Ethnicity
- Gender
- Age (except segment: <21, >35, etc.)
- Religion
- Marital Status
- Disability Status

### Fairness Monitoring

**Quarterly** or **when threshold exceeded**:

```
For each demographic group:
- Approval Rate difference > 5% → Audit required
- Rejection Rate skew > 10% → Review model
- Average Risk Score variance > 8 points → Investigate
```

### Corrective Actions

If bias detected:
1. Analyst reviews affected decisions
2. Adjust pricing/terms to account for disparity
3. Retrain model if systematic bias found
4. Document in compliance report
5. Report to Board within 30 days

---

## 6. Portfolio Risk Limits

Compliance must monitor:

| Metric | Limit | Review Trigger |
|--------|-------|----------------|
| High Risk Concentration | < 15% | > 15% = reduce High Risk approvals |
| Single Borrower Exposure | < $500K | > $500K = Board approval |
| Geographic Concentration | < 50% any one state | > 50% = diversify |
| Loan Int ent Concentration | < 40% any category | > 40% = diversify |
| Average Risk Score | 45-55 | Outside range = rebalance |

---

## 7. Approval Ratios & Targets

**As of v1.0.0:**

- **Target Approval Rate**: 68-75%
- **Target Rejection Rate**: 25-32%
- **Appeal/Override Rate**: 2-5% of total

**Monthly Reporting** required if:
- Approval Rate > 80% (too permissive)
- Approval Rate < 60% (too strict)
- Override Rate > 7% (too many reversals)

---

## 8. Special Policies

### Microfinance vs. Traditional

**Microfinance** (< $5,000):
- Standard approval rules apply
- Lower documentation requirements
- Community member preference
- Fast-track processing (24 hours)

**Traditional** (> $5,000):
- Enhanced verification required
- Collateral evaluation
- Longer review (48 hours)
- More detailed credit check

### Seasonal Lending

**Agricultural/Seasonal Businesses**:
- Adjust LTI thresholds based on off-season
- Accept seasonal income documentation
- May approve higher risk during growing season

### Startup Founders

**Special approval path available**:
- Cannot use traditional income verification
- Must have minimum $100K liquid capital
- Personal guarantee required
- Review by Venture Lending specialist

---

## 9. Exceptions & Appeals

### Appeal Process

Rejected applicants can appeal within 30 days:

1. Submit appeal with new information
2. Escalated to different analyst (not original)
3. Analyst reviews within 5 business days
4. Final decision binding

### Appeal Approval Criteria

- New material information provided
- Original decision had data error
- Material change in applicant circumstances
- Comparable applicant approved (discrimination concern)

### Appeal Statistics (Quarterly Reporting)

- Total appeals received
- Appeals approved
- Appeals rejected
- Time to decision

---

## 10. Compliance & Audit

### Mandatory Audit Procedures (Quarterly)

- [ ] Random sample of 50 decisions (approval + rejection)
- [ ] Verify documentation complete
- [ ] Check risk score calculation accuracy
- [ ] Confirm audit trail present
- [ ] Review overrides for legitimacy
- [ ] Bias analysis by demographic group
- [ ] Report findings to Board

### Annual Model Review

- [ ] Validation against actual defaults
- [ ] Model discrimination testing
- [ ] Recommendations for model update
- [ ] Training for staff on policy changes
- [ ] Policy exception analysis

---

## 11. Conflict of Interest

Analysts/Reviewers cannot approve applications where:

- Applicant is family member
- Personal financial interest with applicant
- Referral fee or compensation involved
- Competitor of existing customer
- Content of applicant-analyst communication

**Process**: Reassign to neutral reviewer immediately

---

## 12. Data Retention & Deletion

**Retention Periods**:
- Approved loans: 7 years post-payoff
- Rejected applications: 1 year (unless appeal pending)
- Audit trail: 7 years (regulatory requirement)
- Personal data: Per GDPR/CCPA

**Deletion Process**:
- Mark record "deleted" in database
- Maintain audit trail showing deletion
- Never permanently erase (for audit purposes)
- Generate deletion report quarterly

---

## 13. Policy Exceptions

### When Exceptions Are Allowed

Up to 2% of quarterly decisions can use exceptions if:
1. Documented by named officer
2. Approved by line manager
3. Reviewed by compliance
4. Reported in monthly exception report

### Exception Documentation Required

```
- Exception ID
- Applicant ID
- Decision Date
- Officer Name
- Requested Exception
- Business Justification
- Approval Authority
- Risk Assessment of Exception
```

---

## 14. Monitoring & Alerts

### Real-Time Alerts

System alerts when:
- Approval rate exceeds 80% daily
- Rejection rate exceeds 35% daily
- High Risk approvals > 20% weekly
- Override rate > 10% daily

### Action Required

- Alert reviewed within 2 hours
- Root cause identified
- Corrective action documented
- Senior management notified if systematic

---

## 15. Policy Review & Updates

- **Review Frequency**: Annually
- **Next Review**: January 2025
- **Policy Effective Date**: January 15, 2024
- **Previous Version**: Not applicable (v1.0 initial)

---

## Appendix A: Decision Matrix

```
┌─────────────────────────────────────────────┐
│ DECISION MATRIX BY RISK SCORE & CONFIDENCE  │
├──────────┬──────────┬──────────┬────────────┤
│ Risk     │ Low Conf │ Med Conf │ High Conf  │
│ Score    │ (55-65%) │ (65-85%) │ (85-100%)  │
├──────────┼──────────┼──────────┼────────────┤
│ 0-30     │ APPROVE  │ APPROVE  │ AUTO-APP   │
│ (Low)    │ Review   │ Normal   │ Log Only   │
├──────────┼──────────┼──────────┼────────────┤
│ 31-65    │ REVIEW   │ REVIEW   │ APPROVE    │
│ (Medium) │ Escalate │ Analyst  │ Standard   │
├──────────┼──────────┼──────────┼────────────┤
│ 66-100   │ REJECT   │ REVIEW   │ REVIEW     │
│ (High)   │ Escalate │ Officer  │ Manager    │
└──────────┴──────────┴──────────┴────────────┘
```

---

**Policy Version**: 1.0.0  
**Effective Date**: 2024-01-15  
**Next Review**: 2025-01-15  
**Approved By**: Board of Directors
