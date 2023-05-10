import mistune
from flask import render_template, request, session, url_for, redirect
from flask_bigapp.security import login_check

from app.globals import pytz_datetime
from app.models.stream import Stream
from .. import bp


@bp.route("/add", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def add():
    if request.method == "POST":
        title = request.form.get("title")
        markdown = request.form.get("markdown")

        markup = mistune.html(markdown).strip()

        stream = Stream.add_new_stream(
            fk_user_id=session.get("user_id", 1),
            title=title,
            markdown=markdown,
            markup=markup,
            created=pytz_datetime()
        )

        return redirect(url_for("backend.streams.edit", stream_id=stream.stream_id))
    return render_template(bp.tmpl("add.html"))
