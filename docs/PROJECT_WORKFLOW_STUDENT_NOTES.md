# MicroRisk AI - Student Notes (One Page)

## Project in 10 Seconds
- User enters loan details.
- App sends data to backend.
- Backend asks AI model.
- Model returns decision + reason.
- UI shows APPROVED/REJECTED + explanation + risk graph.

## Professional Terms To Use
- Credit Risk Intelligence Platform
- Explainable Lending Decision Engine
- AI-Assisted Underwriting
- Risk Scoring and Decision Support
- Portfolio Risk Monitoring
- Delinquency Early Warning Signals
- Compliance-Ready Decision Audit Trail
- Real-Time Applicant Risk Profiling
- Human-in-the-Loop Approval Workflow
- Model Governance and Drift Monitoring

## Full Flow (Very Short)
1. Open app and login.
2. Fill parameter boxes in dashboard.
3. Click EXECUTE NEURAL AUDIT.
4. Frontend sends POST /api/predict.
5. FastAPI validates input.
6. model.py calls Gemini API.
7. Response comes back with prediction and explanation.
8. Frontend displays result and bars.

## Key Files and Their Job

## static folder
- [static/index.html](../static/index.html): page loader + API call + render output.
- [static/login.html](../static/login.html): login/registration screen.
- [static/dashboard.html](../static/dashboard.html): form fields and result section.
- [static/style.css](../static/style.css): UI styling and layout.

## Config.py
- [Config.py](../Config.py): sample loan records.
- Used for testing/demo helpers.

## main.py
- [main.py](../main.py): FastAPI entry point.
- Serves HTML pages.
- Mounts static files.
- Defines LoanData schema.
- Receives /api/predict request.
- Calls prediction function from model.py.
- Returns JSON result.

## model.py
- [model.py](../model.py): AI decision logic.
- Main live function: predict_with_gemini(data_point).
- Builds prompt and calls Gemini API.
- Returns:
  - prediction
  - reason.summary
  - reason.detailed_breakdown
  - overall_conclusion

## Simple Input and Output

Input:
```json
{
  "person_age": 28,
  "person_income": 45000,
  "loan_amnt": 9000,
  "loan_int_rate": 11.5,
  "repayment_history": "good"
}
```

Output:
```json
{
  "prediction": 0,
  "reason": {
    "summary": "Low risk profile",
    "detailed_breakdown": "Stable income and healthy repayment behavior."
  },
  "overall_conclusion": "Approved with normal monitoring."
}
```

## Meaning of prediction
- 0 = APPROVED
- 1 = REJECTED

## If UI updates are not visible
1. Restart server.
2. Open root route /.
3. Press Ctrl+F5.

## Exam/Viva One-Liner
- Frontend collects data -> FastAPI validates -> Gemini predicts -> UI shows decision, reason, and graph.
