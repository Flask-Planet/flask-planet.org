from flask import request, url_for

from app import logger
from app.models.stream import Stream
from .. import bp


@bp.post("/api/search/stream")
def api_search_stream():
    search = request.form.get("search", None)
    logger.debug(f"Searching for title: <{search}>")
    if not search:
        return {"status": "error", "message": "No search term"}

    page = request.args.get("page", 1)
    streams = Stream.search_by_title_pages(
        title=search,
        page=int(page),
        per_page=5
    )

    if not streams:
        logger.debug(f"No streams found for search term: <{search}>")
        return {"status": "error", "message": "No resources found"}

    logger.debug(f"{streams.total} Streams found for search term: <{search}>")

    clean_streams = []
    for stream in streams:
        edit_url = url_for('backend.streams.edit', stream_id=stream.stream_id)

        if stream.thumbnail:
            thumbnail = url_for("stream_cdn", stream_id=stream.stream_id, filename=stream.thumbnail)
        else:
            thumbnail = url_for("theme.static", filename="img/no-thumbnail.png")

        clean_streams.append({
            "stream_id": stream.stream_id,
            "thumbnail": thumbnail,
            "title": stream.title,
            "schedule": stream.schedule.strftime("%Y-%m-%d %H:%M"),
            "url_link": stream.url_link,
            "display_url_link": stream.display_url_link,
            "viewable": stream.viewable,
            "created": stream.created.strftime("%Y-%m-%d"),
            "edit_url": edit_url
        })
    return {
        "status": "success",
        "streams": clean_streams,
        "pages": streams.pages,
        "page": streams.page
    }
