# blueprints/payments.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Invoice, Payment
from datetime import datetime
from flasgger import swag_from
from utils.swagger_docs import (
    PAYMENTS_POST,
    PAYMENTS_PAYMENT_ID_GET,
    PAYMENTS_INVOICE_ID_GET,
    PAYMENTS_PAYMENT_ID_PUT,
    PAYMENTS_PAYMENT_ID_DELETE)

payments_bp = Blueprint('payments', __name__)

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

@payments_bp.route('/', methods=['POST'])
@swag_from(PAYMENTS_POST)
@lead_required
def create_payment():
    data = request.get_json() or {}
    try:
        # Verify invoice exists
        invoice = Invoice.query.get_or_404(data.get('invoice_id'))
        
        new_payment = Payment(
            invoice_id=data.get('invoice_id'),
            amount=data.get('amount'),
            payment_date=datetime.fromisoformat(data.get('payment_date')),
            payment_method=data.get('payment_method'),
            reference_number=data.get('reference_number'),
            notes=data.get('notes'),
            created_at=datetime.now(datetime.UTC)
        )
        
        # Update invoice paid amount
        invoice.amount_paid = invoice.amount_paid + new_payment.amount
        
        # Update invoice balance
        invoice.balance = invoice.total - invoice.amount_paid
        
        # Update payment status if fully paid
        if invoice.balance <= 0:
            invoice.status = 'paid'
        
        db.session.add(new_payment)
        db.session.commit()
        
        return jsonify(payment_to_dict(new_payment)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@payments_bp.route('/<int:payment_id>', methods=['GET'])
@swag_from(PAYMENTS_PAYMENT_ID_GET)
@employee_required
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment_to_dict(payment)), 200

@payments_bp.route('/invoice/<int:invoice_id>', methods=['GET'])
@swag_from(PAYMENTS_INVOICE_ID_GET)
@employee_required
def get_payments_for_invoice(invoice_id):
    # Verify invoice exists
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Get all payments for this invoice
    payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    
    return jsonify([payment_to_dict(payment) for payment in payments]), 200

@payments_bp.route('/<int:payment_id>', methods=['PUT'])
@swag_from(PAYMENTS_PAYMENT_ID_PUT)
@lead_required
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    invoice = Invoice.query.get_or_404(payment.invoice_id)
    
    data = request.get_json() or {}
    old_amount = payment.amount
    
    try:
        if 'amount' in data:
            payment.amount = data.get('amount')
            
            # Update invoice paid amount and balance
            amount_difference = payment.amount - old_amount
            invoice.amount_paid = invoice.amount_paid + amount_difference
            invoice.balance = invoice.total - invoice.amount_paid
            
            # Update payment status if fully paid
            if invoice.balance <= 0:
                invoice.status = 'paid'
            else:
                invoice.status = 'unpaid'
        
        if 'payment_date' in data:
            payment.payment_date = datetime.fromisoformat(data.get('payment_date'))
        
        if 'payment_method' in data:
            payment.payment_method = data.get('payment_method')
            
        if 'reference_number' in data:
            payment.reference_number = data.get('reference_number')
            
        if 'notes' in data:
            payment.notes = data.get('notes')
            
        payment.updated_at = datetime.now(datetime.UTC)
        
        db.session.commit()
        return jsonify(payment_to_dict(payment)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@payments_bp.route('/<int:payment_id>', methods=['DELETE'])
@swag_from(PAYMENTS_PAYMENT_ID_DELETE)
@admin_required
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    invoice = Invoice.query.get_or_404(payment.invoice_id)
    
    try:
        # Update invoice paid amount and balance
        invoice.amount_paid = invoice.amount_paid - payment.amount
        invoice.balance = invoice.total - invoice.amount_paid
        
        # Update payment status
        if invoice.balance <= 0:
            invoice.status = 'paid'
        else:
            invoice.status = 'unpaid'
            
        db.session.delete(payment)
        db.session.commit()
        return jsonify({'msg': 'Payment deleted'}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400 