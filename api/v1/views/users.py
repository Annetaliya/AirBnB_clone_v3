#!/usr/bin/python3
'''objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def user_by_id(user_id=None):
    '''Retrieves the list of all users objects'''
    userObj = storage.all(User)

    new_user = [obj.to_dict() for obj in userObj.values()]
    if not user_id:
        if request.method == 'GET':
            return jsonify(new_user)
        elif request.method == 'POST':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            if new_dict.get("email") is None:
                abort(400, 'Missing email')
            users = User(**new_dict)
            users.save()
            return jsonify(users.to_dict()), 201
    else:
        if request.method == 'GET':
            for user in new_user:
                if user.get('id') == user_id:
                    return jsonify(user)
            abort(404)

        elif request.method == 'PUT':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            for user in userObj.values():
                if user.id == user_id:
                    user.name = new_dict.get("name")
                    user.save()
                    return jsonify(user.to_dict()), 200
            abort(404)

        elif request.method == 'DELETE':
            for obj in userObj.values():
                if obj.id == user_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
