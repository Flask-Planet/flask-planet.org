from datetime import datetime

from flask_sqlalchemy.pagination import Pagination

from app.globals import pytz_datetime_str
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
    markup = schema.Column(types.NVARCHAR, nullable=False)
    markdown = schema.Column(types.NVARCHAR, nullable=False)
    schedule = schema.Column(types.DateTime, nullable=True)
    url_link = schema.Column(types.String(), nullable=True)
    display_url_link = schema.Column(types.String(), nullable=True)

    # Thumbnail
    thumbnail = schema.Column(types.NVARCHAR, nullable=True)

    # Viewable
    viewable = schema.Column(types.Boolean, default=False)
    auto_viewable = schema.Column(types.Boolean, default=False)
    go_viewable_on = schema.Column(types.DateTime, nullable=True)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    def update_thumbnail(self, thumbnail_filename) -> None:
        self.thumbnail = thumbnail_filename
        self.__session__.commit()

    def remove_thumbnail(self) -> None:
        self.thumbnail = ''
        self.__session__.commit()

    @classmethod
    def get_by_id(cls, resource_id):
        return cls.read(id_=resource_id)

    @classmethod
    def streaming_today(cls):
        query = select(cls).where(
            cls.schedule > pytz_datetime(days_delta=-1),  # type: ignore
            cls.schedule < pytz_datetime(days_delta=1)  # type: ignore
        ).order_by(desc(cls.schedule))  # type: ignore
        return cls.__session__.scalars(query).first()

    @classmethod
    def last_stream(cls):
        query = select(cls).order_by(desc(cls.schedule))  # type: ignore
        return cls.__session__.scalars(query).first()

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all streams newest first...")
        return cls.read(all_rows=True, order_by="created", order_desc=True)

    @classmethod
    def all_newest_schedule_first(cls):
        logger.debug("Getting all streams newest first...")
        return cls.read(all_rows=True, order_by="schedule", order_desc=True)

    @classmethod
    def newest_upcoming(cls):
        logger.debug("Getting stream newest upcoming...")
        today = datetime.strptime(pytz_datetime_str(mask="%Y-%m-%d"), "%Y-%m-%d")
        query = select(cls).order_by(desc(cls.schedule)).where(cls.schedule >= today)  # type: ignore
        result = cls.__session__.scalars(query).all()
        return result

    @classmethod
    def most_recent_streams(cls):
        logger.debug("Getting past streams...")
        today = datetime.strptime(pytz_datetime_str(mask="%Y-%m-%d"), "%Y-%m-%d")
        week_ago = datetime.strptime(pytz_datetime_str(mask="%Y-%m-%d", days_delta=-7), "%Y-%m-%d")
        query = select(cls).order_by(
            desc(cls.schedule)  # type: ignore
        ).where(cls.schedule < today, cls.schedule > week_ago, cls.viewable).limit(4)  # type: ignore
        result = cls.__session__.scalars(query).all()
        return result

    @classmethod
    def past_streams(cls):
        logger.debug("Getting past streams...")
        return cls.read(order_by="schedule", order_desc=True, _auto_output=False).first()

    @classmethod
    def all_oldest_first(cls):
        return cls.read(all_rows=True, order_by="created")

    @classmethod
    def search_by_title_pages(cls, title, page: int = 1, per_page: int = 20) -> Pagination:
        query = select(cls).order_by(desc(cls.schedule)).where(cls.title.ilike(f"%{title}%"))  # type: ignore
        return db.paginate(query, page=page, per_page=per_page)

    @classmethod
    def all_schedule_first_pages(cls, page: int = 1, per_page: int = 20) -> Pagination:
        query = select(cls).order_by(desc(cls.schedule))  # type: ignore
        logger.debug("Getting all streams newest first...")
        return db.paginate(query, page=page, per_page=per_page)

    @classmethod
    def add_new_stream(cls, **kwargs):
        logger.debug("Adding new stream...")
        return cls.create(values=kwargs, wash_attributes=True)
