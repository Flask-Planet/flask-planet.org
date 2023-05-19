from datetime import datetime

import mistune
from flask import render_template, abort, request, url_for, redirect
from flask_bigapp.security import login_check

from app.extensions import logger
from app.globals import HighlightRenderer
from app.models.stream import Stream
from .. import bp


@bp.route("/edit/<stream_id>", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def edit(stream_id):
    stream_ = Stream.get_by_id(stream_id)
    if not stream_:
        return abort(404)

    if request.method == "POST":
        logger.debug(f"Updating stream {stream_.stream_id}")

        if request.form.get("go_viewable_on") != "":
            try:
                go_viewable_on = datetime.strptime(request.form.get("go_viewable_on", ''), "%Y-%m-%d")
            except ValueError:
                go_viewable_on = None
        else:
            go_viewable_on = None

        if request.form.get("schedule") != "":
            try:
                schedule = datetime.strptime(request.form.get("schedule", ''), "%Y-%m-%dT%H:%M")
            except ValueError:
                schedule = None
        else:
            schedule = None

        markdown = request.form.get("markdown", '')
        markdown_processor = mistune.create_markdown(renderer=HighlightRenderer())
        markup = markdown_processor(markdown)

        Stream.update(
            values={
                "title": request.form.get("title"),
                "markdown": markdown,
                "markup": markup,
                "schedule": schedule,
                "url_link": request.form.get("url_link"),
                "display_url_link": request.form.get("display_url_link"),
                "viewable": True if request.form.get("viewable") == 'true' else False,
                "auto_viewable": True if request.form.get("auto_viewable") == 'true' else False,
                "go_viewable_on": go_viewable_on
            },
            id_=stream_id,
        )

        return redirect(url_for("backend.streams.edit", stream_id=stream_id))

    if stream_.thumbnail:
        thumbnail = url_for("stream_cdn", stream_id=stream_.stream_id, filename=stream_.thumbnail)
    else:
        thumbnail = url_for("theme.static", filename="img/no-thumbnail.png")

    return render_template(bp.tmpl("edit.html"), stream=stream_, thumbnail=thumbnail)
