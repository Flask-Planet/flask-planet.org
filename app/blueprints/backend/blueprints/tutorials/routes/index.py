from flask import render_template

from app import bigapp
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    q_tutorials = bigapp.model("Tutorial").all_newest_first()

    r_vars = {
        "q_tutorials": q_tutorials,
    }
    return render_template(bp.tmpl("index.html"), **r_vars)
