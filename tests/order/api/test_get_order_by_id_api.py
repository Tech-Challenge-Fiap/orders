from unittest.mock import patch

from system.application.exceptions.order_exceptions import OrderDoesNotExistError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


order_id = 1


def test_get_order_by_id_success(client, mock_get_order_by_id_response):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.GetOrderByIDUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = mock_get_order_by_id_response
        response = client.get(f"/get_order/{order_id}")
        assert response.status_code == 200


def test_get_order_by_id_not_found(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.GetOrderByIDUseCase.execute",
        side_effect=OrderDoesNotExistError,
    ):
        response = client.get(f"/get_order/{order_id}")
        assert response.status_code == 404
        assert response.json == {"error": "This Order does not exist"}
