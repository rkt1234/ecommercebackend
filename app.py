from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.dbinit import db
from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp
import configs
from models.customers import Customers 
# Initialize the Flask application
app = Flask(__name__)

# Load the configuration settings
app.config.from_object(configs.Config)

# Initialize the database and migration tools
db.init_app(app)
with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("Tables created.")
# migrate = Migrate(app, db)

# Initialize the JWT manager
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/product')

if __name__ == '__main__':
    app.run(debug=True)
