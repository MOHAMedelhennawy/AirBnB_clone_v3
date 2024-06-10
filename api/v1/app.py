#!/usr/bin/python3
"""
app instantiation
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(e):
    """ close the storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Custom 404 error page """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
