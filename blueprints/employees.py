# blueprints/employees.py
from flask import Blueprint, request, jsonify
from blueprints.auth import lead_required, admin_required
from models import db, Employee
from werkzeug.security import generate_password_hash

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
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee_to_dict(emp) for emp in employees]), 200

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@lead_required
def get_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    return jsonify(employee_to_dict(emp)), 200

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
@admin_required
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
def delete_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'msg': 'Employee deleted'}), 200
