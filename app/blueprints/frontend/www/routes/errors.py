from flask import render_template

from .. import bp


@bp.route("/error/<code>", methods=["GET"])
def error_styles(code):
    return render_template(f"theme/errors/{code}.html")
