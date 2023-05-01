from .. import bp


@bp.post("/api/delete/resource/<resource_id>")
def api_delete_resource(resource_id):
    return "OK"
