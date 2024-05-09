from typing import List, Optional
from pydantic import BaseModel

from system.domain.enums.enums import OrderStatusEnum


class OrderedProduct(BaseModel):
    type: str
    name: str
    price: str
    description: str
    waiting_time: int
    quantity: int
    observation: str


class CreateOrderRequest(BaseModel):
    products: List[OrderedProduct]
    client_id: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatusEnum

    class Config:
        from_attributes = True
