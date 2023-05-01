from flask_bigapp.security import login_check

from .. import bp


@bp.post("/api/delete/resource/<resource_id>")
@login_check("logged_in", "backend.api_unauth")
def api_delete_resource(resource_id):
    return "OK"
