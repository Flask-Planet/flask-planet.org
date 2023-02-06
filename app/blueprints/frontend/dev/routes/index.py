import random
from time import sleep

from flask import render_template

from app import bigapp, db, logger
from app.globals import pytz_datetime
from .. import bp


@bp.route("/re-create-db", methods=["GET"])
def index():
    logger.debug("Dropping and creating database")
    db.drop_all()
    db.create_all()

    m_user = bigapp.model("User")
    m_tutorial_tag = bigapp.model("TutorialTag")
    m_tutorial_tag_membership = bigapp.model("TutorialTagMembership")

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
        logger.debug(f"Creating tag {tag}")
        m_tutorial_tag.create(tag=tag)

    logger.debug(f"Creating admin user")
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
        logger.debug(f"Creating tutorial {i}")
        tutorial = bigapp.model("Tutorial").create(
            return_instance=True,
            fk_user_id=user.user_id,
            slug=f"test-tutorial-{i}",
            title=f"Test Tutorial {i}",
            summary=f"Test Summary {i}",
            markup=f"<h1>Test HTML {i}</h1>",
            markdown=f"# Test HTML {i}",
            markdown_file=f"test-tutorial-{i}.md",
            created=pytz_datetime(),
        )
        pick_random_amount_from_list = random.sample(list_of_tags, random.randint(1, 3))
        for value in pick_random_amount_from_list:
            tutorial_tag = m_tutorial_tag.get_by_tag(value)
            m_tutorial_tag_membership.create(
                fk_tutorial_id=tutorial.tutorial_id,
                fk_tutorial_tag_id=tutorial_tag.tutorial_tag_id,
            )
        sleep(5)

    return render_template(bp.tmpl("index.html"))
