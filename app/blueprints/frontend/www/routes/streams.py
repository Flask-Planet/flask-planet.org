from flask import render_template

from app.models.stream import Stream
from .. import bp


@bp.route("/streams", methods=["GET"])
def streams():
    upcoming_streams = Stream.newest_upcoming()
    most_recent_streams = Stream.most_recent_streams()

    return render_template(
        bp.tmpl("streams.html"),
        upcoming_streams=upcoming_streams,
        most_recent_streams=most_recent_streams,
    )
