from models.dbinit import db

class Customers(db.Model):
    customerid = db.Column(db.Integer, primary_key=True)
    customername = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)

