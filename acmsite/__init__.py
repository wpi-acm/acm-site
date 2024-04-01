from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_fontawesome import FontAwesome

from werkzeug.middleware.proxy_fix import ProxyFix

from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap5()
font_awesome = FontAwesome()
oauth = OAuth()

def create_app():
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    font_awesome.init_app(app)
    oauth.init_app(app)

    # register Microsoft Graph sign-in
    tenant = app.config["AZURE_TENANT_ID"]
    AZURE_CLIENT_ID = app.config["AZURE_CLIENT_ID"]
    oauth.register(
            name='azure',
            authorize_url=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize",
            access_token_url=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
            api_base_url="https://graph.microsoft.com/v1.0/",
            client_kwargs={"scope": "user.read"}
            )

    from .models import User
    
    # Ensure that uploads directory exists
    try:
        os.mkdir(app.config["UPLOAD_FOLDER"]) 
    except FileExistsError:
        pass

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .dashboard import bp as dash_bp
    app.register_blueprint(dash_bp)

    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)


    return app
