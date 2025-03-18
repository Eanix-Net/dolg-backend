# blueprints/invoices.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Invoice, InvoiceItem, Appointment
from datetime import datetime, date

invoices_bp = Blueprint('invoices', __name__)

def invoice_to_dict(inv):
    return {
        'id': inv.id,
        'appointment_id': inv.appointment_id,
        'subtotal': inv.subtotal,
        'total': inv.total,
        'tax_rate': inv.tax_rate,
        'paid': inv.paid,
        'attempt': inv.attempt,
        'due_date': inv.due_date.isoformat(),
        'created_date': inv.created_date.isoformat()
    }

def invoice_item_to_dict(item):
    return {
        'id': item.id,
        'invoice_id': item.invoice_id,
        'service': item.service,
        'cost': item.cost
    }

# Invoice Endpoints
@invoices_bp.route('/', methods=['GET'])
@employee_required
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([invoice_to_dict(inv) for inv in invoices]), 200

@invoices_bp.route('/', methods=['POST'])
@lead_required
def create_invoice():
    data = request.get_json() or {}
    try:
        # Verify appointment exists
        appointment = Appointment.query.get_or_404(data.get('appointment_id'))
        
        new_invoice = Invoice(
            appointment_id=data.get('appointment_id'),
            subtotal=data.get('subtotal', 0),
            total=data.get('total', 0),
            tax_rate=data.get('tax_rate', 0),
            paid=data.get('paid', 'unpaid'),
            attempt=data.get('attempt', 1),
            due_date=date.fromisoformat(data['due_date']) if data.get('due_date') else None
        )
        db.session.add(new_invoice)
        db.session.commit()
        return jsonify(invoice_to_dict(new_invoice)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@invoices_bp.route('/<int:invoice_id>', methods=['GET'])
@employee_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify(invoice_to_dict(invoice)), 200

@invoices_bp.route('/<int:invoice_id>', methods=['PUT'])
@lead_required
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json() or {}
    try:
        invoice.subtotal = data.get('subtotal', invoice.subtotal)
        invoice.total = data.get('total', invoice.total)
        invoice.tax_rate = data.get('tax_rate', invoice.tax_rate)
        invoice.paid = data.get('paid', invoice.paid)
        invoice.attempt = data.get('attempt', invoice.attempt)
        if data.get('due_date'):
            invoice.due_date = date.fromisoformat(data['due_date'])
        db.session.commit()
        return jsonify(invoice_to_dict(invoice)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@invoices_bp.route('/<int:invoice_id>', methods=['DELETE'])
@admin_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'msg': 'Invoice deleted'}), 200

# Invoice Items Endpoints
@invoices_bp.route('/<int:invoice_id>/items', methods=['GET'])
@lead_required
def get_invoice_items(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify([invoice_item_to_dict(item) for item in invoice.items]), 200

@invoices_bp.route('/<int:invoice_id>/items', methods=['POST'])
@lead_required
def create_invoice_item(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json() or {}
    try:
        new_item = InvoiceItem(
            invoice_id=invoice_id,
            service_id=data.get('service_id'),
            cost=data.get('cost')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify(invoice_item_to_dict(new_item)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@invoices_bp.route('/items/<int:item_id>', methods=['PUT'])
@lead_required
def update_invoice_item(item_id):
    item = InvoiceItem.query.get_or_404(item_id)
    data = request.get_json() or {}
    try:
        item.cost = data.get('cost', item.cost)
        db.session.commit()
        return jsonify(invoice_item_to_dict(item)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@invoices_bp.route('/items/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_invoice_item(item_id):
    item = InvoiceItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'Invoice item deleted'}), 200
