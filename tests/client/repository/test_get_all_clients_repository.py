import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.models.client_model import ClientModel
from system.infrastructure.adapters.database.repositories.client_repository import (
    ClientRepository,
)
from system.domain.entities.client import ClientEntity
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestClientRepository(BaseRepositoryConfTest):
    def client_repository(self):
        return ClientRepository()

    def mock_client_entity(self):
        return ClientEntity(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )

    def test_get_all_clients_success(self):
        # Setup - Adding clients to the database session
        clients_data = [
            ClientModel(
                cpf="64597789065",
                name="Caio Rolando da Rocha",
                email="caio_rolando@email.com.br",
            ),
            ClientModel(
                cpf="98765432100",
                name="Isadora Coelho",
                email="isadora_coelho@email.com.br",
            ),
        ]
        db.session.add_all(clients_data)
        db.session.commit()

        client_repo = self.client_repository()
        retrieved_clients = client_repo.get_all_clients()

        assert len(retrieved_clients) == 2
        assert all(isinstance(client, ClientEntity) for client in retrieved_clients)
        assert set(client.cpf for client in retrieved_clients) == {
            "64597789065",
            "98765432100",
        }

    def test_get_all_clients_error(self):
        # Setup - Mock the query to raise an IntegrityError
        with patch(
            "system.infrastructure.adapters.database.repositories.client_repository.db.session.query",
            side_effect=PostgreSQLError(),
        ):
            with pytest.raises(PostgreSQLError):
                client_repo = self.client_repository()
                client_repo.get_all_clients()
