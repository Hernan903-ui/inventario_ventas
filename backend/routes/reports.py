from flask import Blueprint, request, jsonify, make_response, current_app
import jwt
from datetime import datetime
import logging
from ..models import ProductHistory, Product, User
from ..extensions import db
from ..utils.pdf_generator import generate_pdf_report

logger = logging.getLogger(__name__)
reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/history-report', methods=['GET'])
def generate_history_report():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        history = db.session.query(
            Product.name,
            ProductHistory.quantity,
            ProductHistory.type,
            ProductHistory.date,
            User.first_name
        ).join(Product
        ).join(User
        ).filter(
            Product.business_id == decoded['business_id']
        ).all()
        
        pdf_data = generate_pdf_report(
            title="Historial de Movimientos",
            headers=['Producto', 'Cantidad', 'Tipo', 'Fecha', 'Usuario'],
            data=[(item[0], item[1], item[2], item[3].strftime('%Y-%m-%d'), item[4]) for item in history]
        )
        
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=historial.pdf'
        return response

    except Exception as e:
        logger.error(f"Error generando reporte: {str(e)}")
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/analytics-report', methods=['GET'])
def generate_analytics_report():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        sales_data = db.session.query(
            Product.name,
            db.func.sum(ProductHistory.quantity).label('sales')
        ).join(ProductHistory
        ).filter(
            Product.business_id == decoded['business_id'],
            ProductHistory.type == 'exit'
        ).group_by(Product.name).all()
        
        pdf_data = generate_pdf_report(
            title="Reporte Analítico",
            headers=['Producto', 'Ventas Totales'],
            data=[(item[0], item[1]) for item in sales_data],
            charts=True
        )
        
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=analitico.pdf'
        return response

    except Exception as e:
        logger.error(f"Error generando reporte analítico: {str(e)}")
        return jsonify({'error': str(e)}), 500