from models.dbinit import db
from models.products import Products  
from models.customers import Customers 
class Review(db.Model):
    
    reviewid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productid = db.Column(db.Integer, db.ForeignKey('products.productid'), nullable=False)
    review = db.Column(db.Text, nullable=False)
    customerid = db.Column(db.Integer, db.ForeignKey('customers.customerid'), nullable=False)
    
    # Relationships
    product = db.relationship('Products', backref='reviews', lazy=True)
    customer = db.relationship('Customers', backref='reviews', lazy=True)