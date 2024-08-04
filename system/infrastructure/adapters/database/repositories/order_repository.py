from collections import Counter
from datetime import datetime
from typing import List
from sqlalchemy import case
from sqlalchemy.exc import IntegrityError
from system.application.exceptions.order_exceptions import OrderUpdateError
from system.application.ports.order_port import OrderPort
from system.domain.entities.order import OrderEntity
from system.domain.entities.ordered_product import OrderedProductEntity
from system.domain.enums.enums import OrderStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.order_model import OrderModel
from system.infrastructure.adapters.database.models.ordered_product_model import (
    OrderedProductModel,
)

class OrderRepository(OrderPort):
    @classmethod
    def create_order(cls, order: OrderEntity) -> OrderEntity:
        # ORDER MODEL PAYLOAD CREATE
        order_to_insert = OrderModel(
            price=order.price,
            status=order.status,
            waiting_time=order.waiting_time,
            client_id=order.client_id,
            created_at=order.created_at
        )

        try:
            db.session.add(order_to_insert)
            db.session.commit()
            db.session.flush()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        ordered_products = []
        for product_data in order.products:
            order_product = OrderedProductModel(
                order_id=order_to_insert.order_id,
                type=product_data.type,
                name=product_data.name,
                price=product_data.price,
                description=product_data.description,
                quantity=product_data.quantity
            )
            ordered_products.append(order_product)
        try:
            db.session.add_all(ordered_products)
            db.session.commit()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        
        order_to_insert.products = order.products
        return OrderEntity.model_validate(order_to_insert)

    @classmethod
    def get_order_by_id(cls, order_id: int) -> OrderEntity:
        """Get a order by it's id"""
        try:
            order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not order:
            raise NoObjectFoundError
        try:
            order_products = db.session.query(OrderedProductModel).filter_by(order_id=order_id).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        product_list = []
        for product in order_products:
            product_list.append(OrderedProductEntity.model_validate(product))

        order_dict = order.__dict__
        order_dict["products"] = product_list
        return OrderEntity.model_validate(order_dict)

    @classmethod
    def get_all_orders(cls) -> List[OrderEntity]:
        """Get all orders"""
        try:
            orders = db.session.query(OrderModel).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        orders_dict = []
        for order in orders:
            try:
                order_products = db.session.query(OrderedProductModel).filter_by(order_id=order.order_id).all()
            except IntegrityError:
                raise PostgreSQLError("PostgreSQL Error")
            product_list = []
            for product in order_products:
                product_list.append(OrderedProductEntity.model_validate(product))
            order_dict = order.__dict__
            order_dict["products"] = product_list
            orders_dict.append(order_dict)
        orders_list = [OrderEntity.model_validate(order) for order in orders_dict]
        return orders_list

    @classmethod
    def update_order_status(cls, order_id: int, status: OrderStatusEnum) -> OrderEntity:
        """Update an order's status"""
        try:
            order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
            order_products = db.session.query(OrderedProductModel).filter_by(order_id=order_id).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
         # Preenche a lista de produtos
        product_list = [
            OrderedProductEntity(
                id=product.id,
                order_id=product.order_id,
                type=product.type,
                name=product.name,
                price=product.price,
                description=product.description,
                quantity=product.quantity,
                observation=product.observation
            )
            for product in order_products
        ]
        # Preenche o OrderEntity com as informações necessárias
        order_entity = OrderEntity(
            order_id=order.order_id,
            created_at=order.created_at,
            price=order.price,
            status=order.status,
            waiting_time=order.waiting_time,
            client_id=order.client_id,
            products=product_list  # Garante que products seja preenchido
        )


        if not order:
            raise NoObjectFoundError
        try:
            order.status = status
            db.session.commit()
        except IntegrityError:
            raise OrderUpdateError
        
        return OrderEntity.model_validate(order_entity)
    
    @classmethod
    def get_all_active_orders(cls) -> List[OrderEntity]:
        """Get all orders"""
        try:
            custom_order = case(
                (OrderModel.status == 'READY', 0),
                (OrderModel.status == 'PREPARING', 1),
                (OrderModel.status == 'RECIEVED', 2),
                else_=3
            )
            
            orders = (
                db.session.query(OrderModel)
                .filter(OrderModel.status.in_(['READY', 'PREPARING', 'RECIEVED']))
                .order_by(custom_order, OrderModel.created_at)
                .all()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        orders_dict = []
        for order in orders:
            try:
                order_products = db.session.query(OrderedProductModel).filter_by(order_id=order.order_id).all()
            except IntegrityError:
                raise PostgreSQLError("PostgreSQL Error")
            product_list = []
            for product in order_products:
                product_list.append(OrderedProductEntity.model_validade(product))
            order_dict = order.__dict__
            order_dict["products"] = product_list
            orders_dict.append(order_dict)
        orders_list = [OrderEntity.model_validade(order) for order in orders_dict]
        return orders_list