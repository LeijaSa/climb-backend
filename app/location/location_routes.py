from flask import jsonify, request
from kink import di

from app import app, db
from app.exeptions.location_creation_failure import LocationCreationFailureException
from app.exeptions.location_not_found_exception import LocationNotFoundException
from app.exeptions.location_update_failure import LocationUpdateFailureException
from app.exeptions.request_data_not_found_exception import RequestDataNotFoundException
from app.location.location_creation_handler import LocationCreationHandler
from app.location.location_update_handler import LocationUpdateHandler
from app.models import Location, BoulderProblem
from app.schemas import LocationSchema
from app.types import LocationPayload


@app.errorhandler(LocationCreationFailureException)
def handle_boulder_problem_creation_failure(e):
    return jsonify({'error': {'message': 'Failed to create location:{}'.format(e)}}), 400


@app.errorhandler(LocationNotFoundException)
def handle_location_not_found(e):
    return jsonify({'error': {'message': 'Location not found'}}), 400


@app.errorhandler(LocationUpdateFailureException)
def handle_location_update_failure(e):
    return jsonify({'error': {'message': 'Failed to update location:{}'.format(e)}}), 400


@app.route('/locations', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()
    return jsonify(LocationSchema().dump(all_locations, many=True)), 200


@app.route('/location', methods=['POST'])
def create_location():
    payload: LocationPayload = request.get_json()
    if not payload:
        raise RequestDataNotFoundException()

    location: Location = di[LocationCreationHandler].create_new_location(payload)
    di[LocationCreationHandler].save_created_location(location)
    return jsonify(
        {'message': 'Location created', 'location': LocationSchema().dump(location)}), 200


@app.route('/location/<id>', methods=['PUT'])
def update_location(id: str):
    payload: LocationPayload = request.get_json()
    if not payload:
        raise RequestDataNotFoundException()

    location = db.session.get(Location, int(id))
    if not location:
        raise LocationNotFoundException()

    location = di[LocationUpdateHandler].update_location(location, payload)
    di[LocationUpdateHandler].save_updated_location(location)
    return jsonify(
        {'message': 'Location updated', 'location': LocationSchema().dump(location)}), 200


@app.route('/location/<id>', methods=['DELETE'])
def remove_location(id: str):
    location = Location.query.filter_by(id=int(id)).first()
    if not location:
        raise LocationNotFoundException()

    boulder_problems = BoulderProblem.query.filter_by(location_id=int(id))
    for problem in boulder_problems:
        problem.delete()

    location.delete()
    return jsonify({"status": "success", "message": "Location deleted"}), 200
