from flask import request

from app.models.resource_page import ResourcePage
from .. import bp


@bp.get("/api/delete/page/")
def api_get_delete_page():
    resource_page_id = request.args.get("id", None)
    if not resource_page_id:
        return {"status": "error", "message": "No valid resource_page_id"}
    ResourcePage.delete(int(resource_page_id))
    return {"status": "success", "message": "Resource page deleted"}
