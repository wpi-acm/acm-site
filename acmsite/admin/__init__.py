from operator import pos
import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_file, url_for
import ulid
import datetime
from flask_login import current_user, login_required
from io import BytesIO
from PIL import Image
import base64

from acmsite.models import Link, Officer, User, Event
from acmsite import models

from .forms import EventForm, LinkForm, OfficerForm
from acmsite import db


bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/")
@login_required
def home():
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for('dashboard.home'))
    return render_template("admin/index.html")

@bp.route("/users")
@login_required
def users():
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for('dashboard.home'))

    user_list = User.query.all()

    position_form = OfficerForm(request.form)

    return render_template("admin/users.html", u_list=user_list,
                           form=position_form)

@bp.route("/users/toggle_admin/<string:user_id>")
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        return error_json("Unauthorized")

    u = User.query.filter_by(id=user_id).first()
    if u is None:
        return error_json("Invalid user")

    u.is_admin = not u.is_admin
    db.session.commit()
    return success_json()

@bp.route("/users.csv")
@login_required
def users_csv():
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for('dashboard.home'))

    user_list = User.query.all()

    models.create_acm_csv(user_list)

    return send_file('./tmp/members.csv')

@bp.route("/events")
@login_required
def events():
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for('dashboard.home'))    

    event_list = Event.query.all()

    form = EventForm(request.form)
    return render_template("admin/events.html", e_list=event_list, form=form)

@bp.route("/event/<string:id>")
@login_required
def event(id):
    if not current_user.is_admin:
        return {"status": "error", "message": "Unauthorized"}
    
    event = Event.query.filter_by(id=id).first()

    if event is None:
        return {"status": "error", "message": "Invalid event ID"}

    return event.create_json()


@bp.route("/event/<string:id>/delete")
@login_required
def delete_event(id):
    if not current_user.is_admin:
        return {"status": "error", "message": "Unauthorized"}
    
    event = Event.query.filter_by(id=id).first()

    if event is None:
        return {"status": "error", "message": "Invalid event ID"}

    db.session.delete(event)
    db.session.commit()

    return {"status": "success"}

@bp.route("/event/<string:id>", methods=["POST"])
@login_required
def update_create_event(id):
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for("dashboard.home"))

    name = request.form.get('name')
    description = request.form.get('description')
    location = request.form.get('location')
    start_day = request.form.get('start_day')
    start_time = request.form.get('start_time')
    end_day = request.form.get('end_day')
    end_time = request.form.get('end_time')
    start = datetime.datetime.combine(datetime.date.fromisoformat(start_day),
                              datetime.time.fromisoformat(start_time)) 
    end = datetime.datetime.combine(datetime.date.fromisoformat(end_day),
                                  datetime.time.fromisoformat(end_time)) 

    if id == '0':
        # new event
        e = Event(
                id=ulid.ulid(),
                name=name,
                description=description,
                location=location,
                start_time=start,
                end_time=end)
        db.session.add(e)
        db.session.commit()
    else:
        e = Event.query.filter_by(id=id).first()
        if e is None:
            return {"status": "error", "message": "Invalid event ID"}
        e.name = name
        e.description = description
        e.location = location
        e.start_time = start
        e.end_time = end
        db.session.commit()


    return redirect(url_for("admin.events"))

@bp.route("/links")
@login_required
def links():
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for("dashboard.home"))

    links = Link.query.all()
    form = LinkForm(request.form)

    return render_template("admin/links.html", links=links, form=form)

@bp.route("/link/<string:id>")
@login_required
def link(id):
    if not current_user.is_admin:
        return {"status": "error", "message": "Unauthorized"}

    link = Link.query.filter_by(id=id).first()

    if link is None:
        return {"status": "error", "message": "Invalid ID"}

    return link.create_json()

@bp.route("/link/<string:id>", methods=["POST"])
@login_required
def update_create_link(id):
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for("dashboard.home"))

    slug = request.form.get('slug')
    destination = request.form.get('destination')

    if id == '0':
        # new link
        l = Link(
                id=ulid.ulid(),
                slug=slug,
                destination=destination)
        db.session.add(l)
        db.session.commit()
    else:
        l = Link.query.filter_by(id=id).first()
        if l is None:
            flash("Invalid ID")
            return redirect(url_for("admin.links"))
        l.slug = slug
        l.destination = destination
        db.session.commit()

    return redirect(url_for("admin.links"))

def error_json(message):
    return {"status": "error", "message": message}

def success_json():
    return {"status": "success"}

@bp.route("/officer/<string:user_id>")
@login_required
def officer_positions(user_id):
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for("dashboard.home"))

    form = OfficerForm(request.form)

    position_list = Officer.query.filter_by(user_id=user_id).order_by(Officer.term_end).all()

    return render_template("admin/officers.html", form=form,
                           position_list=position_list, user_id=user_id)

@bp.route("/officer/get/<string:pos_id>")
@login_required
def get_position(pos_id):
    if not current_user.is_admin:
        return error_json("Unauthorized")

    pos = Officer.query.filter_by(id=pos_id).first()

    if pos is None:
        return error_json("Invalid ID")

    return pos.create_json()


@bp.route("/officer/new/<string:user_id>", methods=["POST"])
@login_required
def create_officer(user_id):
    if not current_user.is_admin:
        error_json("Unauthorized")

    form = OfficerForm(request.form)

    if form.validate_on_submit:
        position = request.form.get("position")
        term_end = request.form.get("term_end")
        term_start = request.form.get("term_start")

        position = Officer(
                id=ulid.ulid(),
                user_id=user_id,
                position=position,
                term_start=term_start,
                term_end=term_end)

        db.session.add(position)
        db.session.commit()

    return redirect(url_for("admin.officer_positions", user_id=user_id))

@bp.route("/officer/update/<string:user_id>/<string:officer_id>", methods=["POST"])
@login_required
def update_officer(user_id, officer_id):
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for('dashboard.home'))

    form = OfficerForm(request.form)

    if form.validate_on_submit:
        officer = Officer.query.filter_by(id=officer_id).first()
        if officer is None:
            flash("Invalid ID")
            return redirect(url_for('admin.officer_positions', user_id=user_id))

        officer.position = request.form.get("position")
        officer.term_start = request.form.get("term_start")
        officer.term_end = request.form.get("term_end")

        db.session.commit()

    return redirect(url_for('admin.officer_positions', user_id=user_id))

@bp.route("/officer/photo")
@login_required
def upload_photo():
    if not current_user.is_admin:
        return error_json("Unauthorized")

    return render_template("admin/officer_photo.html")

@bp.route("/officer/photo/upload", methods=["POST"])
@login_required
def upload_photo_post():
    if not current_user.is_admin:
        return error_json("Unauthorized")    

    img_path = os.path.join("acmsite/" + current_app.config["UPLOAD_FOLDER"], f"{current_user.username()}.png")
    b64_string = request.data.decode()
    b64_string += '=' * (len(b64_string) % 4)

    im = Image.open(BytesIO(base64.b64decode(b64_string.split(',')[1])))
    im.save(img_path, format="PNG")    
    return success_json()
