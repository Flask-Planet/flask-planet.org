from flask import request, url_for
from flask_bigapp.security import login_check

from app.models.stream import Stream
from .. import bp


@bp.get("/api/get/all/streams")
@login_check("logged_in", "backend.api_unauth")
def api_get_all_streams():
    page = request.args.get("page", 1)
    streams = Stream.all_schedule_first_pages(
        page=int(page),
        per_page=5,
        backend=True,
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
