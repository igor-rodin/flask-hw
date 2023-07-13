from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from settings import settings
from models.users import User
from models.products import Product
from models.order_status import OrderStatus


class OrderIn(BaseModel):
    order_status: int = Field(default=1)
    user_id: int
    product_id: int
    order_date: datetime = Field(default_factory=datetime.utcnow)
    products_amount: int


class OrderUpdate(BaseModel):
    order_status: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)
    product_id: Optional[int] = Field(default=None)
    order_date: Optional[datetime] = Field(default=None)
    products_amount: Optional[int] = Field(default=None)


class OrderOut(BaseModel):
    id: int
    product: Product
    products_amount: int
    order_date: datetime
    status: OrderStatus


class Order(OrderOut):
    user: User
