from marshmallow import ValidationError
from app.exeptions.location_update_failure import LocationUpdateFailureException
from app.models import Location
from app.schemas import LocationSchema
from kink import inject
from app import ClimbDb
from app.types import LocationPayload


@inject
class LocationUpdateHandler:

    def __init__(self, schema: LocationSchema, dp: ClimbDb):
        self.schema = schema
        self.db = dp

    def update_location(self, location: Location, payload: LocationPayload) -> Location:

        try:
            location = self.schema.load(payload, session=self.db.session, instance=location)
        except ValidationError as ex:
            raise LocationUpdateFailureException(ex)

        return location

    @staticmethod
    def save_updated_location(location: Location):
        location.save()
