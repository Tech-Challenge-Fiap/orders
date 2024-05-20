import pytest
from unittest.mock import patch
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from system.infrastructure.adapters.database.models.client_model import ClientModel
from system.infrastructure.adapters.database.repositories.client_repository import (
    ClientRepository,
)
from tests.conftest import BaseRepositoryConfTest


class TestClientRepository(BaseRepositoryConfTest):
    def client_repository(self):
        return ClientRepository()

    def mock_client_model(self):
        return ClientModel(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )

    def mock_client_entity(self):
        # Define a client fixture for use in tests
        return ClientEntity(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )

    def test_create_client_success(self):
        client = self.mock_client_entity()

        client_repo = self.client_repository()
        created_client = client_repo.create_client(client)

        assert client == created_client

    def test_create_client_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.client_repository.db.session.add"
        ), patch(
            "system.infrastructure.adapters.database.repositories.client_repository.db.session.commit",
            side_effect=PostgreSQLError(),
        ):
            with pytest.raises(PostgreSQLError):
                client = self.mock_client_entity()
                client_repo = self.client_repository()
                client_repo.create_client(client)
