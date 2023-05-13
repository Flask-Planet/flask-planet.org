import os
import secrets

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import bigapp, db, logger

os.environ["CONFIG_SECRET_KEY"] = secrets.token_urlsafe(128)

load_dotenv()


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static",
        template_folder="templates",
    )
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    bigapp.init_app(app)
    db.init_app(app)
    logger.init_app(app)
    bigapp.import_models(from_folder="models")

    with app.app_context():
        db.create_all()

    if os.environ.get("FLASK_PLANET_DEV", None) is not None:
        bigapp.import_blueprints("blueprints")
    else:
        bigapp.import_blueprint("coming_soon")

    bigapp.import_theme("theme")

    @app.before_request
    def before_request():
        bigapp.init_session()

    bigapp.import_builtins()

    return app
