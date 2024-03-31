from typing import Optional
from pydantic import BaseModel


class Goods(BaseModel):
    id: int
    name_of_goods: str
    description: Optional[str]
    price: float


class GoodsIn(BaseModel):
    name_of_goods: str
    description: Optional[str]
    price: float
