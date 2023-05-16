from flask import render_template, request

from app.models.stream import Stream
from .. import bp


@bp.route("/streams/all", methods=["GET"])
def all_streams():
    streams = Stream.all_schedule_first_pages(
        page=int(request.args.get("page", 1)),
        per_page=10,
    )

    return render_template(
        bp.tmpl("all_streams.html"),
        streams=streams,
        page=streams.page,
        pages=streams.pages,
    )
