# from . import db

# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     description = db.Column(db.String(200))
#     price = db.Column(db.Float, nullable=False)
#     image_url = db.Column(db.String(200))

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, nullable=False)

# class OrderDetail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)


from . import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(128), nullable=False)
    brand = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(256), nullable=False, default='default_product.jpg')
    
    # This relationship is used to access order details from the Product side
    order_details = db.relationship('OrderDetail', backref='product')

    def __repr__(self):
        return f'<Product {self.name} - ${self.price}>'

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    total_cost = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # This relationship is used to access product details from the Order side
    order_details = db.relationship('OrderDetail', backref='order')

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderDetail(db.Model):
    __tablename__ = 'orderdetails'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<OrderDetail Order {self.order_id} Product {self.product_id} Quantity {self.quantity}>'
