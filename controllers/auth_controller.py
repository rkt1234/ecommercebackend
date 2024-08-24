import hashlib
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models.customers import Customers
from models.dbinit import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        customerName = data['customerName']
        address=data['address']
        existing_user_email = Customers.query.filter_by(email=email).first()

        if existing_user_email:
            return make_response(jsonify({'message': 'Email already exists'}), 400)

        customer = Customers(email=email, password=password, customername=customerName, address=address)
        db.session.add(customer)
        db.session.commit()
        customer_id = customer.customerid
        db.session.close()
        access_token = create_access_token(identity=customer_id,  additional_claims={
            'address': address,
            'customerName': customerName,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
    )
        return make_response(jsonify({'access_token': access_token}), 200)
    except  Exception as e :
        return make_response(jsonify({'message': 'Could not register'}), 500)
    
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        # Retrieve user by email
        customer = Customers.query.filter_by(email=email).first()

        if customer and password==customer.password:
            # Generate JWT token
            access_token = create_access_token(identity=customer.customerid,  additional_claims={
            'address': customer.address,
            'customerName': customer.customername,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
            })
            return make_response(jsonify({'access_token': access_token}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid email or password'}), 401)
    except Exception as e:
        return make_response(jsonify({'message': f'Could not log in: {str(e)}'}), 500)