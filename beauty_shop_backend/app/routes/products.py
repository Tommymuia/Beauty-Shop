from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional  # <--- Added Optional here
from app.database import get_db
from app.models import Product, Category
from app.schemas import ProductSchema

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def get_products(
    category_id: Optional[int] = None, 
    search: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    # Filter out products with NULL required fields
    query = query.filter(
        Product.name.isnot(None),
        Product.price.isnot(None),
        Product.category_id.isnot(None)
    )
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    products = query.all()
    category_map = {1: 'Skincare', 2: 'Haircare', 3: 'Makeup'}
    
    result = []
    for p in products:
        product_dict = {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'category_id': p.category_id,
            'category': category_map.get(p.category_id, 'Unknown'),
            'stock_quantity': p.stock_quantity,
            'stock': p.stock_quantity,
            'image': p.image,
            'rating': p.rating,
            'is_new': p.is_new,
            'isNew': p.is_new
        }
        result.append(product_dict)
    
    return result


@router.post("/", response_model=ProductSchema)
def create_product(payload: dict, db: Session = Depends(get_db)):
    new = Product(
        name=payload.get('name'),
        description=payload.get('description'),
        price=payload.get('price'),
        stock_quantity=payload.get('stock_quantity', 0),
        category_id=payload.get('category_id'),
        image=payload.get('image'),
        rating=payload.get('rating', 4.5),
        is_new=payload.get('is_new', False)
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    
    category_map = {1: 'Skincare', 2: 'Haircare', 3: 'Makeup'}
    return {
        'id': new.id,
        'name': new.name,
        'description': new.description,
        'price': new.price,
        'category_id': new.category_id,
        'category': category_map.get(new.category_id, 'Unknown'),
        'stock_quantity': new.stock_quantity,
        'stock': new.stock_quantity,
        'image': new.image,
        'rating': new.rating,
        'is_new': new.is_new,
        'isNew': new.is_new
    }


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category_map = {1: 'Skincare', 2: 'Haircare', 3: 'Makeup'}
    return {
        'id': prod.id,
        'name': prod.name,
        'description': prod.description,
        'price': prod.price,
        'category_id': prod.category_id,
        'category': category_map.get(prod.category_id, 'Unknown'),
        'stock_quantity': prod.stock_quantity,
        'stock': prod.stock_quantity,
        'image': prod.image,
        'rating': prod.rating,
        'is_new': prod.is_new,
        'isNew': prod.is_new
    }


@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, payload: dict, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in payload.items():
        if hasattr(prod, k) and v is not None:
            setattr(prod, k, v)
    db.commit()
    db.refresh(prod)
    return prod


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(prod)
    db.commit()
    return {"message": "Product deleted"}