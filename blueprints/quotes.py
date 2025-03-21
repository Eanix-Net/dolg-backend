# blueprints/quotes.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, admin_required, lead_required
from models import db, Quote, QuoteItem, Appointment, Employee, Customer, CustomerLocation
from datetime import datetime, timedelta
from flasgger import swag_from
from utils.swagger_docs import (
    QUOTES_GET,
    QUOTES_POST,
    QUOTES_QUOTE_ID_GET,
    QUOTES_QUOTE_ID_PUT,
    QUOTES_QUOTE_ID_DELETE,
    QUOTES_QUOTE_ID_POST,
    QUOTES_ITEM_ID_PUT,
    QUOTES_ITEM_ID_DELETE)

quotes_bp = Blueprint('quotes', __name__)

def quote_to_dict(quote):
    return {
        'id': quote.id,
        'appointment_id': quote.appointment_id,
        'estimate': quote.estimate,
        'employee_id': quote.employee_id,
        'created_date': quote.created_date.isoformat()
    }

def quote_item_to_dict(qs):
    return {
        'id': qs.id,
        'quote_id': qs.quote_id,
        'service_id': qs.service_id,
        'cost': qs.cost
    }

# Quote Endpoints
@quotes_bp.route('/', methods=['GET'])
@swag_from(QUOTES_GET)
@employee_required
def get_quotes():
    quotes = Quote.query.all()
    return jsonify([quote_to_dict(q) for q in quotes]), 200

@quotes_bp.route('/', methods=['POST'])
@swag_from(QUOTES_POST)
@lead_required
def create_quote():
    data = request.get_json() or {}
    try:
        # Validate required fields
        if not data.get('appointment_id'):
            return jsonify({'msg': 'Appointment ID is required'}), 400
        if not data.get('employee_id'):
            return jsonify({'msg': 'Employee ID is required'}), 400
            
        # Verify appointment exists
        appointment = Appointment.query.get(data.get('appointment_id'))
        if not appointment:
            return jsonify({'msg': 'Appointment not found'}), 400
            
        # Verify employee exists
        employee = Employee.query.get(data.get('employee_id'))
        if not employee:
            return jsonify({'msg': 'Employee not found'}), 400
        
        # Create the quote
        new_quote = Quote(
            appointment_id=data.get('appointment_id'),
            employee_id=data.get('employee_id'),
            estimate=data.get('estimate', 0)
        )
        db.session.add(new_quote)
        db.session.commit()
        return jsonify(quote_to_dict(new_quote)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400

@quotes_bp.route('/<int:quote_id>', methods=['GET'])
@swag_from(QUOTES_QUOTE_ID_GET)
@employee_required
def get_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return jsonify(quote_to_dict(quote)), 200

@quotes_bp.route('/<int:quote_id>', methods=['PUT'])
@swag_from(QUOTES_QUOTE_ID_PUT)
@lead_required
def update_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    data = request.get_json() or {}
    try:
        quote.estimate = data.get('estimate', quote.estimate)
        db.session.commit()
        return jsonify(quote_to_dict(quote)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@quotes_bp.route('/<int:quote_id>', methods=['DELETE'])
@swag_from(QUOTES_QUOTE_ID_DELETE)
@admin_required
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return jsonify({'msg': 'Quote deleted'}), 200

# Quote Items Endpoints
@quotes_bp.route('/<int:quote_id>/items', methods=['GET'])
@swag_from(QUOTES_QUOTE_ID_GET)
@employee_required
def get_quote_items(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return jsonify([quote_item_to_dict(item) for item in quote.items]), 200

@quotes_bp.route('/<int:quote_id>/services', methods=['POST'])
@swag_from(QUOTES_QUOTE_ID_POST)
@lead_required
def create_quote_service(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    data = request.get_json() or {}
    try:
        new_item = QuoteItem(
            quote_id=quote_id,
            service_id=data.get('service_id'),
            cost=data.get('cost')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify(quote_item_to_dict(new_item)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@quotes_bp.route('/items/<int:item_id>', methods=['PUT'])
@swag_from(QUOTES_ITEM_ID_PUT)
@lead_required
def update_quote_item(item_id):
    item = QuoteItem.query.get_or_404(item_id)
    data = request.get_json() or {}
    try:
        item.cost = data.get('cost', item.cost)
        db.session.commit()
        return jsonify(quote_item_to_dict(item)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@quotes_bp.route('/item/<int:item_id>', methods=['DELETE'])
@swag_from(QUOTES_ITEM_ID_DELETE)
@admin_required
def delete_quote_service(item_id):
    item = QuoteItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'Quote service deleted'}), 200
