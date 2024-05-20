import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from system.domain.entities.order import OrderEntity
from tests.conftest import BaseRepositoryConfTest
from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)


class TestCreateOrder(BaseRepositoryConfTest):
    def order_repository(self):
        return OrderRepository()

    def mock_order_entity(self):
        return OrderEntity(
            price=100.0,
            status="WAITING PAYMENT",
            waiting_time=30,
            payment_id="pay_123",
            client_id="client_123",
            order_date="2023-01-01",
            products_ids=[1, 2, 2],
        )

    def test_create_order_success(self):
        order = self.mock_order_entity()
        order_repo = self.order_repository()
        with patch(
            "system.infrastructure.adapters.database.models.db.session.add"
        ), patch(
            "system.infrastructure.adapters.database.models.db.session.commit"
        ), patch(
            "system.infrastructure.adapters.database.models.db.session.flush"
        ):
            created_order = order_repo.create_order(order)
        assert order == created_order

    def test_create_order_failure(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.add",
            side_effect=IntegrityError,
        ):
            with pytest.raises(PostgreSQLError):
                order = self.mock_order_entity()
                order_repo = self.order_repository()
                order_repo.create_order(order)
