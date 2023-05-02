#!/usr/bin/python3
"""restful API functions for Place reviews"""

from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
def places_end_points(place_id):
    """RESTFul API actions for places review"""
    places = storage.all(Place)
    places_objects = [obj.to_dict() for obj in places.values()]
    if request.method == "GET":
        for obj in places_objects:
            if obj.get('id') == place_id:
                place_reviews = storage.all(Review)
                reviews_objects = [obj.to_dict() for obj in
                                   places_reviews.values() if
                                   obj.place_id == place_id]
                return jsonify(reviews_objects)
        abort(404)

    elif request.method == "POST":
        for obj in places_objects:
            if obj.get('id') == place_id:
                new_dict = request.get_json()
                if not new_dict or type(new_dict) is not dict:
                    abort(400, "Not a JSON")
                if not new_dict["name"]:
                    abort(400, "Missing name")
                if not new_dict.get('user_id'):
                    abort(400, "Missing user_id")
                if not new_dict.get('text'):
                    abort(400, "Missing text")
                user_obj = storage.all(User).values()
                user_exists = False
                for user_obj in user_objs:
                    if user_obj.id == new_dict["user_id"]:
                        user_exists = True
                        break
                if not user_exists:
                    abort(404)
                else:
                    new_dict["place_id"] = place_id
                    new_review = Review(**new_dict)
                    new_review.save()
                    return jsonify(new_review.to_dict()), 201
        abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def review_end_points(review_id):
    """place objects that handles all default RESTFul API actions"""
    review_dict = storage.get(Review, review_id)
    if not review_dict:
        abort(404)

    if request.method == "GET":
        return jsonify(review_dict.to_dict())
    elif request.method == "DELETE":
        storage.delete(review_dict)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        new_name = request.get_json()
        if not new_name or type(new_name) is not dict:
            abort(400, "Not a JSON")
        review_dict.__dict__.update(new_name)
        review_dict.save()
        return jsonify(review_dict.to_dict()), 201
