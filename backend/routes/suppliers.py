from flask import Blueprint, jsonify, request
from backend.models import Supplier, db

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    """Obtener todos los proveedores."""
    suppliers = Supplier.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "contact": s.contact,
        "created_at": s.created_at
    } for s in suppliers]), 200

@suppliers_bp.route('/suppliers', methods=['POST'])
def create_supplier():
    """Crear un nuevo proveedor."""
    data = request.get_json()
    if 'name' not in data or 'contact' not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    new_supplier = Supplier(
        name=data['name'],
        contact=data['contact']
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "Proveedor creado"}), 201

@suppliers_bp.route('/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    """Actualizar un proveedor existente."""
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()

    supplier.name = data.get('name', supplier.name)
    supplier.contact = data.get('contact', supplier.contact)

    db.session.commit()
    return jsonify({"message": "Proveedor actualizado"}), 200

@suppliers_bp.route('/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    """Eliminar un proveedor."""
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": "Proveedor eliminado"}), 200