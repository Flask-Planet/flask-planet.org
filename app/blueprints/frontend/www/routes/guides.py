from flask import render_template

from .. import bp


@bp.route("/guides", methods=["GET"])
def guides():
    return render_template(bp.tmpl("guides.html"))
