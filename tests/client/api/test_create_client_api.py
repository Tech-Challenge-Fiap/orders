import pytest
from unittest.mock import patch
from system.application.dto.responses.client_response import CreateClientResponse
from system.application.exceptions.client_exceptions import ClientAlreadyExistsError
from system.application.exceptions.default_exceptions import InfrastructureError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


@pytest.fixture
def create_client_data():
    return {
        "cpf": "64597789065",
        "name": "Caio Rolando da Rocha",
        "email": "caio_rolando@email.com.br",
    }


def test_create_client_success(client, create_client_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.CreateClientUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = CreateClientResponse(create_client_data)
        response = client.post(
            "/create_client",
            json=create_client_data,
            headers={
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcGYiOiJhbm9ueW1vdXMiLCJpYXQiOjE3MTA4MTEwMjUsImV4cCI4758586MTcxMDgxNDYyNX0.Cjzev847laO0V57YyyEimjUmYi10EWOBNpkeQI_xY6c"
            },
        )
        assert response.status_code == 200
        assert response.json == create_client_data


def test_create_client_already_exists(client, create_client_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.CreateClientUseCase.execute",
        side_effect=ClientAlreadyExistsError,
    ):
        response = client.post("/create_client", json=create_client_data)
        assert response.status_code == 400
        assert response.json == {"error": "This Client already exists"}


def test_create_client_infrastructure_error(client, create_client_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.client_usecase.CreateClientUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.post("/create_client", json=create_client_data)
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
