import pathlib

import mistune
from flask import request, current_app
from werkzeug.utils import secure_filename

from app import bigapp, logger
from .. import bp


@bp.post("/api/convert/markdown")
def api_convert_markdown():
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "temp")
    files = request.files.getlist("markdown_file")
    files.sort(key=lambda x: x.filename)
    markup, markdown = "", ""
    logger.debug(f"files: {files}")
    filenames = []
    for file in files:
        filename = secure_filename(file.filename)
        filenames.append(filename)
        save_location = upload_location / filename
        if save_location.suffix == ".md":
            file.save(save_location)
            markdown += save_location.read_text()
            save_location.unlink()

    markup = mistune.html(markdown).strip()
    return {"markup": f"\n{markup}", "markdown": f"\n{markdown}", "files": filenames}


@bp.get("/api/check-if-slug-exists/")
def api_check_if_slug_exists():
    slug = request.args.get("slug", None)
    tutorial_ = bigapp.model("Tutorial").get_by_slug(slug)
    if tutorial_:
        return {"exists": True}
    return {"exists": False}


@bp.get("/api/get/markdown/<slug>")
def api_get_markdown(slug):
    tutorial_ = bigapp.model("Tutorial").get_by_slug(slug)
    return {"markup": f"\n{tutorial_.markup}", "markdown": f"\n{tutorial_.markdown}", "files": tutorial_.markdown_file}


@bp.post("/api/delete/tutorial/<tutorial_id>")
def api_delete_tutorial(tutorial_id):
    return "OK"


@bp.get("/api/get/all-tutorial-tags")
def api_get_all_tutorial_tags():
    q_tutorial_tag = bigapp.model("TutorialTag").get_all_tags()
    return {"tags": q_tutorial_tag}


@bp.post("/api/add/tutorial-tag")
def api_add_tutorial_tag():
    return "OK"


@bp.post("/api/delete/tutorial-tag/<tutorial_tag_id>")
def api_delete_tutorial_tag(tutorial_tag_id):
    return "OK"
