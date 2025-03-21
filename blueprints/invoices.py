# blueprints/invoices.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Invoice, InvoiceItem, Appointment, CustomerLocation, Customer, Service
from datetime import datetime, date, timedelta
from flasgger import swag_from
from utils.swagger_docs import (
    INVOICES_GET,
    INVOICES_POST,
    INVOICES_INVOICE_ID_GET,
    INVOICES_INVOICE_ID_PUT,
    INVOICES_INVOICE_ID_DELETE,
    INVOICES_INVOICE_ID_POST,
    INVOICES_ITEM_ID_PUT,
    INVOICES_ITEM_ID_DELETE
)

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
@swag_from(INVOICES_GET)
@employee_required
def get_invoices():
    customer_id = request.args.get('customer_id', type=int)
    
    # If customer_id is provided, filter by customer
    if customer_id:
        invoices = Invoice.query.filter_by(customer_id=customer_id).all()
    else:
        invoices = Invoice.query.all()
        
    return jsonify([invoice_to_dict(inv) for inv in invoices]), 200

@invoices_bp.route('/', methods=['POST'])
@swag_from(INVOICES_POST)
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
@swag_from(INVOICES_INVOICE_ID_GET)
@employee_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify(invoice_to_dict(invoice)), 200

@invoices_bp.route('/<int:invoice_id>', methods=['PUT'])
@swag_from(INVOICES_INVOICE_ID_PUT)
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
@swag_from(INVOICES_INVOICE_ID_DELETE)
@admin_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'msg': 'Invoice deleted'}), 200

# Invoice Items Endpoints
@invoices_bp.route('/<int:invoice_id>/items', methods=['GET'])
@swag_from(INVOICES_INVOICE_ID_GET)
@lead_required
def get_invoice_items(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify([invoice_item_to_dict(item) for item in invoice.items]), 200

@invoices_bp.route('/<int:invoice_id>/items', methods=['POST'])
@swag_from(INVOICES_INVOICE_ID_POST)
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
@swag_from(INVOICES_ITEM_ID_PUT)
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
@swag_from(INVOICES_ITEM_ID_DELETE)
@admin_required
def delete_invoice_item(item_id):
    item = InvoiceItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'Invoice item deleted'}), 200

# Add endpoint to generate invoice from appointment
@invoices_bp.route('/from-appointment/<int:appointment_id>', methods=['POST'])
@swag_from(INVOICES_POST)
@lead_required
def generate_invoice_from_appointment(appointment_id):
    try:
        # Get the appointment
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Get customer information from location
        customer_location = CustomerLocation.query.get_or_404(appointment.customer_location_id)
        customer = Customer.query.get_or_404(customer_location.customer_id)
        
        # Calculate invoice details
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=30)  # Due in 30 days
        
        # Generate a unique invoice number
        invoice_count = Invoice.query.count()
        invoice_number = f"INV-{issue_date.year}{issue_date.month:02d}-{invoice_count + 1:04d}"
        
        # Create the invoice
        new_invoice = Invoice(
            appointment_id=appointment_id,
            customer_id=customer.id,
            customer_name=customer.name,
            invoice_number=invoice_number,
            subtotal=0.0,  # Will be updated based on items
            total=0.0,     # Will be updated based on items
            tax_rate=0.0,  # Default, can be adjusted
            paid='unpaid',
            status='draft',
            amount_paid=0.0,
            balance=0.0,   # Will be updated based on total
            due_date=due_date,
            notes=f"Invoice for appointment on {appointment.arrival_datetime.strftime('%Y-%m-%d')}"
        )
        
        db.session.add(new_invoice)
        db.session.flush()  # Get the invoice ID without committing
        
        # Create a default invoice item for the lawn service
        service = Service.query.filter_by(name='Lawn Service').first()
        if not service:
            # Create a default service if it doesn't exist
            service = Service(name='Lawn Service', description='Regular lawn maintenance service')
            db.session.add(service)
            db.session.flush()
        
        # Calculate duration in hours (for pricing)
        duration_hours = (appointment.departure_datetime - appointment.arrival_datetime).total_seconds() / 3600
        
        # Default price of $75 per service
        item_cost = 75.0
        
        # Create the invoice item
        item = InvoiceItem(
            invoice_id=new_invoice.id,
            service_id=service.id,
            cost=item_cost
        )
        
        db.session.add(item)
        
        # Update invoice totals
        new_invoice.subtotal = item_cost
        new_invoice.total = item_cost
        new_invoice.balance = item_cost
        
        db.session.commit()
        
        return jsonify(invoice_to_dict(new_invoice)), 201
        
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

# Add endpoint to get payments for an invoice
@invoices_bp.route('/<int:invoice_id>/payments', methods=['GET'])
@swag_from(INVOICES_INVOICE_ID_GET)
@employee_required
def get_invoice_payments(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Import the Payment model and get related payments
    from models import Payment
    payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    
    # Define payment_to_dict function if not already defined
    def payment_to_dict(payment):
        return {
            'id': payment.id,
            'invoice_id': payment.invoice_id,
            'amount': payment.amount,
            'payment_date': payment.payment_date.isoformat(),
            'payment_method': payment.payment_method,
            'reference_number': payment.reference_number,
            'notes': payment.notes,
            'created_at': payment.created_at.isoformat() if payment.created_at else None,
            'updated_at': payment.updated_at.isoformat() if payment.updated_at else None
        }
    
    return jsonify([payment_to_dict(payment) for payment in payments]), 200
