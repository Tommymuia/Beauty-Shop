# Beauty Shop - Full Integration Implementation Plan

## Current Status
- ✅ Database seeded with 90 products
- ✅ Backend API running
- ✅ Frontend displays products from Redux (with backend fallback)
- ❌ Admin operations not connected to backend
- ❌ Customer operations not connected to backend
- ❌ M-Pesa integration not working
- ❌ Order history not persisting

## Critical Issues to Fix

### 1. Admin User Setup
**Problem**: Cannot create admin due to bcrypt library issue
**Solution**: 
```bash
# Manually create admin in database
psql -U beauty_admin -d beauty_shop_db
INSERT INTO users (email, hashed_password, is_admin, phone_number) 
VALUES ('admin@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgdx4HQ4K', true, '0700000000');
\q
```
**Credentials**: admin@gmail.com / admin123

### 2. Remove Admin Signup
**Files to modify**:
- `FrontEnd/src/features/auth/Login.jsx` - Remove signup link for admin route
- `FrontEnd/src/routes/AppRoutes.jsx` - Remove admin register route

### 3. Connect Admin Add Product to Backend
**Files to modify**:
- `FrontEnd/src/features/admin/AddProduct.jsx` - Call API instead of fake data
- `FrontEnd/src/features/admin/EditProduct.jsx` - Call API for updates
- `FrontEnd/src/features/admin/ManageProducts.jsx` - Call API for delete

**Backend routes needed** (already exist):
- POST /api/products/ - Create product
- PUT /api/products/{id} - Update product  
- DELETE /api/products/{id} - Delete product

### 4. Connect Admin Add User to Backend
**Files to modify**:
- `FrontEnd/src/features/admin/AddUser.jsx` - Call backend API
- `FrontEnd/src/features/admin/ManageUsers.jsx` - Fetch from backend

**Backend route needed**:
- POST /api/users/ - Create user (needs to be added)
- GET /api/users/ - List users (needs to be added)

### 5. Customer Order History
**Files to modify**:
- `FrontEnd/src/features/orders/OrderHistory.jsx` - Fetch from backend
- `FrontEnd/src/features/orders/Checkout.jsx` - Save order to backend

**Backend routes** (already exist):
- POST /api/orders/ - Create order
- GET /api/orders/ - Get user orders

### 6. Admin View Orders
**Files to modify**:
- `FrontEnd/src/features/admin/ManageOrders.jsx` - Fetch all orders from backend
- `FrontEnd/src/features/admin/Dashboard.jsx` - Show order stats

**Backend route needed**:
- GET /api/orders/all - Get all orders (admin only)

### 7. M-Pesa Integration
**Current issue**: M-Pesa credentials in backend are sandbox/test
**Files to check**:
- `beauty_shop_backend/app/services/mpesa_service.py`
- `beauty_shop_backend/app/routes/orders.py`

**Fix**: Verify M-Pesa credentials and STK push implementation

### 8. Admin Logout with Password
**Files to modify**:
- `FrontEnd/src/layouts/AdminLayout.jsx` - Add password modal on logout

## Implementation Priority

### Phase 1: Critical (Do First)
1. Create admin user manually in database
2. Remove admin signup option
3. Connect admin product operations to backend
4. Connect customer orders to backend

### Phase 2: Important
5. Admin view all orders
6. Customer order history
7. Admin add/manage users

### Phase 3: Enhancement
8. M-Pesa integration fix
9. Admin logout password requirement

## Quick Fixes You Can Do Now

### Fix 1: Create Admin User
```bash
psql -U beauty_admin -d beauty_shop_db
INSERT INTO users (email, hashed_password, is_admin, phone_number) 
VALUES ('admin@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgdx4HQ4K', true, '0700000000');
```

### Fix 2: Test Backend Endpoints
```bash
# Test products endpoint
curl http://localhost:8000/api/products/

# Test create product
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":1000,"category_id":1,"stock_quantity":10}'
```

## Estimated Time
- Phase 1: 4-6 hours
- Phase 2: 3-4 hours  
- Phase 3: 2-3 hours
**Total**: 9-13 hours of development work

## Notes
- The app currently works with fake data as fallback
- Backend API exists but frontend doesn't call it for admin operations
- Need to add authentication headers to all API calls
- Need to add admin-only routes protection in backend
