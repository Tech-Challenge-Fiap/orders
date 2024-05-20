from unittest.mock import patch


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


def test_get_all_orders_success(client, all_orders_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.order_usecase.GetAllOrdersUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = all_orders_data
        response = client.get("/get_orders/")
        assert response.status_code == 200
        assert response.json == all_orders_data
