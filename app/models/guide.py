from app.models import *
from app.models.__mixins__ import CRUDMixin


class Tutorial(db.Model, CRUDMixin):
    # PriKey
    tutorial_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_user_id = schema.Column(types.Integer, schema.ForeignKey("user.user_id"), nullable=False)

    # Data
    slug = schema.Column(types.String(128), nullable=False, unique=True)
    title = schema.Column(types.String(128), nullable=False)
    summary = schema.Column(types.String(500), nullable=True)
    markup = schema.Column(types.NVARCHAR, nullable=False)
    markdown = schema.Column(types.NVARCHAR, nullable=False)
    markdown_file = schema.Column(types.String(128), default=True)

    # Tracking
    clicks = schema.Column(types.Integer, default=0)
    created = schema.Column(types.DateTime, default=pytz_datetime())

    # Relationships
    rel_user = relationship("User", back_populates="rel_tutorial")

    rel_tutorial_tag_membership = relationship(
        "TutorialTagMembership",
        primaryjoin="Tutorial.tutorial_id==TutorialTagMembership.fk_tutorial_id",
        cascade="all, delete"
    )

    @classmethod
    def get_by_id(cls, tutorial_id):
        return cls.get_by_field('tutorial_id', tutorial_id)

    @classmethod
    def get_by_slug(cls, slug):
        return cls.get_by_field('slug', slug)

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all tutorials newest first...")
        return cls.query.order_by(desc(cls.created)).all()

    @classmethod
    def all_oldest_first(cls):
        return cls.query.order_by(asc(cls.created)).all()

    @classmethod
    def add_new_tutorial(cls, tags: list, **kwargs):
        logger.debug("Adding new tutorial...")
        instance = cls.create(return_instance=True, **kwargs)
        logger.debug("Looping over tags...")
        TutorialTagMembership.process_tag_list(instance.tutorial_id, tags)


class TutorialTag(db.Model, CRUDMixin):
    # PriKey
    tutorial_tag_id = schema.Column(types.Integer, primary_key=True)

    # Data
    tag = schema.Column(types.String(128), nullable=False)

    # Relationships
    rel_tutorial_tag_membership = relationship(
        "TutorialTagMembership",
        primaryjoin="TutorialTag.tutorial_tag_id==TutorialTagMembership.fk_tutorial_tag_id",
        cascade="all, delete"
    )

    @classmethod
    def get_all_tags(cls):
        return db.session.execute(
            select(cls.tag)
        ).scalars().all()

    @classmethod
    def get_by_list_of_tags(cls, tags: list):
        return db.session.execute(
            select(cls).where(cls.tag.in_(tags))
        ).all()

    @classmethod
    def get_by_tag(cls, tag):
        return cls.get_by_field('tag', tag)

    @classmethod
    def add_tag(cls, tag: str):
        return cls.create(return_instance=True, tag=tag)


class TutorialTagMembership(db.Model, CRUDMixin):
    # PriKey
    tutorial_tag_membership_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_tutorial_id = schema.Column(types.Integer, schema.ForeignKey("tutorial.tutorial_id"), nullable=False)
    fk_tutorial_tag_id = schema.Column(types.Integer, schema.ForeignKey("tutorial_tag.tutorial_tag_id"), nullable=False)

    # Relationships
    rel_tutorial = relationship(
        "Tutorial", back_populates="rel_tutorial_tag_membership"
    )
    rel_tutorial_tag = relationship(
        "TutorialTag", back_populates="rel_tutorial_tag_membership"
    )

    @classmethod
    def process_tag_list(cls, tutorial_id: int, tags: list):
        for tag in tags:
            if tag == "" or tag is None or tag == " ":
                continue

            logger.debug(f"Tag: {tag}")
            this_tag = TutorialTag.get_by_tag(tag)

            if not this_tag:
                logger.debug("Tag not found, adding tag...")
                this_tag = TutorialTag.add_tag(tag)

            logger.debug(f"Adding tag membership... {this_tag.tag} - {this_tag.tutorial_tag_id} to {tutorial_id}")

            cls.add_tutorial_tag_membership(tutorial_id, this_tag.tutorial_tag_id)

    @classmethod
    def add_tutorial_tag_membership(cls, tutorial_id: int, tutorial_tag_id: int):
        return cls.create(
            return_instance=True,
            fk_tutorial_id=tutorial_id,
            fk_tutorial_tag_id=tutorial_tag_id
        )

    @classmethod
    def delete_by_tutorial_id(cls, tutorial_id: int):
        db.session.execute(
            delete(cls).where(cls.fk_tutorial_id == tutorial_id)
        )
        db.session.commit()
        return
