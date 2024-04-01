from os.path import exists
from flask import Blueprint, jsonify, url_for, current_app
import os
import datetime

from acmsite.models import Event, Officer, User

bp = Blueprint("api", __name__, url_prefix="/api")


def json(obj):
    """
    Calls a "create_json" method on the passed in object. Write it yourself!
    """
    return obj.create_json()

@bp.route("/events/upcoming")
def upcoming_events():
    event_list = Event.query.filter(Event.start_time >
                                    datetime.datetime.now()).all()
    
    return jsonify(list(map(json, event_list)))

@bp.route("/officers/current")
def current_officers():
    now = datetime.datetime.now()
    officers = Officer.query.filter(Officer.term_start < now, Officer.term_end >
                                    now).all()

    officers_complete = []
    for o in officers:
        u = User.query.filter_by(id = o.user_id).first()
        if u is None:
            continue # Broken reference, continue
        img = url_for('static', filename="img/officers/placeholder.png")
        if exists(f"acmsite/{current_app.config['UPLOAD_FOLDER']}/{u.username()}.png"):
            img = url_for("main.officer_images", username="f{u.username()}.png")
        officers_complete.append({
                "id": o.id,
                "position": o.position,
                "term_end": o.term_end,
                "term_start": o.term_start,
                "name": u.first_name + " " + u.last_name,
                "img": img
            }) 


    return jsonify(list(officers_complete))
