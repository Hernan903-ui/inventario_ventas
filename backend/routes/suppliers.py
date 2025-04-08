from flask import Blueprint, request, jsonify, current_app
import jwt
import logging
from ..models import Supplier
from ..extensions import db

logger = logging.getLogger(__name__)
suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/suppliers', methods=['POST'])
def create_supplier():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        data = request.json
        new_supplier = Supplier(
            business_id=decoded['business_id'],
            name=data['name'],
            contact=data['contact']
        )
        db.session.add(new_supplier)
        db.session.commit()

        logger.info(f"Proveedor creado ID: {new_supplier.id}")
        return jsonify({'message': 'Proveedor creado', 'id': new_supplier.id}), 201

    except Exception as e:
        logger.error(f"Error creando proveedor: {str(e)}")
        return jsonify({'error': str(e)}), 500

@suppliers_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        suppliers = Supplier.query.filter_by(business_id=decoded['business_id']).all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'contact': s.contact,
            'created_at': s.created_at.isoformat()
        } for s in suppliers]), 200

    except Exception as e:
        logger.error(f"Error obteniendo proveedores: {str(e)}")
        return jsonify({'error': str(e)}), 500

@suppliers_bp.route('/suppliers/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        supplier = Supplier.query.filter_by(id=id, business_id=decoded['business_id']).first()
        if not supplier:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
            
        db.session.delete(supplier)
        db.session.commit()
        
        return jsonify({'message': 'Proveedor eliminado'}), 200

    except Exception as e:
        logger.error(f"Error eliminando proveedor: {str(e)}")
        return jsonify({'error': str(e)}), 500