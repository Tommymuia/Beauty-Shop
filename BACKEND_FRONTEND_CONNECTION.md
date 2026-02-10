# Backend-Frontend Connection Guide

## Overview
The Beauty Shop frontend is now connected to the FastAPI backend using Axios for HTTP requests and Redux Toolkit for state management.

## Setup Instructions

### 1. Backend Setup

```bash
cd beauty_shop_backend

# Install dependencies
pip install -r requirements.txt

# Set up database
# Make sure PostgreSQL is running with:
# Database: beauty_shop_db
# User: beauty_admin
# Password: Group8

# Run migrations
alembic upgrade head

# Seed database (optional)
python seed.py

# Start backend server
python run.py
# or
uvicorn app.main:app --reload --port 8000
```

Backend will run on: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd FrontEnd

# Install dependencies (if not already done)
npm install axios

# Start frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

## API Integration

### Configuration Files

1. **`.env`** - Environment variables
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

2. **`src/services/api.js`** - API service layer
   - Axios instance with base URL
   - Request interceptor for JWT tokens
   - API endpoints for auth, products, cart, orders

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user (returns JWT token)

#### Products
- `GET /api/products` - Get all products (with optional filters)
- `GET /api/products/:id` - Get product by ID
- `POST /api/products` - Create product (admin)
- `PUT /api/products/:id` - Update product (admin)
- `DELETE /api/products/:id` - Delete product (admin)

#### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/:id` - Update cart item
- `DELETE /api/cart/:id` - Remove cart item
- `DELETE /api/cart` - Clear cart

#### Orders
- `POST /api/orders/checkout` - Checkout with M-Pesa
- `GET /api/orders` - Get user's orders
- `GET /api/orders/:id` - Get order details

## Redux Integration

### State Structure
```javascript
{
  auth: {
    user: { email, token },
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
    totalQuantity: number
  },
  wishlist: {
    items: []
  }
}
```

### Async Thunks

#### Auth
- `loginUser({ email, password })` - Login with API
- `registerUser({ email, password })` - Register with API

#### Products
- `fetchProducts(params)` - Fetch products from API
- `fetchProductById(id)` - Fetch single product

## Updated Components

### 1. Login Component
- Uses `loginUser` async thunk
- Displays API errors
- Stores JWT token in localStorage

### 2. Auth Slice
- Added async thunks for login/register
- Handles loading and error states
- Manages JWT token

### 3. Products Slice (New)
- Fetches products from backend
- Manages product state
- Handles loading and errors

## Token Management

JWT tokens are:
1. Stored in `localStorage` after login
2. Automatically added to requests via Axios interceptor
3. Removed on logout

```javascript
// Token is added to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## CORS Configuration

Backend CORS is configured to allow all origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing the Connection

### 1. Test Backend
```bash
curl http://localhost:8000/
# Should return: {"message": "Beauty Shop Backend is Active"}
```

### 2. Test Login
```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 3. Test Products
```bash
curl http://localhost:8000/api/products
```

## Next Steps to Complete Integration

### Components to Update:
1. ✅ Login - Connected
2. ✅ Auth Slice - Connected
3. ✅ Products Slice - Created
4. ⏳ Register - Update to use `registerUser` thunk
5. ⏳ ProductList - Use `fetchProducts` thunk
6. ⏳ ProductDetails - Use `fetchProductById` thunk
7. ⏳ Cart - Connect to cart API
8. ⏳ Checkout - Connect to orders API

### Backend Routes to Add:
1. GET `/api/products/:id` - Get single product
2. PUT `/api/products/:id` - Update product
3. DELETE `/api/products/:id` - Delete product
4. GET `/api/cart` - Get cart
5. PUT `/api/cart/:id` - Update cart item

## Troubleshooting

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS middleware configuration

### 401 Unauthorized
- Check if token is stored in localStorage
- Verify token is being sent in Authorization header

### Connection Refused
- Ensure backend server is running
- Check API_BASE_URL in .env file

### Database Errors
- Verify PostgreSQL is running
- Check database credentials in `database.py`
- Run migrations: `alembic upgrade head`

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://beauty_admin:Group8@localhost/beauty_shop_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Production Deployment

For production:
1. Update CORS to specific origins
2. Use environment-specific API URLs
3. Enable HTTPS
4. Secure JWT secret key
5. Use production database credentials
