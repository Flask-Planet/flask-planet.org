import os
import secrets

from flask import Flask

from flask_bigapp import BigApp

bigapp = BigApp()

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app)

    bigapp.import_blueprint("frontend")
    bigapp.import_theme("theme")

    @app.before_request
    def before_request():
        bigapp.init_session()

    return app
