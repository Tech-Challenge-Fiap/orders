from unittest.mock import patch
from system.application.dto.requests.order_request import CreateOrderRequest
from system.application.dto.responses.order_response import CreateOrderResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.order_usecase import CreateOrderUseCase

mocked_payment = {
    "qr_data": "00020101021243650016COM.MERCADOLIBRE02013063638f1192a-5fd1-4180-a180-8bcae3556bc35204000053039865802BR5925IZABEL AAAA DE MELO6007BARUERI62070503***63040B6D",
    "in_store_order_id": "d4e8ca59-3e1d-4c03-b1f6-580e87c654ae",
}


def test_create_order_usecase_success(
    mock_get_products_by_ids_repository_response,
    mock_create_payment_repository,
    mock_create_order,
    mock_update_payment_repository,
):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_products_by_ids"
    ) as mock_get_products:
        mock_get_products.return_value = mock_get_products_by_ids_repository_response
        with patch(
            "system.infrastructure.adapters.database.repositories.payment_repository.PaymentRepository.create_payment"
        ) as mock_create_payment:
            mock_create_payment.return_value = mock_create_payment_repository
            with patch(
                "system.infrastructure.adapters.database.repositories.order_repository.OrderRepository.create_order"
            ) as mock_create_order:
                mock_create_order.return_value = mock_create_order
                with patch(
                    "system.infrastructure.adapters.external_tools.mercado_pago.MercadoPago.create_qr_code_pix_payment"
                ) as mock_create_qr_code:
                    mock_create_qr_code.return_value = mocked_payment
                    with patch(
                        "system.infrastructure.adapters.database.repositories.payment_repository.PaymentRepository.update_payment_qrcode"
                    ) as mock_update_qr_code:
                        mock_update_qr_code.return_value = (
                            mock_update_payment_repository
                        )
                        response = CreateOrderUseCase.execute(
                            CreateOrderRequest(client_id="45789632145", products=[1])
                        )
                        assert isinstance(response, CreateOrderResponse)


def test_create_order_usecase_product_not_found(mock_create_order_request):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_products_by_ids"
    ) as mock_get_products:
        mock_get_products.side_effect = DataRepositoryExeption
        try:
            CreateOrderUseCase.execute(mock_create_order_request)
        except DataRepositoryExeption:
            assert True


def test_create_order_usecase_infrastructure_error(mock_create_order_request):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_products_by_ids"
    ) as mock_get_products:
        mock_get_products.side_effect = InfrastructureError("Database error")
        try:
            CreateOrderUseCase.execute(mock_create_order_request)
        except InfrastructureError as e:
            assert str(e) == "Database error"
