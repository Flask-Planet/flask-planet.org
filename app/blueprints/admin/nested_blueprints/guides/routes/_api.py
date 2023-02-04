import mistune
from flask import request

from .. import bp


@bp.post("/api/convert-markdown")
def api_convert_markdown():
    response = request.json.get("markdown", "")
    return mistune.html(response)


@bp.post("/api/delete/guide/<guide_id>")
def api_delete_guide(guide_id):
    return "OK"


@bp.post("/api/get/all-guide-tags")
def api_get_all_guide_tags():
    return "OK"


@bp.post("/api/add/guide-tag")
def api_add_guide_tag():
    return "OK"


@bp.post("/api/delete/guide-tag/<guide_tag_id>")
def api_delete_guide_tag(guide_tag_id):
    return "OK"
