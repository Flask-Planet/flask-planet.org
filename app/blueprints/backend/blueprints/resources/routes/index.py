from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    """
    Resources are pulled from an api endpoint and handled by AlpineJS on the frontend.
    See:
    - ../resources/api/api_get_all_resources.py
    - ../resources/api/api_search_resource.py
    - ../templates/resources/includes/alpine:data:resources_index.html
    """
    return render_template(bp.tmpl("index.html"))
