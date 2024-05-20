import pytest
from unittest.mock import patch

from system.application.exceptions.default_exceptions import InfrastructureError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


@pytest.fixture
def active_orders_data():
    return [
        {
            "client_id": "45789632145",
            "order_date": "Sat, 20 Jan 2024 00:00:00 GMT",
            "order_id": 1,
            "payment": {
                "id": 1,
                "qr_code": "00020101021243650016COM.MERCADOLIBRE02013063638f1192a-5fd1-4180-a180-8bcae3556bc35204000053039865802BR5925IZABEL AAAA DE MELO6007BARUERI62070503***63040B6D",
                "status": "UNPAID",
            },
            "price": "80",
            "products": [
                {
                    "name": "Frango",
                    "price": 20,
                    "product_id": 1,
                    "quantity": 1,
                    "type": "SNACK",
                },
                {
                    "name": "Hamburguer",
                    "price": 30,
                    "product_id": 5,
                    "quantity": 2,
                    "type": "SNACK",
                },
            ],
            "status": "PREPARING",
            "waiting_time": 90,
        },
        {
            "client_id": "45789632145",
            "order_date": "Sat, 20 Jan 2024 00:00:00 GMT",
            "order_id": 1,
            "payment": {
                "id": 1,
                "qr_code": "00020101021243650016COM.MERCADOLIBRE02013063638f1192a-5fd1-4180-a180-8bcae3556bc35204000053039865802BR5925IZABEL AAAA DE MELO6007BARUERI62070503***63040B6D",
                "status": "UNPAID",
            },
            "price": "80",
            "products": [
                {
                    "name": "Frango",
                    "price": 20,
                    "product_id": 1,
                    "quantity": 1,
                    "type": "SNACK",
                },
                {
                    "name": "Hamburguer",
                    "price": 30,
                    "product_id": 5,
                    "quantity": 2,
                    "type": "SNACK",
                },
            ],
            "status": "PREPARING",
            "waiting_time": 90,
        },
    ]


def test_get_active_orders_success(client, mock_get_orders_response):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.GetOrdersUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = mock_get_orders_response
        response = client.get("/get_active_orders/")
        assert response.status_code == 200


def test_get_active_orders_infrastructure_error(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.GetOrdersUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.get("/get_active_orders/")
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
