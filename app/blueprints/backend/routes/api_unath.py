from .. import bp


@bp.route("/api-unauth", methods=["GET"])
def api_unauth():
    return {"status": "error", "message": "Unauthorized"}
