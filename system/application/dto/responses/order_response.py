from datetime import datetime
from typing import List, Optional
from flask import Response
from system.domain.entities.ordered_product import OrderedProductEntity

from system.domain.enums.enums import OrderStatusEnum


class OrderResponse(Response):
    order_id: int
    order_date: datetime
    products: List[OrderedProductEntity]
    status: OrderStatusEnum
    waiting_time: int
    client_id: Optional[str]

    class Config:
        from_attributes = True
        use_enum_values = True


class CreateOrderResponse(OrderResponse):
    pass


class GetOrderByIDResponse(OrderResponse):
    pass


class GetAllOrdersResponse(OrderResponse):
    orders: List[OrderResponse]


class UpdateOrderResponse(OrderResponse):
    pass
