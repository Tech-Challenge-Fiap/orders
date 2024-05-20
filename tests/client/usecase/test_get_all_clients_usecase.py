from unittest.mock import patch
from system.application.dto.responses.client_response import GetAllClientsResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.client_usecase import GetAllClientsUseCase


def test_get_all_clients_usecase_success(mock_client):
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.get_all_clients"
    ) as mock_get_clients:
        mock_get_clients.return_value = mock_client
        response = GetAllClientsUseCase.execute()
        assert isinstance(response, GetAllClientsResponse)


def test_get_all_clients_usecase_failure():
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.get_all_clients"
    ) as mock_get_clients:
        mock_get_clients.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            GetAllClientsUseCase.execute()
        except InfrastructureError:
            assert True
