import pathlib

from flask import render_template, request, redirect, url_for, current_app, session
from werkzeug.utils import secure_filename

from app import bigapp
from app.globals import pytz_datetime
from .. import bp


@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads")
        temp_location = pathlib.Path(pathlib.Path(current_app.root_path) / "temp")

        title = request.form.get("title")
        slug = request.form.get("slug")
        summary = request.form.get("summary")
        tutorial_tags = request.form.get("tutorial_tags")
        markup = request.form.get("markup").lstrip("\n")
        markdown = request.form.get("markdown").lstrip("\n")

        tags_list = tutorial_tags.split(",")

        files = request.files.getlist("markdown_file")
        files.sort(key=lambda x: x.filename)

        new_file = upload_location / f"{slug}.md"

        if new_file.exists():
            new_file.unlink()

        new_file.touch()

        for i, file in enumerate(files):
            temp_save = temp_location / secure_filename(file.filename)

            if temp_save.suffix == ".md":
                file.save(temp_save)
            with open(new_file, "a") as f:
                f.write(temp_save.read_text())

            temp_save.unlink()

        filename = new_file.name

        bigapp.model("Tutorial").add_new_tutorial(
            fk_user_id=session.get("user_id", 1),
            tags=tags_list,
            title=title,
            slug=slug,
            summary=summary,
            markup=markup,
            markdown=markdown,
            markdown_file=filename,
            created=pytz_datetime()
        )

        return redirect(url_for("backend.tutorials.index"))

    return render_template(bp.tmpl("add.html"))
