from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import hashlib
import jwt
import logging
from ..models import User, Business
from ..extensions import db

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        existing_business = Business.query.filter_by(name=data['business_name']).first()
        if existing_business:
            return jsonify({'error': 'Nombre de negocio ya existe'}), 400

        new_business = Business(name=data['business_name'])
        db.session.add(new_business)
        db.session.commit()

        hashed_password = hash_password(data['password'])
        new_user = User(
            business_id=new_business.id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"Nuevo negocio registrado: {new_business.name}")
        return jsonify({'message': 'Registro exitoso'}), 201

    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or user.password != hash_password(data['password']):
            return jsonify({'error': 'Credenciales inválidas'}), 401

        token = jwt.encode({
            'id': user.id,
            'business_id': user.business_id,
            'exp': datetime.utcnow() + timedelta(hours=8)
        }, current_app.config['JWT_SECRET'], algorithm='HS256')

        logger.info(f"Usuario autenticado: {user.email}")
        return jsonify({
            'token': token,
            'business_id': user.business_id,
            'user_id': user.id
        }), 200

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
def get_users():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Cabecera Authorization inválida'}), 401
            
        token = auth_header.split()[1]
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        
        users = User.query.filter_by(business_id=decoded['business_id']).all()
        return jsonify([{
            'id': u.id,
            'name': f"{u.first_name} {u.last_name}",
            'email': u.email
        } for u in users]), 200

    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {str(e)}")
        return jsonify({'error': str(e)}), 500