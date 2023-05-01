import pathlib

from flask import request, current_app, url_for
from werkzeug.utils import secure_filename

from app import logger
from app.models.stream import Stream
from .. import bp


@bp.post("/api/upload/thumbnail/<stream_id>")
def api_upload_thumbnail(stream_id):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "stream_thumbnails" / stream_id)
    upload_location.mkdir(parents=True, exist_ok=True)

    stream = Stream.get_by_id(stream_id)

    if not stream:
        logger.debug(f"No stream found with id: <{stream_id}>")
        return {"status": "error", "message": "No stream found"}

    thumbnail_file = request.files.get("thumbnail_file", None)

    if stream.thumbnail:
        remove_thumbnail = upload_location / stream.thumbnail
        remove_thumbnail.unlink(missing_ok=True)

    if not thumbnail_file:
        logger.debug(f"No image file found in request")
        return {"status": "error", "message": "No thumbnail file found"}

    safe_filename = secure_filename(thumbnail_file.filename)
    thumbnail_file.save(upload_location / safe_filename)
    stream.update_thumbnail(safe_filename)

    return {
        "status": "success",
        "message": "Thumbnail uploaded successfully",
        "thumbnail": url_for("stream_cdn", stream_id=stream.stream_id, filename=stream.thumbnail)
    }
