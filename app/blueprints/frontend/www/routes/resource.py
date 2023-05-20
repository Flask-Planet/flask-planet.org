from flask import abort, render_template, request

from app.models.resource import Resource
from app.models.resource_click import ResourceClick
from app.models.resource_page import ResourcePage
from .. import bp


@bp.route("/resources/<slug>/", methods=["GET"])
def resource(slug):
    resource_ = Resource.get_by_slug(slug)
    if not resource_:
        return abort(404)

    ResourceClick.add_resource_click(resource_.resource_id)

    url_args = {}

    if "page" in request.args:
        url_args["page"] = request.args["page"]
    if "search" in request.args:
        url_args["search"] = request.args["search"]
    if "tag" in request.args:
        url_args["tag"] = request.args["tag"]

    return render_template(bp.tmpl("resource.html"), resource=resource_, url_args=url_args)


@bp.route("/resources/<slug>/<filename>", methods=["GET"])
def resource_page(slug, filename):
    resource_ = Resource.get_by_slug(slug)
    if not resource_:
        return abort(404)

    page = ResourcePage.get_by_og_filename(filename)
    ResourceClick.add_resource_click(resource_.resource_id)

    url_args = {}

    if "page" in request.args:
        url_args["page"] = request.args["page"]
    if "search" in request.args:
        url_args["search"] = request.args["search"]
    if "tag" in request.args:
        url_args["tag"] = request.args["tag"]

    return render_template(bp.tmpl("resource.html"), resource=resource_, page=page, filename=filename,
                           url_args=url_args)
