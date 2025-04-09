from flask import Blueprint, jsonify, request
from backend.models import Sale, SaleItem, Product, db

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales', methods=['GET'])
def get_sales():
    """Obtener todas las ventas."""
    sales = Sale.query.all()
    return jsonify([{
        "id": s.id,
        "total": s.total,
        "timestamp": s.timestamp
    } for s in sales]), 200

@sales_bp.route('/sales', methods=['POST'])
def create_sale():
    """Crear una nueva venta."""
    data = request.get_json()

    # Validar datos de entrada
    if 'items' not in data or not isinstance(data['items'], list):
        return jsonify({"error": "Items deben ser proporcionados como una lista"}), 400

    total = sum(item['price'] * item['quantity'] for item in data['items'])
    new_sale = Sale(total=total)
    db.session.add(new_sale)
    db.session.commit()

    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({"error": f"Producto con ID {item['product_id']} no encontrado"}), 404
        if product.stock < item['quantity']:
            return jsonify({"error": f"No hay suficiente stock para el producto {product.name}"}), 400

        product.stock -= item['quantity']
        sale_item = SaleItem(
            sale_id=new_sale.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(sale_item)

    db.session.commit()
    return jsonify({"message": "Venta creada"}), 201