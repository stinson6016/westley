from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime

class Users(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(110))
    active = db.Column(db.String(1), default='y')
    admin = db.Column(db.String(1), default='n')
    date_added = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)

class Pictures(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    desc = db.Column(db.String(80))
    name = db.Column(db.String(100))
    folder = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.now)
    userid = db.Column(db.String(36), db.ForeignKey('users.id'))
    user = relationship("Users", primaryjoin="Pictures.userid==Users.id")

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dbversion = db.Column(db.String(20))
    sitename = db.Column(db.String(20))
    signup = db.Column(db.String(1))