import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from model import predict_with_gemini

app = FastAPI(title="MicroRisk AI")

# Check if the static directory exists to avoid the RuntimeError
if not os.path.exists("static"):
    os.makedirs("static")
    print("Created missing 'static' directory. Please put your index.html inside it.")

# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

class LoanData(BaseModel):
    person_income: int
    loan_amnt: int
    loan_int_rate: float
    loan_intent: str
    person_age: int = 25
    person_emp_length: int = 2
    loan_percent_income: float = 0.1
    person_home_ownership: str = "RENT"
    repayment_history: str = "good"
    loan_purpose_category: str = "productive_asset"

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    # Look for index.html inside the static folder
    index_path = os.path.join("static", "index.html")
    if not os.path.exists(index_path):
        return "<h1>Error: static/index.html not found!</h1><p>Please move your HTML file into the 'static' folder.</p>"
    with open(index_path) as f:
        return f.read()

@app.post("/api/predict")
async def get_prediction(data: LoanData):
    try:
        result = await predict_with_gemini(data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
