"""
Configuration Management for Credit Risk Intelligence Platform
Handles environment variables, validation rules, and business constraints.
"""
import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple

# Load environment variables from .env file
load_dotenv()

# --- API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# --- Security Configuration ---
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ENABLE_ROLE_BASED_RBAC = os.getenv("ENABLE_ROLE_BASED_ACCESS", "true").lower() == "true"

# --- JWT Authentication ---
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("APP_SECRET_KEY", "dev-secret-key-change-in-production"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")
ENABLE_STRUCTURED_LOGGING = os.getenv("ENABLE_STRUCTURED_LOGGING", "true").lower() == "true"

# --- Rate Limiting ---
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./credit_risk_history.db")
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")

# --- Application Settings ---
APP_ENV = os.getenv("APP_ENV", "development")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key-change-in-production")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

# --- Fairness & Bias Monitoring ---
ENABLE_FAIRNESS_CHECKS = os.getenv("ENABLE_FAIRNESS_CHECKS", "true").lower() == "true"
FAIRNESS_CHECK_INTERVAL = int(os.getenv("FAIRNESS_CHECK_INTERVAL", "100"))

# --- PDF Export ---
ENABLE_PDF_EXPORT = os.getenv("ENABLE_PDF_EXPORT", "true").lower() == "true"
PDF_LOGO_PATH = os.getenv("PDF_LOGO_PATH", "static/logo.png")

# --- Audit & Compliance ---
ENABLE_AUDIT_TRAIL = os.getenv("ENABLE_AUDIT_TRAIL", "true").lower() == "true"
AUDIT_LOG_FILE = os.getenv("AUDIT_LOG_FILE", "logs/audit.log")

# --- User Roles ---
USER_ROLES = {
    "admin": ["view_all", "approve", "override", "manage_users", "export_data"],
    "analyst": ["view_cases", "predict", "export_own_data"],
    "reviewer": ["view_cases", "approve_override", "export_own_data"],
    "viewer": ["view_cases"]
}

# --- Business Constraints & Validation Rules ---
BUSINESS_CONSTRAINTS = {
    "person_age": {
        "min": 18,
        "max": 75,
        "description": "Applicant age must be between 18 and 75"
    },
    "person_income": {
        "min": 1000,
        "max": 1000000,
        "description": "Annual income must be between $1K and $1M"
    },
    "loan_amnt": {
        "min": 500,
        "max": 100000,
        "description": "Loan amount must be between $500 and $100K"
    },
    "loan_percent_income": {
        "min": 0.01,
        "max": 1.0,
        "description": "Loan-to-income ratio must be between 0.01 and 1.0"
    },
    "loan_int_rate": {
        "min": 1.0,
        "max": 35.0,
        "description": "Interest rate must be between 1% and 35%"
    },
    "person_emp_length": {
        "min": 0,
        "max": 60,
        "description": "Employment length must be 0-60 years"
    }
}

# --- Validation Enum Values ---
VALID_LOAN_INTENTS = [
    "PERSONAL",
    "EDUCATION",
    "MEDICAL",
    "VENTURE",
    "MORTGAGE",
    "AUTO",
    "HOME_IMPROVEMENT",
    "DEBT_CONSOLIDATION"
]

VALID_HOME_OWNERSHIP = [
    "RENT",
    "OWN",
    "MORTGAGE",
    "OTHER"
]

VALID_REPAYMENT_HISTORY = [
    "excellent",
    "good",
    "average",
    "fair",
    "poor",
    "defaulted"
]

VALID_LOAN_PURPOSE = [
    "productive_asset",
    "emergency_need",
    "consumption",
    "business_expansion",
    "education",
    "housing"
]

# --- Risk Assessment Thresholds ---
RISK_THRESHOLDS = {
    "low_risk": {"min": 0, "max": 30},
    "medium_risk": {"min": 31, "max": 65},
    "high_risk": {"min": 66, "max": 100}
}

# --- Approval Thresholds by Role ---
APPROVAL_THRESHOLDS_BY_ROLE = {
    "admin": 0,      # Can approve any risk level
    "analyst": 40,   # Can approve up to medium-low risk
    "reviewer": 50   # Can review high-risk cases
}

# --- Override Reasons ---
VALID_OVERRIDE_REASONS = [
    "special_circumstance",
    "relationship_manager_recommendation",
    "business_development_priority",
    "portfolio_balancing",
    "seasonal_adjustment",
    "collateral_provided",
    "guarantor_available",
    "other"
]

# --- Feature Flags ---
FEATURES = {
    "enable_confidence_scores": True,
    "enable_risk_bands": True,
    "enable_factor_analysis": True,
    "enable_manual_override": True,
    "enable_history_timeline": True,
    "enable_pdf_export": True,
    "enable_monitoring_dashboard": True,
    "enable_bias_checks": True
}

def validate_business_constraints(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate input data against business constraints.
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    # Validate person_age
    age = data.get("person_age")
    if age is not None:
        if not (BUSINESS_CONSTRAINTS["person_age"]["min"] <= age <= BUSINESS_CONSTRAINTS["person_age"]["max"]):
            errors.append(f"Age {age}: {BUSINESS_CONSTRAINTS['person_age']['description']}")
    
    # Validate person_income
    income = data.get("person_income")
    if income is not None:
        if not (BUSINESS_CONSTRAINTS["person_income"]["min"] <= income <= BUSINESS_CONSTRAINTS["person_income"]["max"]):
            errors.append(f"Income {income}: {BUSINESS_CONSTRAINTS['person_income']['description']}")
    
    # Validate loan_amnt
    loan_amnt = data.get("loan_amnt")
    if loan_amnt is not None:
        if not (BUSINESS_CONSTRAINTS["loan_amnt"]["min"] <= loan_amnt <= BUSINESS_CONSTRAINTS["loan_amnt"]["max"]):
            errors.append(f"Loan amount {loan_amnt}: {BUSINESS_CONSTRAINTS['loan_amnt']['description']}")
    
    # Validate loan_percent_income
    lpi = data.get("loan_percent_income")
    if lpi is not None:
        if not (BUSINESS_CONSTRAINTS["loan_percent_income"]["min"] <= lpi <= BUSINESS_CONSTRAINTS["loan_percent_income"]["max"]):
            errors.append(f"Loan-to-income {lpi}: {BUSINESS_CONSTRAINTS['loan_percent_income']['description']}")
    
    # Validate loan_int_rate
    int_rate = data.get("loan_int_rate")
    if int_rate is not None:
        if not (BUSINESS_CONSTRAINTS["loan_int_rate"]["min"] <= int_rate <= BUSINESS_CONSTRAINTS["loan_int_rate"]["max"]):
            errors.append(f"Interest rate {int_rate}: {BUSINESS_CONSTRAINTS['loan_int_rate']['description']}")
    
    # Validate person_emp_length
    emp_len = data.get("person_emp_length")
    if emp_len is not None:
        if not (BUSINESS_CONSTRAINTS["person_emp_length"]["min"] <= emp_len <= BUSINESS_CONSTRAINTS["person_emp_length"]["max"]):
            errors.append(f"Employment length {emp_len}: {BUSINESS_CONSTRAINTS['person_emp_length']['description']}")
    
    # Validate loan_intent enumeration
    intent = data.get("loan_intent")
    if intent and intent not in VALID_LOAN_INTENTS:
        errors.append(f"Invalid loan intent '{intent}'. Must be one of: {', '.join(VALID_LOAN_INTENTS)}")
    
    # Validate home_ownership enumeration
    home = data.get("person_home_ownership")
    if home and home not in VALID_HOME_OWNERSHIP:
        errors.append(f"Invalid home ownership '{home}'. Must be one of: {', '.join(VALID_HOME_OWNERSHIP)}")
    
    # Validate repayment_history enumeration
    repayment = data.get("repayment_history")
    if repayment and repayment not in VALID_REPAYMENT_HISTORY:
        errors.append(f"Invalid repayment history '{repayment}'. Must be one of: {', '.join(VALID_REPAYMENT_HISTORY)}")
    
    return len(errors) == 0, errors

def get_risk_band(risk_score: float) -> str:
    """Determine risk band based on score."""
    if RISK_THRESHOLDS["low_risk"]["min"] <= risk_score <= RISK_THRESHOLDS["low_risk"]["max"]:
        return "Low Risk"
    elif RISK_THRESHOLDS["medium_risk"]["min"] <= risk_score <= RISK_THRESHOLDS["medium_risk"]["max"]:
        return "Medium Risk"
    else:
        return "High Risk"

def can_approve(user_role: str, risk_score: float) -> bool:
    """Check if user role can approve based on risk score."""
    if user_role not in APPROVAL_THRESHOLDS_BY_ROLE:
        return False
    return risk_score <= APPROVAL_THRESHOLDS_BY_ROLE[user_role]

# --- Sample Loan Data (for reference/testing) ---
loan_data = [
    {
        'person_age': 21,
        'person_income': 9600,
        'person_emp_length': 5,
        'loan_amnt': 1000,
        'loan_int_rate': 12.9,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 23,
        'person_income': 45000,
        'person_emp_length': 2,
        'loan_amnt': 5000,
        'loan_int_rate': 7.5,
        'loan_percent_income': 0.11,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 25,
        'person_income': 20000,
        'person_emp_length': 8,
        'loan_amnt': 2000,
        'loan_int_rate': 14.2,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 30,
        'person_income': 70000,
        'person_emp_length': 10,
        'loan_amnt': 10000,
        'loan_int_rate': 8.8,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'RENT',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 28,
        'person_income': 55000,
        'person_emp_length': 4,
        'loan_amnt': 8000,
        'loan_int_rate': 9.5,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 35,
        'person_income': 80000,
        'person_emp_length': 15,
        'loan_amnt': 15000,
        'loan_int_rate': 6.5,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 45,
        'person_income': 95000,
        'person_emp_length': 20,
        'loan_amnt': 20000,
        'loan_int_rate': 5.9,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 22,
        'person_income': 30000,
        'person_emp_length': 1,
        'loan_amnt': 2500,
        'loan_int_rate': 13.5,
        'loan_percent_income': 0.08,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 29,
        'person_income': 60000,
        'person_emp_length': 6,
        'loan_amnt': 7500,
        'loan_int_rate': 10.1,
        'loan_percent_income': 0.12,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 31,
        'person_income': 72000,
        'person_emp_length': 9,
        'loan_amnt': 12000,
        'loan_int_rate': 7.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 24,
        'person_income': 35000,
        'person_emp_length': 3,
        'loan_amnt': 3000,
        'loan_int_rate': 11.5,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 32,
        'person_income': 65000,
        'person_emp_length': 7,
        'loan_amnt': 6000,
        'loan_int_rate': 8.1,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 26,
        'person_income': 42000,
        'person_emp_length': 5,
        'loan_amnt': 4000,
        'loan_int_rate': 13.9,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 38,
        'person_income': 85000,
        'person_emp_length': 12,
        'loan_amnt': 11000,
        'loan_int_rate': 7.2,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 40,
        'person_income': 100000,
        'person_emp_length': 18,
        'loan_amnt': 18000,
        'loan_int_rate': 6.1,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 27,
        'person_income': 50000,
        'person_emp_length': 2,
        'loan_amnt': 3500,
        'loan_int_rate': 12.8,
        'loan_percent_income': 0.07,
        'person_home_ownership': 'RENT',
        'loan_intent': 'PERSONAL',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 33,
        'person_income': 75000,
        'person_emp_length': 8,
        'loan_amnt': 9000,
        'loan_int_rate': 9.2,
        'loan_percent_income': 0.12,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'EDUCATION',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 42,
        'person_income': 92000,
        'person_emp_length': 16,
        'loan_amnt': 15000,
        'loan_int_rate': 6.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 29,
        'person_income': 58000,
        'person_emp_length': 4,
        'loan_amnt': 6500,
        'loan_int_rate': 10.5,
        'loan_percent_income': 0.11,
        'person_home_ownership': 'RENT',
        'loan_intent': 'PERSONAL',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 34,
        'person_income': 78000,
        'person_emp_length': 10,
        'loan_amnt': 13000,
        'loan_int_rate': 8.5,
        'loan_percent_income': 0.17,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 22,
        'person_income': 32000,
        'person_emp_length': 2,
        'loan_amnt': 4000,
        'loan_int_rate': 11.8,
        'loan_percent_income': 0.12,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 25,
        'person_income': 48000,
        'person_emp_length': 4,
        'loan_amnt': 5500,
        'loan_int_rate': 9.2,
        'loan_percent_income': 0.11,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 30,
        'person_income': 68000,
        'person_emp_length': 7,
        'loan_amnt': 9500,
        'loan_int_rate': 8.5,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 36,
        'person_income': 75000,
        'person_emp_length': 11,
        'loan_amnt': 11000,
        'loan_int_rate': 7.1,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 41,
        'person_income': 90000,
        'person_emp_length': 17,
        'loan_amnt': 16000,
        'loan_int_rate': 6.2,
        'loan_percent_income': 0.17,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 23,
        'person_income': 38000,
        'person_emp_length': 1,
        'loan_amnt': 3200,
        'loan_int_rate': 13.2,
        'loan_percent_income': 0.08,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 28,
        'person_income': 52000,
        'person_emp_length': 6,
        'loan_amnt': 7000,
        'loan_int_rate': 10.5,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 34,
        'person_income': 74000,
        'person_emp_length': 9,
        'loan_amnt': 12500,
        'loan_int_rate': 8.1,
        'loan_percent_income': 0.17,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 88000,
        'person_emp_length': 13,
        'loan_amnt': 14000,
        'loan_int_rate': 7.0,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 98000,
        'person_emp_length': 19,
        'loan_amnt': 19000,
        'loan_int_rate': 6.0,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 28000,
        'person_emp_length': 3,
        'loan_amnt': 2500,
        'loan_int_rate': 12.5,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 49000,
        'person_emp_length': 5,
        'loan_amnt': 6000,
        'loan_int_rate': 9.8,
        'loan_percent_income': 0.12,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 71000,
        'person_emp_length': 8,
        'loan_amnt': 10500,
        'loan_int_rate': 8.3,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 83000,
        'person_emp_length': 14,
        'loan_amnt': 13000,
        'loan_int_rate': 7.4,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 96000,
        'person_emp_length': 18,
        'loan_amnt': 18500,
        'loan_int_rate': 6.0,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 40000,
        'person_emp_length': 2,
        'loan_amnt': 3800,
        'loan_int_rate': 11.0,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 58000,
        'person_emp_length': 6,
        'loan_amnt': 8000,
        'loan_int_rate': 10.2,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 77000,
        'person_emp_length': 10,
        'loan_amnt': 13500,
        'loan_int_rate': 8.0,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 89000,
        'person_emp_length': 12,
        'loan_amnt': 14500,
        'loan_int_rate': 7.0,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 99000,
        'person_emp_length': 19,
        'loan_amnt': 21000,
        'loan_int_rate': 6.0,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 29000,
        'person_emp_length': 3,
        'loan_amnt': 2700,
        'loan_int_rate': 12.6,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 50000,
        'person_emp_length': 5,
        'loan_amnt': 6200,
        'loan_int_rate': 9.9,
        'loan_percent_income': 0.12,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 72000,
        'person_emp_length': 8,
        'loan_amnt': 10700,
        'loan_int_rate': 8.4,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 84000,
        'person_emp_length': 14,
        'loan_amnt': 13200,
        'loan_int_rate': 7.5,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 97000,
        'person_emp_length': 18,
        'loan_amnt': 18700,
        'loan_int_rate': 6.1,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 41000,
        'person_emp_length': 2,
        'loan_amnt': 3900,
        'loan_int_rate': 11.1,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 59000,
        'person_emp_length': 6,
        'loan_amnt': 8200,
        'loan_int_rate': 10.3,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 78000,
        'person_emp_length': 10,
        'loan_amnt': 13700,
        'loan_int_rate': 8.1,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 90000,
        'person_emp_length': 12,
        'loan_amnt': 14700,
        'loan_int_rate': 7.1,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 100000,
        'person_emp_length': 19,
        'loan_amnt': 21200,
        'loan_int_rate': 6.1,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 30000,
        'person_emp_length': 3,
        'loan_amnt': 2800,
        'loan_int_rate': 12.7,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 51000,
        'person_emp_length': 5,
        'loan_amnt': 6400,
        'loan_int_rate': 10.0,
        'loan_percent_income': 0.12,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 73000,
        'person_emp_length': 8,
        'loan_amnt': 10900,
        'loan_int_rate': 8.5,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 85000,
        'person_emp_length': 14,
        'loan_amnt': 13400,
        'loan_int_rate': 7.6,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 98000,
        'person_emp_length': 18,
        'loan_amnt': 18900,
        'loan_int_rate': 6.2,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 42000,
        'person_emp_length': 2,
        'loan_amnt': 4000,
        'loan_int_rate': 11.2,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 60000,
        'person_emp_length': 6,
        'loan_amnt': 8400,
        'loan_int_rate': 10.4,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 79000,
        'person_emp_length': 10,
        'loan_amnt': 13900,
        'loan_int_rate': 8.2,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 91000,
        'person_emp_length': 12,
        'loan_amnt': 14900,
        'loan_int_rate': 7.2,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 101000,
        'person_emp_length': 19,
        'loan_amnt': 21400,
        'loan_int_rate': 6.3,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 31000,
        'person_emp_length': 3,
        'loan_amnt': 2900,
        'loan_int_rate': 12.8,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 52000,
        'person_emp_length': 5,
        'loan_amnt': 6600,
        'loan_int_rate': 10.1,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 74000,
        'person_emp_length': 8,
        'loan_amnt': 11100,
        'loan_int_rate': 8.6,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 86000,
        'person_emp_length': 14,
        'loan_amnt': 13600,
        'loan_int_rate': 7.7,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 99000,
        'person_emp_length': 18,
        'loan_amnt': 19100,
        'loan_int_rate': 6.3,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 43000,
        'person_emp_length': 2,
        'loan_amnt': 4100,
        'loan_int_rate': 11.3,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 61000,
        'person_emp_length': 6,
        'loan_amnt': 8600,
        'loan_int_rate': 10.5,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 80000,
        'person_emp_length': 10,
        'loan_amnt': 14100,
        'loan_int_rate': 8.3,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 92000,
        'person_emp_length': 12,
        'loan_amnt': 15100,
        'loan_int_rate': 7.3,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 102000,
        'person_emp_length': 19,
        'loan_amnt': 21600,
        'loan_int_rate': 6.3,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 32000,
        'person_emp_length': 3,
        'loan_amnt': 3000,
        'loan_int_rate': 12.9,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 53000,
        'person_emp_length': 5,
        'loan_amnt': 6800,
        'loan_int_rate': 10.2,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 75000,
        'person_emp_length': 8,
        'loan_amnt': 11300,
        'loan_int_rate': 8.7,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 87000,
        'person_emp_length': 14,
        'loan_amnt': 13800,
        'loan_int_rate': 7.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 100000,
        'person_emp_length': 18,
        'loan_amnt': 19300,
        'loan_int_rate': 6.4,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 44000,
        'person_emp_length': 2,
        'loan_amnt': 4200,
        'loan_int_rate': 11.4,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 62000,
        'person_emp_length': 6,
        'loan_amnt': 8800,
        'loan_int_rate': 10.6,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 81000,
        'person_emp_length': 10,
        'loan_amnt': 14300,
        'loan_int_rate': 8.4,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 93000,
        'person_emp_length': 12,
        'loan_amnt': 15300,
        'loan_int_rate': 7.4,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 103000,
        'person_emp_length': 19,
        'loan_amnt': 21800,
        'loan_int_rate': 6.4,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 33000,
        'person_emp_length': 3,
        'loan_amnt': 3100,
        'loan_int_rate': 13.0,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 54000,
        'person_emp_length': 5,
        'loan_amnt': 7000,
        'loan_int_rate': 10.3,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 76000,
        'person_emp_length': 8,
        'loan_amnt': 11500,
        'loan_int_rate': 8.8,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 88000,
        'person_emp_length': 14,
        'loan_amnt': 14000,
        'loan_int_rate': 7.9,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 101000,
        'person_emp_length': 18,
        'loan_amnt': 19500,
        'loan_int_rate': 6.5,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 45000,
        'person_emp_length': 2,
        'loan_amnt': 4300,
        'loan_int_rate': 11.5,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 63000,
        'person_emp_length': 6,
        'loan_amnt': 9000,
        'loan_int_rate': 10.7,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 82000,
        'person_emp_length': 10,
        'loan_amnt': 14500,
        'loan_int_rate': 8.5,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 94000,
        'person_emp_length': 12,
        'loan_amnt': 15500,
        'loan_int_rate': 7.5,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 104000,
        'person_emp_length': 19,
        'loan_amnt': 22000,
        'loan_int_rate': 6.5,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 34000,
        'person_emp_length': 3,
        'loan_amnt': 3200,
        'loan_int_rate': 13.1,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 55000,
        'person_emp_length': 5,
        'loan_amnt': 7200,
        'loan_int_rate': 10.4,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 77000,
        'person_emp_length': 8,
        'loan_amnt': 11700,
        'loan_int_rate': 8.9,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 89000,
        'person_emp_length': 14,
        'loan_amnt': 14200,
        'loan_int_rate': 8.0,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 102000,
        'person_emp_length': 18,
        'loan_amnt': 19700,
        'loan_int_rate': 6.6,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 46000,
        'person_emp_length': 2,
        'loan_amnt': 4400,
        'loan_int_rate': 11.6,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 64000,
        'person_emp_length': 6,
        'loan_amnt': 9200,
        'loan_int_rate': 10.8,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 83000,
        'person_emp_length': 10,
        'loan_amnt': 14700,
        'loan_int_rate': 8.6,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 95000,
        'person_emp_length': 12,
        'loan_amnt': 15700,
        'loan_int_rate': 7.6,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 105000,
        'person_emp_length': 19,
        'loan_amnt': 22200,
        'loan_int_rate': 6.6,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 35000,
        'person_emp_length': 3,
        'loan_amnt': 3300,
        'loan_int_rate': 13.2,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 56000,
        'person_emp_length': 5,
        'loan_amnt': 7400,
        'loan_int_rate': 10.5,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 78000,
        'person_emp_length': 8,
        'loan_amnt': 11900,
        'loan_int_rate': 9.0,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 90000,
        'person_emp_length': 14,
        'loan_amnt': 14400,
        'loan_int_rate': 8.1,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 103000,
        'person_emp_length': 18,
        'loan_amnt': 19900,
        'loan_int_rate': 6.7,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 47000,
        'person_emp_length': 2,
        'loan_amnt': 4500,
        'loan_int_rate': 11.7,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 65000,
        'person_emp_length': 6,
        'loan_amnt': 9400,
        'loan_int_rate': 10.9,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 84000,
        'person_emp_length': 10,
        'loan_amnt': 14900,
        'loan_int_rate': 8.7,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 96000,
        'person_emp_length': 12,
        'loan_amnt': 15900,
        'loan_int_rate': 7.7,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 106000,
        'person_emp_length': 19,
        'loan_amnt': 22400,
        'loan_int_rate': 6.7,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 36000,
        'person_emp_length': 3,
        'loan_amnt': 3400,
        'loan_int_rate': 13.3,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 57000,
        'person_emp_length': 5,
        'loan_amnt': 7600,
        'loan_int_rate': 10.6,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 79000,
        'person_emp_length': 8,
        'loan_amnt': 12100,
        'loan_int_rate': 9.1,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 91000,
        'person_emp_length': 14,
        'loan_amnt': 14600,
        'loan_int_rate': 8.2,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 104000,
        'person_emp_length': 18,
        'loan_amnt': 20100,
        'loan_int_rate': 6.8,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 48000,
        'person_emp_length': 2,
        'loan_amnt': 4600,
        'loan_int_rate': 11.8,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 66000,
        'person_emp_length': 6,
        'loan_amnt': 9600,
        'loan_int_rate': 11.0,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 85000,
        'person_emp_length': 10,
        'loan_amnt': 15100,
        'loan_int_rate': 8.8,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 97000,
        'person_emp_length': 12,
        'loan_amnt': 16100,
        'loan_int_rate': 7.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 107000,
        'person_emp_length': 19,
        'loan_amnt': 22600,
        'loan_int_rate': 6.8,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 37000,
        'person_emp_length': 3,
        'loan_amnt': 3500,
        'loan_int_rate': 13.4,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 58000,
        'person_emp_length': 5,
        'loan_amnt': 7800,
        'loan_int_rate': 10.7,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 80000,
        'person_emp_length': 8,
        'loan_amnt': 12300,
        'loan_int_rate': 9.2,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 92000,
        'person_emp_length': 14,
        'loan_amnt': 14800,
        'loan_int_rate': 8.3,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 105000,
        'person_emp_length': 18,
        'loan_amnt': 20300,
        'loan_int_rate': 6.9,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 49000,
        'person_emp_length': 2,
        'loan_amnt': 4700,
        'loan_int_rate': 11.9,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 67000,
        'person_emp_length': 6,
        'loan_amnt': 9800,
        'loan_int_rate': 11.1,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 86000,
        'person_emp_length': 10,
        'loan_amnt': 15300,
        'loan_int_rate': 8.9,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 98000,
        'person_emp_length': 12,
        'loan_amnt': 16300,
        'loan_int_rate': 7.9,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 108000,
        'person_emp_length': 19,
        'loan_amnt': 22800,
        'loan_int_rate': 6.9,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 38000,
        'person_emp_length': 3,
        'loan_amnt': 3600,
        'loan_int_rate': 13.5,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 59000,
        'person_emp_length': 5,
        'loan_amnt': 8000,
        'loan_int_rate': 10.8,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 81000,
        'person_emp_length': 8,
        'loan_amnt': 12500,
        'loan_int_rate': 9.3,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 93000,
        'person_emp_length': 14,
        'loan_amnt': 15000,
        'loan_int_rate': 8.4,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 106000,
        'person_emp_length': 18,
        'loan_amnt': 20500,
        'loan_int_rate': 7.0,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 50000,
        'person_emp_length': 2,
        'loan_amnt': 4800,
        'loan_int_rate': 12.0,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 68000,
        'person_emp_length': 6,
        'loan_amnt': 10000,
        'loan_int_rate': 11.2,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 87000,
        'person_emp_length': 10,
        'loan_amnt': 15500,
        'loan_int_rate': 9.0,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 99000,
        'person_emp_length': 12,
        'loan_amnt': 16500,
        'loan_int_rate': 8.0,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 109000,
        'person_emp_length': 19,
        'loan_amnt': 23000,
        'loan_int_rate': 7.0,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 39000,
        'person_emp_length': 3,
        'loan_amnt': 3700,
        'loan_int_rate': 13.6,
        'loan_percent_income': 0.09,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 60000,
        'person_emp_length': 5,
        'loan_amnt': 8200,
        'loan_int_rate': 10.9,
        'loan_percent_income': 0.13,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 82000,
        'person_emp_length': 8,
        'loan_amnt': 12700,
        'loan_int_rate': 9.4,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 94000,
        'person_emp_length': 14,
        'loan_amnt': 15200,
        'loan_int_rate': 8.5,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 107000,
        'person_emp_length': 18,
        'loan_amnt': 20700,
        'loan_int_rate': 7.1,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 51000,
        'person_emp_length': 2,
        'loan_amnt': 4900,
        'loan_int_rate': 12.1,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 69000,
        'person_emp_length': 6,
        'loan_amnt': 10200,
        'loan_int_rate': 11.3,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 88000,
        'person_emp_length': 10,
        'loan_amnt': 15700,
        'loan_int_rate': 9.1,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 100000,
        'person_emp_length': 12,
        'loan_amnt': 16700,
        'loan_int_rate': 8.1,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 110000,
        'person_emp_length': 19,
        'loan_amnt': 23200,
        'loan_int_rate': 7.1,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 40000,
        'person_emp_length': 3,
        'loan_amnt': 3800,
        'loan_int_rate': 13.7,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 61000,
        'person_emp_length': 5,
        'loan_amnt': 8400,
        'loan_int_rate': 11.0,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 83000,
        'person_emp_length': 8,
        'loan_amnt': 12900,
        'loan_int_rate': 9.5,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 95000,
        'person_emp_length': 14,
        'loan_amnt': 15400,
        'loan_int_rate': 8.6,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 108000,
        'person_emp_length': 18,
        'loan_amnt': 20900,
        'loan_int_rate': 7.2,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 52000,
        'person_emp_length': 2,
        'loan_amnt': 5000,
        'loan_int_rate': 12.2,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 70000,
        'person_emp_length': 6,
        'loan_amnt': 10400,
        'loan_int_rate': 11.4,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 89000,
        'person_emp_length': 10,
        'loan_amnt': 15900,
        'loan_int_rate': 9.2,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 101000,
        'person_emp_length': 12,
        'loan_amnt': 16900,
        'loan_int_rate': 8.2,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 111000,
        'person_emp_length': 19,
        'loan_amnt': 23400,
        'loan_int_rate': 7.2,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 41000,
        'person_emp_length': 3,
        'loan_amnt': 3900,
        'loan_int_rate': 13.8,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 62000,
        'person_emp_length': 5,
        'loan_amnt': 8600,
        'loan_int_rate': 11.1,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 84000,
        'person_emp_length': 8,
        'loan_amnt': 13100,
        'loan_int_rate': 9.6,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 96000,
        'person_emp_length': 14,
        'loan_amnt': 15600,
        'loan_int_rate': 8.7,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 109000,
        'person_emp_length': 18,
        'loan_amnt': 21100,
        'loan_int_rate': 7.3,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 53000,
        'person_emp_length': 2,
        'loan_amnt': 5100,
        'loan_int_rate': 12.3,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 71000,
        'person_emp_length': 6,
        'loan_amnt': 10600,
        'loan_int_rate': 11.5,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 90000,
        'person_emp_length': 10,
        'loan_amnt': 16100,
        'loan_int_rate': 9.3,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 102000,
        'person_emp_length': 12,
        'loan_amnt': 17100,
        'loan_int_rate': 8.3,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 112000,
        'person_emp_length': 19,
        'loan_amnt': 23600,
        'loan_int_rate': 7.3,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 42000,
        'person_emp_length': 3,
        'loan_amnt': 4000,
        'loan_int_rate': 13.9,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 63000,
        'person_emp_length': 5,
        'loan_amnt': 8800,
        'loan_int_rate': 11.2,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 85000,
        'person_emp_length': 8,
        'loan_amnt': 13300,
        'loan_int_rate': 9.7,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 97000,
        'person_emp_length': 14,
        'loan_amnt': 15800,
        'loan_int_rate': 8.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 110000,
        'person_emp_length': 18,
        'loan_amnt': 21300,
        'loan_int_rate': 7.4,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 54000,
        'person_emp_length': 2,
        'loan_amnt': 5200,
        'loan_int_rate': 12.4,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 72000,
        'person_emp_length': 6,
        'loan_amnt': 10800,
        'loan_int_rate': 11.6,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 91000,
        'person_emp_length': 10,
        'loan_amnt': 16300,
        'loan_int_rate': 9.4,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 103000,
        'person_emp_length': 12,
        'loan_amnt': 17300,
        'loan_int_rate': 8.4,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 113000,
        'person_emp_length': 19,
        'loan_amnt': 23800,
        'loan_int_rate': 7.4,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 43000,
        'person_emp_length': 3,
        'loan_amnt': 4100,
        'loan_int_rate': 14.0,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 64000,
        'person_emp_length': 5,
        'loan_amnt': 9000,
        'loan_int_rate': 11.3,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 86000,
        'person_emp_length': 8,
        'loan_amnt': 13500,
        'loan_int_rate': 9.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 98000,
        'person_emp_length': 14,
        'loan_amnt': 16000,
        'loan_int_rate': 8.9,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 111000,
        'person_emp_length': 18,
        'loan_amnt': 21500,
        'loan_int_rate': 7.5,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 55000,
        'person_emp_length': 2,
        'loan_amnt': 5300,
        'loan_int_rate': 12.5,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 73000,
        'person_emp_length': 6,
        'loan_amnt': 11000,
        'loan_int_rate': 11.7,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 92000,
        'person_emp_length': 10,
        'loan_amnt': 16500,
        'loan_int_rate': 9.5,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 104000,
        'person_emp_length': 12,
        'loan_amnt': 17500,
        'loan_int_rate': 8.5,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 114000,
        'person_emp_length': 19,
        'loan_amnt': 24000,
        'loan_int_rate': 7.5,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 44000,
        'person_emp_length': 3,
        'loan_amnt': 4200,
        'loan_int_rate': 14.1,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 65000,
        'person_emp_length': 5,
        'loan_amnt': 9200,
        'loan_int_rate': 11.4,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 87000,
        'person_emp_length': 8,
        'loan_amnt': 13700,
        'loan_int_rate': 9.9,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 99000,
        'person_emp_length': 14,
        'loan_amnt': 16200,
        'loan_int_rate': 9.0,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 112000,
        'person_emp_length': 18,
        'loan_amnt': 21700,
        'loan_int_rate': 7.6,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 56000,
        'person_emp_length': 2,
        'loan_amnt': 5400,
        'loan_int_rate': 12.6,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 74000,
        'person_emp_length': 6,
        'loan_amnt': 11200,
        'loan_int_rate': 11.8,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 93000,
        'person_emp_length': 10,
        'loan_amnt': 16700,
        'loan_int_rate': 9.6,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 105000,
        'person_emp_length': 12,
        'loan_amnt': 17700,
        'loan_int_rate': 8.6,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 115000,
        'person_emp_length': 19,
        'loan_amnt': 24200,
        'loan_int_rate': 7.6,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 45000,
        'person_emp_length': 3,
        'loan_amnt': 4300,
        'loan_int_rate': 14.2,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 66000,
        'person_emp_length': 5,
        'loan_amnt': 9400,
        'loan_int_rate': 11.5,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 88000,
        'person_emp_length': 8,
        'loan_amnt': 13900,
        'loan_int_rate': 10.0,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 100000,
        'person_emp_length': 14,
        'loan_amnt': 16400,
        'loan_int_rate': 9.1,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 113000,
        'person_emp_length': 18,
        'loan_amnt': 21900,
        'loan_int_rate': 7.7,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 57000,
        'person_emp_length': 2,
        'loan_amnt': 5500,
        'loan_int_rate': 12.7,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 75000,
        'person_emp_length': 6,
        'loan_amnt': 11400,
        'loan_int_rate': 11.9,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 94000,
        'person_emp_length': 10,
        'loan_amnt': 16900,
        'loan_int_rate': 9.7,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 106000,
        'person_emp_length': 12,
        'loan_amnt': 17900,
        'loan_int_rate': 8.7,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 44,
        'person_income': 116000,
        'person_emp_length': 19,
        'loan_amnt': 24400,
        'loan_int_rate': 7.7,
        'loan_percent_income': 0.21,
        'person_home_ownership': 'OWN',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 21,
        'person_income': 46000,
        'person_emp_length': 3,
        'loan_amnt': 4400,
        'loan_int_rate': 14.3,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'EDUCATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'consumption'
    },
    {
        'person_age': 26,
        'person_income': 67000,
        'person_emp_length': 5,
        'loan_amnt': 9600,
        'loan_int_rate': 11.6,
        'loan_percent_income': 0.14,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 31,
        'person_income': 89000,
        'person_emp_length': 8,
        'loan_amnt': 14100,
        'loan_int_rate': 10.1,
        'loan_percent_income': 0.17,
        'person_home_ownership': 'OWN',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 39,
        'person_income': 101000,
        'person_emp_length': 14,
        'loan_amnt': 16600,
        'loan_int_rate': 9.2,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'VENTURE',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 43,
        'person_income': 114000,
        'person_emp_length': 18,
        'loan_amnt': 22100,
        'loan_int_rate': 7.8,
        'loan_percent_income': 0.19,
        'person_home_ownership': 'OWN',
        'loan_intent': 'MEDICAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'emergency_need'
    },
    {
        'person_age': 24,
        'person_income': 58000,
        'person_emp_length': 2,
        'loan_amnt': 5600,
        'loan_int_rate': 12.8,
        'loan_percent_income': 0.1,
        'person_home_ownership': 'RENT',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'fair',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 29,
        'person_income': 76000,
        'person_emp_length': 6,
        'loan_amnt': 11600,
        'loan_int_rate': 12.0,
        'loan_percent_income': 0.15,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'PERSONAL',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
        'person_age': 35,
        'person_income': 95000,
        'person_emp_length': 10,
        'loan_amnt': 17100,
        'loan_int_rate': 9.8,
        'loan_percent_income': 0.18,
        'person_home_ownership': 'OWN',
        'loan_intent': 'DEBTCONSOLIDATION',
        'loan_status': 1,
        'repayment_history': 'poor',
        'loan_purpose_category': 'debt_restructuring'
    },
    {
        'person_age': 37,
        'person_income': 107000,
        'person_emp_length': 12,
        'loan_amnt': 18100,
        'loan_int_rate': 8.8,
        'loan_percent_income': 0.16,
        'person_home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_status': 0,
        'repayment_history': 'good',
        'loan_purpose_category': 'productive_asset'
    },
    {
    "person_age": 32,
    "person_income": 1000,
    "person_emp_length": 1,
    "loan_amnt": 5000,
    "loan_int_rate": 15.0,
    "loan_percent_income": 1.3,
    "person_home_ownership": "RENT",
    "loan_intent": "PERSONAL",
    "repayment_history": "poor",
    "loan_purpose_category": "emergency",
    "loan_status": 1
},
    {
    "person_age": 25,
    "person_income": 59000,
    "person_emp_length": 5,
    "loan_amnt": 15000,
    "loan_int_rate": 14.0,
    "loan_percent_income": 4.5,
    "person_home_ownership": "OWN",
    "loan_intent": "PERSONAL",
    "repayment_history": "good",
    "loan_purpose_category": "productive_asset",
    "loan_status": 0
},
    {
    "person_age": 24,
    "person_income": 240000,
    "person_emp_length": 5,
    "loan_amnt": 20000,
    "loan_int_rate": 16.0,
    "loan_percent_income": 5.0,
    "person_home_ownership": "OWN",
    "loan_intent": "PERSONAL",
    "repayment_history": "poor",
    "loan_purpose_category": "emergency_need",
    "loan_status": 0
},
    {
    "person_age": 25,
    "person_income": 200000,
    "person_emp_length": 5,
    "loan_amnt": 25000,
    "loan_int_rate": 10.0,
    "loan_percent_income": 8.0,
    "person_home_ownership": "OWN",
    "loan_intent": "PERSONAL",
    "repayment_history": "poor",
    "loan_purpose_category": "emergency_need",
    "loan_status": 1
},
    {
    "person_age": 25,
    "person_income": 2000,
    "person_emp_length": 5,
    "loan_amnt": 5000,
    "loan_int_rate": 15.0,
    "loan_percent_income": 10.0,
    "person_home_ownership": "RENT",
    "loan_intent": "MEDICAL",
    "repayment_history": "good",
    "loan_purpose_category": "emergency need ",
    "loan_status": 1
},
    {
    "person_age": 30,
    "person_income": 2000,
    "person_emp_length": 1,
    "loan_amnt": 5000,
    "loan_int_rate": 15.0,
    "loan_percent_income": 10.0,
    "person_home_ownership": "RENT",
    "loan_intent": "MEDICAL",
    "repayment_history": "good",
    "loan_purpose_category": "emergency_ned",
    "loan_status": 1
},
    {
    "person_age": 25,
    "person_income": 200000,
    "person_emp_length": 12,
    "loan_amnt": 20000,
    "loan_int_rate": 20.0,
    "loan_percent_income": 5.0,
    "person_home_ownership": "RENT",
    "loan_intent": "MEDICAL",
    "repayment_history": "good",
    "loan_purpose_category": "emergency_need ",
    "loan_status": 1
},
    {
    "person_age": 28,
    "person_income": 2300,
    "person_emp_length": 4,
    "loan_amnt": 2300,
    "loan_int_rate": 15.0,
    "loan_percent_income": 10.0,
    "person_home_ownership": "RENT",
    "loan_intent": "VENTURE",
    "repayment_history": "good ",
    "loan_purpose_category": "productive_asset",
    "loan_status": 0
},
    {
    "person_age": 52,
    "person_income": 123433,
    "person_emp_length": 7,
    "loan_amnt": 100000,
    "loan_int_rate": 4.0,
    "loan_percent_income": 10.0,
    "person_home_ownership": "RENT",
    "loan_intent": "MEDICAL",
    "repayment_history": "fair",
    "loan_purpose_category": "emergency need",
    "loan_status": 1
},
    {
    "person_age": 23,
    "person_income": 23456,
    "person_emp_length": 4,
    "loan_amnt": 234,
    "loan_int_rate": 45.0,
    "loan_percent_income": 12.0,
    "person_home_ownership": "RENT",
    "loan_intent": "MEDICAL",
    "repayment_history": "good ",
    "loan_purpose_category": "productive asset",
    "loan_status": 1
},
    {
    "person_age": 12,
    "person_income": 12,
    "person_emp_length": 1,
    "loan_amnt": 233,
    "loan_int_rate": 23.0,
    "loan_percent_income": 4.0,
    "person_home_ownership": "2",
    "loan_intent": "32",
    "repayment_history": "3",
    "loan_purpose_category": "2",
    "loan_status": 3
},
]