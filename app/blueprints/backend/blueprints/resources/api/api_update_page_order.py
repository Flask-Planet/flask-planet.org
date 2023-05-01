from flask import request
from flask_bigapp.security import login_check

from app.models.resource_page import ResourcePage
from .. import bp


@bp.post("/api/update/page/order/")
@login_check("logged_in", "backend.api_unauth")
def api_update_page_order():
    resource_id = request.args.get("id", None)
    if not resource_id:
        return {"status": "error", "message": "No valid resource_page_id"}
    jsond = request.get_json()
    for id_, order in jsond.items():
        ResourcePage.update_order(id_, order)
    return {"status": "success", "message": "Resource pages order updated"}
