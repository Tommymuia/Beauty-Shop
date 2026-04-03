# Beauty Shop 💄

A full-stack e-commerce web application for beauty products, built with **FastAPI** (Python) and **React** (Vite). It supports user authentication, product browsing, cart management, order placement, M-Pesa payments, and PDF invoice generation via email.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Seeding the Database](#seeding-the-database)

---

## Features

- User registration and login with JWT authentication
- Browse products by category (Skincare, Haircare, Makeup)
- Search products by name
- Add/remove/update items in the cart
- Place orders with customer details
- M-Pesa STK Push payment integration (Safaricom Daraja API)
- Auto-generated PDF invoices sent to customer email
- Admin order management
- User profile management

---

## Tech Stack

### Backend
| Tool | Purpose |
|------|---------|
| FastAPI | REST API framework |
| SQLAlchemy | ORM |
| SQLite | Database (default) |
| Pydantic v2 | Data validation |
| python-jose | JWT authentication |
| passlib + bcrypt | Password hashing |
| ReportLab | PDF invoice generation |
| python-dotenv | Environment config |
| Uvicorn | ASGI server |
| Alembic | Database migrations |

### Frontend
| Tool | Purpose |
|------|---------|
| React 19 | UI framework |
| Vite | Build tool |
| Redux Toolkit | State management |
| React Router v7 | Client-side routing |
| Axios | HTTP client |
| Tailwind CSS v4 | Styling |
| Lucide React | Icons |

---

## Project Structure

```
Beauty-Shop/
├── beauty_shop_backend/        # FastAPI backend
│   ├── app/
│   │   ├── routes/             # API route handlers
│   │   │   ├── auth.py         # Register, login, profile
│   │   │   ├── products.py     # Product CRUD
│   │   │   ├── orders.py       # Orders, checkout, M-Pesa
│   │   │   └── cart.py         # Cart management
│   │   ├── services/           # Business logic
│   │   ├── utils/              # Invoice, email, M-Pesa helpers
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── database.py         # DB connection
│   │   └── main.py             # FastAPI app entry point
│   ├── alembic/                # DB migrations
│   ├── invoices/               # Generated PDF invoices
│   ├── seed.py                 # Database seeder
│   ├── run.py                  # Server entry point
│   ├── .env                    # Environment variables
│   └── requirements.txt
│
└── FrontEnd/                   # React frontend
    ├── src/
    │   ├── app/                # Redux store setup
    │   ├── features/           # Redux slices (auth, cart, etc.)
    │   ├── pages/              # Page components
    │   ├── components/         # Reusable UI components
    │   ├── services/           # Axios API service
    │   ├── routes/             # App routing
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- pip

---

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd beauty_shop_backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables (see .env section below)

# 4. Seed the database with sample data
python seed.py

# 5. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd FrontEnd

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev
```

The app will be available at `http://localhost:5173`

> Make sure the backend is running before starting the frontend.

---

## Environment Variables

Create a `.env` file inside `beauty_shop_backend/` with the following:

```env
# Database
DATABASE_URL=sqlite:///./beauty_shop.db

# JWT Auth
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# M-Pesa (Safaricom Daraja API)
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey

# Email (SMTP)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

---

## API Endpoints

### Authentication — `/api/auth`
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register a new user | No |
| POST | `/login` | Login and get JWT token | No |
| GET | `/me` | Get current user profile | Yes |
| PUT | `/me` | Update user profile | Yes |

### Products — `/api/products`
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List all products (supports `?category_id=` & `?search=`) | No |
| GET | `/{id}` | Get a single product | No |
| POST | `/` | Create a product | No |
| PUT | `/{id}` | Update a product | No |
| DELETE | `/{id}` | Delete a product | No |

### Cart — `/api/cart`
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | View cart items | Yes |
| POST | `/` | Add item to cart | Yes |
| PUT | `/{item_id}` | Update item quantity | Yes |
| DELETE | `/{item_id}` | Remove item from cart | Yes |
| DELETE | `/` | Clear entire cart | Yes |

### Orders — `/api/orders`
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Place a new order | Yes |
| GET | `/` | Get current user's orders | Yes |
| GET | `/all` | Get all orders (admin) | No |
| GET | `/{order_id}` | Get order by ID | No |
| PUT | `/{order_id}/status` | Update order status | No |
| POST | `/checkout` | M-Pesa checkout | Yes |
| POST | `/mpesa-callback` | M-Pesa payment callback | No |

---

## Database Models

| Model | Description |
|-------|-------------|
| `User` | Registered users with profile info and admin flag |
| `Category` | Product categories (Skincare, Haircare, Makeup) |
| `Product` | Products with price, stock, image, and rating |
| `CartItem` | Items in a user's cart |
| `Order` | Placed orders with invoice, status, and customer info |
| `Review` | Product reviews with rating and comment |
| `SupportMessage` | Customer support messages |

---

## Seeding the Database

The seed script adds sample categories and products:

```bash
cd beauty_shop_backend
python seed.py
```

This will add:
- **Categories:** Skincare, Haircare
- **Products:** Face Serum, Moisturizer, Shampoo

You can extend `seed.py` to add more products as needed.
