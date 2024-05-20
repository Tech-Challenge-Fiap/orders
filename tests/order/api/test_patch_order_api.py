from unittest.mock import patch

from system.application.exceptions.order_exceptions import OrderDoesNotExistError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


order_id = 1


def test_patch_order_success(client, mock_update_order_response, update_order_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.UpdateOrderStatusUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = mock_update_order_response
        response = client.patch(f"/patch_order/{order_id}", json=update_order_data)
        assert response.status_code == 200


def test_patch_order_not_found(client, update_order_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.UpdateOrderStatusUseCase.execute",
        side_effect=OrderDoesNotExistError,
    ):
        response = client.patch(f"/patch_order/{order_id}", json=update_order_data)
        assert response.status_code == 400
        assert response.text == "This Order does not exist"
