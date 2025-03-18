# blueprints/locations.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required
from models import db, Customer, CustomerLocation

locations_bp = Blueprint('locations', __name__)

def location_to_dict(loc):
    return {
        'id': loc.id,
        'customer_id': loc.customer_id,
        'address': loc.address,
        'point_of_contact': loc.point_of_contact,
        'property_type': loc.property_type,
        'approx_acres': loc.approx_acres,
        'notes': loc.notes
    }

@locations_bp.route('/customer/<int:customer_id>', methods=['GET'])
@employee_required
def get_locations_for_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    locations = customer.locations
    return jsonify([location_to_dict(loc) for loc in locations]), 200

@locations_bp.route('/customer/<int:customer_id>', methods=['POST'])
@lead_required
def create_location_for_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    try:
        new_location = CustomerLocation(
            customer_id=customer_id,
            address=data.get('address'),
            point_of_contact=data.get('point_of_contact'),
            property_type=data.get('property_type'),
            approx_acres=data.get('approx_acres'),
            notes=data.get('notes')
        )
        db.session.add(new_location)
        db.session.commit()
        return jsonify(location_to_dict(new_location)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@locations_bp.route('/<int:location_id>', methods=['PUT'])
@lead_required
def update_location(location_id):
    location = CustomerLocation.query.get_or_404(location_id)
    data = request.get_json() or {}
    try:
        location.address = data.get('address', location.address)
        location.point_of_contact = data.get('point_of_contact', location.point_of_contact)
        location.property_type = data.get('property_type', location.property_type)
        location.approx_acres = data.get('approx_acres', location.approx_acres)
        location.notes = data.get('notes', location.notes)
        db.session.commit()
        return jsonify(location_to_dict(location)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@lead_required
def delete_location(location_id):
    location = CustomerLocation.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({'msg': 'Location deleted'}), 200
