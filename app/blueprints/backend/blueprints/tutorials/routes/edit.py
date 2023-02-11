import pathlib

from flask import render_template, abort, request, current_app, redirect, url_for
from werkzeug.utils import secure_filename

from app import bigapp, logger
from .. import bp


@bp.route("/edit/<slug>", methods=["GET", "POST"])
def edit(slug):
    tutorial_ = bigapp.model("Tutorial").get_by_slug(slug)

    if not tutorial_:
        return abort(404)

    if request.method == "POST":
        tutorial_tag_membership = bigapp.model("TutorialTagMembership")

        upload_location = pathlib.Path(pathlib.Path(current_app.root_path) / "uploads")
        temp_location = pathlib.Path(pathlib.Path(current_app.root_path) / "temp")

        old_file = upload_location / tutorial_.markdown_file
        new_file = upload_location / f"{request.form.get('slug')}.md"

        edit_values = dict()

        if request.form.get("title") != tutorial_.title:
            logger.debug("Title changed")
            edit_values["title"] = request.form.get("title")

        if request.form.get("slug") != tutorial_.slug:
            logger.debug("Slug changed")
            edit_values["slug"] = request.form.get("slug")
            if old_file.exists():
                logger.debug("Old file exists, renaming")
                old_file.rename(new_file)
                logger.debug(f"{old_file.name} -> {new_file.name}")
                edit_values["markdown_file"] = new_file.name

        if request.form.get("summary") != tutorial_.summary:
            logger.debug("Summary changed")
            edit_values["summary"] = request.form.get("summary")

        files = request.files.getlist("markdown_file")
        files.sort(key=lambda x: x.filename)

        if files[0]:
            logger.debug("New file(s) selected, updating markdown")
            edit_values["markup"] = request.form.get("markup").lstrip("\n")
            edit_values["markdown"] = request.form.get("markdown").lstrip("\n")

            logger.debug("Getting selected files")
            files = request.files.getlist("markdown_file")
            logger.debug(files)

            if old_file.exists():
                logger.debug("Old file exists, deleting")
                old_file.unlink()

            if new_file.exists():
                logger.debug("New file exists, deleting")
                new_file.unlink()

            logger.debug("Creating new file")
            new_file.touch()

            for i, file in enumerate(files):
                temp_save = temp_location / secure_filename(file.filename)

                if temp_save.suffix == ".md":
                    logger.debug(f"Saving temp file {temp_save}")
                    file.save(temp_save)
                with open(new_file, "a") as f:
                    logger.debug(f"Writing to new file {new_file}")
                    f.write(temp_save.read_text())

                logger.debug(f"Deleting temp file {temp_save}")
                temp_save.unlink()

            edit_values["markdown_file"] = new_file.name

        logger.debug(f"Updating tutorial {tutorial_.tutorial_id}")
        tutorial_.update_by_id(
            id_field="tutorial_id",
            id_value=tutorial_.tutorial_id,
            **edit_values
        )

        logger.debug("Processing tags")
        tutorial_tags = request.form.get("tutorial_tags")
        tags_list = tutorial_tags.split(",")
        tags_list.sort()

        def generate_tags():
            for tag in tutorial_.rel_tutorial_tag_membership:
                yield tag.rel_tutorial_tag.tag

        current_tags = [*generate_tags()]
        current_tags.sort()

        if tags_list != current_tags:
            logger.debug("Tags changed")
            logger.debug(f"{tags_list} != {current_tags}")
            logger.debug(f"Deleting tags for tutorial {tutorial_.tutorial_id}")
            tutorial_tag_membership.delete_by_tutorial_id(tutorial_.tutorial_id)
            logger.debug(f"Adding tags for tutorial {tutorial_.tutorial_id}")
            tutorial_tag_membership.process_tag_list(tutorial_.tutorial_id, tags_list)

        return redirect(url_for("backend.tutorials.index"))

    return render_template(bp.tmpl("edit.html"), tutorial=tutorial_)
