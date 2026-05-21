from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.logging_config import get_logger
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])
logger = get_logger()


@router.get("", response_model=list[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 50,
    category_id: int | None = None,
    featured_only: bool = Query(False),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
):
    logger.info("Listing products category_id=%s", category_id)
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if featured_only:
        query = query.filter(Product.is_featured.is_(True))
    if active_only:
        query = query.filter(Product.is_active.is_(True))
    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    if not db.get(Category, payload.category_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")
    if db.query(Product).filter(
        (Product.sku == payload.sku) | (Product.slug == payload.slug)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU or slug already exists",
        )
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info("Created product id=%s sku=%s", product.id, product.sku)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    data = payload.model_dump(exclude_unset=True)
    if "category_id" in data and not db.get(Category, data["category_id"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")
    for field, value in data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    logger.info("Updated product id=%s", product_id)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    logger.info("Deleted product id=%s", product_id)
