from flask import request

from app.models.resource import Resource
from .. import bp


@bp.get("/api/check-if-slug-exists/")
def api_check_if_slug_exists():
    slug = request.args.get("slug", None)
    resource_ = Resource.get_by_slug(slug)
    if resource_:
        return {"exists": True}
    return {"exists": False}
