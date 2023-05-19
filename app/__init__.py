from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import bigapp, db, logger


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
    bigapp.import_builtins()
    bigapp.import_blueprints("blueprints")
    bigapp.import_theme("theme")

    with app.app_context():
        db.create_all()

    @app.before_request
    def before_request():
        bigapp.init_session()

    return app
