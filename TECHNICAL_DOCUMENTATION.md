# Beauty Shop - Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Database Schema](#database-schema)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [API Documentation](#api-documentation)
7. [State Management](#state-management)
8. [Authentication Flow](#authentication-flow)
9. [Data Flow](#data-flow)
10. [Deployment](#deployment)

---

## 1. System Architecture

### High-Level Architecture
```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │◄───────►│  FastAPI Backend│◄───────►│   PostgreSQL    │
│   (Port 5173)   │  HTTP   │   (Port 8000)   │   SQL   │    Database     │
│                 │         │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
        │                           │
        │                           │
        ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  Redux Store    │         │  M-Pesa API     │
│  (State Mgmt)   │         │  (Payments)     │
└─────────────────┘         └─────────────────┘
```

### Component Interaction
- **Frontend**: React 19 SPA with Redux Toolkit for state management
- **Backend**: FastAPI REST API with SQLAlchemy ORM
- **Database**: PostgreSQL for persistent data storage
- **External Services**: M-Pesa Daraja API for payment processing

---

## 2. Technology Stack

### Frontend
- **Framework**: React 19.0.0
- **State Management**: Redux Toolkit 2.5.0
- **Routing**: React Router DOM 7.1.1
- **HTTP Client**: Axios 1.7.9
- **Styling**: Tailwind CSS 3.4.17
- **Icons**: Lucide React 0.469.0
- **Build Tool**: Vite 6.0.5
- **Testing**: Jest 29.7.0, React Testing Library 16.1.0

### Backend
- **Framework**: FastAPI 0.115.6
- **ORM**: SQLAlchemy 2.0.36
- **Database Driver**: psycopg2-binary 2.9.10
- **Authentication**: JWT (python-jose 3.3.0)
- **Password Hashing**: bcrypt 4.2.1
- **ASGI Server**: Uvicorn 0.34.0
- **Environment**: Python 3.8+

### Database
- **RDBMS**: PostgreSQL 12+
- **Database Name**: beauty_shop_db
- **User**: beauty_admin
- **Port**: 5432

---

## 3. Database Schema

### Entity Relationship Diagram
```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    users     │       │  categories  │       │   products   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │       │ id (PK)      │
│ email        │       │ name         │       │ name         │
│ password     │       └──────────────┘       │ description  │
│ phone_number │              │               │ price        │
│ is_admin     │              │               │ stock_qty    │
└──────────────┘              │               │ category_id  │
       │                      └──────────────►│ image        │
       │                                      │ rating       │
       │                                      │ is_new       │
       │                                      └──────────────┘
       │                                             │
       │                                             │
       ▼                                             ▼
┌──────────────┐                            ┌──────────────┐
│    orders    │                            │   reviews    │
├──────────────┤                            ├──────────────┤
│ id (PK)      │                            │ id (PK)      │
│ user_id (FK) │                            │ product_id   │
│ total_amount │                            │ user_id (FK) │
│ status       │                            │ user_name    │
│ created_at   │                            │ rating       │
│ invoice_no   │                            │ comment      │
│ customer_json│                            │ created_at   │
│ items_json   │                            └──────────────┘
└──────────────┘
       │
       ▼
┌──────────────┐
│  cart_items  │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ product_id   │
│ quantity     │
└──────────────┘
```

### Table Definitions

#### users
- **Purpose**: Store user accounts (customers and admins)
- **Key Fields**: email (unique), password (hashed), is_admin (boolean)
- **Relationships**: One-to-Many with orders, cart_items, reviews

#### categories
- **Purpose**: Product categorization
- **Values**: Skincare (id=1), Haircare (id=2), Makeup (id=3)
- **Relationships**: One-to-Many with products

#### products
- **Purpose**: Store product catalog
- **Key Fields**: name, price (KES), stock_quantity, rating, is_new
- **Relationships**: Many-to-One with categories, One-to-Many with reviews

#### orders
- **Purpose**: Store customer orders
- **Key Fields**: total_amount, status, invoice_number, customer_json, items_json
- **JSON Fields**: customer_json (billing info), items_json (order items)
- **Status Values**: pending, processing, shipped, delivered

#### reviews
- **Purpose**: Store product reviews
- **Key Fields**: product_id, user_name, rating (1-5), comment
- **Relationships**: Many-to-One with products and users

#### cart_items
- **Purpose**: Store shopping cart items
- **Key Fields**: user_id, product_id, quantity
- **Relationships**: Many-to-One with users and products

---

## 4. Backend Architecture

### Directory Structure
```
beauty_shop_backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── products.py      # Product CRUD
│   │   ├── orders.py        # Order management
│   │   ├── cart.py          # Shopping cart
│   │   ├── users.py         # User management
│   │   └── reviews.py       # Product reviews
│   └── utils/
│       └── mpesa.py         # M-Pesa integration
├── venv/                    # Virtual environment
├── .env                     # Environment variables
└── requirements.txt         # Python dependencies
```

### Core Components

#### main.py
- **Purpose**: Application entry point
- **Responsibilities**:
  - Initialize FastAPI app
  - Configure CORS middleware
  - Register API routers
  - Define root endpoint

#### database.py
- **Purpose**: Database connection management
- **Key Functions**:
  - `get_db()`: Dependency injection for database sessions
  - Database URL configuration
  - Session management

#### models.py
- **Purpose**: SQLAlchemy ORM models
- **Models**: User, Category, Product, Order, CartItem, Review
- **Features**: Relationships, JSON serialization methods

#### schemas.py
- **Purpose**: Pydantic models for request/response validation
- **Schemas**: UserCreate, ProductSchema, OrderCreate, ReviewCreate
- **Validation**: Type checking, required fields, data transformation

### API Routes

#### Authentication (`/api/auth`)
- `POST /register`: Create new user account
- `POST /login`: Authenticate user, return JWT token
- `GET /me`: Get current user profile

#### Products (`/api/products`)
- `GET /`: List all products (with filters)
- `GET /{id}`: Get product by ID
- `POST /`: Create product (admin only)
- `PUT /{id}`: Update product (admin only)
- `DELETE /{id}`: Delete product (admin only)

#### Orders (`/api/orders`)
- `POST /`: Create new order
- `GET /`: Get user's orders
- `GET /all`: Get all orders (admin only)
- `GET /{id}`: Get order by ID
- `PUT /{id}/status`: Update order status (admin only)

#### Users (`/api/users`)
- `GET /`: Get all users (admin only)
- `POST /`: Create user (admin only)
- `PUT /{id}`: Update user (admin only)
- `DELETE /{id}`: Delete user (admin only)

#### Reviews (`/api/reviews`)
- `POST /`: Create product review
- `GET /product/{id}`: Get reviews for product

#### Cart (`/api/cart`)
- `GET /`: Get user's cart
- `POST /`: Add item to cart
- `PUT /{id}`: Update cart item
- `DELETE /{id}`: Remove cart item

---

## 5. Frontend Architecture

### Directory Structure
```
FrontEnd/
├── src/
│   ├── app/
│   │   ├── store.js         # Redux store configuration
│   │   └── rootReducer.js   # Combine reducers
│   ├── features/
│   │   ├── auth/            # Authentication
│   │   │   ├── authSlice.js
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── products/        # Product catalog
│   │   │   ├── productsSlice.js
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductDetails.jsx
│   │   │   └── ProductList.jsx
│   │   ├── cart/            # Shopping cart
│   │   │   ├── cartSlice.js
│   │   │   ├── Cart.jsx
│   │   │   └── CartItem.jsx
│   │   ├── orders/          # Order management
│   │   │   ├── ordersSlice.js
│   │   │   ├── Checkout.jsx
│   │   │   ├── OrderHistory.jsx
│   │   │   └── Invoice.jsx
│   │   ├── admin/           # Admin dashboard
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ManageProducts.jsx
│   │   │   ├── ManageOrders.jsx
│   │   │   └── ManageUsers.jsx
│   │   └── wishlist/        # Wishlist feature
│   │       └── wishlistSlice.js
│   ├── pages/               # Page components
│   │   ├── Home.jsx
│   │   ├── CategoryPage.jsx
│   │   ├── NewArrivals.jsx
│   │   ├── About.jsx
│   │   └── ContactUs.jsx
│   ├── components/          # Reusable components
│   │   ├── Navbar.jsx
│   │   ├── Footer.jsx
│   │   ├── MpesaPayment.jsx
│   │   └── Notification.jsx
│   ├── layouts/             # Layout wrappers
│   │   ├── MainLayout.jsx
│   │   └── AdminLayout.jsx
│   ├── routes/              # Routing configuration
│   │   └── AppRoutes.jsx
│   ├── services/            # API services
│   │   ├── api.js           # Axios instance & endpoints
│   │   └── fakeData.js      # Fallback data
│   ├── styles/              # Global styles
│   │   └── globals.css
│   ├── App.jsx              # Root component
│   └── main.jsx             # Entry point
├── public/                  # Static assets
├── .env                     # Environment variables
└── package.json             # Dependencies
```

### Component Hierarchy
```
App
├── ScrollToTop
├── AppRoutes
│   ├── MainLayout
│   │   ├── Navbar
│   │   ├── [Page Component]
│   │   └── Footer
│   └── AdminLayout
│       ├── Sidebar
│       ├── [Admin Component]
│       └── LogoutModal
└── Toast Notifications
```

### Key Components

#### App.jsx
- Root component
- Renders AppRoutes
- Manages global notifications

#### AppRoutes.jsx
- Route configuration
- Protected routes for admin
- Layout wrappers

#### MainLayout.jsx
- Customer-facing layout
- Navbar with cart/wishlist
- Footer

#### AdminLayout.jsx
- Admin dashboard layout
- Sidebar navigation
- Logout with password confirmation

---

## 6. API Documentation

### Base URL
```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

### Authentication
All protected endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

### Response Format
```json
{
  "data": {},
  "message": "Success",
  "status": 200
}
```

### Error Format
```json
{
  "detail": "Error message",
  "status": 400
}
```

### Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Register new user |
| POST | /auth/login | No | Login user |
| GET | /auth/me | Yes | Get user profile |
| GET | /products/ | No | List products |
| GET | /products/{id} | No | Get product |
| POST | /products/ | Admin | Create product |
| PUT | /products/{id} | Admin | Update product |
| DELETE | /products/{id} | Admin | Delete product |
| POST | /orders/ | Yes | Create order |
| GET | /orders/ | Yes | Get user orders |
| GET | /orders/all | Admin | Get all orders |
| PUT | /orders/{id}/status | Admin | Update order status |
| GET | /users/ | Admin | List users |
| POST | /users/ | Admin | Create user |
| PUT | /users/{id} | Admin | Update user |
| DELETE | /users/{id} | Admin | Delete user |
| POST | /reviews/ | Yes | Create review |
| GET | /reviews/product/{id} | No | Get product reviews |

---

## 7. State Management

### Redux Store Structure
```javascript
{
  auth: {
    user: { email, is_admin, token },
    isAuthenticated: boolean,
    isLoading: boolean,
    error: string
  },
  products: {
    items: [],
    currentProduct: {},
    isLoading: boolean,
    error: string
  },
  cart: {
    items: [],
    totalAmount: number,
    notification: { message, isVisible, type }
  },
  orders: {
    userOrders: [],
    allOrders: [],
    isLoading: boolean,
    error: string
  },
  wishlist: {
    items: [],
    notification: { message, isVisible, type }
  }
}
```

### Redux Slices

#### authSlice
- **Actions**: loginUser, registerUser, logout
- **State**: user, isAuthenticated, isLoading, error
- **Persistence**: JWT token in localStorage

#### productsSlice
- **Actions**: fetchProducts, fetchProductById
- **State**: items, currentProduct, isLoading
- **Fallback**: Uses fakeData if API fails

#### cartSlice
- **Actions**: addItemToCart, removeItem, updateQuantity, clearCart
- **State**: items, totalAmount
- **Persistence**: localStorage

#### ordersSlice
- **Actions**: createOrder, fetchUserOrders, fetchAllOrders
- **State**: userOrders, allOrders, isLoading

---

## 8. Authentication Flow

### Registration Flow
```
User fills form → Frontend validates → POST /api/auth/register
→ Backend creates user → Returns JWT → Redirect to login
```

### Login Flow
```
User enters credentials → POST /api/auth/login
→ Backend validates → Returns JWT + user data
→ Store token in localStorage → Update Redux state
→ Redirect based on role (admin → /admin, customer → /)
```

### Admin Login (Temporary Workaround)
```
Hardcoded: admin@gmail.com / admin123
→ Bypasses backend authentication
→ Sets is_admin: true in Redux
→ Redirects to /admin
```

### Protected Routes
```javascript
<ProtectedRoute>
  {isAuthenticated && user?.is_admin ? (
    <AdminComponent />
  ) : (
    <Navigate to="/login" />
  )}
</ProtectedRoute>
```

---

## 9. Data Flow

### Product Display Flow
```
1. Component mounts → useEffect triggers
2. dispatch(fetchProducts())
3. Redux thunk → axios.get('/api/products/')
4. Backend queries database
5. Returns products with category names
6. Redux updates state
7. Component re-renders with data
```

### Checkout Flow
```
1. User fills shipping form
2. Selects payment method (Card/M-Pesa)
3. If M-Pesa: Opens modal → Simulates STK Push
4. On success: dispatch(createOrder(payload))
5. Backend creates order in database
6. Returns order ID
7. dispatch(clearCart())
8. Navigate to /invoice/{orderId}
```

### Review Submission Flow
```
1. User writes review on ProductDetails
2. POST /api/reviews/ with product_id, rating, comment
3. Backend saves to reviews table
4. Frontend refetches reviews
5. New review appears immediately
```

---

## 10. Deployment

### Environment Variables

#### Backend (.env)
```
DATABASE_URL=postgresql://beauty_admin:Group8@localhost:5432/beauty_shop_db
SECRET_KEY=your-secret-key
MPESA_CONSUMER_KEY=...
MPESA_CONSUMER_SECRET=...
```

#### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Database Setup
```bash
# Create database
createdb beauty_shop_db

# Run migrations (create tables)
python seed_products.py

# Create admin user
python create_admin.py
```

### Backend Deployment
```bash
cd beauty_shop_backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment
```bash
cd FrontEnd
npm install
npm run build
npm run preview  # or deploy dist/ to hosting
```

### Production Considerations
1. Use environment-specific .env files
2. Enable HTTPS
3. Configure proper CORS origins
4. Use production database
5. Implement rate limiting
6. Add logging and monitoring
7. Set up CI/CD pipeline
8. Configure backup strategy

---

## Key Design Decisions

### 1. Currency: Kenyan Shillings (KES)
- All prices stored and displayed in KES
- No conversion multipliers in frontend
- Backend stores prices as Float

### 2. Role-Based Access Control
- Only 2 roles: admin and customer
- is_admin boolean flag in User model
- Protected routes in frontend
- Middleware checks in backend

### 3. Category Mapping
- Database: category_id (1, 2, 3)
- Frontend: category name (Skincare, Haircare, Makeup)
- Backend transforms on response

### 4. Order Storage
- customer_json: Stores billing information
- items_json: Stores order items array
- Allows flexible schema without migrations

### 5. Authentication Workaround
- bcrypt broken in Python 3.8
- Frontend bypasses backend for admin login
- Hardcoded: admin@gmail.com / admin123
- TODO: Fix bcrypt or upgrade Python

### 6. M-Pesa Integration
- Simulated STK Push (80% success rate)
- Real integration requires Daraja API setup
- Callback URL needs public endpoint

---

## Testing

### Frontend Tests
- Location: `FrontEnd/src/__tests__/`
- Framework: Jest + React Testing Library
- Coverage: Cart, Auth, Products, Currency
- Run: `npm test`

### Backend Tests
- TODO: Implement pytest tests
- Test API endpoints
- Test database operations
- Test authentication

---

## Known Issues & Workarounds

1. **bcrypt Authentication**: Broken in Python 3.8
   - Workaround: Frontend bypasses backend login for admin

2. **M-Pesa Integration**: Currently simulated
   - Requires: Valid callback URL, Daraja API credentials

3. **User Model**: Simplified (email + password only)
   - Missing: firstName, lastName, address fields

4. **Product Images**: Using placeholder URLs
   - TODO: Implement image upload to cloud storage

---

## Future Enhancements

1. Real M-Pesa Daraja API integration
2. Fix bcrypt authentication
3. Add user profile management
4. Email notifications for orders
5. Product image upload (AWS S3/Cloudinary)
6. Advanced search and filters
7. Wishlist backend persistence
8. Admin analytics dashboard
9. Export reports (PDF/CSV)
10. Multi-language support

---

## Conclusion

This Beauty Shop application demonstrates a full-stack e-commerce solution with:
- Modern React frontend with Redux state management
- RESTful FastAPI backend with PostgreSQL database
- Role-based access control
- Payment integration (M-Pesa)
- Product reviews and ratings
- Order management system
- Admin dashboard

The architecture is modular, scalable, and follows industry best practices for separation of concerns, state management, and API design.
