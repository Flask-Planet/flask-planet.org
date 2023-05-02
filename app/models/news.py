from flask_sqlalchemy.pagination import Pagination

from app.models import *


class News(db.Model, CrudMixin):
    __id_field__ = 'news_id'
    __session__ = db.session

    # PriKey
    news_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_user_id = schema.Column(types.Integer, schema.ForeignKey("user.user_id"), nullable=False)

    # Data
    title = schema.Column(types.String(128), nullable=False)
    thumbnail = schema.Column(types.NVARCHAR, nullable=True)
    markup = schema.Column(types.NVARCHAR, nullable=False)
    markdown = schema.Column(types.NVARCHAR, nullable=False)
    markdown_og_filename = schema.Column(types.String(512), default=True)
    markdown_safe_filename = schema.Column(types.String(512), default=True)

    # Author
    author = schema.Column(types.String(128), nullable=True)
    author_link = schema.Column(types.String(1024), nullable=True)

    # Viewable
    viewable = schema.Column(types.Boolean, default=False)
    viewable_after = schema.Column(types.DateTime, nullable=True)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def get_by_id(cls, news_id):
        return cls.read(id_=news_id)

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all news newest first...")
        return cls.read(all_rows=True, order_by="viewable_on", order_desc=True)

    @classmethod
    def all_oldest_first(cls):
        return cls.read(all_rows=True, order_by="created")

    @classmethod
    def search_by_title_pages(cls, title, page: int = 1, per_page: int = 20) -> Pagination:
        query = select(cls).order_by(desc(cls.viewable_on)).where(cls.title.ilike(f"%{title}%"))  # type: ignore
        return db.paginate(query, page=page, per_page=per_page)

    @classmethod
    def all_newest_first_pages(cls, page: int = 1, per_page: int = 20) -> Pagination:
        query = select(cls).order_by(desc(cls.viewable_on))  # type: ignore
        logger.debug("Getting all news viewable_on first...")
        return db.paginate(query, page=page, per_page=per_page)
