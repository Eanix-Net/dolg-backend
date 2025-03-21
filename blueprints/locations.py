# blueprints/locations.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Customer, CustomerLocation
from flasgger import swag_from
from utils.swagger_docs import (
    LOCATION_LIST, LOCATION_CREATE, LOCATION_GET, 
    LOCATION_UPDATE, LOCATION_DELETE
)

locations_bp = Blueprint('locations', __name__)

def location_to_dict(loc):
    if not loc:
        return None
    return {
        'id': loc.id,
        'customer_id': loc.customer_id,
        'address': loc.address,
        'city': loc.city,
        'state': loc.state,
        'zip_code': loc.zip_code,
        'point_of_contact': loc.point_of_contact,
        'property_type': loc.property_type,
        'approx_acres': loc.approx_acres,
        'notes': loc.notes,
        'created_at': loc.created_at.isoformat() if loc.created_at else None,
        'updated_at': loc.updated_at.isoformat() if loc.updated_at else None
    }

@locations_bp.route('/', methods=['GET'])
@employee_required
@swag_from(LOCATION_LIST)
def get_all_locations():
    """Get all locations"""
    locations = CustomerLocation.query.all()
    return jsonify([location_to_dict(loc) for loc in locations]), 200

@locations_bp.route('/customer/<int:customer_id>', methods=['GET'])
@employee_required
@swag_from(LOCATION_LIST)
def get_customer_locations(customer_id):
    """Get all locations for a customer"""
    customer = Customer.query.get_or_404(customer_id)
    locations = CustomerLocation.query.filter_by(customer_id=customer_id).all()
    return jsonify([location_to_dict(loc) for loc in locations]), 200

@locations_bp.route('/', methods=['POST'])
@lead_required
@swag_from(LOCATION_CREATE)
def create_location():
    """Create a new location for a customer"""
    data = request.get_json() or {}
    
    # Validate required fields
    if not data.get('customer_id'):
        return jsonify({'error': 'Customer ID is required'}), 400
    if not data.get('address'):
        return jsonify({'error': 'Address is required'}), 400
    
    # Check if customer exists
    customer = Customer.query.get(data.get('customer_id'))
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    try:
        new_location = CustomerLocation(
            customer_id=data.get('customer_id'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            point_of_contact=data.get('point_of_contact'),
            property_type=data.get('property_type'),
            approx_acres=data.get('approx_acres'),
            notes=data.get('notes')
        )
        db.session.add(new_location)
        db.session.commit()
        return jsonify(location_to_dict(new_location)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@locations_bp.route('/<int:location_id>', methods=['GET'])
@employee_required
@swag_from(LOCATION_GET)
def get_location(location_id):
    """Get a specific location by ID"""
    location = CustomerLocation.query.get_or_404(location_id)
    return jsonify(location_to_dict(location)), 200

@locations_bp.route('/<int:location_id>', methods=['PUT'])
@lead_required
@swag_from(LOCATION_UPDATE)
def update_location(location_id):
    """Update a location"""
    location = CustomerLocation.query.get_or_404(location_id)
    data = request.get_json() or {}
    
    try:
        if 'address' in data:
            location.address = data.get('address')
        if 'city' in data:
            location.city = data.get('city')
        if 'state' in data:
            location.state = data.get('state')
        if 'zip_code' in data:
            location.zip_code = data.get('zip_code')
        if 'point_of_contact' in data:
            location.point_of_contact = data.get('point_of_contact')
        if 'property_type' in data:
            location.property_type = data.get('property_type')
        if 'approx_acres' in data:
            location.approx_acres = data.get('approx_acres')
        if 'notes' in data:
            location.notes = data.get('notes')
        
        db.session.commit()
        return jsonify(location_to_dict(location)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@admin_required
@swag_from(LOCATION_DELETE)
def delete_location(location_id):
    """Delete a location"""
    try:
        location = CustomerLocation.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return jsonify({'msg': 'Location deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
