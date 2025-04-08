from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import jwt
import logging
from ..models import Product, ProductHistory, User
from ..extensions import db

logger = logging.getLogger(__name__)
products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['POST'])
def create_product():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        data = request.json
        if Product.query.filter_by(barcode=data['barcode'], business_id=decoded['business_id']).first():
            return jsonify({'error': 'Código de barras ya existe'}), 400

        new_product = Product(
            business_id=decoded['business_id'],
            supplier_id=data['supplier_id'],
            barcode=data['barcode'],
            name=data['name'],
            cost_price=data['cost_price'],
            sale_price=data['sale_price'],
            stock=data.get('stock', 0)
        )
        db.session.add(new_product)
        db.session.commit()

        logger.info(f"Producto creado ID: {new_product.id}")
        return jsonify({'message': 'Producto creado', 'id': new_product.id}), 201

    except Exception as e:
        logger.error(f"Error creando producto: {str(e)}")
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        products = Product.query.filter_by(business_id=decoded['business_id']).all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'barcode': p.barcode,
            'stock': p.stock,
            'sale_price': p.sale_price,
            'last_updated': p.last_updated.isoformat()
        } for p in products]), 200

    except Exception as e:
        logger.error(f"Error obteniendo productos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        product = Product.query.filter_by(id=id, business_id=decoded['business_id']).first()
        if not product:
            return jsonify({'error': 'Producto no encontrado'}), 404

        data = request.json
        product.name = data.get('name', product.name)
        product.cost_price = data.get('cost_price', product.cost_price)
        product.sale_price = data.get('sale_price', product.sale_price)
        product.stock = data.get('stock', product.stock)
        product.last_updated = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'message': 'Producto actualizado'}), 200

    except Exception as e:
        logger.error(f"Error actualizando producto: {str(e)}")
        return jsonify({'error': str(e)}), 500

@products_bp.route('/stock', methods=['POST'])
def update_stock():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        data = request.json
        product = Product.query.filter_by(id=data['product_id'], business_id=decoded['business_id']).first()
        if not product:
            return jsonify({'error': 'Producto no encontrado'}), 404

        product.stock += data['quantity']
        product.last_updated = datetime.utcnow()
        
        history = ProductHistory(
            product_id=product.id,
            type='entry' if data['quantity'] > 0 else 'exit',
            quantity=abs(data['quantity']),
            user_id=decoded['id']
        )
        db.session.add(history)
        db.session.commit()

        logger.info(f"Stock actualizado para producto {product.id}")
        return jsonify({'new_stock': product.stock}), 200

    except Exception as e:
        logger.error(f"Error actualizando stock: {str(e)}")
        return jsonify({'error': str(e)}), 500

@products_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        LOW_STOCK_THRESHOLD = 10
        products = Product.query.filter(
            Product.business_id == decoded['business_id'],
            Product.stock <= LOW_STOCK_THRESHOLD
        ).all()
        
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'stock': p.stock,
            'supplier_id': p.supplier_id
        } for p in products]), 200

    except Exception as e:
        logger.error(f"Error obteniendo stock bajo: {str(e)}")
        return jsonify({'error': str(e)}), 500