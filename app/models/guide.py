from app.models import *
from app.models.__mixins__ import CRUDMixin


class Guide(db.Model, CRUDMixin):
    # PriKey
    guide_id = schema.Column(types.Integer, primary_key=True)

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
    rel_user = relationship("User", back_populates="rel_guide")

    rel_guide_tag_membership = relationship(
        "GuideTagMembership",
        primaryjoin="Guide.guide_id==GuideTagMembership.fk_guide_id",
        cascade="all, delete"
    )

    @classmethod
    def get_by_id(cls, guide_id):
        return cls.get_by_field('guide_id', guide_id)

    @classmethod
    def get_by_slug(cls, slug):
        return cls.get_by_field('slug', slug)

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all guides newest first...")
        return cls.query.order_by(desc(cls.created)).all()

    @classmethod
    def all_oldest_first(cls):
        return cls.query.order_by(asc(cls.created)).all()

    @classmethod
    def add_new_guide(cls, tags: list, **kwargs):
        logger.debug("Adding new guide...")
        instance = cls.create(return_instance=True, **kwargs)
        logger.debug("Looping over tags...")
        GuideTagMembership.process_tag_list(instance.guide_id, tags)


class GuideTag(db.Model, CRUDMixin):
    # PriKey
    guide_tag_id = schema.Column(types.Integer, primary_key=True)

    # Data
    tag = schema.Column(types.String(128), nullable=False)

    # Relationships
    rel_guide_tag_membership = relationship(
        "GuideTagMembership",
        primaryjoin="GuideTag.guide_tag_id==GuideTagMembership.fk_guide_tag_id",
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


class GuideTagMembership(db.Model, CRUDMixin):
    # PriKey
    guide_tag_membership_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_guide_id = schema.Column(types.Integer, schema.ForeignKey("guide.guide_id"), nullable=False)
    fk_guide_tag_id = schema.Column(types.Integer, schema.ForeignKey("guide_tag.guide_tag_id"), nullable=False)

    # Relationships
    rel_guide = relationship(
        "Guide", back_populates="rel_guide_tag_membership"
    )
    rel_guide_tag = relationship(
        "GuideTag", back_populates="rel_guide_tag_membership"
    )

    @classmethod
    def process_tag_list(cls, guide_id: int, tags: list):
        for tag in tags:
            if tag == "" or tag is None or tag == " ":
                continue

            logger.debug(f"Tag: {tag}")
            this_tag = GuideTag.get_by_tag(tag)

            if not this_tag:
                logger.debug("Tag not found, adding tag...")
                this_tag = GuideTag.add_tag(tag)

            logger.debug(f"Adding tag membership... {this_tag.tag} - {this_tag.guide_tag_id} to {guide_id}")

            cls.add_guide_tag_membership(guide_id, this_tag.guide_tag_id)

    @classmethod
    def add_guide_tag_membership(cls, guide_id: int, guide_tag_id: int):
        return cls.create(
            return_instance=True,
            fk_guide_id=guide_id,
            fk_guide_tag_id=guide_tag_id
        )

    @classmethod
    def delete_by_guide_id(cls, guide_id: int):
        db.session.execute(
            delete(cls).where(cls.fk_guide_id == guide_id)
        )
        db.session.commit()
        return
