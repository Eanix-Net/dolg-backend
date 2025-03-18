# blueprints/customers.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Customer
from werkzeug.security import generate_password_hash

customers_bp = Blueprint('customers', __name__)


def customer_to_dict(cust):
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
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer_to_dict(cust) for cust in customers]), 200


@customers_bp.route('/', methods=['POST'])
@lead_required
def create_customer():
    data = request.get_json() or {}
    new_customer = Customer(
        name=data.get('name'),
        phone=data.get('phone'),
        email=data.get('email'),
        notes=data.get('notes')
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(customer_to_dict(new_customer)), 201


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@employee_required
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer_to_dict(customer)), 200


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@lead_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    customer.name = data.get('name', customer.name)
    customer.phone = data.get('phone', customer.phone)
    customer.email = data.get('email', customer.email)
    customer.notes = data.get('notes', customer.notes)
    db.session.commit()
    return jsonify(customer_to_dict(customer)), 200


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@admin_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'msg': 'Customer deleted'}), 200