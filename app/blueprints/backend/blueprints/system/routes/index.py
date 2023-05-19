import mistune
from flask import render_template, url_for, redirect, request
from flask_bigapp.security import login_check

from app.globals import HighlightRenderer
from app.models.system import System
from .. import bp


@bp.route("/", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def index():
    system = System.get_first()

    if request.method == "POST":
        terms_and_conditions_markdown = request.form.get("terms_and_conditions_markdown", '')
        privacy_policy_markdown = request.form.get("privacy_policy_markdown", '')

        markdown_processor = mistune.create_markdown(renderer=HighlightRenderer())

        terms_and_conditions_markup = markdown_processor(terms_and_conditions_markdown)
        privacy_policy_markup = markdown_processor(privacy_policy_markdown)

        System.update(
            values={
                "terms_and_conditions_markdown": terms_and_conditions_markdown,
                "terms_and_conditions_markup": terms_and_conditions_markup,
                "privacy_policy_markdown": privacy_policy_markdown,
                "privacy_policy_markup": privacy_policy_markup,
            },
            id_=system.system_id,
        )
        return redirect(url_for("backend.system.index"))

    if system is None:
        System.create({
            "terms_and_conditions_markdown": "",
            "terms_and_conditions_markup": "",
            "privacy_policy_markdown": "",
            "privacy_policy_markup": "",
        })
        return redirect(url_for("backend.system.index"))

    return render_template(bp.tmpl("index.html"), system=system)
