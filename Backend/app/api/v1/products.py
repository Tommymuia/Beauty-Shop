from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductOut, ProductBase
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/", response_model=List[ProductOut])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category:
        query = query.join(Category).filter(Category.name.ilike(f"%{category}%"))
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate category exists
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    
    try:
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock_qty=product.stock_qty,
            category_id=product.category_id,
            image_url=product.image_url,
            rating=product.rating or 0.0,
            reviews_count=product.reviews_count or 0,
            is_new=product.is_new or False
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product: ProductBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/search", response_model=List[ProductOut])
def search_products(
    q: str,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.name.ilike(f"%{q}%") | 
        Product.description.ilike(f"%{q}%")
    ).all()
    return products

@router.get("/category/{category_name}", response_model=List[ProductOut])
def get_products_by_category(category_name: str, db: Session = Depends(get_db)):
    products = db.query(Product).join(Category).filter(
        Category.name.ilike(f"%{category_name}%")
    ).all()
    return products

@router.put("/{product_id}/stock")
def update_product_stock(
    product_id: int,
    stock_qty: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.stock_qty = stock_qty
    db.commit()
    db.refresh(db_product)
    return {"message": "Stock updated successfully", "new_stock": stock_qty}

@router.get("/low-stock", response_model=List[ProductOut])
def get_low_stock_products(
    threshold: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    products = db.query(Product).filter(Product.stock_qty <= threshold).all()
    return products