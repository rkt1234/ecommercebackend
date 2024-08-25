import datetime
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.cart import Cart
from models.dbinit import db
from sqlalchemy import text

from models.orders import Order
from models.products import Products
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
    data = request.get_json()
    try:
        customerId = data['customerId']
        productId = data['productId']
        quantity = data['quantity']
        total = data['total']
        
        # Check if the product is already in the cart
        existing_cart_item = Cart.query.filter_by(customerid=customerId, productid=productId).first()
        
        if existing_cart_item:
            return make_response({'message': 'Product is already in the cart'}, 409)  # 409 Conflict

        # Add new item to the cart
        cart = Cart(customerid=customerId, productid=productId, quantity=quantity, total=total)
        db.session.add(cart)
        db.session.commit()
        
        return make_response({'message': 'Added to cart Successfully'}, 200)
    except Exception as e:
        return make_response({'message': 'Could not add to cart'}, 500)


@product_bp.route('/fetch/cart',methods=['GET'])
@jwt_required()
def fetchCart():
    try:
        customerId = get_jwt_identity()
        print(customerId)
        results = db.session.query(Cart, Products).join(Products, Cart.productid == Products.productid).filter(Cart.customerid == customerId).all()
        cart_items = []
        for cart, product in results:
            cart_items.append({
            "cartid": cart.cartid,
            "userid": cart.customerid,
            "productid": product.productid,
            "quantity": cart.quantity,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "imageurl": product.imageurl,
            "total":cart.total
        })
            print(product.title)
        return make_response(cart_items,200)
        
    except:
        return make_response({'message':'Could not fetch cart'},500)
    
@product_bp.route('/update/cart', methods=['PUT'])
@jwt_required()
def updateCart():
    try:
        data=request.get_json()
        cartid=data['cartId']
        quantity=data['quantity']
        cart = Cart.query.filter_by(cartid=cartid).first()
        cart.quantity=quantity
        db.session.commit()
        return make_response({'message':'Cart updated successfully'},200)
    except:
        return make_response({'message':'Could not update cart'},500)

@product_bp.route('/delete/cart', methods=['DELETE'])
@jwt_required()
def deleteCart():
    try:
        data=request.get_json()
        cartid=data['cartId']
        cart = Cart.query.filter_by(cartid=cartid).first()
        db.session.delete(cart)
        db.session.commit()
        return make_response({'message':'Item deleted successfully'},200)
    except:
        return make_response({'message':'Could not delete item'},500)
    
@product_bp.route('/place/order', methods=['POST'])
@jwt_required()
def placeOrder():
    try:
        print("yaha aa chuka h ");
        data=request.get_json()
        customerId=data['customerId']
        items=data['items']
        deliveryAddress=data['deliveryAddress']
        order = Order(customerid=customerId, date=datetime.now(), items=items, deliveryaddress=deliveryAddress)
        db.session.add(order)
        db.session.commit()
        return make_response({'message':'Order placed successfully'},200)
    
    except Exception as e:
        # Log the full stack trace if needed
        # Return the exception message
        return make_response({'message': str(e)}, 500)
