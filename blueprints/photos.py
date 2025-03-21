# blueprints/photos.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, lead_required
from models import db, Photo
from datetime import datetime
from flasgger import swag_from
from utils.swagger_docs import (
    PHOTOS_GET,
    PHOTOS_POST,
    PHOTOS_PHOTO_ID_PUT,
    PHOTOS_PHOTO_ID_DELETE)

photos_bp = Blueprint('photos', __name__)

def photo_to_dict(photo):
    return {
        'id': photo.id,
        'appointment_id': photo.appointment_id,
        'file_path': photo.file_path,
        'uploaded_by': photo.uploaded_by,
        'approved_by': photo.approved_by,
        'show_to_customer': photo.show_to_customer,
        'show_on_website': photo.show_on_website,
        'datetime': photo.datetime.isoformat()
    }

@photos_bp.route('/', methods=['GET'])
@swag_from(PHOTOS_GET)
@employee_required
def get_photos():
    photos = Photo.query.all()
    return jsonify([photo_to_dict(p) for p in photos]), 200

@photos_bp.route('/', methods=['POST'])
@swag_from(PHOTOS_POST)
@employee_required
def create_photo():
    data = request.get_json() or {}
    try:
        new_photo = Photo(
            appointment_id=data.get('appointment_id'),
            file_path=data.get('file_path'),
            uploaded_by=data.get('uploaded_by'),
            approved_by=data.get('approved_by'),
            show_to_customer=data.get('show_to_customer', False),
            show_on_website=data.get('show_on_website', False),
            datetime=datetime.now(datetime.UTC)
        )
        db.session.add(new_photo)
        db.session.commit()
        return jsonify(photo_to_dict(new_photo)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@photos_bp.route('/<int:photo_id>', methods=['PUT'])
@swag_from(PHOTOS_PHOTO_ID_PUT)
@lead_required
def update_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    data = request.get_json() or {}
    try:
        photo.approved_by = data.get('approved_by', photo.approved_by)
        photo.show_to_customer = data.get('show_to_customer', photo.show_to_customer)
        photo.show_on_website = data.get('show_on_website', photo.show_on_website)
        db.session.commit()
        return jsonify(photo_to_dict(photo)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@photos_bp.route('/<int:photo_id>', methods=['DELETE'])
@swag_from(PHOTOS_PHOTO_ID_DELETE)
@lead_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({'msg': 'Photo deleted'}), 200
