from app.models import *
from app.models.__mixins__ import CRUDMixin


class Stream(db.Model, CRUDMixin):
    # PriKey
    stream_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_user_id = schema.Column(types.Integer, schema.ForeignKey("user.user_id"), nullable=False)

    # Data
    title = schema.Column(types.String(128), nullable=False)
    summary = schema.Column(types.String(500), nullable=True)
    image = schema.Column(types.NVARCHAR, nullable=True)
    date = schema.Column(types.Date, nullable=False)
    time = schema.Column(types.Time, nullable=False)
    link = schema.Column(types.String(500), default=True)
    display_link = schema.Column(types.String(500), default=True)

    # Tracking
    clicks = schema.Column(types.Integer, default=0)
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def get_by_id(cls, tutorial_id):
        return cls.get_by_field('tutorial_id', tutorial_id)

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all tutorials newest first...")
        return cls.query.order_by(desc(cls.created)).all()

    @classmethod
    def all_oldest_first(cls):
        return cls.query.order_by(asc(cls.created)).all()
