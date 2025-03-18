# blueprints/equipment.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, admin_required
from models import db, EquipmentCategory, Equipment, EquipmentAssignment, ConsumableUsage
from datetime import datetime, date

equipment_bp = Blueprint('equipment', __name__)

# --- Equipment Categories ---
def category_to_dict(cat):
    return {
        'id': cat.id,
        'name': cat.name
    }

@equipment_bp.route('/categories', methods=['GET'])
@employee_required
def get_categories():
    categories = EquipmentCategory.query.all()
    return jsonify([category_to_dict(cat) for cat in categories]), 200

@equipment_bp.route('/categories', methods=['POST'])
@admin_required
def create_category():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'Name is required'}), 400
    new_cat = EquipmentCategory(name=name)
    db.session.add(new_cat)
    db.session.commit()
    return jsonify(category_to_dict(new_cat)), 201

# --- Equipment ---
def equipment_to_dict(eq):
    return {
        'id': eq.id,
        'name': eq.name,
        'purchased_date': eq.purchased_date.isoformat() if eq.purchased_date else None,
        'purchased_condition': eq.purchased_condition,
        'warranty_expiration_date': eq.warranty_expiration_date.isoformat() if eq.warranty_expiration_date else None,
        'manufacturer': eq.manufacturer,
        'model': eq.model,
        'equipment_category_id': eq.equipment_category_id,
        'purchase_price': eq.purchase_price,
        'repair_cost_to_date': eq.repair_cost_to_date,
        'purchased_by': eq.purchased_by,
        'fuel_type': eq.fuel_type,
        'oil_type': eq.oil_type,
        'created_date': eq.created_date.isoformat()
    }

@equipment_bp.route('/', methods=['GET'])
@employee_required
def get_equipment():
    equipment = Equipment.query.all()
    return jsonify([equipment_to_dict(eq) for eq in equipment]), 200

@equipment_bp.route('/', methods=['POST'])
@admin_required
def create_equipment():
    data = request.get_json() or {}
    try:
        new_eq = Equipment(
            name=data['name'],
            purchased_date=date.fromisoformat(data['purchased_date']) if data.get('purchased_date') else None,
            purchased_condition=data.get('purchased_condition'),
            warranty_expiration_date=date.fromisoformat(data['warranty_expiration_date']) if data.get('warranty_expiration_date') else None,
            manufacturer=data.get('manufacturer'),
            model=data.get('model'),
            equipment_category_id=data.get('equipment_category_id'),
            purchase_price=float(data.get('purchase_price', 0)),
            repair_cost_to_date=float(data.get('repair_cost_to_date', 0)),
            purchased_by=data.get('purchased_by'),
            fuel_type=data.get('fuel_type'),
            oil_type=data.get('oil_type')
        )
    except Exception as e:
        return jsonify({'msg': 'Invalid input', 'error': str(e)}), 400
    db.session.add(new_eq)
    db.session.commit()
    return jsonify({'msg': 'Equipment created', 'equipment_id': new_eq.id}), 201

@equipment_bp.route('/<int:eq_id>', methods=['GET'])
@employee_required
def get_equipment_item(eq_id):
    eq = Equipment.query.get_or_404(eq_id)
    return jsonify(equipment_to_dict(eq)), 200

@equipment_bp.route('/<int:eq_id>', methods=['PUT'])
@admin_required
def update_equipment(eq_id):
    eq = Equipment.query.get_or_404(eq_id)
    data = request.get_json() or {}
    eq.name = data.get('name', eq.name)
    # (Add additional field updates as needed)
    db.session.commit()
    return jsonify({'msg': 'Equipment updated'}), 200

@equipment_bp.route('/<int:eq_id>', methods=['DELETE'])
@admin_required
def delete_equipment(eq_id):
    eq = Equipment.query.get_or_404(eq_id)
    db.session.delete(eq)
    db.session.commit()
    return jsonify({'msg': 'Equipment deleted'}), 200

# --- Equipment Assignments ---
def assignment_to_dict(assign):
    return {
        'id': assign.id,
        'equipment_id': assign.equipment_id,
        'team': assign.team,
        'assigned_date': assign.assigned_date.isoformat()
    }

@equipment_bp.route('/<int:eq_id>/assignments', methods=['GET'])
@employee_required
def get_assignments(eq_id):
    eq = Equipment.query.get_or_404(eq_id)
    return jsonify([assignment_to_dict(a) for a in eq.assignments]), 200

@equipment_bp.route('/<int:eq_id>/assignments', methods=['POST'])
@admin_required
def create_assignment(eq_id):
    Equipment.query.get_or_404(eq_id)  # Ensure equipment exists
    data = request.get_json() or {}
    new_assign = EquipmentAssignment(
        equipment_id=eq_id,
        team=data.get('team'),
        assigned_date=date.fromisoformat(data['assigned_date']) if data.get('assigned_date') else date.today()
    )
    db.session.add(new_assign)
    db.session.commit()
    return jsonify({'msg': 'Assignment created', 'assignment_id': new_assign.id}), 201

# --- Consumable Usage ---
def consumable_to_dict(c):
    return {
        'id': c.id,
        'equipment_id': c.equipment_id,
        'consumable_type': c.consumable_type,
        'amount_used': c.amount_used,
        'cost_per_liter': c.cost_per_liter,
        'date_recorded': c.date_recorded.isoformat()
    }

@equipment_bp.route('/<int:eq_id>/consumables', methods=['GET'])
@employee_required
def get_consumables(eq_id):
    eq = Equipment.query.get_or_404(eq_id)
    return jsonify([consumable_to_dict(c) for c in eq.consumables]), 200

@equipment_bp.route('/<int:eq_id>/consumables', methods=['POST'])
@admin_required
def create_consumable(eq_id):
    Equipment.query.get_or_404(eq_id)
    data = request.get_json() or {}
    try:
        new_consumable = ConsumableUsage(
            equipment_id=eq_id,
            consumable_type=data['consumable_type'],
            amount_used=float(data['amount_used']),
            cost_per_liter=float(data['cost_per_liter']),
            date_recorded=date.fromisoformat(data['date_recorded']) if data.get('date_recorded') else date.today()
        )
    except Exception as e:
        return jsonify({'msg': 'Invalid input', 'error': str(e)}), 400
    db.session.add(new_consumable)
    db.session.commit()
    return jsonify({'msg': 'Consumable usage recorded', 'consumable_id': new_consumable.id}), 201
