from flask import request, url_for
from flask_bigapp.security import login_check

from app.models.news import News
from .. import bp


@bp.get("/api/get/all/news")
@login_check("logged_in", "backend.api_unauth")
def api_get_all_news():
    page = request.args.get("page", 1)
    news = News.all_newest_first_pages(
        page=int(page),
        per_page=5
    )
    clean_articles = []
    for article in news:
        edit_url = url_for('backend.news.edit', news_id=article.news_id)

        if article.thumbnail:
            thumbnail = url_for("news_cdn", news_id=article.news_id, filename=article.thumbnail)
        else:
            thumbnail = url_for("theme.static", filename="img/no-thumbnail.png")

        clean_articles.append({
            "news_id": article.news_id,
            "title": article.title,
            "thumbnail": thumbnail,
            "author": article.author,
            "viewable": article.viewable,
            "release_date": article.release_date.strftime("%Y-%m-%d %H:%M") if article.release_date else '',
            "edit_url": edit_url
        })
    return {
        "status": "success",
        "news": clean_articles,
        "pages": news.pages,
        "page": news.page
    }
