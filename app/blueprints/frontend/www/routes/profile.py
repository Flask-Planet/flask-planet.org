from flask import render_template

from .. import bp


@bp.route("/profile", methods=["GET"])
def profile():
    return render_template(bp.tmpl("profile.html"))
