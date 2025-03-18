# blueprints/auth.py
from flask import Blueprint, request, jsonify
from models import db, Employee
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import timedelta
import os
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
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
        identity=employee.id,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=12)
    )
    return jsonify({'access_token': access_token}), 200

def employee_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("user_type") != "employee":
            return jsonify({'msg': 'Unauthorized - employee token required'}), 403
        if not (claims.get("user_role") == "admin" or claims.get("user_role") == "lead" or claims.get("user_role") == "employee"):
            return jsonify({'msg': 'Unauthorized - admin, lead, or employee token required'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
def lead_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("user_type") != "employee":
            return jsonify({'msg': 'Unauthorized - employee token required'}), 403
        if not (claims.get("user_role") == "admin" or claims.get("user_role") == "lead"):
            return jsonify({'msg': 'Unauthorized - admin, lead, or employee token required'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("user_type") != "employee":
            return jsonify({'msg': 'Unauthorized - employee token required'}), 403
        if not (claims.get("user_role") == "admin"):
            return jsonify({'msg': 'Unauthorized - admin, lead, or employee token required'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def api_key_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        if os.getenv('API_KEY') != request.headers.get('X-API-KEY'):
            return jsonify({'msg': 'Unauthorized - Invalid API Key'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper