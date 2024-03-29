from flask import render_template
from flask_bigapp.security import login_check

from .. import bp


@bp.route("/", methods=["GET"])
@login_check("logged_in", "backend.login")
def index():
    """
    Streams are pulled from an api endpoint and handled by AlpineJS on the frontend.
    See:
    - ../streams/api/api_get_all_streams.py
    - ../streams/api/api_search_stream.py
    - ../templates/streams/includes/alpine:data:streams_index.html
    """
    return render_template(bp.tmpl("index.html"))
