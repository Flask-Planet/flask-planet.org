from flask import render_template, request

from app.models.resource import Resource
from app.models.resource_tag import ResourceTag
from .. import bp


@bp.route("/resources", methods=["GET"])
def resources():
    if request.args.get('search'):
        resources_pages = Resource.search_by_title_pages(
            title=request.args.get('search'),
            page=int(request.args.get("page", 1)),
            per_page=9,
            tag=request.args.get('tag'),
        )
    else:
        resources_pages = Resource.all_newest_first_pages(
            page=int(request.args.get("page", 1)),
            per_page=9,
            tag=request.args.get('tag'),
        )

    tags = ResourceTag.get_all_tags()

    return render_template(
        bp.tmpl("resources.html"),
        resources=resources_pages.items,
        page=resources_pages.page,
        pages=resources_pages.pages,
        tags=tags
    )
