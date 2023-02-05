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
    guide_ = bigapp.model("Guide").get_by_slug(slug)
    if guide_:
        return {"exists": True}
    return {"exists": False}


@bp.get("/api/get/markdown/<slug>")
def api_get_markdown(slug):
    guide_ = bigapp.model("Guide").get_by_slug(slug)
    return {"markup": f"\n{guide_.markup}", "markdown": f"\n{guide_.markdown}", "files": guide_.markdown_file}


@bp.post("/api/delete/guide/<guide_id>")
def api_delete_guide(guide_id):
    return "OK"


@bp.get("/api/get/all-guide-tags")
def api_get_all_guide_tags():
    q_guide_tag = bigapp.model("GuideTag").get_all_tags()
    return {"tags": q_guide_tag}


@bp.post("/api/add/guide-tag")
def api_add_guide_tag():
    return "OK"


@bp.post("/api/delete/guide-tag/<guide_tag_id>")
def api_delete_guide_tag(guide_tag_id):
    return "OK"
