from flask import render_template

from .. import bp


@bp.route("/guides/guide/<slug_title>", methods=["GET"])
def guide(slug_title):


    return render_template(bp.tmpl("guide.html"))
