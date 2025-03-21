# blueprints/auth.py
from flask import Blueprint, request, jsonify
from models import db, Employee, Customer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt, verify_jwt_in_request,
    get_jwt_identity, create_refresh_token, get_current_user
)
from datetime import timedelta
import os
from flasgger import swag_from
from utils.swagger_docs import AUTH_LOGIN
from functools import wraps
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@swag_from(AUTH_LOGIN)
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'msg': 'Email and password required'}), 400

    employee = Employee.query.filter_by(email=email).first()
    
    if not employee:
        return jsonify({'msg': 'Bad email' + str(employee)}), 401
    if not check_password_hash(employee.password_hash, password):
        return jsonify({'msg': 'Bad password' + str(employee)}), 401

    # Add a claim to distinguish employee tokens from customer tokens.
    additional_claims = {"user_type": "employee", "user_role": employee.role}
    access_token = create_access_token(
        identity=str(employee.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=12)
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(
        identity=str(employee.id),
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': employee.id,
            'name': employee.name,
            'email': employee.email,
            'role': employee.role
        }
    }), 200

@auth_bp.route('/customer/login', methods=['POST'])
def customer_login():
    """
    Customer Login Endpoint
    ---
    tags:
      - Authentication
    description: Login with customer credentials
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: customer@example.com
            password:
              type: string
              example: password123
          required:
            - email
            - password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
      400:
        description: Email and password required
      401:
        description: Invalid email or password
    """
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'msg': 'Email and password required'}), 400
        
    customer = Customer.query.filter_by(email=email).first()
    
    if not customer:
        return jsonify({'msg': 'Invalid email'}), 401
    if not customer.password_hash or not check_password_hash(customer.password_hash, password):
        return jsonify({'msg': 'Invalid password'}), 401
        
    # Add claim for customer
    additional_claims = {"user_type": "customer"}
    access_token = create_access_token(
        identity=str(customer.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=12)
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(
        identity=str(customer.id),
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh Token Endpoint
    ---
    tags:
      - Authentication
    description: Refresh access token using refresh token
    security:
      - Bearer: []
    responses:
      200:
        description: Token refreshed successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Invalid refresh token
    """
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    # Get the user type and role from the claims
    user_type = claims.get("user_type")
    user_role = claims.get("user_role", "")
    
    additional_claims = {"user_type": user_type}
    additional_claims["user_role"] = user_role
    
    access_token = create_access_token(
        identity=current_user,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=12)
    )
    
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/register', methods=['POST'])
def register_employee():
    """
    Register New Employee Endpoint
    ---
    tags:
      - Authentication
    description: Register a new employee (admin only)
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: employee@example.com
            password:
              type: string
              example: password123
            phone:
              type: string
              example: "5551234567"
            team:
              type: string
              example: "Team A"
            role:
              type: string
              enum: [admin, lead, employee]
              example: employee
          required:
            - name
            - email
            - password
            - role
    responses:
      201:
        description: Employee created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
            role:
              type: string
      400:
        description: Invalid input data
      409:
        description: Email already exists
    """
    data = request.get_json() or {}
    
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'msg': f'Missing required field: {field}'}), 400
    
    # Check if email already exists
    if Employee.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already registered'}), 409
    
    # Validate role
    valid_roles = ['admin', 'lead', 'employee']
    if data['role'] not in valid_roles:
        return jsonify({'msg': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
    
    # Create new employee
    new_employee = Employee(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        phone=data.get('phone', ''),
        team=data.get('team', '')
    )
    
    # Set password
    new_employee.set_password(data['password'])
    
    # Save to database
    db.session.add(new_employee)
    db.session.commit()
    
    return jsonify({
        'id': new_employee.id,
        'name': new_employee.name,
        'email': new_employee.email,
        'role': new_employee.role
    }), 201

@auth_bp.route('/password/change', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change Password Endpoint
    ---
    tags:
      - Authentication
    description: Change user password
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            current_password:
              type: string
              example: oldpassword123
            new_password:
              type: string
              example: newpassword456
          required:
            - current_password
            - new_password
    responses:
      200:
        description: Password changed successfully
        schema:
          type: object
          properties:
            msg:
              type: string
              example: Password updated successfully
      400:
        description: Invalid input data
      401:
        description: Current password is incorrect
    """
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    claims = get_jwt()
    user_type = claims.get("user_type")
    
    # Check required fields
    if 'current_password' not in data or 'new_password' not in data:
        return jsonify({'msg': 'Current password and new password required'}), 400
    
    if user_type == "employee":
        user = Employee.query.get(user_id)
    else:  # customer
        user = Customer.query.get(user_id)
    
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    # Verify current password
    if not check_password_hash(user.password_hash, data['current_password']):
        return jsonify({'msg': 'Current password is incorrect'}), 401
    
    # Update password
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'msg': 'Password updated successfully'}), 200

def employee_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") != "employee":
            return jsonify({'msg': 'Unauthorized - employee token required'}), 403
        if not (claims.get("user_role") == "admin" or claims.get("user_role") == "lead" or claims.get("user_role") == "employee"):
            return jsonify({'msg': 'Unauthorized - admin, lead, or employee token required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def lead_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") != "employee":
            return jsonify({'msg': 'Unauthorized - employee token required'}), 403
        if not (claims.get("user_role") == "admin" or claims.get("user_role") == "lead"):
            return jsonify({'msg': 'Unauthorized - admin, lead, or employee token required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") != "employee":
            return jsonify({'msg': 'Unauthorized - employee token required'}), 403
        if not (claims.get("user_role") == "admin"):
            return jsonify({'msg': 'Unauthorized - admin, lead, or employee token required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def api_key_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if os.getenv('API_KEY') != request.headers.get('X-API-KEY'):
            return jsonify({'msg': 'Unauthorized - Invalid API Key'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def customer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") != "customer":
            return jsonify({'msg': 'Unauthorized - customer token required'}), 403
        return fn(*args, **kwargs)
    return wrapper