import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

from app.main import app
from app.database import Base, get_db
from app.models import User, Product, Category, CartItem, Order
from app.services.auth_service import hash_password, create_access_token

# Load environment variables
load_dotenv()

# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create test client
Base.metadata.create_all(bind=engine)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide database session for fixtures"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_category(db_session):
    """Create a test category"""
    category = Category(name="Beauty Products")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def test_product(db_session, test_category):
    """Create a test product"""
    product = Product(
        name="Face Cream",
        description="Premium face cream",
        price=1500.0,
        stock_quantity=100,
        category_id=test_category.id
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="testuser@example.com",
        password=hash_password("Test123!"),
        phone_number="0712345678",
        is_admin=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session):
    """Create a test admin user"""
    user = User(
        email="admin@example.com",
        password=hash_password("Admin123!"),
        is_admin=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_token(test_user):
    """Generate test JWT token"""
    return create_access_token(data={"sub": test_user.email})


@pytest.fixture
def auth_headers(test_token):
    """Auth headers with token"""
    return {"Authorization": f"Bearer {test_token}"}


# ====== AUTH ENDPOINTS TESTS ======

class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_register_success(self):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "NewPass123!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_register_duplicate_email(self, test_user):
        """Test registration with duplicate email"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "testuser@example.com",
                "password": "Password123!"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_login_success(self, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "Test123!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_email(self):
        """Test login with non-existent email"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Password123!"
            }
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_invalid_password(self, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "WrongPassword123!"
            }
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]


# ====== PRODUCT ENDPOINTS TESTS ======

class TestProductEndpoints:
    """Test product endpoints"""
    
    def test_get_all_products_empty(self):
        """Test getting products when none exist"""
        response = client.get("/api/products/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_products(self, test_product):
        """Test getting all products"""
        response = client.get("/api/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Face Cream"
        assert data[0]["price"] == 1500.0
    
    def test_get_products_by_category(self, test_product):
        """Test filtering products by category"""
        category_id = test_product.category_id
        response = client.get(f"/api/products/?category_id={category_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_id"] == category_id
    
    def test_get_products_by_nonexistent_category(self):
        """Test filtering by non-existent category"""
        response = client.get("/api/products/?category_id=999")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_products_by_search(self, test_product):
        """Test searching products by name"""
        response = client.get("/api/products/?search=Face")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Face" in data[0]["name"]
    
    def test_get_products_by_search_no_match(self):
        """Test search with no matching product"""
        response = client.get("/api/products/?search=Nonexistent")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_products_by_search_case_insensitive(self, test_product):
        """Test case-insensitive search"""
        response = client.get("/api/products/?search=face")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1


# ====== CART ENDPOINTS TESTS ======

class TestCartEndpoints:
    """Test shopping cart endpoints"""
    
    def test_add_to_cart_success(self, test_product, auth_headers):
        """Test successfully adding product to cart"""
        response = client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={
                "product_id": test_product.id,
                "quantity": 2
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "Added" in data["message"]
        assert "Face Cream" in data["message"]
    
    def test_add_to_cart_nonexistent_product(self, auth_headers):
        """Test adding non-existent product to cart"""
        response = client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={
                "product_id": 999,
                "quantity": 1
            }
        )
        assert response.status_code == 404
        assert "Product not found" in response.json()["detail"]
    
    def test_add_to_cart_without_auth(self, test_product):
        """Test adding to cart without authentication"""
        response = client.post(
            "/api/cart/add",
            json={
                "product_id": test_product.id,
                "quantity": 1
            }
        )
        assert response.status_code == 401
    
    def test_add_to_cart_update_quantity(self, test_product, test_user, auth_headers, db_session):
        """Test updating quantity when adding same product again"""
        # Add product first time
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 2}
        )
        
        # Add same product again
        response = client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 3}
        )
        
        assert response.status_code == 200
        
        # Verify quantity is updated
        cart_items = db_session.query(CartItem).filter(
            CartItem.user_id == test_user.id,
            CartItem.product_id == test_product.id
        ).all()
        assert len(cart_items) == 1
        assert cart_items[0].quantity == 5
    
    def test_view_cart_empty(self, auth_headers):
        """Test viewing empty cart"""
        response = client.get("/api/cart/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []
    
    def test_view_cart_with_items(self, test_product, test_user, auth_headers):
        """Test viewing cart with items"""
        # Add items to cart
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 2}
        )
        
        response = client.get("/api/cart/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["product_id"] == test_product.id
        assert data[0]["quantity"] == 2
    
    def test_view_cart_without_auth(self):
        """Test viewing cart without authentication"""
        response = client.get("/api/cart/")
        assert response.status_code == 401
    
    def test_view_cart_only_user_items(self, test_product, test_user, db_session, auth_headers):
        """Test that users only see their cart items"""
        # Add to first user's cart
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 1}
        )
        
        # Create second user
        user2 = User(
            email="user2@example.com",
            password=hash_password("Pass123!"),
            phone_number="0787654321"
        )
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)
        
        token2 = create_access_token(data={"sub": user2.email})
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Add to second user's cart
        client.post(
            "/api/cart/add",
            headers=headers2,
            json={"product_id": test_product.id, "quantity": 3}
        )
        
        # View first user's cart
        response = client.get("/api/cart/", headers=auth_headers)
        data = response.json()
        assert len(data) == 1
        assert data[0]["quantity"] == 1


# ====== ORDER/CHECKOUT ENDPOINTS TESTS ======

class TestOrderEndpoints:
    """Test order/checkout endpoints"""
    
    def test_checkout_success(self, test_product, test_user, auth_headers, db_session):
        """Test successful checkout"""
        # Add product to cart
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 2}
        )
        
        # Checkout
        response = client.post(
            "/api/orders/checkout",
            headers=auth_headers,
            json={"phone_number": "0712345678"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "order_details" in data
        assert data["order_details"]["total"] == 3000.0
        assert "INV-" in data["order_details"]["invoice"]
    
    def test_checkout_empty_cart(self, test_user, auth_headers):
        """Test checkout with empty cart"""
        response = client.post(
            "/api/orders/checkout",
            headers=auth_headers,
            json={"phone_number": "0712345678"}
        )
        
        assert response.status_code == 400
        assert "Cart is empty" in response.json()["detail"]
    
    def test_checkout_without_auth(self, test_product):
        """Test checkout without authentication"""
        response = client.post(
            "/api/orders/checkout",
            json={"phone_number": "0712345678"}
        )
        
        assert response.status_code == 401
    
    def test_checkout_clears_cart(self, test_product, test_user, auth_headers, db_session):
        """Test that checkout clears the user's cart"""
        # Add to cart
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 1}
        )
        
        # Checkout
        client.post(
            "/api/orders/checkout",
            headers=auth_headers,
            json={"phone_number": "0712345678"}
        )
        
        # Verify cart is empty
        response = client.get("/api/cart/", headers=auth_headers)
        assert response.json() == []
    
    def test_checkout_creates_order(self, test_product, test_user, auth_headers, db_session):
        """Test that checkout creates an order in database"""
        # Add to cart and checkout
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 1}
        )
        
        response = client.post(
            "/api/orders/checkout",
            headers=auth_headers,
            json={"phone_number": "0712345678"}
        )
        
        # Verify order exists
        order = db_session.query(Order).filter(
            Order.user_id == test_user.id
        ).first()
        
        assert order is not None
        assert order.total_amount == 1500.0
        assert order.status == "pending"
    
    def test_checkout_multiple_products(self, test_product, test_user, auth_headers, db_session, test_category):
        """Test checkout with multiple different products"""
        # Create another product
        product2 = Product(
            name="Lipstick",
            description="Premium lipstick",
            price=800.0,
            stock_quantity=50,
            category_id=test_category.id
        )
        db_session.add(product2)
        db_session.commit()
        db_session.refresh(product2)
        
        # Add both products to cart
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": test_product.id, "quantity": 2}
        )
        client.post(
            "/api/cart/add",
            headers=auth_headers,
            json={"product_id": product2.id, "quantity": 3}
        )
        
        # Checkout
        response = client.post(
            "/api/orders/checkout",
            headers=auth_headers,
            json={"phone_number": "0712345678"}
        )
        
        assert response.status_code == 200
        # Total: (1500 * 2) + (800 * 3) = 3000 + 2400 = 5400
        assert response.json()["order_details"]["total"] == 5400.0


# ====== ROOT ENDPOINT TEST ======

class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test that the root endpoint works"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Beauty Shop Backend is Active" in data["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
