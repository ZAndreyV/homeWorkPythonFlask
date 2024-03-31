from datetime import datetime
from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    user_id: int
    goods_id: int
    date: datetime
    status: str = Field(max_length=32)


class Order(OrderIn):
    id: int
