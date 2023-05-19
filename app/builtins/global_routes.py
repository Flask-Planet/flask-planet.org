from flask import render_template

from app.models.system import System


def loader(app):
    @app.get("/terms-and-conditions")
    def terms_and_conditions():
        system = System.get_first()
        return render_template("theme/terms-and-conditions.html", system=system)

    @app.get("/privacy-policy")
    def privacy_policy():
        system = System.get_first()
        return render_template("theme/privacy-policy.html", system=system)
