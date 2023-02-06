import pathlib

from flask import current_app, send_file, abort

from .. import bp


@bp.route("/download/markdown/<slug>.md", methods=["GET"])
def download_markdown(slug):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads")
    file = upload_location / f"{slug}.md"
    if file.exists():
        return send_file(file, as_attachment=True)

    return abort(404)
