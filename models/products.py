from models.dbinit import db
class Products(db.Model):
    
    productid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Adjust precision and scale as needed
    category = db.Column(db.String(255), nullable=False)
    imageurl = db.Column(db.String(255), nullable=True)
