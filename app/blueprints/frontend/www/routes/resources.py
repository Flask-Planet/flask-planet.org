from flask import render_template

from .. import bp


@bp.route("/resources", methods=["GET"])
def resources():
    return render_template(bp.tmpl("resources.html"))
