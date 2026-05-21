"""Seed sample categories and products. Run after DB is created: python scripts/seed_data.py"""

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal, init_db
from app.logging_config import setup_logging
from app.models.category import Category
from app.models.product import Product

setup_logging()
init_db()

SAMPLE_DATA = [
    {
        "category": {"name": "Men", "slug": "men", "description": "Men's clothing"},
        "products": [
            {
                "name": "Classic Cotton T-Shirt",
                "slug": "men-cotton-tshirt",
                "sku": "MEN-TS-001",
                "price": Decimal("29.99"),
                "discount_price": Decimal("24.99"),
                "stock_quantity": 100,
                "size": "L",
                "color": "Navy",
                "brand": "UrbanWear",
                "is_featured": True,
            },
            {
                "name": "Slim Fit Denim Jeans",
                "slug": "men-slim-jeans",
                "sku": "MEN-JN-002",
                "price": Decimal("59.99"),
                "stock_quantity": 50,
                "size": "32",
                "color": "Blue",
                "brand": "DenimCo",
            },
        ],
    },
    {
        "category": {"name": "Women", "slug": "women", "description": "Women's clothing"},
        "products": [
            {
                "name": "Floral Summer Dress",
                "slug": "women-floral-dress",
                "sku": "WOM-DR-001",
                "price": Decimal("79.99"),
                "discount_price": Decimal("64.99"),
                "stock_quantity": 40,
                "size": "M",
                "color": "Floral",
                "brand": "BloomStyle",
                "is_featured": True,
            },
        ],
    },
    {
        "category": {"name": "Kids", "slug": "kids", "description": "Children's clothing"},
        "products": [
            {
                "name": "Kids Hoodie",
                "slug": "kids-hoodie",
                "sku": "KID-HD-001",
                "price": Decimal("34.99"),
                "stock_quantity": 60,
                "size": "S",
                "color": "Red",
                "brand": "LittleStars",
            },
        ],
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Category).count() > 0:
            print("Database already has data. Skipping seed.")
            return
        for group in SAMPLE_DATA:
            category = Category(**group["category"])
            db.add(category)
            db.flush()
            for prod in group["products"]:
                db.add(Product(category_id=category.id, **prod))
        db.commit()
        print("Sample data seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
