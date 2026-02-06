from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from typing import Optional

# Config for JWT
SECRET_KEY = "beauty_secret_key_123" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# We use bcrypt for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Ensure password is treated as a clean string before hashing
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    # Passlib verify handles the salt and comparison
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # Updated to use timezone-aware UTC to avoid deprecation warnings
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)