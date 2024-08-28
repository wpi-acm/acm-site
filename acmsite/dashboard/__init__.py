
from datetime import datetime
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from ulid import ulid

from acmsite.models import Event, EventCheckin
from acmsite import db


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route("/")
@login_required
def home():
    now = datetime.now()
    events = db.session.execute(db.select(Event).where(Event.start_time < now,
                                                       Event.end_time >
                                                       now)).scalars()
    return render_template('dashboard.html', events=events)

@bp.route("/checkin/<string:event_id>")
@login_required
def checkin(event_id):
    # actually first check if the event even exists
    event = db.get_or_404(Event, event_id)
    # first check if this user has already checked in
    checkins = db.session.execute(db.select(EventCheckin).where(EventCheckin.user ==
                                                     current_user.id,
                                                     EventCheckin.event
                                                                ==event_id)).scalar_one_or_none()

    current_app.logger.debug(checkins)
    if checkins is None:
        # There's not a checkin already, let's create one!
        check = EventCheckin(
                id = ulid(),
                user = current_user.id,
                event = event_id)
        db.session.add(check)
        db.session.commit()

        flash(f"Checked in to {event.name} successfully")
        return redirect(url_for("dashboard.home"))
    else:
        flash(f"You've already checked in to {event.name}")
        return redirect(url_for("dashboard.home"))
