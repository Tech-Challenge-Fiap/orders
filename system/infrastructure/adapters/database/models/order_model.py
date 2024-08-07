from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from system.domain.enums.enums import OrderStatusEnum
from . import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    price = db.Column(db.Integer)
    status = db.Column(SQLAlchemyEnum(OrderStatusEnum), nullable=False)
    waiting_time = db.Column(db.Integer)
    client_id = db.Column(db.String, db.ForeignKey("clients.cpf"), nullable=True)
    client = relationship("ClientModel", back_populates="order")
