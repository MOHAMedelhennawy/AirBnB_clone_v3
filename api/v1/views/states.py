from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response

state = State()

@app_views.route('/states/', methods=['GET'])
def getAllStates():
    """Retrieves the list of all State objects"""
    all_state = [state.to_dict() for state in storage.all(State).values()]
    return all_state

@app_views.route('/states/<state_id>', methods=['GET'])
def getStateWithID(state_id):
    """Retrieves a State object with state_id"""
    key = State.__name__ + '.' + state_id
    all_states = storage.all(State)
    if key not in all_states.keys():
        abort(404)
    return storage.all(State)[key].to_dict()

@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleteState(state_id):
    """Deletes a State object with state_id"""
    all_states = storage.all(State)
    key = State.__name__ + '.' + state_id
    if key not in all_states.keys():
        abort(404)
    storage.delete(all_states[key])
    storage.save()
    return {}, 200

@app_views.route('/states/', methods=['POST'])
def createState():
    """Creates a new state"""
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    new_state = State(name=body.get('name'))
    new_state.save()
    return new_state.to_dict(), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def updateState(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return state.to_dict(), 200
