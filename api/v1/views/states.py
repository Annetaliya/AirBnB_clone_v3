#!/usr/bin/python3
'''objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def states(state_id=None):
    '''Retrieves the list of all State objects'''
    statesObj = storage.all(State)

    new_state = [obj.to_dict() for obj in statesObj.values()]
    if not state_id:
        if request.method == 'GET':
            return jsonify(new_state)
        elif request.method == 'POST':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            if new_dict.get("name") is None:
                abort(400, 'Missing name')
            created_state = State(**new_dict)
            created_state.save()
            return jsonify(created_state.to_dict()), 201
    else:
        if request.method == 'GET':
            for state in new_state:
                if state.get('id') == state_id:
                    return jsonify(state)
            abort(404)

        elif request.method == 'PUT':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            for state in statesObj.values():
                if state.id == state_id:
                    state.name = new_dict.get("name")
                    state.save()
                    return jsonify(state.to_dict()), 200
            abort(404)

        elif request.method == 'DELETE':
            for obj in statesObj.values():
                if obj.id == state_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
