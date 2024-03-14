from flask import Flask
from flask_restful import Api
from models import db
from resources import ProductListResource, ProductResource, CartResource, CartItemResource, ProductCreateResource, HomePage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db.init_app(app)
api = Api(app)

api.add_resource(HomePage, '/')
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(ProductCreateResource, '/products/create')
api.add_resource(CartResource, '/cart')
api.add_resource(CartItemResource, '/cart/<int:cart_item_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
