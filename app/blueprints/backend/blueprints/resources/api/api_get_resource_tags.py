from flask import request

from app.models.resource import Resource
from .. import bp


@bp.get("/api/get/resource-tags")
def api_get_resource_tags():
    id_ = request.args.get("id", None)
    if not id_:
        return {"status": "No valid resource", "tags": []}
    return {"status": "success", "tags": Resource.get_tags_by_id(id_)}
