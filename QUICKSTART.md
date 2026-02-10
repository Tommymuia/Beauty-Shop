# 🚀 Quick Start - Beauty Shop

## One Command Start

```bash
./start.sh
```

This will:
1. Start PostgreSQL (if not running)
2. Run database migrations
3. Start backend on http://localhost:8000
4. Start frontend on http://localhost:5173

## Manual Start

### Backend
```bash
cd beauty_shop_backend
python run.py
```

### Frontend (in new terminal)
```bash
cd FrontEnd
npm run dev
```

## Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Test the Connection

1. Open http://localhost:5173
2. Click "Register" or "Login"
3. Try to register a new account
4. If successful, you're connected! ✅

## Troubleshooting

### Backend won't start
```bash
# Check PostgreSQL
sudo service postgresql status
sudo service postgresql start

# Run migrations
cd beauty_shop_backend
alembic upgrade head
```

### Frontend errors
```bash
cd FrontEnd
npm install
npm run dev
```

### Connection refused
- Ensure backend is running on port 8000
- Check `.env` file has correct API URL
- Verify CORS is enabled in backend

## Features Available

✅ User Registration & Login  
✅ Product Browsing  
✅ Shopping Cart  
✅ M-Pesa Checkout  
✅ Admin Dashboard  
✅ Product Management  

## Default Test Accounts

Create your own by registering at http://localhost:5173/register

## Stop Servers

Press `Ctrl+C` in the terminal running `start.sh`

Or manually:
```bash
# Find and kill processes
pkill -f "python run.py"
pkill -f "vite"
```
