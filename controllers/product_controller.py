from flask import Blueprint, jsonify, make_response, request
from models.dbinit import db
from sqlalchemy import text

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
            products.append(jsonify({'productid':product[0],'title':product[1],'description':product[2], 'price':product[3],'category':product[4],'imageurl':product[4]}))
        
        return make_response(products,200)
    
    except:
        return make_response(jsonify({'error': 'Error fetching products'}), 500)
        

