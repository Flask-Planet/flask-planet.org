from flask import session, redirect, url_for

from .. import bp


@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("backend.login"))
