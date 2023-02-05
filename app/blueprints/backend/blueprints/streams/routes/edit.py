from flask import render_template

from .. import bp


@bp.route("/edit/<stream_id>", methods=["GET"])
def edit(stream_id):
    r_vars = {
        "stream_id": stream_id,
    }
    return render_template(bp.tmpl("edit.html"), **r_vars)
