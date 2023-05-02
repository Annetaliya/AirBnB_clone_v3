#!/usr/bin/python3
'''falsk framework'''

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(exception=None):
    '''eliminate session'''
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    '''handling 404 error'''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True, debug=True)
