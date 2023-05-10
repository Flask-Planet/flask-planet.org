from flask import render_template
from flask_bigapp.security import login_check

from .. import bp


@bp.route("/", methods=["GET"])
@login_check("logged_in", "backend.login")
def index():
    """
    News articles are pulled from an api endpoint and handled by AlpineJS on the frontend.
    See:
    - ../news/api/api_get_all_news.py
    - ../news/api/api_search_news.py
    - ../templates/news/includes/alpine:data:news_index.html
    """
    return render_template(bp.tmpl("index.html"))
