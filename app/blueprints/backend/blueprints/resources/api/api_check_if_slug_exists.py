from flask import request
from flask_bigapp.security import login_check

from app.models.resource import Resource
from .. import bp


@bp.get("/api/check-if-slug-exists/")
@login_check("logged_in", "backend.api_unauth")
def api_check_if_slug_exists():
    slug = request.args.get("slug", None)
    resource_ = Resource.get_by_slug(slug, backend=True)
    if resource_:
        return {"exists": True}
    return {"exists": False}
