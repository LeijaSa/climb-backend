from marshmallow import ValidationError

from app.exeptions.boulder_problem_creation_failure import BoulderProblemCreationFailureException
from app.models import BoulderProblem
from app.schemas import BoulderProblemSchema
from kink import inject
from app import ClimbDb


@inject
class BoulderProblemCreationHandler:

    def __init__(self, schema: BoulderProblemSchema, dp: ClimbDb):
        self.schema = schema
        self.db = dp

    def create_new_boulder_problem(self, payload) -> BoulderProblem:

        try:
            boulder_problem = self.schema.load(payload, session=self.db.session, instance=None)

        except ValidationError as ex:
            raise BoulderProblemCreationFailureException(ex)

        return boulder_problem

    @staticmethod
    def save_created_boulder_problem(boulder_problem: BoulderProblem):
        boulder_problem.save()
