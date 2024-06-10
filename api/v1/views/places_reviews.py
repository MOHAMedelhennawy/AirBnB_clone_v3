#!/usr/bin/python3
"""new view for Review objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models import storage
from models.user import User


@app_views.route(
        'places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def getAllReviews(place_id):
    """retrieves all reviews for a certain place"""
    place = storage.get(Place, place_id)
    if place:
        all_reviews = [place.to_dict() for place in place.reviews]
        if all_reviews is []:
            abort(404)
        return jsonify(all_reviews)
    else:
        abort(404)


@app_views.route(
        "reviews/<review_id>", methods=['GET'], strict_slashes=False)
def getReview(review_id):
    """retrieves a review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route(
        "reviews/<review_id>", methods=['DELETE'], strict_slashes=False)
def deleteReview(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "places/<place_id>/reviews", methods=['POST'], strict_slashes=False)
def createReview(place_id):
    """create a review"""
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, {'error': 'Not a JSON'})
        if 'user_id' not in data.keys():
            abort(400, {'error': 'Missing user_id'})
        elif "text" not in data.keys():
            abort(400, {'error': 'Missing user_id'})
        else:
            user = storage.get(User, content['user_id'])
            if user:
                review = Review(**data)
                review.place_id = place_id
                storage.new(review)
                storage.save()
                return jsonify(review.to_dict()), 201
            else:
                abort(404)
    else:
        abort(404)


@app_views.route(
        'reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """update review"""
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if not isinstance(data, dict) or not data:
            abort(400, {'error': 'Not a JSON'})
        ignore_key = ['id', 'created_at', 'updated_at', 'used_id', 'place_id']
        for key, value in data.items():
            if key not in ignore_key:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
