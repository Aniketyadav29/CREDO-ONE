# API Contract Documentation
## Credit Risk Intelligence Platform v1.0.0

### Base URL
```
http://localhost:8000
```

### Authentication
All endpoints requiring role-based access use request headers:
- `X-User-Role`: User's role (admin, analyst, reviewer, viewer)
- `X-User-ID`: Unique identifier for the user

### Response Format
All endpoints return JSON with consistent structure:
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {}
}
```

---

## Endpoints

### 1. Health Check
**GET** `/health`

Returns platform availability status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### 2. Make Prediction
**POST** `/api/predict`

**Headers:**
- `X-User-Role`: User role (required for RBAC)
- `X-User-ID`: User identifier (optional)

**Request Body:**
```json
{
  "person_income": 65000,
  "loan_amnt": 15000,
  "loan_int_rate": 8.5,
  "loan_intent": "PERSONAL",
  "person_age": 35,
  "person_emp_length": 10,
  "loan_percent_income": 0.23,
  "person_home_ownership": "MORTGAGE",
  "repayment_history": "good",
  "loan_purpose_category": "productive_asset",
  "applicant_id": "APP-2024-001",
  "user_id": "john_doe"
}
```

**Response (200 OK):**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "prediction": 0,
  "confidence": 0.87,
  "risk_score": 28.5,
  "risk_band": "Low Risk",
  "model_version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "reason": {
    "summary": "Application is APPROVED based on strong financial profile.",
    "detailed_breakdown": "Stable employment history, good repayment record, moderate LTI ratio."
  },
  "decision_factors": [
    {
      "factor": "Stable Employment (10 years)",
      "impact": "positive",
      "value": 10
    },
    {
      "factor": "Good Repayment History",
      "impact": "positive",
      "value": 15
    },
    {
      "factor": "Favorable Loan Terms",
      "impact": "positive",
      "value": 5
    }
  ],
  "positive_factors": [...],
  "negative_factors": [...],
  "overall_conclusion": "Application is APPROVED. Risk score 28.5/100 within acceptable range."
}
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": {
    "validation_errors": [
      "Age 25: must be between 18 and 75",
      "Invalid loan intent 'UNKNOWN'. Must be one of: PERSONAL, EDUCATION..."
    ]
  }
}
```

---

### 3. Manual Override
**POST** `/api/override`

Submit a manual override for a previous decision (admin, reviewer roles only).

**Request Body:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "override_decision": 0,
  "reason": "Collateral provided by applicant - special circumstance",
  "user_id": "alice_reviewer"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Decision overridden and logged",
  "original_decision": 1,
  "override_decision": 0,
  "timestamp": "2024-01-15T10:32:00Z"
}
```

---

### 4. Get Applicant History
**GET** `/api/applicant/{applicant_id}/history`

Retrieve prediction history for a specific applicant.

**Response:**
```json
{
  "applicant_id": "APP-2024-001",
  "history_count": 3,
  "history": [
    {
      "request_id": "550e8400-e29b-41d4-a716-446655440000",
      "prediction": 0,
      "confidence": 0.87,
      "risk_band": "Low Risk",
      "risk_score": 28.5,
      "model_version": "1.0.0",
      "timestamp": "2024-01-15T10:30:00Z",
      "is_overridden": false
    }
  ],
  "timestamp": "2024-01-15T10:35:00Z"
}
```

---

### 5. Platform Statistics
**GET** `/api/stats?days=30`

Get operational KPIs and approval statistics.

**Query Parameters:**
- `days`: Number of days to analyze (default: 30)

**Response:**
```json
{
  "period_days": 30,
  "statistics": {
    "total": 542,
    "approved": 380,
    "rejected": 162,
    "approval_rate": 70.11,
    "rejection_rate": 29.89,
    "avg_risk_score": 42.3,
    "avg_confidence": 0.82
  },
  "timestamp": "2024-01-15T10:35:00Z"
}
```

---

### 6. Audit Trail Export
**GET** `/api/audit-trail?start_date=2024-01-01&end_date=2024-01-31`

Export complete audit trail for compliance (admin only).

**Response:**
```json
{
  "record_count": 542,
  "audit_trail": [
    {
      "id": 1,
      "request_id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "john_doe",
      "applicant_id": "APP-2024-001",
      "prediction": 0,
      "confidence": 0.87,
      "risk_band": "Low Risk",
      "risk_score": 28.5,
      "model_version": "1.0.0",
      "timestamp": "2024-01-15T10:30:00Z",
      "is_overridden": false,
      "override_reason": null,
      "override_decision": null
    }
  ],
  "timestamp": "2024-01-15T10:35:00Z"
}
```

---

## Input Validation Rules

### Numeric Ranges
- **Age**: 18-75 years
- **Annual Income**: $1,000 - $1,000,000
- **Loan Amount**: $500 - $100,000
- **Interest Rate**: 1% - 35%
- **Employment Years**: 0-60
- **Loan-to-Income Ratio**: 0.01 - 1.0

### Enumeration Values
- **Loan Intent**: PERSONAL, EDUCATION, MEDICAL, VENTURE, MORTGAGE, AUTO, HOME_IMPROVEMENT, DEBT_CONSOLIDATION
- **Home Ownership**: RENT, OWN, MORTGAGE, OTHER
- **Repayment History**: excellent, good, average, fair, poor, defaulted
- **Loan Purpose**: productive_asset, emergency_need, consumption, business_expansion, education, housing

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Successful prediction |
| 400 | Invalid input - validation failed |
| 403 | Insufficient permissions for action |
| 404 | Resource not found |
| 422 | Unprocessable entity - business constraint violation |
| 500 | Internal server error |

---

## Rate Limiting

- **Limit**: 60 requests per minute per user
- **Headers in Response**:
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

---

## Request/Response Headers

All responses include:
- `X-Request-ID`: Unique request identifier for tracing
- `X-Process-Time`: Total processing time in milliseconds
- `X-Model-Version`: Current model version used

---

## Example Request Curl

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
  -H "X-User-ID: john_doe" \
  -d '{
    "person_income": 65000,
    "loan_amnt": 15000,
    "loan_int_rate": 8.5,
    "loan_intent": "PERSONAL",
    "person_age": 35,
    "person_emp_length": 10,
    "loan_percent_income": 0.23,
    "person_home_ownership": "MORTGAGE",
    "repayment_history": "good",
    "loan_purpose_category": "productive_asset"
  }'
```

---

## Webhooks (Future Enhancement)

Planned for v1.1.0:
- Prediction completed webhook
- Override logged webhook
- Daily statistics summary webhook

---

**API Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Maintained By**: Credit Risk Intelligence Platform Team
