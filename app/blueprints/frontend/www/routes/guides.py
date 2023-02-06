from flask import render_template

from app import bigapp
from .. import bp


@bp.route("/tutorials", methods=["GET"])
def tutorials():
    tutorials_ = bigapp.model("Tutorial").all_newest_first()
    return render_template(bp.tmpl("tutorials.html"), tutorials=tutorials_)
