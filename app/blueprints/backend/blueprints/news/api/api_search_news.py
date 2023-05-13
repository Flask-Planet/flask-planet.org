from flask import request, url_for
from flask_bigapp.security import login_check

from app import logger
from app.models.news import News
from .. import bp


@bp.post("/api/search/news")
@login_check("logged_in", "backend.api_unauth")
def api_search_news():
    search = request.form.get("search", None)
    logger.debug(f"Searching for title: <{search}>")
    if not search:
        return {"status": "error", "message": "No search term"}

    page = request.args.get("page", 1)
    news = News.search_by_title_pages(
        title=search,
        page=int(page),
        per_page=5
    )

    if not news:
        logger.debug(f"No news found for search term: <{search}>")
        return {"status": "error", "message": "No resources found"}

    logger.debug(f"{news.total} Streams found for search term: <{search}>")

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
            "clicks": len(article.rel_news_clicks),
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
