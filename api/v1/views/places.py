#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_place_by_cityId(city_id):
    if request.method == 'GET':
        city_object = storage.get(City, city_id)
        if city:
            for places in city.places():
                return jsonify(places.to_dict())
        abort(404)
    elif request.method == 'POST':
        city = storage.get(City, city_id)

        if city:
            user_dict = request.get_json()
            if not user_dict:
                abort(400, 'Not a JSON')
            if not user_dict.get('user_id'):
                abort(400, 'Missing user_id')
            if not user_dict.get('name'):
                abort(400, 'Missing name')

            user = storage.get(User, user_dict.get('user_id'))
            if not user:
                abort(404)
            else:
                place = Place(**new_dict)
                place.save()
                return jsonify(place.to_dict()), 201
        abort(404)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_place_by_place_id(place_id):
    '''Gets place based on the place_id'''
    place = storage.get(Place, place_id)

    if place is not None:
        if request.method == 'GET':
            return jsonify(place.to_dict())
        if request.method == 'PUT':
            new_dict = request.get_json()
            if not new_dict:
                abort(400, 'Not a JSON')
            for key, value in new_dict.items():
                setattr(place, key, value)
        if request.method == 'DELETE':
            place.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)
