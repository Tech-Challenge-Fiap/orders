import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)
from tests.conftest import BaseRepositoryConfTest


class TestGetAllActiveOrders(BaseRepositoryConfTest):
    def order_repository(self):
        return OrderRepository()

    def test_get_all_active_orders_success(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query"
        ) as mock_query:
            mock_query.return_value.filter.return_value.order_by.return_value.all.return_value = [
                "ActiveOrder1",
                "ActiveOrder2",
            ]
            order_repo = self.order_repository()
            active_orders = order_repo.get_all_active_orders()
            assert active_orders == ["ActiveOrder1", "ActiveOrder2"]

    def test_get_all_active_orders_failure(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query",
            side_effect=IntegrityError,
        ):
            order_repo = self.order_repository()
            with pytest.raises(PostgreSQLError):
                order_repo.get_all_active_orders()
