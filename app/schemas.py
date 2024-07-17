from typing import Any

from flask import jsonify, Response
from marshmallow import ValidationError, fields

from app.di.injectable import injectable
from app.models import BoulderProblem, Location
from app import ma


class SchemaDumb(object):

    def dump(self, obj: Any, many: bool = None) -> dict | Response:
        try:
            return super(ma.SQLAlchemyAutoSchema, self).dump(obj, many=many)
        except ValidationError as ex:
            response = {
                "status": "error",
                "message": "Validation failed",
                "errors": ex.messages
            }
            return jsonify(response)


@injectable
class BoulderProblemSchema(SchemaDumb, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BoulderProblem
        include_relationships = True
        load_instance = True
        add_date = fields.Date(format='%d-%m-%Y')
        fields = ('id', 'description', 'grade', 'state', 'add_date', 'location_id')


@injectable
class LocationSchema(SchemaDumb, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_relationships = True
        load_instance = True
