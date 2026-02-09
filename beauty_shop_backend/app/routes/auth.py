from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta
from app.database import get_db
from app.config import settings
from app.models import User
from app.schemas import UserCreate, Token, UserOut, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token  # FIXED IMPORTS

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with hashed password
    new_user = User(
        email=user_data.email,
        password=get_password_hash(user_data.password),  # FIXED: use get_password_hash
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        address=user_data.address,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_user.id)},  # Use user ID instead of email for consistency
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    # Authenticate user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):  # FIXED: use verify_password
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """Decodes JWT token to get current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserOut)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle password update
    if "password" in update_data and update_data["password"]:
        current_user.password = get_password_hash(update_data["password"])
        del update_data["password"]
    
    # Prevent admin status changes
    update_data.pop("is_admin", None)
    
    # Handle email change (check uniqueness)
    if "email" in update_data and update_data["email"] != current_user.email:
        if db.query(User).filter(User.email == update_data["email"]).first():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update remaining fields
    for field, value in update_data.items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user