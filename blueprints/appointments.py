# blueprints/appointments.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required, admin_required
from models import db, Appointment, RecurringAppointment, CustomerLocation, Customer, Employee
from datetime import datetime, date
from flasgger import swag_from
from utils.swagger_docs import (
    APPOINTMENTS_GET, get_detail_docs, get_create_docs, get_update_docs, get_delete_docs
)

appointments_bp = Blueprint('appointments', __name__)

# Helper functions to serialize model objects

def appointment_to_dict(appointment):
    if not appointment:
        return None
    
    # Get start and end times consistently
    start_time = appointment.arrival_datetime
    end_time = appointment.departure_datetime
    if hasattr(appointment, 'start_time') and callable(getattr(appointment, 'start_time')):
        start_time = appointment.start_time
    if hasattr(appointment, 'end_time') and callable(getattr(appointment, 'end_time')):
        end_time = appointment.end_time
    
    result = {
        'id': appointment.id,
        'customer_id': appointment.customer_id,
        'employee_id': appointment.employee_id,
        'location_id': appointment.customer_location_id,
        'description': appointment.description,
        'start_time': start_time.isoformat() if start_time else None,
        'end_time': end_time.isoformat() if end_time else None,
        'status': appointment.status,
        'notes': appointment.notes,
        'created_datetime': appointment.created_datetime.isoformat() if appointment.created_datetime else None,
        # Add test-specific field names for compatibility
        'scheduled_start_datetime': start_time.isoformat() if start_time else None,
        'scheduled_end_datetime': end_time.isoformat() if end_time else None,
        'service_type': appointment.description
    }
    return result

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
@swag_from(APPOINTMENTS_GET)
def get_appointments():
    # Get query parameters
    customer_id = request.args.get('customer_id', type=int)
    employee_id = request.args.get('employee_id', type=int)
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build query
    query = Appointment.query
    
    if customer_id:
        query = query.filter(Appointment.customer_id == customer_id)
    if employee_id:
        query = query.filter(Appointment.employee_id == employee_id)
    if status:
        query = query.filter(Appointment.status == status)
    if start_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            query = query.filter(Appointment.start_time >= start_date)
        except ValueError:
            return jsonify({'msg': 'Invalid start_date format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    if end_date:
        try:
            end_date = datetime.fromisoformat(end_date)
            query = query.filter(Appointment.start_time <= end_date)
        except ValueError:
            return jsonify({'msg': 'Invalid end_date format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    appointments = query.all()
    return jsonify([appointment_to_dict(appt) for appt in appointments]), 200

@appointments_bp.route('/', methods=['POST'])
@lead_required
@swag_from(get_create_docs(
    "Appointments", "appointment",
    {
        'customer_id': {"type": "integer", "example": 1},
        'employee_id': {"type": "integer", "example": 2},
        'location_id': {"type": "integer", "example": 3},
        'description': {"type": "string", "example": "Lawn Mowing"},
        'start_time': {"type": "string", "format": "date-time", "example": "2023-05-15T09:00:00"},
        'end_time': {"type": "string", "format": "date-time", "example": "2023-05-15T12:00:00"},
        'status': {"type": "string", "enum": ["scheduled", "in_progress", "completed", "cancelled"], "example": "scheduled"},
        'notes': {"type": "string", "example": "Customer requested service in the morning"}
    },
    {
        'id': {"type": "integer"},
        'customer_id': {"type": "integer"},
        'employee_id': {"type": "integer"},
        'location_id': {"type": "integer"},
        'description': {"type": "string"},
        'start_time': {"type": "string", "format": "date-time"},
        'end_time': {"type": "string", "format": "date-time"},
        'status': {"type": "string"},
        'notes': {"type": "string"},
        'created_datetime': {"type": "string", "format": "date-time"}
    }
))
def create_appointment():
    data = request.get_json() or {}
    
    # Validate required fields
    required_fields = ['customer_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if customer exists
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # Check if location exists if provided
    if data.get('location_id'):
        location = CustomerLocation.query.get(data['location_id'])
        if not location:
            return jsonify({'error': 'Location not found'}), 404
    
    # Check if employee exists if provided
    if data.get('employee_id'):
        employee = Employee.query.get(data['employee_id'])
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
    
    # Parse dates - handle both field naming conventions
    try:
        # First try the API test field names
        if data.get('scheduled_start_datetime'):
            start_time = datetime.fromisoformat(data['scheduled_start_datetime'])
        else:
            # Then try the implementation field names
            start_time = datetime.fromisoformat(data['start_time']) if data.get('start_time') else None
            
        if data.get('scheduled_end_datetime'):
            end_time = datetime.fromisoformat(data['scheduled_end_datetime'])
        else:
            end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None
    except ValueError:
        return jsonify({'error': 'Invalid date format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if not start_time:
        return jsonify({'error': 'Start time is required'}), 400
    
    # Get description from either field
    description = data.get('service_type') or data.get('description')
    
    try:
        # Create new appointment
        new_appointment = Appointment(
            customer_id=data['customer_id'],
            employee_id=data.get('employee_id'),
            location_id=data.get('location_id'),
            description=description,
            start_time=start_time,
            end_time=end_time,
            status=data.get('status', 'scheduled'),
            notes=data.get('notes')
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify(appointment_to_dict(new_appointment)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@employee_required
@swag_from(get_detail_docs(
    "Appointments", "appointment", "appointment_id",
    {
        'id': {"type": "integer"},
        'customer_id': {"type": "integer"},
        'customer_name': {"type": "string"},
        'employee_id': {"type": "integer"},
        'employee_name': {"type": "string"},
        'location_id': {"type": "integer"},
        'location_address': {"type": "string"},
        'description': {"type": "string"},
        'start_time': {"type": "string", "format": "date-time"},
        'end_time': {"type": "string", "format": "date-time"},
        'status': {"type": "string"},
        'notes': {"type": "string"},
        'created_datetime': {"type": "string", "format": "date-time"}
    }
))
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    response_data = appointment_to_dict(appointment)
    
    # Add additional fields for the response if needed
    if appointment.customer_id:
        customer = Customer.query.get(appointment.customer_id)
        if customer:
            response_data['customer_name'] = customer.name
            
    if appointment.employee_id:
        employee = Employee.query.get(appointment.employee_id)
        if employee:
            response_data['employee_name'] = employee.name
            
    if appointment.location_id:
        location = CustomerLocation.query.get(appointment.location_id)
        if location:
            response_data['location_address'] = location.address
            
    # Add additional mappings for test compatibility
    if 'start_time' in response_data:
        response_data['scheduled_start_datetime'] = response_data['start_time']
    if 'end_time' in response_data:
        response_data['scheduled_end_datetime'] = response_data['end_time']
    if 'description' in response_data:
        response_data['service_type'] = response_data['description']
    
    return jsonify(response_data), 200

@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
@lead_required
@swag_from(get_update_docs(
    "Appointments", "appointment", "appointment_id",
    {
        'customer_id': {"type": "integer", "example": 1},
        'employee_id': {"type": "integer", "example": 2},
        'location_id': {"type": "integer", "example": 3},
        'description': {"type": "string", "example": "HVAC Maintenance"},
        'start_time': {"type": "string", "format": "date-time", "example": "2023-05-16T10:00:00"},
        'end_time': {"type": "string", "format": "date-time", "example": "2023-05-16T13:00:00"},
        'status': {"type": "string", "enum": ["scheduled", "in_progress", "completed", "cancelled"], "example": "completed"},
        'notes': {"type": "string", "example": "Maintenance completed successfully"}
    },
    {
        'id': {"type": "integer"},
        'customer_id': {"type": "integer"},
        'customer_name': {"type": "string"},
        'employee_id': {"type": "integer"},
        'employee_name': {"type": "string"},
        'location_id': {"type": "integer"},
        'location_address': {"type": "string"},
        'description': {"type": "string"},
        'start_time': {"type": "string", "format": "date-time"},
        'end_time': {"type": "string", "format": "date-time"},
        'status': {"type": "string"},
        'notes': {"type": "string"},
        'created_datetime': {"type": "string", "format": "date-time"}
    }
))
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json() or {}
    
    # Update fields
    if 'customer_id' in data:
        appointment.customer_id = data['customer_id']
    if 'employee_id' in data:
        appointment.employee_id = data['employee_id']
    if 'location_id' in data:
        appointment.location_id = data['location_id']
    
    # Handle description from either field name
    if 'description' in data:
        appointment.description = data['description']
    elif 'service_type' in data:
        appointment.description = data['service_type']
    
    # Handle start time from either field name
    if 'start_time' in data:
        try:
            appointment.start_time = datetime.fromisoformat(data['start_time'])
        except ValueError:
            return jsonify({'msg': 'Invalid start_time format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    elif 'scheduled_start_datetime' in data:
        try:
            appointment.start_time = datetime.fromisoformat(data['scheduled_start_datetime'])
        except ValueError:
            return jsonify({'msg': 'Invalid scheduled_start_datetime format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Handle end time from either field name
    if 'end_time' in data:
        try:
            appointment.end_time = datetime.fromisoformat(data['end_time']) if data['end_time'] else None
        except ValueError:
            return jsonify({'msg': 'Invalid end_time format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    elif 'scheduled_end_datetime' in data:
        try:
            appointment.end_time = datetime.fromisoformat(data['scheduled_end_datetime']) if data['scheduled_end_datetime'] else None
        except ValueError:
            return jsonify({'msg': 'Invalid scheduled_end_datetime format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if 'status' in data:
        appointment.status = data['status']
    if 'notes' in data:
        appointment.notes = data['notes']
    
    db.session.commit()
    
    # Return with the same format as get_appointment for consistency
    return get_appointment(appointment_id)

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
@lead_required
@swag_from(get_delete_docs("Appointments", "appointment", "appointment_id"))
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

@appointments_bp.route('/available-employees', methods=['GET'])
@employee_required
def get_available_employees():
    """
    Get Available Employees for an Appointment Time Range
    ---
    tags:
      - Appointments
    parameters:
      - name: start_time
        in: query
        type: string
        format: date-time
        required: true
        description: Start time for the appointment in ISO format
      - name: end_time
        in: query
        type: string
        format: date-time
        required: true
        description: End time for the appointment in ISO format
    responses:
      200:
        description: List of available employees
        schema:
          type: array
          items:
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
        description: Invalid request parameters
      401:
        description: Unauthorized
      403:
        description: Forbidden - Insufficient permissions
    security:
      - Bearer: []
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not start_time or not end_time:
        return jsonify({'msg': 'Missing required parameters: start_time and end_time'}), 400
    
    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({'msg': 'Invalid date format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Find employees who don't have conflicting appointments
    busy_employee_ids = db.session.query(Appointment.employee_id).filter(
        Appointment.employee_id.isnot(None),
        Appointment.status != 'cancelled',
        db.or_(
            db.and_(Appointment.start_time >= start, Appointment.start_time < end),
            db.and_(Appointment.end_time > start, Appointment.end_time <= end),
            db.and_(Appointment.start_time <= start, Appointment.end_time >= end)
        )
    ).distinct().all()
    
    busy_ids = [id[0] for id in busy_employee_ids]
    
    available_employees = Employee.query.filter(~Employee.id.in_(busy_ids) if busy_ids else True).all()
    
    result = [{
        'id': emp.id,
        'name': emp.name,
        'email': emp.email,
        'role': emp.role
    } for emp in available_employees]
    
    return jsonify(result), 200
