from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import SupportMessage
from datetime import datetime

router = APIRouter()

class SupportMessageCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@router.post("/")
def create_support_message(payload: SupportMessageCreate, db: Session = Depends(get_db)):
    """Create a new support message from contact form"""
    new_message = SupportMessage(
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        message=payload.message,
        status="pending"
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"message": "Support message received", "id": new_message.id}

@router.get("/")
def get_all_support_messages(db: Session = Depends(get_db)):
    """Get all support messages for admin"""
    messages = db.query(SupportMessage).order_by(SupportMessage.created_at.desc()).all()
    return [{
        "id": msg.id,
        "name": msg.name,
        "email": msg.email,
        "subject": msg.subject,
        "message": msg.message,
        "status": msg.status,
        "created_at": msg.created_at
    } for msg in messages]

@router.put("/{message_id}/status")
def update_message_status(message_id: int, payload: dict, db: Session = Depends(get_db)):
    """Update support message status"""
    message = db.query(SupportMessage).filter(SupportMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = payload.get('status', message.status)
    db.commit()
    return {"message": "Status updated", "status": message.status}
