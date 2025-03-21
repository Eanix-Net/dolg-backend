# blueprints/customer_portal.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from flasgger import swag_from
from utils.swagger_docs import (
    CUSTOMER_PORTAL_REGISTER_POST,
    CUSTOMER_PORTAL_LOGIN_POST,
    CUSTOMER_PORTAL_PROFILE_GET,
    CUSTOMER_PORTAL_PROFILE_PUT,
    CUSTOMER_PORTAL_APPOINTMENTS_GET,
    CUSTOMER_PORTAL_INVOICES_GET,
    CUSTOMER_PORTAL_PHOTOS_GET,
    CUSTOMER_PORTAL_REVIEWS_POST,
    CUSTOMER_PORTAL_INVOICE_ID_GET)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Customer, CustomerLocation, Appointment, Invoice, Photo, Review
from datetime import timedelta, datetime
import re

customer_portal_bp = Blueprint('customer_portal', __name__)

# Helper: Serialize a customer object
def customer_to_dict(cust):
    return {
        'id': cust.id,
        'name': cust.name,
        'phone': cust.phone,
        'email': cust.email,
        'notes': cust.notes,
        'created_datetime': cust.created_datetime.isoformat() if cust.created_datetime else None
    }

# Simple email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ------------------------------------------
# Customer Registration (Separate from Employees)
# ------------------------------------------
@swag_from(CUSTOMER_PORTAL_REGISTER_POST)
@customer_portal_bp.route('/register', methods=['POST'])
def customer_register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')

    if not all([email, password, name]):
        return jsonify({'msg': 'Missing required fields'}), 400

    if not is_valid_email(email):
        return jsonify({'msg': 'Invalid email format'}), 400

    if Customer.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already registered'}), 400

    try:
        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({
            'msg': 'Customer registered successfully',
            'customer_id': new_customer.id
        }), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@swag_from(CUSTOMER_PORTAL_LOGIN_POST)
@customer_portal_bp.route('/login', methods=['POST'])
def customer_login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'Email and password required'}), 400

    customer = Customer.query.filter_by(email=email).first()
    if not customer or not check_password_hash(customer.password_hash, password):
        return jsonify({'msg': 'Invalid email or password'}), 401

    # Add a claim to distinguish customer tokens from employee tokens
    additional_claims = {"user_type": "customer"}
    access_token = create_access_token(
        identity=str(customer.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=12)
    )
    return jsonify({
        'access_token': access_token,
        'customer': {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }
    }), 200

def customer_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("user_type") != "customer":
            return jsonify({'msg': 'Unauthorized - customer token required'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@customer_portal_bp.route('/profile', methods=['GET'])
@swag_from(CUSTOMER_PORTAL_PROFILE_GET)
@customer_required
def get_customer_profile():
    customer_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(customer_id, str):
        customer_id = int(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer_to_dict(customer)), 200

@customer_portal_bp.route('/profile', methods=['PUT'])
@swag_from(CUSTOMER_PORTAL_PROFILE_PUT)
@customer_required
def update_customer_profile():
    customer_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(customer_id, str):
        customer_id = int(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    try:
        customer.name = data.get('name', customer.name)
        customer.phone = data.get('phone', customer.phone)
        if data.get('password'):
            customer.password_hash = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify(customer_to_dict(customer)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@customer_portal_bp.route('/appointments', methods=['GET'])
@swag_from(CUSTOMER_PORTAL_APPOINTMENTS_GET)
@customer_required
def get_customer_appointments():
    customer_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(customer_id, str):
        customer_id = int(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    appointments = []
    for location in customer.locations:
        appointments.extend(location.appointments)
    return jsonify([{
        'id': apt.id,
        'location_id': apt.customer_location_id,
        'arrival_datetime': apt.arrival_datetime.isoformat(),
        'departure_datetime': apt.departure_datetime.isoformat(),
        'team': apt.team
    } for apt in appointments]), 200

@customer_portal_bp.route('/invoices', methods=['GET'])
@swag_from(CUSTOMER_PORTAL_INVOICES_GET)
@customer_required
def get_customer_invoices():
    customer_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(customer_id, str):
        customer_id = int(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    invoices = []
    for location in customer.locations:
        for appointment in location.appointments:
            invoices.extend(appointment.invoices)
    return jsonify([{
        'id': inv.id,
        'appointment_id': inv.appointment_id,
        'subtotal': inv.subtotal,
        'total': inv.total,
        'tax_rate': inv.tax_rate,
        'paid': inv.paid,
        'due_date': inv.due_date.isoformat(),
        'created_date': inv.created_date.isoformat()
    } for inv in invoices]), 200

@customer_portal_bp.route('/photos', methods=['GET'])
@swag_from(CUSTOMER_PORTAL_PHOTOS_GET)
@customer_required
def get_customer_photos():
    customer_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(customer_id, str):
        customer_id = int(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    photos = []
    for location in customer.locations:
        for appointment in location.appointments:
            photos.extend(appointment.photos)
    return jsonify([{
        'id': photo.id,
        'appointment_id': photo.appointment_id,
        'file_path': photo.file_path,
        'datetime': photo.datetime.isoformat()
    } for photo in photos if photo.show_to_customer]), 200

@customer_portal_bp.route('/reviews', methods=['POST'])
@swag_from(CUSTOMER_PORTAL_REVIEWS_POST)
@customer_required
def submit_review():
    customer_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(customer_id, str):
        customer_id = int(customer_id)
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    try:
        new_review = Review(
            customer_id=customer_id,
            location_id=data.get('location_id'),
            appointment_id=data.get('appointment_id'),
            rating=data.get('rating'),
            comment=data.get('comment'),
            datetime=datetime.now(datetime.UTC)
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'msg': 'Review submitted successfully'}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@customer_portal_bp.route('/payment/<int:invoice_id>', methods=['GET'])
@swag_from(CUSTOMER_PORTAL_INVOICE_ID_GET)
@customer_required
def initiate_payment(invoice_id):
    # In a real integration, call the payment provider (e.g., Stripe) to create a payment session.
    return jsonify({'msg': 'Payment integration not implemented'}), 501
