from flask import flash, redirect, url_for
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, null
import csv
from . import db
from . import login

class User(db.Model, UserMixin):
    __tablename__ = "acm_users"
    id = Column(String, primary_key=True)
    microsoft_id = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    def username(self):
        return self.email.split("@")[0]

def create_acm_csv(user_list):
    with open('acmsite/tmp/members.csv', 'w') as members_csv:
        header = ['last', 'first', 'email']
        writer = csv.DictWriter(members_csv, fieldnames=header)

        for u in user_list:
            writer.writerow({'last': u.last_name, 'first': u.first_name,
                             'email': u.email})

@login.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()

@login.unauthorized_handler
def unauth():
    flash("Please log in first!")
    return redirect("/")

class Officer(db.Model):
    __tablename__ = "acm_officers"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('acm_users.id'), nullable=False)
    term_start = Column(Date, nullable=False)
    term_end = Column(Date, nullable=True)
    position = Column(String, nullable=False)

    def create_json(self):
        return {
                "id": self.id,
                "user_id": self.user_id,
                "term_start": self.term_start,
                "term_end": self.term_end,
                "position": self.position
                }

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

    def create_json(self):
        return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "location": self.location,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
                }

class Link(db.Model):
    __tablename__ = "acm_links"
    id = Column(String, primary_key=True)
    slug = Column(String, nullable=False, unique=True)
    destination = Column(String, nullable=False)

    def create_json(self):
        return {
                "id": self.id,
                "slug": self.slug,
                "destination": self.destination
                }
