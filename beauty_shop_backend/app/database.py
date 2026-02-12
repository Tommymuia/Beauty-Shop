import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

# 1. Get the URL from Render's environment variables. 
# 2. If it's not there, fall back to your local localhost string.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://beauty_admin:Group8@localhost/beauty_shop_db"
)

# Render fix: SQLAlchemy 2.0 requires "postgresql://" instead of "postgres://"
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the engine using the dynamic URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency used in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()