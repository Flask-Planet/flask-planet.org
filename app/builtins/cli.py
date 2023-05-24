import random
from getpass import getpass

from flask import Flask

from app.extensions import logger, db, bigapp
from app.globals import pytz_datetime


def loader(app: Flask):
    @app.cli.command("reset-db")
    def re_create_db():
        logger.debug("Dropping and creating database")
        db.drop_all()
        db.create_all()

    @app.cli.command("create-user")
    def re_create_db():
        db.create_all()

        m_user = bigapp.model("User")

        logger.debug(f"Creating user")

        username = input("Enter a username: ")
        password = getpass("Enter a password: ")

        m_user.add_new_user(
            username,
            password,
        )

    @app.cli.command("example-data")
    def example_data():

        user = bigapp.model("User").get_by_username("admin")
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
                markdown=f"Test Summary {i}",
                markup=f"<p>Test Summary {i}</p>",
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

        logger.debug(f"Creating streams")
        m_stream = bigapp.model("Stream")
        for i in range(1, 8):
            random_created = int(f"-{abs(random.randrange(1, 20))}")
            random_schedule = random.randrange(-20, 20)
            m_stream.add_new_stream(
                fk_user_id=user.user_id,
                title=f"Test stream {i}",
                markdown=f"Test stream {i}",
                markup=f"<p>Test stream {i}</p>",
                url_link=f"https://www.twitch.tv/username{i}",
                display_url_link=f"https://www.twitch.tv/username{i}",
                viewable=True,
                schedule=pytz_datetime(days_delta=random_schedule),
                created=pytz_datetime(days_delta=random_created),
            )

        logger.debug(f"Creating news")
        m_news = bigapp.model("News")
        for i in range(1, 25):
            random_release = random.randrange(-20, 20)
            m_news.add_new_article(
                fk_user_id=user.user_id,
                title=f"Test news {i}",
                slug=f"test-news-{i}",
                markdown=f"Test news {i}",
                markup=f"<p>Test news {i}</p>",
                viewable=True,
                release_date=pytz_datetime(days_delta=random_release),
                created=pytz_datetime(),
            )
