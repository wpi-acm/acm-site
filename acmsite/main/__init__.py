from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route("/")
def homepage():
    return render_template("index.html")

@bp.route("/events")
def events():
    return render_template("events.html")

@bp.route("/join")
def join():
    return render_template("join.html")
