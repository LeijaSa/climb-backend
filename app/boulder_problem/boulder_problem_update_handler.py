from marshmallow import ValidationError
from app.exeptions.boulder_problem_update_failure import BoulderProblemUpdateFailureException
from app.models import BoulderProblem
from app.schemas import BoulderProblemSchema
from kink import inject
from app import ClimbDb
from app.types import BoulderProblemPayload


@inject
class BoulderProblemUpdateHandler:

    def __init__(self, schema: BoulderProblemSchema, dp: ClimbDb):
        self.schema = schema
        self.db = dp

    def update_boulder_problem(self, boulder_problem_model: BoulderProblem, payload: BoulderProblemPayload) -> (
            BoulderProblem):

        try:
            boulder_problem = self.schema.load(payload, session=self.db.session, instance=boulder_problem_model)

        except ValidationError as ex:
            raise BoulderProblemUpdateFailureException(ex)

        return boulder_problem

    @staticmethod
    def save_updated_boulder_problem(boulder_problem: BoulderProblem):
        boulder_problem.save()
