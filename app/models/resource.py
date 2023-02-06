from app.models import *
from app.models.__mixins__ import CRUDMixin


class Resource(db.Model, CRUDMixin):
    # PriKey
    resource_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_user_id = schema.Column(types.Integer, schema.ForeignKey("user.user_id"), nullable=False)

    # Data
    slug = schema.Column(types.String(128), nullable=False, unique=True)
    title = schema.Column(types.String(128), nullable=False)
    summary = schema.Column(types.String(500), nullable=True)

    # Tracking
    clicks = schema.Column(types.Integer, default=0)
    created = schema.Column(types.DateTime, default=pytz_datetime())

    # # Relationships
    # rel_user = relationship("User", back_populates="rel_tutorial")
    #
    # rel_tutorial_tag_membership = relationship(
    #     "TutorialTagMembership",
    #     primaryjoin="Tutorial.tutorial_id==TutorialTagMembership.fk_tutorial_id",
    #     cascade="all, delete"
    # )

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
