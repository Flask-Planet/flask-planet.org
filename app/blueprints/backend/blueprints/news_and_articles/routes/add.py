import pathlib
from datetime import datetime

import mistune
from flask import render_template, request, session, url_for, redirect, current_app
from flask_bigapp.security import login_check
from werkzeug.utils import secure_filename

from app.globals import HighlightRenderer
from app.models.news import News
from .. import bp


@bp.route("/add", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def add():
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        thumbnail = request.files.get("thumbnail")

        markdown = request.form.get("markdown", '')
        markdown_processor = mistune.create_markdown(renderer=HighlightRenderer())
        markup = markdown_processor(markdown)

        viewable = True if request.form.get("viewable") == 'true' else False

        if request.form.get("release_date") != "":
            try:
                release_date = datetime.strptime(request.form.get("release_date", ''), "%Y-%m-%dT%H:%M")
            except ValueError:
                release_date = None
        else:
            release_date = None

        author = request.form.get("author")
        author_link = request.form.get("author_link")

        news = News.create(
            values={
                "fk_user_id": session.get("user_id", 1),
                "title": title,
                "slug": slug,
                "markdown": markdown,
                "markup": markup,
                "viewable": viewable,
                "release_date": release_date,
                "author": author,
                "author_link": author_link
            },
        )

        if thumbnail:
            upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads" / "news" / news.news_id)
            upload_location.mkdir(parents=True, exist_ok=True)

            safe_filename = secure_filename(thumbnail.filename)
            save_location = upload_location / safe_filename
            rename_file = upload_location / f"{news.news_id}-{news.slug}-thumbnail{save_location.suffix}"
            thumbnail.save(rename_file)
            news.thumbnail = rename_file.name
            news.save()

        return redirect(url_for("backend.news_and_articles.edit", news_id=news.news_id))

    return render_template(bp.tmpl("add.html"))
