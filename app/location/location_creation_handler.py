from marshmallow import ValidationError
from app.exeptions.location_creation_failure import LocationCreationFailureException
from app.models import Location
from app.schemas import LocationSchema
from kink import inject
from app import ClimbDb


@inject
class LocationCreationHandler:

    def __init__(self, schema: LocationSchema, dp: ClimbDb):
        self.schema = schema
        self.db = dp

    def create_new_location(self, payload) -> Location:

        try:
            location = self.schema.load(payload, session=self.db.session, instance=None)
        except ValidationError as ex:
            raise LocationCreationFailureException(ex)

        return location

    @staticmethod
    def save_created_location(location: Location):
        location.save()
