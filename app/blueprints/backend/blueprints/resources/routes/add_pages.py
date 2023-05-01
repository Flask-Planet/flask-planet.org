import pathlib

import mistune
from flask import abort, request, current_app, redirect, url_for
from flask_bigapp.security import login_check
from werkzeug.utils import secure_filename

from app import logger
from app.models.resource import Resource
from .. import bp


@bp.post("/add-pages/<resource_id>")
@login_check("logged_in", "backend.login")
def add_pages(resource_id):
    resource_ = Resource.read(id_=resource_id)
    if not resource_:
        return abort(400)

    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads")

    files = request.files.getlist("markdown_file")
    files.sort(key=lambda x: x.filename)

    if files[0]:
        markup, markdown = "", ""
        logger.debug(f"files: {files}")
        filenames = []
        for file in files:
            filename = secure_filename(file.filename)
            filenames.append(filename)
            save_location = upload_location / filename
            if save_location.suffix == ".md":
                file.save(save_location)
                markdown += save_location.read_text()
                save_location.unlink()

        markup = mistune.html(markdown).strip()

    return redirect(url_for("backend.resources.index"))
