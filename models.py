from flask_login import UserMixin
from sqlalchemy import ForeignKey, orm

from a import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)
    count = db.Column(db.Integer)
    habit = db.Column(db.Integer, ForeignKey('habit.id'))


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    allday = db.Column(db.Integer)
    nowday = db.Column(db.Integer)
    data = db.Column(db.DateTime)
