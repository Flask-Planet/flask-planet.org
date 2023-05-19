import pathlib

from flask import request, current_app
from flask_bigapp.security import login_check

from app.models.resource_page import ResourcePage
from .. import bp


@bp.get("/api/delete/page/")
@login_check("logged_in", "backend.api_unauth")
def api_get_delete_page():
    resource_page_id = int(request.args.get("id", None))
    if not resource_page_id:
        return {"status": "error", "message": "No valid resource_page_id"}

    resource_page = ResourcePage.get_by_id(resource_page_id)

    upload_location = pathlib.Path(
        pathlib.Path(current_app.root_path) / "uploads" / "resources" / str(resource_page.fk_resource_id))
    file_location = upload_location / resource_page.markdown_safe_filename
    file_location.unlink(missing_ok=True)

    ResourcePage.delete_by_id(resource_page_id)

    return {"status": "success", "message": "Resource page deleted"}
