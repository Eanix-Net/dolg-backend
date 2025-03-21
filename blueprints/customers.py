# blueprints/customers.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Customer
from werkzeug.security import generate_password_hash
from flasgger import swag_from
from utils.swagger_docs import (
    CUSTOMER_LIST, CUSTOMER_CREATE, CUSTOMER_GET, 
    CUSTOMER_UPDATE, CUSTOMER_DELETE
)

customers_bp = Blueprint('customers', __name__)


def customer_to_dict(cust):
    if not cust:
        return None
    return {
        'id': cust.id,
        'name': cust.name,
        'phone': cust.phone,
        'email': cust.email,
        'notes': cust.notes,
        'created_datetime': cust.created_datetime.isoformat() if cust.created_datetime else None
    }


@customers_bp.route('/', methods=['GET'])
@employee_required
@swag_from(CUSTOMER_LIST)
def get_customers():
    """Get all customers"""
    customers = Customer.query.all()
    return jsonify([customer_to_dict(cust) for cust in customers]), 200


@customers_bp.route('/', methods=['POST'])
@lead_required
@swag_from(CUSTOMER_CREATE)
def create_customer():
    """Create a new customer"""
    data = request.get_json() or {}
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    # Check for duplicate email if provided
    if data.get('email'):
        existing = Customer.query.filter_by(email=data.get('email')).first()
        if existing:
            return jsonify({'error': 'Email already exists'}), 400
    
    try:
        new_customer = Customer(
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            notes=data.get('notes')
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(customer_to_dict(new_customer)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@employee_required
@swag_from(CUSTOMER_GET)
def get_customer(customer_id):
    """Get a specific customer by ID"""
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer_to_dict(customer)), 200


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@lead_required
@swag_from(CUSTOMER_UPDATE)
def update_customer(customer_id):
    """Update a customer"""
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    
    # Check for duplicate email if changing
    if data.get('email') and data.get('email') != customer.email:
        existing = Customer.query.filter_by(email=data.get('email')).first()
        if existing:
            return jsonify({'error': 'Email already exists'}), 400
    
    try:
        if 'name' in data:
            customer.name = data.get('name')
        if 'phone' in data:
            customer.phone = data.get('phone')
        if 'email' in data:
            customer.email = data.get('email')
        if 'notes' in data:
            customer.notes = data.get('notes')
        
        db.session.commit()
        return jsonify(customer_to_dict(customer)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@admin_required
@swag_from(CUSTOMER_DELETE)
def delete_customer(customer_id):
    """Delete a customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'msg': 'Customer deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400