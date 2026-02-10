from datetime import datetime, timedelta, timezone
from jose import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

# Config for JWT
SECRET_KEY = "beauty_secret_key_123" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    """Hash password using werkzeug (no 72-byte limit, Python 3.8 compatible)"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using werkzeug"""
    return check_password_hash(hashed_password, plain_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)