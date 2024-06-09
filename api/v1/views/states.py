from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

state = State()


@app_views.route('/states/', methods=['GET'])
def getAllStates():
    all_state = [ state.to_dict() for state in storage.all(State).values() ]
    return all_state

@app_views.route('/states/<state_id>', methods=['GET'])
def getStateWithID(state_id):
    key = State.__name__ + '.' + state_id
    all_states = storage.all(State)
    if key not in all_states.keys():
        abort(404)
    return storage.all(State)[key].to_dict()

@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleteState(state_id):
    all_states = storage.all(State)
    key = State.__name__ + '.' + state_id
    state = all_states[key]
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return '', 200

@app_views.route('/states/', methods=['POST'])
def createState():
    body = request.get_json()
    if not body:
        abort(400, message='Not a JSON')
    if 'name' not in body:
        abort(400, message='Missing name')
    new_state = State(name=body['name'])
    new_state.save()
    return new_state.to_dict(), 201