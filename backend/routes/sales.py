from flask import request, jsonify
from flask_jwt_extended import jwt_required
from ..models import Sale, Product
from ..schemas import SaleSchema

sales_bp = Blueprint('sales', __name__)
sales_schema = SaleSchema()

@sales_bp.route('/sales', methods=['POST'])
@jwt_required()
def create_sale():
    data = request.get_json()
    errors = sales_schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        # Lógica para procesar la venta
        new_sale = Sale(total=calculate_total(data['items']))
        db.session.add(new_sale)
        update_stock(data['items'])
        db.session.commit()
        return jsonify({"message": "Venta registrada"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500