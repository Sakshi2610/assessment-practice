from flask_restful import Resource, reqparse
from models import db, Product, CartItem
from flask import current_app, render_template, make_response

class HomePage(Resource):
     def get(self):
        html_content = render_template('documentation.html')
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        return response
     
class ProductListResource(Resource):
    def get(self):
        with current_app.app_context():
            products = Product.query.all()
            return [{'id': product.id, 'name': product.name, 'description': product.description,
                     'price': product.price, 'image_url': product.image_url} for product in products]

class ProductResource(Resource):
    def get(self, product_id):
        with current_app.app_context():
            product = Product.query.get_or_404(product_id)
            return {'id': product.id, 'name': product.name, 'description': product.description,
                    'price': product.price, 'image_url': product.image_url}

class ProductCreateResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str)
    parser.add_argument('price', type=float, required=True)
    parser.add_argument('image_url', type=str)

    def post(self):
        args = self.parser.parse_args()
        name = args['name']
        description = args.get('description', '')
        price = args['price']
        image_url = args.get('image_url', '')

        with current_app.app_context():
            product = Product(name=name, description=description, price=price, image_url=image_url)
            db.session.add(product)
            db.session.commit()

        return {'message': 'Product added successfully.', 'product_id': product.id}

class CartResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id', type=int, required=True)
    parser.add_argument('quantity', type=int, required=True)

    def post(self):
        args = self.parser.parse_args()
        product_id = args['product_id']
        quantity = args['quantity']

        with current_app.app_context():
            cart_item = CartItem(product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()

        return {'message': 'Product added to the cart successfully.'}

    def get(self):
        with current_app.app_context():
            cart_items = CartItem.query.all()
            return [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]

class CartItemResource(Resource):
    def delete(self, cart_item_id):
        with current_app.app_context():
            cart_item = CartItem.query.get_or_404(cart_item_id)
            db.session.delete(cart_item)
            db.session.commit()
        return {'message': 'Item removed from the cart successfully.'}
        