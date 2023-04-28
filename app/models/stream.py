from app.models import *


class Stream(db.Model, CrudMixin):
    __id_field__ = 'stream_id'
    __session__ = db.session

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

    # Viewable
    viewable = schema.Column(types.Boolean, default=False)
    auto_viewable = schema.Column(types.Boolean, default=False)
    go_viewable_on = schema.Column(types.DateTime, nullable=True)

    # Tracking
    clicks = schema.Column(types.Integer, default=0)
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def get_by_id(cls, resource_id):
        return cls.read(id_=resource_id)

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all streams newest first...")
        return cls.read(all_rows=True, order_by="created", order_desc=True)

    @classmethod
    def all_oldest_first(cls):
        return cls.read(all_rows=True, order_by="created")
