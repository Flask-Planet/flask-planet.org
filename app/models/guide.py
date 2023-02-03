from app.models import *
from app.models.__mixins__ import CRUDMixin


class Guide(db.Model, CRUDMixin):
    # PriKey
    guide_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_user_id = schema.Column(types.Integer, schema.ForeignKey("user.user_id"), nullable=False)

    # Data
    slug = schema.Column(types.String(128), nullable=False)
    title = schema.Column(types.String(128), nullable=False)
    summary = schema.Column(types.String(256), nullable=False)
    html = schema.Column(types.NVARCHAR, nullable=False)

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
        return cls.query.order_by(desc(cls.created)).all()

    @classmethod
    def all_oldest_first(cls):
        return cls.query.order_by(asc(cls.created)).all()


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
    def get_by_tag(cls, tag):
        return cls.get_by_field('tag', tag)


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
