#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions
"""
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAllAmenities():
    """Retrieves the list of all amenities objects"""
    all_amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(all_amenities)

@app_views.route('amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def getِAmenityWithID(amenity_id):
    """Retrieves a amenities object with amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)

@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def deleteAmenity(amenity_id):
    """Deletes a amenity object with amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenty():
    """Creates a new amenity"""
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, {'error': 'Not a JSON'})
    if 'name' not in data:
        abort(400, {'error': 'Missing name'})
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def updateAmenity(amenity_id):
    """Updates a amenity object based on amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    print(amenity)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict) or not data:
        abort(400, {'error': 'Not a JSON'})
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
