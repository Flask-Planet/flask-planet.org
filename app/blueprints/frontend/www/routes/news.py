from flask import render_template

from .. import bp


@bp.route("/news", methods=["GET"])
def news():
    return render_template(bp.tmpl("news.html"))
