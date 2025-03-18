# blueprints/integrations.py
from flask import Blueprint, request, jsonify
from blueprints.auth import admin_required, api_key_required
import json

integrations_bp = Blueprint('integrations', __name__)

# In a full implementation you might store webhook URLs in a database.
# For this example we simply echo the event.

# Endpoint to register a webhook (stub implementation)
@integrations_bp.route('/register_webhook', methods=['POST'])
@admin_required
def register_webhook():
    data = request.get_json() or {}
    webhook_url = data.get('webhook_url')
    if not webhook_url:
        return jsonify({'msg': 'webhook_url is required'}), 400
    # In a real app, store the webhook URL with details (e.g., events of interest)
    return jsonify({'msg': 'Webhook registered', 'webhook_url': webhook_url}), 201

# Endpoint to receive a webhook event (from external systems)
@integrations_bp.route('/webhook', methods=['POST'])
@api_key_required
def receive_webhook():
    data = request.get_json() or {}
    # Log the received event; in production, verify signature/authentication
    print("Received webhook event:", json.dumps(data))
    # Process event (e.g., update appointment status, send notification)
    return jsonify({'msg': 'Webhook event received'}), 200

# Test endpoint to simulate sending an integration event from your system
@integrations_bp.route('/test_event', methods=['GET'])
@api_key_required
def test_event():
    # In a real system, you might trigger a webhook call here.
    sample_event = {
        'event': 'appointment.created',
        'data': {
            'appointment_id': 123,
            'customer_location_id': 45,
            'arrival_datetime': "2025-04-01T10:00:00",
            'departure_datetime': "2025-04-01T12:00:00"
        }
    }
    # For testing, simply return the sample event
    return jsonify(sample_event), 200
