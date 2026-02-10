# Quick Frontend-Backend Connection Guide

## ✅ Minimal Changes Approach

The frontend and backend are now connected using an **adapter layer** that transforms data between formats without changing either system significantly.

## What Was Done

### 1. Created Adapter Layer (`src/services/adapter.js`)
- Transforms backend data (category_id, stock_quantity) to frontend format (category, stock)
- Maps category IDs to names: 1=Skincare, 2=Haircare, 3=Makeup
- Provides default values for missing fields (image, rating, isNew)

### 2. Updated API Service (`src/services/api.js`)
- Uses adapter to transform all API responses
- Handles missing backend endpoints gracefully
- Falls back to local operations when endpoints don't exist

### 3. Updated Products Slice
- Falls back to fake data if backend is unavailable
- Seamlessly switches between backend and local data
- No errors if backend is down

## How It Works

### Authentication ✅
```javascript
// Works directly - no transformation needed
authAPI.login(email, password)
authAPI.register(email, password)
```

### Products ✅
```javascript
// Backend returns: { id, name, category_id: 1, stock_quantity: 50 }
// Frontend receives: { id, name, category: "Skincare", stock: 50, image, rating }
productsAPI.getAll()
```

### Cart ⚠️
```javascript
// Backend: POST /cart/add
// Frontend uses: cartAPI.addItem(productId, quantity)
// Missing endpoints (update/delete) use local state
```

### Orders ⚠️
```javascript
// Checkout works: ordersAPI.checkout(phoneNumber)
// Order history falls back to empty array if endpoint missing
```

## Running the System

### Option 1: With Backend (Full Features)
```bash
# Terminal 1 - Backend
cd beauty_shop_backend
python run.py

# Terminal 2 - Frontend
cd FrontEnd
npm run dev
```

### Option 2: Frontend Only (Fake Data)
```bash
cd FrontEnd
npm run dev
# Uses fake data automatically if backend is unavailable
```

## What Works

### ✅ Fully Functional
- User registration and login
- JWT authentication
- Product listing (with data transformation)
- Add to cart
- Checkout with M-Pesa
- Invoice generation

### ⚠️ Partially Functional (Uses Local State)
- Cart update/delete (works in UI, not persisted)
- Order history (shows empty if backend unavailable)
- Product CRUD (admin features use fake data)

### 🔄 Graceful Degradation
- If backend is down, frontend uses fake data
- No errors or crashes
- Seamless user experience

## Testing

### 1. Test Authentication
```bash
# Backend must be running
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### 2. Test Products
```bash
# Should return products with category_id
curl http://localhost:8000/api/products
```

### 3. Test Frontend
- Open http://localhost:5173
- Try login/register
- Browse products (will show transformed data)
- Add to cart (will call backend)

## Data Transformation Example

**Backend Response:**
```json
{
  "id": 1,
  "name": "Vitamin C Serum",
  "description": "Brightening serum",
  "price": 6240.0,
  "category_id": 1,
  "stock_quantity": 50
}
```

**Frontend Receives:**
```javascript
{
  id: 1,
  name: "Vitamin C Serum",
  description: "Brightening serum",
  price: 6240,
  category: "Skincare",  // Transformed from category_id: 1
  stock: 50,             // Transformed from stock_quantity
  image: "default-url",  // Added default
  rating: 4.5,           // Added default
  isNew: false          // Added default
}
```

## Benefits of This Approach

1. **No Backend Changes** - Backend code remains unchanged
2. **No Major Frontend Changes** - Existing components work as-is
3. **Graceful Degradation** - Works with or without backend
4. **Easy Testing** - Can test frontend independently
5. **Future-Proof** - Easy to update when backend adds missing fields

## Limitations

- Cart operations (update/delete) not persisted to backend
- Order history requires backend endpoint (returns empty otherwise)
- Product images use defaults (backend doesn't store images yet)
- Admin CRUD operations use fake data

## Next Steps (Optional)

If you want full backend integration:
1. Add missing endpoints to backend (see COMPATIBILITY_ANALYSIS.md)
2. Add image, rating, is_new fields to Product model
3. Run database migration
4. Update seed data

But the system works now with minimal changes! 🎉
