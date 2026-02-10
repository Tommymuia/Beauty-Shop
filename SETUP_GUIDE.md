# Beauty Shop - Complete Setup Guide

## Step-by-Step Backend Setup with Database

### Step 1: Start PostgreSQL Service
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```
You should see "active (running)" in green.

### Step 2: Create Database and User
```bash
sudo -u postgres psql
```

In the PostgreSQL prompt, run these commands one by one:
```sql
DROP DATABASE IF EXISTS beauty_shop_db;
DROP USER IF EXISTS beauty_admin;
CREATE USER beauty_admin WITH PASSWORD 'Group8';
CREATE DATABASE beauty_shop_db OWNER beauty_admin;
GRANT ALL PRIVILEGES ON DATABASE beauty_shop_db TO beauty_admin;
\c beauty_shop_db
GRANT ALL ON SCHEMA public TO beauty_admin;
\q
```

### Step 3: Run Database Migrations
```bash
cd ~/Development/code./se-prep/phase-five/Beauty-Shop/beauty_shop_backend
source ../venv/bin/activate  # If not already activated
alembic upgrade head
```
You should see: "Running upgrade -> [migration_id], add image rating isnew to products"

### Step 4: Seed Database with 90 Products
```bash
python seed_products.py
```
You should see: "✅ Successfully added 90 products (30 per category)"

### Step 5: Start Backend Server
```bash
python run.py
```
Backend will run on http://localhost:8000

### Step 6: Start Frontend (New Terminal)
Open a new terminal:
```bash
cd ~/Development/code./se-prep/phase-five/Beauty-Shop/FrontEnd
npm run dev
```
Frontend will run on http://localhost:5173

### Step 7: Verify Everything Works
1. Open browser: http://localhost:5173
2. You should see 90 products (not just 6)
3. Login with admin credentials
4. Check admin dashboard - should show all products

---

## Quick Start (After Initial Setup)

### Terminal 1 - Backend:
```bash
cd ~/Development/code./se-prep/phase-five/Beauty-Shop/beauty_shop_backend
source ../venv/bin/activate
python run.py
```

### Terminal 2 - Frontend:
```bash
cd ~/Development/code./se-prep/phase-five/Beauty-Shop/FrontEnd
npm run dev
```

---

## Troubleshooting

### PostgreSQL not starting?
```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### Password authentication failed?
Repeat Step 2 to recreate the user.

### No products showing?
1. Check backend is running: `curl http://localhost:8000/api/products/`
2. Re-run seed script: `python seed_products.py`

### Port already in use?
```bash
# Kill process on port 8000
sudo lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
sudo lsof -ti:5173 | xargs kill -9
```

---

## Database Info
- **Database Name**: beauty_shop_db
- **Username**: beauty_admin
- **Password**: Group8
- **Host**: localhost
- **Port**: 5432

## API Endpoints
- Products: http://localhost:8000/api/products/
- Auth: http://localhost:8000/api/auth/
- Cart: http://localhost:8000/api/cart/
- Orders: http://localhost:8000/api/orders/

## Default Admin Credentials
Create an admin user through the registration page, then manually update the database:
```sql
sudo -u postgres psql -d beauty_shop_db
UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';
\q
```
