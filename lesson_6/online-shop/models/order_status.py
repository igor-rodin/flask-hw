from pydantic import BaseModel, Field
from settings import settings


class OrderStatusIn(BaseModel):
    status_name: str = Field(..., min_length=2, max_length=settings.NAME_MAX_LENGTH)


class OrderStatus(OrderStatusIn):
    id: int
