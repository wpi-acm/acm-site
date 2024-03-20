import datetime
from flask import Blueprint, render_template
from acmsite.models import Event

bp = Blueprint('main', __name__)

@bp.route("/")
def homepage():
    return render_template("index.html")

@bp.route("/events")
def events():
    events = Event.query.filter(Event.start_time > datetime.datetime.now()).all()
    return render_template("events.html", events=events)

@bp.route("/join")
def join():
    return render_template("join.html")
