from flask import request
from flask_bigapp.security import login_check

from app.models.news import News
from .. import bp


@bp.get("/api/check-if-slug-exists/")
@login_check("logged_in", "backend.api_unauth")
def api_check_if_slug_exists():
    slug = request.args.get("slug", None)
    resource_ = News.get_by_slug(slug)
    if resource_:
        return {"exists": True}
    return {"exists": False}
