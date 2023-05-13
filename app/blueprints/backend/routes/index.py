from flask import render_template, redirect, url_for
from flask_bigapp.security import login_check

from .. import bp


@bp.route("/", methods=["GET"])
@login_check("logged_in", "backend.login")
def index():
    return redirect(url_for("backend.streams.index"))
