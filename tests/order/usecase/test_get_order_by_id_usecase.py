from unittest.mock import patch
from system.application.dto.responses.order_response import GetOrderByIDResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.order_exceptions import OrderDoesNotExistError
from system.application.usecase.order_usecase import GetOrderByIDUseCase


def test_get_order_by_id_usecase_success(mock_order_id, mock_order):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_order_by_id"
    ) as mock_get_order_by_id:
        mock_get_order_by_id.return_value = mock_order
        response = GetOrderByIDUseCase.execute(mock_order_id)
        assert isinstance(response, GetOrderByIDResponse)


def test_get_order_by_id_usecase_order_not_found(mock_order_id):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_order_by_id"
    ) as mock_get_order_by_id:
        mock_get_order_by_id.side_effect = OrderDoesNotExistError
        try:
            GetOrderByIDUseCase.execute(mock_order_id)
        except OrderDoesNotExistError:
            assert True


def test_get_order_by_id_usecase_infrastructure_error(mock_order_id):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.get_order_by_id"
    ) as mock_get_order_by_id:
        mock_get_order_by_id.side_effect = InfrastructureError("Database error")
        try:
            GetOrderByIDUseCase.execute(mock_order_id)
        except InfrastructureError as e:
            assert str(e) == "Database error"
