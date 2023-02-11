from flask import render_template

from .. import bp


@bp.route("/authors", methods=["GET"])
def authors():
    return render_template(bp.tmpl("authors.html"))
