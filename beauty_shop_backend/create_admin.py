from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User
import os

# Use DATABASE_URL from environment when available
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://beauty_admin:Group8@localhost:5432/beauty_shop_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    admin = db.query(User).filter(User.email == "admin@gmail.com").first()
    
    if admin:
        admin.password = generate_password_hash("admin123", method='pbkdf2:sha256')
        admin.is_admin = True
        db.commit()
        print("✓ Updated admin user password")
    else:
        admin = User(
            email="admin@gmail.com",
            password=generate_password_hash("admin123", method='pbkdf2:sha256'),
            phone_number="0712345678",
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("✓ Created admin user")
    
    print(f"  Email: admin@gmail.com")
    print(f"  Password: admin123")
    print(f"  Is Admin: {admin.is_admin}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    db.rollback()
finally:
    db.close()
