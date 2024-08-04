from decimal import Decimal
from flask_restful import Resource
from psycopg2 import IntegrityError
from system.application.dto.requests.order_request import CreateOrderRequest
from system.application.dto.responses.order_response import (
    CreateOrderResponse,
    GetAllOrdersResponse,
    GetOrderByIDResponse,
    UpdateOrderResponse,
)
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.order_exceptions import (
    OrderDoesNotExistError,
    OrderUpdateError,
)
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.order import OrderEntity
from system.domain.entities.ordered_product import OrderedProductEntity
from system.domain.enums.enums import OrderStatusEnum
from system.application.exceptions.repository_exception import (
    NoObjectFoundError,
    DataRepositoryExeption,
)
from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)
from system.infrastructure.adapters.external_tools.payment_service import PaymentService
from rabbitmq import publish_message
import json

class CreateOrderUseCase(UseCase, Resource):
    def execute(request: CreateOrderRequest) -> CreateOrderResponse:
        """
        Create Order
        """
        order_price = Decimal("0")
        order_waiting_time = 0
        products_models = []
        for product in request.products:
            order_price += Decimal(product.price) * Decimal(str(product.quantity))
            order_waiting_time += product.waiting_time * product.quantity
            products_models.append(OrderedProductEntity(**product.model_dump()))
        try:
            order = OrderEntity(
                price=order_price,
                products=products_models,
                waiting_time=order_waiting_time,
                client_id=request.client_id,
            )
            response = OrderRepository.create_order(order)

            message = json.dumps({
                "order_id": response.order_id,
                "client_id": request.client_id,
                "price": str(order_price),
            })
            publish_message('fila-pagamentos', message)
            
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return CreateOrderResponse(response.model_dump())


class GetOrderByIDUseCase(UseCase, Resource):
    def execute(order_id: int) -> GetOrderByIDResponse:
        """
        Get order by its id
        """
        try:
            response = OrderRepository.get_order_by_id(order_id)
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return GetOrderByIDResponse(response.model_dump())


class GetAllOrdersUseCase(UseCaseNoRequest, Resource):
    def execute() -> GetAllOrdersResponse:
        """
        Get orders with filters
        """
        try:
            response = OrderRepository.get_all_orders()
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))

        orders = [r.model_dump() for r in response]
        return GetAllOrdersResponse(orders)


class UpdateOrderStatusUseCase(UseCase, Resource):
    def execute(
        status: OrderStatusEnum,
        order_id: int,
    ) -> UpdateOrderResponse:
        """
        Update order status
        """
        try:
            response = OrderRepository.update_order_status(order_id, status)
        except IntegrityError as err:
            raise OrderUpdateError(str(err))
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        return UpdateOrderResponse(response.model_dump())
    
class GetOrdersUseCase(UseCaseNoRequest, Resource):
    def execute() -> GetAllOrdersResponse:
        """
        Get orders with filters
        """
        try:
            response = OrderRepository.get_all_active_orders()
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))

        orders = [r.model_dump() for r in response]
        return GetAllOrdersResponse(orders)
