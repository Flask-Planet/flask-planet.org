from flask import request
from flask_bigapp.security import login_check

from app.models.resource import Resource
from .. import bp


@bp.get("/api/get/resource-tags")
@login_check("logged_in", "backend.api_unauth")
def api_get_resource_tags():
    id_ = request.args.get("id", None)
    if not id_:
        return {"status": "No valid resource", "tags": []}
    return {"status": "success", "tags": Resource.get_tags_by_id(id_)}
