from flask import abort, render_template

from app import bigapp
from .. import bp


@bp.route("/guides/guide/<slug>", methods=["GET"])
def guide(slug):
    guide_ = bigapp.model("Guide").get_by_slug(slug)
    if not guide_:
        return abort(404)

    return render_template(bp.tmpl("guide.html"), guide=guide_)
