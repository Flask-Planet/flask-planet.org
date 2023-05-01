from flask import request, url_for

from app.models.resource import Resource
from .. import bp


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
