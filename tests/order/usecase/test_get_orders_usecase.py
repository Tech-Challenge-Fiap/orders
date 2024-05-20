from unittest.mock import patch
from system.application.dto.responses.order_response import GetAllOrdersResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.usecase.order_usecase import GetOrdersUseCase


def test_get_orders_usecase_success(mock_orders):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_all_active_orders"
    ) as mock_get_all_active_orders:
        mock_get_all_active_orders.return_value = mock_orders
        response = GetOrdersUseCase.execute()
        assert isinstance(response, GetAllOrdersResponse)


def test_get_orders_usecase_infrastructure_error():
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_all_active_orders"
    ) as mock_get_all_active_orders:
        mock_get_all_active_orders.side_effect = InfrastructureError("Database error")
        try:
            GetOrdersUseCase.execute()
        except InfrastructureError as e:
            assert str(e) == "Database error"
