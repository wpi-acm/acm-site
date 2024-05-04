from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from acmsite.dashboard.forms import PasswordForm
from acmsite import db


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route("/")
@login_required
def home():
    form = PasswordForm()
    return render_template('dashboard.html', form=form)

@bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    form = PasswordForm(request.form)

    if form.validate_on_submit():
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        password_confirm = request.form.get("password_confirm")

        if new_password == password_confirm:
            if current_password == '' and current_user.password == '':
                current_user.password = generate_password_hash(new_password)
                flash("Password set successfully.")
            elif check_password_hash(current_user.password, current_password):
                current_user.password = generate_password_hash(new_password)
                flash("Password updated successfully.")
            else:
                flash("Incorrect password.")
        else:
            flash("Passwords do not match!")
        db.session.commit()
        return redirect(url_for("dashboard.home"))
