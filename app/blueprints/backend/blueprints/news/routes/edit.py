import pathlib
from datetime import datetime

import mistune
from flask import render_template, abort, request, url_for, current_app, redirect
from flask_bigapp.security import login_check
from werkzeug.utils import secure_filename

from app.extensions import logger
from app.globals import HighlightRenderer
from app.models.news import News
from .. import bp


@bp.route("/edit/<news_id>", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def edit(news_id):
    news_ = News.get_by_id(news_id)
    if not news_:
        return abort(404)

    if request.method == "POST":
        logger.debug(f"Updating news {news_.news_id}")

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

        News.update(
            values={
                "title": title,
                "slug": slug,
                "markdown": markdown,
                "markup": markup,
                "viewable": viewable,
                "release_date": release_date,
                "author": author or "",
                "author_link": author_link or "",
            },
            id_=news_id,
        )

        if thumbnail:
            upload_location = pathlib.Path(
                pathlib.Path(current_app.root_path) / "uploads" / "news" / str(news_.news_id))
            upload_location.mkdir(parents=True, exist_ok=True)

            if news_.thumbnail:
                old_file = upload_location / str(news_.thumbnail)
                if old_file.exists():
                    old_file.unlink()

            safe_filename = secure_filename(thumbnail.filename)
            save_location = upload_location / safe_filename
            thumbnail.save(save_location)
            news_.thumbnail = safe_filename
            news_.save()

        return redirect(url_for("backend.news.edit", news_id=news_.news_id))

    if news_.thumbnail:
        thumbnail = url_for("news_cdn", news_id=news_.news_id, filename=news_.thumbnail)
    else:
        thumbnail = url_for("theme.static", filename="img/no-thumbnail.png")

    return render_template(bp.tmpl("edit.html"), news=news_, thumbnail=thumbnail)
