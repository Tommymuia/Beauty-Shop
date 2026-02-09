from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import CartItem, Product, User
from app.schemas import CartItemCreate, CartItemResponse
from app.routes.auth import get_current_user 

router = APIRouter(prefix="/api/v1/cart", tags=["cart"])

@router.get("/", response_model=List[CartItemResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all cart items for authenticated user with product details"""
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .options(joinedload(CartItem.product))  # Prevent N+1 queries
        .all()
    )

@router.post("/", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate quantity
    if item.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero"
        )
    
    # Verify product exists and is active
    product = db.query(Product).filter(
        Product.id == item.product_id,
        Product.is_active == True  # Critical: prevent adding deleted/inactive products
    ).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or unavailable")
    
    # Stock validation (if applicable to business logic)
    if hasattr(product, 'stock') and product.stock is not None and item.quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} units available in stock"
        )
    
    # Handle existing cart item
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if cart_item:
        new_quantity = cart_item.quantity + item.quantity
        # Re-validate total quantity after merge
        if new_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resulting quantity must be greater than zero"
            )
        if hasattr(product, 'stock') and product.stock is not None and new_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cart quantity exceeds available stock ({product.stock} units)"
            )
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
        
    db.delete(cart_item)
    db.commit()
    return  # Explicitly return None for 204 responses

@router.put("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    item_update: CartItemCreate,  # Note: Only quantity is used; product_id ignored
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Critical validation: quantity must be positive
    if item_update.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero"
        )
    
    # Verify product still exists and is active
    product = db.query(Product).filter(
        Product.id == cart_item.product_id,
        Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product no longer available"
        )
    
    # Stock validation
    if hasattr(product, 'stock') and product.stock is not None and item_update.quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} units available in stock"
        )
    
    cart_item.quantity = item_update.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.post("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove all items from user's cart"""
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return  # Consistent 204 response with no content