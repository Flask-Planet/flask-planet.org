import random

from flask import Flask

from app.extensions import logger, db, bigapp
from app.globals import pytz_datetime


def loader(app: Flask):
    @app.cli.command("first-run")
    def re_create_db():
        db.init_app(app)
        bigapp.init_app(app)

        bigapp.import_models(from_folder="models")

        logger.debug("Dropping and creating database")
        db.drop_all()
        db.create_all()

        m_user = bigapp.model("User")

        logger.debug(f"Creating admin user")

        user = m_user.add_new_user(
            "admin",
            "password",
            "Admin",
            "admin.link",
        )

        @app.cli.command("example-data")
        def example_data():
            db.init_app(app)
            bigapp.init_app(app)

            bigapp.import_models(from_folder="models")

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
                m_resource_tag.add_tag(tag=tag)

            for i in range(1, 25):
                logger.debug(f"Creating resource {i}")
                resource = bigapp.model("Resource").add_new_resource(
                    fk_user_id=user.user_id,
                    slug=f"test-resource-{i}",
                    title=f"Test resource {i}",
                    summary=f"<p>Test Summary {i}</p>",
                    author=user.author,
                    author_link=user.author_link,
                    viewable=True,
                    created=pytz_datetime(),
                )
                pick_random_amount_from_list = random.sample(list_of_tags, random.randint(1, 3))
                for value in pick_random_amount_from_list:
                    resource_tag = m_resource_tag.get_by_tag(value)
                    m_resource_tag_membership.add_resource_tag_membership(
                        resource.resource_id, resource_tag.resource_tag_id,
                    )
