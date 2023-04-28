#!/usr/bin/python3
'''falsk framework'''

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
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
    app.run(host='0.0.0.0', port=5000, threaded=True)
