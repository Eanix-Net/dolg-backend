# blueprints/timelogs.py
from flask import Blueprint, request, jsonify
from models import db, TimeLog
from datetime import datetime
from blueprints.auth import employee_required

timelogs_bp = Blueprint('timelogs', __name__)

def timelog_to_dict(tl):
    return {
        'id': tl.id,
        'appointment_id': tl.appointment_id,
        'employee_id': tl.employee_id,
        'time_in': tl.time_in.isoformat(),
        'time_out': tl.time_out.isoformat() if tl.time_out else None,
        'total_time': tl.total_time
    }

@timelogs_bp.route('/', methods=['GET'])
@employee_required
def get_timelogs():
    logs = TimeLog.query.all()
    return jsonify([timelog_to_dict(log) for log in logs]), 200

@timelogs_bp.route('/', methods=['POST'])
@employee_required
def create_timelog():
    data = request.get_json() or {}
    try:
        new_log = TimeLog(
            appointment_id=data.get('appointment_id'),
            employee_id=data.get('employee_id'),
            time_in=datetime.fromisoformat(data['time_in'])
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify(timelog_to_dict(new_log)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@timelogs_bp.route('/<int:log_id>', methods=['PUT'])
@employee_required
def update_timelog(log_id):
    log = TimeLog.query.get_or_404(log_id)
    data = request.get_json() or {}
    try:
        if data.get('time_out'):
            log.time_out = datetime.fromisoformat(data['time_out'])
            # Calculate total time
            if log.time_in and log.time_out:
                log.total_time = (log.time_out - log.time_in).total_seconds() / 3600  # Convert to hours
        db.session.commit()
        return jsonify(timelog_to_dict(log)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@timelogs_bp.route('/<int:log_id>', methods=['DELETE'])
@employee_required
def delete_timelog(log_id):
    log = TimeLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'msg': 'Time log deleted'}), 200
