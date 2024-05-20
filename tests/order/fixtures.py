import datetime
from decimal import Decimal
from typing import Any, List
from unittest.mock import patch

import pytest

from system.application.dto.requests.order_request import (
    CreateOrderRequest,
    UpdateOrderStatusRequest,
)
from system.application.dto.responses.order_response import (
    GetOrderByIDResponse,
    OrderResponse,
    CreateOrderResponse,
    GetAllOrdersResponse,
    UpdateOrderResponse,
)
from system.domain.entities.order import OrderEntity
from system.domain.entities.ordered_product import OrderedProductEntity
from system.domain.enums.enums import OrderStatusEnum


def create_order() -> OrderEntity:
    return OrderEntity(
        order_id=None,
        order_date=datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
        price=Decimal("20"),
        products_ids=[1],
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SIDE",
                description="Fritas",
            ),
        ],
        status=OrderStatusEnum.TO_BE_PAYED,
        waiting_time=6,
        client_id="64597789065",
        payment_id=1,
    )


@pytest.fixture
def mock_order_repository():
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository",
        autospec=True,
    ) as mock_repo:
        yield mock_repo


@pytest.fixture
def mock_order() -> OrderEntity:
    return create_order()


@pytest.fixture
def mock_create_order() -> OrderEntity:
    return OrderEntity(
        order_id=1,
        order_date=datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SIDE",
                description="Fritas",
            ),
        ],
        status="WAITING PAYMENT",
        waiting_time=6,
        client_id="64597789065",
        payment_id=1,
    )


@pytest.fixture
def mock_create_order_repository_response() -> Any:
    return {
        "client_id": "45789632145",
        "order_date": datetime.datetime(2024, 1, 20, 0, 0, 0),
        "order_id": 1,
        "payment_id": 1,
        "price": Decimal("80"),
        "products": [
            {
                "name": "Batata Frita Grande",
                "price": Decimal("20"),
                "product_id": 1,
                "quantity": 1,
                "type": "SNACK",
            }
        ],
        "status": OrderStatusEnum.PREPARING,
        "waiting_time": 90,
    }


@pytest.fixture
def mock_create_order_request() -> CreateOrderRequest:
    return CreateOrderRequest(products=[1], client_id="45789632145")


@pytest.fixture
def mock_create_order_response() -> CreateOrderResponse:
    return CreateOrderResponse(
        order_id=1,
        order_date=datetime.datetime(2024, 1, 20, 0, 0, 0),
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SNACK",
                description="Fritas",
            )
        ],
        status=OrderStatusEnum.PREPARING,
        waiting_time=6,
        client_id="45789632145",
        payment_id=1,
    )


@pytest.fixture
def mock_get_orders_response() -> GetAllOrdersResponse:
    """
    Mock that creates a GetAllOrdersResponse with correct type annotations and attributes.
    """
    order_list: List[OrderResponse] = [
        OrderResponse(
            order_id=1,
            order_date=datetime.datetime(2024, 1, 20, 0, 0, 0),
            products=[
                OrderedProductEntity(
                    name="Batata Frita Grande",
                    price=Decimal("20"),
                    product_id=1,
                    quantity=1,
                    type="SNACK",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=6,
            client_id="45789632145",
            payment_id=1,
        ),
        OrderResponse(
            order_id=2,
            order_date=datetime.datetime.now(),
            products=[
                OrderedProductEntity(
                    name="Cheeseburger com bacon",
                    price=Decimal("34"),
                    product_id=2,
                    quantity=1,
                    type="SNACK",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=10,
            client_id="12345678889",
            payment_id=2,
        ),
    ]
    return GetAllOrdersResponse(orders=order_list)


@pytest.fixture
def mock_get_orders_usecase_response() -> List[OrderEntity]:
    """
    Mock that creates a List of OrderEntity for use case testing.
    """
    return [
        OrderEntity(
            order_id=1,
            order_date=datetime.datetime.now(),
            price=Decimal("20"),
            products=[
                OrderedProductEntity(
                    name="Batata Frita Grande",
                    price=Decimal("20"),
                    product_id=1,
                    quantity=1,
                    type="SIDE",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=6,
            client_id="example_client_id",
            payment_id = 1,
        ),
        OrderEntity(
            order_id=2,
            order_date=datetime.datetime.now(),
            price=Decimal("34"),
            products=[
                OrderedProductEntity(
                    name="Cheeseburger com bacon",
                    price=Decimal("34"),
                    product_id=2,
                    quantity=1,
                    type="SNACK",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=10,
            client_id="example_client_id",
            payment_id = 1,
        ),
    ]


@pytest.fixture
def mock_get_orders_by_type_repository_response() -> List[OrderEntity]:
    """
    Mock that creates a List of OrderEntity based on a specific type.
    """
    return [
        OrderEntity(
            order_id=1,
            order_date=datetime.datetime.now(),
            price=Decimal("20"),
            products=[
                OrderedProductEntity(
                    name="Batata Frita Grande",
                    price=Decimal("20"),
                    product_id=1,
                    quantity=1,
                    type="SIDE",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=6,
            client_id="example_client_id",
            payment_id = 1,
        )
    ]


@pytest.fixture
def mock_get_orders_by_type_response() -> GetAllOrdersResponse:
    """
    Mock that creates a GetAllOrdersResponse containing Orders of a specific type.
    """
    order_list = mock_get_orders_by_type_repository_response()
    return GetAllOrdersResponse(orders=order_list)


@pytest.fixture
def order_repository_response() -> OrderEntity:
    """
    Mock that creates an OrderEntity for repository testing.
    """
    return OrderEntity(
        order_id=1,
        order_date=datetime.datetime.now(),
        price=Decimal("20"),
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SIDE",
                description="Fritas",
            )
        ],
        status=OrderStatusEnum.PREPARING,
        waiting_time=6,
        client_id="example_client_id",
        payment_id = 1,
    )


@pytest.fixture
def mock_get_orders_repository_response() -> List[OrderEntity]:
    """
    Mock that creates a List of OrderEntity representing multiple orders.
    """
    return [
        OrderEntity(
            order_id=1,
            order_date=datetime.datetime.now(),
            price=Decimal("20"),
            products=[
                OrderedProductEntity(
                    name="Batata Frita Grande",
                    price=Decimal("20"),
                    product_id=1,
                    quantity=1,
                    type="SIDE",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=6,
            client_id="example_client_id",
            payment_id = 1,
        ),
        OrderEntity(
            order_id=2,
            order_date=datetime.datetime.now(),
            price=Decimal("34"),
            products=[
                OrderedProductEntity(
                    name="Cheeseburger com bacon",
                    price=Decimal("34"),
                    product_id=2,
                    quantity=1,
                    type="SNACK",
                    description="Fritas",
                )
            ],
            status=OrderStatusEnum.PREPARING,
            waiting_time=10,
            client_id="example_client_id",
            payment_id = 1,
        ),
    ]


@pytest.fixture
def mock_update_order_request() -> UpdateOrderStatusRequest:
    """
    Mock that creates an UpdateOrderStatusRequest.
    """
    return UpdateOrderStatusRequest(status=OrderStatusEnum.RECIEVED)


@pytest.fixture
def mock_get_active_orders_usecase_response() -> GetAllOrdersResponse:
    """
    Mock that creates a List[OrderResponse]
    """
    orders = []
    # Create OrderResponse for each order and append to orders list
    for i in range(1, 3):
        orders.append(
            OrderResponse(
                order_id=i,
                order_date=datetime.datetime(
                    2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                ),
                products=[
                    OrderedProductEntity(
                        name="Batata Frita Grande",
                        price=Decimal("20"),
                        product_id=1,
                        quantity=1,
                        type="SIDE",
                        description="Fritas",
                    )
                ],
                status=OrderStatusEnum.TO_BE_PAYED.value,
                waiting_time=6,
                client_id="64597789065",
                payment_id=1,
            )
        )
    return GetAllOrdersResponse(orders=orders)


@pytest.fixture
def active_orders_data():
    return [
        {
            "client_id": "45789632145",
            "order_date": datetime.datetime(2024, 1, 20, 0, 0, 0),
            "order_id": 1,
            "payment_id": 1,  # Assuming this is the missing field
            "payment": {
                "id": 1,
                "qr_code": "00020101021243650016COM.MERCADOLIBRE02013063638f1192a-5fd1-4180-a180-8bcae3556bc35204000053039865802BR5925IZABEL AAAA DE MELO6007BARUERI62070503***63040B6D",
                "status": "UNPAID",
            },
            "price": Decimal("80"),
            "products": [
                {
                    "name": "Frango",
                    "price": Decimal("20"),
                    "product_id": 1,
                    "quantity": 1,
                    "type": "SNACK",
                },
                {
                    "name": "Hamburguer",
                    "price": Decimal("30"),
                    "product_id": 5,
                    "quantity": 2,
                    "type": "SNACK",
                },
            ],
            "status": "PREPARING",
            "waiting_time": 90,
        }
    ]


@pytest.fixture
def mock_get_all_orders_response(active_orders_data):
    orders = [
        OrderResponse(
            order_id=data["order_id"],
            order_date=data["order_date"],
            products=[OrderedProductEntity(**prod) for prod in data["products"]],
            status=data["status"],
            waiting_time=data["waiting_time"],
            client_id=data["client_id"],
            payment_id=data["payment_id"],
        )
        for data in active_orders_data
    ]
    return GetAllOrdersResponse(orders=orders)


@pytest.fixture
def update_order_data():
    return {"status": "READY"}


@pytest.fixture
def mock_update_order_response() -> CreateOrderResponse:
    return CreateOrderResponse(
        order_id=1,
        order_date=datetime.datetime(2024, 1, 20, 0, 0, 0),
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SNACK",
                description="Fritas",
            )
        ],
        status=OrderStatusEnum.PREPARING,
        waiting_time=6,
        client_id="45789632145",
        payment_id=1,
    )


@pytest.fixture
def mock_get_order_by_id_response() -> GetOrderByIDResponse:
    return GetOrderByIDResponse(
        order_id=1,
        order_date=datetime.datetime(2024, 1, 20, 0, 0, 0),
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SNACK",
                description="Fritas",
            )
        ],
        status=OrderStatusEnum.PREPARING,
        waiting_time=6,
        client_id="45789632145",
        payment_id=1,
    )


@pytest.fixture
def mock_update_order_response() -> UpdateOrderResponse:
    return UpdateOrderResponse(
        order_id=1,
        order_date=datetime.datetime(2024, 1, 20, 0, 0, 0),
        products=[
            OrderedProductEntity(
                name="Batata Frita Grande",
                price=Decimal("20"),
                product_id=1,
                quantity=1,
                type="SNACK",
                description="Fritas",
            )
        ],
        status=OrderStatusEnum.PREPARING,
        waiting_time=6,
        client_id="45789632145",
        payment_id=1,
    )
