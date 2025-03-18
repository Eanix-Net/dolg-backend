# blueprints/quotes.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, admin_required, lead_required
from models import db, Quote, QuoteItem, Appointment, Employee
from datetime import datetime

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
@employee_required
def get_quotes():
    quotes = Quote.query.all()
    return jsonify([quote_to_dict(q) for q in quotes]), 200

@quotes_bp.route('/', methods=['POST'])
@lead_required
def create_quote():
    data = request.get_json() or {}
    try:
        # Verify appointment exists
        appointment = Appointment.query.get_or_404(data.get('appointment_id'))
        # Verify employee exists
        employee = Employee.query.get_or_404(data.get('employee_id'))
        
        new_quote = Quote(
            appointment_id=data.get('appointment_id'),
            estimate=data.get('estimate'),
            employee_id=data.get('employee_id')
        )
        db.session.add(new_quote)
        db.session.commit()
        return jsonify(quote_to_dict(new_quote)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@quotes_bp.route('/<int:quote_id>', methods=['GET'])
@employee_required
def get_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return jsonify(quote_to_dict(quote)), 200

@quotes_bp.route('/<int:quote_id>', methods=['PUT'])
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
@admin_required
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return jsonify({'msg': 'Quote deleted'}), 200

# Quote Items Endpoints
@quotes_bp.route('/<int:quote_id>/items', methods=['GET'])
@employee_required
def get_quote_items(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return jsonify([quote_item_to_dict(item) for item in quote.items]), 200

@quotes_bp.route('/<int:quote_id>/services', methods=['POST'])
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
@admin_required
def delete_quote_service(item_id):
    item = QuoteItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'Quote service deleted'}), 200
