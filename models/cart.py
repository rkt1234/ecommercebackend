from models.dbinit import db
from models.products import Products  
from models.customers import Customers 


class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customers.customerid'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('products.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total = db.Column(db.Float, nullable=False)

    product = db.relationship('Products', backref='cart', lazy=True)
    customer = db.relationship('Customers', backref='cart', lazy=True)
