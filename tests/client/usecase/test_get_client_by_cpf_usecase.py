from unittest.mock import patch
from system.application.dto.responses.client_response import GetClientByCPFResponse
from system.application.exceptions.client_exceptions import ClientDoesNotExistError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.client_usecase import GetClientByCPFUseCase


def test_get_client_by_cpf_usecase_success(mock_client):
    cpf = "64597789065"
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.get_client_by_cpf"
    ) as mock_get_client:
        mock_get_client.return_value = mock_client
        response = GetClientByCPFUseCase.execute(cpf)
        assert isinstance(response, GetClientByCPFResponse)


def test_get_client_by_cpf_usecase_failure():
    cpf = "64597789065"
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.get_client_by_cpf"
    ) as mock_get_client:
        mock_get_client.side_effect = ClientDoesNotExistError
        try:
            GetClientByCPFUseCase.execute(cpf)
        except ClientDoesNotExistError:
            assert True


def test_get_client_by_cpf_usecase_infrastructure_error():
    cpf = "64597789065"
    with patch(
        "system.application.usecase.client_usecase.ClientRepository.get_client_by_cpf"
    ) as mock_get_client:
        mock_get_client.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            GetClientByCPFUseCase.execute(cpf)
        except InfrastructureError:
            assert True
