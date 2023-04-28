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
    if state_id is None:
        if request.method == 'GET':
            return jsonify(new_state)
        elif request.method == 'POST':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            if new_dict.get("name") is None:
                abort(400, 'Missing name')

