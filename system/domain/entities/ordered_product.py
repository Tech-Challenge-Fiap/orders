from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class OrderedProductEntity(BaseModel):
    type: str
    name: str
    price: Decimal
    description: str
    quantity: int
    observation: Optional[str]

    class Config:
        from_attributes = True
