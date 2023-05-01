from flask import render_template, request, session, url_for, redirect, flash
from flask_bigapp.security import login_check

from app.models.user import User
from .. import bp


@bp.route("/login", methods=["GET", "POST"])
@login_check("logged_in", "backend.index", redirect_on_value=True)
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        auth = User.check_login(username, password)

        if auth:
            session['logged_in'] = True
            session['user_id'] = auth.user_id
            session['username'] = auth.username
            return redirect(url_for("backend.index"))

        else:
            flash("Invalid username or password")
            return redirect(url_for("backend.index"))

    return render_template(
        bp.tmpl("login.html")
    )
