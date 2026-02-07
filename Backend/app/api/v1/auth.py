from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # ADDED: Import Session
from pydantic import BaseModel
from app.core import security
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.db.session import get_db  # FIXED: Import directly from db.session

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=security.Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):  # FIXED
    # 1. Check if user exists
    existing = security.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash the password
    hashed = security.get_password_hash(user_in.password)
    
    # 3. Create user
    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=hashed,
        is_active=True,
        phone=user_in.phone,
        address=user_in.address
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    token = security.create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=security.Token)
def login(credentials: LoginSchema, db: Session = Depends(get_db)):  # FIXED
    user = security.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = security.create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(security.get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "address": current_user.address,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }

@router.put("/profile", response_model=UserOut)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),  # FIXED
    current_user: User = Depends(security.get_current_user)
):
    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True) if hasattr(user_update, 'model_dump') else user_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        if key == "password" and value:
            setattr(current_user, "hashed_password", security.get_password_hash(value))
        elif key != "password":
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "address": current_user.address,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }