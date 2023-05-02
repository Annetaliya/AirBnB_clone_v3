#!/usr/bin/python3

"""Handles all restful actions for reviews"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models import storage
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews_by_place(place_id):
    """retrieve reviews based on place_id"""
    places = storage.get(Place, place_id)

    if places is None:
        abort(404)
    if request.method == 'GET':
        reviews_obj = [review.to_dict() for review in places.reviews]
        return jsonify(reviews_obj)
    elif request.method == 'POST':
        new_dict = request.get_json()
        user_obj = storage.get(User, new_dict.get('user_id'))

        if new_dict is None:
            abort(400, 'Not a JSON')
        if new_dict.get("user_id") is None:
            abort(400, 'Missing user_id')
        if new_dict.get("text") is None:
            abort(400, 'Missing text')
        if user_obj is None:
            abort(404)
        review_inst = Review(**new_dict)
        review_inst.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_by_review_id(review_id):
    """retrieves review by using review id"""
    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review_object.to_dict())
    if request.method == 'DELETE':
        storage.delete(review_object)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        review_dict = request.get_json()
        if review_dict is None:
            abort(400, 'Not a JSON')
        for k, v in review_dict.items():
            setattr(review_object, k, v)
        review.save()
        return jsonify(review_object.to_dict()), 200
