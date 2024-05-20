import pytest
from unittest.mock import patch

from system.application.exceptions.repository_exception import DataRepositoryExeption


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


@pytest.fixture
def create_order_data():
    return {"products": [1, 4, 4], "client_id": "45789632145"}


@pytest.fixture
def payment_data():
    return {
        "id": 1,
        "qr_code": "00020101021243650016COM.MERCADOLIBRE02013063638f1192a-5fd1-4180-a180-8bcae3556bc35204000053039865802BR5925IZABEL AAAA DE MELO6007BARUERI62070503***63040B6D",
        "status": "UNPAID",
    }


order_id = 1


def test_create_order_success(client, mock_create_order_response, create_order_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.CreateOrderUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = mock_create_order_response
        response = client.post("/create_order", json=create_order_data)
        assert response.status_code == 200


def test_create_order_product_not_found(client, create_order_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.CreateOrderUseCase.execute",
        side_effect=DataRepositoryExeption,
    ):
        response = client.post("/create_order", json=create_order_data)
        assert response.status_code == 400
