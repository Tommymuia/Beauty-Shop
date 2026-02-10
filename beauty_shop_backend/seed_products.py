import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Product, Category, Base

def seed_products():
    db = SessionLocal()
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Create categories
        categories_data = ['Skincare', 'Haircare', 'Makeup']
        categories = {}
        
        for cat_name in categories_data:
            cat_obj = db.query(Category).filter(Category.name == cat_name).first()
            if not cat_obj:
                cat_obj = Category(name=cat_name)
                db.add(cat_obj)
        
        db.commit()
        
        # Refresh categories dict
        for cat_name in categories_data:
            categories[cat_name] = db.query(Category).filter(Category.name == cat_name).first()
        
        # Skincare products
        skincare_products = [
            ("Hydrating Facial Cleanser", "Gentle cleanser for all skin types", 2600, 4.5),
            ("Vitamin C Serum", "Brightening serum with antioxidants", 4500, 4.7),
            ("Retinol Night Cream", "Anti-aging night treatment", 5200, 4.6),
            ("Hyaluronic Acid Moisturizer", "Deep hydration for dry skin", 3900, 4.8),
            ("Niacinamide Toner", "Pore-refining toner", 2800, 4.4),
            ("Clay Face Mask", "Detoxifying mask for oily skin", 3200, 4.3),
            ("Eye Cream", "Reduces dark circles and puffiness", 4200, 4.5),
            ("Sunscreen SPF 50", "Broad spectrum UV protection", 3500, 4.9),
            ("Glycolic Acid Exfoliant", "Chemical exfoliant for smooth skin", 3800, 4.6),
            ("Rose Water Mist", "Refreshing facial spray", 2200, 4.2),
            ("Collagen Boosting Serum", "Firms and plumps skin", 5500, 4.7),
            ("Acne Treatment Gel", "Spot treatment for blemishes", 2900, 4.4),
            ("Peptide Face Cream", "Anti-wrinkle moisturizer", 6200, 4.8),
            ("Micellar Water", "Gentle makeup remover", 2400, 4.5),
            ("Aloe Vera Gel", "Soothing and healing gel", 1800, 4.6),
            ("Charcoal Peel-Off Mask", "Deep pore cleansing", 3100, 4.3),
            ("Snail Mucin Essence", "Hydrating and repairing", 4800, 4.7),
            ("Tea Tree Oil Serum", "Antibacterial treatment", 3300, 4.4),
            ("Ceramide Barrier Cream", "Strengthens skin barrier", 4900, 4.8),
            ("Lactic Acid Peel", "Gentle exfoliating treatment", 3600, 4.5),
            ("Vitamin E Oil", "Nourishing facial oil", 2700, 4.3),
            ("Green Tea Face Wash", "Antioxidant cleanser", 2500, 4.4),
            ("Bakuchiol Serum", "Natural retinol alternative", 5100, 4.6),
            ("Centella Asiatica Cream", "Calming moisturizer", 3700, 4.7),
            ("Salicylic Acid Cleanser", "Acne-fighting face wash", 2900, 4.5),
            ("Squalane Oil", "Lightweight facial oil", 4300, 4.8),
            ("Azelaic Acid Serum", "Brightening treatment", 4100, 4.6),
            ("Cucumber Eye Patches", "Cooling under-eye treatment", 2600, 4.2),
            ("Propolis Ampoule", "Healing and soothing serum", 4700, 4.7),
            ("Mandelic Acid Toner", "Gentle exfoliating toner", 3200, 4.4)
        ]
        
        # Haircare products
        haircare_products = [
            ("Argan Oil Shampoo", "Nourishing shampoo for dry hair", 3200, 4.5),
            ("Keratin Hair Mask", "Deep conditioning treatment", 4500, 4.7),
            ("Biotin Hair Growth Serum", "Promotes hair growth", 5200, 4.6),
            ("Coconut Oil Conditioner", "Moisturizing conditioner", 3100, 4.4),
            ("Purple Shampoo", "Tones blonde and gray hair", 3400, 4.5),
            ("Hair Repair Oil", "Split end treatment", 3800, 4.6),
            ("Volumizing Mousse", "Adds body and volume", 2900, 4.3),
            ("Anti-Frizz Serum", "Smooths and controls frizz", 3600, 4.7),
            ("Scalp Scrub", "Exfoliates and cleanses scalp", 3300, 4.4),
            ("Heat Protectant Spray", "Shields from styling damage", 2800, 4.5),
            ("Castor Oil Hair Treatment", "Strengthens and thickens", 2600, 4.6),
            ("Dry Shampoo", "Refreshes hair between washes", 2400, 4.3),
            ("Leave-In Conditioner", "Detangles and moisturizes", 3200, 4.5),
            ("Hair Growth Vitamins", "Supplements for healthy hair", 4200, 4.4),
            ("Rosemary Mint Shampoo", "Stimulating scalp treatment", 3100, 4.6),
            ("Silk Hair Wrap", "Protects hair while sleeping", 1900, 4.2),
            ("Protein Hair Treatment", "Strengthens damaged hair", 4800, 4.7),
            ("Tea Tree Scalp Oil", "Treats dandruff and itchiness", 3400, 4.5),
            ("Curl Defining Cream", "Enhances natural curls", 3700, 4.6),
            ("Hair Detox Mask", "Removes buildup and impurities", 4100, 4.4),
            ("Bamboo Extract Shampoo", "Strengthens and repairs", 3300, 4.5),
            ("Jojoba Oil Treatment", "Nourishes scalp and hair", 2900, 4.6),
            ("Color Protect Shampoo", "Preserves hair color", 3500, 4.7),
            ("Aloe Vera Hair Gel", "Natural styling gel", 2200, 4.3),
            ("Peppermint Scalp Tonic", "Refreshing scalp treatment", 2700, 4.4),
            ("Quinoa Protein Spray", "Strengthening leave-in", 3600, 4.5),
            ("Avocado Hair Butter", "Deep moisture treatment", 4400, 4.8),
            ("Rice Water Rinse", "Traditional hair strengthener", 2500, 4.6),
            ("Ginseng Hair Tonic", "Energizes hair follicles", 4900, 4.7),
            ("Shea Butter Hair Cream", "Moisturizes and defines", 3800, 4.5)
        ]
        
        # Makeup products
        makeup_products = [
            ("Matte Foundation", "Full coverage foundation", 4200, 4.6),
            ("Liquid Concealer", "High coverage concealer", 3100, 4.5),
            ("Setting Powder", "Translucent finishing powder", 2900, 4.4),
            ("Eyeshadow Palette", "12-color neutral palette", 5200, 4.8),
            ("Waterproof Mascara", "Lengthening and volumizing", 2600, 4.5),
            ("Liquid Eyeliner", "Precision tip liner", 2200, 4.4),
            ("Brow Pencil", "Natural-looking brow definer", 1900, 4.3),
            ("Blush Palette", "4-color blush collection", 3400, 4.6),
            ("Highlighter Stick", "Creamy illuminator", 2800, 4.7),
            ("Contour Kit", "Sculpting powder set", 3900, 4.5),
            ("Lip Gloss Set", "6 glossy shades", 2400, 4.3),
            ("Matte Lipstick", "Long-lasting lip color", 2100, 4.6),
            ("Makeup Primer", "Smoothing base", 3200, 4.5),
            ("Setting Spray", "Long-wear makeup setter", 2700, 4.7),
            ("BB Cream", "Tinted moisturizer with SPF", 3300, 4.4),
            ("Bronzer Powder", "Sun-kissed glow", 3100, 4.5),
            ("False Lashes", "Dramatic volume lashes", 1600, 4.2),
            ("Makeup Sponge Set", "Blending sponges 5-pack", 1400, 4.6),
            ("Brush Set", "12-piece professional set", 5800, 4.8),
            ("Eyebrow Gel", "Tinted brow setter", 2000, 4.4),
            ("Lip Liner Set", "6 essential shades", 2300, 4.3),
            ("Cream Eyeshadow", "Long-lasting cream shadow", 2500, 4.5),
            ("Makeup Remover Wipes", "Gentle cleansing wipes", 1800, 4.4),
            ("Face Primer Serum", "Hydrating primer", 3600, 4.6),
            ("Lip Tint", "Natural flush of color", 2200, 4.5),
            ("Glitter Gel", "Sparkle for eyes and face", 2400, 4.3),
            ("Cushion Foundation", "Dewy finish compact", 4500, 4.7),
            ("Lip Plumper", "Volumizing lip treatment", 2900, 4.4),
            ("Color Corrector", "Multi-tone correcting palette", 3200, 4.5),
            ("Makeup Fixing Mist", "Hydrating setting spray", 2800, 4.6)
        ]
        
        # Add products to database
        for name, desc, price, rating in skincare_products:
            product = Product(
                name=name,
                description=desc,
                price=price,
                category_id=categories['Skincare'].id,
                stock_quantity=50,
                rating=rating,
                is_new=False,
                image="https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400"
            )
            db.add(product)
        
        for name, desc, price, rating in haircare_products:
            product = Product(
                name=name,
                description=desc,
                price=price,
                category_id=categories['Haircare'].id,
                stock_quantity=50,
                rating=rating,
                is_new=False,
                image="https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400"
            )
            db.add(product)
        
        for name, desc, price, rating in makeup_products:
            product = Product(
                name=name,
                description=desc,
                price=price,
                category_id=categories['Makeup'].id,
                stock_quantity=50,
                rating=rating,
                is_new=False,
                image="https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400"
            )
            db.add(product)
        
        db.commit()
        print(f"✅ Successfully added 90 products (30 per category)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
