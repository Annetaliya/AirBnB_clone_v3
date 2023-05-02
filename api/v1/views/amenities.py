#!/usr/bin/python3
'''objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def amenity(amenity_id=None):
    '''Retrieves the list of all amenity objects'''
    amenityObj = storage.all(Amenity)

    new_amenity = [obj.to_dict() for obj in amenityObj.values()]
    if not amenity_id:
        if request.method == 'GET':
            return jsonify(new_amenity)
        elif request.method == 'POST':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            if new_dict.get("name") is None:
                abort(400, 'Missing name')
            amenities = Amenity(**new_dict)
            amenities.save()
            return jsonify(amenities.to_dict()), 201
    else:
        if request.method == 'GET':
            for amenity in new_amenity:
                if amenity.get('id') == amenity_id:
                    return jsonify(amenity)
            abort(404)

        elif request.method == 'PUT':
            new_dict = request.get_json()

            if new_dict is None:
                abort(400, 'Not a JSON')
            for state in amenityObj.values():
                if amenity.id == amenity_id:
                    amenity.name = new_dict.get("name")
                    amenity.save()
                    return jsonify(amenity.to_dict()), 200
            abort(404)

        elif request.method == 'DELETE':
            for obj in amenityObj.values():
                if obj.id == amenity_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
