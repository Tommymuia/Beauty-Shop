"""Create test user in Render database"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
from app.routes.auth import hash_password

db = SessionLocal()

try:
    # Check if test user exists
    test_user = db.query(User).filter(User.email == "test@test.com").first()
    
    if test_user:
        print("✅ Test user already exists: test@test.com")
    else:
        # Create test user
        new_user = User(
            email="test@test.com",
            password=hash_password("password123")
        )
        db.add(new_user)
        db.commit()
        print("✅ Test user created!")
        print("   Email: test@test.com")
        print("   Password: password123")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
