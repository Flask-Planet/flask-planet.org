from flask import render_template

from .. import bp


@bp.route("/add", methods=["GET"])
def add():
    return render_template(bp.tmpl("add.html"))
