from flask import render_template, session, request, url_for, redirect, flash
from flask_bigapp.security import login_check

from app.models.user import User
from .. import bp


@bp.route("/", methods=["GET", "POST"])
@login_check("logged_in", "backend.login")
def index():
    user = User.get_by_id(session.get("user_id"))
    if request.method == "POST":
        username = request.form.get("username")
        author = request.form.get("author")
        author_link = request.form.get("author_link")

        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        user.username = username
        user.author = author
        user.author_link = author_link
        user.save()

        if new_password != '':
            if len(new_password) < 8:
                flash("Password must be at least 8 characters long")
                return redirect(url_for("backend.account.index"))
            if new_password == confirm_new_password:
                user.set_new_password(new_password)

        return redirect(url_for("backend.account.index"))

    return render_template(
        bp.tmpl("index.html"),
        user=user
    )
