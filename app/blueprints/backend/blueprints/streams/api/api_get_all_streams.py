from flask import request, url_for

from app.models.stream import Stream
from .. import bp


@bp.get("/api/get/all/streams")
def api_get_all_streams():
    page = request.args.get("page", 1)
    streams = Stream.all_newest_first_pages(
        page=int(page),
        per_page=5
    )
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
            "schedule": stream.schedule.strftime("%Y-%m-%d %H:%M") if stream.schedule else '',
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
