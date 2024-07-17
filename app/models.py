from datetime import datetime

from app import db
from app.base import CRUDMixin


class BoulderProblem(CRUDMixin, db.Model):
    __tablename__ = 'boulder_problem'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(550), nullable=False)
    grade = db.Column(db.String(5), nullable=False)
    state = db.Column(db.String(15), nullable=False)
    add_date = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', back_populates='boulder_problems')


class Location(CRUDMixin, db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(40), nullable=False)

    boulder_problems = db.relationship('BoulderProblem', back_populates='location')
