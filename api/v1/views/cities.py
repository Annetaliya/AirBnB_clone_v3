#!/usr/bin/python3

'''retrivieng city by city id and state id'''

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def city_state(state_id):
    '''A method that Retrieves the list of all City objects of a State'''
    state_obj = storage.all(State)
    states = [obj for obj in state_obj.values()]

    if request.method == 'GET':
        for state in states:
            if state.id == state_id:
                cities_obj = storage.all(City)
                cities = [objects.to_dict() for objects in
                          cities_obj.values() if objects.state_id == state_id]
                return jsonify(cities)
        abort(404)

    elif request.method == 'POST':
        for state in states:
            if state.id == state_id:
                new_dict = request.get_json()
                if new_dict is None:
                    abort(400, 'Not a JSON')
                if new_dict.get('name') is None:
                    abort(400, 'Missing name')
                new_dict['state_id'] = state_id
                city = City(**new_dict)
                city.save()
                return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city_by_cityid(city_id):
    '''Retrieves a City object by its id'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        new_dict = request.get_json()
        if new_dict is None:
            abort(400, 'Not a JSON')
        city.name = new_dict.get('name')
        city.save()
        return jsonify(city.to_dict()), 200
