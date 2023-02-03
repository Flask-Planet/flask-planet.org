import random
from time import sleep

from flask import render_template

from app import bigapp, db
from app.globals import pytz_datetime
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    db.drop_all()
    db.create_all()

    m_user = bigapp.model("User")
    m_guide = bigapp.model("Guide")
    m_guide_tag = bigapp.model("GuideTag")
    m_guide_tag_membership = bigapp.model("GuideTagMembership")

    list_of_tags = [
        "Flask",
        "Flask-SQLAlchemy",
        "Flask-Login",
        "Flask-Admin",
        "Flask-RESTful",
        "Flask-BigApp",
        "Python",
        "SQLAlchemy",
        "JavaScript",
        "AlpineJS",
        "Bootstrap",
    ]

    for tag in list_of_tags:
        m_guide_tag.create(tag=tag)

    user = m_user.create(
        return_instance=True,
        username="admin",
        password="admin",
        salt="1234",
        private_key="1234",
        display_name="Admin",
        disabled=False,
    )

    for i in range(1, 10):
        guide = m_guide.create(
            return_instance=True,
            fk_user_id=user.user_id,
            slug=f"test-guide-{i}",
            title=f"Test Guide {i}",
            summary=f"Test Summary {i}",
            html=f"<p>Test HTML {i}</p>",
            created=pytz_datetime(),
        )
        pick_random_amount_from_list = random.sample(list_of_tags, random.randint(1, 3))
        for value in pick_random_amount_from_list:
            guide_tag = m_guide_tag.get_by_tag(value)
            m_guide_tag_membership.create(
                fk_guide_id=guide.guide_id,
                fk_guide_tag_id=guide_tag.guide_tag_id,
            )
        sleep(5)

    return render_template(bp.tmpl("index.html"))
