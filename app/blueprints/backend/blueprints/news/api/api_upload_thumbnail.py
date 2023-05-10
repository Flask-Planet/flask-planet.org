import pathlib

from flask import request, current_app, url_for
from flask_bigapp.security import login_check
from werkzeug.utils import secure_filename

from app import logger
from app.models.news import News
from .. import bp


@bp.post("/api/upload/thumbnail/<news_id>")
@login_check("logged_in", "backend.api_unauth")
def api_upload_thumbnail(news_id):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads" / "news" / news_id)
    upload_location.mkdir(parents=True, exist_ok=True)

    news = News.get_by_id(news_id)

    if not news_id:
        logger.debug(f"No article found with id: <{news_id}>")
        return {"status": "error", "message": "No stream found"}

    thumbnail_file = request.files.get("thumbnail_file", None)

    if news.thumbnail:
        remove_thumbnail = upload_location / news.thumbnail
        remove_thumbnail.unlink(missing_ok=True)

    if not thumbnail_file:
        logger.debug(f"No image file found in request")
        return {"status": "error", "message": "No thumbnail file found"}

    safe_filename = secure_filename(thumbnail_file.filename)
    thumbnail_file.save(upload_location / safe_filename)
    news.update_thumbnail(safe_filename)

    return {
        "status": "success",
        "message": "Thumbnail uploaded successfully",
        "thumbnail": url_for("news_cdn", news_id=news.news_id, filename=news.thumbnail)
    }
