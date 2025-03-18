# blueprints/appointments.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Appointment, RecurringAppointment, CustomerLocation
from datetime import datetime, date

appointments_bp = Blueprint('appointments', __name__)

# Helper functions to serialize model objects

def appointment_to_dict(appointment):
    return {
        'id': appointment.id,
        'customer_location_id': appointment.customer_location_id,
        'arrival_datetime': appointment.arrival_datetime.isoformat(),
        'departure_datetime': appointment.departure_datetime.isoformat(),
        'team': appointment.team
    }

def recurring_appointment_to_dict(recurring):
    return {
        'id': recurring.id,
        'customer_location_id': recurring.customer_location_id,
        'start_date': recurring.start_date.isoformat(),
        'schedule': recurring.schedule,
        'team': recurring.team
    }

# ----------------------------
# One-Time Appointment Endpoints
# ----------------------------

@appointments_bp.route('/', methods=['GET'])
@employee_required
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment_to_dict(app) for app in appointments]), 200

@appointments_bp.route('/', methods=['POST'])
@lead_required
def create_appointment():
    data = request.get_json() or {}
    try:
        customer_location_id = data['customer_location_id']
        arrival_datetime = datetime.fromisoformat(data['arrival_datetime'])
        departure_datetime = datetime.fromisoformat(data['departure_datetime'])
    except Exception:
        return jsonify({'msg': 'Invalid input or missing required fields'}), 400
    
    # Validate that the provided customer location exists.
    location = CustomerLocation.query.get(customer_location_id)
    if not location:
        return jsonify({'msg': 'Customer location not found'}), 404

    new_appointment = Appointment(
        customer_location_id=customer_location_id,
        arrival_datetime=arrival_datetime,
        departure_datetime=departure_datetime,
        team=data.get('team')
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'msg': 'Appointment created', 'appointment_id': new_appointment.id}), 201

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@employee_required
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify(appointment_to_dict(appointment)), 200

@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
@lead_required
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json() or {}
    if 'customer_location_id' in data:
        appointment.customer_location_id = data['customer_location_id']
    if 'arrival_datetime' in data:
        appointment.arrival_datetime = datetime.fromisoformat(data['arrival_datetime'])
    if 'departure_datetime' in data:
        appointment.departure_datetime = datetime.fromisoformat(data['departure_datetime'])
    if 'team' in data:
        appointment.team = data['team']
    db.session.commit()
    return jsonify({'msg': 'Appointment updated'}), 200

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
@admin_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'msg': 'Appointment deleted'}), 200

# ----------------------------
# Recurring Appointment Endpoints
# ----------------------------

@appointments_bp.route('/recurring', methods=['GET'])
@employee_required
def get_recurring_appointments():
    recurring_apps = RecurringAppointment.query.all()
    return jsonify([recurring_appointment_to_dict(r) for r in recurring_apps]), 200

@appointments_bp.route('/recurring', methods=['POST'])
@lead_required
def create_recurring_appointment():
    data = request.get_json() or {}
    try:
        customer_location_id = data['customer_location_id']
        start_date = date.fromisoformat(data['start_date'])
        schedule = data['schedule']
    except Exception:
        return jsonify({'msg': 'Invalid input or missing required fields'}), 400

    # Validate that the provided customer location exists.
    location = CustomerLocation.query.get(customer_location_id)
    if not location:
        return jsonify({'msg': 'Customer location not found'}), 404

    new_recurring = RecurringAppointment(
        customer_location_id=customer_location_id,
        start_date=start_date,
        schedule=schedule,
        team=data.get('team')
    )
    db.session.add(new_recurring)
    db.session.commit()
    return jsonify({'msg': 'Recurring appointment created', 'recurring_id': new_recurring.id}), 201

@appointments_bp.route('/recurring/<int:recurring_id>', methods=['GET'])
@employee_required
def get_recurring_appointment(recurring_id):
    recurring = RecurringAppointment.query.get_or_404(recurring_id)
    return jsonify(recurring_appointment_to_dict(recurring)), 200

@appointments_bp.route('/recurring/<int:recurring_id>', methods=['PUT'])
@lead_required
def update_recurring_appointment(recurring_id):
    recurring = RecurringAppointment.query.get_or_404(recurring_id)
    data = request.get_json() or {}
    if 'customer_location_id' in data:
        recurring.customer_location_id = data['customer_location_id']
    if 'start_date' in data:
        recurring.start_date = date.fromisoformat(data['start_date'])
    if 'schedule' in data:
        recurring.schedule = data['schedule']
    if 'team' in data:
        recurring.team = data['team']
    db.session.commit()
    return jsonify({'msg': 'Recurring appointment updated'}), 200

@appointments_bp.route('/recurring/<int:recurring_id>', methods=['DELETE'])
@lead_required
def delete_recurring_appointment(recurring_id):
    recurring = RecurringAppointment.query.get_or_404(recurring_id)
    db.session.delete(recurring)
    db.session.commit()
    return jsonify({'msg': 'Recurring appointment deleted'}), 200
