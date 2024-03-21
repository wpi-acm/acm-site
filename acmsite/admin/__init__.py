from flask import Blueprint, flash, redirect, render_template, request, url_for
import ulid
import datetime
from flask_login import current_user, login_required

from acmsite.models import Link, User, Event

from .forms import EventForm, LinkForm
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

    return render_template("admin/users.html", u_list=user_list)


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
