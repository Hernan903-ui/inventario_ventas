# backend/routes/sales.py
from flask import Blueprint, request, jsonify
from ..models import Sale, SaleItem, Product
from ..extensions import db
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['POST'])
def create_sale():
    data = request.get_json()
    
    sale = Sale(total=0)
    db.session.add(sale)
    
    total = 0
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        product.stock -= item['quantity']
        
        sale_item = SaleItem(
            sale=sale,
            product_id=product.id,
            quantity=item['quantity'],
            price=product.sale_price
        )
        total += product.sale_price * item['quantity']
        
        db.session.add(sale_item)
    
    sale.total = total
    db.session.commit()
    
    return jsonify({
        "id": sale.id,
        "total": sale.total,
        "timestamp": sale.timestamp
    }), 201