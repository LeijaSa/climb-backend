from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from kink import di

app = Flask(__name__)
app.config.from_object('config.Config')


class ClimbDb(SQLAlchemy):
    pass


db = ClimbDb(app)
ma = Marshmallow(app)
di[ClimbDb] = db

from app import models, schemas
from app.boulder_problem import boulder_routes
from app.location import location_routes
from app.base import CRUDMixin
