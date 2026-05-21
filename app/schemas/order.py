from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate] = Field(..., min_length=1)
    shipping_address: str | None = Field(None, max_length=500)
    notes: str | None = Field(None, max_length=500)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    order_number: str
    status: str
    total_amount: Decimal
    shipping_address: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]
