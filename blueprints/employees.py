# blueprints/employees.py
from flask import Blueprint, request, jsonify
from blueprints.auth import lead_required, admin_required
from models import db, Employee
from werkzeug.security import generate_password_hash
from flasgger import swag_from
from utils.swagger_docs import (
    EMPLOYEES_GET, get_detail_docs, get_update_docs, get_delete_docs, get_create_docs
)

employees_bp = Blueprint('employees', __name__)

def employee_to_dict(emp):
    return {
        'id': emp.id,
        'name': emp.name,
        'phone': emp.phone,
        'email': emp.email,
        'team': emp.team,
        'role': emp.role
    }

@employees_bp.route('/', methods=['GET'])
@lead_required
@swag_from(EMPLOYEES_GET)
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee_to_dict(emp) for emp in employees]), 200

@employees_bp.route('/', methods=['POST'])
@admin_required
@swag_from(get_create_docs(
    "Employees", "employee",
    {
        'name': {"type": "string", "example": "John Smith"},
        'phone': {"type": "string", "example": "555-123-4567"},
        'email': {"type": "string", "example": "john@example.com"},
        'password': {"type": "string", "example": "password123"},
        'team': {"type": "string", "example": "Installation"},
        'role': {"type": "string", "enum": ["admin", "lead", "employee"], "example": "employee"}
    },
    {
        'id': {"type": "integer"},
        'name': {"type": "string"},
        'phone': {"type": "string"},
        'email': {"type": "string"},
        'team': {"type": "string"},
        'role': {"type": "string", "enum": ["admin", "lead", "employee"]}
    }
))
def create_employee():
    data = request.get_json() or {}
    
    # Validate required fields
    if not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    if not data.get('password'):
        return jsonify({'error': 'Password is required'}), 400
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    # Check if email already exists
    if Employee.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    try:
        new_employee = Employee(
            name=data.get('name'),
            phone=data.get('phone', ''),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            team=data.get('team', ''),
            role=data.get('role', 'employee')
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify(employee_to_dict(new_employee)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@lead_required
@swag_from(get_detail_docs(
    "Employees", "employee", "employee_id", 
    {
        'id': {"type": "integer"},
        'name': {"type": "string"},
        'phone': {"type": "string"},
        'email': {"type": "string"},
        'team': {"type": "string"},
        'role': {"type": "string", "enum": ["admin", "lead", "employee"]}
    }
))
def get_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    return jsonify(employee_to_dict(emp)), 200

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
@admin_required
@swag_from(get_update_docs(
    "Employees", "employee", "employee_id",
    {
        'name': {"type": "string", "example": "John Smith"},
        'phone': {"type": "string", "example": "555-123-4567"},
        'email': {"type": "string", "example": "john@example.com"},
        'team': {"type": "string", "example": "Installation"},
        'role': {"type": "string", "enum": ["admin", "lead", "employee"], "example": "lead"},
        'password': {"type": "string", "example": "newpassword123"}
    },
    {
        'id': {"type": "integer"},
        'name': {"type": "string"},
        'phone': {"type": "string"},
        'email': {"type": "string"},
        'team': {"type": "string"},
        'role': {"type": "string", "enum": ["admin", "lead", "employee"]}
    }
))
def update_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    data = request.get_json() or {}
    emp.name = data.get('name', emp.name)
    emp.phone = data.get('phone', emp.phone)
    emp.email = data.get('email', emp.email)
    emp.team = data.get('team', emp.team)
    emp.role = data.get('role', emp.role)
    if data.get('password'):
        emp.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'msg': 'Employee updated successfully'}), 200

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
@admin_required
@swag_from(get_delete_docs("Employees", "employee", "employee_id"))
def delete_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'msg': 'Employee deleted'}), 200
