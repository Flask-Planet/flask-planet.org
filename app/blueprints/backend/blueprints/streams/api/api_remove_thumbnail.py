import pathlib

from flask import current_app

from app import logger
from app.models.stream import Stream
from .. import bp


@bp.post("/api/remove/thumbnail/<stream_id>")
def api_remove_thumbnail(stream_id):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "stream_thumbnails" / stream_id)
    upload_location.mkdir(parents=True, exist_ok=True)

    stream = Stream.get_by_id(stream_id)

    if not stream:
        logger.debug(f"No stream found with id: <{stream_id}>")
        return {"status": "error", "message": "No stream found"}

    if not stream.thumbnail:
        logger.debug(f"No thumbnail found for stream: <{stream_id}>")
        return {"status": "success", "message": "No thumbnail found"}

    thumbnail_file = upload_location / stream.thumbnail
    thumbnail_file.unlink(missing_ok=True)
    stream.remove_thumbnail()

    return {"status": "success", "message": "Thumbnail removed successfully"}
