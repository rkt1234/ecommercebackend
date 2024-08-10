from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from models.cart import Cart
from models.dbinit import db
from sqlalchemy import text

from models.reviews import Review

product_bp= Blueprint('product_bp', __name__)

@product_bp.route('/fetch/categories', methods=['GET'])
def fetchCategory():
    try:
        result = db.session.execute(text('select * from categories')).fetchall()
        categories=[]
        for item in result:
            categories.append(item[1])
        return make_response(categories,200)
    except:
        return make_response(jsonify({'error': 'Error fetching categories'}), 500)
    
@product_bp.route('/fetch/products/', methods=['GET'])
def fetchProducts():
    category = request.args.get('category', default=None, type=str)
    products=[]
    try:
        if category == "all":
            result = db.session.execute(text('select * from products')).fetchall()
        else:
            result = db.session.execute(text('select * from products where category = :category'), {'category':category}).fetchall()
        
        print(result)
        
        for product in result:
            print(product)
            products.append({'productid':product[0],'title':product[1],'description':product[2], 'price':product[3],'category':product[4],'imageurl':product[5]})
        
        return make_response(products,200)
    
    except:
        return make_response(jsonify({'error': 'Error fetching products'}), 500)

@product_bp.route('/add/review', methods=['POST'])
@jwt_required()
def addReviews():
    data=request.get_json()
    try:
        review=data['review']
        productId=data['productId']
        customerId=data['customerId']
        print(review)
        cutomerReview = Review(review=review, productid=productId, customerid=customerId)
        db.session.add(cutomerReview)
        db.session.commit()
        return make_response({'message':'Review Added Successfully'},200)
    except :
        return make_response({'message':'Could not add review'},500)
    
@product_bp.route('/fetch/reviews', methods=['POST'])
def fetchReviews():
    data = request.get_json()
    try:
        productId=data['productId']
        result = db.session.execute(text('select * from review where productid = :productId'), {'productId':productId}).fetchall()
        print(result)
        reviews=[]
        for review in result:
            customerId = review[3]
            customer = db.session.execute(text('select customername from customers where customerid = :customerId'), {'customerId':customerId}).fetchone()
            customerName = customer[0] if customer else 'Unknown'
            reviews.append({'review':review[2], 'customerName':customerName})
        
        return make_response(reviews,200)
    except:
        return make_response({'message':'Could not fetch review'},500)


@product_bp.route('/add/cart', methods=['POST'])
@jwt_required()
def addCart():
    data=request.get_json()
    try:
        customerId=data['customerId']
        productId=data['productId']
        quantity=data['quantity']
        total=data['total']
        cart = Cart(customerid=customerId, productid=productId, quantity=quantity, total=total)
        db.session.add(cart)
        db.session.commit()
        return make_response({'message':'Added to cart Successfully'},200)
    except Exception as e:
        print(e)
        # return make_response({'message':e},500)
        return e;

