# backend/routes/reports.py
from flask import Blueprint, jsonify
from ..models import Sale, Product
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/sales', methods=['GET'])
def sales_report():
    start_date = datetime.now() - timedelta(days=30)
    sales = Sale.query.filter(Sale.timestamp >= start_date).all()
    
    report_data = [{
        "date": sale.timestamp.strftime("%Y-%m-%d"),
        "total": sale.total,
        "items": [{"product": item.product.name, "quantity": item.quantity} 
                 for item in sale.items]
    } for sale in sales]
    
    return jsonify(report_data), 200