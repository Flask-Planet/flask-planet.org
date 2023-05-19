import mistune
from flask import render_template, request, redirect, url_for, session
from flask_bigapp.security import login_check

from app.globals import pytz_datetime, HighlightRenderer
from app.models.resource import Resource
from .. import bp


@bp.route("/add", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def add():
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")

        markdown = request.form.get("markdown", '')
        markdown_processor = mistune.create_markdown(renderer=HighlightRenderer())
        markup = markdown_processor(markdown)

        resource = Resource.add_new_resource(
            fk_user_id=session.get("user_id", 1),
            title=title,
            slug=slug,
            markup=markup,
            markdown=markdown,
            created=pytz_datetime()
        )

        return redirect(url_for("backend.resources.edit", resource_id=resource.resource_id))

    return render_template(bp.tmpl("add.html"))
