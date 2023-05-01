from flask import request, url_for

from app import logger
from app.models.resource import Resource
from .. import bp


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
                "viewable": resource.viewable,
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
