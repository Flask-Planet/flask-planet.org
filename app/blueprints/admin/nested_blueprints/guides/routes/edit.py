from flask import render_template

from .. import bp


@bp.route("/edit/<guide_id>", methods=["GET"])
def edit(guide_id):
    return render_template(bp.tmpl("edit.html"))
