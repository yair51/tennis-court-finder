from flask_login.mixins import UserMixin
from sqlalchemy.orm import backref
from . import db
from datetime import datetime
# from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    #profile = db.relationship('Profile', backref=db.backref('user'))

# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     graduation_year = db.Column(db.Integer)
#     interests = db.Column(db.String(150))
#     skills = db.Column(db.String(150))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Location(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(200))
     address = db.Column(db.String(150))
     city = db.Column(db.String(150))
     state = db.Column(db.String(150))
     zip_code = db.Column(db.Integer)
     court = db.relationship('Court', backref=db.backref('location'))
    #  country = db.Column(db.String(150))

class LocationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    court_status = db.relationship('CourtStatus', backref=db.backref('court'))
    # arduino_id ToDo

class CourtStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'))
