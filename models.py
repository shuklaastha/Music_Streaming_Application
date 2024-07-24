from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Manager(db.Model, UserMixin):
    m_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    m_name = db.Column(db.String(50), nullable=False)
    m_email = db.Column(db.String(20), unique=True, nullable=False)
    m_password = db.Column(db.String(10), nullable=False)

    def get_id(self):
        return str(self.m_id)

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    out_of_stock = db.Column(db.Boolean, nullable=False, default=False)
    category = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
 



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), unique=True, nullable=False)



# Define the UOM model
class UOM(db.Model, UserMixin):
    __tablename__ = 'uom'
    
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String, nullable=False)
    
 


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False, default=0.0)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False, default=0.0)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    overall_total = db.Column(db.Float, nullable=False, default=0.0)
    cart_items = db.relationship('CartItem', backref='order')





