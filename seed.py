import psycopg2
import time
from datetime import datetime

# Database configuration
DB_NAME = "beauty_shop"
DB_USER = "tommy"
DB_PASSWORD = "Group8"
DB_HOST = "localhost"
DB_PORT = "5432"

# 1. The "Database" (In-Memory Lists)
products = [
    {
        "id": 1,
        "name": "Radiance Vitamin C Serum",
        "category": "Skincare",
        "price": 48.00,
        "rating": 4.8,
        "reviews": 120,
        "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=600",
        "description": "A powerful serum that brightens skin tone and reduces signs of aging.",
        "stock": 50,
        "is_new": True,
        "reviews_list": [
            {"id": 101, "user": "Sarah J.", "rating": 5, "comment": "Absolutely love this! My skin glows.", "date": "2023-10-15"},
            {"id": 102, "user": "Mike T.", "rating": 4, "comment": "Good texture, but smells a bit strong.", "date": "2023-09-22"}
        ]
    },
    {
        "id": 2,
        "name": "Hydra-Boost Moisturizer",
        "category": "Skincare",
        "price": 56.00,
        "rating": 4.5,
        "reviews": 85,
        "image": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&q=80&w=600",
        "description": "Deep hydration for dry and sensitive skin.",
        "stock": 30,
        "is_new": False,
        "reviews_list": [
            {"id": 201, "user": "Emily R.", "rating": 5, "comment": "Saved my dry skin in winter!", "date": "2023-11-05"}
        ]
    },
    {
        "id": 3,
        "name": "Velvet Matte Lipstick",
        "category": "Makeup",
        "price": 32.00,
        "rating": 4.9,
        "reviews": 210,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&q=80&w=600",
        "description": "Long-lasting matte finish that doesn't dry out lips.",
        "stock": 100,
        "is_new": True,
        "reviews_list": []
    },
    {
        "id": 4,
        "name": "Argan Repair Hair Oil",
        "category": "Haircare",
        "price": 36.00,
        "rating": 4.2,
        "reviews": 45,
        "image": "https://images.unsplash.com/photo-1608248597279-f99d160bfbc8?auto=format&fit=crop&q=80&w=600",
        "description": "Restores shine and softness to damaged hair.",
        "stock": 25,
        "is_new": False,
        "reviews_list": []
    },
    {
        "id": 5,
        "name": "Sunshield SPF 50 Sunscreen",
        "category": "Skincare",
        "price": 29.00,
        "rating": 4.7,
        "reviews": 95,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=600",
        "description": "Broad-spectrum sunscreen that protects against UVA and UVB rays.",
        "stock": 60,
        "is_new": True,
        "reviews_list": [
            {"id": 501, "user": "Liam K.", "rating": 5, "comment": "Lightweight and non-greasy. Perfect for daily use.", "date": "2023-08-30"}
        ]
    },
    {
        "id": 6,
        "name": "Volume Boost Shampoo",
        "category": "Haircare",
        "price": 24.00,
        "rating": 4.3,
        "reviews": 65,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&q=80&w=600",
        "description": "Enhances volume and adds body to fine hair.",
        "stock": 40,
        "is_new": False,
        "reviews_list": [
            {"id": 601, "user": "Sophie M.", "rating": 4, "comment": "Great for adding volume. My hair feels fuller now.", "date": "2023-10-12"}
        ]
    }
]

categories = [
    {
        "id": 1,
        "title": "Skincare",
        "subtitle": "Nourish & Glow",
        "image": "https://images.unsplash.com/photo-1596462502278-27bfdd403cc2?auto=format&fit=crop&q=80&w=600"
    },
    {
        "id": 2,
        "title": "Haircare",
        "subtitle": "Strength & Shine",
        "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&q=80&w=600"
    },
    {
        "id": 3,
        "title": "Makeup",
        "subtitle": "Define & Enhance",
        "image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?auto=format&fit=crop&q=80&w=600"
    }
]

# This list acts as our "Database" for orders
orders_db = []

def get_product_by_id(id):
    """Get single product by ID"""
    return next((p for p in products if p["id"] == int(id)), None)

def create_order(order_data):
    """Simulate creating an order (Async)"""
    time.sleep(1.5)  # 1.5 second delay to simulate network
    
    new_order = {
        **order_data,
        "id": f"ORD-{int(time.time())}",  # Generate unique ID based on timestamp
        "created_at": datetime.now().isoformat(),
        "status": "Processing"
    }
    orders_db.append(new_order)  # Save to "DB"
    return new_order

def get_order_by_id(order_id):
    """Simulate fetching an order by ID"""
    return next((o for o in orders_db if o["id"] == order_id), None)

def create_tables(conn):
    """Create database tables"""
    cursor = conn.cursor()
    
    # Drop existing tables with CASCADE to remove all dependencies
    cursor.execute("DROP TABLE IF EXISTS orders CASCADE")
    cursor.execute("DROP TABLE IF EXISTS reviews CASCADE")
    cursor.execute("DROP TABLE IF EXISTS products CASCADE")
    cursor.execute("DROP TABLE IF EXISTS categories CASCADE")
    
    # Create categories table
    cursor.execute("""
    CREATE TABLE categories (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        subtitle VARCHAR(100),
        image VARCHAR(255)
    )
    """)
    
    # Create products table
    cursor.execute("""
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        category_id INTEGER REFERENCES categories(id),
        price DECIMAL(10,2) NOT NULL,
        rating DECIMAL(3,1),
        reviews INTEGER,
        image VARCHAR(255),
        description TEXT,
        stock INTEGER,
        is_new BOOLEAN
    )
    """)
    
    # Create reviews table
    cursor.execute("""
    CREATE TABLE reviews (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id),
        username VARCHAR(100),
        rating INTEGER,
        comment TEXT,
        date DATE
    )
    """)
    
    # Create orders table
    cursor.execute("""
    CREATE TABLE orders (
        id VARCHAR(50) PRIMARY KEY,
        created_at TIMESTAMP,
        status VARCHAR(50)
    )
    """)
    
    conn.commit()

def seed_categories(conn):
    """Seed categories table"""
    cursor = conn.cursor()
    
    for category in categories:
        cursor.execute("""
        INSERT INTO categories (id, title, subtitle, image)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """, (category["id"], category["title"], category["subtitle"], category["image"]))
    
    conn.commit()

def seed_products(conn):
    """Seed products and reviews tables"""
    cursor = conn.cursor()
    
    # Create a mapping of category titles to IDs
    cursor.execute("SELECT id, title FROM categories")
    category_mapping = {row[1]: row[0] for row in cursor.fetchall()}
    
    for product in products:
        # Get category ID from mapping
        category_id = category_mapping.get(product["category"])
        
        # Insert product
        cursor.execute("""
        INSERT INTO products (
            id, name, category_id, price, rating, reviews, image, 
            description, stock, is_new
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """, (
            product["id"], product["name"], category_id,
            product["price"], product["rating"], product["reviews"],
            product["image"], product["description"], product["stock"],
            product["is_new"]
        ))
        
        # Insert reviews
        for review in product["reviews_list"]:
            cursor.execute("""
            INSERT INTO reviews (
                id, product_id, username, rating, comment, date
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, (
                review["id"], product["id"], review["user"],
                review["rating"], review["comment"], review["date"]
            ))
    
    conn.commit()

def seed_orders(conn):
    """Seed orders table"""
    cursor = conn.cursor()
    
    for order in orders_db:
        cursor.execute("""
        INSERT INTO orders (id, created_at, status)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """, (
            order["id"], 
            datetime.fromisoformat(order["created_at"]), 
            order["status"]
        ))
    
    conn.commit()

def main():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    try:
        print("Creating tables...")
        create_tables(conn)
        
        print("Seeding categories...")
        seed_categories(conn)
        
        print("Seeding products and reviews...")
        seed_products(conn)
        
        print("Seeding orders...")
        seed_orders(conn)
        
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()