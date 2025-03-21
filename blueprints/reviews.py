# blueprints/reviews.py
from flask import Blueprint, request, jsonify
from blueprints.auth import employee_required, admin_required
from models import db, Review
from datetime import datetime
from flasgger import swag_from
from utils.swagger_docs import (
    REVIEWS_GET,
    REVIEWS_POST,
    REVIEWS_REVIEW_ID_PUT,
    REVIEWS_REVIEW_ID_DELETE)

reviews_bp = Blueprint('reviews', __name__)

def review_to_dict(review):
    return {
        'id': review.id,
        'customer_id': review.customer_id,
        'location_id': review.location_id,
        'appointment_id': review.appointment_id,
        'rating': review.rating,
        'comment': review.comment,
        'datetime': review.datetime.isoformat()
    }

@reviews_bp.route('/', methods=['GET'])
@swag_from(REVIEWS_GET)
@employee_required
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review_to_dict(r) for r in reviews]), 200

@reviews_bp.route('/', methods=['POST'])
@swag_from(REVIEWS_POST)
@admin_required
def create_review():
    data = request.get_json() or {}
    try:
        new_review = Review(
            customer_id=data.get('customer_id'),
            location_id=data.get('location_id'),
            appointment_id=data.get('appointment_id'),
            rating=data.get('rating'),
            comment=data.get('comment'),
            datetime=datetime.now(datetime.UTC)
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify(review_to_dict(new_review)), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@swag_from(REVIEWS_REVIEW_ID_PUT)
@admin_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.get_json() or {}
    try:
        review.rating = data.get('rating', review.rating)
        review.comment = data.get('comment', review.comment)
        db.session.commit()
        return jsonify(review_to_dict(review)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@swag_from(REVIEWS_REVIEW_ID_DELETE)
@admin_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'msg': 'Review deleted'}), 200
