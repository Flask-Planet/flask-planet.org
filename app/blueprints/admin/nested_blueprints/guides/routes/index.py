from flask import render_template

from app import bigapp
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    q_guides = bigapp.model("Guide").all_newest_first()

    r_vars = {
        "q_guides": q_guides,
    }
    return render_template(bp.tmpl("index.html"), **r_vars)
