import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.models.client_model import ClientModel
from system.infrastructure.adapters.database.repositories.client_repository import (
    ClientRepository,
)
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
    NoObjectFoundError,
)
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestClientRepository(BaseRepositoryConfTest):
    def client_repository(self):
        return ClientRepository()

    def test_get_client_by_cpf_success(self):
        client_model = ClientModel(
            cpf="64597789065",
            name="Caio Rolando da Rocha",
            email="caio_rolando@email.com.br",
        )
        db.session.add(client_model)
        db.session.commit()

        client_repo = self.client_repository()
        retrieved_client = client_repo.get_client_by_cpf("64597789065")

        assert retrieved_client is not None
        assert retrieved_client.cpf == "64597789065"
        assert retrieved_client.name == "Caio Rolando da Rocha"

    def test_get_client_by_cpf_not_found(self):
        db.session.query(ClientModel).delete()
        db.session.commit()

        client_repo = self.client_repository()
        with pytest.raises(NoObjectFoundError):
            client_repo.get_client_by_cpf("nonexistent_cpf")

    def test_get_client_by_cpf_integrity_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.client_repository.db.session.query",
            side_effect=PostgreSQLError(),
        ):
            with pytest.raises(PostgreSQLError):
                client_repo = self.client_repository()
                client_repo.get_client_by_cpf("64597789065")
