from flask import Blueprint, jsonify
from flask_restx import Api, Resource
from backend.models import Product  # Asegúrate de que este modelo exista

docs_bp = Blueprint('docs', __name__)
api = Api(docs_bp, version='1.0', title='Inventario API', description='API for inventory management')

@api.route('/products')
class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        return jsonify([{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products])