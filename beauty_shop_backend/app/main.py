from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, products, orders, cart, users, reviews, support
from app.database import engine
from app.models import Base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project 8: Beauty Shop API")

# CORS Configuration - Must be before routes
# Note: allow_credentials=True cannot be used with allow_origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://beauty-shop-murex.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# These assume that in your routes/__init__.py, you have:
# from .orders import router as orders
app.include_router(auth, prefix="/api/auth", tags=["Authentication"])
app.include_router(products, prefix="/api/products", tags=["Products"])
app.include_router(orders, prefix="/api/orders", tags=["Orders"])
app.include_router(cart, prefix="/api/cart", tags=["Cart"])
app.include_router(users, prefix="/api/users", tags=["Users"])
app.include_router(reviews, prefix="/api/reviews", tags=["Reviews"])
app.include_router(support, prefix="/api/support", tags=["Support"])

@app.get("/")
async def root():
    return {"message": "Beauty Shop Backend is Active"}