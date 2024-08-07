from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models import db
import config

# Initialize the Flask application
app = Flask(__name__)

# Load the configuration settings
app.config.from_object(config.Config)

# Initialize the database and migration tools
db.init_app(app)
migrate = Migrate(app, db)

# Initialize the JWT manager
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(home_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
