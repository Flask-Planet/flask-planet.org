import os
import secrets

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_bigapp import BigApp
from flask_sqlalchemy import SQLAlchemy

bigapp = BigApp()
db = SQLAlchemy()

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    bigapp.init_app(app)
    db.init_app(app)

    bigapp.import_blueprints("blueprints")
    bigapp.import_theme("theme")

    @app.before_request
    def before_request():
        bigapp.init_session()

    return app
