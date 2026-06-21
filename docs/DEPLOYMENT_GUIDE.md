# Deployment Guide & Production Checklist

## Credit Risk Intelligence Platform v1.0.0

---

## Pre-Deployment Checklist

### Security
- [ ] API key moved to environment variables (GEMINI_API_KEY)
- [ ] Admin password encrypted (use passlib)
- [ ] Django secret key generated and stored securely
- [ ] HTTPS enabled on production domain
- [ ] CORS properly configured (not allow_origins=["*"])
- [ ] SQL injection protections verified
- [ ] Rate limiting enabled (MAX_REQUESTS_PER_MINUTE > 0)
- [ ] Audit logging enabled (ENABLE_AUDIT_TRAIL=true)
- [ ] Secrets not in `.env` file committed to Git

### Performance
- [ ] Database indexed on frequently queried fields
- [ ] Async API calls implemented (aiohttp)
- [ ] Response time monitoring in place
- [ ] Rate limiting configured
- [ ] Cache headers set for static assets
- [ ] Compression enabled for responses

### Compliance & Audit
- [ ] Audit trail database initialized
- [ ] User roles defined for RBAC
- [ ] Override approval workflow tested
- [ ] CSV export tested for audits
- [ ] PDF export functional
- [ ] Bias metrics calculation verified

### Testing
- [ ] Unit tests passing (pytest)
- [ ] Integration tests with mock API
- [ ] Load testing (at least 100 concurrent requests)
- [ ] Fallback mode tested (simulate 503)
- [ ] Error handling verified
- [ ] Input validation tested

### Documentation
- [ ] API documentation up to date
- [ ] Runbook for on-call support
- [ ] Incident response plan documented
- [ ] Architecture ADRs reviewed
- [ ] Staff trained on system

### Monitoring
- [ ] Application logging configured
- [ ] Error tracking (Sentry/similar) enabled
- [ ] Performance monitoring setup
- [ ] Alerting for prediction failures
- [ ] Alerting for API quota near limit
- [ ] Dashboard for KPIs created

---

## Deployment Steps

### 1. Environment Setup

```bash
# Create production .env file
cp .env.example .env

# Edit .env with production values
nano .env

# Verify critical variables
GEMINI_API_KEY=your_actual_key_here
DATABASE_URL=sqlite:///./production_db.sqlite
APP_ENV=production
LOG_LEVEL=WARNING
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Initialization

```bash
# Database will auto-initialize on first request
# But manually verify:
python3 -c "from database import db; print('Database ready')"
```

### 4. Run Tests

```bash
# Unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### 5. Run Production Server

```bash
# Option A: Direct (for small deployments)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Option B: With Gunicorn (recommended)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Option C: Docker (recommended for cloud)
docker build -t credit-risk-platform .
docker run -p 8000:8000 --env-file .env credit-risk-platform
```

### 6. Nginx/Reverse Proxy Setup

```nginx
upstream credit_risk_api {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;  # For load balancing
}

server {
    listen 443 ssl http2;
    server_name api.creditorisk.com;
    
    ssl_certificate /etc/ssl/certs/certificate.crt;
    ssl_certificate_key /etc/ssl/private/key.key;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    location / {
        proxy_pass http://credit_risk_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### 7. Monitoring & Logging

```bash
# Monitor logs in real-time
tail -f logs/app.log

# Check audit trail
tail -f logs/audit.log

# Monitor database size
du -h credit_risk_history.db
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create log directory
RUN mkdir -p logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (Multi-service)

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=sqlite:///./db.sqlite
      - APP_ENV=production
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/ssl/certs:/etc/ssl/certs:ro
    depends_on:
      - api
    restart: unless-stopped
```

---

## Kubernetes Deployment

### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: credit-risk-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: credit-risk-api
  template:
    metadata:
      labels:
        app: credit-risk-api
    spec:
      containers:
      - name: api
        image: credit-risk-platform:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: gemini-key
        - name: APP_ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: credit-risk-api-service
spec:
  selector:
    app: credit-risk-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## Database Migration (SQLite to PostgreSQL)

When ready to scale:

```bash
# 1. Export current SQLite data
python3 -c "
from database import db
import json

# Export all predictions
auditdata = db.export_audit_trail()
with open('audit_export.json', 'w') as f:
    json.dump(audit_data, f)
"

# 2. Update config to use PostgreSQL
# Change DATABASE_URL=postgresql://user:pass@localhost/credit_risk

# 3. Initialize PostgreSQL schema
alembic upgrade head

# 4. Restore data
python3 scripts/migrate_data.py audit_export.json
```

---

## Rollback Procedure

If deployment has critical issues:

```bash
# 1. Revert to previous Git commit
git checkout v0.9.0

# 2. Restore previous database (if schema compatible)
cp .backup/credit_risk_history.db.bak credit_risk_history.db

# 3. Restart services
systemctl restart credit-risk-platform

# 4. Verify with smoke tests
python tests/smoke_test.py
```

---

## Post-Deployment Verification

```bash
# 1. Health check
curl https://api.creditorisk.com/health

# 2. Test prediction endpoint (with auth header)
curl -X POST https://api.creditorisk.com/api/predict \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
  -d '{"person_income": 50000, ...}'

# 3. Verify logging
tail -f logs/app.log | grep "REQUEST"

# 4. Check database
sqlite3 credit_risk_history.db "SELECT COUNT(*) FROM predictions;"

# 5. Monitor performance
# - Check response times in logs
# - Verify CPU/Memory usage
# - Check database file size
```

---

## Scaling Strategies

### Horizontal Scaling
- Run multiple API instances behind load balancer
- Use connection pooling for database
- Implement caching for frequently accessed data

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries (add indexes)
- Enable response compression

### Asynchronous Processing
- Move PDF generation to background tasks (Celery)
- Queue long-running predictions
- Implement job status tracking

---

## Disaster Recovery

### Backup Strategy
```bash
# Daily backup of database
0 2 * * * cp /app/credit_risk_history.db /backups/credit_risk_history.db.$(date +\%Y\%m\%d)

# Keep 30 days of backups
find /backups -name "*.bak" -mtime +30 -delete
```

### Recovery Time Objectives
- RTO (Recovery Time): 1 hour
- RPO (Recovery Point): 24 hours

---

## Maintenance Windows

### Production Support Hours
- **Business**: 8am - 6pm EST (weekdays)
- **On-Call**: 24/7 for critical issues

### Scheduled Maintenance
- Tuesdays 2-3am EST (low traffic window)
- Communicate 48 hours in advance
- Estimated downtime: 15 minutes

---

## Monitoring & Alerts

### Key Metrics to Alert On
- API response time > 2 seconds
- Prediction failures > 1%
- Gemini API quota near limit
- Database size > 10GB
- Audit log disk space > 90%
- Error rate > 0.5%

### Tools Recommended
- **Application Monitoring**: New Relic, Datadog, Sentry
- **Infrastructure**: Prometheus, Grafana
- **Logging**: ELK Stack, Splunk
- **Alerting**: PagerDuty, Opsgenie

---

**Deployment Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Next Review**: 2024-04-15
