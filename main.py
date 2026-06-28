import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import os
import time
import json
import sqlite3
from typing import Optional, Dict, List
from datetime import datetime

from model import predict_with_gemini
from Config import (
    get_risk_band, 
    ENABLE_ROLE_BASED_RBAC,
    USER_ROLES,
    MODEL_VERSION
)
from auth import (
    init_users_table,
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    require_role,
)

app = FastAPI(
    title="Credit Risk Intelligence Platform",
    description="Enterprise-grade AI-assisted underwriting system",
    version=MODEL_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced LoanData model with comprehensive validation
class LoanData(BaseModel):
    person_income: int = Field(..., gt=0, description="Annual income in dollars")
    loan_amnt: int = Field(..., gt=0, description="Loan amount in dollars")
    loan_int_rate: float = Field(..., gt=0, lt=50, description="Interest rate as percentage")
    loan_intent: str = Field(..., description="Purpose of the loan")
    person_age: int = Field(..., ge=18, le=120, description="Applicant age")
    person_emp_length: int = Field(..., ge=0, le=100, description="Years of employment")
    loan_percent_income: float = Field(default=0.1, ge=0, description="Loan-to-income input (supports ratio or percentage values)")
    person_home_ownership: str = Field(default="RENT", description="Home ownership status")
    repayment_history: str = Field(default="good", description="Payment history quality")
    loan_purpose_category: str = Field(default="productive_asset", description="Loan category")
    user_id: Optional[str] = Field(default=None, description="User making the request")
    applicant_id: Optional[str] = Field(default=None, description="Unique applicant identifier")
    
    @field_validator('loan_intent')
    @classmethod
    def validate_intent(cls, v):
        valid_intents = [
            "PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "MORTGAGE",
            "AUTO", "HOME_IMPROVEMENT", "DEBT_CONSOLIDATION"
        ]
        if v not in valid_intents:
            raise ValueError(f"Invalid loan intent. Must be one of: {valid_intents}")
        return v
    
    @field_validator('person_home_ownership')
    @classmethod
    def validate_ownership(cls, v):
        valid_values = ["RENT", "OWN", "MORTGAGE", "OTHER"]
        if v not in valid_values:
            raise ValueError(f"Invalid home ownership. Must be one of: {valid_values}")
        return v
    
    @field_validator('repayment_history')
    @classmethod
    def validate_repayment(cls, v):
        valid_values = ["excellent", "good", "average", "fair", "poor", "defaulted"]
        if v.lower() in valid_values:
            return v.lower()
        raise ValueError(f"Invalid repayment history. Must be one of: {valid_values}")

    @field_validator('loan_percent_income')
    @classmethod
    def normalize_loan_percent_income(cls, v):
        """
        Accept both ratio input (0.25) and percentage input (4, 25, 40, ...).
        Any value > 1 is treated as percent and converted to ratio.
        """
        value = float(v)
        if value > 1:
            value = value / 100.0
        return max(0.0, value)

class OverrideRequest(BaseModel):
    """Request for manual override of a decision"""
    request_id: str
    override_decision: int = Field(..., ge=0, le=1, description="0=Approve, 1=Reject")
    reason: str = Field(..., description="Reason for override")
    user_id: str = Field(..., description="User ID of reviewer")


class RegisterRequest(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique login ID")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    mobile: str = Field(default="", description="Mobile number")


class LoginRequest(BaseModel):
    """User login request"""
    username: str = Field(..., description="Login ID")
    password: str = Field(..., description="Password")

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.getenv("VERCEL") == "1":
    DB_PATH = "/tmp/credit_risk_app.db"
else:
    DB_PATH = os.path.join(BASE_DIR, "credit_risk_app.db")


def init_db():
    """Create database tables if they do not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT UNIQUE,
                user_id TEXT,
                applicant_id TEXT,
                input_payload TEXT NOT NULL,
                prediction_result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_prediction_record(request_id: str, user: Dict, data_payload: Dict, result_payload: Dict):
    """Persist user-provided data and prediction output for every request."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO predictions (
                request_id, user_id, applicant_id, input_payload, prediction_result, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                user.get("user_id", "anonymous"),
                data_payload.get("applicant_id"),
                json.dumps(data_payload),
                json.dumps(result_payload),
                datetime.now().isoformat()
            ),
        )
        conn.commit()


def fetch_applicant_history(applicant_id: str) -> List[Dict]:
    """Fetch saved predictions for one applicant from SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT request_id, user_id, applicant_id, input_payload, prediction_result, created_at
            FROM predictions
            WHERE applicant_id = ?
            ORDER BY id DESC
            """,
            (applicant_id,),
        ).fetchall()

    output = []
    for row in rows:
        output.append(
            {
                "request_id": row["request_id"],
                "user_id": row["user_id"],
                "applicant_id": row["applicant_id"],
                "input_payload": json.loads(row["input_payload"]),
                "prediction_result": json.loads(row["prediction_result"]),
                "created_at": row["created_at"],
            }
        )
    return output

# Check if the static directory exists to avoid the RuntimeError
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
    print("Created missing 'static' directory. Please put your index.html inside it.")

init_db()
init_users_table()

# Mount the static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- Middleware for Request/Response ---
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    """Middleware to add request ID and timing"""
    request_id = request.headers.get("X-Request-ID", str(time.time()))
    request.state.request_id = request_id
    
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response

# =====================================================================
# Authentication Endpoints (public — no token required)
# =====================================================================

@app.post("/api/auth/register")
async def register_user(req: RegisterRequest):
    """Register a new user, or login if credentials match an existing account."""
    try:
        user = create_user(
            username=req.username,
            full_name=req.full_name,
            plain_password=req.password,
            role="analyst",           # default role for self-registration
            mobile=req.mobile,
        )
        msg = "Registration successful"
    except HTTPException as e:
        if e.status_code == 409: # HTTP 409 Conflict (Username already taken)
            # Try to log them in with the existing account
            user = authenticate_user(req.username, req.password)
            if user:
                msg = "Logged in to existing account"
            else:
                # Password didn't match, so we throw the original "Username taken" error
                raise e 
        else:
            raise e

    # Issue a token immediately so the user is logged-in
    token = create_access_token({
        "sub": user["username"],
        "role": user["role"],
        "full_name": user["full_name"],
    })
    return {
        "status": "success",
        "message": msg,
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }


@app.post("/api/auth/login")
async def login_user(req: LoginRequest):
    """Authenticate and return a JWT access token."""
    user = authenticate_user(req.username, req.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )
    token = create_access_token({
        "sub": user["username"],
        "role": user["role"],
        "full_name": user["full_name"],
    })
    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
        },
    }


@app.get("/api/auth/me")
async def get_me(user: Dict = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return {"user": user}

@app.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    # Look for index.html inside the static folder
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        return "<h1>Error: static/index.html not found!</h1><p>Please move your HTML file into the 'static' folder.</p>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), headers=NO_CACHE_HEADERS)

@app.get("/index.html", response_class=HTMLResponse)
async def serve_index_page():
    return await serve_home()

@app.get("/login.html", response_class=HTMLResponse)
async def serve_login_page():
    login_path = os.path.join(STATIC_DIR, "login.html")
    if not os.path.exists(login_path):
        raise HTTPException(status_code=404, detail="login.html not found in static directory")
    with open(login_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), headers=NO_CACHE_HEADERS)

@app.get("/dashboard.html", response_class=HTMLResponse)
async def serve_dashboard_page():
    dashboard_path = os.path.join(STATIC_DIR, "dashboard.html")
    if not os.path.exists(dashboard_path):
        raise HTTPException(status_code=404, detail="dashboard.html not found in static directory")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), headers=NO_CACHE_HEADERS)

@app.post("/api/predict")
async def get_prediction(
    data: LoanData,
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """
    Primary prediction endpoint.
    Returns prediction with confidence, risk band, and decision factors.
    """
    request_id = request.state.request_id
    
    try:
        # Get prediction from model
        result = await predict_with_gemini(data.model_dump(), request_id=request_id)
        
        # Add metadata
        result["request_id"] = request_id
        result["model_version"] = MODEL_VERSION
        result["timestamp"] = datetime.now().isoformat()

        save_prediction_record(
            request_id=request_id,
            user=user,
            data_payload=data.model_dump(),
            result_payload=result,
        )
        
        return result
        
    except Exception as e:
        error_text = str(e)
        if "Gemini" in error_text or "GEMINI_API_KEY" in error_text:
            raise HTTPException(status_code=503, detail=error_text)
        raise HTTPException(status_code=500, detail=f"Prediction error: {error_text}")

@app.post("/api/override")
async def override_decision(
    override_req: OverrideRequest,
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """Manual override endpoint"""
    return {
        "status": "success",
        "message": "Override recorded",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/applicant/{applicant_id}/history")
async def get_applicant_history(
    applicant_id: str,
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """Get prediction history for an applicant"""
    history = fetch_applicant_history(applicant_id)
    return {
        "applicant_id": applicant_id,
        "history_count": len(history),
        "history": history,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stats")
async def get_platform_stats(
    days: int = 30,
    user: Dict = Depends(get_current_user)
):
    """Get operational statistics and KPIs"""
    return {
        "period_days": days,
        "statistics": {},
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/audit-trail")
async def get_audit_trail(
    start_date: str = None,
    end_date: str = None,
    user: Dict = Depends(get_current_user)
):
    """Export audit trail for compliance"""
    return {
        "audit_trail": [],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)