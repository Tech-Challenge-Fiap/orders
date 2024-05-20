from unittest.mock import patch
from system.application.dto.responses.order_response import GetAllOrdersResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.usecase.order_usecase import GetAllOrdersUseCase


def test_get_all_orders_usecase_success(mock_orders):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_all_orders"
    ) as mock_get_all_orders:
        mock_get_all_orders.return_value = mock_orders
        response = GetAllOrdersUseCase.execute()
        assert isinstance(response, GetAllOrdersResponse)


def test_get_all_orders_usecase_infrastructure_error():
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_all_orders"
    ) as mock_get_all_orders:
        mock_get_all_orders.side_effect = InfrastructureError("Database error")
        try:
            GetAllOrdersUseCase.execute()
        except InfrastructureError as e:
            assert str(e) == "Database error"
