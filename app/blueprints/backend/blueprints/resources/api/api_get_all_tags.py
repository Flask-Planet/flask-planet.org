from app.models.resource_tag import ResourceTag
from .. import bp


@bp.get("/api/get/all-tags")
def api_get_all_tags():
    q_resource_tag = ResourceTag.get_all_tags()
    return {"tags": q_resource_tag}
