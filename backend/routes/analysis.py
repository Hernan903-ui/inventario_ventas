from flask import Blueprint, jsonify
from backend.models import Sale
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/sales-analysis', methods=['GET'])
def sales_analysis():
    """Obtener análisis de ventas."""
    sales = Sale.query.all()
    total_sales = sum(s.total for s in sales)
    monthly_sales = {}

    for sale in sales:
        month = sale.timestamp.strftime('%Y-%m')
        monthly_sales[month] = monthly_sales.get(month, 0) + sale.total

    return jsonify({
        "total_sales": total_sales,
        "number_of_sales": len(sales),
        "monthly_sales": monthly_sales
    }), 200