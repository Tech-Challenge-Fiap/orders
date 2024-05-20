from typing import Any, Iterator, List
from unittest.mock import patch

from flask import Flask
from flask.testing import FlaskClient
from httpx import Headers
import pytest

from app import app
from system.application.dto.requests.client_request import (
    CreateClientRequest,
)
from system.application.dto.responses.client_response import (
    ClientResponse,
    CreateClientResponse,
    GetClientByCPFResponse,
    GetAllClientsResponse,
)
from system.domain.entities.client import ClientEntity


def create_client():
    return ClientEntity(
        cpf="64597789065",
        name="Caio Rolando da Rocha",
        email="caio_rolando@email.com.br",
    )


@pytest.fixture
def mock_client_repository():
    with patch(
        "system.infrastructure.adapters.database.repositories.client_repository.ClientRepository",
        autospec=True,
    ) as client_repository:
        yield client_repository


@pytest.fixture
def mock_client() -> ClientEntity:
    """
    Mock that creates a Client
    """
    return create_client()


@pytest.fixture
def mock_create_client_repository_response() -> Any:
    """
    Mock that creates a Client
    """
    return {
        "cpf": "64597789065",
        "name": "Caio Rolando da Rocha",
        "email": "caio_rolando@email.com.br",
    }


@pytest.fixture
def mock_create_client_request() -> CreateClientRequest:
    """
    Mock that creates a CreateClientRequest
    """
    return CreateClientRequest(
        cpf="64597789065",
        name="Caio Rolando da Rocha",
        email="caio_rolando@email.com.br",
    )


@pytest.fixture
def mock_create_client_response() -> CreateClientResponse:
    """
    Mock that creates a CreateClientResponse
    """
    return CreateClientResponse(
        cpf="64597789065",
        name="Caio Rolando da Rocha",
        email="caio_rolando@email.com.br",
    )


@pytest.fixture
def mock_get_client_by_cpf_response() -> GetClientByCPFResponse:
    """
    Mock that creates a GetClientByCPFResponse
    """
    return GetClientByCPFResponse(
        cpf="64597789065",
        name="Caio Rolando da Rocha",
        email="caio_rolando@email.com.br",
    )


@pytest.fixture
def mock_get_clients_response() -> GetAllClientsResponse:
    """
    Mock that creates a GetAllClientsResponse
    """
    client_list: List[ClientResponse] = []
    client_list.append(
        ClientResponse(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )
    )
    client_list.append(
        ClientResponse(
            cpf="98765432100",
            name="Isadora Coelho",
            email="isadora_coelho@email.com.br",
        )
    )
    return GetAllClientsResponse(clients=client_list)


@pytest.fixture
def mock_get_clients_usecase_response() -> List[ClientEntity]:
    """
    Mock that creates a List[ClientEntity]
    """
    client_list: List[ClientEntity] = []
    client_list.append(
        ClientEntity(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )
    )
    client_list.append(
        ClientEntity(
            cpf="98765432100",
            name="Isadora Coelho",
            email="isadora_coelho@email.com.br",
        )
    )
    return GetAllClientsResponse(client_list)


@pytest.fixture
def client_repository_response() -> ClientEntity:
    """
    Mock that creates a ClientEntity
    """
    return ClientEntity(
        cpf="64597789065",
        name="Caio Rolando da Rocha",
        email="caio_rolando@email.com.br",
    )


@pytest.fixture
def mock_get_clients_repository_response() -> List[ClientEntity]:
    """
    Mock that creates a List[ClientEntity]
    """
    client_list: List[ClientEntity] = []
    client_list.append(
        ClientEntity(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )
    )
    client_list.append(
        ClientEntity(
            cpf="98765432100",
            name="Isadora Coelho",
            email="isadora_coelho@email.com.br",
        )
    )
    return client_list


@pytest.fixture
def flask_app() -> Flask:
    """
    Fixture for creating Flask app.
    :return: flask app with mocked dependencies.
    """
    return app


@pytest.fixture
def client(flask_app: Flask) -> Iterator[FlaskClient]:
    """
    Fixture that creates client for requesting server.
    :param flask_app: the application.
    :yield: client for the app.
    """
    authorization_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcGYiOiJhbm9ueW1vdXMiLCJpYXQiOjE3MTA4MTEwMjUsImV4cCI4758586MTcxMDgxNDYyNX0.Cjzev847laO0V57YyyEimjUmYi10EWOBNpkeQI_xY6c"

    with flask_app.test_client() as test_client:
        headers = Headers()
        headers.add("Authorization", f"Bearer {authorization_token}")
        test_client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {authorization_token}"
        yield test_client
