#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions
"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from werkzeug.exceptions import BadRequest

state = State()


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def getAllStates():
    """Retrieves the list of all State objects"""
    all_state = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getStateWithID(state_id):
    """Retrieves a State object with state_id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deleteState(state_id):
    """Deletes a State object with state_id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def createState():
    """Creates a new state"""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, {'error': 'Not a JSON'})
        if 'name' not in data:
            abort(400, {'error': 'Missing name'})
        new_state = State(**data)
        storage.new(new_state)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    except BadRequest:
        abort(400, {'error': 'Not a JSON'})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    """Updates a State object based on state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict) or not data:
        abort(400, {'error': 'Not a JSON'})
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
