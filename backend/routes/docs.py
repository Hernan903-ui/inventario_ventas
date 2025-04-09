from flask_restx import Api, Resource

api = Api(version='1.0', title='Inventory API',
          description='Sistema de gestión de inventario y ventas')

products_ns = api.namespace('products', description='Operaciones con productos')

@products_ns.route('/')
class ProductList(Resource):
    def get(self):
        """Listar todos los productos"""
        return jsonify(Product.query.all())