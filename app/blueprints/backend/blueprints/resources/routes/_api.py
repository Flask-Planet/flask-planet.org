import pathlib

import mistune
from flask import request, current_app, abort, url_for
from werkzeug.utils import secure_filename

from app import logger
from app.globals import pytz_datetime
from app.models.resource import Resource
from app.models.resource_page import ResourcePage
from app.models.resource_tag import ResourceTag
from .. import bp


@bp.post("/api/convert/markdown")
def api_convert_markdown():
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "temp")
    files = request.files.getlist("markdown_file")
    files.sort(key=lambda x: x.filename)
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
    return {"markup": f"\n{markup}", "markdown": f"\n{markdown}", "files": filenames}


@bp.post("/api/add/pages/to/<resource_id>")
def api_add_pages_to(resource_id):
    upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads")
    if not upload_location.exists():
        upload_location.mkdir()

    resource_ = Resource.get_by_id(resource_id)
    if not resource_:
        abort(404)

    files = request.files.getlist("markdown_file")

    logger.debug(f"files: {files}")

    filenames = []
    for file in files:
        safe_filename = secure_filename(f"{resource_id}_{file.filename}")
        filenames.append(safe_filename)
        save_location = upload_location / safe_filename
        if save_location.suffix == ".md":
            file.save(save_location)
            markdown = save_location.read_text()
            markup = mistune.html(markdown).strip()
            ResourcePage.create(
                values={
                    "fk_resource_id": resource_.resource_id,
                    "order": request.form.get(f"{file.filename}", 0),
                    "markup": markup,
                    "markdown": markdown,
                    "markdown_og_filename": file.filename,
                    "markdown_safe_filename": safe_filename,
                    "created": pytz_datetime()
                }
            )

    return {"files": filenames}


@bp.get("/api/check-if-slug-exists/")
def api_check_if_slug_exists():
    slug = request.args.get("slug", None)
    resource_ = Resource.get_by_slug(slug)
    if resource_:
        return {"exists": True}
    return {"exists": False}


@bp.get("/api/get/all/resources")
def api_get_all_resources():
    page = request.args.get("page", 1)
    resources = Resource.all_newest_first_pages(
        page=int(page),
        per_page=10
    )
    clean_resources = []
    for resource in resources:
        tags = ", ".join([tag.rel_resource_tag.tag for tag in resource.rel_resource_tag_membership])
        edit_url = url_for('backend.resources.edit', resource_id=resource.resource_id)
        clean_resources.append(
            {
                "resource_id": resource.resource_id,
                "title": resource.title,
                "slug": resource.slug,
                "tags": tags,
                "clicks": len(resource.rel_resource_clicks),
                "created": resource.created.strftime("%Y-%m-%d"),
                "edit_url": edit_url
            })
    return {
        "status": "success",
        "resources": clean_resources,
        "pages": resources.pages,
        "page": resources.page
    }


@bp.post("/api/search/resource")
def api_search_resource():
    search = request.form.get("search", None)
    logger.debug(f"Searching for title: <{search}>")
    if not search:
        return {"status": "error", "message": "No search term"}

    page = request.args.get("page", 1)
    resources = Resource.search_by_title_pages(
        title=search,
        page=int(page),
        per_page=10
    )

    if not resources:
        logger.debug(f"No resources found for search term: <{search}>")
        return {"status": "error", "message": "No resources found"}

    logger.debug(f"{resources.total} Resources found for search term: <{search}>")

    clean_resources = []
    for resource in resources:
        tags = ", ".join([tag.rel_resource_tag.tag for tag in resource.rel_resource_tag_membership])
        edit_url = url_for('backend.resources.edit', resource_id=resource.resource_id)
        clean_resources.append(
            {
                "resource_id": resource.resource_id,
                "title": resource.title,
                "slug": resource.slug,
                "tags": tags,
                "clicks": len(resource.rel_resource_clicks),
                "created": resource.created.strftime("%Y-%m-%d"),
                "edit_url": edit_url
            })
    return {
        "status": "success",
        "resources": clean_resources,
        "pages": resources.pages,
        "page": resources.page
    }


@bp.post("/api/delete/resource/<resource_id>")
def api_delete_resource(resource_id):
    return "OK"


@bp.get("/api/get/all-pages/")
def api_get_all_pages():
    resource_id = request.args.get("id", None)
    if not resource_id:
        return {"status": "error", "message": "No valid resource_id", "pages": []}
    resource_ = Resource.get_by_id(resource_id)
    pages = resource_.rel_resource_pages
    clean_pages = []
    for page in pages:
        clean_pages.append({
            "resource_page_id": page.resource_page_id,
            "order": page.order,
            "markup": page.markup,
            "markdown": page.markdown,
            "markdown_og_filename": page.markdown_og_filename
        })
    return {"status": "success", "pages": clean_pages}


@bp.post("/api/update/page/order/")
def api_update_page_order():
    resource_id = request.args.get("id", None)
    if not resource_id:
        return {"status": "error", "message": "No valid resource_page_id"}
    jsond = request.get_json()
    for id_, order in jsond.items():
        ResourcePage.update_order(id_, order)
    return {"status": "success", "message": "Resource pages order updated"}


@bp.get("/api/delete/page/")
def api_get_delete_page():
    resource_page_id = request.args.get("id", None)
    if not resource_page_id:
        return {"status": "error", "message": "No valid resource_page_id"}
    ResourcePage.delete(int(resource_page_id))
    return {"status": "success", "message": "Resource page deleted"}


@bp.get("/api/get/all-tags")
def api_get_all_tags():
    q_resource_tag = ResourceTag.get_all_tags()
    return {"tags": q_resource_tag}


@bp.get("/api/get/resource-tags")
def api_get_resource_tags():
    id_ = request.args.get("id", None)
    if not id_:
        return {"status": "No valid resource", "tags": []}
    return {"status": "success", "tags": Resource.get_tags_by_id(id_)}
