from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_admin: Optional[bool] = None

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "is_admin": u.is_admin} for u in users]

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    from werkzeug.security import generate_password_hash
    
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email, 
        password=generate_password_hash(user.password, method='pbkdf2:sha256'), 
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "is_admin": new_user.is_admin}

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email:
        db_user.email = user.email
    if user.is_admin is not None:
        db_user.is_admin = user.is_admin
    
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "email": db_user.email, "is_admin": db_user.is_admin}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
