from flask_bigapp.security import login_check

from app.models.resource_tag import ResourceTag
from .. import bp


@bp.get("/api/get/all-tags")
@login_check("logged_in", "backend.api_unauth")
def api_get_all_tags():
    q_resource_tag = ResourceTag.get_all_tags()
    return {"tags": q_resource_tag}
