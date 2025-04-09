from flask import Blueprint, jsonify, request
from backend.models import Product, db
from backend.schemas import ProductSchema  # Asegúrate de tener este archivo

products_bp = Blueprint('products', __name__)
product_schema = ProductSchema()

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Obtener todos los productos."""
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "cost_price": p.cost_price,
        "sale_price": p.sale_price,
        "stock": p.stock,
        "last_updated": p.last_updated
    } for p in products]), 200

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obtener un producto específico por ID."""
    product = Product.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "cost_price": product.cost_price,
        "sale_price": product.sale_price,
        "stock": product.stock,
        "last_updated": product.last_updated
    }), 200

@products_bp.route('/products', methods=['POST'])
def create_product():
    """Crear un nuevo producto."""
    errors = product_schema.validate(request.json)
    if errors:
        return jsonify({"errors": errors}), 400

    new_product = Product(
        name=request.json['name'],
        cost_price=request.json['cost_price'],
        sale_price=request.json['sale_price'],
        stock=request.json.get('stock', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Producto creado"}), 201

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualizar un producto existente."""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.cost_price = data.get('cost_price', product.cost_price)
    product.sale_price = data.get('sale_price', product.sale_price)
    product.stock = data.get('stock', product.stock)

    db.session.commit()
    return jsonify({"message": "Producto actualizado"}), 200

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Eliminar un producto."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Producto eliminado"}), 200