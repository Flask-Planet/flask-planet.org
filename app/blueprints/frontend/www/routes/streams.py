from flask import render_template

from .. import bp


@bp.route("/streams", methods=["GET"])
def streams():
    return render_template(bp.tmpl("streams.html"))
