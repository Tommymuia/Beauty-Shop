# Beauty Shop - Setup Guide

A full-stack e-commerce application for beauty products with customer and admin interfaces.

## Prerequisites

- **Python 3.8+** - Backend runtime
- **Node.js 16+** and **npm** - Frontend runtime and package manager
- **PostgreSQL 12+** - Database

## Database Setup

1. **Install PostgreSQL** (if not already installed)

2. **Create Database**:
   ```bash
   psql -U postgres
   CREATE DATABASE beauty_shop;
   \q
   ```

3. **Database Credentials**:
   - Host: `localhost`
   - Port: `5432`
   - Database: `beauty_shop`
   - User: `postgres`
   - Password: `Group8`

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd beauty_shop_backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the `beauty_shop_backend` directory:
```env
DATABASE_URL=postgresql://postgres:Group8@localhost:5432/beauty_shop
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run Database Migrations
```bash
alembic upgrade head
```

### 7. Start Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```

Backend will run at: `http://localhost:8000`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd FrontEnd
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Create a `.env` file in the `FrontEnd` directory:
```env
VITE_API_URL=http://localhost:8000/api
```

### 4. Start Frontend Development Server
```bash
npm run dev
```

Frontend will run at: `http://localhost:5173`

## Default Admin Credentials

- **Email**: `admin@gmail.com`
- **Password**: `admin123`

## Project Structure

```
Beauty-Shop/
├── beauty_shop_backend/     # FastAPI backend
│   ├── app/
│   │   ├── models.py        # Database models
│   │   ├── routes/          # API endpoints
│   │   └── main.py          # Application entry point
│   ├── requirements.txt     # Python dependencies
│   └── alembic/             # Database migrations
│
└── FrontEnd/                # React frontend
    ├── src/
    │   ├── features/        # Feature modules
    │   ├── components/      # Reusable components
    │   ├── routes/          # Route configuration
    │   └── store/           # Redux store
    └── package.json         # Node dependencies
```

## Available Scripts

### Backend
- `uvicorn app.main:app --reload` - Start development server with hot reload
- `alembic revision --autogenerate -m "message"` - Create new migration
- `alembic upgrade head` - Apply migrations
- `pytest` - Run tests

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Features

### Customer Features
- Browse products with search and filters
- Add products to cart and wishlist
- Checkout with M-Pesa payment
- View order history and invoices
- Contact support
- User profile management

### Admin Features
- Dashboard with real-time statistics
- Product management (CRUD operations)
- Order management and status updates
- User management
- Customer support messages
- Analytics and reports
- Invoice generation

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Backend Issues

**Database Connection Error**:
- Verify PostgreSQL is running: `sudo service postgresql status`
- Check database credentials in `.env` file
- Ensure database `beauty_shop` exists

**Module Import Errors**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Port Already in Use**:
- Kill process on port 5173: `lsof -ti:5173 | xargs kill -9`
- Or use different port: `npm run dev -- --port 3000`

**API Connection Error**:
- Verify backend is running on port 8000
- Check `VITE_API_URL` in `.env` file

**Module Not Found**:
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

## Tech Stack

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- Alembic - Database migrations
- Pydantic - Data validation
- Python-Jose - JWT authentication

### Frontend
- React 18 - UI library
- Redux Toolkit - State management
- React Router - Routing
- Tailwind CSS - Styling
- Axios - HTTP client
- Lucide React - Icons

## License

This project is for educational purposes.
