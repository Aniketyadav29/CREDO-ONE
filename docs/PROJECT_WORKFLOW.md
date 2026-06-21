# MicroRisk AI - Workflow and Terminology Standard

## Professional Terminology Standard

Use these terms consistently in UI, docs, and presentations:
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

## Simple Project Workflow

1. User enters applicant details in dashboard.
2. Frontend sends POST request to `/api/predict`.
3. FastAPI validates payload using `LoanData`.
4. Backend calls Gemini through `predict_with_gemini()`.
5. API returns decision and explanation JSON.
6. Frontend displays status, explanation, and profiling graph.

## File-Wise Role Summary

- [main.py](../main.py): API routes, schema validation, response handling
- [model.py](../model.py): AI decision and explanation generation
- [static/index.html](../static/index.html): request orchestration and UI rendering
- [static/dashboard.html](../static/dashboard.html): input forms and output panels
- [static/login.html](../static/login.html): business and product information layer
- [Config.py](../Config.py): sample applicant records used by helper utilities

## Presentation One-Liner

CREDO AI is a Credit Risk Intelligence Platform combining AI-Assisted Underwriting, Real-Time Applicant Risk Profiling, and a Compliance-Ready Decision Audit Trail with Human-in-the-Loop Approval Workflow.
