import random
from time import sleep

from flask import render_template
from flask_bigapp import Auth

from app import bigapp, db, logger
from app.globals import pytz_datetime
from .. import bp


@bp.route("/re-create-db", methods=["GET"])
def index():
    logger.debug("Dropping and creating database")
    db.drop_all()
    db.create_all()

    m_user = bigapp.model("User")
    m_resource_tag = bigapp.model("ResourceTag")
    m_resource_tag_membership = bigapp.model("ResourceTagMembership")

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
        m_resource_tag.create(tag=tag)

    logger.debug(f"Creating admin user")

    salt = Auth.generate_salt()
    password = Auth.sha_password("password", salt)

    user = m_user.create(
        return_instance=True,
        username="admin",
        password=password,
        salt=salt,
        private_key="1234",
        display_name="Admin",
        disabled=False,
    )

    for i in range(1, 10):
        logger.debug(f"Creating resource {i}")
        resource = bigapp.model("Resource").create(
            return_instance=True,
            fk_user_id=user.user_id,
            slug=f"test-resource-{i}",
            title=f"Test Resource {i}",
            summary=f"Test Summary {i}",
            created=pytz_datetime(),
        )
        pick_random_amount_from_list = random.sample(list_of_tags, random.randint(1, 3))
        for value in pick_random_amount_from_list:
            resource_tag = m_resource_tag.get_by_tag(value)
            m_resource_tag_membership.create(
                fk_resource_id=resource.resource_id,
                fk_resource_tag_id=resource_tag.resource_tag_id,
            )
        sleep(5)

    return render_template(bp.tmpl("index.html"))
