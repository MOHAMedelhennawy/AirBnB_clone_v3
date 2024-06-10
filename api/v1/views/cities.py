#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions
"""
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response

state = State()


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def getCitiesOfState(state_id):
    """Retrieves all cities of state with id == state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'])
def getCityWithID(city_id):
    """Retrieves a City object with id == city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city.to_dict()

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deleteCityWithID(city_id):
    """Deletes a City object with id == city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createCity(state_id):
    """Creates a new City"""
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    new_city = City(name=body.get('name'), state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def updateCity(city_id):
    """Updates a City object based on city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
