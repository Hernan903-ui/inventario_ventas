from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import jwt
import logging
from ..models import Product, ProductHistory
from ..extensions import db

logger = logging.getLogger(__name__)
analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/sales-data', methods=['GET'])
def get_sales_data():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        start_date = datetime.utcnow() - timedelta(days=30)
        
        sales_data = db.session.query(
            Product.name,
            db.func.sum(ProductHistory.quantity).label('total_sales')
        ).join(ProductHistory
        ).filter(
            Product.business_id == decoded['business_id'],
            ProductHistory.type == 'exit',
            ProductHistory.date >= start_date
        ).group_by(Product.name).all()
        
        return jsonify([{
            'product': item[0],
            'sales': item[1]
        } for item in sales_data]), 200

    except Exception as e:
        logger.error(f"Error obteniendo datos de ventas: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/stock-analysis', methods=['GET'])
def get_stock_analysis():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        analysis = {
            'total_products': Product.query.filter_by(business_id=decoded['business_id']).count(),
            'low_stock': Product.query.filter(
                Product.business_id == decoded['business_id'],
                Product.stock <= 10
            ).count(),
            'out_of_stock': Product.query.filter(
                Product.business_id == decoded['business_id'],
                Product.stock == 0
            ).count()
        }
        
        return jsonify(analysis), 200

    except Exception as e:
        logger.error(f"Error en análisis de stock: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/demand-analysis', methods=['GET'])
def get_demand_analysis():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        top_products = db.session.query(
            Product.name,
            db.func.sum(ProductHistory.quantity).label('sales')
        ).join(ProductHistory
        ).filter(
            Product.business_id == decoded['business_id'],
            ProductHistory.type == 'exit',
            ProductHistory.date >= datetime.utcnow() - timedelta(days=30)
        ).group_by(Product.name
        ).order_by(db.desc('sales')).limit(5).all()
        
        low_products = db.session.query(
            Product.name,
            db.func.sum(ProductHistory.quantity).label('sales')
        ).join(ProductHistory
        ).filter(
            Product.business_id == decoded['business_id'],
            ProductHistory.type == 'exit',
            ProductHistory.date >= datetime.utcnow() - timedelta(days=30)
        ).group_by(Product.name
        ).order_by('sales').limit(5).all()
        
        return jsonify({
            'top_products': [{'name': item[0], 'sales': item[1]} for item in top_products],
            'low_products': [{'name': item[0], 'sales': item[1]} for item in low_products]
        }), 200

    except Exception as e:
        logger.error(f"Error en análisis de demanda: {str(e)}")
        return jsonify({'error': str(e)}), 500