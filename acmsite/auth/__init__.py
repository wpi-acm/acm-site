import datetime
from flask import Blueprint, redirect, render_template, url_for
import ulid
import flask_login

from acmsite.models import User
from acmsite import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

from acmsite import oauth


@bp.route('/login')
def login():
    return oauth.azure.authorize_redirect(url_for('auth.oauth2_callback',
                                                  _external=True))

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route("/oauth2")
def oauth2_callback():
    token = oauth.azure.authorize_access_token()
    resp = oauth.azure.get('me')
    resp.raise_for_status()
    profile = resp.json()
    print(profile)
    u = User.query.filter_by(microsoft_id=profile['id']).first()
    if u is None:
        u = User(
            id=ulid.ulid(),
            microsoft_id=profile['id'],
            password='',
            email=profile['mail'],
            first_name=profile['givenName'],
            last_name=profile['surname'],
            created=datetime.datetime.now(),
            last_login=datetime.datetime.now()
            )
        db.session.add(u)
        db.session.commit()
    else:
        # Returning user
        u.last_login = datetime.datetime.now()
        db.session.commit()
    flask_login.login_user(u)
    return redirect('/')

@bp.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('main.homepage'))
