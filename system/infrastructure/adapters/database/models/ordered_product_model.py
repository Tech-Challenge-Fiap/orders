from . import db

class OrderedProductModel(db.Model):
    __tablename__ = "ordered_products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column("order_id", db.ForeignKey("orders.order_id"))
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    observation = db.Column(db.String(200), nullable=True)
