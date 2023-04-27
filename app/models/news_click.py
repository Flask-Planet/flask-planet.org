from app.models import *


class NewsClick(db.Model, CrudMixin):
    __id_field__ = 'news_click_id'
    __session__ = db.session

    # PriKey
    news_click_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_news_id = schema.Column(types.Integer, schema.ForeignKey("news.news_id"), nullable=False)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def add_news_click(cls, news_id: int):
        return cls.create(values={
            'fk_news_id': news_id,
            'created': pytz_datetime()
        })
