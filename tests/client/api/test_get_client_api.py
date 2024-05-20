from unittest.mock import patch
from system.application.dto.responses.client_response import ClientResponse
from system.application.exceptions.client_exceptions import ClientDoesNotExistError
from system.application.exceptions.default_exceptions import InfrastructureError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


def test_get_client_by_cpf_success(client):
    client_data = {
        "cpf": "64597789065",
        "name": "Caio Rolando da Rocha",
        "email": "caio_rolando@email.com.br",
    }
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.GetClientByCPFUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = ClientResponse(client_data)
        response = client.get(f'/get_client/{"64597789065"}')
        assert response.status_code == 200
        assert response.json == client_data


def test_get_client_by_cpf_not_found(client):
    cpf = "64597789065"
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.GetClientByCPFUseCase.execute",
        side_effect=ClientDoesNotExistError,
    ):
        response = client.get(f"/get_client/{cpf}")
        assert response.status_code == 404
        assert response.json == {"error": "This Client does not exist"}


def test_get_client_by_cpf_infrastructure_error(client):
    cpf = "12345678900"
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.GetClientByCPFUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.get(f"/get_client/{cpf}")
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
