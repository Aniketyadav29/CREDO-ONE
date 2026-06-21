"""Quick end-to-end test for the JWT authentication flow."""
import requests
import json

BASE = "http://127.0.0.1:8000"

# 1) Unauthenticated access to /api/predict => should get 401
r = requests.post(f"{BASE}/api/predict", json={
    "person_income": 50000, "loan_amnt": 5000, "loan_int_rate": 10.0,
    "loan_intent": "PERSONAL", "person_age": 30, "person_emp_length": 5
})
detail = r.json().get("detail", "")
print(f"[1] Unauth predict: {r.status_code} => {detail}")
assert r.status_code == 401, f"Expected 401, got {r.status_code}"

# 2) Register a new user
r = requests.post(f"{BASE}/api/auth/register", json={
    "username": "testuser_auth", "full_name": "Test User",
    "password": "secret123", "mobile": "9876543210"
})
data = r.json()
token_preview = str(data.get("access_token", ""))[:25]
print(f"[2] Register: {r.status_code} => status={data.get('status')}, token={token_preview}...")
assert r.status_code == 200, f"Register failed: {data}"
token = data["access_token"]

# 3) Duplicate registration => 409
r = requests.post(f"{BASE}/api/auth/register", json={
    "username": "testuser_auth", "full_name": "Dup User", "password": "secret456"
})
print(f"[3] Dup register: {r.status_code} => {r.json().get('detail', '')}")
assert r.status_code == 409

# 4) Login with correct credentials
r = requests.post(f"{BASE}/api/auth/login", json={
    "username": "testuser_auth", "password": "secret123"
})
data = r.json()
user_name = data.get("user", {}).get("full_name", "")
print(f"[4] Login OK: {r.status_code} => user={user_name}")
assert r.status_code == 200

# 5) Login with wrong password => 401
r = requests.post(f"{BASE}/api/auth/login", json={
    "username": "testuser_auth", "password": "wrongpass"
})
print(f"[5] Bad login: {r.status_code} => {r.json().get('detail', '')}")
assert r.status_code == 401

# 6) GET /api/auth/me with valid token
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{BASE}/api/auth/me", headers=headers)
me_user = r.json().get("user", {}).get("username", "")
print(f"[6] /me: {r.status_code} => username={me_user}")
assert r.status_code == 200 and me_user == "testuser_auth"

# 7) Authenticated /api/predict
r = requests.post(f"{BASE}/api/predict", headers=headers, json={
    "person_income": 50000, "loan_amnt": 5000, "loan_int_rate": 10.0,
    "loan_intent": "PERSONAL", "person_age": 30, "person_emp_length": 5
})
pred = r.json().get("prediction", "N/A")
print(f"[7] Auth predict: {r.status_code} => prediction={pred}")
assert r.status_code == 200

# 8) Fake/expired token => 401 
r = requests.get(f"{BASE}/api/auth/me", headers={"Authorization": "Bearer fake.token.here"})
print(f"[8] Fake token: {r.status_code} => {r.json().get('detail', '')}")
assert r.status_code == 401

print()
print("=" * 50)
print("ALL 8 TESTS PASSED ✅")
print("=" * 50)
