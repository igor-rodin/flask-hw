from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from settings import settings


class ProductIn(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=settings.NAME_MAX_LENGTH)
    description: Optional[str] = Field(
        default=None, min_length=2, max_length=settings.NAME_MAX_LENGTH
    )
    price: Decimal


class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=settings.NAME_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        default=None, min_length=2, max_length=settings.NAME_MAX_LENGTH
    )
    price: Optional[Decimal] = Field(default=None)


class Product(ProductUpdate):
    id: int
