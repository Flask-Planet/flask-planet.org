from flask import render_template, abort

from app.models.news import News
from app.models.news_click import NewsClick

from .. import bp


@bp.route("/news/article/<slug>", methods=["GET"])
def article(slug):
    article_ = News.get_by_slug(slug)
    if not article_:
        return abort(404)

    NewsClick.add_news_click(article_.news_id)

    return render_template(bp.tmpl("article.html"), article=article_)
