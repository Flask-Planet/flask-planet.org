from flask import render_template, request

from app.models.resource import Resource
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    # All resources pulled via API route -> api_get_all_resources()
    return render_template(bp.tmpl("index.html"))
