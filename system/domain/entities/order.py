from decimal import Decimal
from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional
from system.domain.entities.ordered_product import OrderedProductEntity
from system.domain.enums.enums import OrderStatusEnum


class OrderEntity(BaseModel):
    order_id: Optional[int] = None
    created_at: datetime = datetime.now()
    price: Optional[Decimal] = None
    products: Optional[List[OrderedProductEntity]]
    status: OrderStatusEnum = OrderStatusEnum.TO_BE_PAYED
    waiting_time: Optional[int] = None
    client_id: Optional[str] = None
    payment_id: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True

    @validator("products", pre=True, always=True)
    def validate_exclusive_fields(cls, value, values):
        products_ids = values.get("products_ids")
        if value is None and products_ids is None:
            raise ValueError("Deve ser fornecido products_ids ou products")
        return value
