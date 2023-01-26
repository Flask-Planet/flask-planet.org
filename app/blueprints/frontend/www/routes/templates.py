from flask import render_template

from .. import bp


@bp.route("/templates", methods=["GET"])
def templates():
    return render_template(bp.tmpl("templates.html"))
