from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_nested_blueprint("www")
bp.import_nested_blueprint("dev")


@bp.before_app_request
def before_app_request():
    bp.init_session()
