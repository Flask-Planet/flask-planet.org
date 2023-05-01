from flask import render_template
from flask_bigapp.security import login_check

from .. import bp


@bp.route("/", methods=["GET"])
@login_check("logged_in", "backend.login")
def index():
    return render_template(bp.tmpl("index.html"))
