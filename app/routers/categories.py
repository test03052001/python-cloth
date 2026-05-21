from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.logging_config import get_logger
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])
logger = get_logger()


@router.get("", response_model=list[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    logger.info("Listing categories skip=%s limit=%s", skip, limit)
    return db.query(Category).offset(skip).limit(limit).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()

    if payload.name is not None:
        existing = db.query(Category).filter(
            (Category.name == payload.name) | (Category.slug == payload.slug)
        ).first()
    else:
        existing = db.query(Category).filter(Category.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name or slug already exists",
        )
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    logger.info("Created category id=%s name=%s", category.id, category.name)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)
):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    logger.info("Updated category id=%s", category_id)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(category)
    db.commit()
    logger.info("Deleted category id=%s", category_id)
