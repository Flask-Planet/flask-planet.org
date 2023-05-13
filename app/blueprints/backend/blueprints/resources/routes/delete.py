from flask import redirect, url_for
from flask_bigapp.security import login_check

from app.models.resource import Resource
from app.models.resource_click import ResourceClick
from app.models.resource_page import ResourcePage
from app.models.resource_tag_membership import ResourceTagMembership
from .. import bp


@bp.route("/delete/<resource_id>", methods=["GET"])
@login_check("logged_in", "backend.login")
def delete(resource_id):
    ResourceTagMembership.delete_by_resource_id(resource_id)
    ResourceClick.delete_by_resource_id(resource_id)
    ResourcePage.delete_by_resource_id(resource_id)
    Resource.delete(id_=resource_id)
    return redirect(url_for('backend.resources.index'))
