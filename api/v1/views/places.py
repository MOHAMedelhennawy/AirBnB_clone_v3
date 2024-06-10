#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions
"""
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.place import Place


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def getAllPlaces(city_id):
    """Retrieves all places"""
    city = storage.get(City, city_id)
    all_places = [place.to_dict() for place in city.places]
    if all_places is []:
        abort(404)
    return jsonify(all_places)


@app_views.route(
        "/places/<place_id>", methods=['GET'], strict_slashes=False)
def getPlaceWithID(place_id):
    """Retrieves place with id == place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        "/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def deletePlaceWithID(place_id):
    """Delete place with id == place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def createPlace(city_id):
    """Create new Place linked to city with id == city_id"""
    data = request.get_json()

    if not isinstance(data, dict):
        abort(400, {'error': 'Not a JSON'})

    city = storage.get(City, city_id)
    if city is None:
        abort(404, {'error', 'city not found'})

    if 'user_id' not in data:
        abort(400, {'error': 'Missing user_id'})

    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404, {'error', 'user not found'})
        # abort(404)

    if 'name' not in data:
        abort(400, {'error': 'Missing name'})

    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route(
        '/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """Update place with id == place_id"""
    user = storage.get(Place, place_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict) or not data:
        abort(400, {'error': 'Not a JSON'})
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
