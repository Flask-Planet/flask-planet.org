from flask import abort, render_template

from app import bigapp
from .. import bp


@bp.route("/tutorials/tutorial/<slug>", methods=["GET"])
def tutorial(slug):
    tutorial_ = bigapp.model("Tutorial").get_by_slug(slug)
    if not tutorial_:
        return abort(404)

    return render_template(bp.tmpl("tutorial.html"), tutorial=tutorial_)
