# Setup & Installation Guide

## Credit Risk Intelligence Platform v1.0.0

**Estimated Setup Time**: 15-20 minutes  
**Prerequisites**: Python 3.9+, pip, Git

---

## Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourcompany/credit-risk-platform.git
cd credit-risk-platform

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run server
uvicorn main:app --reload
```

Server will be available at `http://localhost:8000`

---

## Detailed Setup Steps

### Step 1: Prerequisites Check

```bash
# Verify Python version
python3 --version  # Should be 3.9 or higher

# Verify pip
pip --version

# Verify Git (optional but recommended)
git --version
```

### Step 2: Clone Repository

```bash
# Using HTTPS (recommended for quick start)
git clone https://github.com/yourcompany/credit-risk-platform.git

# OR using SSH (if SSH key configured)
git clone git@github.com:yourcompany/credit-risk-platform.git

cd credit-risk-platform
```

### Step 3: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# **Windows Users**:
# venv\Scripts\activate

# **macOS/Linux Users**:
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
which python  # Should show path inside venv
```

### Step 4: Install Dependencies

```bash
# Update pip (recommended)
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi  # Should show fastapi version
```

### Step 5: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Open and edit .env
nano .env  # macOS/Linux
# or
notepad .env  # Windows
```

**Required Variables**:
```
GEMINI_API_KEY=your_actual_api_key_here
DEBUG_MODE=false
LOG_LEVEL=INFO
```

**Get Gemini API Key**:
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy and paste in `.env` file
4. Keep this key private!

### Step 6: Initialize Database

```bash
# Database auto-initializes on first request
# But verify it works:
python3 -c "from database import db; print('✓ Database ready')"
```

### Step 7: Run Tests (Optional but Recommended)

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html
```

### Step 8: Start Development Server

```bash
# Start with auto-reload (great for development)
uvicorn main:app --reload

# OR standard start
python main.py
```

**Access Points**:
- Application: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---

## Testing the Installation

### Test 1: Health Check

```bash
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2024-01-15T..."}
```

### Test 2: Create Prediction

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
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

# Should return detailed decision with confidence, risk band, etc.
```

### Test 3: Access Interactive API Docs

Open browser to: `http://localhost:8000/docs`

You should see:
- All available endpoints
- Request/response examples
- "Try It Out" buttons for testing

---

## File Structure

```
credit-risk-platform/
├── main.py                      # FastAPI application entry point
├── model.py                     # AI model & prediction engine
├── Config.py                    # Configuration & business rules
├── database.py                  # Prediction history storage
├── utils.py                     # Logging utilities
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git exclusions
├── docs/
│   ├── API_CONTRACT.md         # API documentation
│   ├── ARCHITECTURE_DECISION_RECORD.md
│   ├── DEPLOYMENT_GUIDE.md     # Production deployment
│   ├── RISK_POLICY.md          # Approval rules
│   ├── RELEASE_NOTES.md        # Version info
│   ├── SECURITY_COMPLIANCE.md
│   └── images/
├── static/
│   ├── index.html              # Main UI
│   ├── dashboard.html          # Prediction dashboard
│   ├── login.html              # Pre-login landing
│   └── style.css               # Styling
├── tests/
│   ├── test_api.py             # Endpoint tests
│   ├── test_model.py           # Model tests
│   ├── test_validation.py      # Input validation
│   └── test_integration.py     # End-to-end
├── logs/
│   ├── app.log                 # Application logs
│   └── audit.log               # Compliance audit
└── credit_risk_history.db      # SQLite database
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Virtual environment not activated
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Issue: "GEMINI_API_KEY not found"

**Solution**: Environment variable not set
```bash
# Verify .env file exists
cat .env  # Should show GEMINI_API_KEY=...

# If not set, add it:
echo "GEMINI_API_KEY=your_key_here" >> .env
```

### Issue: "Address already in use" on port 8000

**Solution**: Change port or kill existing process
```bash
# Use different port
uvicorn main:app --port 8001

# OR find and kill existing process
lsof -i :8000  # macOS/Linux
# Find PID and: kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Database locked error

**Solution**: SQLite file concurrency issue
```bash
# This typically happens with concurrent writes
# Solution 1: Restart server
# Solution 2: Delete lock file
rm credit_risk_history.db-shm
# Solution 3: Switch to PostgreSQL (production recommended)
```

### Issue: Slow API responses

**Solution 1**: Check Gemini API status (may be rate limited)
```bash
# Check logs
tail -f logs/app.log | grep "SERVICE_BUSY"
```

**Solution 2**: Check database file size
```bash
du -h credit_risk_history.db
# If > 100MB, consider archiving old predictions
```

### Issue: "ImportError: cannot import name 'predict_with_gemini'"

**Solution**: Module path issue
```bash
# Ensure you're in correct directory
pwd  # Should end with /credit-risk-platform
ls main.py  # Should exist

# Reinstall
pip install -r requirements.txt
```

---

## Configuration Guide

### Environment Variables

All variables (from `.env`):

```ini
# Gemini AI Configuration
GEMINI_API_KEY=          # Your Google API key (REQUIRED)
GEMINI_MODEL=gemini-2.5-flash  # Model version

# Application
APP_ENV=development      # OR: production, testing
APP_SECRET_KEY=dev-key   # Change in production!
MODEL_VERSION=1.0.0

# Security
ENABLE_ROLE_BASED_ACCESS=true
ADMIN_PASSWORD=admin123

# Logging
LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR
LOG_FILE_PATH=logs/app.log
ENABLE_STRUCTURED_LOGGING=true

# Rate Limiting
ENABLE_RATE_LIMITING=true
MAX_REQUESTS_PER_MINUTE=60

# Database
DATABASE_URL=sqlite:///./credit_risk_history.db
DATABASE_TYPE=sqlite

# Fairness
ENABLE_FAIRNESS_CHECKS=true
FAIRNESS_CHECK_INTERVAL=100

# PDF Export
ENABLE_PDF_EXPORT=true
PDF_LOGO_PATH=static/logo.png

# Audit/Compliance
ENABLE_AUDIT_TRAIL=true
AUDIT_LOG_FILE=logs/audit.log
```

---

## Docker Setup (Optional)

### Build Docker Image

```bash
# Build
docker build -t credit-risk-platform:1.0.0 .

# Run
docker run -p 8000:8000 \
  --env GEMINI_API_KEY=your_key \
  credit-risk-platform:1.0.0
```

### Docker Compose

```bash
docker-compose up -d
```

---

## Directory Setup for Logs

```bash
# Ensure log directory exists
mkdir -p logs
chmod 755 logs

# Verify
ls -la logs/  # Should show with write permissions
```

---

## Next Steps

1. **Read Documentation**
   - API_CONTRACT.md - Understand available endpoints
   - RISK_POLICY.md - Learn approval rules
   - ARCHITECTURE_DECISION_RECORD.md - Understand design

2. **Explore Interactive API Docs**
   - Visit http://localhost:8000/docs
   - Try sample predictions
   - Understand request/response format

3. **Run Tests**
   - `pytest tests/ -v`
   - Verify all tests pass

4. **Integrate with Frontend**
   - Update frontend URL to your API
   - Test with sample data
   - Add user authentication

5. **Deploy**
   - See DEPLOYMENT_GUIDE.md
   - Configure production environment
   - Set up monitoring

---

## Development Tips

### Enable Debug Mode

```python
# In main.py
DEBUG=True  # Not recommended for production
```

### Profile Performance

```bash
# Install flamegraph
pip install pyflame

# Run with profiling
python -m cProfile -s cumtime main.py
```

### Database Inspection

```bash
# Inspect database
sqlite3 credit_risk_history.db

# Common queries
sqlite> SELECT COUNT(*) FROM predictions;
sqlite> SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 5;
sqlite> .tables  # Show all tables
```

### View Logs

```bash
# Real-time app logs
tail -f logs/app.log

# Real-time audit logs
tail -f logs/audit.log

# Search for errors
grep ERROR logs/app.log
grep VALIDATION_ERROR logs/app.log
```

---

## Support

- **Documentation**: See `/docs/` folder
- **Interactive Docs**: http://localhost:8000/docs
- **Issues**: GitHub issues or support@creditorisk.com
- **Community**: Check discussions at [GitHub Discussions]

---

**Setup Guide Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Next Update**: When new features released
