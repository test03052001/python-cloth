from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    phone: str | None = Field(None, max_length=20)
    address: str | None = Field(None, max_length=500)
    city: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
