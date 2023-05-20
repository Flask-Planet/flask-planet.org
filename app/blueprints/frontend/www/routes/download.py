import pathlib

from flask import current_app, send_file, abort

from app.models.resource import Resource
from .. import bp


@bp.route("/download/markdown/<slug>/<safe_filename>", methods=["GET"])
def download_markdown(slug, safe_filename):
    resource = Resource.get_by_slug(slug)

    if not resource:
        return abort(404)

    upload_location = pathlib.Path(
        pathlib.Path(current_app.root_path) / "uploads" / "resources" / str(resource.resource_id)
    )
    file = upload_location / safe_filename
    if file.exists():
        return send_file(file, as_attachment=True)

    return abort(404)
