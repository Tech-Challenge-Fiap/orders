import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    NoObjectFoundError,
)
from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)
from tests.conftest import BaseRepositoryConfTest


class TestGetOrderById(BaseRepositoryConfTest):
    def order_repository(self):
        return OrderRepository()

    def test_get_order_by_id_found(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query"
        ) as mock_query:
            mock_query.return_value.filter_by.return_value.first.return_value = (
                "MockOrder"
            )
            order_repo = self.order_repository()
            order = order_repo.get_order_by_id(1)
            assert order == "MockOrder"

    def test_get_order_by_id_not_found(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query"
        ) as mock_query:
            mock_query.return_value.filter_by.return_value.first.return_value = None
            order_repo = self.order_repository()
            with pytest.raises(NoObjectFoundError):
                order_repo.get_order_by_id(999)
