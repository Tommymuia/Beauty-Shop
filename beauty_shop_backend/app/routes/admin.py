from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
import io
from app.database import get_db
from app.models import User, Product, Order, OrderItem
from app.schemas import UserOut, UserUpdate
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get stats
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()
    total_users = db.query(User).count()
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    
    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "total_revenue": float(total_revenue)
    }

@router.get("/dashboard/recent-orders")
def get_recent_orders(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    orders = db.query(Order).join(User).order_by(Order.created_at.desc()).limit(limit).all()
    
    result = []
    for order in orders:
        result.append({
            "id": f"ORD-{order.id:03d}",
            "customer": f"{order.owner.first_name or ''} {order.owner.last_name or ''}".strip() or order.owner.email,
            "amount": float(order.total_amount or 0),
            "status": order.status,
            "date": order.created_at.isoformat()
        })
    
    return result

@router.get("/dashboard/top-products")
def get_top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get top products by sales
    top_products = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_sales'),
        func.sum(OrderItem.quantity * OrderItem.price_at_purchase).label('total_revenue')
    ).join(OrderItem).group_by(Product.id, Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(limit).all()
    
    result = []
    for product in top_products:
        result.append({
            "name": product.name,
            "sales": int(product.total_sales),
            "revenue": float(product.total_revenue or 0)
        })
    
    return result

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    from app.services.auth_service import hash_password
    
    db_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        address=user_data.address,
        password=hash_password(user_data.password or "defaultpass123"),
        is_admin=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/users", response_model=List[UserOut])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        if key == "password" and value:
            from app.services.auth_service import hash_password
            setattr(user, "password", hash_password(value))
        else:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/users/{user_id}/toggle-admin")
def toggle_admin_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = not user.is_admin
    db.commit()
    db.refresh(user)
    return {"message": f"User admin status updated to {user.is_admin}"}
    
@router.get("/analytics/sales")
def get_sales_analytics(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get daily sales for the period
    daily_sales = db.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('total'),
        func.count(Order.id).label('orders')
    ).filter(
        Order.created_at >= start_date,
        Order.created_at <= end_date
    ).group_by(func.date(Order.created_at)).all()
    
    return {
        "period": f"{days} days",
        "daily_sales": [
            {
                "date": str(sale.date),
                "total": float(sale.total),
                "orders": sale.orders
            }
            for sale in daily_sales
        ]
    }

@router.get("/reports/export")
def export_orders_report(
    format: str = "csv",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    orders = db.query(Order).join(User).all()
    
    if format == "csv":
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Order ID', 'Customer', 'Email', 'Date', 'Total', 'Status'])
        
        # Write data
        for order in orders:
            writer.writerow([
                f"ORD-{order.id:03d}",
                f"{order.owner.first_name or ''} {order.owner.last_name or ''}".strip() or order.owner.email,
                order.owner.email,
                order.created_at.strftime('%Y-%m-%d'),
                float(order.total_amount),
                order.status
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=orders-report.csv"}
        )
    
    return {"message": "Format not supported"}