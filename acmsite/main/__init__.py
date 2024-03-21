import datetime
from flask import Blueprint, render_template, abort, redirect
from acmsite.models import Event, Link

bp = Blueprint('main', __name__)

@bp.route("/")
def homepage():
    return render_template("index.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/events")
def events():
    events = Event.query.filter(Event.start_time > datetime.datetime.now()).all()
    return render_template("events.html", events=events)

@bp.route("/join")
def join():
    return render_template("join.html")


@bp.route("/<string:slug>")
def shortlink(slug):
    l = Link.query.filter_by(slug=slug).first()
    if l is None:
        abort(404)

    return redirect(l.destination)
