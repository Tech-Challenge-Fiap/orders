from unittest.mock import patch
from system.application.dto.responses.client_response import CreateClientResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.client_usecase import CreateClientUseCase


def test_create_client_usecase_success(mock_client, mock_create_client_request):
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.create_client"
    ) as mock_create_client:
        mock_create_client.return_value = mock_client
        response = CreateClientUseCase.execute(mock_create_client_request)
        assert isinstance(response, CreateClientResponse)


def test_create_client_usecase_failure(mock_create_client_request):
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.create_client"
    ) as mock_create_client:
        mock_create_client.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            CreateClientUseCase.execute(mock_create_client_request)
        except InfrastructureError:
            assert True
