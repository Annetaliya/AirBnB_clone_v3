#!/usr/bin/python3
'''file that jsonify our input'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def convert():
    ''' returns a string in json format'''

    return jsonify({"status": "OK"})
