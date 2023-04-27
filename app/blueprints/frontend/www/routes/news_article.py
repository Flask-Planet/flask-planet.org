from flask import render_template

from .. import bp


@bp.route("/news/article/<slug>", methods=["GET"])
def news_article(slug):
    return render_template(bp.tmpl("news_article.html"))
