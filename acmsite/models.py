from flask import flash, redirect, url_for
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, null
from . import db
from . import login

class User(db.Model, UserMixin):
    __tablename__ = "acm_users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)

@login.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()

@login.unauthorized_handler
def unauth():
    flash("Please log in first!")
    return redirect("/")

class PwResetRequest(db.Model):
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('acm_users.id'), nullable=False)
    expires = Column(DateTime, nullable=False)

class Event(db.Model):
    __tablename__ = "acm_events"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=False)
    start_time=Column(DateTime, nullable=False)
    end_time=Column(DateTime, nullable=False)
