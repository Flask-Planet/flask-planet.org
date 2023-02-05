from flask import render_template

from app import bigapp
from .. import bp


@bp.route("/guides", methods=["GET"])
def guides():
    guides_ = bigapp.model("Guide").all_newest_first()
    return render_template(bp.tmpl("guides.html"), guides=guides_)
