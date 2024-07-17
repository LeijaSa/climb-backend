from typing import Tuple
from flask import jsonify, request, Response
from kink import di

from app import app, db
from app.boulder_problem.boulder_problem_creation_handler import BoulderProblemCreationHandler
from app.boulder_problem.boulder_problem_update_handler import BoulderProblemUpdateHandler
from app.exeptions.boulder_problem_creation_failure import BoulderProblemCreationFailureException
from app.exeptions.boulder_problem_not_found_exception import BoulderProblemNotFoundException
from app.exeptions.boulder_problem_update_failure import BoulderProblemUpdateFailureException
from app.exeptions.request_data_not_found_exception import RequestDataNotFoundException
from app.models import BoulderProblem
from app.schemas import BoulderProblemSchema
from app.types import BoulderProblemPayload


@app.errorhandler(RequestDataNotFoundException)
def handle_request_data_not_found(e):
    return jsonify({'error': {'message': 'No request data provided'}}), 400


@app.errorhandler(BoulderProblemCreationFailureException)
def handle_boulder_problem_creation_failure(e):
    return jsonify({'error': {'message': 'Failed to create boulder problem:{}'.format(e)}}), 400


@app.errorhandler(BoulderProblemNotFoundException)
def handle_boulder_problem_not_found(e):
    return jsonify({'error': {'message': 'Boulder problem not found'}}), 400


@app.errorhandler(BoulderProblemUpdateFailureException)
def handle_boulder_problem_update_failure(e):
    return jsonify({'error': {'message': 'Failed to update boulder problem:{}'.format(e)}}), 400


@app.route('/boulders', methods=['GET'])
def get_boulder_problems() -> Tuple[Response, int]:
    query = BoulderProblem.query

    grade: str | None = request.args.get('grade')
    state: str | None = request.args.get('state')
    location_id: str | None = request.args.get('location_id')

    if grade:
        query = query.filter(BoulderProblem.grade == grade)
    if state:
        query = query.filter(BoulderProblem.state == state)
    if location_id:
        query = query.filter(BoulderProblem.location_id == int(location_id))

    all_boulder_problems = query.all()

    data = BoulderProblemSchema().dump(all_boulder_problems, many=True)
    return jsonify(data), 200


@app.route('/boulder', methods=['POST'])
def create_boulder_problem():
    payload: BoulderProblemPayload = request.get_json()
    if not payload:
        RequestDataNotFoundException()

    boulder_problem = di[BoulderProblemCreationHandler].create_new_boulder_problem(payload)
    di[BoulderProblemCreationHandler].save_created_boulder_problem(boulder_problem)
    return jsonify(
        {'message': 'Boulder problem created', 'boulder problem': BoulderProblemSchema().dump(boulder_problem)}), 200


@app.route('/boulder/<id>', methods=['PUT'])
def update_boulder_problem(id: str):
    payload: BoulderProblemPayload = request.get_json()
    if not payload:
        RequestDataNotFoundException()

    boulder_problem = db.session.get(BoulderProblem, int(id))
    if not boulder_problem:
        raise BoulderProblemNotFoundException()

    boulder_problem = di[BoulderProblemUpdateHandler].update_boulder_problem(boulder_problem, payload)
    di[BoulderProblemUpdateHandler].save_updated_boulder_problem(boulder_problem)
    return jsonify(
        {'message': 'Boulder problem updated', 'boulder problem': BoulderProblemSchema().dump(boulder_problem)}), 200


@app.route('/boulder/<id>', methods=['DELETE'])
def remove_boulder_problem(id: str):
    boulder_problem = BoulderProblem.query.filter_by(id=int(id)).first()
    if not boulder_problem:
        raise BoulderProblemNotFoundException()

    boulder_problem.delete()
    return jsonify({"status": "success", "message": "Boulder problem deleted"}), 200
