import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from system.domain.enums.enums import OrderStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
    NoObjectFoundError,
)
from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)
from tests.conftest import BaseRepositoryConfTest


class TestUpdateOrderStatus(BaseRepositoryConfTest):
    def order_repository(self):
        return OrderRepository()

    def test_update_order_status_success(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query"
        ) as mock_query, patch(
            "system.infrastructure.adapters.database.models.db.session.commit"
        ):
            mock_query.return_value.filter_by.return_value.first.return_value = (
                mock_order
            ) = Mock()
            mock_order.order_id = 1
            order_repo = self.order_repository()
            order = order_repo.update_order_status(1, OrderStatusEnum.READY)
            assert order.status == OrderStatusEnum.READY
            assert order.order_id == 1

    def test_update_order_status_not_found(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query"
        ) as mock_query:
            mock_query.return_value.filter_by.return_value.first.return_value = None
            order_repo = self.order_repository()
            with pytest.raises(NoObjectFoundError):
                order_repo.update_order_status(999, OrderStatusEnum.READY)

    def test_update_order_status_failure(self):
        with patch(
            "system.infrastructure.adapters.database.models.db.session.query"
        ) as mock_query, patch(
            "system.infrastructure.adapters.database.models.db.session.commit",
            side_effect=IntegrityError,
        ):
            mock_query.return_value.filter_by.return_value.first.return_value = Mock()
            order_repo = self.order_repository()
            with pytest.raises(PostgreSQLError):
                order_repo.update_order_status(1, OrderStatusEnum.READY)
