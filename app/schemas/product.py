from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    category_id: int
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=220)
    description: str | None = None
    sku: str = Field(..., min_length=1, max_length=50)
    price: Decimal = Field(..., gt=0)
    discount_price: Decimal | None = Field(None, gt=0)
    stock_quantity: int = Field(0, ge=0)
    size: str | None = Field(None, max_length=20)
    color: str | None = Field(None, max_length=50)
    brand: str | None = Field(None, max_length=100)
    image_url: str | None = Field(None, max_length=500)
    is_featured: bool = False
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(None, min_length=1, max_length=200)
    slug: str | None = Field(None, min_length=1, max_length=220)
    description: str | None = None
    sku: str | None = Field(None, min_length=1, max_length=50)
    price: Decimal | None = Field(None, gt=0)
    discount_price: Decimal | None = Field(None, gt=0)
    stock_quantity: int | None = Field(None, ge=0)
    size: str | None = None
    color: str | None = None
    brand: str | None = None
    image_url: str | None = None
    is_featured: bool | None = None
    is_active: bool | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
