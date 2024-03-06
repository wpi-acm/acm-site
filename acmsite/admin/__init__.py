from flask import Blueprint, flash, redirect, render_template, request, url_for
import ulid
import datetime
from flask_login import current_user, login_required

from acmsite.models import User, Event

from .forms import EventForm
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


@bp.route("/events", methods=["GET","POST"])
@login_required
def events():
    if not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for('dashboard.home'))    

    event_list = Event.query.all()

    form = EventForm(request.form)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        start_day = request.form.get('start_day')
        start_time = request.form.get('start_time')
        end_day = request.form.get('end_day')
        end_time = request.form.get('end_time')
        print(start_day)
        print(start_time)

        start = datetime.datetime.combine(datetime.date.fromisoformat(start_day),
                                  datetime.time.fromisoformat(start_time)) 
        end = datetime.datetime.combine(datetime.date.fromisoformat(end_day),
                                  datetime.time.fromisoformat(end_time)) 

        e = Event(
                id=ulid.ulid(),
                name=name,
                description=description,
                location=location,
                start_time=start,
                end_time=end)
        db.session.add(e)
        db.session.commit()

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
