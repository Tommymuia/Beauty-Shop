from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Review
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class ReviewCreate(BaseModel):
    product_id: int
    user_name: Optional[str] = "Anonymous"
    rating: int
    comment: str

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_name: str
    rating: int
    comment: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Review(
        product_id=review.product_id,
        user_name=review.user_name,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).order_by(Review.created_at.desc()).all()
    return reviews
