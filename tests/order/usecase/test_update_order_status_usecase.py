from unittest.mock import patch
from system.application.dto.responses.order_response import UpdateOrderResponse
from system.application.exceptions.order_exceptions import OrderUpdateError
from system.application.usecase.order_usecase import UpdateOrderStatusUseCase


def test_update_order_status_usecase_success(mock_order_id, mock_status):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.update_order_status"
    ) as mock_update_order_status:
        mock_update_order_status.return_value = {
            "status": mock_status.name,
            "order_id": mock_order_id,
        }
        response = UpdateOrderStatusUseCase.execute(
            status=mock_status, order_id=mock_order_id
        )
        assert isinstance(response, UpdateOrderResponse)
        assert response.status == mock_status.name


def test_update_order_status_usecase_order_update_error(mock_order_id, mock_status):
    with patch(
        "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.update_order_status"
    ) as mock_update_order_status:
        mock_update_order_status.side_effect = OrderUpdateError("Update failed")
        try:
            UpdateOrderStatusUseCase.execute(status=mock_status, order_id=mock_order_id)
        except OrderUpdateError as e:
            assert str(e) == "Update failed"
