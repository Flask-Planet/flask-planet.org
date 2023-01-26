from flask import render_template

from .. import bp


@bp.route("/authors/author/<slug_name>", methods=["GET"])
def author(slug_name):
    return render_template(bp.tmpl("author.html"))
