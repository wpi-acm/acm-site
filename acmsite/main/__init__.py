import datetime
from flask import Blueprint, current_app, render_template, abort, redirect, send_from_directory, send_file
from acmsite.models import Event, Link

bp = Blueprint('main', __name__)

@bp.route("/")
def homepage():
    return render_template("main/index.html")

@bp.route("/about")
def about():
    return render_template("main/about.html")

@bp.route("/officers")
def officers():
    return render_template("main/officers.html")

@bp.route("/what-we-do")
def activities():
    return render_template("main/how_we_help.html")

@bp.route("/events")
def events():
    events = Event.query.filter(Event.start_time > datetime.datetime.now()).all()
    return render_template("main/events.html", events=events)

@bp.route("/join")
def join():
    return render_template("join.html")

@bp.route("/officers/<path:username>")
def officer_images(username):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], username)


@bp.route("/<string:slug>")
def shortlink(slug):
    l = Link.query.filter_by(slug=slug).first()
    if l is None:
        abort(404)

    return redirect(l.destination)
