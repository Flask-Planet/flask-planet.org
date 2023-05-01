from flask import render_template

from app.models.stream import Stream
from .. import bp


@bp.route("/streams", methods=["GET"])
def streams():
    upcoming_streams = Stream.newest_upcoming()

    past_steams = Stream.newest_past()
    most_recent_stream = past_steams[0] if past_steams else None
    rest_of_past_streams = past_steams[1:] if len(past_steams) > 1 else None
    return render_template(
        bp.tmpl("streams.html"),
        upcoming_streams=upcoming_streams,
        most_recent_stream=most_recent_stream,
        rest_of_past_streams=rest_of_past_streams,
    )
