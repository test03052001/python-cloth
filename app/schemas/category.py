from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    slug: str = Field(..., min_length=1, max_length=120)
    description: str | None = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    # DB requires a non-null name, so create payload must provide one.
    name: str = Field(..., min_length=1, max_length=100)


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    slug: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None
    is_active: bool | None = None


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    name: str
    id: int
    created_at: datetime
    updated_at: datetime
