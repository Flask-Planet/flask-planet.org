from flask import render_template, abort, request

from app.models.news import News
from app.models.news_click import NewsClick
from .. import bp


@bp.route("/news-and-articles/<slug>", methods=["GET"])
def news_article(slug):
    article_ = News.get_by_slug(slug, backend=True)
    if not article_:
        return abort(404)

    NewsClick.add_news_click(article_.news_id)

    url_args = {}

    if "page" in request.args:
        url_args["page"] = request.args["page"]

    return render_template(bp.tmpl("news_article.html"), article=article_, url_args=url_args, slug=slug)
