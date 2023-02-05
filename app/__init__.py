import logging
import os
import secrets

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import bigapp, db

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)


class Sprinkles:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()

if os.environ.get("FLASK_DEBUG"):
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)

formatter = logging.Formatter(f'{Sprinkles.OKGREEN}::RUNNING APP::{Sprinkles.END} - {Sprinkles.OKCYAN}%(message)s{Sprinkles.END}')
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    bigapp.init_app(app)
    bigapp.import_models(from_folder="models")
    db.init_app(app)

    bigapp.import_blueprints("blueprints")
    bigapp.import_theme("theme")

    @app.before_request
    def before_request():
        bigapp.init_session()

    return app
