from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from models.customers import Customers 
from models.dbinit import db


class Order(db.Model):
    __tablename__ = 'orders'

    orderid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deliveryaddress = db.Column(db.Text, nullable=False)
    items = db.Column(JSONB, nullable=False)  # Map<String, dynamic> stored as JSONB
    customerid = db.Column(db.Integer, db.ForeignKey('customers.customerid'), nullable=False)
    customer = db.relationship('Customers', backref='orders', lazy=True)
