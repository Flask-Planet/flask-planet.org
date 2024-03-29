from datetime import datetime

import mistune
from flask import render_template, abort, request, redirect, url_for, flash
from flask_bigapp.security import login_check

from app import logger
from app.globals import HighlightRenderer
from app.models.resource import Resource
from app.models.resource_tag_membership import ResourceTagMembership
from .. import bp


@bp.route("/edit/<resource_id>", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def edit(resource_id):
    resource_ = Resource.get_by_id(resource_id)
    if not resource_:
        return abort(404)

    if request.method == "POST":
        logger.debug(f"Updating resource {resource_.resource_id}")

        if request.form.get("go_viewable_on") != "":
            try:
                go_viewable_on = datetime.strptime(request.form.get("go_viewable_on", ''), "%Y-%m-%d")
            except ValueError:
                go_viewable_on = None
        else:
            go_viewable_on = None

        markdown = request.form.get("markdown")
        markdown_processor = mistune.create_markdown(renderer=HighlightRenderer())
        markup = markdown_processor(markdown)

        Resource.update(
            values={
                "slug": request.form.get("slug"),
                "title": request.form.get("title"),
                "markup": markup,
                "markdown": markdown,
                "viewable": True if request.form.get("viewable") == 'true' else False,
                "auto_viewable": True if request.form.get("auto_viewable") == 'true' else False,
                "go_viewable_on": go_viewable_on
            },
            id_=resource_id,
        )

        logger.debug("Resource updated")

        logger.debug("Processing tags")
        resource_tags = request.form.get("resource_tags")

        tags_list = resource_tags.split(",")
        tags_list.sort()

        def generate_tags():
            for tag in resource_.rel_resource_tag_membership:
                yield tag.rel_resource_tag.tag

        current_tags = [*generate_tags()]
        current_tags.sort()

        if tags_list != current_tags:
            logger.debug("Tags changed")
            logger.debug(f"{tags_list} != {current_tags}")
            logger.debug(f"Deleting tags for resource {resource_id}")
            ResourceTagMembership.delete_by_resource_id(resource_id)
            if resource_tags:
                logger.debug(f"Adding tags for resource {resource_id}")
                ResourceTagMembership.process_tag_list(resource_id, tags_list)

        flash("Resource updated!")
        return redirect(url_for("backend.resources.edit", resource_id=resource_id))

    return render_template(bp.tmpl("edit.html"), resource=resource_)
