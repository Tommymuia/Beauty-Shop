from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models import Product, Category, User
from app.schemas import ProductSchema, ProductCreate, ProductUpdate
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/v1/products", tags=["products"])

# ======================
# PUBLIC ENDPOINTS (No auth required)
# ======================

@router.get("/", response_model=List[ProductSchema])
def get_products(
    skip: int = 0,
    limit: int = 20,  # Reduced default for safety
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Public product catalog - ONLY active products visible"""
    query = (
        db.query(Product)
        .filter(Product.is_active == True)  # CRITICAL: Hide inactive products
        .options(joinedload(Product.category))  # Prevent N+1 queries
    )
    
    if category_id:
        # Validate category exists AND is active before filtering
        category = db.query(Category).filter(
            Category.id == category_id,
            Category.is_active == True
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or inactive category"
            )
        query = query.filter(Product.category_id == category_id)
    
    if search:
        # Sanitize search input (prevent regex injection in ilike)
        safe_search = search.strip().replace("%", "\\%").replace("_", "\\_")
        query = query.filter(
            Product.name.ilike(f"%{safe_search}%", escape="\\") |
            Product.description.ilike(f"%{safe_search}%", escape="\\")
        )
    
    # Enforce reasonable limits
    limit = min(limit, 100)
    return query.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Public product detail - ONLY active products visible"""
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.is_active == True  # CRITICAL: Hide inactive products
        )
        .options(joinedload(Product.category))
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

# ======================
# ADMIN ENDPOINTS (Require auth + admin)
# ======================

def verify_admin(current_user: User):
    """Centralized admin verification"""
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_admin(current_user)
    
    # Validate category exists AND is active
    category = db.query(Category).filter(
        Category.id == product_data.category_id,
        Category.is_active == True
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive"
        )
    
    # Prevent creating inactive products via create endpoint
    if hasattr(product_data, 'is_active') and product_data.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create inactive product. Use DELETE endpoint to deactivate."
        )
    
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_admin(current_user)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = product_update.dict(exclude_unset=True)
    
    # Validate category if being updated
    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.id == update_data["category_id"],
            Category.is_active == True
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New category not found or inactive"
            )
    
    # Block direct deactivation via update (use DELETE endpoint)
    if "is_active" in update_data and update_data["is_active"] is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate product via update. Use DELETE endpoint."
        )
    
    # Apply updates
    for key, value in update_data.items():
        if key != "is_active":  # Extra safety
            setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_admin(current_user)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Idempotent soft delete
    if product.is_active:
        product.is_active = False
        if hasattr(product, 'deleted_at'):
            product.deleted_at = datetime.now(timezone.utc)
        db.commit()
    # If already inactive, still return 204 (idempotent)
    return