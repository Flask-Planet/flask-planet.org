import pathlib

from flask import current_app
from flask_bigapp.security import login_check

from app import logger
from app.models.news import News
from .. import bp


@bp.post("/api/remove/thumbnail/<news_id>")
@login_check("logged_in", "backend.api_unauth")
def api_remove_thumbnail(news_id):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads" / "news" / news_id)
    upload_location.mkdir(parents=True, exist_ok=True)

    news = News.get_by_id(news_id)

    if not news:
        logger.debug(f"No news found with id: <{news_id}>")
        return {"status": "error", "message": "No stream found"}

    if not news.thumbnail:
        logger.debug(f"No thumbnail found for article: <{news_id}>")
        return {"status": "success", "message": "No thumbnail found"}

    thumbnail_file = upload_location / news.thumbnail
    thumbnail_file.unlink(missing_ok=True)
    news.remove_thumbnail()

    return {"status": "success", "message": "Thumbnail removed successfully"}
