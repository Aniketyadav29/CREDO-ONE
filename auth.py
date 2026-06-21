"""
Authentication Module for Credit Risk Intelligence Platform.
Handles JWT token management, password hashing, and user database operations.
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Dict

import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ---------------------------------------------------------------------------
# Password hashing (bcrypt — direct, no passlib wrapper)
# ---------------------------------------------------------------------------


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    pwd_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------
# These are populated at import time from Config.py (circular-import safe
# because we only read plain values).
from Config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT access token.  Raises HTTPException on failure."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------------------------------------------------------------------
# Database helpers — users table
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "credit_risk_app.db")


def init_users_table():
    """Create the users table if it does not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    UNIQUE NOT NULL,
                full_name   TEXT    NOT NULL,
                password    TEXT    NOT NULL,
                role        TEXT    NOT NULL DEFAULT 'viewer',
                mobile      TEXT,
                created_at  TEXT    NOT NULL
            )
            """
        )
        # Seed default admin user so login works right out of the box
        row = conn.execute("SELECT 1 FROM users WHERE username = 'admin'").fetchone()
        if not row:
            from Config import ADMIN_PASSWORD
            hashed = hash_password(ADMIN_PASSWORD)
            conn.execute(
                """
                INSERT INTO users (username, full_name, password, role, mobile, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                ("admin", "System Administrator", hashed, "admin", "", datetime.now().isoformat())
            )
        conn.commit()


def create_user(
    username: str,
    full_name: str,
    plain_password: str,
    role: str = "viewer",
    mobile: str = "",
) -> Dict:
    """Register a new user.  Returns the created user dict (without password)."""
    hashed = hash_password(plain_password)
    now = datetime.now().isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO users (username, full_name, password, role, mobile, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, full_name, hashed, role, mobile, now),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{username}' is already taken",
        )
    return {
        "username": username,
        "full_name": full_name,
        "role": role,
        "created_at": now,
    }


def authenticate_user(username: str, plain_password: str) -> Optional[Dict]:
    """Verify credentials.  Returns user dict on success, None on failure."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

    if row is None:
        return None
    if not verify_password(plain_password, row["password"]):
        return None

    return {
        "id": row["id"],
        "username": row["username"],
        "full_name": row["full_name"],
        "role": row["role"],
        "mobile": row["mobile"],
        "created_at": row["created_at"],
    }


# ---------------------------------------------------------------------------
# FastAPI dependency — extract & validate the current user from the JWT
# ---------------------------------------------------------------------------
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Dict:
    """
    FastAPI dependency that extracts and validates the JWT from the
    Authorization header.  Returns a dict with user claims.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(credentials.credentials)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user identity",
        )

    return {
        "username": username,
        "role": payload.get("role", "viewer"),
        "full_name": payload.get("full_name", ""),
        "user_id": username,  # backward-compatible with existing code
    }


def require_role(*allowed_roles: str):
    """
    Returns a FastAPI dependency that checks the current user's role
    against a whitelist.  Usage:

        @app.get("/admin", dependencies=[Depends(require_role("admin"))])
    """
    async def _checker(user: Dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {', '.join(allowed_roles)}",
            )
        return user
    return _checker
