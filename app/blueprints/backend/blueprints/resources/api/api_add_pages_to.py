import pathlib

import mistune
from flask import request, current_app, abort
from werkzeug.utils import secure_filename

from app import logger
from app.globals import pytz_datetime
from app.models.resource import Resource
from app.models.resource_page import ResourcePage
from .. import bp


@bp.post("/api/add/pages/to/<resource_id>")
def api_add_pages_to(resource_id):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "resource_markdown" / resource_id)
    upload_location.mkdir(parents=True, exist_ok=True)

    resource_ = Resource.get_by_id(resource_id)
    if not resource_:
        abort(404)

    file_count = ResourcePage.count_by_resource_id(resource_id)
    files = request.files.getlist("markdown_file")

    logger.debug(f"Previous file count: {file_count}")
    logger.debug(f"Files: {files}")

    filenames = []
    for index, file in enumerate(files):
        safe_filename = secure_filename(file.filename)
        filenames.append(safe_filename)
        save_location = upload_location / safe_filename
        if save_location.exists():
            save_location.unlink()
            ResourcePage.delete_by_og_filename(safe_filename, resource_id)
        if save_location.suffix == ".md":
            file.save(save_location)
            markdown = save_location.read_text()
            markup = mistune.html(markdown).strip()
            ResourcePage.create(
                values={
                    "fk_resource_id": resource_.resource_id,
                    "order": file_count + index + 1,
                    "markup": markup,
                    "markdown": markdown,
                    "markdown_og_filename": file.filename,
                    "markdown_safe_filename": safe_filename,
                    "created": pytz_datetime()
                }
            )

    return {"files": filenames}
