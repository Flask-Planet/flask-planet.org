import os

from flask import render_template, request, session, url_for, redirect, flash, abort
from flask_bigapp.security import login_check

from app.extensions import logger
from app.models.user import User
from .. import bp


@bp.route("/login", methods=["GET", "POST"])
@login_check("logged_in", "backend.index", redirect_on_value=True)
def login():
    if os.environ.get("ALLOWED_IPS"):
        ips = os.environ.get("ALLOWED_IPS").split(",")
        logger.debug(f"Checking allowed IPs: {ips}")
        if request.remote_addr not in ips:
            logger.debug(f"Refusing access to: {request.remote_addr}")
            return abort(403)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        auth = User.check_login(username, password)

        if auth:
            session['logged_in'] = True
            session['user_id'] = auth.user_id
            session['username'] = auth.username
            flash("Logged in successfully!")
            return redirect(url_for("backend.index"))

        else:
            flash("Invalid username or password")
            return redirect(url_for("backend.index"))

    return render_template(
        bp.tmpl("login.html")
    )
