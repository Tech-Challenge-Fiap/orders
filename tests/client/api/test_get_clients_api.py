from unittest.mock import patch
from system.application.exceptions.default_exceptions import InfrastructureError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


def test_get_clients_success(client, mock_get_clients_usecase_response):
    clients_data = [
        {
            "cpf": "64597789065",
            "email": "caio_rolando@email.com.br",
            "name": "Caio Rolando da Rocha",
        },
        {
            "cpf": "98765432100",
            "email": "isadora_coelho@email.com.br",
            "name": "Isadora Coelho",
        },
    ]
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.GetAllClientsUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = mock_get_clients_usecase_response
        response = client.get("/get_clients/")
        assert response.status_code == 200
        assert response.json == clients_data


def test_get_clients_infrastructure_error(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.GetAllClientsUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.get(f"/get_clients/")
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
